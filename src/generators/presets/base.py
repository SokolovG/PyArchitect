from abc import ABC, abstractmethod
from logging import getLogger
from pathlib import Path

from src.generators.base import GeneratorUtilsMixin
from src.generators.layer_generator import LayerGenerator
from src.schemas import ConfigModel
from src.templates.engine import TemplateEngine

logger = getLogger(__name__)


class AbstractPresetGenerator(ABC):
    """Base class for preset-specific generators."""

    def __init__(
        self,
        config: ConfigModel,
    ) -> None:
        """Initialize the preset generator with layer generators and configuration.

        Args:
            config: Project configuration

        """
        self.config = config

    @abstractmethod
    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate project structure according to preset.

        Args:
            root_path: Root path where to generate the project
            config: Project configuration

        """


class BasePresetGenerator(AbstractPresetGenerator, GeneratorUtilsMixin):
    """Base class for all preset generators.

    Contains common functionality for creating generators and directories.
    """

    def __init__(self, config: ConfigModel, template_engine: TemplateEngine) -> None:
        """Initialize the base preset generator.

        Args:
            config: Project configuration
            template_engine: Template engine for rendering

        """
        super().__init__(config)
        self.template_engine = template_engine
        self.layer_generators: dict[str, LayerGenerator] = {}

    def _get_layer_generator(
        self,
        layer_name: str,
        root_name: str,
        group_components: bool,
        init_imports: bool,
    ) -> LayerGenerator:
        """Get or create a layer generator for the given layer.

        Args:
            layer_name: Layer name (domain, application, etc.)
            root_name: Root package name
            group_components: Whether to group components
            init_imports: Whether to generate imports

        Returns:
            Configured LayerGenerator instance

        """
        cache_key = f"{layer_name}_{root_name}_{group_components}_{init_imports}"
        logger.debug(f"cache_key - {cache_key}")
        if cache_key not in self.layer_generators:
            self.layer_generators[cache_key] = LayerGenerator(
                template_engine=self.template_engine,
                root_name=root_name,
                layer_name=layer_name,
                group_components=group_components,
                init_imports=init_imports,
            )
        logger.debug(f"layer_generator - {self.layer_generators[cache_key]}")
        return self.layer_generators[cache_key]

    def create_layer_dir(self, root_path: Path, layer_name: str) -> Path:
        """Create a directory for a layer.

        Args:
            root_path: Root directory path
            layer_name: Name of the layer

        Returns:
            Path to the created layer directory

        """
        layer_path = root_path / layer_name
        self.create_directory(layer_path)
        self.create_init_file(layer_path)
        return layer_path

    def create_component_dir(self, layer_path: Path, component_type: str) -> Path:
        """Create a directory for a component type.

        Args:
            layer_path: Layer directory path
            component_type: Type of component

        Returns:
            Path to the created component directory

        """
        component_dir = layer_path / component_type
        self.create_directory(component_dir)
        self.create_init_file(component_dir)
        return component_dir
