import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "default-key-change-me")
STREAMLIT_PASSWORD = os.getenv("STREAMLIT_PASSWORD", "admin123")

def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == STREAMLIT_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

def make_api_request(endpoint, method="GET", data=None):
    """Make API request with authentication"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        
        return response.status_code, response.json()
    except Exception as e:
        return None, str(e)

def main():
    st.set_page_config(
        page_title="Continual ML Dashboard",
        page_icon="🤖",
        layout="wide"
    )
    
    if not check_password():
        st.stop()
    
    st.title("🤖 Continual ML Dashboard")
    st.markdown("---")
    
    # Sidebar with API configuration
    with st.sidebar:
        st.header("Configuration")
        st.text(f"API URL: {API_BASE_URL}")
        st.text(f"API Key: {'*' * len(API_KEY)}")
        
        if st.button("🔄 Refresh Status"):
            st.rerun()
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🏥 System Status")
        
        # Health Check
        if st.button("Check Health", type="primary"):
            with st.spinner("Checking health..."):
                status_code, response = make_api_request("/health")
                
                if status_code == 200:
                    st.success("✅ API is healthy!")
                    st.json(response)
                else:
                    st.error(f"❌ Health check failed: {response}")
        
        # Model Status
        if st.button("Check Model Status"):
            with st.spinner("Checking model status..."):
                status_code, response = make_api_request("/model-status")
                
                if status_code == 200:
                    if response.get("model_trained"):
                        st.success("✅ Model is trained")
                        performance = response.get("performance", 0)
                        threshold = response.get("threshold", 0.8)
                        
                        st.metric("Model Performance", f"{performance:.3f}")
                        st.metric("Threshold", f"{threshold:.3f}")
                        
                        if response.get("needs_retraining"):
                            st.warning("⚠️ Model needs retraining")
                        else:
                            st.success("✅ Model performance is good")
                    else:
                        st.warning("⚠️ No model trained")
                else:
                    st.error(f"❌ Status check failed: {response}")
    
    with col2:
        st.header("🛠️ Actions")
        
        # Generate Dataset
        if st.button("Generate Dataset", type="secondary"):
            with st.spinner("Generating dataset..."):
                status_code, response = make_api_request("/generate", method="POST")
                
                if status_code == 200:
                    st.success("✅ Dataset generated successfully!")
                    st.json(response)
                else:
                    st.error(f"❌ Dataset generation failed: {response}")
        
        # Automation Status
        st.markdown("### 🤖 Automated Retraining")
        st.info("🔄 **Retraining is now fully automated via Prefect!**\n\n"
                "• ⏰ Checks performance every 30 seconds\n"
                "• 🎯 Retrains automatically when performance drops below 80%\n"
                "• 📢 Sends Discord notifications for all events\n"
                "• 🚫 No manual intervention required")
        
        if st.button("View Automation Details", type="secondary"):
            with st.spinner("Getting automation status..."):
                status_code, response = make_api_request("/model-status")
                
                if status_code == 200:
                    st.success("✅ Automation Status Retrieved!")
                    
                    # Display automation details
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Model Trained", "✅ Yes" if response.get("model_trained") else "❌ No")
                        st.metric("Performance", f"{response.get('performance', 0):.3f}")
                    with col_b:
                        st.metric("Threshold", f"{response.get('threshold', 0.8):.3f}")
                        needs_retrain = "🔄 Yes" if response.get("needs_retraining") else "✅ No"
                        st.metric("Needs Retraining", needs_retrain)
                    
                    if "automation_note" in response:
                        st.info(f"ℹ️ {response['automation_note']}")
                else:
                    st.error(f"❌ Could not get automation status: {response}")
    
    st.markdown("---")
    
    # Prediction section
    st.header("🎯 Make Prediction")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        feature1 = st.number_input("Feature 1", value=0.0, step=0.1)
    
    with col2:
        feature2 = st.number_input("Feature 2", value=0.0, step=0.1)
    
    with col3:
        if st.button("Predict", type="primary"):
            prediction_data = {"feature1": feature1, "feature2": feature2}
            
            with st.spinner("Making prediction..."):
                status_code, response = make_api_request("/predict", method="POST", data=prediction_data)
                
                if status_code == 200:
                    prediction = response.get("prediction")
                    probability = response.get("probability")
                    
                    st.success(f"✅ Prediction: {prediction}")
                    st.metric("Confidence", f"{probability:.3f}")
                    
                    # Visual indicator
                    if prediction == 1:
                        st.balloons()
                else:
                    st.error(f"❌ Prediction failed: {response}")

if __name__ == "__main__":
    main() 