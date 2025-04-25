from pathlib import Path

from src.generator import ProjectGenerator
from src.generator_helper import DomainGenerator, GeneratorHelper
from src.parser import YamlParser


def main() -> None:
    """Entry point."""
    project_root = Path(__file__).parent.parent
    config_path = project_root / "ddd-config.yaml"

    try:
        parser = YamlParser(str(config_path))
        helper = GeneratorHelper()
        domain_helper = DomainGenerator()
        generator = ProjectGenerator(
            parser=parser,
            helper=helper,
            domain_helper=domain_helper,
        )
        generator.generate()

    except Exception as error:
        print(f"Error: {error}")
        exit(1)


if __name__ == "__main__":
    main()
