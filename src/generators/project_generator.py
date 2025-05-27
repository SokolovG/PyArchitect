from logging import getLogger
from pathlib import Path

from src.core.utils import GenerationContext
from src.generators.presets import (
    AdvancedPresetGenerator,
    SimplePresetGenerator,
    StandardPresetGenerator,
)
from src.generators.presets.base import AbstractPresetGenerator
from src.generators.utils import FileOperations

logger = getLogger(__name__)


class ProjectGenerator:
    """Main project generator.

    This class coordinates the generation of all project components
    and layers based on the configuration file.
    """

    PRESET_GENERATORS: dict[str, type[AbstractPresetGenerator]] = {
        "simple": SimplePresetGenerator,
        "standard": StandardPresetGenerator,
        "advanced": AdvancedPresetGenerator,
    }

    def __init__(self, context: GenerationContext) -> None:
        """Initialize the project generator.

        Args:
            context: Context config


        """
        self.context = context
        self.file_ops = FileOperations(context.engine, context.preview_collector)

        preset_type = self.context.config.settings.preset
        preset_generator_class = self.PRESET_GENERATORS.get(preset_type, StandardPresetGenerator)
        logger.debug(f"Set preset - {preset_generator_class}")

        self.preset_generator = preset_generator_class(self.context)

    def generate(self) -> None:
        """Generate the project structure based on the preset.

        Args:
            If None, use default.

        """
        logger.debug("Project generator starting...")

        project_root = Path.cwd()
        root_name = self.context.config.settings.root_name
        root_path = project_root / root_name
        self.file_ops.create_directory(root_path)
        self.file_ops.create_init_file(root_path)
        self.preset_generator.generate(root_path, self.context.config, self.context.preview_mode)
