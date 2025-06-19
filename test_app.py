import pytest
from fastapi.testclient import TestClient
from app import app, current_model
import os

client = TestClient(app)

# Test API key
TEST_API_KEY = os.getenv("API_KEY", "default-key-change-me")
AUTH_HEADERS = {"Authorization": f"Bearer {TEST_API_KEY}"}

def test_health():
    """Test the health endpoint (no auth required)"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "API is running" in data["message"]

def test_model_status():
    """Test the model status endpoint (no auth required)"""
    response = client.get("/model-status")
    assert response.status_code == 200
    data = response.json()
    assert "model_trained" in data
    assert "performance" in data
    assert "threshold" in data
    assert "needs_retraining" in data

def test_generate_dataset():
    """Test dataset generation endpoint"""
    response = client.post("/generate", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "Dataset generated and stored successfully" in data["message"]
    assert data["samples"] == 1000

def test_generate_dataset_without_auth():
    """Test dataset generation without authentication should fail"""
    response = client.post("/generate")
    assert response.status_code == 403

def test_retrain_model():
    """Test model retraining endpoint"""
    # First generate a dataset
    client.post("/generate", headers=AUTH_HEADERS)
    
    # Then retrain
    response = client.post("/retrain", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    # Could be either successful retraining or skipped due to performance
    assert "accuracy" in data or "current_performance" in data

def test_retrain_without_auth():
    """Test retraining without authentication should fail"""
    response = client.post("/retrain")
    assert response.status_code == 403

def test_predict_without_model():
    """Test prediction without a trained model should fail"""
    from app import current_model
    import app
    
    # Save current model state and reset
    original_model = app.current_model
    app.current_model = None
    
    try:
        response = client.post("/predict", json={"feature1": 1.0, "feature2": 2.0}, headers=AUTH_HEADERS)
        assert response.status_code == 400
        data = response.json()
        assert "No model available" in data["detail"]
    finally:
        # Restore original model state to avoid affecting other tests
        app.current_model = original_model

def test_predict_with_model():
    """Test prediction with a trained model"""
    # First generate dataset and train model
    client.post("/generate", headers=AUTH_HEADERS)
    client.post("/retrain", headers=AUTH_HEADERS)
    
    # Now test prediction
    response = client.post("/predict", json={"feature1": 1.0, "feature2": 2.0}, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1

def test_predict_without_auth():
    """Test prediction without authentication should fail"""
    response = client.post("/predict", json={"feature1": 1.0, "feature2": 2.0})
    assert response.status_code == 403

def test_predict_invalid_input():
    """Test prediction with invalid input"""
    response = client.post("/predict", json={"feature1": "invalid"}, headers=AUTH_HEADERS)
    assert response.status_code == 422  # Validation error 