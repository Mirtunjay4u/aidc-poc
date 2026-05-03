# Omniverse Scene Specification v1

## 1. Document Control

| Field | Value |
|---|---|
| Project | AIDC Phase 1 |
| Document | Omniverse Scene Specification v1 |
| Environment | NVIDIA Brev for backend/API; Santa Clara RTX workstation for Omniverse authoring |
| Latest Git checkpoint | 61d4070 - List GPU screen UI in health response |
| Primary use case | AI Data Centre Blueprint on Omniverse for Santa Clara lab demonstration |
| Supporting flow | Separate AI workload and GPU resource optimization screen |
| Purpose | Define Omniverse scene structure, rack mapping, visual state model, telemetry binding approach, camera/storyboard plan, and authoring boundary before Santa Clara RTX scene work |

## 2. Objective

This document defines the target Omniverse scene specification for the AIDC Phase 1 demonstration.

The purpose is to prepare the scene authoring package before Santa Clara RTX workstation access and Omniverse authoring begins.

The specification must support:

- a representative AI data centre hall view
- 8 rack objects matching the backend rack model
- scenario-driven visual state changes
- thermal, power, and GPU pressure interpretation
- operator walkthrough storytelling
- alignment with existing backend APIs and scenario acceptance rules
- clear separation between the Omniverse blueprint view and the separate GPU screen UI

The Omniverse scene is intended to be a visual blueprint and scenario interpretation layer. It is not a production digital twin, not a live facility control system, and not a certified thermal simulation model.

## 3. Phase 1 Scope Boundary

### 3.1 In Scope

- Representative hall or room scene
- 8 deterministic rack objects
- Compute, cooling, and power zone context
- Scenario-driven rack visual states
- Visual mapping for normal, warning, and critical rack status
- Basic telemetry overlay labels
- Camera positions for guided walkthrough
- Storyboard for demo narration
- API-to-scene mapping specification
- Asset checklist for Santa Clara RTX authoring
- Validation criteria for scene readiness

### 3.2 Out of Scope

- Live DCIM/BMS integration
- Live Redfish, Kubernetes, Slurm, or scheduler integration
- Real workload migration
- Automatic control action
- Computational fluid dynamics
- Certified thermal modelling
- Production digital twin claim
- Real facility control
- Real-time streaming telemetry beyond deterministic Phase 1 scenario data

## 4. Source System and Data Boundary

The Omniverse scene should be designed against the existing Phase 1 backend/API model.

| Source | Current role |
|---|---|
| GET /health | Confirms API service health and endpoint inventory |
| GET /scenarios | Lists supported Phase 1 scenarios |
| GET /hall/summary/{scenario_id} | Provides hall-level scenario summary |
| GET /hall/racks/{scenario_id} | Provides rack-level evaluated telemetry |
| GET /scenario/current | Provides current scenario controller state |
| POST /scenario/{scenario_id}/start | Updates file-backed current scenario state |
| POST /scenario/reset | Resets file-backed current scenario state |
| GET /gpu/screen/{scenario_id} | Feeds the separate GPU screen UI |
| GET /gpu/screen-ui | Serves the separate GPU screen UI shell |

For Phase 1, Omniverse should consume or mirror deterministic scenario outputs. It should not claim live operational telemetry.

## 5. Scene Concept

The scene should represent one AI data centre hall with eight racks distributed across functional zones.

Recommended visual concept:

- one rectangular hall shell
- two rows of rack objects
- four compute-facing racks
- two cooling-context racks
- two power-context racks
- overhead or angled camera view for blueprint storytelling
- optional side camera for rack-level detail
- color-coded rack state overlay
- simple labels showing rack ID, status, and primary metric signal

The visual objective is to let a visitor understand scenario impact within seconds.

## 6. Scene Hierarchy

Recommended OpenUSD-style scene hierarchy:

- /World
- /World/AIDC_Hall
- /World/AIDC_Hall/Floor
- /World/AIDC_Hall/Walls
- /World/AIDC_Hall/Zones
- /World/AIDC_Hall/Zones/Compute_Zone
- /World/AIDC_Hall/Zones/Cooling_Zone
- /World/AIDC_Hall/Zones/Power_Zone
- /World/AIDC_Hall/Racks
- /World/AIDC_Hall/Racks/R01
- /World/AIDC_Hall/Racks/R02
- /World/AIDC_Hall/Racks/R03
- /World/AIDC_Hall/Racks/R04
- /World/AIDC_Hall/Racks/R05
- /World/AIDC_Hall/Racks/R06
- /World/AIDC_Hall/Racks/R07
- /World/AIDC_Hall/Racks/R08
- /World/AIDC_Hall/Overlays
- /World/AIDC_Hall/Overlays/Scenario_Label
- /World/AIDC_Hall/Overlays/Legend
- /World/AIDC_Hall/Cameras
- /World/AIDC_Hall/Cameras/Overview_Camera
- /World/AIDC_Hall/Cameras/Rack_Detail_Camera
- /World/AIDC_Hall/Cameras/Scenario_Impact_Camera

