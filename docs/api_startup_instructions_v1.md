# API Startup Instructions v1

## Purpose
Start the Phase 1 FastAPI backend locally in the NVIDIA Brev environment using the standardized startup script.

## Prerequisites
- Project path available at ~/aidc-poc
- Python environment active
- Dependencies installed from ~/aidc-poc/api/requirements_v1.txt
- Response artifacts available under ~/aidc-poc/tests

## Standard start command
Run this from Terminal 1:

    cd ~/aidc-poc
    scripts/start_api_v1.sh

## What the startup script validates
The startup script performs basic local readiness checks before launching Uvicorn:

- Confirms the project directory exists
- Confirms api/app_v1.py exists
- Confirms api/requirements_v1.txt exists
- Confirms the tests response artifact directory exists
- Confirms required Python packages fastapi and uvicorn are available

The FastAPI application then performs startup-time validation of required response files for all supported scenarios.

## Runtime endpoint
By default, the API is validated locally at:

    http://127.0.0.1:8000

The startup script binds Uvicorn to:

    0.0.0.0:8000

## Optional environment overrides
The startup script supports these optional environment variables:

    AIDC_PROJECT_DIR=/home/ubuntu/aidc-poc
    AIDC_API_HOST=0.0.0.0
    AIDC_API_PORT=8000

Example:

    AIDC_API_PORT=8001 scripts/start_api_v1.sh

## Quick validation commands
Run these from Terminal 2 while the API is running:

    curl http://127.0.0.1:8000/health
    curl http://127.0.0.1:8000/scenarios
    curl http://127.0.0.1:8000/hall/summary/baseline_normal_operation
    curl http://127.0.0.1:8000/hall/racks/baseline_normal_operation

## Smoke test command
Run this from Terminal 2 while the API is running:

    cd ~/aidc-poc
    scripts/smoke_test_api_v1.sh

## Stop command
Press Ctrl+C in Terminal 1 where scripts/start_api_v1.sh / Uvicorn is running.

## Notes
- Keep the Uvicorn process in its own terminal tab.
- Use a separate terminal tab for smoke test and curl validation.
- The backend remains file-backed for Phase 1 demo use.
