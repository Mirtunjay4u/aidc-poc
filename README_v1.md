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

## Current checkpoint extension - 3ba5d56

Omniverse Scene Specification v1 is complete in `docs/omniverse_scene_specification_v1.md`.

Current completed scope now includes the Brev backend/API foundation, scenario controller, scenario acceptance validation, structured logging, GPU screen backend/API, browser-reviewed GPU screen UI shell, health endpoint inventory alignment, and Omniverse scene specification.

Formal Phase 1 demo evidence packaging is now complete under `evidence/phase1_demo_evidence_pack_v1/`. The next controlled focus is evidence review, optional screenshot enrichment, GPU UI polish only if needed, and Santa Clara RTX readiness follow-up. Omniverse authoring should not start until workstation access, permissions, Omniverse toolchain readiness, and OpenUSD authoring path are confirmed.

## Current checkpoint extension - 6aba416

Formal Phase 1 demo evidence pack is complete in `evidence/phase1_demo_evidence_pack_v1/`.

The evidence pack includes endpoint samples, smoke-test output, GPU screen UI HTML/status evidence, structured API runtime logs, shutdown evidence, fallback/access notes, evidence manifest, and screenshot placeholders for future browser captures.

Current next focus is AWS GPU workstation readiness validation, evidence review, optional screenshot enrichment, and continued Santa Clara RTX readiness follow-up.

## Current checkpoint extension - 7cd26fb

AWS GPU Workstation Readiness Specification v1 is complete in `docs/aws_gpu_workstation_readiness_v1.md`.

This document defines the interim AWS GPU workstation path for Omniverse/OpenUSD authoring while Santa Clara RTX access is delayed. It covers the recommended EC2 G5-class baseline, preferred `g5.4xlarge` or higher starting point, NVIDIA A10G 24 GB or equivalent GPU expectation, NVIDIA driver/graphics stack, Amazon DCV or approved remote desktop, Omniverse Kit/USD Composer/OpenUSD tooling, GitHub/file transfer access, validation gates, security controls, cost-control expectations, and responsibility split.

Omniverse authoring should not start until the AWS workstation passes readiness validation, including GPU visibility, remote graphics, Omniverse/OpenUSD launch, sample USD render, GitHub access, and file transfer validation.

