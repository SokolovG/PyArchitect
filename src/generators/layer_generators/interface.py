from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import InterfaceLayerConfig, PresetType


class InterfaceGenerator(BaseGenerator, AbstractLayerGenerator[InterfaceLayerConfig]):
    """Generator for the domain layer components.

    This class is responsible for generating all components of the domain layer
    based on the configuration.
    """

    def generate_components(self, path: Path, config: dict, preset: PresetType) -> None:
        """Generate all interface layer components.

        Args:
            path: Path where to generate components
            config: Configuration for interface components
            preset: Selected preset in the settings

        """
        flat_config = preset.value
        if flat_config == preset.SIMPLE:
            flat = True
        else:
            flat = False
        self._generate_components(path, config, flat)

    def _generate_components(
        self, interface_path: Path, interface_layer: dict, flat: bool = False
    ) -> None:
        """Generate  interface components.

        Args:
            interface_path: Path where to generate components
            interface_layer: Configuration for interface components
            flat: Whether to use flat structure instead of nested

        """
        for component_type, components in interface_layer.items():
            if not components or not isinstance(components, list):
                continue

            component_dir = interface_path

            if not flat:
                component_dir = interface_path / component_type
                self.create_directory(component_dir)
                self.create_init_file(component_dir)
