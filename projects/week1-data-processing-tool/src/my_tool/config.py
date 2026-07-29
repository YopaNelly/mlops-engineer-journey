import yaml
from pathlib import Path
from exceptions import ConfigMissingError

# Keys that MUST exist in any config file for this tool to run safely
REQUIRED_KEYS = ["required_columns"]

def load_config(path: str) -> dict:
    """
    Loads a YAML config file and checks it has everything this tool needs.
    Raises a clear, specific error if something required is missing,
    instead of silently continuing with incomplete settings.
    """
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(config_path) as f:
        cfg = yaml.safe_load(f) or {}

    missing = [key for key in REQUIRED_KEYS if key not in cfg]
    if missing:
        raise ConfigMissingError(
            f"Config is missing required key(s): {missing}. "
            f"Check {path} and add them before continuing."
        )

    return cfg
