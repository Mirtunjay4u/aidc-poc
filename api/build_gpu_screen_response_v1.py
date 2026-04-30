import json
import sys
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"


OPTIMIZATION_MESSAGES = {
    "baseline_normal_operation": "GPU load is balanced. No redistribution required.",
    "ai_workload_surge": "GPU load surge detected. Consider shifting non-critical workload away from high-utilization racks.",
    "cooling_degradation_hotspot": "Thermal risk is dominant. Avoid adding GPU load to hotspot-affected racks.",
    "workload_redistribution": "Workload redistribution is active. Monitor shifted load and confirm rack status remains within warning bounds.",
}


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def gpu_pressure_label(gpu_util_pct: int) -> str:
    if gpu_util_pct >= 85:
        return "high"
    if gpu_util_pct >= 70:
        return "elevated"
    return "normal"


def main():
    scenario_id = sys.argv[1] if len(sys.argv) > 1 else "baseline_normal_operation"

    rack_response_path = TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json"
    hall_summary_path = TESTS_DIR / f"{scenario_id}_hall_summary_v1.json"
    output_path = TESTS_DIR / f"{scenario_id}_gpu_screen_response_v1.json"

    rack_response = load_json(rack_response_path)
    hall_summary = load_json(hall_summary_path)
    records = rack_response["records"]

    if not records:
        raise ValueError(f"No rack records found for scenario: {scenario_id}")

    rack_gpu_records = []
    for record in records:
        rack_gpu_records.append(
            {
                "rack_id": record["rack_id"],
                "zone_id": record["zone_id"],
                "gpu_util_pct": record["gpu_util_pct"],
                "power_kw": record["power_kw"],
                "inlet_temp_c": record["inlet_temp_c"],
                "evaluated_status": record["evaluated_status"],
                "hotspot_risk": record["hotspot_risk"],
                "gpu_pressure_label": gpu_pressure_label(record["gpu_util_pct"]),
            }
        )

    gpu_values = [record["gpu_util_pct"] for record in records]
    power_values = [record["power_kw"] for record in records]

    hottest_record = max(records, key=lambda record: record["inlet_temp_c"])
    highest_gpu_record = max(records, key=lambda record: record["gpu_util_pct"])

    summary = {
        "avg_gpu_util_pct": round(sum(gpu_values) / len(gpu_values), 2),
        "max_gpu_util_pct": max(gpu_values),
        "min_gpu_util_pct": min(gpu_values),
        "high_gpu_rack_count": sum(
            1 for record in rack_gpu_records if record["gpu_pressure_label"] == "high"
        ),
        "critical_rack_count": sum(
            1 for record in records if record["evaluated_status"] == "critical"
        ),
        "warning_rack_count": sum(
            1 for record in records if record["evaluated_status"] == "warning"
        ),
        "total_power_kw": round(sum(power_values), 2),
        "max_power_kw": max(power_values),
        "hottest_rack_id": hottest_record["rack_id"],
        "highest_gpu_rack_id": highest_gpu_record["rack_id"],
        "optimization_message": OPTIMIZATION_MESSAGES.get(
            scenario_id,
            "Review GPU workload distribution for the selected scenario.",
        ),
    }

    response = {
        "scenario_id": scenario_id,
        "hall_id": rack_response.get("hall_id", hall_summary.get("hall_id")),
        "rack_count": rack_response.get("rack_count", len(records)),
        "summary": summary,
        "rack_gpu_records": rack_gpu_records,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2)
        f.write("\n")

    print("Scenario:", scenario_id)
    print("Output file:", output_path)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
