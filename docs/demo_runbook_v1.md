# Demo Runbook v1

## Objective
Demonstrate the Phase 1 backend/API prototype in the local NVIDIA Brev environment using the standardized startup script, file-backed scenario controller, and separate GPU screen backend/API response.

## Demo preparation
1. Open Terminal 1 for the API server.
2. Open Terminal 2 for validation and demo commands.
3. Confirm project path exists at ~/aidc-poc.
4. Confirm latest code is available on main branch.
5. Keep the backend-only fallback demo available for Phase 1 review.

## Start API
Run from Terminal 1:

    cd ~/aidc-poc
    scripts/start_api_v1.sh

Expected startup result:
- Python dependency check passes.
- Required response file validation completes successfully.
- Uvicorn starts on 0.0.0.0:8000.
- Local validation uses http://127.0.0.1:8000.

## Pre-demo smoke test
Run from Terminal 2 while the API is running:

    cd ~/aidc-poc
    scripts/smoke_test_api_v1.sh

Expected result:
- Smoke test completes successfully.
- Health, scenario list, baseline summary, GPU screen, scenario controller, and negative-path checks pass.

## Demo sequence

### 1. Health check
    curl http://127.0.0.1:8000/health

Purpose:
- Confirm API is healthy.
- Show available backend endpoints.

### 2. Supported scenarios
    curl http://127.0.0.1:8000/scenarios

Purpose:
- Show the four supported Phase 1 scenarios.

### 3. Current scenario state
    curl http://127.0.0.1:8000/scenario/current

Purpose:
- Show the current file-backed scenario controller state.

### 4. Baseline hall summary
    curl http://127.0.0.1:8000/hall/summary/baseline_normal_operation

Purpose:
- Establish normal hall operating condition.

### 5. Start AI workload surge scenario
    curl -X POST http://127.0.0.1:8000/scenario/ai_workload_surge/start

Purpose:
- Demonstrate scenario control through the API.

### 6. Confirm current scenario after start
    curl http://127.0.0.1:8000/scenario/current

Expected:
- current_scenario_id is ai_workload_surge.
- status is running.

### 7. AI workload surge hall summary
    curl http://127.0.0.1:8000/hall/summary/ai_workload_surge

Purpose:
- Show increased GPU utilization, power draw, and operating stress for the workload surge scenario.

### 8. AI workload surge rack records
    curl -s http://127.0.0.1:8000/hall/racks/ai_workload_surge | head -c 1200

Purpose:
- Show rack-level evaluated telemetry records.

### 8A. AI workload surge GPU screen response
    curl http://127.0.0.1:8000/gpu/screen/ai_workload_surge

Purpose:
- Show the separate GPU screen backend response.
- Highlight GPU utilization, high-GPU rack count, power impact, rack pressure, and redistribution guidance.
- Confirm this is a separate decision-support flow, not live GPU scheduling or Omniverse scene binding.

### 9. Start cooling degradation hotspot scenario
    curl -X POST http://127.0.0.1:8000/scenario/cooling_degradation_hotspot/start

Purpose:
- Demonstrate another controlled operating condition.

### 10. Cooling degradation hotspot summary
    curl http://127.0.0.1:8000/hall/summary/cooling_degradation_hotspot

Purpose:
- Show thermal/cooling degradation behavior.

### 11. Start workload redistribution scenario
    curl -X POST http://127.0.0.1:8000/scenario/workload_redistribution/start

Purpose:
- Demonstrate workload shift across racks.

### 12. Workload redistribution summary
    curl http://127.0.0.1:8000/hall/summary/workload_redistribution

Purpose:
- Show redistributed rack load and changed operating state.

### 13. Reset scenario controller
    curl -X POST http://127.0.0.1:8000/scenario/reset

Expected:
- current_scenario_id returns to baseline_normal_operation.
- status returns to reset.

### 14. Confirm current scenario after reset
    curl http://127.0.0.1:8000/scenario/current

Purpose:
- Confirm the demo returns to the baseline state.

## Negative-path validation
Optional commands:

    curl -i -X POST http://127.0.0.1:8000/scenario/unknown_scenario/start
    curl -i http://127.0.0.1:8000/gpu/screen/unknown_scenario

Expected:
- HTTP 404
- error.code is unknown_scenario

## Expected outcome
- API starts successfully through scripts/start_api_v1.sh.
- Smoke test passes.
- All read endpoints respond with expected JSON.
- Scenario controller supports current, start, and reset behavior.
- Separate GPU screen backend/API response is available for scenario-driven decision support.
- Scenario outputs reflect the designed Phase 1 operating conditions.
- Demo can be executed as a backend-only fallback while Santa Clara RTX / Omniverse readiness remains pending.

## Stop API
Press Ctrl+C in Terminal 1 where scripts/start_api_v1.sh / Uvicorn is running.

Expected shutdown result:
- Uvicorn shuts down cleanly.
- API shutdown log appears.
