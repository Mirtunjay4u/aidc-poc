# GPU Screen UI Definition v1

## 1. Document Control

| Field | Value |
|---|---|
| Project | AIDC Phase 1 |
| Document | GPU Screen UI Definition v1 |
| Environment | NVIDIA Brev |
| Implementation mode | File-backed deterministic scenario prototype |
| Supporting flow | Separate AI workload and GPU resource optimization screen |
| Current Git checkpoint | 5a46359 - Align documentation for structured API event logging |
| Purpose | Define the separate GPU screen layout, data mapping, operator interpretation model, and implementation boundary before dashboard build |

## 2. Objective

This document defines the intended layout and interpretation model for the separate GPU screen.

The purpose is to ensure the screen is built as a credible decision-support view for AI workload and GPU resource pressure, while staying inside the approved Phase 1 boundary.

The screen must communicate:

- current scenario context
- GPU utilization pressure
- rack-level GPU and power impact
- warning and critical rack visibility
- hotspot and thermal risk awareness
- scenario-specific optimization guidance

This screen is not a live GPU scheduler, not a workload migration engine, and not an Omniverse scene binding.

## 3. Scope Boundary

### 3.1 In Scope

- Separate GPU dashboard/screen definition
- Layout sections and data cards
- Mapping from GET /gpu/screen/{scenario_id}
- Operator interpretation rules
- Scenario-specific screen behavior
- Demo language guardrails
- UI acceptance criteria

### 3.2 Out of Scope

- Live GPU scheduler integration
- Slurm or Kubernetes control
- Real workload migration
- Production optimization engine
- Omniverse scene control
- Live DCIM/BMS integration
- Production alerting or ticketing workflow

## 4. Source API

The screen should consume the existing backend endpoint:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /gpu/screen/{scenario_id} | Returns file-backed GPU screen response for the requested scenario |

The endpoint is already implemented and smoke-tested for Phase 1.

## 5. Top-Level UI Intent

The separate GPU screen should answer four operator questions:

1. Which scenario is currently being demonstrated?
2. Are GPU workloads balanced or under pressure?
3. Which racks are creating the highest GPU/power/thermal concern?
4. What decision-support guidance should the operator explain?

## 6. Primary Screen Sections

The proposed screen should contain the following sections:

| Section | Purpose |
|---|---|
| Scenario header | Show active scenario and hall context |
| KPI summary strip | Show aggregate GPU, power, warning, and critical indicators |
| Rack GPU pressure table | Show rack-by-rack GPU utilization and status |
| Rack pressure visual band | Give a quick visual view of rack pressure distribution |
| Optimization guidance panel | Explain recommended operator interpretation |
| Boundary note | State that this is scenario-driven decision support, not live scheduling |


## 7. API Data Mapping

The UI should map directly from GET /gpu/screen/{scenario_id}.

### 7.1 Top-level response mapping

| API field | UI usage |
|---|---|
| scenario_id | Scenario header |
| hall_id | Scenario header / context label |
| rack_count | KPI summary strip |
| summary | KPI summary, guidance panel, visual state |
| rack_gpu_records | Rack table and pressure visual band |

### 7.2 Summary field mapping

| API field | UI component | Interpretation |
|---|---|---|
| avg_gpu_util_pct | KPI card | Average GPU pressure across hall |
| max_gpu_util_pct | KPI card | Highest rack GPU pressure |
| min_gpu_util_pct | KPI card | Lowest rack GPU pressure |
| high_gpu_rack_count | KPI card | Number of racks with high GPU pressure |
| critical_rack_count | KPI card | Count of racks in critical state |
| warning_rack_count | KPI card | Count of racks in warning state |
| total_power_kw | KPI card | Aggregate rack power load |
| max_power_kw | KPI card | Highest rack power draw |
| hottest_rack_id | Highlight badge | Rack with highest inlet temperature |
| highest_gpu_rack_id | Highlight badge | Rack with highest GPU utilization |
| optimization_message | Guidance panel | Operator-facing scenario recommendation |

### 7.3 Rack record mapping

