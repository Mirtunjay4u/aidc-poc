#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:8000}"

check_status() {
  local name="$1"
  local path="$2"
  local expected_status="$3"

  local status
  status=$(curl -s -o /tmp/aidc_api_response.json -w "%{http_code}" "${BASE_URL}${path}")

  if [ "$status" != "$expected_status" ]; then
    echo "[FAIL] ${name} -> expected ${expected_status}, got ${status}"
    echo "Path: ${path}"
    echo "Response:"
    cat /tmp/aidc_api_response.json
    exit 1
  fi

  echo "[PASS] ${name} -> ${status}"
}

check_json_field() {
  local name="$1"
  local python_expr="$2"

  python3 -c 'import json, sys; from pathlib import Path; data = json.loads(Path("/tmp/aidc_api_response.json").read_text(encoding="utf-8")); expr = sys.argv[1]; name = sys.argv[2]; assert eval(expr, {"data": data}), f"check failed: {name}"' "$python_expr" "$name"

  echo "[PASS] ${name}"
}

echo "Running API smoke test against ${BASE_URL}"

check_status "health endpoint" "/health" "200"
check_json_field "health status is healthy" "data.get('status') == 'healthy'"

check_status "scenarios endpoint" "/scenarios" "200"
check_json_field "scenario count is 4" "data.get('scenario_count') == 4"

check_status "baseline hall summary" "/hall/summary/baseline_normal_operation" "200"
check_json_field "baseline hall summary scenario id" "data.get('scenario_id') == 'baseline_normal_operation'"

check_status "unknown summary scenario" "/hall/summary/unknown_scenario" "404"
check_json_field "unknown summary error code" "data.get('error', {}).get('code') == 'unknown_scenario'"

check_status "unknown rack scenario" "/hall/racks/unknown_scenario" "404"
check_json_field "unknown rack error code" "data.get('error', {}).get('code') == 'unknown_scenario'"

echo "Smoke test completed successfully"
