# Day 1 Setup Instructions

## Prerequisites

1. **Environment Configuration**
   - Copy `env.example` to `.env`:
     ```bash
     cp env.example .env
     ```
   - The `.env` file already contains your Discord webhook URL
   - Modify any other settings as needed

2. **Discord Webhook Setup** (Already configured)
   - Your webhook URL is already set in the `.env` file
   - If you need to change it, update the `DISCORD_WEBHOOK_URL` in `.env`

## Installation & Setup

### Option 1: Local Development

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Running the Components

### 1. FastAPI Application
- **Local**: `python app.py`
- **Docker**: Automatically starts with `docker-compose up`
- Access: http://localhost:8000
- Health check: http://localhost:8000/health

### 2. Prefect Pipeline

#### Setup Prefect Server (in separate terminal):
```bash
# Set Prefect API URL
# PowerShell:
$Env:PREFECT_API_URL = "http://127.0.0.1:4200/api"
# Bash:
export PREFECT_API_URL=http://127.0.0.1:4200/api

# Start Prefect server
prefect server start
```

#### Run the Pipeline:
```bash
# In another terminal, with same environment variables:
python flow.py
```

- Prefect UI: http://localhost:4200
- Pipeline runs every 30 seconds
- Generates random number and simulates model drift detection

### 3. Uptime Kuma Setup
- Access: http://localhost:3001
- Create account on first visit
- Add monitor:
  - Monitor Type: HTTP(s)
  - Friendly Name: FastAPI Health Check
  - URL: http://fastapi_app:8000/health (if using Docker) or http://localhost:8000/health (if local)
  - Heartbeat Interval: 30 seconds

## Expected Behavior

1. **FastAPI App**: Responds to health checks at `/health` endpoint
2. **Prefect Pipeline**: 
   - Runs every 30 seconds
   - Generates random number
   - If < 0.5: Simulates retraining failure (with retries)
   - If >= 0.5: Reports "OK" status
   - Sends Discord notifications for both cases
3. **Uptime Kuma**: Monitors API health and sends alerts if down

## Verification

- Check Prefect UI for flow runs and logs
- Verify Discord notifications are being sent
- Confirm Uptime Kuma is successfully pinging the health endpoint
- Check that retries work when random value < 0.5 