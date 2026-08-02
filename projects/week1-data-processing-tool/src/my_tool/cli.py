import typer
from .config import load_config
from .etl import extract, transform, load
from logger import get_logger

app = typer.Typer(help="ML Data Processing Automation Tool — cleans and validates raw data.")
logger = get_logger(__name__)


@app.command()
def clean(
    input: str = typer.Option(..., "--input", help="Path to the raw input CSV file"),
    config: str = typer.Option("configs/config.yaml", "--config", help="Path to the YAML config file"),
    db: str = typer.Option("cleaned_data.db", "--db", help="Path to the output SQLite database"),
):
    """
    Run the full ETL pipeline: extract, transform, load.
    """
    cfg = load_config(config)
    logger.info(f"Loaded config: {cfg}")

    df = extract(input)
    df = transform(df, cfg["required_columns"], cfg.get("numeric_columns", []))
    load(df, db)


if __name__ == "__main__":
    app()
