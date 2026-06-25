from pyflow.config_manager import load_config
from pyflow.orchestrator import run_pipeline


def main() -> None:
    config = load_config("config/config.yaml")
    run_pipeline(config)


if __name__ == "__main__":
    main()