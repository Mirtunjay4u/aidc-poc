# API Contract v2

## 1. Document Control

| Field | Value |
|---|---|
| Project | AIDC Phase 1 |
| Document | API Contract v2 |
| Environment | NVIDIA Brev |
| Runtime mode | Local FastAPI runtime |
| Implementation mode | File-backed deterministic scenario prototype |
| Current Git checkpoint | 6093902 - Add scenario acceptance validation script |
| Purpose | Define the current Phase 1 API surface, response expectations, error behavior, and local-demo boundary |

## 2. Objective

This document describes the current AIDC Phase 1 API contract for technical review, demo validation, and engineering handoff.

The API supports:

- health validation
- supported scenario discovery
- hall-level scenario summary
- rack-level evaluated telemetry
- file-backed scenario control
- separate GPU screen backend response
- structured unknown-scenario error handling

This contract documents the current file-backed prototype behavior. It is not a production security contract, deployment contract, or live infrastructure integration contract.

## 3. Scope Boundary

### 3.1 In Scope

- Current local FastAPI endpoints
- Supported HTTP methods
- Path parameters
- Success response purpose
- Key response fields
- Error response behavior
- Local demo validation expectations

### 3.2 Out of Scope

- Authentication and authorization
- Enterprise API gateway policy
- Live DCIM/BMS integration
- Live GPU scheduler integration
- Kubernetes or Slurm integration
- Real workload migration
- Omniverse scene binding
- Production deployment topology
- Production monitoring and alerting

## 4. API Inventory

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Return service health and available endpoint inventory |
| GET | /scenarios | Return supported Phase 1 scenario catalogue |
| GET | /hall/summary/{scenario_id} | Return hall-level scenario summary |
| GET | /hall/racks/{scenario_id} | Return rack-level evaluated telemetry records |
| GET | /scenario/current | Return current file-backed scenario controller state |
| POST | /scenario/{scenario_id}/start | Start a supported scenario and update current scenario state |
| POST | /scenario/reset | Reset current scenario state to baseline normal operation |
| GET | /gpu/screen/{scenario_id} | Return separate GPU screen backend/API response |

## 5. Supported Scenario IDs

The API currently supports four deterministic Phase 1 scenarios.

| Scenario ID | Purpose |
|---|---|
| baseline_normal_operation | Normal hall operating condition |
| ai_workload_surge | AI workload pressure and GPU utilization surge |
| cooling_degradation_hotspot | Cooling degradation / hotspot condition |
| workload_redistribution | Controlled redistribution scenario without claiming live migration |

## 6. Common Error Response

Unsupported scenario IDs return structured HTTP 404 responses.

### 6.1 Error schema

```json
{
  "error": {
    "code": "unknown_scenario",
    "message": "Unknown scenario_id",
    "scenario_id": "unknown_scenario"
  }
}
```

### 6.2 Error behavior

| Condition | Expected status | Expected code |
|---|---:|---|
| Unknown hall summary scenario | 404 | unknown_scenario |
| Unknown rack records scenario | 404 | unknown_scenario |
| Unknown GPU screen scenario | 404 | unknown_scenario |
| Unknown scenario start request | 404 | unknown_scenario |

## 7. Endpoint Contract Details

### 7.1 GET /health

**Purpose:** Return service health and available endpoint inventory.

**Request:** No path parameter.

**Success status:** HTTP 200

**Key response fields:**

| Field | Type | Purpose |
|---|---|---|
| service | string | Service identifier |
| version | string | API version |
| status | string | Health status |
| available_endpoints | array | Endpoint inventory exposed by the service |

**Acceptance expectation:**
- status equals healthy.
- available_endpoints includes /gpu/screen/{scenario_id}.

### 7.2 GET /scenarios

**Purpose:** Return the supported Phase 1 scenario catalogue.

**Request:** No path parameter.

**Success status:** HTTP 200

**Key response fields:**

| Field | Type | Purpose |
|---|---|---|
| phase | string | Phase identifier |
| scenario_count | integer | Number of supported scenarios |
| scenarios | array | Scenario metadata list |

**Acceptance expectation:**
- scenario_count equals 4.
- all four supported scenario IDs are present.

### 7.3 GET /hall/summary/{scenario_id}

**Purpose:** Return hall-level summary for a supported scenario.

**Path parameter:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| scenario_id | string | Yes | Supported Phase 1 scenario ID |

**Success status:** HTTP 200

**Key response fields:**

| Field | Type | Purpose |
|---|---|---|
| scenario_id | string | Scenario identifier |
| hall_id | string | Representative hall identifier |
| rack_count | integer | Number of racks represented |
| status_counts | object | Count of normal, warning, and critical racks |
| max_inlet_temp_c | number | Maximum rack inlet temperature |
| max_power_kw | number | Maximum rack power draw |
| max_gpu_util_pct | integer | Maximum rack GPU utilization |

**Error status:** HTTP 404 for unsupported scenario IDs.

### 7.4 GET /hall/racks/{scenario_id}

**Purpose:** Return rack-level evaluated telemetry records for a supported scenario.

**Path parameter:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| scenario_id | string | Yes | Supported Phase 1 scenario ID |

**Success status:** HTTP 200

**Key response fields:**

| Field | Type | Purpose |
|---|---|---|
| scenario_id | string | Scenario identifier |
| hall_id | string | Representative hall identifier |
| rack_count | integer | Number of rack records |
| records | array | Rack-level evaluated telemetry records |

**Key rack record fields:**

