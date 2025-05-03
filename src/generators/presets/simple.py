from pathlib import Path

from src.generators.base import PresetGenerator
from src.generators.utils import LayerPaths
from src.schemas import ConfigModel


class SimplePresetGenerator(PresetGenerator):
    """Generator for the simple preset without contexts."""

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate simple project structure without contexts."""
        layer_paths = LayerPaths.from_config(root_path, config)

        if not config.layers:
            return

        # Generate domain layer
        if config.layers.domain:
            self.domain_generator.generate_components(
                layer_paths.layer_1, config.layers.domain.dict()
            )

        # Generate application layer
        if config.layers.application:
            self.app_generator.generate_components(
                layer_paths.layer_2, config.layers.application.dict()
            )

        # Generate infrastructure layer
        if config.layers.infrastructure:
            self.infra_generator.generate_components(
                layer_paths.layer_3, config.layers.infrastructure.dict()
            )

        # Generate interface layer
        if config.layers.interface:
            self.interface_generator.generate_components(
                layer_paths.layer_4, config.layers.interface.dict()
            )
