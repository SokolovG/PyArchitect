from logging import getLogger
from pathlib import Path

from src.generators.base import GeneratorUtilsMixin
from src.generators.layer_generator import LayerGenerator
from src.generators.presets.base import AbstractPresetGenerator
from src.schemas import ConfigModel

logger = getLogger(__name__)


class AdvancedPresetGenerator(AbstractPresetGenerator, GeneratorUtilsMixin):
    """Generator for the advanced preset with custom layout.

    This generator creates a project structure with custom layout options,
    allowing for more flexibility in organizing bounded contexts and layers.
    """

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate advanced project structure with custom organization.

        This implementation allows for highly customized project layouts,
        supporting both nested contexts (layers inside contexts) and
        other advanced organizational patterns.

        Args:
            root_path: Path to the project root directory
            config: Project configuration model containing settings and layout definitions

        """
        logger.info("Starting advanced preset generation...")
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
