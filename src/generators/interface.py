from pathlib import Path

from src.generators.base import BaseGenerator
from src.schemas.config_schema import InterfaceLayer


class InterfaceGenerator(BaseGenerator):
    """Generator for the domain layer components.

    This class is responsible for generating all components of the domain layer
    based on the configuration.
    """

    def generate_interface_components(
        self, interface_path: Path, domain_layer: InterfaceLayer
    ) -> None:
        """Generate all interface layer components.

        Args:
            interface_path: Path where to generate components
            domain_layer: Configuration for interface components

        """
        pass
