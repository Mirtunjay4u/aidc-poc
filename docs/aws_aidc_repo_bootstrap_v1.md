# AWS AIDC Repository Bootstrap v1

## 1. Purpose

This document defines the application-side repository bootstrap and validation sequence to run on the AWS GPU workstation once access is available.

It is a bootstrap and validation guide only.

It does not start Omniverse authoring.
It does not create or modify Omniverse scene files.
It does not change backend/API or UI code.

## 2. Current Project Checkpoint

Latest validated repo checkpoint before this bootstrap note:

- 84810f8 - Add AWS readiness evidence template

## 3. Bootstrap Rule

Run one block at a time.

Proceed to the next block only after the previous block passes.

Stop immediately if any command fails.

Do not begin Omniverse authoring from this document.

## 4. Repository Setup on AWS

After AWS workstation access is available, open a terminal on the AWS machine and run:

    cd ~
    git clone https://github.com/Mirtunjay4u/aidc-poc.git
    cd aidc-poc
    git status --short
    git status -sb
    git log --oneline -5

Expected result:

- repository clones successfully
- branch is main
- working tree is clean
- latest checkpoint matches current origin/main
- no local edits are present before validation begins

## 5. Static Validation on AWS

After repository setup passes, run static validation on the AWS machine:

    cd ~/aidc-poc
    python3 -m py_compile api/app_v1.py
    bash -n scripts/start_api_v1.sh
    bash -n scripts/smoke_test_api_v1.sh
    python3 -m py_compile tests/validate_scenario_acceptance_v1.py
    python3 tests/validate_scenario_acceptance_v1.py

Expected result:

- api/app_v1.py compiles successfully
- startup script syntax passes
- smoke test script syntax passes
- scenario acceptance validation script compiles successfully
- all four Phase 1 scenarios pass acceptance validation

## 6. Runtime Startup Validation

After static validation passes, start the API in Terminal 1 on the AWS machine:

    cd ~/aidc-poc
    bash scripts/start_api_v1.sh

Expected result:

- Python dependency check passes
- Uvicorn starts successfully
- startup validation checks all required scenario response files
- startup validation passes with scenario_count = 4
- structured log event api_ready appears
- API listens on port 8000

Keep Terminal 1 running for the smoke test.

## 7. Runtime Smoke Validation

With the API still running in Terminal 1, open Terminal 2 on the AWS machine and run:

    cd ~/aidc-poc
    bash scripts/smoke_test_api_v1.sh

Expected result:

- /health returns HTTP 200 and healthy status
- /scenarios returns HTTP 200 and scenario count = 4
- baseline hall summary passes
- baseline GPU screen API passes
- workload surge GPU screen API passes
- /gpu/screen-ui route returns HTTP 200
- GPU screen UI title is present
- scenario current/start/reset checks pass
- unknown scenario negative-path checks return expected 404 responses
- smoke test completes successfully

## 8. GPU Screen Browser Review on AWS

After runtime smoke validation passes, review the GPU screen from the AWS remote desktop or approved browser path:

    http://127.0.0.1:8000/gpu/screen-ui

If the browser is outside the AWS workstation, use the approved DCV, tunnel, or remote-access path provided by infrastructure.

Review all four scenarios:

- baseline_normal_operation
- ai_workload_surge
- cooling_degradation_hotspot
- workload_redistribution

Expected result:

- scenario selector works
- KPI cards populate
- rack pressure table shows 8 racks
- rack visual band renders
- optimization guidance updates by scenario
- boundary note remains visible
- no live scheduler or real workload migration claim is shown

## 9. Evidence Capture

Save AWS bootstrap and validation outputs under:

    evidence/aws_readiness_validation_evidence_v1/

Recommended mapping:

| Validation area | Evidence file |
|---|---|
| AWS host identity | aws_host_identity.txt |
| Repo clone and checkpoint verification | repo_validation_output.txt |
| Static validation | aidc_static_validation_output.txt |
| Runtime smoke validation | aidc_smoke_test_output.txt |
| GPU screen browser review | gpu_screen_browser_review.md |
| Shutdown and cost control | shutdown_cost_control_confirmation.md |

Update this manifest after evidence is captured:

    evidence/aws_readiness_validation_evidence_v1/evidence_manifest_aws_readiness_v1.md

Only mark a gate passed when evidence is saved and reviewed.

## 10. Shutdown and Process Safety

After smoke and browser validation, stop the API in Terminal 1 using CTRL+C.

Then run this check on the AWS machine:

    cd ~/aidc-poc
    ps -ef | grep -E "uvicorn|api.app_v1" | grep -v grep || true
    git status --short
    git status -sb

Expected result:

- no Uvicorn or api.app_v1 process remains
- repository is clean unless evidence files were intentionally updated
- any evidence updates are limited to evidence/aws_readiness_validation_evidence_v1/
- shutdown and cost-control confirmation is recorded before leaving the GPU workstation idle

## 11. Authoring Gate

AIDC Omniverse authoring may begin only after AWS readiness gates pass and evidence is reviewed.

Until then:

- do not create AIDC Omniverse scene files
- do not modify scene assets
- do not claim production digital twin behavior
- do not claim live scheduler behavior
- do not claim live DCIM/BMS integration
- do not claim certified thermal simulation

## 12. Next Step

After AWS repo bootstrap validation passes, continue with:

    docs/aws_readiness_validation_command_pack_v1.md

Save all AWS validation outputs into:

    evidence/aws_readiness_validation_evidence_v1/

Then update the evidence manifest and project report/tracker only after the validation evidence is reviewed.
