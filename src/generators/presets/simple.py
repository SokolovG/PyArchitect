from logging import getLogger
from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generator import LayerGenerator
from src.generators.presets.base import PresetGenerator
from src.schemas import ConfigModel

logger = getLogger(__name__)


class SimplePresetGenerator(PresetGenerator, BaseGenerator):
    """Generator for the simple preset without contexts.

    This generator creates a flat structure with all layers directly
    under the root directory. Doesn't support contexts.
    """

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate simple project structure without contexts.

        Args:
            root_path: Path to the project root directory
            config: Project configuration

        """
        logger.info("Starting simple preset generation...")
        layers_data = config.layers.model_dump()
        for layer_name, layer_config in layers_data.items():
            if not layer_config:
                logger.debug(f"Skipping empty layer: {layer_name}")
                continue

            layer_path = root_path / layer_name

            self.create_directory(layer_path)
            self.create_init_file(layer_path)

            root_name = config.settings.root_name
            generator = self._create_layer_generator(
                layer_name=layer_name,
                root_name=root_name,
                group_components=config.settings.group_components,
                generate_all_exports=config.settings.generate_all_exports,
            )
            generator.generate_components(layer_path, layer_config)

        logger.info("Simple preset generation completed successfully")

    def _create_layer_generator(
        self,
        layer_name: str,
        root_name: str,
        group_components: bool,
        generate_all_exports: bool,
    ) -> LayerGenerator:
        """Create layer generator for specific layer.

        Args:
            layer_name: Layer name (domain, application, etc.)

        Returns:
            Configured LayerGenerator instance

        """
        return LayerGenerator(
            template_engine=self.template_engine,
            root_name=root_name,
            layer_name=layer_name,
            group_components=group_components,
            generate_all_exports=generate_all_exports,
        )
