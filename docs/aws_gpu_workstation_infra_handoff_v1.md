# AWS GPU Workstation Infrastructure Handoff v1

## 1. Purpose

This note provides the infrastructure/platform handoff requirements for provisioning an AWS GPU workstation for AIDC Phase 1 readiness validation.

It is a provisioning and readiness handoff document only.

It does not start Omniverse authoring.
It does not create or modify Omniverse scene files.
It does not change backend/API or UI code.

## 2. Current Project Position

Current repo checkpoint:

- da2f6dd - Clarify AWS command pack checkpoint wording

Current validated baseline:

- Brev backend/API validated
- Scenario controller validated
- Hall/rack APIs validated
- GPU screen API and UI validated
- Scenario acceptance validation passed
- Omniverse Scene Specification v1 complete
- Demo evidence pack complete
- AWS readiness specification complete
- AWS readiness validation command pack complete

## 3. Required AWS Workstation Baseline

Minimum expectation:

- EC2 G5 class or equivalent GPU workstation instance
- Preferred starting point: g5.4xlarge or higher
- NVIDIA A10G 24 GB GPU or equivalent RTX-capable GPU
- Ubuntu 22.04 LTS or approved Windows workstation image
- Minimum 250 GB storage recommended
- Sufficient CPU/RAM for Omniverse/OpenUSD authoring, browser review, and local API validation

## 4. Required Graphics and Remote Access Stack

Infrastructure/platform team should provide or confirm:

- NVIDIA driver from AWS/CSP-supported path
- NVIDIA RTX/GRID driver where required for virtual workstation graphics
- Amazon DCV or approved remote desktop/streaming access
- GPU acceleration visible inside the remote session
- Approved browser access for `/gpu/screen-ui` validation

## 5. Required Toolchain Access

The workstation should support installation or launch of:

- Omniverse Kit, USD Composer, or approved Omniverse/OpenUSD authoring tools
- OpenUSD tooling
- Python 3
- Git
- Shell tools required for repo validation
- Browser for GPU screen UI review
- VS Code or approved remote editor, if allowed

## 6. Network, Security, and Access Requirements

Infrastructure/platform team should confirm:

- Approved user access
- SSH/RDP/DCV access method
- Security group or VPN restrictions
- No broad public remote desktop exposure
- GitHub access from the workstation
- NVIDIA/NGC/Omniverse download access
- File transfer path from Brev/GitHub to AWS
- No secrets stored in repository

## 7. Cost-Control Requirements

Before long-running GPU use, confirm:

- Cost owner
- Cost-center tag
- Project tag
- Manual stop/shutdown process
- Stop schedule, if available
- Owner responsible for avoiding idle GPU cost

## 8. Readiness Validation Gates

AIDC Omniverse authoring must not begin until these checks pass:

- `nvidia-smi` passes
- NVIDIA graphics/RTX/GRID driver is active
- Amazon DCV or approved remote desktop works
- GPU acceleration is visible inside remote session
- Omniverse/OpenUSD tool launches
- Sample USD scene opens and renders
- `aidc-poc` repository can be cloned or pulled
- Brev/GitHub to AWS file transfer path is confirmed
- AIDC static validation passes on AWS
- AIDC smoke test passes on AWS
- `/gpu/screen-ui` browser review passes on AWS
- AWS validation evidence is captured
- Stop/shutdown process is confirmed

## 9. Responsibility Split

Application/demo owner responsibilities:

- Provide AIDC repo and validation commands
- Run AIDC static validation
- Run AIDC runtime smoke validation
- Review `/gpu/screen-ui`
- Capture application and demo evidence
- Keep Omniverse authoring blocked until readiness gates pass

Infrastructure/platform owner responsibilities:

- Provision GPU workstation
- Configure NVIDIA driver and graphics stack
- Configure DCV or approved remote desktop
- Confirm network/security access
- Confirm GitHub/download access
- Confirm cost-control and shutdown process
- Support Omniverse/OpenUSD installation if admin access is restricted

## 10. Handoff Request Summary

Please provision an AWS GPU workstation that satisfies the baseline, graphics, access, security, cost-control, and toolchain requirements above.

The first objective is readiness validation only.

AIDC Omniverse authoring should begin only after readiness validation evidence is captured and reviewed.

## 11. Next Step After Provisioning

Once AWS access is available, run:

- `docs/aws_readiness_validation_command_pack_v1.md`

Use one validation block at a time.

Stop immediately if any readiness gate fails.
