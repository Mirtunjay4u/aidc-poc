import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse


BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"
HEALTH_RESPONSE_PATH = TESTS_DIR / "health_response_v1.json"
SUPPORTED_SCENARIOS_PATH = TESTS_DIR / "supported_scenarios_v1.json"


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing response file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_supported_scenario_ids():
    data = load_json(SUPPORTED_SCENARIOS_PATH)
    scenarios = data.get("scenarios")

    if not isinstance(scenarios, list):
        raise ValueError("Invalid supported_scenarios_v1.json: 'scenarios' must be a list")

    scenario_ids = []
    for item in scenarios:
        scenario_id = item.get("id") if isinstance(item, dict) else None
        if not scenario_id:
            raise ValueError(
                "Invalid supported_scenarios_v1.json: each scenario must include a non-empty 'id'"
            )
        scenario_ids.append(scenario_id)

    return scenario_ids


def validate_required_files():
    load_json(HEALTH_RESPONSE_PATH)
    load_json(SUPPORTED_SCENARIOS_PATH)

    for scenario_id in get_supported_scenario_ids():
        load_json(TESTS_DIR / f"{scenario_id}_hall_summary_v1.json")
        load_json(TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json")


def unknown_scenario_response(scenario_id: str):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "unknown_scenario",
                "message": "Unknown scenario_id",
                "scenario_id": scenario_id,
            }
        },
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_required_files()
    yield


app = FastAPI(title="AIDC POC API", version="v1", lifespan=lifespan)


@app.get("/health")
def get_health():
    return load_json(HEALTH_RESPONSE_PATH)


@app.get("/scenarios")
def get_scenarios():
    return load_json(SUPPORTED_SCENARIOS_PATH)


@app.get("/hall/summary/{scenario_id}")
def get_hall_summary(scenario_id: str):
    path = TESTS_DIR / f"{scenario_id}_hall_summary_v1.json"
    try:
        return load_json(path)
    except FileNotFoundError:
        return unknown_scenario_response(scenario_id)


@app.get("/hall/racks/{scenario_id}")
def get_hall_racks(scenario_id: str):
    path = TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json"
    try:
        return load_json(path)
    except FileNotFoundError:
        return unknown_scenario_response(scenario_id)
