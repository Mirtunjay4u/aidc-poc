# AIDC Phase 1 Demo Evidence Pack v1

## Purpose

This folder captures formal evidence for the AIDC Phase 1 Brev-based backend/API, GPU screen UI, scenario validation, and Omniverse scene-specification readiness.

## Latest repo checkpoint at pack creation

- c8f84a0 - Align documentation for Omniverse scene specification

## Evidence categories

| Folder | Purpose |
|---|---|
| screenshots/ | Browser screenshots for GPU screen UI and future scene evidence |
| logs/ | Structured API log extracts and shutdown/startup evidence |
| endpoint_samples/ | Captured JSON samples from health, scenarios, GPU screen, hall summary, and racks endpoints |
| smoke_tests/ | Smoke-test command output and validation results |
| fallback_notes/ | Demo access path, fallback route, and dependency notes |

## Current validated position

- Brev backend/API foundation is validated for Phase 1 file-backed demo scope.
- Scenario controller, hall/rack APIs, GPU screen API, and GPU screen UI route are implemented.
- GPU screen UI shell has been browser-reviewed across all four Phase 1 scenarios.
- Health endpoint inventory lists /gpu/screen-ui.
- Omniverse Scene Specification v1 is complete.

## Boundary language

Phase 1 remains synthetic, deterministic, file-backed, and scenario-driven. It is not a production digital twin, not a live scheduler, not live facility control, and not certified thermal simulation.

## Open dependency

Santa Clara RTX workstation access, user permissions, Omniverse toolchain readiness, and OpenUSD authoring path must be confirmed before Omniverse authoring begins.