| API field | UI usage |
|---|---|
| rack_id | Rack row identifier and visual band label |
| zone_id | Grouping / zone context |
| gpu_util_pct | GPU utilization bar |
| power_kw | Power load value |
| inlet_temp_c | Thermal condition value |
| evaluated_status | Status badge |
| hotspot_risk | Thermal risk badge |
| gpu_pressure_label | GPU pressure badge |

## 8. KPI Summary Strip

The KPI strip should be visible at the top of the screen below the scenario header.

Recommended KPI cards:

| KPI card | Source field | Display rule |
|---|---|---|
| Average GPU Utilization | avg_gpu_util_pct | Percentage with one or two decimals |
| Maximum GPU Utilization | max_gpu_util_pct | Percentage integer |
| High GPU Racks | high_gpu_rack_count | Count |
| Critical Racks | critical_rack_count | Count |
| Warning Racks | warning_rack_count | Count |
| Total Power | total_power_kw | kW |
| Hottest Rack | hottest_rack_id | Rack ID |
| Highest GPU Rack | highest_gpu_rack_id | Rack ID |

## 9. Rack GPU Pressure Table

The rack table should be the primary detailed section.

Recommended columns:

| Column | Source field | Purpose |
|---|---|---|
| Rack | rack_id | Identify the rack |
| Zone | zone_id | Show compute/cooling/power zone context |
| GPU Utilization | gpu_util_pct | Show AI workload pressure |
| GPU Pressure | gpu_pressure_label | Show normal/elevated/high classification |
| Power | power_kw | Show power impact |
| Inlet Temp | inlet_temp_c | Show thermal context |
| Hotspot Risk | hotspot_risk | Show thermal risk label |
| Status | evaluated_status | Show normal/warning/critical state |

Recommended default sorting:
1. critical evaluated_status first
2. high gpu_pressure_label second
3. highest gpu_util_pct third
4. highest inlet_temp_c fourth

## 10. Rack Pressure Visual Band

The screen should include a compact rack pressure visual band for quick operator interpretation.

Recommended behavior:

| Visual element | Source field | Interpretation |
|---|---|---|
| Rack tile label | rack_id | Shows rack identity |
| Tile group | zone_id | Groups racks by operating zone |
| GPU pressure indicator | gpu_pressure_label | Shows normal, elevated, or high pressure |
| Status indicator | evaluated_status | Shows normal, warning, or critical status |
| Thermal indicator | hotspot_risk | Shows low, medium, or high hotspot risk |

The visual band should help the operator immediately see whether pressure is concentrated in one zone or distributed across the hall.

## 11. Optimization Guidance Panel

The guidance panel should display summary.optimization_message prominently.

The message should be treated as operator guidance for demo explanation, not as an automatic control command.

Recommended display rules:

| Condition | UI treatment |
|---|---|
| Baseline / no issue | Display as normal advisory |
| Workload surge | Display as workload pressure guidance |
| Cooling hotspot | Display as thermal caution guidance |
| Redistribution | Display as monitoring guidance |

The panel should also include a small boundary note:

"Scenario-driven decision support only. No live scheduling or automatic workload migration is performed in Phase 1."

## 12. Scenario-Specific Screen Behavior

### 12.1 baseline_normal_operation

Expected screen reading:
- GPU load appears balanced.
- high_gpu_rack_count equals 0.
- critical_rack_count equals 0.
- all GPU pressure labels should be normal.
- optimization guidance should indicate no redistribution required.

Operator interpretation:
- The hall is stable.
- No operator action is required.
- This scenario is the reference baseline.

### 12.2 ai_workload_surge

Expected screen reading:
- GPU utilization rises across racks.
- high_gpu_rack_count equals 4.
- critical_rack_count equals 4.
- highest_gpu_rack_id should highlight the most pressured rack.
- optimization guidance should recommend shifting non-critical workload away from high-utilization racks.

Operator interpretation:
- The hall is under AI workload pressure.
- GPU pressure is concentrated enough to require attention.
- The demo should explain redistribution guidance without claiming real migration.

