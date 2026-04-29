import json
import sys
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    scenario_id = sys.argv[1] if len(sys.argv) > 1 else "baseline_normal_operation"

    input_path = TESTS_DIR / f"{scenario_id}_rules_evaluated_v1.json"
    output_path = TESTS_DIR / f"{scenario_id}_hall_summary_v1.json"

    records = load_json(input_path)

    summary = {
        "scenario_id": scenario_id,
        "hall_id": "hall_a",
        "rack_count": len(records),
        "status_counts": {
            "normal": 0,
            "warning": 0,
            "critical": 0
        },
        "max_inlet_temp_c": max(r["inlet_temp_c"] for r in records),
        "max_power_kw": max(r["power_kw"] for r in records),
        "max_gpu_util_pct": max(r["gpu_util_pct"] for r in records)
    }

    for record in records:
        summary["status_counts"][record["evaluated_status"]] += 1

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Scenario:", scenario_id)
    print("Output file:", output_path)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
