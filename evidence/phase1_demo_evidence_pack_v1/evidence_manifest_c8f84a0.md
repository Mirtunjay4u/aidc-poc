# Evidence Manifest

## Checkpoint

- c8f84a0 - Align documentation for Omniverse scene specification

## Runtime evidence captured

| Evidence type | File / folder | Status |
|---|---|---|
| Health endpoint sample | endpoint_samples/health_c8f84a0.json | Captured |
| Scenario list sample | endpoint_samples/scenarios_c8f84a0.json | Captured |
| GPU screen samples | endpoint_samples/gpu_screen_*_c8f84a0.json | Captured for all four scenarios |
| Hall summary samples | endpoint_samples/hall_summary_*_c8f84a0.json | Captured for all four scenarios |
| Hall rack samples | endpoint_samples/hall_racks_*_c8f84a0.json | Captured for all four scenarios |
| GPU screen UI HTML | endpoint_samples/gpu_screen_ui_c8f84a0.html | Captured |
| GPU screen UI HTTP status | endpoint_samples/gpu_screen_ui_http_status_c8f84a0.txt | Captured: 200 |
| Smoke test output | smoke_tests/smoke_test_api_v1_c8f84a0.txt | Passed |
| Full API runtime log | logs/full_api_runtime_c8f84a0.log | Captured |
| Structured API event extract | logs/structured_api_events_c8f84a0_pre_shutdown.log | Captured |
| Shutdown event log | logs/shutdown_events_c8f84a0.log | Captured |
| Post-shutdown process check | logs/process_check_after_shutdown_c8f84a0.txt | Captured; empty means no process remained |

## Runtime validation notes

- The smoke test completed successfully.
- /gpu/screen-ui returned HTTP 200.
- /health includes /gpu/screen-ui.
- Structured logs include api_ready, gpu_screen_requested, gpu_screen_ui_requested, scenario_started, scenario_reset_completed, and api_shutdown_completed.
- Screenshot evidence is still pending and should be added when browser capture is available.

## Boundary

This evidence pack supports Phase 1 synthetic, deterministic, file-backed scenario demonstration only. It does not prove production digital twin behavior, live scheduling, live facility control, or certified thermal simulation.
