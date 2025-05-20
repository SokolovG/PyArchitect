from pathlib import Path
from typing import Any

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
        """Provide a default None value for a path."""
        return getattr(self, "_file_path", None)

    @provide(scope=Scope.APP)
    def get_config(self, parser: YamlParser, file_path: Path | None = None) -> ConfigModel:
        """Provide a validated ConfigModel loaded from YAML configuration."""
        return parser.load(file_path)

    def set_file_path(self, path: Path | None = None) -> None:
        """Provide a path if isn't None."""
        self._file_path = path

    @provide(scope=Scope.APP)
    def get_template_engine(self) -> TemplateEngine:
        """Provide a template engine instance for the app scope."""
        return TemplateEngine()

    def set_generator_mode(self, preview_mode: bool = False) -> bool:
        """Provide generation mode for the app scope."""
        return preview_mode

    @provide(scope=Scope.APP)
    def get_project_generator(
        self, config: ConfigModel, engine: TemplateEngine, get_generator_mode: bool
    ) -> ProjectGenerator:
        """Provide a ProjectGenerator instance with all dependencies injected."""
        return ProjectGenerator(config, engine, get_generator_mode)


class Container:
    def __init__(self):
        """F."""
        self.provider = MyProvider()
        self.di_container = make_container(self.provider)

    def get(self, dependency_type: Any):
        """F."""
        return self.di_container.get(dependency_type)


container = Container()
