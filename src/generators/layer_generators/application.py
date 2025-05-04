from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import ApplicationLayerConfig, PresetType


class ApplicationGenerator(BaseGenerator, AbstractLayerGenerator[ApplicationLayerConfig]):
    """Generator for the application layer components.

    This class is responsible for generating all components of the application layer
    based on the configuration.
    """

    def generate_components(
        self, path: Path, config: ApplicationLayerConfig, preset: PresetType
    ) -> None:
        """Generate all application layer components.

        Args:
            path: Path where to generate components
            config: Configuration for application components
            preset: Selected preset in the settings

        """
        flat = False
        self._generate_components(path, config, flat)

    def _generate_components(
        self, app_path: Path, app_layer: ApplicationLayerConfig, flat: bool = False
    ) -> None:
        """Generate application components based on configuration.

        Args:
            app_path: Path where to generate components
            app_layer: Configuration for application components
            flat: Whether to use flat structure instead of nested

        """
