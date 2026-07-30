"""
This file holds the actual data-cleaning logic.
Each function does ONE clean-up job, and logs a short summary
of what it did, so nothing happens silently.
"""

import pandas as pd
from logger import get_logger

logger = get_logger(__name__)


def handle_missing(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    """
    Looks at the columns we absolutely need (required_columns).
    Any row missing a value in ANY of those columns gets dropped,
    because a row with missing critical data isn't safe to use later.
    """
    # Count how many rows have a missing value in any required column,
    # BEFORE we touch anything — so we can report exactly what we removed.
    missing_mask = df[required_columns].isna().any(axis=1)
    num_missing = int(missing_mask.sum())

    if num_missing > 0:
        logger.warning(f"Dropping {num_missing} row(s) with missing required values")
    else:
        logger.info("No missing values found in required columns")

    # Keep only the rows where missing_mask is False (i.e. nothing was missing)
    cleaned_df = df[~missing_mask].copy()
    return cleaned_df


def fix_types(df: pd.DataFrame, numeric_columns: list[str]) -> pd.DataFrame:
    """
    Makes sure columns that are SUPPOSED to be numbers actually are numbers.
    Real-world data often has numbers stored as text, sometimes with
    symbols like '$' or ',' mixed in — this function cleans and converts them.
    """
    df = df.copy()

    for col in numeric_columns:
        # Remember how many valid (non-missing) values we had BEFORE converting,
        # so we can compare after and catch anything that silently broke.
        before_valid_count = df[col].notna().sum()

        # Strip out common junk characters that stop a value from being read as a number:
        # '$' (currency), ',' (thousands separator)
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
        )

        # Now actually convert to a real number.
        # errors="coerce" means: if something still can't be converted,
        # turn it into NaN INSTEAD of crashing the whole program.
        df[col] = pd.to_numeric(df[col], errors="coerce")

        after_valid_count = df[col].notna().sum()
        newly_broken = before_valid_count - after_valid_count

        # THIS is the check that directly answers today's Challenge question.
        # If a column that used to have real values now has fewer valid numbers,
        # something went wrong during conversion — and we log it LOUDLY,
        # instead of letting it quietly become a column full of NaN.
        if newly_broken > 0:
            logger.error(
                f"Column '{col}': {newly_broken} value(s) became invalid (NaN) "
                f"after type conversion — check for unexpected symbols or formats"
            )
        else:
            logger.info(f"Column '{col}' converted to numeric successfully")

    return df


def dedupe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes exact duplicate rows — rows that are 100% identical to another row.
    """
    num_before = len(df)
    df_deduped = df.drop_duplicates()
    num_removed = num_before - len(df_deduped)

    if num_removed > 0:
        logger.warning(f"Removed {num_removed} duplicate row(s)")
    else:
        logger.info("No duplicate rows found")

    return df_deduped
