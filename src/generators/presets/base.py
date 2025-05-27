from abc import ABC, abstractmethod
from logging import getLogger
from pathlib import Path

from src.core.utils import GenerationContext
from src.generators.layer_generator import LayerGenerator
from src.generators.utils import (
    FileOperations,
    ImportPathGenerator,
)
from src.preview.collector import PreviewCollector
from src.schemas import ConfigModel

logger = getLogger(__name__)


class AbstractPresetGenerator(ABC):
    """Base class for preset-specific generators."""

    def __init__(
        self,
        context: GenerationContext,
    ) -> None:
        """Initialize the preset generator with layer generators and configuration.

        Args:
            context: Project configuration

        """
        self.config = context.config

    @abstractmethod
    def generate(self, root_path: Path, config: ConfigModel, preview_mode: bool) -> None:
        """Generate project structure according to preset.

        Args:
            root_path: Root path where to generate the project
            config: Project configuration
            preview_mode: Special mode for dry generation

        """


class BasePresetGenerator(AbstractPresetGenerator):
    """Base class for all preset generators.

    Contains common capability for creating generators and directories.
    """

    def __init__(self, context: GenerationContext) -> None:
        """Initialize the base preset generator.

        Args:
            context: Project configuration

        """
        super().__init__(context)
        self.context = context
        self.template_engine = context.engine
        self.layer_generators: dict[str, LayerGenerator] = {}
        self.file_ops = FileOperations(context.engine, context.preview_collector)

    def _get_layer_generator(
        self,
        layer_name: str,
        root_name: str,
        group_components: bool,
        init_imports: bool,
        context_name: str | None = None,
        import_path_generator: ImportPathGenerator | None = None,
        preview_collector: PreviewCollector | None = None,
    ) -> LayerGenerator:
        """Get or create a layer generator for the given layer.

        Args:
            layer_name: Layer name
            root_name: Root package name
            group_components: Whether to group components
            init_imports: Whether to generate imports
            context_name: Name context
            import_path_generator: What kind of imports
            preview_collector: Preview collector for dry generation

        Returns:
            Configured LayerGenerator instance

        """
        cache_key = f"{layer_name}_{root_name}_{group_components}_{init_imports}"
        logger.debug(f"cache_key - {cache_key}")
        if cache_key not in self.layer_generators:
            self.layer_generators[cache_key] = LayerGenerator(
                template_engine=self.template_engine,
                root_name=root_name,
                preview_collector=preview_collector,
                layer_name=layer_name,
                group_components=group_components,
                init_imports=init_imports,
                context_name=context_name,
                import_path_generator=import_path_generator,
            )
        logger.debug(f"layer_generator - {self.layer_generators[cache_key].layer_name}")
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
        self.file_ops.create_directory(layer_path)
        self.file_ops.create_init_file(layer_path)
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
        self.file_ops.create_directory(component_dir)
        self.file_ops.create_init_file(component_dir)
        return component_dir
