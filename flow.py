import os
import random
import requests
from prefect import flow, task
from prefect.logging import get_run_logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "default-key-change-me")
PERFORMANCE_THRESHOLD = float(os.getenv("PERFORMANCE_THRESHOLD", "0.8"))

def send_discord_embed(message, title="Continual ML Automation", color=0x00ff00):
    """Send structured message to Discord webhook"""
    if not DISCORD_WEBHOOK_URL or "REPLACE_WITH_YOUR_WEBHOOK_URL" in DISCORD_WEBHOOK_URL:
        print(f"Discord notification: {title} - {message}")
        return
    
    try:
        embed = {
            "title": title,
            "description": message,
            "color": color,
            "timestamp": "2024-01-01T00:00:00.000Z"
        }
        
        data = {
            "embeds": [embed],
            "username": "Continual ML Bot"
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
        if response.status_code == 204:
            print(f"Discord notification sent: {message}")
        else:
            print(f"Discord notification failed: {response.status_code}")
            
    except Exception as e:
        print(f"Discord notification error: {str(e)}")

@task(retries=2, retry_delay_seconds=1)
def check_model_performance():
    """Check current model performance and determine if retraining is needed"""
    logger = get_run_logger()
    
    try:
        # Get current model status
        response = requests.get(f"{API_BASE_URL}/model-status", timeout=10)
        if response.status_code != 200:
            logger.warning("Could not get model status")
            # Simulate performance check with random value for demo
            performance = random.random()
        else:
            status = response.json()
            performance = status.get("performance", 0.0)
            model_trained = status.get("model_trained", False)
            
            if not model_trained:
                logger.info("No model found - triggering initial training")
                send_discord_embed("🤖 No model detected. Initiating first-time training.", "Initial Setup", 0xffa500)
                raise Exception("No model available - retraining required")
        
        logger.info(f"Current model performance: {performance:.3f}, threshold: {PERFORMANCE_THRESHOLD}")
        
        # Check if performance has degraded below threshold
        if performance < PERFORMANCE_THRESHOLD:
            logger.warning(f"Model drift detected! Performance {performance:.3f} < threshold {PERFORMANCE_THRESHOLD}")
            send_discord_embed(
                f"🔄 **Model drift detected!**\n"
                f"• Current performance: {performance:.3f}\n"
                f"• Threshold: {PERFORMANCE_THRESHOLD}\n"
                f"• Action: Retraining initiated",
                "Model Drift Alert",
                0xff6b6b
            )
            raise Exception("Model performance below threshold - retraining required")
        else:
            logger.info("Model performance is above threshold - no retraining needed")
            send_discord_embed(
                f"✅ **Model performance OK**\n"
                f"• Current performance: {performance:.3f}\n"
                f"• Threshold: {PERFORMANCE_THRESHOLD}\n"
                f"• Status: No action required",
                "Performance Check",
                0x51cf66
            )
            return "ok"
            
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        # Fallback to random check if API is unavailable
        performance = random.random()
        if performance < 0.5:
            send_discord_embed(
                f"⚠️ **Simulated drift detected** (API unavailable)\n"
                f"• Simulated performance: {performance:.3f}\n"
                f"• Action: Demonstration retraining",
                "Demo Mode",
                0xffd43b
            )
            raise Exception("Simulated model drift for demonstration")
        else:
            send_discord_embed("✅ Simulated performance check OK (API unavailable)", "Demo Mode", 0x51cf66)
            return "ok"

@task(retries=1, retry_delay_seconds=2)
def trigger_retraining():
    """Trigger model retraining via internal function"""
    logger = get_run_logger()
    
    try:
        # Import and call the internal retraining function
        from app import retrain_model_internal
        
        logger.info("Starting automated model retraining")
        result = retrain_model_internal()
        
        accuracy = result.get("accuracy", 0.0)
        logger.success(f"Model retraining completed successfully with accuracy: {accuracy:.3f}")
        
        send_discord_embed(
            f"🎉 **Model retraining successful!**\n"
            f"• New accuracy: {accuracy:.3f}\n"
            f"• Training samples: Auto-generated\n"
            f"• MLflow: Experiment logged\n"
            f"• Status: Ready for predictions",
            "Retraining Success",
            0x69db7c
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Model retraining failed: {str(e)}")
        send_discord_embed(
            f"❌ **Model retraining failed!**\n"
            f"• Error: {str(e)}\n"
            f"• Action: Will retry on next check\n"
            f"• Status: Manual intervention may be needed",
            "Retraining Failed",
            0xff5630
        )
        raise

@task(retries=2, retry_delay_seconds=1)  
def ensure_dataset_exists():
    """Ensure training dataset exists before retraining"""
    logger = get_run_logger()
    
    try:
        # Try to generate dataset if none exists
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.post(f"{API_BASE_URL}/generate", headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            samples = result.get("samples", 0)
            logger.info(f"Dataset ensured with {samples} samples")
            send_discord_embed(f"📊 Training dataset ready with {samples} samples", "Dataset Check", 0x339af0)
        else:
            logger.warning(f"Dataset generation failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        logger.warning(f"Could not connect to API for dataset generation: {str(e)}")
        # This is OK - the internal retraining function will handle missing datasets

@flow(log_prints=True)
def continuous_ml_pipeline():
    """Main automated continuous learning pipeline"""
    logger = get_run_logger()
    
    logger.info("🚀 Starting Continual ML automated pipeline")
    
    try:
        # Check if retraining is needed
        check_model_performance()
        
        # If we get here, no retraining is needed
        logger.info("✅ Model performance check completed - no action required")
        
    except Exception as e:
        # Performance check failed, retraining is needed
        logger.info("🔄 Performance check triggered retraining workflow")
        
        # Ensure dataset exists
        ensure_dataset_exists()
        
        # Perform retraining
        trigger_retraining()
        
        logger.success("🎯 Automated retraining workflow completed successfully")

if __name__ == "__main__":
    # Send startup notification
    send_discord_embed(
        "🚀 **Continual ML System Started**\n"
        "• Automated monitoring: Active\n"
        "• Performance threshold: 80%\n"
        "• Check interval: Every 30 seconds\n"
        "• Features: Auto-retraining, Discord alerts",
        "System Startup",
        0x74c0fc
    )
    
    print("🤖 Starting Continual ML automated monitoring...")
    print(f"📊 Performance threshold: {PERFORMANCE_THRESHOLD}")
    print(f"🔔 Discord notifications: {'Enabled' if DISCORD_WEBHOOK_URL and 'REPLACE_WITH_YOUR_WEBHOOK_URL' not in DISCORD_WEBHOOK_URL else 'Demo mode'}")
    print("⏰ Checking every 30 seconds...")
    
    # Start the automated pipeline
    continuous_ml_pipeline.serve(
        name="continual-ml-automation",
        interval=30  # Run every 30 seconds
    ) 