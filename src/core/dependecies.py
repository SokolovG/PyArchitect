from dishka import Provider, Scope, make_async_container, provide

from src.core.parser import YamlParser
from src.generators import ProjectGenerator
from src.generators.layer_generators import (
    ApplicationGenerator,
    DomainGenerator,
    InfrastructureGenerator,
    InterfaceGenerator,
)
from src.schemas import ConfigModel


class MyProvider(Provider):
    @provide(scope=Scope.APP)
    def get_domain_gen(self) -> DomainGenerator:
        """F."""
        return DomainGenerator()

    @provide(scope=Scope.APP)
    def get_app_gen(self) -> ApplicationGenerator:
        """F."""
        return ApplicationGenerator()

    @provide(scope=Scope.APP)
    def get_infra_gen(self) -> InfrastructureGenerator:
        """F."""
        return InfrastructureGenerator()

    @provide(scope=Scope.APP)
    def get_interface_gen(self) -> InterfaceGenerator:
        """F."""
        return InterfaceGenerator()

    @provide(scope=Scope.APP)
    def get_parser(self) -> YamlParser:
        """F."""
        return YamlParser()

    @provide(scope=Scope.APP)
    def get_config(self, parser: YamlParser) -> ConfigModel:
        """F."""
        return parser.load()

    @provide(scope=Scope.APP)
    def get_project_generator(
        self,
        config: ConfigModel,
        domain_generator: DomainGenerator,
        app_generator: ApplicationGenerator,
        infra_generator: InfrastructureGenerator,
        interface_generator: InterfaceGenerator,
    ) -> ProjectGenerator:
        """F."""
        return ProjectGenerator(
            config,
            domain_generator,
            app_generator,
            infra_generator,
            interface_generator,
        )


container = make_async_container(MyProvider())