## 7. Rack Naming and Identity Mapping

Rack identity must match the backend exactly.

| Backend rack_id | Scene prim name | Recommended display label | Zone |
|---|---|---|---|
| R01 | /World/AIDC_Hall/Racks/R01 | R01 | compute |
| R02 | /World/AIDC_Hall/Racks/R02 | R02 | compute |
| R03 | /World/AIDC_Hall/Racks/R03 | R03 | compute |
| R04 | /World/AIDC_Hall/Racks/R04 | R04 | compute |
| R05 | /World/AIDC_Hall/Racks/R05 | R05 | cooling |
| R06 | /World/AIDC_Hall/Racks/R06 | R06 | cooling |
| R07 | /World/AIDC_Hall/Racks/R07 | R07 | power |
| R08 | /World/AIDC_Hall/Racks/R08 | R08 | power |

The rack IDs must not be renamed during scene authoring. API-to-scene mapping depends on exact identity consistency.

## 8. Suggested Rack Layout

Recommended initial layout:

| Rack | Row | Relative position | Zone |
|---|---|---|---|
| R01 | Row A | A1 | compute |
| R02 | Row A | A2 | compute |
| R03 | Row A | A3 | compute |
| R04 | Row A | A4 | compute |
| R05 | Row B | B1 | cooling |
| R06 | Row B | B2 | cooling |
| R07 | Row B | B3 | power |
| R08 | Row B | B4 | power |

The layout should be simple, readable, and optimized for demonstration clarity rather than exact physical facility replication.

## 9. Visual State Model

The Omniverse scene should use the same operational interpretation already defined in the backend artifacts.

### 9.1 Rack evaluated status

| evaluated_status | Visual treatment | Interpretation |
|---|---|---|
| normal | Green rack accent or glow | Normal operating state |
| warning | Amber rack accent or glow | Review or monitor condition |
| critical | Red rack accent or glow | Critical scenario condition requiring attention |

### 9.2 Hotspot risk

| hotspot_risk | Visual treatment | Interpretation |
|---|---|---|
| low | No heat plume or subtle blue/neutral thermal indicator | Low hotspot concern |
| medium | Amber thermal marker | Elevated hotspot watch condition |
| high | Red thermal marker or heat plume | Thermal risk dominates |

### 9.3 GPU pressure

| gpu_pressure_label | Visual treatment | Interpretation |
|---|---|---|
| normal | No additional GPU pressure marker | GPU load within expected range |
| elevated | Amber GPU badge or bar | Elevated GPU pressure |
| high | Red GPU badge or bar | High GPU pressure scenario |

## 10. Scenario Visual Mapping

### 10.1 baseline_normal_operation

Expected scene reading:

- All racks should appear normal.
- No critical or warning rack state should dominate.
- Guidance should support balanced operation narrative.
- Scene should visually communicate stable baseline operation.

| Rack group | Expected visual |
|---|---|
| R01-R08 | Green or neutral normal state |
| Thermal markers | Low or none |
| GPU pressure markers | Normal or none |
| Visitor interpretation | Hall is stable and balanced |

### 10.2 ai_workload_surge

Expected scene reading:

- GPU pressure rises across the highest-utilization racks.
- Racks with critical status should become visually prominent.
- The scene should show AI workload pressure rather than cooling failure.
- Power draw and GPU utilization should be highlighted.

| Rack group | Expected visual |
|---|---|
| High GPU racks | Red or high GPU pressure marker |
| Warning racks | Amber status marker |
| Critical racks | Red status marker |
| Visitor interpretation | AI workload surge is stressing selected racks |

### 10.3 cooling_degradation_hotspot

Expected scene reading:

- Thermal risk dominates the scene.
- Critical rack status appears due to cooling degradation or hotspot.
- GPU pressure may not be the primary driver.
- Heat or thermal overlays should be more prominent than GPU-only markers.

| Rack group | Expected visual |
|---|---|
| Hotspot-affected racks | Red thermal marker or heat plume |
| Critical racks | Red status marker |
| GPU pressure | May show normal or elevated depending on rack |
| Visitor interpretation | Cooling risk is the primary concern |

### 10.4 workload_redistribution

Expected scene reading:

- Load has shifted across the hall.
- Some racks are warning or elevated but not necessarily critical.
- The screen should support a monitored redistribution narrative without claiming real migration.
- Visual state should show redistributed pressure, not automatic control.

| Rack group | Expected visual |
|---|---|
| Highest GPU rack | High GPU marker |
| Warning racks | Amber status marker |
| Normal racks | Green or neutral status |
| Visitor interpretation | Redistributed state is visible and monitored |

## 11. Telemetry-to-Scene Binding Map

The following fields should drive scene display logic.

