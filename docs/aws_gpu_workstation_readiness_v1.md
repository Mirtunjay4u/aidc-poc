# AWS GPU Workstation Readiness Specification v1

## 1. Document Control

| Field | Value |
|---|---|
| Project | AIDC Phase 1 |
| Document | AWS GPU Workstation Readiness Specification v1 |
| Latest Git checkpoint before creation | 614fdd4 - Align documentation for demo evidence pack |
| Current development base | NVIDIA Brev backend/API development and validation environment |
| Interim visual authoring path | AWS GPU remote workstation |
| Deferred path | Santa Clara RTX workstation, currently unavailable until later date |
| Purpose | Define the minimum AWS infrastructure, toolchain, validation gates, security controls, and responsibility split required before Omniverse authoring begins |

## 2. Objective

This document defines the minimum AWS GPU workstation readiness requirements for continuing AIDC Phase 1 Omniverse authoring and remote demo preparation while Santa Clara RTX workstation access is not yet available.

The objective is to support a workable Phase 1 demo with:

- validated backend/API and scenario controller
- separate GPU decision-support screen
- Omniverse/OpenUSD representative hall authoring
- R01-R08 rack and zone mapping
- scenario-driven visual state changes
- remote review and demo access
- evidence capture and controlled shutdown

AWS is an interim authoring and demo-hosting path. It does not change the Phase 1 scope boundary.

## 3. Current Completed Baseline

The following work is already complete before AWS setup:

- Brev backend/API foundation
- scenario controller
- hall summary and rack APIs
- separate GPU screen backend/API
- GPU screen UI shell
- browser-level GPU UI review
- structured API event logging
- scenario acceptance validation
- API Contract v2
- thermal/power threshold rationale
- Omniverse Scene Specification v1
- formal Phase 1 demo evidence pack

Latest completed repository checkpoint:

- 614fdd4 - Align documentation for demo evidence pack

## 4. Recommended AWS Instance Baseline

Minimum recommended AWS instance class:

| Requirement | Recommendation |
|---|---|
| Instance family | EC2 G5 class or equivalent GPU workstation instance |
| Preferred starting size | g5.4xlarge or higher |
| GPU | NVIDIA A10G 24 GB or equivalent RTX-capable GPU |
| CPU/RAM | Enough for Omniverse authoring, browser review, and local API validation |
| Storage | Minimum 250 GB recommended for tools, repo, assets, screenshots, and scene outputs |
| Operating system | Ubuntu 22.04 LTS or Windows workstation image |

Smaller G5 sizes may be used for smoke validation, but g5.4xlarge or higher is preferred for actual Omniverse authoring and smoother remote review.

## 5. Required Toolchain

The AWS workstation must include or support installation of:

- NVIDIA driver from AWS/CSP-supported path
- NVIDIA RTX/GRID graphics driver where required for virtual workstation graphics
- Amazon DCV or approved remote desktop/streaming access
- Omniverse Kit, USD Composer, or approved current Omniverse/OpenUSD authoring tools
- OpenUSD support
- Git
- Python 3
- shell tools required for repo validation
- browser access for GPU screen UI review
- screenshot or screen recording capability

Optional but useful:

- AWS CLI
- S3 access for artifact transfer
- NGC access if required for NVIDIA tools
- VS Code or approved remote editor
- file compression/extract tools

## 6. Network, Access, and Security Requirements

Infrastructure team should confirm:

- AWS account and region
- G5 or equivalent GPU instance quota
- approved subnet/VPC placement
- security group rules
- VPN or corporate access path
- allowed source IPs
- whether public IP is permitted
- SSH/RDP/DCV access method
- GitHub access from the workstation
- NVIDIA/NGC/Omniverse download access
- file transfer method from Brev/GitHub to AWS
- IAM role or credential approach for storage access
- cost owner and cost-center tagging
- stop schedule or manual shutdown process

Security expectations:

- do not expose remote desktop access broadly
- restrict inbound access to approved users/IPs/VPN
- avoid storing secrets in repository
- use approved credentials and access controls
- confirm shutdown process before long-running GPU use

## 7. Minimum Readiness Validation Gates

