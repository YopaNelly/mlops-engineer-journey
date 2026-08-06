"""
Combines all three individual checks (from Day 12) into ONE report,
and includes an overall pass/fail verdict — because the whole point
of combining them is to answer one question at a glance:
"is this data safe to use, yes or no?"
"""

from datetime import datetime
import pandas as pd
from .checks import check_missing, check_types, check_ranges


def run_quality_checks(
    df: pd.DataFrame,
    required_columns: list[str],
    expected_types: dict[str, type],
    ranges: dict[str, tuple[float, float]],
) -> dict:
    """
    Runs all three checks and combines them into one structured report.
    This is the ONLY function most callers will ever need to use directly —
    everything from Day 12 becomes an internal detail.
    """
    missing_issues = check_missing(df, required_columns)
    type_issues = check_types(df, expected_types)
    range_issues = check_ranges(df, ranges)

    # "passed" is true only if ALL THREE checks came back completely empty.
    # This is the single most important line in the whole report — it's
    # the answer to "is this data okay?" boiled down to one true/false.
    passed = not (missing_issues or type_issues or range_issues)

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "row_count": len(df),
        "passed": passed,
        "checks": {
            "missing": missing_issues,
            "types": type_issues,
            "ranges": range_issues,
        },
    }
    return report