| API field | Scene usage |
|---|---|
| scenario_id | Scenario label and storyboard context |
| hall_id | Hall label |
| rack_id | Rack prim mapping |
| zone_id | Zone label and grouping |
| evaluated_status | Primary rack status color |
| gpu_util_pct | GPU bar, badge, or rack overlay |
| gpu_pressure_label | GPU pressure marker |
| power_kw | Power label or optional power intensity marker |
| inlet_temp_c | Thermal label or heat intensity marker |
| hotspot_risk | Thermal marker severity |

## 12. Scene Overlay Requirements

Minimum overlay elements:

- current scenario label
- legend for normal, warning, critical
- legend for hotspot risk
- selected rack label
- optional hall summary panel
- boundary note stating synthetic scenario data

Recommended boundary note:

Phase 1 synthetic scenario visualization. Not live facility control, not certified thermal simulation, and not automatic workload migration.

## 13. Camera and Storyboard Plan

### 13.1 Overview camera

Purpose:

- establish the full AI data centre hall
- show all 8 racks and zone grouping
- support executive-level visual orientation

Expected use:

- opening shot
- baseline scenario
- transition between scenarios

### 13.2 Rack detail camera

Purpose:

- focus on affected racks
- show rack ID, status, GPU pressure, and thermal markers

Expected use:

- workload surge
- cooling hotspot
- critical rack explanation

### 13.3 Scenario impact camera

Purpose:

- show before and after impact from scenario switch
- support operator narration

Expected use:

- scenario start
- redistribution story
- demo walkthrough conclusion

## 14. Demo Storyline Alignment

Recommended walkthrough sequence:

1. Open with baseline hall view.
2. Explain synthetic, deterministic Phase 1 scenario boundary.
3. Trigger or select baseline_normal_operation.
4. Show all racks normal and stable.
5. Trigger or select ai_workload_surge.
6. Show high GPU pressure and critical or warning rack interpretation.
7. Trigger or select cooling_degradation_hotspot.
8. Show thermal risk as dominant.
9. Trigger or select workload_redistribution.
10. Show redistributed load and monitored state.
11. Open separate GPU screen UI to show detailed KPI, table, and guidance view.
12. Close with roadmap to Omniverse telemetry binding and Santa Clara RTX authoring.

## 15. Materials and Color Guidance

Recommended color semantics:

| Meaning | Color family |
|---|---|
| Normal | Green |
| Warning | Amber |
| Critical | Red |
| Neutral hall structure | Dark grey, graphite, or muted industrial material |
| Compute zone | Blue or cool accent |
| Cooling zone | Cyan or blue accent |
| Power zone | Purple or amber accent |
| Scenario highlight | White or electric blue outline |

Avoid overly saturated colors that make labels unreadable. The scene should be polished but operationally clear.

## 16. Asset Checklist

Minimum required assets:

- hall floor plane
- wall or room boundary
- 8 rack models
- rack labels R01-R08
- zone labels
- status legend
- thermal marker asset
- GPU pressure marker asset
- scenario label panel
- overview camera
- rack detail camera
- scenario impact camera

Optional assets:

- cable tray
- cooling unit representation
- power distribution representation
- aisle arrows
- overhead lighting
- simple operator viewpoint marker

## 17. Authoring Prerequisites

Before Santa Clara RTX Omniverse authoring starts, confirm:

- RTX workstation access is available
- user account and permissions are ready
- Omniverse tooling is installed or installable
- OpenUSD authoring path is confirmed
- repository or asset handoff location is agreed
- scene specification is reviewed
- rack naming convention is frozen
- scenario visual state mapping is approved
- fallback demo path remains available from Brev

## 18. Validation Criteria

The Omniverse scene specification is accepted when:

- all 8 backend rack IDs are represented in the scene
- rack IDs match backend rack_id values exactly
- normal, warning, and critical visual states are defined
- hotspot risk visual treatment is defined
- GPU pressure visual treatment is defined
- all four Phase 1 scenarios have expected visual interpretation
- camera/storyboard plan supports leadership walkthrough
- scene boundary language avoids production digital twin overclaim
- scene authoring prerequisites are listed before Santa Clara RTX work

## 19. Implementation Boundary

Do not implement Omniverse scene authoring inside the Brev backend task unless the environment is explicitly confirmed as suitable for Omniverse authoring.

Do not claim:

- live telemetry
- production digital twin
- real workload migration
- live scheduler integration
- real facility control
- certified thermal simulation
- automated remediation

Use the following approved language:

- deterministic scenario visualization
- synthetic telemetry
- operational decision-support view
- representative hall blueprint
- Phase 1 file-backed prototype
- Omniverse-ready scene specification

## 20. Next Recommended Step

After this specification is reviewed, the next controlled task should be:

- align README, backend status, validation summary, and tracker/report language to show Omniverse scene specification v1 is complete
- prepare a demo evidence pack structure for screenshots, logs, endpoint samples, and UI/scene validation evidence
- continue Santa Clara RTX readiness follow-up before authoring work begins
