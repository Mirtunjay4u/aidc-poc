# Separate GPU Screen Scope v1

## Purpose
Define the Phase 1 separate AI workload / GPU optimization screen before implementation. This screen is separate from the Omniverse hall blueprint and should use the existing validated synthetic telemetry and scenario outputs.

## Scope boundary
The Phase 1 GPU screen is a backend/demo support screen, not a production GPU scheduler. It should summarize GPU workload pressure, rack-level utilization, power impact, and redistribution guidance using file-backed synthetic scenario data.

## In scope
- Use existing Phase 1 scenario data.
- Use existing rack-level telemetry records.
- Show current scenario context.
- Show GPU utilization by rack.
- Show rack power draw alongside GPU utilization.
- Show evaluated rack status.
- Highlight high-utilization racks.
- Provide a simple optimization/redistribution recommendation for demo storytelling.
- Support all four Phase 1 scenarios:
  - baseline_normal_operation
  - ai_workload_surge
  - cooling_degradation_hotspot
  - workload_redistribution

## Out of scope
- No live DCIM integration.
- No live GPU scheduler integration.
- No Kubernetes, Slurm, or cluster scheduler integration.
- No real workload migration.
- No predictive optimization model.
- No Omniverse scene binding in this step.
- No production dashboard implementation in this step.

## Existing data inputs
The GPU screen should initially derive from existing rack response artifacts under tests/:

- tests/{scenario_id}_rack_records_response_v1.json
- tests/{scenario_id}_hall_summary_v1.json
- tests/current_scenario_state_v1.json

Available rack fields:
- rack_id
- zone_id
- timestamp
- inlet_temp_c
- power_kw
- gpu_util_pct
- cooling_health
- hotspot_risk
- status
- evaluated_status

Available hall summary fields:
- scenario_id
- hall_id
- rack_count
- status_counts
- max_inlet_temp_c
- max_power_kw
- max_gpu_util_pct

## Proposed GPU screen summary fields
The first GPU screen response should include:

- scenario_id
- hall_id
- rack_count
- avg_gpu_util_pct
- max_gpu_util_pct
- min_gpu_util_pct
- high_gpu_rack_count
- critical_rack_count
- warning_rack_count
- total_power_kw
- max_power_kw
- hottest_rack_id
- highest_gpu_rack_id
- optimization_message

## Proposed rack-level display fields
Each rack row should include:

- rack_id
- zone_id
- gpu_util_pct
- power_kw
- inlet_temp_c
- evaluated_status
- hotspot_risk
- gpu_pressure_label

## Proposed GPU pressure labels
Use a simple Phase 1 rule:

- normal: gpu_util_pct < 70
- elevated: gpu_util_pct >= 70 and gpu_util_pct < 85
- high: gpu_util_pct >= 85

## Proposed optimization message logic
Use simple deterministic text for the Phase 1 demo:

- baseline_normal_operation:
  "GPU load is balanced. No redistribution required."
- ai_workload_surge:
  "GPU load surge detected. Consider shifting non-critical workload away from high-utilization racks."
- cooling_degradation_hotspot:
  "Thermal risk is dominant. Avoid adding GPU load to hotspot-affected racks."
- workload_redistribution:
  "Workload redistribution is active. Monitor shifted load and confirm rack status remains within warning bounds."

## Proposed implementation sequence
1. Create GPU screen scope definition. This document.
2. Create GPU screen schema definition.
3. Build file-backed GPU screen response generator.
4. Generate GPU screen response artifacts for all four scenarios.
5. Add read-only API endpoint for GPU screen data.
6. Extend smoke test.
7. Update README/runbook/status docs.

## Proposed endpoint after implementation
GET /gpu/screen/{scenario_id}

## Completion condition for definition step
This definition step is complete when the scope, data inputs, proposed response fields, display fields, pressure labels, and implementation sequence are documented and reviewed.
