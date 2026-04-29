# API Startup Instructions v1

## Purpose
Start the Phase 1 FastAPI backend locally in the Brev environment.

## Prerequisites
- Project path available at `~/aidc-poc`
- Python environment active
- Dependencies installed from `~/aidc-poc/api/requirements_v1.txt`

## Start command
uvicorn app_v1:app --app-dir ~/aidc-poc/api --host 0.0.0.0 --port 8000

## Quick validation commands
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/scenarios
curl http://127.0.0.1:8000/hall/summary/baseline_normal_operation
curl http://127.0.0.1:8000/hall/racks/baseline_normal_operation

## Stop command
Press Ctrl+C in the terminal where Uvicorn is running.

## Notes
- Keep the Uvicorn process in its own terminal tab
- Use a separate terminal tab for curl validation
