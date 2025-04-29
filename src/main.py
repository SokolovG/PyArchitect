from pathlib import Path

from src.generators import ProjectGenerator


def main() -> None:
    """Entry point for the application.

    This function initializes the project generator with the
    configuration file and starts the generation process.
    """
    project_root = Path(__file__).parent.parent
    config_path = project_root / "ddd-config.yaml"

    try:
        generator = ProjectGenerator(config_path)
        generator.generate()

    except Exception as error:
        print(f"Error: {error}")
        exit(1)
