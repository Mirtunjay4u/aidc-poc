# Demo Runbook v1

## Objective
Demonstrate the Phase 1 backend/API prototype in the local Brev environment.

## Demo preparation
1. Open one terminal tab for the API server
2. Open one terminal tab for validation commands
3. Confirm project path exists at `~/aidc-poc`

## Start API
uvicorn app_v1:app --app-dir ~/aidc-poc/api --host 0.0.0.0 --port 8000

## Demo sequence
1. Health check
   - `curl http://127.0.0.1:8000/health`

2. Supported scenarios
   - `curl http://127.0.0.1:8000/scenarios`

3. Baseline summary
   - `curl http://127.0.0.1:8000/hall/summary/baseline_normal_operation`

4. AI workload surge summary
   - `curl http://127.0.0.1:8000/hall/summary/ai_workload_surge`

5. Cooling degradation hotspot summary
   - `curl http://127.0.0.1:8000/hall/summary/cooling_degradation_hotspot`

6. Workload redistribution summary
   - `curl http://127.0.0.1:8000/hall/summary/workload_redistribution`

7. Baseline rack records
   - `curl -s http://127.0.0.1:8000/hall/racks/baseline_normal_operation | head -c 1200`

8. AI workload surge rack records
   - `curl -s http://127.0.0.1:8000/hall/racks/ai_workload_surge | head -c 1200`

## Expected outcome
- API starts successfully
- All endpoints respond with expected JSON
- Scenario outputs reflect the designed Phase 1 operating conditions

## Stop API
Press Ctrl+C in the server terminal
