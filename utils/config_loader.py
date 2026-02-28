from pathlib import Path
from typing import Any
import yaml
from exception.custom_exception import ExceptionHandler
from logger.custom_logger import CustomLogger

# Initialize module-level logger and exception handler
app_logger = CustomLogger().get_logger(__file__)
exception_handler = ExceptionHandler()


def load_config(config_relative_path: str = "config/config.yaml") -> dict[str, Any]:
    """Load YAML config from a project-relative path and return it as a dict."""
    try:
        # Step 1 — Build absolute path from project root
        config_path = Path(__file__).resolve().parents[1] / config_relative_path
        app_logger.info("Loading configuration", config_path=str(config_path))

        # Step 2 — Verify the config file exists
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        # Step 3 — Read and parse YAML content
        with config_path.open("r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}

        # Step 4 — Log success and return parsed config
        app_logger.info("Configuration loaded successfully", keys=len(config_data))
        return config_data

    except Exception as error:
        # Step 5 — Handle exception (create, log, raise) in one reusable call
        exception_handler.handle_exception(
            f"Failed to load config from '{config_relative_path}'.", error=error
        )


if __name__ == "__main__":
    config = load_config()
    print("\n--- Loaded Configuration ---")
    for key, value in config.items():
        print(f"  {key}: {value}")
