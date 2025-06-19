import random
import requests
import os
from prefect import flow, task
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Configuration from environment variables
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", 30))
TASK_RETRIES = int(os.getenv("TASK_RETRIES", 2))
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", 1))

def send_discord_embed(message):
    """Send a message to Discord via webhook"""
    if not DISCORD_WEBHOOK_URL:
        logger.warning("Discord webhook URL not configured - skipping notification")
        return
    
    data = {
        "embeds": [{
            "title": "Continual ML Notification",
            "description": message,
            "color": 5814783  # Blue color
        }]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
        logger.success("Discord notification sent successfully")
    except Exception as e:
        logger.error(f"Failed to send Discord notification: {e}")

@task(retries=TASK_RETRIES, retry_delay_seconds=RETRY_DELAY_SECONDS)
def check_random():
    """Generate random number and simulate retraining if < 0.5"""
    random_value = random.random()
    logger.info(f"Generated random value: {random_value}")
    
    if random_value < 0.5:
        logger.warning("Drift detected! Initiating retraining...")
        send_discord_embed(f"🔄 Model drift detected (value: {random_value:.3f}). Retraining initiated.")
        # Simulate retraining failure for demonstration
        raise Exception("Retraining failed - simulated failure")
    else:
        logger.info("Model performance OK - no retraining needed")
        send_discord_embed(f"✅ Model performance OK (value: {random_value:.3f})")
        return "ok"

@flow
def periodic_check():
    """Periodic check flow that runs the random check"""
    logger.info("Starting periodic model check...")
    
    try:
        result = check_random()
        logger.info(f"Check completed successfully: {result}")
    except Exception as e:
        logger.error(f"Check failed: {e}")
        send_discord_embed(f"❌ Periodic check failed: {str(e)}")

if __name__ == "__main__":
    # Serve the flow with configurable interval
    logger.info(f"Starting periodic check flow with {CHECK_INTERVAL_SECONDS}s interval")
    periodic_check.serve(name="random-check", interval=CHECK_INTERVAL_SECONDS) 