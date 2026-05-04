# Demo Access and Fallback Notes

## Current validated access path

- Direct EC2/Brev-hosted API route was used successfully for /gpu/screen-ui browser review.
- Jupyter proxy path previously returned a Jupyter 404 in the current environment; treat this as an environment/proxy access limitation, not an application failure.

## Fallback position

- Backend/API validation can be demonstrated through smoke test output and endpoint samples.
- GPU screen UI can be demonstrated through the direct API host route when the API is running.
- Omniverse authoring remains gated until Santa Clara RTX workstation readiness is confirmed.

## Boundary

- Phase 1 remains synthetic, deterministic, file-backed, and scenario-driven.
