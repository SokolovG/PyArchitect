from pathlib import Path

from src.generators.base import BaseGenerator
from src.schemas.config_schema import InfrastructureLayer


class InfrastructureGenerator(BaseGenerator):
    """Generator for the domain layer components.

    This class is responsible for generating all components of the domain layer
    based on the configuration.
    """

    def generate_infrastructure_components(
        self, infra_path: Path, domain_layer: InfrastructureLayer
    ) -> None:
        """Generate all infrastructure layer components.

        Args:
            infra_path: Path where to generate components
            domain_layer: Configuration for infrastructure components

        """
        pass
