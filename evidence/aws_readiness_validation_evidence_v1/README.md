# AWS Readiness Validation Evidence v1

## Purpose

This folder captures AWS GPU workstation readiness validation evidence for AIDC Phase 1.

It is an evidence template only.

It does not start Omniverse authoring.
It does not create or modify Omniverse scene files.
It does not change backend/API or UI code.

## Current Gate

AIDC Omniverse authoring may begin only after AWS readiness validation passes and evidence is reviewed.

## Expected Evidence Files

- aws_host_identity.txt
- gpu_visibility_nvidia_smi.txt
- driver_readiness.txt
- dcv_remote_graphics_check.md
- omniverse_openusd_launch_check.md
- sample_usd_render_check.md
- repo_validation_output.txt
- aidc_static_validation_output.txt
- aidc_smoke_test_output.txt
- gpu_screen_browser_review.md
- shutdown_cost_control_confirmation.md
- evidence_manifest_aws_readiness_v1.md

## Evidence Rule

Capture one validation block at a time.

Do not mark a gate as passed unless the related command output, screenshot note, or reviewer observation is saved.

Stop immediately if any readiness gate fails.
