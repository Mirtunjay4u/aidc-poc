# Scenario Acceptance Matrix v1

## 1. Document Control

| Field | Value |
|---|---|
| Project | AIDC Phase 1 |
| Document | Scenario Acceptance Matrix v1 |
| Environment | NVIDIA Brev |
| Implementation mode | File-backed deterministic scenario prototype |
| Primary use case | Datacentre Blueprint on Omniverse |
| Supporting flow | Separate AI workload and GPU resource optimization screen |
| Current Git checkpoint | 91be606 - Align documentation for GPU screen backend API |
| Purpose | Define scenario-level acceptance criteria for validation and demo readiness |

## 2. Objective

This document defines how each Phase 1 scenario must be validated.

The purpose is to move from basic endpoint validation to scenario correctness validation. Each scenario must have a clear intent, expected behavior, API response expectation, operator interpretation, pass criteria, and fail criteria.

## 3. Scope Boundary

### 3.1 In Scope

- Synthetic telemetry behavior
- Rules-engine evaluated status
- Hall summary API response
- Rack records API response
- Scenario controller behavior
- Separate GPU screen backend/API response
- Unknown scenario negative-path behavior
- Operator interpretation for demo storytelling

### 3.2 Out of Scope

- Live DCIM/BMS integration
- Live GPU scheduler integration
- Kubernetes or Slurm integration
- Real workload migration
- Omniverse scene authoring
- Omniverse telemetry-to-scene binding
- CFD simulation
- Production digital twin behavior

## 4. API Surface Under Acceptance

| Method | Endpoint | Validation purpose |
|---|---|---|
| GET | /health | Confirm service health and endpoint inventory |
| GET | /scenarios | Confirm four supported Phase 1 scenarios |
| GET | /hall/summary/{scenario_id} | Confirm hall-level scenario state |
| GET | /hall/racks/{scenario_id} | Confirm rack-level evaluated telemetry |
| GET | /scenario/current | Confirm current scenario controller state |
| POST | /scenario/{scenario_id}/start | Confirm supported scenario can be started |
| POST | /scenario/reset | Confirm scenario can reset to baseline |
| GET | /gpu/screen/{scenario_id} | Confirm separate GPU screen backend response |

## 5. Acceptance Principles

A scenario is accepted only when:

1. Required response artifacts exist.
2. Supported scenario endpoints return HTTP 200.
3. Unsupported scenario endpoints return structured HTTP 404.
4. Hall summary, rack records, and GPU screen response are internally consistent.
5. Scenario output matches the intended operating condition.
6. Operator interpretation is clear and aligned with the demo flow.
7. The system does not overclaim live scheduling, real workload migration, or production digital twin behavior.

## 6. Scenario Summary

| Scenario ID | Intent | Expected acceptance outcome |
|---|---|---|
| baseline_normal_operation | Normal hall operation | All racks normal, no high GPU pressure, no action required |
| ai_workload_surge | AI workload demand spike | GPU pressure and rack stress appear; redistribution guidance is triggered |
| cooling_degradation_hotspot | Cooling degradation or hotspot | Thermal risk dominates and critical status appears |
| workload_redistribution | Controlled redistribution state | Load shift is visible without claiming real migration |

## 7. Scenario Acceptance Details

### 7.1 baseline_normal_operation

**Intent:** Represent stable AI data centre hall operation.

**Expected behavior:**
- GPU utilization remains normal.
- Rack power remains in baseline range.
- Inlet temperature remains normal.
- Hotspot risk remains low.
- All racks remain normal.

**Expected hall summary:**
- scenario_id = baseline_normal_operation
- rack_count = 8
- status_counts.normal = 8
- status_counts.warning = 0
- status_counts.critical = 0

**Expected GPU screen response:**
- high_gpu_rack_count = 0
- critical_rack_count = 0
- warning_rack_count = 0
- all rack GPU pressure labels are normal
- optimization_message indicates no redistribution required

**Operator interpretation:** The hall is stable. GPU load is balanced. No operational action is required.

**Pass criteria:**
- GET /hall/summary/baseline_normal_operation returns HTTP 200.
- GET /hall/racks/baseline_normal_operation returns HTTP 200.
- GET /gpu/screen/baseline_normal_operation returns HTTP 200.
- rack_count equals 8.
- high_gpu_rack_count equals 0.
- critical_rack_count equals 0.

**Fail criteria:**
- Any rack is warning or critical.
- high_gpu_rack_count is greater than 0.
- optimization_message recommends action during baseline operation.

### 7.2 ai_workload_surge

**Intent:** Represent a spike in AI workload demand where GPU utilization and rack power increase.

**Expected behavior:**
- GPU utilization increases materially.
- Rack power draw increases.
- Some racks move into warning or critical state.
- GPU pressure is visible in the separate GPU screen response.

**Expected hall summary:**
- scenario_id = ai_workload_surge
- rack_count = 8
- max_gpu_util_pct reaches high utilization range
- warning and critical rack counts are non-zero

