import json
import sys
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    endpoint = sys.argv[1] if len(sys.argv) > 1 else "/health"
    scenario_id = sys.argv[2] if len(sys.argv) > 2 else "baseline_normal_operation"

    if endpoint == "/health":
        response_path = TESTS_DIR / "health_response_v1.json"
    elif endpoint == "/scenarios":
        response_path = TESTS_DIR / "supported_scenarios_v1.json"
    elif endpoint == "/hall/summary":
        response_path = TESTS_DIR / f"{scenario_id}_hall_summary_v1.json"
    elif endpoint == "/hall/racks":
        response_path = TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json"
    else:
        raise ValueError(f"Unsupported endpoint: {endpoint}")

    response = load_json(response_path)

    print("Endpoint:", endpoint)
    print("Scenario:", scenario_id)
    print("Response file:", response_path)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
