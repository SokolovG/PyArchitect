from logging import getLogger
from pathlib import Path

from icecream import ic

from src.generators.presets.base import BasePresetGenerator
from src.schemas import ConfigModel

logger = getLogger(__name__)


class AdvancedPresetGenerator(BasePresetGenerator):
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
        logger.debug("Starting advanced preset generation...")

        layers_data = config.layers.model_dump().get("contexts")
        for context_config in layers_data:  # type:ignore[union-attr]
            context_name = context_config.get("name")
            ic(context_name)
            context_path = self.create_layer_dir(root_path, context_name)

            for layer_name, layer_components in context_config.items():
                if layer_name == "name":
                    continue
                ic(layer_name, layer_components)

                layer_generator = self._get_layer_generator(
                    layer_name=layer_name,
                    root_name=config.settings.root_name,
                    group_components=config.settings.group_components,
                    init_imports=config.settings.init_imports,
                )

                layer_path = self.create_layer_dir(context_path, layer_name)
                for component_type, component_values in layer_components.items():
                    ic(component_type, component_values)
                    component_dir = self.create_component_dir(layer_path, component_type)

                    layer_generator.generate_components(
                        component_dir, component_type, component_values
                    )

        logger.debug("Advanced preset generation completed successfully")
