from logging import getLogger
from pathlib import Path

from src.core.parser import YamlParser
from src.generators.base import BaseGenerator, PresetGenerator
from src.generators.layer_generators import (
    ApplicationGenerator,
    DomainGenerator,
    InfrastructureGenerator,
    InterfaceGenerator,
)
from src.generators.presets import (
    AdvancedPresetGenerator,
    SimplePresetGenerator,
    StandardPresetGenerator,
)


class ProjectGenerator(BaseGenerator):
    """Main project generator.

    This class coordinates the generation of all project components
    and layers based on the configuration file.

    Attributes:
        parser: YAML configuration parser
        config: Parsed configuration
        domain_generator: Generator for domain layer components

    """

    PRESET_GENERATORS: dict[str, type[PresetGenerator]] = {
        "simple": SimplePresetGenerator,
        "standard": StandardPresetGenerator,
        "advanced": AdvancedPresetGenerator,
    }

    def __init__(self, path: Path) -> None:
        """Initialize the project generator.

        Args:
            path: Path to the configuration file

        """
        super().__init__()
        self.logger = getLogger(__name__)
        self.parser = YamlParser(path)
        self.config = self.parser.load()

        preset_type = self.config.settings.preset
        preset_generator_class = self.PRESET_GENERATORS.get(preset_type, StandardPresetGenerator)

        self.domain_generator = DomainGenerator()
        self.app_generator = ApplicationGenerator()
        self.infra_generator = InfrastructureGenerator()
        self.interface_generator = InterfaceGenerator()

        self.preset_generator = preset_generator_class(
            self.domain_generator,
            self.app_generator,
            self.infra_generator,
            self.interface_generator,
            self.config,
        )

    def generate(self) -> None:
        """Generate the project structure based on the preset."""
        project_root = Path.cwd()
        root_name = self.config.settings.root_name
        root_path = project_root / root_name

        self.create_directory(root_path)
        self.create_init_file(root_path)

        self.preset_generator.generate(root_path, self.config)
