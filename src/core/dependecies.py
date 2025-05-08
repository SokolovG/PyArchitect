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
from src.templates.engine import TemplateEngine


class MyProvider(Provider):
    """Dependency provider for project generators and configuration.

    This provider registers all generators and configuration objects
    for dependency injection using the Dishka library.
    """

    @provide(scope=Scope.APP)
    def get_engine(self) -> TemplateEngine:
        """F."""
        return TemplateEngine()

    @provide(scope=Scope.APP)
    def get_domain_gen(self, template_engine: TemplateEngine) -> DomainGenerator:
        """Provide a DomainGenerator instance for the application scope."""
        return DomainGenerator(template_engine)

    @provide(scope=Scope.APP)
    def get_app_gen(self, template_engine: TemplateEngine) -> ApplicationGenerator:
        """Provide an ApplicationGenerator instance for the application scope."""
        return ApplicationGenerator(template_engine)

    @provide(scope=Scope.APP)
    def get_infra_gen(self, template_engine: TemplateEngine) -> InfrastructureGenerator:
        """Provide an InfrastructureGenerator instance for the application scope."""
        return InfrastructureGenerator(template_engine)

    @provide(scope=Scope.APP)
    def get_interface_gen(self, template_engine: TemplateEngine) -> InterfaceGenerator:
        """Provide an InterfaceGenerator instance for the application scope."""
        return InterfaceGenerator(template_engine)

    @provide(scope=Scope.APP)
    def get_parser(self) -> YamlParser:
        """Provide a YamlParser instance for the application scope."""
        return YamlParser()

    @provide(scope=Scope.APP)
    def get_config(self, parser: YamlParser) -> ConfigModel:
        """Provide a validated ConfigModel loaded from YAML configuration."""
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
        """Provide a ProjectGenerator instance with all dependencies injected."""
        return ProjectGenerator(
            config,
            domain_generator,
            app_generator,
            infra_generator,
            interface_generator,
        )


container = make_async_container(MyProvider())
