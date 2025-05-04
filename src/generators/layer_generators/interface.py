from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import InterfaceLayerConfig, PresetType


class InterfaceGenerator(BaseGenerator, AbstractLayerGenerator[InterfaceLayerConfig]):
    """Generator for the domain layer components.

    This class is responsible for generating all components of the domain layer
    based on the configuration.
    """

    def generate_components(
        self, path: Path, config: InterfaceLayerConfig, preset: PresetType
    ) -> None:
        """Generate all interface layer components.

        Args:
            path: Path where to generate components
            config: Configuration for interface components
            preset: Selected preset in the settings

        """
        self._generate_components(path, config)

    def _generate_components(
        self, interface_path: Path, interface_layer: InterfaceLayerConfig
    ) -> None:
        """Generate  interface components.

        Args:
            interface_path: Path where to generate components
            interface_layer: Configuration for interface components

        """
