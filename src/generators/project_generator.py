from logging import getLogger
from pathlib import Path

from src.core.template_engine import TemplateEngine
from src.generators.presets import (
    AdvancedPresetGenerator,
    SimplePresetGenerator,
    StandardPresetGenerator,
)
from src.generators.presets.base import AbstractPresetGenerator
from src.generators.utils import GeneratorUtilsMixin
from src.schemas import ConfigModel

logger = getLogger(__name__)


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

    def __init__(
        self, config: ConfigModel, engine: TemplateEngine, preview_mode: bool = False
    ) -> None:
        """Initialize the project generator.

        Args:
            config: Model config
            engine: TemplateEngine
            preview_mode: Preview mode

        """
        super().__init__(engine)
        self.config = config
        self.preview_mode = preview_mode

        preset_type = self.config.settings.preset
        preset_generator_class = self.PRESET_GENERATORS.get(preset_type, StandardPresetGenerator)
        logger.debug(f"Set preset - {preset_generator_class}")

        self.preset_generator = preset_generator_class(self.config, engine)  # type: ignore

    def generate(self) -> None:
        """Generate the project structure based on the preset.

        Args:
            If None, use default.

        """
        logger.debug("Project generator starting...")

        project_root = Path.cwd()
        root_name = self.config.settings.root_name
        root_path = project_root / root_name
        self.create_directory(root_path)
        self.create_init_file(root_path)

        self.preset_generator.generate(root_path, self.config, self.preview_mode)
