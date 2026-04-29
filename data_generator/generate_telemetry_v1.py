import json
import sys
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
CONFIG_DIR = BASE_DIR / "config"
SCENARIO_DIR = BASE_DIR / "scenarios"
TESTS_DIR = BASE_DIR / "tests"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def value_from_range(min_val, max_val, position, total):
    if total == 1:
        return round((min_val + max_val) / 2, 2)
    step = (max_val - min_val) / (total - 1)
    return round(min_val + (step * position), 2)


def generate_records(rack_inventory, scenario_profiles, scenario_id):
    if scenario_id not in scenario_profiles:
        raise ValueError(f"Unknown scenario_id: {scenario_id}")

    profile = scenario_profiles[scenario_id]
    records = []

    all_racks = []
    for zone in rack_inventory["zones"]:
        for rack_id in zone["racks"]:
            all_racks.append((zone["zone_id"], rack_id))

    total = len(all_racks)
    timestamp = "2026-06-01T10:00:00Z"

    for idx, (zone_id, rack_id) in enumerate(all_racks):
        record = {
            "rack_id": rack_id,
            "zone_id": zone_id,
            "timestamp": timestamp,
            "inlet_temp_c": value_from_range(profile["inlet_temp_c"][0], profile["inlet_temp_c"][1], idx, total),
            "power_kw": value_from_range(profile["power_kw"][0], profile["power_kw"][1], idx, total),
            "gpu_util_pct": int(value_from_range(profile["gpu_util_pct"][0], profile["gpu_util_pct"][1], idx, total)),
            "cooling_health": profile["cooling_health"],
            "hotspot_risk": profile["hotspot_risk"],
            "status": profile["status"]
        }
        records.append(record)

    return records


def main():
    scenario_id = sys.argv[1] if len(sys.argv) > 1 else "baseline_normal_operation"

    rack_inventory = load_json(CONFIG_DIR / "rack_inventory_v1.json")
    scenario_profiles = load_json(SCENARIO_DIR / "scenario_profiles_v1.json")

    records = generate_records(rack_inventory, scenario_profiles, scenario_id)
    output_path = TESTS_DIR / f"{scenario_id}_sample_output_v1.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    print("Scenario:", scenario_id)
    print("Records generated:", len(records))
    print("Output file:", output_path)
    print(json.dumps(records[:2], indent=2))


if __name__ == "__main__":
    main()
