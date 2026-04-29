import json
import sys
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"
OUTPUT_DIR = BASE_DIR / "tests"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    scenario_id = sys.argv[1] if len(sys.argv) > 1 else "baseline_normal_operation"

    input_path = TESTS_DIR / f"{scenario_id}_rules_evaluated_v1.json"
    output_path = OUTPUT_DIR / f"{scenario_id}_rack_records_response_v1.json"

    records = load_json(input_path)

    response = {
        "scenario_id": scenario_id,
        "hall_id": "hall_a",
        "rack_count": len(records),
        "records": records
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2)

    print("Scenario:", scenario_id)
    print("Output file:", output_path)
    print(json.dumps({
        "scenario_id": response["scenario_id"],
        "hall_id": response["hall_id"],
        "rack_count": response["rack_count"],
        "first_record": response["records"][0]
    }, indent=2))


if __name__ == "__main__":
    main()