Do not begin AIDC Omniverse scene authoring until the AWS workstation passes the following checks:

| Gate | Validation |
|---|---|
| GPU visibility | nvidia-smi passes |
| Driver readiness | NVIDIA graphics/RTX/GRID driver installed and active |
| Remote graphics | Amazon DCV or approved remote desktop works |
| GPU acceleration | GPU acceleration visible inside remote session |
| Omniverse/OpenUSD | Omniverse Kit/USD Composer/OpenUSD tool launches |
| Sample rendering | Sample USD scene opens and renders |
| GitHub access | aidc-poc repository can be cloned or pulled |
| File transfer | Brev/GitHub to AWS transfer path confirmed |
| Browser validation | GPU screen UI can open in browser when API is running |
| Evidence capture | screenshot/export path confirmed |
| Cost control | stop/shutdown process confirmed |

## 8. AIDC Application Validation on AWS

After infrastructure readiness passes, validate the AIDC application baseline on AWS:

1. Clone the repository.
2. Confirm latest checkpoint or agreed branch.
3. Install required Python dependencies.
4. Compile api/app_v1.py.
5. Validate scripts/start_api_v1.sh syntax.
6. Validate scripts/smoke_test_api_v1.sh syntax.
7. Run tests/validate_scenario_acceptance_v1.py.
8. Start the API.
9. Run smoke_test_api_v1.sh.
10. Open /gpu/screen-ui in the AWS browser session.
11. Confirm /health lists /gpu/screen-ui.
12. Capture AWS validation evidence.

## 9. Omniverse Authoring Entry Criteria

Begin Omniverse authoring only after:

- AWS GPU workstation passes readiness validation
- AIDC repo can run on AWS or connect to validated backend path
- Omniverse/OpenUSD tool launches successfully
- sample USD scene renders
- Omniverse Scene Specification v1 is reviewed
- R01-R08 rack naming convention remains frozen
- file save/export path is confirmed
- screenshot/render evidence path is confirmed

## 10. Initial Omniverse Authoring Scope on AWS

First AWS Omniverse authoring scope should be intentionally controlled:

- create representative hall shell
- create R01-R08 rack objects
- add compute, cooling, and power zone labels
- add basic normal/warning/critical materials
- add hotspot/GPU pressure visual markers
- add scenario label and legend overlays
- add overview, rack detail, and scenario impact cameras
- map the four deterministic scenarios to visual states
- capture first render/screenshots

The first scene should prioritize correctness, readability, and scenario interpretation before visual polish.

## 11. Responsibility Split

Application/demo owner responsibilities:

- repository setup
- backend/API validation
- GPU screen validation
- scenario mapping
- Omniverse scene logic/content
- evidence capture
- demo flow and runbook updates
- report/tracker updates

Infrastructure support responsibilities:

- AWS GPU instance provisioning
- NVIDIA driver/graphics stack
- DCV or remote desktop setup
- network/security access
- Omniverse/OpenUSD toolchain installation if admin access is restricted
- GitHub/download access
- file transfer path
- cost-control and shutdown policy

## 12. Phase 1 Boundary Language

This AWS path supports a Phase 1 workable demo. It does not change the project boundary.

Use approved language:

- synthetic telemetry
- deterministic scenario visualization
- file-backed prototype
- operational decision-support screen
- representative AI data centre hall blueprint
- Omniverse/OpenUSD authoring path

Do not claim:

- production digital twin
- live scheduler
- real workload migration
- live DCIM/BMS control
- live facility control
- certified thermal simulation
- automated remediation

## 13. Next Step After This Document

After this document is reviewed, request the AWS environment using the minimum baseline:

- EC2 G5 class, preferably g5.4xlarge or higher
- NVIDIA A10G 24 GB GPU or equivalent
- Ubuntu 22.04 or Windows workstation image
- NVIDIA RTX/GRID driver
- Amazon DCV or approved remote desktop
- Omniverse Kit/USD Composer/OpenUSD tooling
- GitHub and file transfer access
- cost-control/shutdown process

Once AWS access is available, run infrastructure readiness validation before any AIDC Omniverse authoring starts.
