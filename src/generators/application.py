from pathlib import Path

from src.schemas.config_schema import ApplicationLayer


class ApplicationGenerator:
    """Generator for the application layer components.

    This class is responsible for generating all components of the application layer
    based on the configuration.
    """

    def generate_application_components(
        self, application_path: Path, domain_layer: ApplicationLayer
    ) -> None:
        """Generate all application layer components.

        Args:
            application_path: Path where to generate components
            domain_layer: Configuration for application components

        """
        pass
