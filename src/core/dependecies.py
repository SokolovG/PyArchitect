from dishka import Provider, Scope, make_async_container, provide

from src.core.parser import YamlParser
from src.generators import ProjectGenerator
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
    def get_parser(self) -> YamlParser:
        """Provide a YamlParser instance for the application scope."""
        return YamlParser()

    @provide(scope=Scope.APP)
    def get_config(self, parser: YamlParser) -> ConfigModel:
        """Provide a validated ConfigModel loaded from YAML configuration."""
        return parser.load()

    @provide(scope=Scope.APP)
    def get_template_engine(self) -> TemplateEngine:
        """Provide a template engine instance for the application scope."""
        return TemplateEngine()

    @provide(scope=Scope.APP)
    def get_project_generator(
        self, config: ConfigModel, engine: TemplateEngine
    ) -> ProjectGenerator:
        """Provide a ProjectGenerator instance with all dependencies injected."""
        return ProjectGenerator(config, engine)


container = make_async_container(MyProvider())
