import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("aidc_poc_api")

BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"
HEALTH_RESPONSE_PATH = TESTS_DIR / "health_response_v1.json"
SUPPORTED_SCENARIOS_PATH = TESTS_DIR / "supported_scenarios_v1.json"
CURRENT_SCENARIO_STATE_PATH = TESTS_DIR / "current_scenario_state_v1.json"
DEFAULT_SCENARIO_ID = "baseline_normal_operation"


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


def is_supported_scenario(scenario_id: str) -> bool:
    return scenario_id in get_supported_scenario_ids()


def write_current_scenario_state(scenario_id: str, status: str, message: str):
    state = {
        "current_scenario_id": scenario_id,
        "status": status,
        "message": message,
    }

    with open(CURRENT_SCENARIO_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")

    logger.info("Scenario state updated: %s", state)
    return state


def validate_required_files():
    logger.info("Starting required response file validation")
    load_json(HEALTH_RESPONSE_PATH)
    load_json(SUPPORTED_SCENARIOS_PATH)
    load_json(CURRENT_SCENARIO_STATE_PATH)

    scenario_ids = get_supported_scenario_ids()
    logger.info("Validating response files for %d scenarios", len(scenario_ids))

    for scenario_id in scenario_ids:
        load_json(TESTS_DIR / f"{scenario_id}_hall_summary_v1.json")
        load_json(TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json")
        load_json(TESTS_DIR / f"{scenario_id}_gpu_screen_response_v1.json")

    logger.info("Required response file validation completed successfully")


def unknown_scenario_response(scenario_id: str):
    logger.warning("Unknown scenario requested: %s", scenario_id)
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
    logger.info("API startup initiated")
    validate_required_files()
    logger.info("API startup validation passed")
    yield
    logger.info("API shutdown complete")


app = FastAPI(title="AIDC POC API", version="v1", lifespan=lifespan)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled internal error on path %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_error",
                "message": "Internal server error",
            }
        },
    )


@app.get("/health")
def get_health():
    return load_json(HEALTH_RESPONSE_PATH)


@app.get("/scenarios")
def get_scenarios():
    return load_json(SUPPORTED_SCENARIOS_PATH)


@app.get("/scenario/current")
def get_current_scenario():
    return load_json(CURRENT_SCENARIO_STATE_PATH)


@app.post("/scenario/{scenario_id}/start")
def start_scenario(scenario_id: str):
    if not is_supported_scenario(scenario_id):
        return unknown_scenario_response(scenario_id)

    return write_current_scenario_state(
        scenario_id=scenario_id,
        status="running",
        message=f"Scenario started: {scenario_id}",
    )


@app.post("/scenario/reset")
def reset_scenario():
    return write_current_scenario_state(
        scenario_id=DEFAULT_SCENARIO_ID,
        status="reset",
        message="Scenario reset to baseline normal operation",
    )


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


@app.get("/gpu/screen/{scenario_id}")
def get_gpu_screen(scenario_id: str):
    path = TESTS_DIR / f"{scenario_id}_gpu_screen_response_v1.json"
    try:
        return load_json(path)
    except FileNotFoundError:
        return unknown_scenario_response(scenario_id)
