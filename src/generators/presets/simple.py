from pathlib import Path

from src.generators.presets.base import PresetGenerator
from src.generators.utils import LayerPaths
from src.schemas import ConfigModel
from src.schemas.config_schema import PresetType


class SimplePresetGenerator(PresetGenerator):
    """Generator for the simple preset without contexts."""

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate simple project structure without contexts."""
        layer_paths = LayerPaths.from_config(root_path, config)

        if not config.layers:
            return

        if config.layers.domain:
            self.domain_generator.generate_components(
                layer_paths.layer_1, config.layers.domain, PresetType.SIMPLE
            )

        if config.layers.application:
            self.app_generator.generate_components(
                layer_paths.layer_2, config.layers.application, PresetType.SIMPLE
            )

        if config.layers.infrastructure:
            self.infra_generator.generate_components(
                layer_paths.layer_3, config.layers.infrastructure, PresetType.SIMPLE
            )

        if config.layers.interface:
            self.interface_generator.generate_components(
                layer_paths.layer_4, config.layers.interface, PresetType.SIMPLE
            )
