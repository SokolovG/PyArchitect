from pathlib import Path

from src.generators.layer_generators import (
    ApplicationGenerator,
    DomainGenerator,
    InfrastructureGenerator,
    InterfaceGenerator,
)
from src.schemas import ConfigModel


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
