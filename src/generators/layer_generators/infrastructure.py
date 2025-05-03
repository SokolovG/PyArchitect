from pathlib import Path
from typing import Any

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import InfrastructureLayerConfig


class InfrastructureGenerator(BaseGenerator, AbstractLayerGenerator):
    """Generator for the infrastructure layer components.

    This class is responsible for generating all components of the infrastructure layer
    based on the configuration.
    """

    def generate_components(self, path: Path, config: dict[str, Any]) -> None:
        """Generate all infrastructure layer components.

        Args:
            path: Path where to generate components
            config: Configuration for infrastructure components

        """
        infra_layer = InfrastructureLayerConfig(**config)
        self._generate_components(path, infra_layer)

    def _generate_components(
        self, infra_path: Path, infra_layer: InfrastructureLayerConfig
    ) -> None:
        """Generate infrastructure components based on configuration.

        Args:
            infra_path: Path where to generate components
            infra_layer: Configuration for infrastructure components

        """
