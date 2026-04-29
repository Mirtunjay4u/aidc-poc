import json
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
SCENARIO_MATRIX_PATH = BASE_DIR / "scenarios" / "scenario_matrix_v1.json"
OUTPUT_PATH = BASE_DIR / "tests" / "supported_scenarios_v1.json"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    scenario_matrix = load_json(SCENARIO_MATRIX_PATH)

    response = {
        "phase": scenario_matrix["phase"],
        "scenario_count": len(scenario_matrix["scenarios"]),
        "scenarios": scenario_matrix["scenarios"]
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2)

    print("Output file:", OUTPUT_PATH)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
