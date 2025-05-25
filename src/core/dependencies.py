from pathlib import Path
from typing import TypeVar

from dishka import Provider, Scope, make_container, provide

from src.core.parser import YamlParser
from src.core.template_engine import TemplateEngine
from src.core.utils import GenerationContext
from src.generators import ProjectGenerator
from src.preview.collector import PreviewCollector
from src.schemas import ConfigModel


class MyProvider(Provider):
    """Dependency provider for project generators and configuration.

    This provider registers all generators and configuration objects
    for dependency injection using the Dishka library.
    """

    @provide(scope=Scope.APP, provides=YamlParser)
    def get_parser(self) -> YamlParser:
        """Provide a YamlParser instance for the app scope."""
        return YamlParser()

    @provide(scope=Scope.APP, provides=Path | None)
    def get_default_file_path(self) -> Path | None:
        """Provide a default None value for a path."""
        return getattr(self, "_file_path", None)

    @provide(scope=Scope.APP, provides=ConfigModel)
    def get_config(self, parser: YamlParser, file_path: Path | None = None) -> ConfigModel:
        """Provide a validated ConfigModel loaded from YAML configuration."""
        return parser.load(file_path)

    def set_file_path(self, path: Path | None = None) -> None:
        """Provide a path if isn't None."""
        self._file_path = path

    @provide(scope=Scope.APP, provides=TemplateEngine)
    def get_template_engine(self) -> TemplateEngine:
        """Provide a template engine instance for the app scope."""
        return TemplateEngine()

    @provide(scope=Scope.APP, provides=bool)
    def get_generator_mode(self) -> bool:
        """Provide generation mode for the app scope."""
        return getattr(self, "_preview_mode", False)

    def set_preview_mode(self, preview_mode: bool = False) -> None:
        """Set preview mode value."""
        self._preview_mode = preview_mode

    def set_render_format(self, render_format: str) -> None:
        """Set render format value."""
        self._render_format = render_format

    @provide(scope=Scope.APP, provides=str)
    def get_render_format(self) -> str:
        """Provide a render format for the app scope."""
        return getattr(self, "render_format", "tree")

    @provide(scope=Scope.APP, provides=PreviewCollector)
    def get_preview_collector(self) -> PreviewCollector:
        """Provide preview collector for the app scope."""
        return PreviewCollector(render_format="tree")

    @provide(scope=Scope.APP, provides=ProjectGenerator)
    def get_project_generator(
        self,
        config: ConfigModel,
        engine: TemplateEngine,
        get_generator_mode: bool,
        preview_collector: PreviewCollector,
    ) -> ProjectGenerator:
        """Provide a ProjectGenerator instance with all dependencies injected."""
        return ProjectGenerator(
            GenerationContext(config, engine, preview_collector, get_generator_mode)
        )


T = TypeVar("T")


class Container:
    def __init__(self) -> None:
        """Initialize the dependency injection container with a provider."""
        self.provider = MyProvider()
        self.di_container = make_container(self.provider)

    def get(self, dependency_type: type[T]) -> T:
        """Get a dependency instance of the specified type from the container."""
        obj: T = self.di_container.get(dependency_type)
        return obj


container = Container()
