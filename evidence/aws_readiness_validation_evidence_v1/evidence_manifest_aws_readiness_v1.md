# AWS Readiness Validation Evidence Manifest v1

## 1. Purpose

This manifest tracks AWS GPU workstation readiness evidence for AIDC Phase 1.

It supports readiness validation only.

It does not authorize Omniverse authoring by itself.

## 2. Current Project Checkpoint

Latest repo checkpoint before this evidence template:

- 86692af - Add AWS GPU workstation infra handoff

## 3. Readiness Gate Evidence Tracker

| Gate | Evidence file | Status | Review note |
|---|---|---|---|
| AWS host identity | aws_host_identity.txt | Pending AWS environment | Capture hostname, user, OS, working directory, and kernel details. |
| GPU visibility | gpu_visibility_nvidia_smi.txt | Pending AWS environment | Capture `nvidia-smi` output. |
| Driver readiness | driver_readiness.txt | Pending AWS environment | Capture NVIDIA driver / RTX / GRID readiness output. |
| Remote graphics / DCV | dcv_remote_graphics_check.md | Pending AWS environment | Capture DCV or approved remote desktop access confirmation. |
| GPU acceleration in remote session | dcv_remote_graphics_check.md | Pending AWS environment | Confirm GPU acceleration is visible inside the remote session. |
| Omniverse/OpenUSD launch | omniverse_openusd_launch_check.md | Pending AWS environment | Capture launch confirmation for Omniverse Kit, USD Composer, or approved OpenUSD tooling. |
| Sample USD render | sample_usd_render_check.md | Pending AWS environment | Capture sample USD open/render confirmation. |
| GitHub/repo access | repo_validation_output.txt | Pending AWS environment | Capture clone/pull and checkpoint verification. |
| AIDC static validation | aidc_static_validation_output.txt | Pending AWS environment | Capture Python compile, shell syntax, and scenario acceptance validation. |
| AIDC runtime smoke validation | aidc_smoke_test_output.txt | Pending AWS environment | Capture API startup and smoke test result. |
| GPU screen browser review | gpu_screen_browser_review.md | Pending AWS environment | Capture `/gpu/screen-ui` browser review notes/screenshots. |
| Evidence review | evidence_manifest_aws_readiness_v1.md | Pending AWS environment | Confirm all required evidence files are present and reviewed. |
| Cost/shutdown control | shutdown_cost_control_confirmation.md | Pending AWS environment | Capture stop/shutdown and cost-control confirmation. |

## 4. Authoring Gate

AIDC Omniverse authoring must not begin until all readiness gates are marked passed and evidence is reviewed.

Until then:

- do not create AIDC Omniverse scene files
- do not modify scene assets
- do not claim production digital twin behavior
- do not claim live scheduler behavior
- do not claim live DCIM/BMS integration
- do not claim certified thermal simulation

## 5. Next Step

When AWS access is available, run the AWS readiness validation command pack one block at a time and save outputs into this folder.
