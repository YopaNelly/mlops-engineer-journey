import pandas as pd
from logger import get_logger
from exceptions import DataValidationError

logger = get_logger(__name__)

def check_row_count(df: pd.DataFrame):
    """
    A tiny example check: warns if the dataframe looks suspiciously small,
    and raises a real error if it's completely empty.
    """
    if len(df) == 0:
        logger.error("DataValidationError: dataframe is completely empty")
        raise DataValidationError("Dataframe has zero rows — cannot continue")

    if len(df) < 5:
        logger.warning(f"Dataframe looks unusually small: only {len(df)} rows")

def hello():
    logger.info("Week 1 project started")

    # A tiny fake dataset to demonstrate both log levels
    small_df = pd.DataFrame({"id": [1, 2]})   # small enough to trigger WARNING
    check_row_count(small_df)

    empty_df = pd.DataFrame()                  # empty, will trigger ERROR
    try:
        check_row_count(empty_df)
    except DataValidationError as e:
        logger.error(f"Caught expected error: {e}")

    logger.info("Week 1 project finished")

if __name__ == "__main__":
    hello()