**Expected GPU screen response:**
- high_gpu_rack_count = 4
- critical_rack_count = 4
- optimization_message recommends shifting non-critical workload away from high-utilization racks

**Operator interpretation:** The hall is under AI workload pressure. GPU load concentration requires operator attention and redistribution guidance.

**Pass criteria:**
- GET /hall/summary/ai_workload_surge returns HTTP 200.
- GET /hall/racks/ai_workload_surge returns HTTP 200.
- GET /gpu/screen/ai_workload_surge returns HTTP 200.
- rack_count equals 8.
- high_gpu_rack_count equals 4.
- critical_rack_count equals 4.

**Fail criteria:**
- high_gpu_rack_count equals 0.
- critical_rack_count equals 0.
- optimization_message says no action is required.

### 7.3 cooling_degradation_hotspot

**Intent:** Represent a cooling degradation or hotspot condition where thermal risk is the main concern.

**Expected behavior:**
- Inlet temperature increases.
- Cooling health is degraded.
- Hotspot risk increases.
- Critical rack state appears because of thermal/cooling stress.
- GPU utilization may be elevated, but thermal risk is the dominant concern.

**Expected hall summary:**
- scenario_id = cooling_degradation_hotspot
- rack_count = 8
- critical rack count is greater than 0
- max_inlet_temp_c reflects thermal stress

**Expected GPU screen response:**
- high_gpu_rack_count is lower than workload surge scenario
- critical_rack_count is greater than 0
- optimization_message warns against adding GPU load to hotspot-affected racks

**Operator interpretation:** Cooling degradation is the dominant issue. The operator should avoid adding workload to thermally stressed racks.

**Pass criteria:**
- GET /hall/summary/cooling_degradation_hotspot returns HTTP 200.
- GET /hall/racks/cooling_degradation_hotspot returns HTTP 200.
- GET /gpu/screen/cooling_degradation_hotspot returns HTTP 200.
- rack_count equals 8.
- critical_rack_count is greater than 0.
- optimization_message references thermal risk or hotspot-affected racks.

**Fail criteria:**
- Scenario looks like baseline.
- No critical thermal or rules state appears.
- GPU screen message treats the condition only as workload surge.

### 7.4 workload_redistribution

**Intent:** Represent a controlled workload redistribution state without claiming actual live workload migration.

**Expected behavior:**
- GPU utilization distribution changes across racks.
- Rack pressure changes are visible.
- Critical rack count remains controlled.
- The scenario shows monitored redistribution, not real scheduler behavior.

**Expected hall summary:**
- scenario_id = workload_redistribution
- rack_count = 8
- distribution differs from baseline
- critical state does not dominate

**Expected GPU screen response:**
- high_gpu_rack_count = 1
- critical_rack_count = 0
- optimization_message indicates redistribution is active and should be monitored

**Operator interpretation:** Redistribution is active. The operator should monitor shifted load and confirm rack status remains within acceptable bounds.

**Pass criteria:**
- GET /hall/summary/workload_redistribution returns HTTP 200.
- GET /hall/racks/workload_redistribution returns HTTP 200.
- GET /gpu/screen/workload_redistribution returns HTTP 200.
- rack_count equals 8.
- high_gpu_rack_count equals 1.
- critical_rack_count equals 0.

**Fail criteria:**
- Scenario looks identical to baseline.
- critical_rack_count dominates the scenario.
- Message claims real workload migration occurred.

## 8. Negative-Path Acceptance

Unsupported scenario IDs must return structured HTTP 404 responses.

| Method | Endpoint |
|---|---|
| GET | /hall/summary/unknown_scenario |
| GET | /hall/racks/unknown_scenario |
| GET | /gpu/screen/unknown_scenario |
| POST | /scenario/unknown_scenario/start |

Expected error schema:

| Field | Expected value |
|---|---|
| error.code | unknown_scenario |
| error.message | Unknown scenario_id |
| error.scenario_id | requested unknown scenario |

Pass if:
- HTTP status is 404.
- Response body is structured JSON.
- error.code equals unknown_scenario.

Fail if:
- API returns HTTP 500.
- Response is unstructured.
- Unsupported scenario is silently accepted.

## 9. Current Acceptance Status

Current smoke-test validation already confirms:

- health endpoint
- scenario list endpoint
- baseline hall summary
- baseline GPU screen endpoint
- workload surge GPU screen endpoint
- unknown GPU screen negative path
- scenario current/start/reset flow
- unknown scenario start
- unknown hall summary
- unknown rack records

## 10. Next Engineering Step

Create a lightweight validation script to check this matrix against generated JSON artifacts and/or live API responses.

Recommended file:

tests/validate_scenario_acceptance_v1.py

The script should validate:

- required artifacts exist
- all four scenario responses are structurally valid
- scenario-specific acceptance expectations match this matrix
- negative-path expectations remain covered by the smoke test
