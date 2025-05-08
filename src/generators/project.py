from logging import getLogger
from pathlib import Path

from src.generators.base import BaseGenerator
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
from src.generators.presets.base import PresetGenerator
from src.schemas import ConfigModel


class ProjectGenerator(BaseGenerator):
    """Main project generator.

    This class coordinates the generation of all project components
    and layers based on the configuration file.
    """

    PRESET_GENERATORS: dict[str, type[PresetGenerator]] = {
        "simple": SimplePresetGenerator,
        "standard": StandardPresetGenerator,
        "advanced": AdvancedPresetGenerator,
    }

    def __init__(
        self,
        config: ConfigModel,
        domain_generator: DomainGenerator,
        app_generator: ApplicationGenerator,
        infra_generator: InfrastructureGenerator,
        interface_generator: InterfaceGenerator,
    ) -> None:
        """Initialize the project generator."""
        self.config = config
        self.domain_generator = domain_generator
        self.app_generator = app_generator
        self.infra_generator = infra_generator
        self.interface_generator = interface_generator
        self.logger = getLogger(__name__)

        preset_type = self.config.settings.preset
        preset_generator_class = self.PRESET_GENERATORS.get(preset_type, StandardPresetGenerator)

        self.preset_generator = preset_generator_class(
            self.domain_generator,
            self.app_generator,
            self.infra_generator,
            self.interface_generator,
            self.config,
        )

    def generate(self) -> None:
        """Generate the project structure based on the preset."""
        self.logger.info("Project generator staring...")
        project_root = Path.cwd()
        root_name = self.config.settings.root_name
        root_path = project_root / root_name
        self.logger.info(f"path {root_path}")
        self.create_directory(root_path)
        self.create_init_file(root_path)

        self.preset_generator.generate(root_path, self.config)
