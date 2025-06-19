import os
import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sqlalchemy import create_engine, Column, Integer, Float, Table, MetaData
from sqlalchemy.orm import sessionmaker
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

app = FastAPI(title="Continual ML API")

# Security
security = HTTPBearer()
API_KEY = os.getenv("API_KEY", "default-key-change-me")

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

# Database setup
DATABASE_URL = "sqlite:///./ml_data.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Dataset table
dataset_table = Table(
    'datasets',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('feature1', Float),
    Column('feature2', Float),
    Column('target', Integer)
)

metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Global model variable and performance tracking
current_model = None
model_performance = 0.0
PERFORMANCE_THRESHOLD = float(os.getenv("PERFORMANCE_THRESHOLD", "0.8"))

class PredictionInput(BaseModel):
    feature1: float
    feature2: float

@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok", "message": "API is running"}

@app.post("/generate")
def generate_dataset(api_key: str = Depends(verify_api_key)):
    """Generate a linear dataset with 2 features and store in DB"""
    try:
        logger.info("Starting dataset generation")
        
        # Generate dataset
        X, y = make_classification(n_samples=1000, n_features=2, n_redundant=0, 
                                 n_informative=2, n_clusters_per_class=1, random_state=42)
        
        # Store in database
        session = SessionLocal()
        
        # Clear existing data
        session.execute(dataset_table.delete())
        
        # Insert new data
        for i in range(len(X)):
            session.execute(dataset_table.insert().values(
                feature1=float(X[i][0]),
                feature2=float(X[i][1]),
                target=int(y[i])
            ))
        
        session.commit()
        session.close()
        
        logger.success(f"Dataset generated successfully with {len(X)} samples")
        return {"message": "Dataset generated and stored successfully", "samples": len(X)}
    except Exception as e:
        logger.error(f"Dataset generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrain")
def retrain_model(api_key: str = Depends(verify_api_key)):
    """Retrain the model with hot retraining, tracked by MLflow"""
    global current_model, model_performance
    
    try:
        logger.info("Starting model retraining process")
        
        # Check current performance first
        if current_model is not None and model_performance >= PERFORMANCE_THRESHOLD:
            logger.info(f"Current model performance ({model_performance:.3f}) is above threshold ({PERFORMANCE_THRESHOLD}). Skipping retraining.")
            return {
                "message": "Retraining skipped - performance above threshold", 
                "current_performance": model_performance,
                "threshold": PERFORMANCE_THRESHOLD
            }
        
        # Load data from database
        session = SessionLocal()
        result = session.execute(dataset_table.select()).fetchall()
        session.close()
        
        if not result:
            logger.error("No data available for training")
            raise HTTPException(status_code=400, detail="No data available for training")
        
        # Prepare data
        X = np.array([[row.feature1, row.feature2] for row in result])
        y = np.array([row.target for row in result])
        
        logger.info(f"Training with {len(X)} samples")
        
        # Start MLflow tracking (moved here to prevent hanging during import)
        mlflow.set_experiment("continual_ml")
        with mlflow.start_run():
            # Train model
            model = LogisticRegression(random_state=42)
            model.fit(X, y)
            
            # Log metrics
            score = model.score(X, y)
            mlflow.log_metric("accuracy", score)
            mlflow.log_param("model_type", "LogisticRegression")
            mlflow.log_param("n_samples", len(X))
            mlflow.log_param("performance_threshold", PERFORMANCE_THRESHOLD)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            # Update global model and performance
            current_model = model
            model_performance = score
            
            logger.success(f"Model retrained successfully with accuracy: {score:.3f}")
            return {"message": "Model retrained successfully", "accuracy": score}
            
    except Exception as e:
        logger.error(f"Model retraining failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict(input_data: PredictionInput, api_key: str = Depends(verify_api_key)):
    """Make prediction using logistic regression on the latest dataset"""
    global current_model
    
    if current_model is None:
        logger.warning("Prediction attempted without trained model")
        raise HTTPException(status_code=400, detail="No model available. Please retrain first.")
    
    try:
        # Prepare input
        X = np.array([[input_data.feature1, input_data.feature2]])
        
        # Make prediction
        prediction = current_model.predict(X)[0]
        probability = current_model.predict_proba(X)[0].max()
        
        logger.info(f"Prediction made: {prediction} with probability {probability:.3f}")
        
        return {
            "prediction": int(prediction),
            "probability": float(probability)
        }
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-status")
def get_model_status():
    """Get current model status and performance"""
    global current_model, model_performance
    return {
        "model_trained": current_model is not None,
        "performance": model_performance,
        "threshold": PERFORMANCE_THRESHOLD,
        "needs_retraining": model_performance < PERFORMANCE_THRESHOLD
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application")
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", 8000))
    uvicorn.run(app, host=host, port=port) 