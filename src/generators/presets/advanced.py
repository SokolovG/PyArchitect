from pathlib import Path

from src.generators.presets.base import PresetGenerator
from src.schemas import ConfigModel


class AdvancedPresetGenerator(PresetGenerator):
    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate simple project structure without contexts."""
