# Thermal and Power Threshold Rationale v1

## 1. Document Control

| Field | Value |
|---|---|
| Project | AIDC Phase 1 |
| Document | Thermal and Power Threshold Rationale v1 |
| Environment | NVIDIA Brev |
| Implementation mode | File-backed deterministic scenario prototype |
| Primary use case | Datacentre Blueprint on Omniverse |
| Supporting flow | Separate AI workload and GPU resource optimization screen |
| Current Git checkpoint | 690a44c - Add API contract v2 documentation |
| Purpose | Explain Phase 1 thermal, power, GPU, cooling, hotspot, and evaluated-status assumptions |

## 2. Objective

This document explains the rationale for the Phase 1 telemetry signals and threshold-style behavior used in the AIDC prototype.

The purpose is to make the current implementation technically defensible by clearly separating:

- deterministic demo assumptions
- operationally meaningful signals
- current Phase 1 limitations
- future production validation requirements

This document does not claim that the current thresholds are certified production thermal limits, ASHRAE design envelopes, live DCIM thresholds, or GPU scheduler policies.

## 3. Current Phase 1 Position

Phase 1 is a synthetic telemetry and scenario-driven operational prototype.

The current implementation uses file-backed JSON artifacts to represent:

- rack inlet temperature
- rack power draw
- GPU utilization
- cooling health
- hotspot risk
- rules-engine evaluated status
- GPU pressure label
- scenario-specific optimization guidance

These values support a credible demo flow, but they remain deterministic prototype assumptions until live infrastructure data, validated environmental limits, and formal engineering thresholds are introduced.

## 4. Signals Covered

| Signal | Current field | Why it is used |
|---|---|---|
| Rack inlet temperature | inlet_temp_c | Represents thermal condition at rack inlet and supports hotspot/cooling degradation scenarios |
| Rack power draw | power_kw | Represents rack-level electrical load and supports workload/power impact storytelling |
| GPU utilization | gpu_util_pct | Represents AI workload pressure and supports the separate GPU screen |
| Cooling health | cooling_health | Represents qualitative cooling condition for scenario interpretation |
| Hotspot risk | hotspot_risk | Represents simplified thermal risk state for demo storytelling |
| Evaluated rack status | evaluated_status | Represents rules-engine classification into normal, warning, or critical |
| GPU pressure label | gpu_pressure_label | Represents GPU utilization pressure classification for the separate GPU screen |

## 5. Scope Boundary

### 5.1 In Scope

This rationale covers:

- why the selected telemetry fields are useful for Phase 1
- how they support the four deterministic scenarios
- how they support hall summary, rack records, and GPU screen responses
- why thresholds are treated as demo assumptions
- what must be validated before any production claim

### 5.2 Out of Scope

This rationale does not define:

- production thermal operating envelope
- ASHRAE compliance boundary
- CFD model
- live BMS/DCIM integration rule
- live GPU scheduler policy
- Kubernetes or Slurm scheduling threshold
- automatic workload migration logic
- real facility alarm configuration

## 6. Signal Rationale

### 6.1 inlet_temp_c

Rack inlet temperature is used because it is an intuitive and operationally meaningful signal for rack thermal condition. In Phase 1, it helps demonstrate normal operation, cooling degradation, and hotspot scenarios.

Current use:
- show normal thermal condition in baseline
- show elevated thermal condition in cooling degradation
- support identification of the hottest rack
- support operator interpretation of thermal risk

Phase 1 limitation:
- values are synthetic and scenario-driven
- values are not certified facility thermal limits
- values are not derived from live sensors or BMS/DCIM data

Future requirement:
- align with facility environmental guidelines
- validate against real sensor data
- calibrate against site-specific operating envelopes

### 6.2 power_kw

Rack power draw is used because AI workload pressure usually has an operational relationship with electrical load and cooling demand. In Phase 1, it supports the workload surge and redistribution story.

Current use:
- show baseline rack power condition
- show higher rack load during AI workload surge
- show redistribution effect across racks
- support total_power_kw and max_power_kw in GPU screen response

Phase 1 limitation:
- values are synthetic rack-level demo values
- values are not metered from live electrical infrastructure
- values do not represent a production power capacity model

Future requirement:
- integrate with real power telemetry
- map rack load to facility electrical constraints
- validate against electrical design and operational thresholds

### 6.3 gpu_util_pct

GPU utilization is used because the supporting flow is a separate AI workload and GPU resource optimization screen. It provides the clearest signal for AI workload pressure in the Phase 1 demo.

Current use:
- classify GPU pressure as normal, elevated, or high
- identify high-utilization racks
- support high_gpu_rack_count
- support workload surge and redistribution scenarios
- drive scenario-specific optimization guidance

Phase 1 limitation:
- values are deterministic synthetic assumptions
- no live GPU telemetry is connected
- no production GPU scheduler is controlled

Future requirement:
- connect to approved live GPU telemetry source
- validate utilization thresholds with operations and platform teams
- define whether scheduler data comes from Slurm, Kubernetes, DCGM, or another approved system

### 6.4 cooling_health

Cooling health is used as a simplified qualitative state to support scenario interpretation. It helps the demo communicate whether the thermal condition is normal, degraded, or under stress.

Current use:
- support baseline healthy state
- support cooling degradation storyline
- support thermal risk explanation

Phase 1 limitation:
- qualitative and synthetic
- not connected to live cooling plant, BMS, or CRAC/CRAH data
- not a production fault diagnosis indicator

Future requirement:
- define mapping to real cooling system telemetry
- align state labels with facility operations terminology
- validate with data centre operations stakeholders

### 6.5 hotspot_risk

Hotspot risk is used as a simplified risk indicator for thermal storytelling. It allows the demo to highlight racks where additional load should be avoided.

