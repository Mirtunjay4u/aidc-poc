import json
import sys
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
RULES_PATH = BASE_DIR / "rules_engine" / "rules_thresholds_v1.json"
TESTS_DIR = BASE_DIR / "tests"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_status(record, thresholds):
    if record["cooling_health"] in ["degraded", "failed"] and record["hotspot_risk"] in ["medium", "high"]:
        return "critical"

    if (
        record["inlet_temp_c"] > thresholds["temperature_c"]["warning_max"]
        or record["power_kw"] > thresholds["power_kw"]["warning_max"]
        or record["gpu_util_pct"] > thresholds["gpu_util_pct"]["warning_max"]
    ):
        return "critical"

    if (
        record["inlet_temp_c"] > thresholds["temperature_c"]["normal_max"]
        or record["power_kw"] > thresholds["power_kw"]["normal_max"]
        or record["gpu_util_pct"] > thresholds["gpu_util_pct"]["normal_max"]
    ):
        return "warning"

    return "normal"


def main():
    scenario_id = sys.argv[1] if len(sys.argv) > 1 else "baseline_normal_operation"

    input_path = TESTS_DIR / f"{scenario_id}_sample_output_v1.json"
    output_path = TESTS_DIR / f"{scenario_id}_rules_evaluated_v1.json"

    thresholds = load_json(RULES_PATH)
    records = load_json(input_path)

    evaluated = []
    for record in records:
        updated = dict(record)
        updated["evaluated_status"] = evaluate_status(record, thresholds)
        evaluated.append(updated)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(evaluated, f, indent=2)

    print("Scenario:", scenario_id)
    print("Records evaluated:", len(evaluated))
    print("Output file:", output_path)
    print(json.dumps(evaluated[:2], indent=2))


if __name__ == "__main__":
    main()
