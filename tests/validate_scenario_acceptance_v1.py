import json
from pathlib import Path


BASE_DIR = Path.home() / "aidc-poc"
TESTS_DIR = BASE_DIR / "tests"

SCENARIOS = [
    "baseline_normal_operation",
    "ai_workload_surge",
    "cooling_degradation_hotspot",
    "workload_redistribution",
]

EXPECTED_GPU_ACCEPTANCE = {
    "baseline_normal_operation": {
        "high_gpu_rack_count": 0,
        "critical_rack_count": 0,
        "warning_rack_count": 0,
        "message_contains": "No redistribution required",
    },
    "ai_workload_surge": {
        "high_gpu_rack_count": 4,
        "critical_rack_count": 4,
        "message_contains": "workload",
    },
    "cooling_degradation_hotspot": {
        "critical_rack_count_min": 1,
        "message_contains": "Thermal risk",
    },
    "workload_redistribution": {
        "high_gpu_rack_count": 1,
        "critical_rack_count": 0,
        "message_contains": "redistribution",
    },
}


def load_json(path: Path):
    if not path.exists():
        raise AssertionError(f"Missing required artifact: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def assert_equal(label: str, actual, expected):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def assert_contains(label: str, text: str, expected_fragment: str):
    if expected_fragment.lower() not in text.lower():
        raise AssertionError(
            f"{label}: expected to contain {expected_fragment!r}, got {text!r}"
        )


def validate_common_artifacts(scenario_id: str):
    hall_path = TESTS_DIR / f"{scenario_id}_hall_summary_v1.json"
    rack_path = TESTS_DIR / f"{scenario_id}_rack_records_response_v1.json"
    gpu_path = TESTS_DIR / f"{scenario_id}_gpu_screen_response_v1.json"

    hall = load_json(hall_path)
    rack = load_json(rack_path)
    gpu = load_json(gpu_path)

    assert_equal(f"{scenario_id} hall scenario_id", hall.get("scenario_id"), scenario_id)
    assert_equal(f"{scenario_id} rack scenario_id", rack.get("scenario_id"), scenario_id)
    assert_equal(f"{scenario_id} gpu scenario_id", gpu.get("scenario_id"), scenario_id)

    assert_equal(f"{scenario_id} hall rack_count", hall.get("rack_count"), 8)
    assert_equal(f"{scenario_id} rack rack_count", rack.get("rack_count"), 8)
    assert_equal(f"{scenario_id} gpu rack_count", gpu.get("rack_count"), 8)

    records = rack.get("records", [])
    gpu_records = gpu.get("rack_gpu_records", [])

    assert_equal(f"{scenario_id} rack records length", len(records), 8)
    assert_equal(f"{scenario_id} gpu records length", len(gpu_records), 8)

    for record in records:
        for key in [
            "rack_id",
            "zone_id",
            "inlet_temp_c",
            "power_kw",
            "gpu_util_pct",
            "hotspot_risk",
            "evaluated_status",
        ]:
            if key not in record:
                raise AssertionError(f"{scenario_id} rack record missing key: {key}")

    for record in gpu_records:
        for key in [
            "rack_id",
            "zone_id",
            "gpu_util_pct",
            "power_kw",
            "inlet_temp_c",
            "evaluated_status",
            "hotspot_risk",
            "gpu_pressure_label",
        ]:
            if key not in record:
                raise AssertionError(f"{scenario_id} GPU record missing key: {key}")

    status_counts = {"normal": 0, "warning": 0, "critical": 0}
    for record in records:
        status = record.get("evaluated_status")
        if status not in status_counts:
            raise AssertionError(f"{scenario_id} unexpected evaluated_status: {status}")
        status_counts[status] += 1

    hall_status_counts = hall.get("status_counts", {})
    for status, count in status_counts.items():
        assert_equal(
            f"{scenario_id} hall status_counts.{status}",
            hall_status_counts.get(status),
            count,
        )

    gpu_summary = gpu.get("summary", {})
    assert_equal(
        f"{scenario_id} GPU warning_rack_count consistency",
        gpu_summary.get("warning_rack_count"),
        status_counts["warning"],
    )
    assert_equal(
        f"{scenario_id} GPU critical_rack_count consistency",
        gpu_summary.get("critical_rack_count"),
        status_counts["critical"],
    )

    return hall, rack, gpu


def validate_gpu_acceptance(scenario_id: str, gpu: dict):
    summary = gpu.get("summary", {})
    expected = EXPECTED_GPU_ACCEPTANCE[scenario_id]

    for key, expected_value in expected.items():
        if key == "message_contains":
            assert_contains(
                f"{scenario_id} optimization_message",
                summary.get("optimization_message", ""),
                expected_value,
            )
        elif key.endswith("_min"):
            real_key = key[:-4]
            actual = summary.get(real_key)
            if actual is None or actual < expected_value:
                raise AssertionError(
                    f"{scenario_id} {real_key}: expected >= {expected_value}, got {actual}"
                )
        else:
            assert_equal(f"{scenario_id} {key}", summary.get(key), expected_value)

    for key in [
        "avg_gpu_util_pct",
        "max_gpu_util_pct",
        "min_gpu_util_pct",
        "high_gpu_rack_count",
        "critical_rack_count",
        "warning_rack_count",
        "total_power_kw",
        "max_power_kw",
        "hottest_rack_id",
        "highest_gpu_rack_id",
        "optimization_message",
    ]:
        if key not in summary:
            raise AssertionError(f"{scenario_id} GPU summary missing key: {key}")


def validate_baseline_specific(gpu: dict):
    labels = {record["gpu_pressure_label"] for record in gpu["rack_gpu_records"]}
    assert_equal("baseline GPU pressure labels", labels, {"normal"})


def validate_all():
    for scenario_id in SCENARIOS:
        _, _, gpu = validate_common_artifacts(scenario_id)
        validate_gpu_acceptance(scenario_id, gpu)
        if scenario_id == "baseline_normal_operation":
            validate_baseline_specific(gpu)

        summary = gpu["summary"]
        print(
            "[PASS]",
            scenario_id,
            "rack_count=",
            gpu["rack_count"],
            "high_gpu_rack_count=",
            summary["high_gpu_rack_count"],
            "critical_rack_count=",
            summary["critical_rack_count"],
        )

    print("[PASS] scenario acceptance artifact validation completed")


if __name__ == "__main__":
    validate_all()
