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
    and layers based on the configuration file, supporting different
    architectural presets.
    """

    PRESET_GENERATORS: dict[str, type[AbstractPresetGenerator]] = {
        "simple": SimplePresetGenerator,
        "standard": StandardPresetGenerator,
        "advanced": AdvancedPresetGenerator,
    }

    def __init__(self, context: GenerationContext) -> None:
        """Initialize the project generator.

        Args:
            context: Project configuration context

        """
        self.context = context
        if self.context.preview_mode:
            self.file_ops = FileOperations(context.engine, context.preview_collector)
        else:
            self.file_ops = FileOperations(context.engine)

        preset_type = self.context.config.settings.preset
        preset_generator_class = self.PRESET_GENERATORS.get(preset_type, StandardPresetGenerator)
        logger.debug(f"Set preset - {preset_generator_class}")

        self.preset_generator = preset_generator_class(self.context)

    def generate(self) -> None:
        """Generate the project structure based on the preset.

        Creates the project root directory and initializes the structure
        according to the selected preset configuration.
        """
        logger.debug("Project generator starting...")

        project_root = Path.cwd()
        root_name = self.context.config.settings.root_name
        root_path = project_root / root_name
        self.file_ops.create_directory(root_path)
        self.file_ops.create_init_file(root_path)
        self.preset_generator.generate(root_path, self.context.config, self.context.preview_mode)
