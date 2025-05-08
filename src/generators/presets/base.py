from pathlib import Path

from src.schemas import ConfigModel


class PresetGenerator:
    """Base class for preset-specific generators."""

    def __init__(
        self,
        config: ConfigModel,
    ) -> None:
        """Initialize the preset generator with layer generators and configuration.

        Args:
            config: Project configuration

        """
        self.config = config

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate project structure according to preset.

        Args:
            root_path: Root path where to generate the project
            config: Project configuration

        """
