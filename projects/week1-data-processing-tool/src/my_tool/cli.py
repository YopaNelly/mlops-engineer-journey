import typer
import pandas as pd
from .config import load_config
from .cleaning import handle_missing, fix_types, dedupe
from logger import get_logger

app = typer.Typer(help="ML Data Processing Automation Tool — cleans and validates raw data.")
logger = get_logger(__name__)


@app.command()
def clean(
    input: str = typer.Option(..., "--input", help="Path to the raw input CSV file"),
    config: str = typer.Option("configs/config.yaml", "--config", help="Path to the YAML config file"),
    output: str = typer.Option("cleaned_output.csv", "--output", help="Where to save the cleaned CSV"),
):
    """
    Clean and validate a raw CSV file according to the given config.
    """
    # Step 1: load and validate the config (built on Day 5)
    cfg = load_config(config)
    logger.info(f"Loaded config: {cfg}")

    # Step 2: load the raw data
    df = pd.read_csv(input)
    logger.info(f"Loaded {len(df)} rows from {input}")

    # Step 3: run each cleaning step, one at a time, in a clear order
    df = handle_missing(df, cfg["required_columns"])
    df = dedupe(df)

    # Only try to fix number columns if the config actually specifies any.
    # .get() with a default of [] means "if this key isn't in the config,
    # just use an empty list instead of crashing."
    numeric_cols = cfg.get("numeric_columns", [])
    if numeric_cols:
        df = fix_types(df, numeric_cols)

    # Step 4: save the result
    df.to_csv(output, index=False)
    logger.info(f"Saved cleaned data to {output} ({len(df)} rows remaining)")


if __name__ == "__main__":
    app()
