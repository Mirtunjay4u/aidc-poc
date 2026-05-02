# AIDC POC README.md

## Purpose
Phase 1 backend/API prototype for synthetic AIDC scenario simulation, local API validation, file-backed scenario control, the separate GPU screen backend/API feed, and the first lightweight GPU screen UI shell.

## Main folders
- config/ - schema and inventory configuration
- scenarios/ - scenario matrix and profiles
- data_generator/ - synthetic telemetry generation logic
- rules_engine/ - rules evaluation logic
- api/ - FastAPI application, API contract, and dependency file
- scripts/ - startup and smoke-test automation
- tests/ - generated mock API response files and current scenario state
- docs/ - checkpoint, startup, runbook, validation, API contract, rationale, and observability notes
- ui/ - lightweight local UI shells

## Current status
Phase 1 backend/API prototype is validated for local runtime demo in the NVIDIA Brev environment. The API now supports standardized startup, health/scenario reads, hall and rack response retrieval, file-backed scenario control, a separate GPU screen backend/API response, structured API event logging, and a first lightweight GPU screen UI shell served at /gpu/screen-ui. The UI remains a Phase 1 decision-support shell, not a live scheduler or Omniverse scene binding.

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
- GET /gpu/screen/{scenario_id}

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
- docs/gpu_screen_scope_v1.md
- docs/gpu_screen_ui_definition_v1.md
