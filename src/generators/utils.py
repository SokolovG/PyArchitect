from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas.config_schema import ConfigModel


@dataclass
class LayerPaths:
    """Represents paths to all architecture layers.

    Uses neutral layer numbering but provides convenient properties
    for accessing specific layers.
    """

    layer_1: Path  # domain
    layer_2: Path  # application
    layer_3: Path  # infrastructure
    layer_4: Path  # interface

    @property
    def domain(self) -> Path:
        """Get the path to the domain layer.

        Returns:
            Path to the domain layer

        """
        return self.layer_1

    @property
    def application(self) -> Path:
        """Get the path to the application layer.

        Returns:
            Path to the application layer

        """
        return self.layer_2

    @property
    def infrastructure(self) -> Path:
        """Get the path to the infrastructure layer.

        Returns:
            Path to the infrastructure layer

        """
        return self.layer_3

    @property
    def interface(self) -> Path:
        """Get the path to the interface layer.

        Returns:
            Path to the interface layer

        """
        return self.layer_4

    @classmethod
    def from_config(cls, root_path: Path, config: ConfigModel) -> "LayerPaths":
        """Create a LayerPaths instance from configuration.

        Args:
            root_path: Root path of the project
            config: Configuration object

        Returns:
            LayerPaths instance with paths matching the configuration

        """
        return cls(
            layer_1=root_path / config.settings.domain_layer,
            layer_2=root_path / config.settings.application_layer,
            layer_3=root_path / config.settings.infrastructure_layer,
            layer_4=root_path / config.settings.interface_layer,
        )
