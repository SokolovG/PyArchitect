from pathlib import Path

from src.generators.presets.base import PresetGenerator
from src.generators.utils import LayerPaths
from src.schemas import ConfigModel
from src.schemas.config_schema import PresetType


class StandardPresetGenerator(PresetGenerator):
    """Generator for the standard preset with contexts in layers."""

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate standard project structure with contexts organized by layers."""
        layer_paths = LayerPaths.from_config(root_path, config)

        layer_paths = LayerPaths.from_config(root_path, config)

        if not config.layers:
            return

        if config.layers.domain:
            self.domain_generator.generate_components(
                layer_paths.layer_1, config.layers.domain, PresetType.STANDARD
            )

        if config.layers.application:
            self.app_generator.generate_components(
                layer_paths.layer_2, config.layers.application, PresetType.STANDARD
            )

        if config.layers.infrastructure:
            self.infra_generator.generate_components(
                layer_paths.layer_3, config.layers.infrastructure, PresetType.STANDARD
            )

        if config.layers.interface:
            self.interface_generator.generate_components(
                layer_paths.layer_4, config.layers.interface, PresetType.STANDARD
            )
