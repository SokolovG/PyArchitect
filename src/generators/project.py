from pathlib import Path

from src.core.parser import YamlParser
from src.generators.application import ApplicationGenerator
from src.generators.base import BaseGenerator
from src.generators.domain import DomainGenerator
from src.generators.infrastructure import InfrastructureGenerator
from src.generators.interface import InterfaceGenerator
from src.generators.utils import LayerPaths


class ProjectGenerator(BaseGenerator):
    """Main project generator.

    This class coordinates the generation of all project components
    and layers based on the configuration file.

    Attributes:
        parser: YAML configuration parser
        config: Parsed configuration
        domain_generator: Generator for domain layer components

    """

    def __init__(self, path: Path) -> None:
        """Initialize the project generator.

        Args:
            path: Path to the configuration file

        """
        super().__init__()
        self.parser = YamlParser(path)
        self.config = self.parser.load()
        self.domain_generator = DomainGenerator()
        self.app_generator = ApplicationGenerator()
        self.infra_generator = InfrastructureGenerator()
        self.interface_generator = InterfaceGenerator()

    def generate(self) -> None:
        """Generate the project structure based on the configuration.

        This method creates the entire project structure with all layers
        and their components as specified in the configuration.
        """
        print("Starting project generation...")
        project_root = Path.cwd()
        root_name = self.config.settings.naming.root_name
        root_path = project_root / root_name

        self.create_directory(root_path)
        self.create_init_file(root_path)

        layer_paths = LayerPaths.from_config(root_path, self.config)
        for path in [
            layer_paths.layer_1,
            layer_paths.layer_2,
            layer_paths.layer_3,
            layer_paths.layer_4,
        ]:
            self.create_directory(path)
            self.create_init_file(path)

        if self.config.settings.structure.use_contexts:
            self._generate_with_contexts(layer_paths)
        else:
            self._generate_without_contexts(layer_paths)

    def _generate_with_contexts(self, layer_paths: LayerPaths) -> None:
        """Generate project structure with bounded contexts.

        This method creates separate subdirectories for each bounded context
        in each layer and populates them with components.

        Args:
            layer_paths: Base path for domain layer

        """
        for context in self.config.contexts:
            # Создаем контекстные директории в каждом слое
            context_domain_path = layer_paths.domain / context.name
            context_app_path = layer_paths.application / context.name
            context_infra_path = layer_paths.infrastructure / context.name
            context_interface_path = layer_paths.interface / context.name

            context_paths = [
                context_domain_path,
                context_app_path,
                context_infra_path,
                context_interface_path,
            ]

            for path in context_paths:
                self.create_directory(path)
                self.create_init_file(path)

            if context.domain:
                self.domain_generator.generate_domain_components(
                    context_domain_path,
                    context.domain,
                    flat=self.config.settings.structure.flat_domain,
                )

            self.app_generator.generate_application_components(
                context_app_path, context.application
            )
            self.infra_generator.generate_infrastructure_components(
                context_infra_path, context.infrastructure
            )
            self.interface_generator.generate_interface_components(
                context_interface_path, context.interface
            )

    def _generate_without_contexts(self, layer_paths: LayerPaths) -> None:
        """Generate project structure without bounded contexts.

        This method creates components directly in each layer without
        subdividing them by bounded contexts.

        Args:
            layer_paths: Path for domain layer

        """
        if self.config.contexts:  # Проверяем, что список контекстов не пуст
            context = self.config.contexts[0]

            # Генерируем компоненты доменного слоя
            if context.domain:
                self.domain_generator.generate_domain_components(
                    layer_paths.domain,
                    context.domain,
                    flat=self.config.settings.structure.flat_domain,
                )

            # Здесь можно добавить генерацию для других слоев
            # self._generate_application_components(application_path, context.application)
            # self._generate_infrastructure_components(infrastructure_path, context.infrastructure)
            # self._generate_interface_components(interface_path, context.interface)
