from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.presets.base import PresetGenerator
from src.schemas import ConfigModel


class StandardPresetGenerator(PresetGenerator, BaseGenerator):
    """Generator for the standard preset with contexts in layers."""

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate standard project structure with contexts organized by layers."""
