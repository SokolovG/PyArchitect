from logging import getLogger
from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generator import LayerGenerator
from src.generators.presets.base import PresetGenerator
from src.schemas import ConfigModel


class StandardPresetGenerator(PresetGenerator, BaseGenerator):
    """Generator for the standard preset with contexts in layers."""

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate standard project structure with contexts organized by layers.

        This method creates a project structure where contexts are organized within
        architectural layers, with a standard DDD organization. Each layer contains
        multiple bounded contexts with their specific components.

        Args:
            root_path: Path to the project root directory
            config: Project configuration model containing settings and layer definitions

        """
        logger = getLogger(__name__)
        logger.info("Starting standard preset generation...")

        domain_layer = config.settings.domain_layer
        application_layer = config.settings.application_layer
        infrastructure_layer = config.settings.infrastructure_layer
        interface_layer = config.settings.interface_layer

        layers_data = config.layers.model_dump()

        for layer_name in [domain_layer, application_layer, infrastructure_layer, interface_layer]:
            layer_path = root_path / layer_name
            self.create_directory(layer_path)
            self.create_init_file(layer_path)

            if layer_name not in layers_data or not layers_data[layer_name]:
                logger.debug(f"Skipping empty layer: {layer_name}")
                continue

            generator = LayerGenerator(self.template_engine, layer_name)
            generator.generate_components(layer_path, layers_data[layer_name])

        logger.info("Standard preset generation completed successfully")
