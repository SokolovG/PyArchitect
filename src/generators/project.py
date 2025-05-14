from logging import getLogger
from pathlib import Path

from src.generators.base import GeneratorUtilsMixin
from src.generators.presets import (
    AdvancedPresetGenerator,
    SimplePresetGenerator,
    StandardPresetGenerator,
)
from src.generators.presets.base import AbstractPresetGenerator
from src.schemas import ConfigModel
from src.templates.engine import TemplateEngine


class ProjectGenerator(GeneratorUtilsMixin):
    """Main project generator.

    This class coordinates the generation of all project components
    and layers based on the configuration file.
    """

    PRESET_GENERATORS: dict[str, type[AbstractPresetGenerator]] = {
        "simple": SimplePresetGenerator,
        "standard": StandardPresetGenerator,
        "advanced": AdvancedPresetGenerator,
    }

    def __init__(self, config: ConfigModel, engine: TemplateEngine) -> None:
        """Initialize the project generator.

        Args:
            config: Model config
            engine: TemplateEngine

        """
        super().__init__(engine)
        self.config = config
        self.logger = getLogger(__name__)

        preset_type = self.config.settings.preset
        preset_generator_class = self.PRESET_GENERATORS.get(preset_type, StandardPresetGenerator)

        self.preset_generator = preset_generator_class(self.config)
        self.preset_generator.template_engine = engine  # type: ignore

    def generate(self) -> None:
        """Generate the project structure based on the preset."""
        self.logger.info("Project generator staring...")
        project_root = Path.cwd()
        root_name = self.config.settings.root_name
        root_path = project_root / root_name
        self.create_directory(root_path)
        self.create_init_file(root_path)

        self.preset_generator.generate(root_path, self.config)
