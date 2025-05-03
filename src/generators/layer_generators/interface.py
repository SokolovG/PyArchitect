from pathlib import Path
from typing import Any

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import InterfaceLayerConfig


class InterfaceGenerator(BaseGenerator, AbstractLayerGenerator):
    """Generator for the domain layer components.

    This class is responsible for generating all components of the domain layer
    based on the configuration.
    """

    def generate_components(self, path: Path, config: dict[str, Any]) -> None:
        """Generate all interface layer components.

        Args:
            path: Path where to generate components
            config: Configuration for interface components

        """
        interface_layer = InterfaceLayerConfig(**config)
        self._generate_components(path, interface_layer)

    def _generate_components(
        self, interface_path: Path, interface_layer: InterfaceLayerConfig
    ) -> None:
        """Generate  interface components.

        Args:
            interface_path: Path where to generate components
            interface_layer: Configuration for interface components

        """
