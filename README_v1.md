# AIDC POC README v1

## Purpose
Phase 1 backend/API prototype for synthetic AIDC scenario simulation and local API validation.

## Main folders
- config/ - schema and inventory configuration
- scenarios/ - scenario matrix and profiles
- data_generator/ - synthetic telemetry generation logic
- rules_engine/ - rules evaluation logic
- api/ - FastAPI application and dependency file
- tests/ - generated mock API response files
- docs/ - checkpoint, startup, runbook, and validation notes

## Current status
Phase 1 backend/API prototype is validated for local runtime demo in the Brev environment.

## Start API
uvicorn app_v1:app --app-dir ~/aidc-poc/api --host 0.0.0.0 --port 8000

## Key docs
- docs/api_startup_instructions_v1.md
- docs/demo_runbook_v1.md
- docs/api_validation_summary_v1.md
