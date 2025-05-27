from logging import getLogger
from pathlib import Path

from src.generators.presets.base import BasePresetGenerator
from src.schemas import ConfigModel

logger = getLogger(__name__)


class StandardPresetGenerator(BasePresetGenerator):
    """Generator for the standard preset with contexts in layers."""

    def generate(self, root_path: Path, config: ConfigModel, preview_mode: bool) -> None:
        """Generate standard project structure with contexts organized by layers.

        This method creates a project structure where contexts are organized within
        architectural layers, with a standard DDD organization. Each layer contains
        multiple bounded contexts with their specific components.

        Args:
            root_path: Path to the project root directory
            config: Project configuration model containing settings and layer definitions
            preview_mode: Special mode for dry generation

        """
        logger.debug("Starting standard preset generation...")

        layers_data = config.layers.model_dump()
        for layer_name, layer_config in layers_data.items():
            if not layer_config:
                continue

            layer_path = self.create_layer_dir(root_path, layer_name)

            if isinstance(layer_config, dict) and "contexts" in layer_config:
                contexts = layer_config["contexts"]
                remaining_config = {k: v for k, v in layer_config.items() if k != "contexts"}

                for context in contexts:
                    context_name = context.pop("name", "default")
                    context_path = layer_path / context_name
                    self.file_ops.create_directory(context_path)
                    self.file_ops.create_init_file(context_path)

                    for component_type, components in context.items():
                        component_dir = self.create_component_dir(context_path, component_type)
                        layer_generator = self._get_layer_generator(
                            layer_name=layer_name,
                            root_name=config.settings.root_name,
                            group_components=config.settings.group_components,
                            init_imports=config.settings.init_imports,
                            context_name=context_name,
                            preview_collector=self.context.preview_collector,
                        )
                        layer_generator.generate_components(
                            component_dir, component_type, components
                        )

                layer_config = remaining_config

            if isinstance(layer_config, dict):
                for component_type, components in layer_config.items():
                    if not components:
                        continue

                    component_dir = self.create_component_dir(layer_path, component_type)
                    layer_generator = self._get_layer_generator(
                        layer_name=layer_name,
                        root_name=config.settings.root_name,
                        group_components=config.settings.group_components,
                        init_imports=config.settings.init_imports,
                        preview_collector=self.context.preview_collector,
                    )
                    layer_generator.generate_components(component_dir, component_type, components)

        logger.debug("Standard preset generation completed successfully")
