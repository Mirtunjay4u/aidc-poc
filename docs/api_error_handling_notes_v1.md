# API Error Handling Notes v1

## Current behavior
- `/health` returns static health JSON
- `/scenarios` returns supported scenario list
- `/hall/summary/{scenario_id}` returns HTTP 404 for unknown scenario_id
- `/hall/racks/{scenario_id}` returns HTTP 404 for unknown scenario_id

## Known limitations
- Responses are currently file-backed mock responses
- No structured application logging yet
- No custom error response schema yet
- No input validation beyond route parameter matching

## Recommended next improvements
- Add structured error response format
- Add request/response logging
- Add startup validation for required response files
- Add simple exception handling standard for internal errors
