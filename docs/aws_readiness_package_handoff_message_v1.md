# AWS Readiness Package Handoff Message v1

## 1. Purpose

This document provides the draft handoff message for Brian / platform / infrastructure team.

It summarizes what is ready from the AIDC application side, what infrastructure support is required, which repository artifacts should be reviewed first, and what must happen before Omniverse authoring can begin.

It does not start AWS execution.
It does not start Omniverse authoring.
It does not create or modify Omniverse scene files.
It does not change backend/API or UI code.

## 2. Current Checkpoint

Latest repo checkpoint before this handoff message:

- f504f7e - Align documentation for AWS readiness package index

## 3. Draft Message

Hi Brian,

I can drive the AIDC application-side development, validation, and demo packaging once the AWS GPU environment is available.

From the application side, the current AIDC Phase 1 baseline is ready for AWS readiness validation. The backend/API, scenario controller, GPU decision-support screen, Omniverse scene specification, formal demo evidence pack, AWS readiness command pack, AWS infrastructure handoff, AWS evidence template, AWS repo bootstrap note, and AWS readiness package index are complete and referenced from the core repository documentation.

The main blocker is the GPU workstation infrastructure itself. I will need platform/infrastructure support for provisioning and preparing the AWS workstation, including the GPU instance, NVIDIA driver and graphics stack, Amazon DCV or approved remote desktop access, Omniverse/OpenUSD toolchain availability, network/security access, GitHub/file transfer access, and cost-control/shutdown setup.

The first document to review is:

- `docs/aws_readiness_package_index_v1.md`

For the infrastructure provisioning request, please use:

- `docs/aws_gpu_workstation_infra_handoff_v1.md`

Minimum starting expectation is an AWS EC2 G5 class workstation, preferably `g5.4xlarge` or higher, with NVIDIA A10G 24 GB GPU or equivalent RTX-capable GPU, Ubuntu 22.04 or approved Windows workstation image, NVIDIA RTX/GRID driver where required, Amazon DCV or approved remote access, Omniverse Kit/USD Composer or approved current Omniverse/OpenUSD tooling, GitHub access, and a confirmed Brev/GitHub-to-AWS file transfer path.

Once the AWS environment is available and I can access it remotely, I will run the repo bootstrap, static validation, runtime smoke validation, GPU screen browser review, AWS readiness validation, evidence capture, and demo-readiness checks.

Omniverse authoring should not begin until readiness validation passes and evidence is reviewed.

Thanks,
Mirtunjay

## 4. Attach / Reference These Repo Artifacts

Primary navigation document:

- `docs/aws_readiness_package_index_v1.md`

Infrastructure/platform provisioning handoff:

- `docs/aws_gpu_workstation_infra_handoff_v1.md`

Detailed readiness specification:

- `docs/aws_gpu_workstation_readiness_v1.md`

Readiness validation command sequence:

- `docs/aws_readiness_validation_command_pack_v1.md`

Application-side AWS repository bootstrap:

- `docs/aws_aidc_repo_bootstrap_v1.md`

Evidence capture location and manifest:

- `evidence/aws_readiness_validation_evidence_v1/`
- `evidence/aws_readiness_validation_evidence_v1/evidence_manifest_aws_readiness_v1.md`

## 5. Core Dependency / Blocker

The core blocker is AWS GPU workstation availability and readiness.

The AIDC application-side baseline is ready for AWS validation, but Omniverse authoring cannot begin until the workstation environment is provisioned, accessible, validated, and evidence-backed.

Current blocked areas:

- AWS GPU workstation provisioning
- NVIDIA driver / RTX / GRID graphics stack readiness
- Amazon DCV or approved remote desktop access
- Omniverse/OpenUSD toolchain availability
- GitHub and Brev/GitHub-to-AWS file transfer access
- Network/security access confirmation
- Cost-control and shutdown process confirmation

This is an infrastructure dependency, not an application-code blocker.

## 6. Requested Infrastructure Support

Requested infrastructure/platform support:

- Provision AWS EC2 G5 class or equivalent GPU workstation.
- Prefer `g5.4xlarge` or higher as the starting baseline.
- Provide NVIDIA A10G 24 GB GPU or equivalent RTX-capable GPU.
- Provide Ubuntu 22.04 LTS or approved Windows workstation image.
- Install/configure NVIDIA driver from AWS/CSP-supported path.
- Configure RTX/GRID driver where required for virtual workstation graphics.
- Provide Amazon DCV or approved remote desktop/streaming access.
- Confirm GPU acceleration is visible inside the remote session.
- Confirm Omniverse Kit, USD Composer, or approved Omniverse/OpenUSD tooling is available.
- Confirm Python 3, Git, browser, and approved editor/tooling access.
- Confirm GitHub access from the workstation.
- Confirm Brev/GitHub-to-AWS file transfer path.
- Confirm security group, VPN, user access, and no broad public remote desktop exposure.
- Confirm cost owner, cost-center/project tags, stop/shutdown process, and idle-cost control.

## 7. Application-Side Commitment

Once AWS access is available, the AIDC application/demo owner will:

- Clone or pull the `aidc-poc` repository on the AWS workstation.
- Verify the latest expected checkpoint.
- Run static validation.
- Run scenario acceptance validation.
- Start the AIDC API.
- Run runtime smoke validation.
- Review `/gpu/screen-ui` in the approved AWS browser/remote desktop path.
- Run AWS readiness validation one block at a time.
- Save outputs into `evidence/aws_readiness_validation_evidence_v1/`.
- Update the AWS readiness evidence manifest after evidence is captured.
- Confirm shutdown/process safety before leaving the GPU workstation idle.
- Proceed to controlled Omniverse authoring only if readiness gates pass and evidence is reviewed.

## 8. Authoring Gate

AIDC Omniverse authoring may begin only after AWS or Santa Clara readiness validation passes and evidence is reviewed.

Until then:

- do not create AIDC Omniverse scene files
- do not modify scene assets
- do not claim production digital twin behavior
- do not claim live scheduler behavior
- do not claim live DCIM/BMS integration
- do not claim certified thermal simulation

## 9. Next Step

After this skeleton is validated, expand the draft message one section at a time.
