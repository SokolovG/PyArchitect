from logging import getLogger
from pathlib import Path

from src.generators.base import GeneratorUtilsMixin
from src.generators.layer_generator import LayerGenerator
from src.generators.presets.base import AbstractPresetGenerator
from src.schemas import ConfigModel

logger = getLogger(__name__)


class StandardPresetGenerator(AbstractPresetGenerator, GeneratorUtilsMixin):
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
        logger.info("Starting standard preset generation...")
        layers_data = config.layers.model_dump()
        for layer_name, layer_config in layers_data.items():
            if not layer_config:
                continue

            layer_path = root_path / layer_name

            self.create_directory(layer_path)
            self.create_init_file(layer_path)

            root_name = config.settings.root_name
            generator = self._create_layer_generator(
                layer_name=layer_name,
                root_name=root_name,
                group_components=config.settings.group_components,
                init_imports=config.settings.init_imports,
            )
            generator.generate_components(layer_path, layer_config)  # noqa

        logger.info("Standard preset generation completed successfully")

    def _create_layer_generator(
        self,
        layer_name: str,
        root_name: str,
        group_components: bool,
        init_imports: bool,
    ) -> LayerGenerator:
        """Create layer generator for specific layer.

        Args:
            layer_name: Layer name (domain, application, etc.)
            root_name: f
            group_components: f
            init_imports: f

        Returns:
            Configured LayerGenerator instance

        """
        return LayerGenerator(
            template_engine=self.template_engine,
            root_name=root_name,
            layer_name=layer_name,
            group_components=group_components,
            init_imports=init_imports,
        )
