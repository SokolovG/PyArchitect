from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import InfrastructureLayerConfig, PresetType


class InfrastructureGenerator(BaseGenerator, AbstractLayerGenerator[InfrastructureLayerConfig]):
    """Generator for the infrastructure layer components.

    This class is responsible for generating all components of the infrastructure layer
    based on the configuration.
    """

    def generate_components(self, path: Path, config: dict, preset: PresetType) -> None:
        """Generate all infrastructure layer components.

        Args:
            path: Path where to generate components
            config: Configuration for infrastructure components
            preset: Selected preset in the settings

        """
        flat_config = preset.value
        if flat_config == preset.SIMPLE:
            flat = True
        else:
            flat = False
        self._generate_components(path, config, flat)

    def _generate_components(self, infra_path: Path, infra_layer: dict, flat: bool = False) -> None:
        """Generate infrastructure components based on configuration.

        Args:
            infra_path: Path where to generate components
            infra_layer: Configuration for infrastructure components
            flat: Whether to use flat structure instead of nested

        """
        for component_type, components in infra_layer.items():
            if not components or not isinstance(components, list):
                continue

            component_dir = infra_path

            if not flat:
                component_dir = infra_path / component_type
                self.create_directory(component_dir)
                self.create_init_file(component_dir)
