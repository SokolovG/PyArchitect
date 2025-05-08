from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import ApplicationLayerConfig, PresetType


class ApplicationGenerator(BaseGenerator, AbstractLayerGenerator[ApplicationLayerConfig]):
    """Generator for the application layer components.

    This class is responsible for generating all components of the application layer
    based on the configuration.
    """

    def generate_components(self, path: Path, config: dict, preset: PresetType) -> None:
        """Generate all application layer components.

        Args:
            path: Path where to generate components
            config: Configuration for application components
            preset: Selected preset in the settings

        """
        flat_config = preset.value
        if flat_config == preset.SIMPLE:
            flat = True
        else:
            flat = False
        self._generate_components(path, config, flat)

    def _generate_components(self, app_path: Path, app_layer: dict, flat: bool = False) -> None:
        """Generate application components based on configuration.

        Args:
            app_path: Path where to generate components
            app_layer: Configuration for application components
            flat: Whether to use flat structure instead of nested

        """
        for component_type, components in app_layer.items():
            if not components or not isinstance(components, list):
                continue

            component_dir = app_path

            if not flat:
                component_dir = app_path / component_type
                self.create_directory(component_dir)
                self.create_init_file(component_dir)
