# AIDC POC README.md

## Purpose
Phase 1 backend/API prototype for synthetic AIDC scenario simulation, local API validation, and initial file-backed scenario control.

## Main folders
- config/ - schema and inventory configuration
- scenarios/ - scenario matrix and profiles
- data_generator/ - synthetic telemetry generation logic
- rules_engine/ - rules evaluation logic
- api/ - FastAPI application, API contract, and dependency file
- scripts/ - startup and smoke-test automation
- tests/ - generated mock API response files and current scenario state
- docs/ - checkpoint, startup, runbook, and validation notes

## Current status
Phase 1 backend/API prototype is validated for local runtime demo in the NVIDIA Brev environment. The API now supports standardized startup, health/scenario reads, hall and rack response retrieval, and initial file-backed scenario control.

## Start API
Run from Terminal 1:

    cd ~/aidc-poc
    scripts/start_api_v1.sh

## Validate API
Run from Terminal 2 while the API is running:

    cd ~/aidc-poc
    scripts/smoke_test_api_v1.sh

## Current API endpoints
- GET /health
- GET /scenarios
- GET /hall/summary/{scenario_id}
- GET /hall/racks/{scenario_id}
- GET /scenario/current
- POST /scenario/{scenario_id}/start
- POST /scenario/reset

## Supported Phase 1 scenarios
- baseline_normal_operation
- ai_workload_surge
- cooling_degradation_hotspot
- workload_redistribution

## Key docs
- docs/api_startup_instructions_v1.md
- docs/demo_runbook_v1.md
- docs/api_validation_summary_v1.md
- docs/api_progress_note_v1.md
- docs/phase1_backend_status_v1.md
