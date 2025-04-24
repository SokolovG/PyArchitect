from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from pathlib import Path

    from src.parser import YamlParser

T = TypeVar("T")


class ProjectGenerator:
    def __init__(self, parser: YamlParser) -> None:
        """F."""
        self.parser = parser
        self.config = parser.load()

    def generate(self, output_path: str | None = None) -> None:
        """Generate the project structure based on the configuration.

        Args:
            output_path: Optional path where to generate the project.
            If not provided, use current directory.

        """

    def _create_file_from_template(
        self, template_name: str, target_path: Path, context: dict
    ) -> None:
        """Create a file from a template.

        Args:
            template_name: Name of the template to use
            target_path: Path where to create the file
            context: Context variables for the template

        """

    def _create_bounded_context(self, context: str, base_path: Path) -> None:
        """Create structure for a single bounded context."""

    def _create_project_root(self, path: str) -> None:
        """Create the root project directory."""

    def _create_domain_layer(self, domain_config: T, context_path: Path) -> None:
        """Create domain layer structure for a bounded context."""

    def _create_application_layer(self, application_config: T, context_path: Path) -> None:
        """Create application layer structure for a bounded context."""

    def _create_infrastructure_layer(self, infrastructure_config: T, context_path: Path) -> None:
        """Create infrastructure layer structure for a bounded context."""

    def _create_interfaces_layer(self, interface_config: T, context_path: Path) -> None:
        """Create interface layer structure for a bounded context."""
