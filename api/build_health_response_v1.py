import json
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
OUTPUT_PATH = BASE_DIR / "tests" / "health_response_v1.json"


def main():
    response = {
        "service": "aidc-poc-api",
        "version": "v1",
        "status": "healthy",
        "available_endpoints": [
            "/health",
            "/hall/summary/{scenario_id}",
            "/hall/racks/{scenario_id}",
            "/scenarios"
        ]
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=2)

    print("Output file:", OUTPUT_PATH)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
