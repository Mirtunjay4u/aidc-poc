import json
from pathlib import Path

from fastapi import FastAPI, HTTPException


BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"

app = FastAPI(title="AIDC POC API", version="v1")


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing response file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/health")
def get_health():
    return load_json(TESTS_DIR / "health_response_v1.json")


@app.get("/scenarios")
def get_scenarios():
    return load_json(TESTS_DIR / "supported_scenarios_v1.json")


@app.get("/hall/summary/{scenario_id}")
def get_hall_summary(scenario_id: str):
    path = TESTS_DIR / f"{scenario_id}_hall_summary_v1.json"
    try:
        return load_json(path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Unknown scenario_id: {scenario_id}")


@app.get("/hall/racks/{scenario_id}")
def get_hall_racks(scenario_id: str):
    path = TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json"
    try:
        return load_json(path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Unknown scenario_id: {scenario_id}")
