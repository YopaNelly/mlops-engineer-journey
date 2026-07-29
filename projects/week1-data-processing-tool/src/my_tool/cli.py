import typer
from .config import load_config
from logger import get_logger

app = typer.Typer(help="ML Data Processing Automation Tool — cleans and validates raw data.")
logger = get_logger(__name__)

@app.command()
def clean(
    input: str = typer.Option(..., "--input", help="Path to the raw input CSV file"),
    config: str = typer.Option("configs/config.yaml", "--config", help="Path to the YAML config file"),
):
    """
    Clean and validate a raw CSV file according to the given config.
    """
    cfg = load_config(config)
    logger.info(f"Loaded config successfully: {cfg}")
    logger.info(f"Would now clean: {input}  (actual cleaning logic arrives Day 6)")

if __name__ == "__main__":
    app()
