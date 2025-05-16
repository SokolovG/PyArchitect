from logging import getLogger
from pathlib import Path

from src.generators.presets.base import BasePresetGenerator
from src.schemas import ConfigModel

logger = getLogger(__name__)


class SimplePresetGenerator(BasePresetGenerator):
    """Generator for the simple preset without contexts."""

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate simple project structure without contexts."""
        logger.debug("Starting simple preset generation...")

        layers_data = config.layers.model_dump()
        for layer_name, layer_config in layers_data.items():
            if not layer_config:
                continue

            layer_path = self.create_layer_dir(root_path, layer_name)

            for component_type, components in layer_config.items():
                if not components:
                    continue

                component_dir = self.create_component_dir(layer_path, component_type)

                layer_generator = self._get_layer_generator(
                    layer_name=layer_name,
                    root_name=config.settings.root_name,
                    group_components=config.settings.group_components,
                    init_imports=config.settings.init_imports,
                )

                layer_generator.generate_components(component_dir, component_type, components)

        logger.debug("Simple preset generation completed successfully")
