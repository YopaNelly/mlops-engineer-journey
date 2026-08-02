"""
The Week 1 tool restructured into 3 explicit ETL functions:
  extract() -> reads raw data
  transform() -> cleans it (reuses Day 6's functions)
  load()     -> saves it into SQLite, safely, even if run twice

Each function takes plain inputs and returns plain outputs — no hidden
shared state — so each one can be tested completely on its own.
"""

import pandas as pd
import sqlite3
from .cleaning import handle_missing, dedupe, fix_types
from logger import get_logger

logger = get_logger(__name__)


def extract(input_path: str) -> pd.DataFrame:
    """
    EXTRACT: just reads the raw file. Does no cleaning, no saving.
    Testing this only requires a sample CSV — nothing else.
    """
    df = pd.read_csv(input_path)
    logger.info(f"Extracted {len(df)} rows from {input_path}")
    return df


def transform(df: pd.DataFrame, required_columns: list[str], numeric_columns: list[str]) -> pd.DataFrame:
    """
    TRANSFORM: takes a raw dataframe in, returns a cleaned dataframe out.
    No file reading, no database writing — just pure data cleaning.
    Testing this only requires a dataframe in memory — no files, no database.
    """
    df = handle_missing(df, required_columns)
    df = dedupe(df)
    if numeric_columns:
        df = fix_types(df, numeric_columns)
    logger.info(f"Transformed data: {len(df)} rows remain")
    return df


def load(df: pd.DataFrame, db_path: str, table_name: str = "cleaned_data") -> None:
    """
    LOAD: saves the cleaned dataframe into a SQLite table.

    IMPORTANT: this is written to be IDEMPOTENT — running it 5 times in a
    row with the same data produces the same final table, not 5x the rows.

    How: instead of blindly appending (INSERT), we first DELETE any rows
    that share the same 'id' as the incoming data, then insert fresh.
    This means "load" really means "make the table match this data",
    not "add this data on top of whatever's already there."
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Make sure the table exists at all (harmless if it already does)
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            price REAL,
            category TEXT
        )
    """)

    # THE IDEMPOTENCY FIX: remove any existing rows with these same IDs
    # before inserting, so re-running this never creates duplicates.
    ids = tuple(df["id"].tolist())
    if ids:
        placeholders = ",".join("?" * len(ids))
        cursor.execute(f"DELETE FROM {table_name} WHERE id IN ({placeholders})", ids)

    # Now insert the fresh, current data
    df.to_sql(table_name, conn, if_exists="append", index=False)

    conn.commit()
    row_count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    conn.close()

    logger.info(f"Loaded {len(df)} rows into {table_name} — table now has {row_count} total rows")
