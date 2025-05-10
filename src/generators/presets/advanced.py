from logging import getLogger
from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generator import LayerGenerator
from src.generators.presets.base import PresetGenerator
from src.schemas import ConfigModel
from src.schemas.config_schema import ContextsLayout

logger = getLogger(__name__)


class AdvancedPresetGenerator(PresetGenerator, BaseGenerator):
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

        # Configuration is already available through the config parameter

        # Get configuration for components
        layers_data = config.layers.model_dump()

        # Check context layout type
        if config.settings.contexts_layout == ContextsLayout.NESTED:
            # Nested layout: Layers inside contexts
            self._generate_nested_layout(root_path, config, layers_data)
        else:
            # Flat layout: Similar to standard but with more options
            self._generate_flat_layout(root_path, config, layers_data)

        logger.info("Advanced preset generation completed successfully")

    def _generate_nested_layout(
        self, root_path: Path, config: ConfigModel, layers_data: dict
    ) -> None:
        """Generate nested layout with layers inside contexts.

        Args:
            root_path: Project root path
            config: Project configuration
            layers_data: Layer configuration data

        """
        # For each context, create all layers inside it
        for context_name, context_config in layers_data.items():
            if not isinstance(context_config, dict):
                continue

            context_path = root_path / context_name
            self.create_directory(context_path)
            self.create_init_file(context_path)

            # Create each layer inside the context
            for layer_name, layer_config in context_config.items():
                if not layer_config:
                    continue

                layer_path = context_path / layer_name
                self.create_directory(layer_path)
                self.create_init_file(layer_path)

                # Generate components for this layer
                generator = LayerGenerator(self.template_engine, layer_name)
                generator.generate_components(layer_path, layer_config)

    def _generate_flat_layout(
        self, root_path: Path, config: ConfigModel, layers_data: dict
    ) -> None:
        """Generate flat layout with contexts inside layers.

        Args:
            root_path: Project root path
            config: Project configuration
            layers_data: Layer configuration data

        """
        # Create each layer directory
        for layer_name, layer_config in layers_data.items():
            if not layer_config:
                continue

            layer_path = root_path / layer_name
            self.create_directory(layer_path)
            self.create_init_file(layer_path)

            # Advanced layout allows grouping components or custom organization
            if config.settings.group_components:
                # Group by component type
                generator = LayerGenerator(self.template_engine, layer_name)
                generator.generate_components(layer_path, layer_config)
            else:
                # Custom organization based on configuration
                for component_type, components in layer_config.items():
                    component_dir = layer_path / component_type
                    self.create_directory(component_dir)
                    self.create_init_file(component_dir)

                    # Generate each component
                    for component_name in components:
                        component_path = component_dir / f"{component_name.lower()}.py"
                        template_path = "base_template.py.jinja"
                        content = self.template_engine.render(
                            template_path, {"name": component_name, "type": component_type}
                        )
                        self.write_file(component_path, content)
