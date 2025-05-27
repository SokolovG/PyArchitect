from abc import ABC, abstractmethod
from pathlib import Path

from src.core.template_engine import TemplateEngine
from src.preview.collector import PreviewCollector

single_form_words = {
    "entities": "entity",
    "repositories": "repository",
    "services": "service",
    "value_objects": "value_object",
    "aggregates": "aggregate",
    "factories": "factory",
    "domain_events": "domain_event",
    "commands": "command",
    "queries": "query",
    "exceptions": "exception",
    "controllers": "controller",
    "dto": "dto",
    "models": "model",
    "adapters": "adapter",
    "handlers": "handler",
    "validators": "validator",
    "specifications": "specification",
}


class FileOperations:
    """Base class for all code generators.

    This class provides common utility methods used by all specific
    generator implementations for file system operations and template rendering.

    Attributes:
        template_engine: Template engine instance for rendering code templates
        preview_collector: Optional collector for dry generation

    """

    def __init__(
        self,
        template_engine: TemplateEngine,
        preview_collector: PreviewCollector | None = None,
    ) -> None:
        """Initialize the base generator with a template engine.

        Args:
            template_engine: Engine instance for rendering templates
            preview_collector: Collector for dry generation

        """
        self.template_engine = template_engine
        self.preview_collector = preview_collector

    def create_directory(self, path: Path) -> Path:
        """Create a directory if it doesn't exist.

        Args:
            path: Path to create

        Returns:
            Created path object

        """
        if self.preview_collector:
            self.preview_collector.add_directory(path)
        else:
            path.mkdir(exist_ok=True, parents=True)
        return path

    def create_init_file(self, path: Path) -> None:
        """Create an empty __init__.py file in the specified directory.

        Args:
            path: Directory where to create the file

        """
        init_file = path / "__init__.py"
        if self.preview_collector:
            self.preview_collector.add_init_file(init_file)
        else:
            if not init_file.exists():
                init_file.touch()

    def get_init_path(self, path: Path) -> Path:
        """Return a path to init file.

        Args:
            path: Directory where the init file should be located

        Returns:
            Path to the init file

        """
        init_file = path / "__init__.py"
        return init_file

    def write_file(self, path: Path, content: str) -> None:
        """Write content to a file.

        Args:
            path: Path where to write the file
            content: Content to write to the file

        """
        if self.preview_collector:
            self.preview_collector.add_file(path)
        else:
            with open(path, "w") as file:
                file.write(content)


class ImportPathGenerator(ABC):
    """Abstract base class for generating Python import statements.

    Defines the interface for generating import paths based on project
    structure and component information.
    """

    @abstractmethod
    def generate_import_path(
        self,
        root_name: str,
        layer_name: str,
        context_name: str,
        component_type: str,
        module_name: str,
        component_name: str,
    ) -> str:
        """Generate an import statement for a component.

        Args:
            root_name: Root package name
            layer_name: Architecture layer name
            context_name: Business context name
            component_type: Type of component
            module_name: Name of the module file
            component_name: Name of the component to import

        Returns:
            Complete import statement string

        """


class StandardImportPathGenerator(ImportPathGenerator):
    """Standard implementation of import path generator.

    Generates import paths following the standard project structure:
    root.layer.context.component_type.module or root.layer.component_type.module
    """

    def generate_import_path(
        self,
        root_name: str,
        layer_name: str,
        context_name: str,
        component_type: str,
        module_name: str,
        component_name: str,
    ) -> str:
        """Generate a standard import path.

        Args:
            root_name: Root package name
            layer_name: Architecture layer name
            context_name: Business context name
            component_type: Type of component
            module_name: Name of the module file
            component_name: Name of the component to import

        Returns:
            Complete import statement string

        """
        if context_name:
            return (
                f"from {root_name}.{layer_name}.{context_name}."
                f"{component_type}.{module_name} import {component_name}"
            )
        return (
            f"from {root_name}.{layer_name}.{component_type}.{module_name} import {component_name}"  # noqa
        )


class AdvancedImportPathGenerator(ImportPathGenerator):
    """Advanced implementation of import path generator.

    Generates import paths with context-first structure:
    root.context.layer.component_type.module or root.layer.component_type.module
    """

    def generate_import_path(
        self,
        root_name: str,
        layer_name: str,
        context_name: str,
        component_type: str,
        module_name: str,
        component_name: str,
    ) -> str:
        """Generate an advanced import path with context-first structure.

        Creates import statements following the pattern:
        - With context: from root.context.layer.component_type.module import component
        - Without context: from root.layer.component_type.module import component

        Args:
            root_name: Root package name
            layer_name: Architecture layer name
            context_name: Business context name
            component_type: Type of component
            module_name: Name of the module file
            component_name: Name of the component to import

        Returns:
            Complete import statement string

        """
        if context_name:
            import_string = (
                f"from {root_name}.{context_name}.{layer_name}."
                f"{component_type}."
                f"{module_name} import {component_name}"
            )
            return import_string

        import_string = (
            f"from {root_name}.{layer_name}.{component_type}.{module_name} import {component_name}"  # noqa
        )
        return import_string
