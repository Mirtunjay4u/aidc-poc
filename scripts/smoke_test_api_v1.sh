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


check_method_status() {
  local method="$1"
  local name="$2"
  local path="$3"
  local expected_status="$4"

  local status
  status=$(curl -s -X "${method}" -o /tmp/aidc_api_response.json -w "%{http_code}" "${BASE_URL}${path}")

  if [ "$status" != "$expected_status" ]; then
    echo "[FAIL] ${name} -> expected ${expected_status}, got ${status}"
    echo "Method: ${method}"
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

check_status "baseline GPU screen" "/gpu/screen/baseline_normal_operation" "200"
check_json_field "baseline GPU screen scenario id" "data.get('scenario_id') == 'baseline_normal_operation'"
check_json_field "baseline GPU screen rack count" "data.get('rack_count') == 8"
check_json_field "baseline GPU high rack count is zero" "data.get('summary', {}).get('high_gpu_rack_count') == 0"

check_status "workload surge GPU screen" "/gpu/screen/ai_workload_surge" "200"
check_json_field "workload surge GPU screen scenario id" "data.get('scenario_id') == 'ai_workload_surge'"
check_json_field "workload surge GPU high rack count" "data.get('summary', {}).get('high_gpu_rack_count') == 4"

check_status "unknown GPU screen scenario" "/gpu/screen/unknown_scenario" "404"
check_json_field "unknown GPU screen error code" "data.get('error', {}).get('code') == 'unknown_scenario'"


check_status "current scenario endpoint" "/scenario/current" "200"
check_json_field "current scenario has scenario id" "data.get('current_scenario_id') is not None"

check_method_status "POST" "start workload surge scenario" "/scenario/ai_workload_surge/start" "200"
check_json_field "started scenario id is workload surge" "data.get('current_scenario_id') == 'ai_workload_surge'"
check_json_field "started scenario status is running" "data.get('status') == 'running'"

check_status "current scenario after start" "/scenario/current" "200"
check_json_field "current scenario reflects workload surge" "data.get('current_scenario_id') == 'ai_workload_surge'"

check_method_status "POST" "reset current scenario" "/scenario/reset" "200"
check_json_field "reset scenario id is baseline" "data.get('current_scenario_id') == 'baseline_normal_operation'"
check_json_field "reset scenario status is reset" "data.get('status') == 'reset'"

check_method_status "POST" "unknown scenario start" "/scenario/unknown_scenario/start" "404"
check_json_field "unknown scenario start error code" "data.get('error', {}).get('code') == 'unknown_scenario'"


check_status "unknown summary scenario" "/hall/summary/unknown_scenario" "404"
check_json_field "unknown summary error code" "data.get('error', {}).get('code') == 'unknown_scenario'"

check_status "unknown rack scenario" "/hall/racks/unknown_scenario" "404"
check_json_field "unknown rack error code" "data.get('error', {}).get('code') == 'unknown_scenario'"

echo "Smoke test completed successfully"