### 12.3 cooling_degradation_hotspot

Expected screen reading:
- Thermal and hotspot risk dominate the interpretation.
- critical_rack_count is greater than 0.
- hottest_rack_id should be emphasized.
- high_gpu_rack_count may remain lower than the workload surge scenario.
- optimization guidance should warn against adding GPU load to hotspot-affected racks.

Operator interpretation:
- Cooling degradation is the primary operational issue.
- The operator should avoid increasing workload on thermally stressed racks.
- This is not a GPU-only issue.

### 12.4 workload_redistribution

Expected screen reading:
- GPU pressure distribution changes from baseline.
- high_gpu_rack_count equals 1.
- critical_rack_count equals 0.
- guidance should indicate redistribution is active and should be monitored.

Operator interpretation:
- Redistribution state is visible.
- The system is showing a controlled scenario state.
- The screen must not imply real scheduler-driven workload movement.

## 13. Operator Language Guardrails

Use the following language:

- GPU workload pressure
- rack-level GPU utilization
- scenario-driven redistribution guidance
- decision-support screen
- synthetic telemetry prototype
- file-backed Phase 1 response

Avoid the following language:

- live GPU optimizer
- automatic workload migration
- production scheduler
- real-time Slurm control
- Kubernetes workload movement
- Omniverse-bound optimizer
- production digital twin control

## 14. UI Acceptance Criteria

The GPU screen UI definition is accepted when:

- The screen is clearly separate from the Omniverse blueprint view.
- The screen consumes GET /gpu/screen/{scenario_id}.
- The screen shows scenario_id, hall_id, and rack_count.
- KPI cards show GPU utilization, high GPU rack count, warning rack count, critical rack count, total power, hottest rack, and highest GPU rack.
- Rack table shows all 8 rack_gpu_records.
- Rack table includes gpu_util_pct, power_kw, inlet_temp_c, evaluated_status, hotspot_risk, and gpu_pressure_label.
- Guidance panel displays optimization_message.
- Baseline scenario clearly shows no redistribution required.
- Workload surge scenario clearly shows high GPU pressure.
- Cooling degradation scenario clearly shows thermal risk.
- Workload redistribution scenario clearly shows monitored redistribution state.
- UI language avoids claims of live scheduling, real workload migration, or production digital twin control.

## 15. Recommended UI Build Sequence

The recommended build sequence is:

1. Build static layout shell.
2. Connect scenario selector to supported scenario IDs.
3. Fetch GET /gpu/screen/{scenario_id}.
4. Render scenario header.
5. Render KPI summary strip.
6. Render rack GPU pressure table.
7. Render rack pressure visual band.
8. Render optimization guidance panel.
9. Add boundary note.
10. Validate all four scenarios.
11. Add fallback/error display for unknown or failed API response.
12. Capture demo evidence after validation.

## 16. Runtime Validation Plan

After UI implementation, validate the screen against:

| Validation item | Expected result |
|---|---|
| Baseline scenario | Renders 8 racks, zero high GPU racks, no redistribution guidance |
| AI workload surge | Renders high GPU rack count as 4 and critical rack count as 4 |
| Cooling degradation hotspot | Renders thermal risk and critical state emphasis |
| Workload redistribution | Renders high GPU rack count as 1 and critical rack count as 0 |
| Unknown scenario / API error | Shows controlled error state, not blank screen |
| API unavailable | Shows fallback message and does not crash |
| Boundary note | Clearly states decision-support only |

## 17. Engineering Boundary

The first implementation should be a deterministic local UI consuming the existing file-backed API.

Do not add:
- live scheduler integration
- real workload migration
- Omniverse binding
- production authentication assumptions
- external telemetry connectors
- automatic optimization action

Future enhancements can be considered only after the Phase 1 dashboard works reliably against the existing backend.

## 18. Next Recommended Step

After this UI definition is reviewed, the next controlled task should be:

- build the first separate GPU screen UI shell

The UI shell should be built against the existing backend endpoint and validated scenario by scenario.
