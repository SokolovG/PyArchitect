from pathlib import Path
from typing import Any

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import DomainLayerConfig


class DomainGenerator(BaseGenerator, AbstractLayerGenerator):
    """Generator for the domain layer components.

    This class is responsible for generating all components of the domain layer
    based on the configuration.
    """

    def generate_components(self, path: Path, config: dict[str, Any]) -> None:
        """Generate all domain layer components.

        Args:
            path: Path where to generate components
            config: Configuration for domain components

        """
        domain_layer = DomainLayerConfig(**config)
        flat = config.get("flat", False)
        self._generate_components(path, domain_layer, flat)

    def _generate_components(
        self, domain_path: Path, domain_layer: DomainLayerConfig, flat: bool = False
    ) -> None:
        """Generate domain components based on configuration.

        Args:
            domain_path: Path where to generate components
            domain_layer: Configuration for domain components
            flat: Whether to use flat structure instead of nested

        """
