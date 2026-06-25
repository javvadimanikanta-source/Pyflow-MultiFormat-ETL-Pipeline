from pathlib import Path
from typing import Any
import json
import yaml


def load_config(config_path: str) -> dict[str, Any]:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    if path.suffix in {".yaml", ".yml"}:
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    if path.suffix == ".json":
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    raise ValueError("Only YAML and JSON config files are supported")