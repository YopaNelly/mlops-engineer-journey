"""
Three independent data quality checks. Each one:
  - takes a dataframe (and whatever config it needs)
  - returns a dict shaped like {column_name: issue_count}
  - never mutates the original data — only reports on it

Keeping the SAME return shape across all three is deliberate — it's what
lets us combine all three reports into one, cleanly, in the next lesson.
"""

import pandas as pd
from logging import getLogger, basicConfig, INFO

basicConfig(level=INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = getLogger(__name__)


def check_missing(df: pd.DataFrame, required_columns: list[str]) -> dict[str, int]:
    """
    For each required column, count how many rows have a missing (NaN) value.
    Only reports columns that actually HAVE at least one issue — a column
    with zero missing values doesn't appear in the result at all.
    """
    issues = {}
    for col in required_columns:
        if col not in df.columns:
            # The column doesn't even exist — that's worth flagging loudly,
            # not silently skipping.
            logger.warning(f"Column '{col}' expected but not found in data")
            continue

        missing_count = int(df[col].isna().sum())
        if missing_count > 0:
            issues[col] = missing_count

    return issues


def check_types(df: pd.DataFrame, expected_types: dict[str, type]) -> dict[str, int]:
    """
    For each column with an expected type, count how many values DON'T
    match that type. expected_types looks like: {"price": float, "id": int}
    """
    issues = {}
    for col, expected_type in expected_types.items():
        if col not in df.columns:
            logger.warning(f"Column '{col}' expected but not found in data")
            continue

        # pd.to_numeric with errors="coerce" turns anything that ISN'T a
        # valid number into NaN, without crashing — this is how we detect
        # "this value claims to be numeric but isn't" cleanly.
        if expected_type in (int, float):
            coerced = pd.to_numeric(df[col], errors="coerce")
            # A value that was NOT already missing, but became NaN after
            # coercion, is a genuine type problem — not just missing data.
            bad_mask = coerced.isna() & df[col].notna()
            bad_count = int(bad_mask.sum())
        else:
            # For non-numeric expected types, check with isinstance directly
            bad_count = int(df[col].apply(lambda x: not isinstance(x, expected_type) and pd.notna(x)).sum())

        if bad_count > 0:
            issues[col] = bad_count

    return issues


def check_ranges(df: pd.DataFrame, ranges: dict[str, tuple[float, float]]) -> dict[str, int]:
    """
    For each column with a defined valid range, count how many values
    fall OUTSIDE that range. ranges looks like: {"age": (0, 120)}
    """
    issues = {}
    for col, (low, high) in ranges.items():
        if col not in df.columns:
            logger.warning(f"Column '{col}' expected but not found in data")
            continue

        # Convert to numeric first so comparison doesn't crash on bad data —
        # rows that fail this conversion become NaN and are naturally excluded
        # from the range check (check_types already catches those separately).
        numeric_col = pd.to_numeric(df[col], errors="coerce")
        out_of_range = (numeric_col < low) | (numeric_col > high)
        bad_count = int(out_of_range.sum())

        if bad_count > 0:
            issues[col] = bad_count

    return issues
