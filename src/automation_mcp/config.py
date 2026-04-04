import json
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".automation-mcp"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "default_site": "",
    "sites": {},
}


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    if config_path.exists():
        with open(config_path) as f:
            stored = json.load(f)
        return {**DEFAULT_CONFIG, **stored}

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    return dict(DEFAULT_CONFIG)


def save_config(config: dict[str, Any], config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_site_config(
    site_name: str | None = None,
    config_path: Path = DEFAULT_CONFIG_PATH,
) -> dict[str, str]:
    config = load_config(config_path)
    name = site_name or config.get("default_site", "")

    if not name or name not in config.get("sites", {}):
        available = list(config.get("sites", {}).keys())
        raise ValueError(
            f"Site '{name}' não encontrado. Sites disponíveis: {available}"
        )

    return config["sites"][name]