| Field | Type | Purpose |
|---|---|---|
| rack_id | string | Rack identifier |
| zone_id | string | Zone identifier |
| timestamp | string | Scenario telemetry timestamp |
| inlet_temp_c | number | Rack inlet temperature |
| power_kw | number | Rack power draw |
| gpu_util_pct | integer | Rack GPU utilization percentage |
| cooling_health | string | Cooling health state |
| hotspot_risk | string | Hotspot risk label |
| status | string | Source operating status |
| evaluated_status | string | Rules-engine evaluated status |

**Error status:** HTTP 404 for unsupported scenario IDs.

### 7.5 GET /scenario/current

**Purpose:** Return the current file-backed scenario controller state.

**Request:** No path parameter.

**Success status:** HTTP 200

**Key response fields:**

| Field | Type | Purpose |
|---|---|---|
| current_scenario_id | string | Current active scenario |
| status | string | Current controller status |
| updated_at | string | Last update timestamp or marker |

**Acceptance expectation:**
- response includes current_scenario_id.
- after reset, current_scenario_id returns to baseline_normal_operation.

### 7.6 POST /scenario/{scenario_id}/start

**Purpose:** Start a supported scenario and update the current file-backed scenario controller state.

**Path parameter:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| scenario_id | string | Yes | Supported Phase 1 scenario ID |

**Success status:** HTTP 200

**Key response fields:**

| Field | Type | Purpose |
|---|---|---|
| current_scenario_id | string | Scenario that was started |
| status | string | Scenario controller status |
| updated_at | string | Last update timestamp or marker |

**Acceptance expectation:**
- starting ai_workload_surge returns current_scenario_id = ai_workload_surge.
- status = running.
- GET /scenario/current reflects the started scenario.

**Error status:** HTTP 404 for unsupported scenario IDs.

### 7.7 POST /scenario/reset

**Purpose:** Reset current scenario state to baseline normal operation.

**Request:** No path parameter.

**Success status:** HTTP 200

**Key response fields:**

| Field | Type | Purpose |
|---|---|---|
| current_scenario_id | string | Reset scenario ID |
| status | string | Reset status |
| updated_at | string | Last update timestamp or marker |

**Acceptance expectation:**
- current_scenario_id = baseline_normal_operation.
- status = reset.
- GET /scenario/current reflects baseline_normal_operation after reset.

### 7.8 GET /gpu/screen/{scenario_id}

**Purpose:** Return the separate GPU screen backend/API response for a supported scenario.

This endpoint supports the separate AI workload and GPU resource optimization screen. It is a decision-support response, not a live GPU scheduler and not an Omniverse scene binding endpoint.

**Path parameter:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| scenario_id | string | Yes | Supported Phase 1 scenario ID |

**Success status:** HTTP 200

**Top-level response fields:**

| Field | Type | Purpose |
|---|---|---|
| scenario_id | string | Scenario identifier |
| hall_id | string | Representative hall identifier |
| rack_count | integer | Number of racks represented |
| summary | object | Aggregate GPU screen summary |
| rack_gpu_records | array | Rack-level GPU screen display records |

**Summary fields:**

| Field | Type | Purpose |
|---|---|---|
| avg_gpu_util_pct | number | Average GPU utilization across racks |
| max_gpu_util_pct | integer | Maximum GPU utilization |
| min_gpu_util_pct | integer | Minimum GPU utilization |
| high_gpu_rack_count | integer | Count of racks labelled high GPU pressure |
| critical_rack_count | integer | Count of critical racks |
| warning_rack_count | integer | Count of warning racks |
| total_power_kw | number | Total rack power draw |
| max_power_kw | number | Maximum rack power draw |
| hottest_rack_id | string | Rack with highest inlet temperature |
| highest_gpu_rack_id | string | Rack with highest GPU utilization |
| optimization_message | string | Scenario-specific decision-support guidance |

**Rack GPU record fields:**

| Field | Type | Purpose |
|---|---|---|
| rack_id | string | Rack identifier |
| zone_id | string | Zone identifier |
| gpu_util_pct | integer | GPU utilization percentage |
| power_kw | number | Rack power draw |
| inlet_temp_c | number | Rack inlet temperature |
| evaluated_status | string | Rules-engine status |
| hotspot_risk | string | Hotspot risk label |
| gpu_pressure_label | string | Derived GPU pressure label |

**Error status:** HTTP 404 for unsupported scenario IDs.

## 8. Current Validation Coverage

The following validation assets support this contract:

| Asset | Purpose |
|---|---|
| scripts/smoke_test_api_v1.sh | Runtime endpoint smoke validation |
| docs/scenario_acceptance_matrix_v1.md | Scenario-level acceptance criteria |
| tests/validate_scenario_acceptance_v1.py | Artifact-level scenario acceptance validation |
| docs/api_validation_summary_v1.md | Validation summary |
| docs/demo_runbook_v1.md | Demo execution flow |

## 9. Local Demo Security Boundary

This API contract is for a local Phase 1 Brev demo prototype.

Current boundary:

- no authentication implemented
- no authorization model implemented
- no live infrastructure credentials used
- no external DCIM/BMS system connected
- no production scheduler connected
- no customer or live operational data used

Future production hardening would require:

- authentication and authorization
- API gateway or access control
- secrets management
- audit logging
- request validation policy
- rate limiting where applicable
- environment-specific configuration
- integration security review

## 10. Engineering Position

The current API is suitable for:

- local technical walkthrough
- leadership demo support
- backend-only fallback demo
- scenario validation
- separate GPU screen backend support

The current API is not yet suitable for:

- production deployment
- live infrastructure control
- live GPU scheduling
- real workload migration
- Omniverse scene control without a formal binding layer

## 11. Next Recommended Step

After this contract is reviewed, the next engineering-quality artifact should be:

- thermal_power_threshold_rationale_v1.md

That document should explain the Phase 1 threshold assumptions for inlet temperature, rack power, GPU utilization, hotspot risk, and evaluated status.
