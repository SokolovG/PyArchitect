from pathlib import Path
from typing import TypeVar

from dishka import Provider, Scope, make_container, provide

from src.core.parser import YamlParser
from src.core.template_engine import TemplateEngine
from src.generators import ProjectGenerator
from src.schemas import ConfigModel

T = TypeVar("T")


class MyProvider(Provider):
    """Dependency provider for project generators and configuration.

    This provider registers all generators and configuration objects
    for dependency injection using the Dishka library.
    """

    def __init__(self) -> None:
        """Initialize provider obj.

        Attrs:
            _file_path: Path to file config
            _preview_mode: Special mode for dry generation.
            False by default
        """
        super().__init__()
        self._file_path: Path | None = None
        self._preview_mode: bool = False

    @provide(scope=Scope.APP)
    def get_parser(self) -> YamlParser:
        """Provide a YamlParser instance for the app scope."""
        return YamlParser()

    @provide(scope=Scope.APP)
    def get_file_path(self) -> Path | None:
        """Provide the configured path."""
        return self._file_path

    @provide(scope=Scope.APP)
    def get_config(self, parser: YamlParser, file_path: Path | None) -> ConfigModel:
        """Provide a validated ConfigModel loaded from YAML configuration."""
        return parser.load(file_path)

    def set_file_path(self, path: Path | None = None) -> None:
        """Set the path for configuration loading."""
        self._file_path = path

    @provide(scope=Scope.APP)
    def get_template_engine(self) -> TemplateEngine:
        """Provide a template engine instance for the app scope."""
        return TemplateEngine()

    @provide(scope=Scope.APP)
    def get_preview_mode(self) -> bool:
        """Provide generation mode for the app scope."""
        return self._preview_mode

    def set_preview_mode(self, preview_mode: bool = False) -> None:
        """Set preview mode value."""
        self._preview_mode = preview_mode

    @provide(scope=Scope.APP)
    def get_project_generator(
        self, config: ConfigModel, engine: TemplateEngine, preview_mode: bool
    ) -> ProjectGenerator:
        """Provide a ProjectGenerator instance with all dependencies injected."""
        return ProjectGenerator(config, engine, preview_mode)


class Container:
    def __init__(self) -> None:
        """Initialize container with provider and DI container."""
        self.provider = MyProvider()
        self.di_container = make_container(self.provider)

    def get(self, dependency_type: T) -> T:
        """Get dependency from container."""
        obj: T = self.di_container.get(dependency_type)
        return obj


container = Container()
