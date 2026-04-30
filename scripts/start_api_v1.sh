#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${AIDC_PROJECT_DIR:-$HOME/aidc-poc}"
API_DIR="${PROJECT_DIR}/api"
TESTS_DIR="${PROJECT_DIR}/tests"
HOST="${AIDC_API_HOST:-0.0.0.0}"
PORT="${AIDC_API_PORT:-8000}"

echo "[INFO] Starting AIDC POC API v1"
echo "[INFO] Project directory: ${PROJECT_DIR}"
echo "[INFO] API directory: ${API_DIR}"
echo "[INFO] Host: ${HOST}"
echo "[INFO] Port: ${PORT}"

if [ ! -d "${PROJECT_DIR}" ]; then
  echo "[ERROR] Project directory not found: ${PROJECT_DIR}"
  exit 1
fi

if [ ! -f "${API_DIR}/app_v1.py" ]; then
  echo "[ERROR] FastAPI app not found: ${API_DIR}/app_v1.py"
  exit 1
fi

if [ ! -f "${API_DIR}/requirements_v1.txt" ]; then
  echo "[ERROR] Requirements file not found: ${API_DIR}/requirements_v1.txt"
  exit 1
fi

if [ ! -d "${TESTS_DIR}" ]; then
  echo "[ERROR] Response artifacts directory not found: ${TESTS_DIR}"
  exit 1
fi

python3 - <<'PY'
import importlib.util
import sys

required = ["fastapi", "uvicorn"]
missing = [name for name in required if importlib.util.find_spec(name) is None]

if missing:
    print(f"[ERROR] Missing Python packages: {', '.join(missing)}")
    print("[ERROR] Install dependencies with: python3 -m pip install -r ~/aidc-poc/api/requirements_v1.txt")
    sys.exit(1)

print("[INFO] Python dependency check passed")
PY

cd "${PROJECT_DIR}"

echo "[INFO] Launching Uvicorn"
exec python3 -m uvicorn app_v1:app --app-dir "${API_DIR}" --host "${HOST}" --port "${PORT}"
