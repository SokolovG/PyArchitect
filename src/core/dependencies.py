from pathlib import Path

from dishka import Provider, Scope, make_container, provide

from src.core.parser import YamlParser
from src.core.template_engine import TemplateEngine
from src.generators import ProjectGenerator
from src.schemas import ConfigModel


class MyProvider(Provider):
    """Dependency provider for project generators and configuration.

    This provider registers all generators and configuration objects
    for dependency injection using the Dishka library.
    """

    @provide(scope=Scope.APP)
    def get_parser(self) -> YamlParser:
        """Provide a YamlParser instance for the app scope."""
        return YamlParser()

    @provide(scope=Scope.APP)
    def get_default_file_path(self) -> Path | None:
        """Provide a default None value for file path."""
        return None

    @provide(scope=Scope.APP)
    def get_config(self, parser: YamlParser, file_path: Path | None = None) -> ConfigModel:
        """Provide a validated ConfigModel loaded from YAML configuration."""
        return parser.load(file_path)

    @provide(scope=Scope.APP)
    def get_template_engine(self) -> TemplateEngine:
        """Provide a template engine instance for the app scope."""
        return TemplateEngine()

    @provide(scope=Scope.APP)
    def get_project_generator(
        self, config: ConfigModel, engine: TemplateEngine
    ) -> ProjectGenerator:
        """Provide a ProjectGenerator instance with all dependencies injected."""
        return ProjectGenerator(config, engine)


container = make_container(MyProvider())
