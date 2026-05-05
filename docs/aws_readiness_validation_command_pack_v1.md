# AWS Readiness Validation Command Pack v1

## 1. Purpose

This command pack defines the validation sequence to run once the AWS GPU workstation is available.

It is a readiness validation pack only.

It does not start Omniverse authoring.
It does not create or modify any Omniverse scene.
It does not change API or UI code.

## 2. Execution Rule

Run one validation block at a time.

Proceed to the next block only after the previous block passes.

Stop immediately if any readiness gate fails.

## 3. Readiness Gates Covered

1. AWS host identity check
2. GPU visibility check
3. NVIDIA driver readiness check
4. Remote graphics / DCV access check
5. GPU acceleration check
6. Omniverse / OpenUSD toolchain check
7. Sample USD open/render check
8. GitHub and repository access check
9. AIDC static validation on AWS
10. AIDC runtime smoke validation on AWS
11. GPU screen browser review on AWS
12. Evidence capture
13. Shutdown and cost-control confirmation

## 4. Authoring Gate

AIDC Omniverse authoring may begin only after all AWS readiness gates pass and evidence is reviewed.

Until then:

- do not create AIDC Omniverse scene files
- do not modify scene assets
- do not claim production digital twin behavior
- do not claim live scheduler behavior
- do not claim live DCIM/BMS integration
- do not claim certified thermal simulation

## 5. Next Step

After this command pack is created, validate that the file exists and contains the expected sections.
