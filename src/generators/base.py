from pathlib import Path

from src.generators.layer_generators import (
    ApplicationGenerator,
    DomainGenerator,
    InfrastructureGenerator,
    InterfaceGenerator,
)
from src.schemas import ConfigModel


class BaseGenerator:
    """Base class for all code generators.

    This class provides common utility methods used by all specific
    generator implementations.
    """

    def create_directory(self, path: Path) -> Path:
        """Create a directory if it doesn't exist.

        Args:
            path: Path to create

        Returns:
            Created path object

        """
        path.mkdir(exist_ok=True, parents=True)
        return path

    def create_init_file(self, path: Path) -> Path:
        """Create an empty __init__.py file in the specified directory.

        Args:
            path: Directory where to create the file

        Returns:
            Path to the created file

        """
        init_file = path / "__init__.py"
        if not init_file.exists():
            init_file.touch()
        return init_file

    def ensure_list(self, value: str | list[str]) -> list[str]:
        """Convert a value to a list if it's a string or return as is if it's already a list.

        Args:
            value: String or list of strings

        Returns:
            List of strings

        """
        if isinstance(value, str):
            return [value]
        return value if value is not None else []


class PresetGenerator:
    """Base class for preset-specific generators."""

    def __init__(
        self,
        domain_gen: DomainGenerator,
        app_gen: ApplicationGenerator,
        infra_gen: InfrastructureGenerator,
        interface_gen: InterfaceGenerator,
        config: ConfigModel,
    ) -> None:
        """Initialize the preset generator with layer generators and configuration.

        Args:
            domain_gen: Domain layer generator
            app_gen: Application layer generator
            infra_gen: Infrastructure layer generator
            interface_gen: Interface layer generator
            config: Project configuration

        """
        self.domain_generator = domain_gen
        self.app_generator = app_gen
        self.infra_generator = infra_gen
        self.interface_generator = interface_gen
        self.config = config

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate project structure according to preset.

        Args:
            root_path: Root path where to generate the project
            config: Project configuration

        """
        raise NotImplementedError("Subclasses must implement generate method")
