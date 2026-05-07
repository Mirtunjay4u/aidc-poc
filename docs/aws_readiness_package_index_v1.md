# AWS Readiness Package Index v1

## 1. Purpose

This document is the navigation index for the AIDC Phase 1 AWS readiness package.

It helps leadership, platform/infrastructure owners, and the application/demo owner understand which AWS readiness artifacts exist and how they should be used.

It does not start AWS execution.
It does not start Omniverse authoring.
It does not create or modify Omniverse scene files.
It does not change backend/API or UI code.

## 2. Current Project Checkpoint

Latest repo checkpoint before this package index:

- b3cfb32 - Align documentation for AWS readiness package

## 3. AWS Readiness Package Artifacts

The current AWS readiness package contains the following artifacts:

| Artifact | Purpose | Primary user |
|---|---|---|
| docs/aws_gpu_workstation_readiness_v1.md | Defines AWS GPU workstation baseline, validation gates, security/cost controls, and responsibility split. | Leadership, infrastructure/platform owner, application/demo owner |
| docs/aws_readiness_validation_command_pack_v1.md | Defines the readiness validation sequence to run once AWS access is available. | Application/demo owner |
| docs/aws_gpu_workstation_infra_handoff_v1.md | Provides the concise provisioning and responsibility handoff for the infrastructure/platform owner. | Infrastructure/platform owner |
| docs/aws_aidc_repo_bootstrap_v1.md | Defines application-side repository setup, static validation, runtime smoke validation, browser review, evidence capture, and shutdown checks on AWS. | Application/demo owner |
| evidence/aws_readiness_validation_evidence_v1/ | Provides the evidence folder, placeholders, and manifest for AWS readiness validation outputs. | Application/demo owner, reviewer |

## 4. Who Uses What

| Role | Use these artifacts | Purpose |
|---|---|---|
| Leadership / management | docs/aws_gpu_workstation_readiness_v1.md and this package index | Understand current readiness posture, dependency, blocker, and next execution path. |
| Infrastructure / platform owner | docs/aws_gpu_workstation_infra_handoff_v1.md and docs/aws_gpu_workstation_readiness_v1.md | Provision the AWS GPU workstation, remote graphics path, security/access controls, GitHub/file transfer access, and cost-control/shutdown setup. |
| Application / demo owner | docs/aws_aidc_repo_bootstrap_v1.md and docs/aws_readiness_validation_command_pack_v1.md | Clone/pull the repo on AWS, run static validation, run smoke validation, review /gpu/screen-ui, capture evidence, and confirm process shutdown. |
| Reviewer / evidence owner | evidence/aws_readiness_validation_evidence_v1/ | Confirm readiness evidence is saved, reviewed, and traceable before authoring begins. |

## 5. Recommended Execution Order

Run the AWS readiness package in this order:

1. Share `docs/aws_gpu_workstation_infra_handoff_v1.md` with the infrastructure/platform owner.
2. Use `docs/aws_gpu_workstation_readiness_v1.md` to confirm AWS GPU workstation baseline, access, security, toolchain, and cost-control expectations.
3. Once AWS access is available, use `docs/aws_aidc_repo_bootstrap_v1.md` to clone/pull the repo and validate the AIDC application baseline on AWS.
4. Use `docs/aws_readiness_validation_command_pack_v1.md` to run readiness validation one block at a time.
5. Save outputs into `evidence/aws_readiness_validation_evidence_v1/`.
6. Review the evidence manifest before marking readiness gates passed.
7. Begin Omniverse authoring only after readiness validation passes and evidence is reviewed.

## 6. Evidence Capture Location

All AWS readiness validation outputs should be saved under:

    evidence/aws_readiness_validation_evidence_v1/

Primary manifest:

    evidence/aws_readiness_validation_evidence_v1/evidence_manifest_aws_readiness_v1.md

Minimum expected evidence areas:

- AWS host identity
- GPU visibility / nvidia-smi
- NVIDIA driver readiness
- DCV or approved remote graphics access
- Omniverse/OpenUSD launch
- sample USD render
- GitHub/repo access
- AIDC static validation
- AIDC runtime smoke validation
- /gpu/screen-ui browser review on AWS
- shutdown and cost-control confirmation

Do not mark an AWS readiness gate as passed unless evidence has been saved and reviewed.

## 7. Authoring Gate

AIDC Omniverse authoring may begin only after AWS or Santa Clara readiness validation passes and evidence is reviewed.

Until then:

- do not create AIDC Omniverse scene files
- do not modify scene assets
- do not claim production digital twin behavior
- do not claim live scheduler behavior
- do not claim live DCIM/BMS integration
- do not claim certified thermal simulation

## 8. Next Step

After this skeleton is validated, expand each section one at a time.
