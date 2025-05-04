from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import InfrastructureLayerConfig, PresetType


class InfrastructureGenerator(BaseGenerator, AbstractLayerGenerator[InfrastructureLayerConfig]):
    """Generator for the infrastructure layer components.

    This class is responsible for generating all components of the infrastructure layer
    based on the configuration.
    """

    def generate_components(
        self, path: Path, config: InfrastructureLayerConfig, preset: PresetType
    ) -> None:
        """Generate all infrastructure layer components.

        Args:
            path: Path where to generate components
            config: Configuration for infrastructure components
            preset: Selected preset in the settings

        """
        self._generate_components(path, config)

    def _generate_components(
        self, infra_path: Path, infra_layer: InfrastructureLayerConfig
    ) -> None:
        """Generate infrastructure components based on configuration.

        Args:
            infra_path: Path where to generate components
            infra_layer: Configuration for infrastructure components

        """
