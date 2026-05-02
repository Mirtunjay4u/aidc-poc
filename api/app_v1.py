import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("aidc_poc_api")


def log_event(event_name: str, level: str = "info", **fields):
    payload = {
        "event_name": event_name,
        "service": "aidc-poc-api",
        "version": "v1",
        **fields,
    }
    message = json.dumps(payload, sort_keys=True)
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message)


BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"
HEALTH_RESPONSE_PATH = TESTS_DIR / "health_response_v1.json"
SUPPORTED_SCENARIOS_PATH = TESTS_DIR / "supported_scenarios_v1.json"
CURRENT_SCENARIO_STATE_PATH = TESTS_DIR / "current_scenario_state_v1.json"
DEFAULT_SCENARIO_ID = "baseline_normal_operation"
UI_SCREEN_PATH = BASE_DIR / "ui" / "gpu_screen_v1.html"


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

    if status == "running":
        event_name = "scenario_started"
    elif status == "reset":
        event_name = "scenario_reset_completed"
    else:
        event_name = "scenario_state_updated"

    log_event(
        event_name,
        scenario_id=scenario_id,
        result=status,
        message=message,
    )
    return state


def validate_required_files():
    log_event(
        "startup_validation_started",
        result="started",
        message="Starting required response file validation",
    )
    load_json(HEALTH_RESPONSE_PATH)
    load_json(SUPPORTED_SCENARIOS_PATH)
    load_json(CURRENT_SCENARIO_STATE_PATH)

    if not UI_SCREEN_PATH.exists():
        raise FileNotFoundError(f"Missing UI file: {UI_SCREEN_PATH}")

    scenario_ids = get_supported_scenario_ids()
    log_event(
        "startup_validation_scenario_files_check",
        result="running",
        scenario_count=len(scenario_ids),
        message="Validating scenario response files",
    )

    for scenario_id in scenario_ids:
        load_json(TESTS_DIR / f"{scenario_id}_hall_summary_v1.json")
        load_json(TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json")
        load_json(TESTS_DIR / f"{scenario_id}_gpu_screen_response_v1.json")

    log_event(
        "startup_validation_passed",
        result="passed",
        scenario_count=len(scenario_ids),
        message="Required response file validation completed successfully",
    )


def unknown_scenario_response(scenario_id: str):
    log_event(
        "unknown_scenario_requested",
        level="warning",
        scenario_id=scenario_id,
        status_code=404,
        result="not_found",
        error_code="unknown_scenario",
        message="Unknown scenario_id requested",
    )
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
    log_event(
        "api_startup_initiated",
        result="started",
        message="API startup initiated",
    )
    validate_required_files()
    log_event(
        "api_ready",
        result="ready",
        message="API startup validation passed",
    )
    yield
    log_event(
        "api_shutdown_completed",
        result="completed",
        message="API shutdown complete",
    )


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


@app.get("/gpu/screen-ui", include_in_schema=False)
def get_gpu_screen_ui():
    log_event(
        "gpu_screen_ui_requested",
        endpoint="/gpu/screen-ui",
        method="GET",
        status_code=200,
        result="served",
        message="GPU screen UI served",
    )
    return FileResponse(UI_SCREEN_PATH)


@app.get("/health")
def get_health():
    log_event(
        "health_requested",
        endpoint="/health",
        method="GET",
        status_code=200,
        result="served",
        message="Health response served",
    )
    return load_json(HEALTH_RESPONSE_PATH)


@app.get("/scenarios")
def get_scenarios():
    log_event(
        "scenarios_requested",
        endpoint="/scenarios",
        method="GET",
        status_code=200,
        result="served",
        message="Supported scenarios response served",
    )
    return load_json(SUPPORTED_SCENARIOS_PATH)


@app.get("/scenario/current")
def get_current_scenario():
    log_event(
        "scenario_current_requested",
        endpoint="/scenario/current",
        method="GET",
        status_code=200,
        result="served",
        message="Current scenario state response served",
    )
    return load_json(CURRENT_SCENARIO_STATE_PATH)


@app.post("/scenario/{scenario_id}/start")
def start_scenario(scenario_id: str):
    log_event(
        "scenario_start_requested",
        scenario_id=scenario_id,
        endpoint="/scenario/{scenario_id}/start",
        method="POST",
        result="requested",
        message="Scenario start requested",
    )
    if not is_supported_scenario(scenario_id):
        return unknown_scenario_response(scenario_id)

    return write_current_scenario_state(
        scenario_id=scenario_id,
        status="running",
        message=f"Scenario started: {scenario_id}",
    )


@app.post("/scenario/reset")
def reset_scenario():
    log_event(
        "scenario_reset_requested",
        scenario_id=DEFAULT_SCENARIO_ID,
        endpoint="/scenario/reset",
        method="POST",
        result="requested",
        message="Scenario reset requested",
    )
    return write_current_scenario_state(
        scenario_id=DEFAULT_SCENARIO_ID,
        status="reset",
        message="Scenario reset to baseline normal operation",
    )


@app.get("/hall/summary/{scenario_id}")
def get_hall_summary(scenario_id: str):
    log_event(
        "hall_summary_requested",
        scenario_id=scenario_id,
        endpoint="/hall/summary/{scenario_id}",
        method="GET",
        result="requested",
        message="Hall summary requested",
    )
    path = TESTS_DIR / f"{scenario_id}_hall_summary_v1.json"
    try:
        return load_json(path)
    except FileNotFoundError:
        return unknown_scenario_response(scenario_id)


@app.get("/hall/racks/{scenario_id}")
def get_hall_racks(scenario_id: str):
    log_event(
        "rack_records_requested",
        scenario_id=scenario_id,
        endpoint="/hall/racks/{scenario_id}",
        method="GET",
        result="requested",
        message="Rack records requested",
    )
    path = TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json"
    try:
        return load_json(path)
    except FileNotFoundError:
        return unknown_scenario_response(scenario_id)


@app.get("/gpu/screen/{scenario_id}")
def get_gpu_screen(scenario_id: str):
    log_event(
        "gpu_screen_requested",
        scenario_id=scenario_id,
        endpoint="/gpu/screen/{scenario_id}",
        method="GET",
        result="requested",
        message="GPU screen requested",
    )
    path = TESTS_DIR / f"{scenario_id}_gpu_screen_response_v1.json"
    try:
        return load_json(path)
    except FileNotFoundError:
        return unknown_scenario_response(scenario_id)
