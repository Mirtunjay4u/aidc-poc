# AIDC POC Development Baseline v1

## Phase 1 Scope
- One representative hall
- 8 representative racks
- 3 logical zones: compute, cooling, power
- Synthetic telemetry only
- 4 replayable scenarios
- AI workload / GPU optimization handled as a separate screen

## Frozen files
- config/telemetry_schema_v1.json
- config/rack_inventory_v1.json
- scenarios/scenario_matrix_v1.json
- scenarios/scenario_profiles_v1.json

## Development rule
Build backend and scenario logic first.
Do not expand scope or schema until the first telemetry generator run is validated.