Current use:
- low risk in baseline
- medium or high risk during stress scenarios
- supports cooling_degradation_hotspot interpretation
- supports GPU screen optimization message

Phase 1 limitation:
- simplified scenario label
- not computed through CFD
- not derived from live thermal maps

Future requirement:
- validate with real thermal monitoring approach
- decide whether hotspot risk should come from sensor data, CFD, rules, or model-based inference
- define escalation logic for production use

### 6.6 evaluated_status

Evaluated status is the current rules-engine output. It provides a simple normal, warning, or critical classification for rack-level operational state.

Current use:
- aggregate rack state into hall status counts
- support rack-level response records
- support scenario acceptance validation
- support GPU screen warning and critical rack counts

Phase 1 limitation:
- rules are deterministic and demo-oriented
- not an enterprise alarm model
- not a production incident severity model

Future requirement:
- align rules with operational severity definitions
- validate thresholds with facilities and platform engineering
- map status levels to alerting or visualization standards

### 6.7 gpu_pressure_label

GPU pressure label is the separate GPU screen classification derived from GPU utilization.

Current Phase 1 rule:
- normal: gpu_util_pct < 70
- elevated: gpu_util_pct >= 70 and gpu_util_pct < 85
- high: gpu_util_pct >= 85

Current use:
- support separate GPU screen display
- support high_gpu_rack_count
- make GPU utilization easier for leadership and operator review

Phase 1 limitation:
- simple deterministic label
- not a production scheduler threshold
- not an SLA/SLO threshold

Future requirement:
- validate utilization bands with GPU operations stakeholders
- align to real workload profiles and platform policy
- include workload priority and thermal headroom if moving toward production design

## 7. Scenario-Level Interpretation

### 7.1 baseline_normal_operation

Baseline represents stable operating behavior.

Expected interpretation:
- normal rack temperature
- normal rack power draw
- normal GPU utilization
- low hotspot risk
- no redistribution action required

Engineering meaning:
- establishes a clean reference point
- proves the system can represent non-stressed operation
- prevents every scenario from looking like an alert condition

### 7.2 ai_workload_surge

AI workload surge represents increased compute demand.

Expected interpretation:
- GPU utilization rises
- rack power draw rises
- warning and critical states appear
- high GPU rack count increases
- redistribution guidance is triggered

Engineering meaning:
- demonstrates cause and effect between workload pressure and rack stress
- supports the separate GPU screen decision-support flow
- does not claim live workload movement or scheduler control

### 7.3 cooling_degradation_hotspot

Cooling degradation / hotspot represents thermal stress.

Expected interpretation:
- inlet temperature rises
- cooling health degrades
- hotspot risk increases
- critical rack count appears because thermal risk is dominant

Engineering meaning:
- demonstrates that thermal risk can dominate even when GPU utilization is not the highest scenario driver
- supports operator guidance to avoid adding GPU load to hotspot-affected racks
- does not claim CFD-grade thermal modeling

### 7.4 workload_redistribution

Workload redistribution represents a controlled shifted-load state.

Expected interpretation:
- GPU utilization distribution changes across racks
- some pressure remains visible
- critical rack count remains controlled
- operator monitors shifted load

Engineering meaning:
- demonstrates the concept of redistribution state
- does not claim actual live workload migration
- does not imply Kubernetes, Slurm, or scheduler integration

## 8. Current Threshold Boundary

The current threshold behavior is acceptable for Phase 1 because it is:

- deterministic
- repeatable
- easy to validate
- aligned to the four demo scenarios
- visible through API responses and smoke tests
- suitable for leadership and technical walkthrough

The current threshold behavior is not yet:

- site-certified
- ASHRAE-validated
- derived from live facilities telemetry
- connected to live power meters
- connected to live GPU scheduler data
- approved for production alerting
- approved for automatic control action

## 9. Production Qualification Requirements

Before this logic can support any production or real infrastructure claim, the following must be addressed:

| Area | Required future validation |
|---|---|
| Thermal thresholds | Validate against site environmental policy, rack inlet sensor data, and data centre operations guidance |
| Power thresholds | Validate against rack power metering, electrical design capacity, and operational constraints |
| GPU utilization thresholds | Validate against actual workload profiles, platform policy, and GPU operations expectations |
| Cooling health | Map to real BMS/DCIM/cooling system signals |
| Hotspot risk | Define whether risk is rule-based, sensor-based, CFD-based, or model-based |
| Evaluated status | Align normal/warning/critical levels with operational severity definitions |
| Optimization message | Review with operations team to avoid implying automatic control or live scheduler action |

## 10. Language Guardrails

Use the following language:

- scenario-driven thermal and power indicators
- deterministic Phase 1 threshold assumptions
- GPU workload pressure and redistribution guidance
- separate GPU decision-support screen
- file-backed operational prototype

Avoid the following language:

- production digital twin
- live GPU optimizer
- automatic workload migration
- certified thermal model
- live facility control
- Omniverse-bound optimization engine

## 11. Current Engineering Position

The current implementation is appropriate for Phase 1 because it gives the team a repeatable, explainable, scenario-driven operating model.

It is strong enough for:
- local technical walkthrough
- leadership demonstration
- scenario acceptance validation
- backend-only fallback demo
- preparation for future Omniverse visualization

It still requires future validation before:
- production use
- live telemetry integration
- real facility alarm mapping
- scheduler integration
- Omniverse scene control
- operational decision automation

## 12. Next Recommended Step

After this rationale is reviewed, the next engineering-quality artifact should be:

- observability_event_model_v1.md

That document should define expected event names and log fields for startup, validation, scenario start/reset, GPU screen request, unknown scenario request, and shutdown.
