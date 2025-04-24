from pathlib import Path
from pprint import pprint

from src.parser import YamlParser


def main() -> None:
    """Entry point."""
    project_root = Path(__file__).parent.parent
    config_path = project_root / "ddd-config.yaml"

    try:
        parser = YamlParser(str(config_path))
        data = parser.load()
        pprint(f"Successfully loaded configuration: {data}")

    except Exception as error:
        print(f"Error: {error}")
        exit(1)


if __name__ == "__main__":
    main()
