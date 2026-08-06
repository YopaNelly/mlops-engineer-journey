"""
Saves a quality report dict to a real JSON file on disk —
so the report isn't just something printed once and lost.
"""
import json


def save_json_report(report: dict, path: str = "quality_report.json") -> None:
    with open(path, "w") as f:
        # indent=2 makes the file human-readable if someone opens it directly,
        # not just machine-readable.
        json.dump(report, f, indent=2)
