from abc import ABC, abstractmethod
from pathlib import Path

from src.templates.engine import TemplateEngine

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


class GeneratorUtilsMixin:
    """Base class for all code generators.

    This class provides common utility methods used by all specific
    generator implementations.
    """

    def __init__(self, template_engine: TemplateEngine) -> None:
        """Initialize the base generator with a template engine.

        Args:
            template_engine: Engine instance for rendering templates

        """
        self.template_engine = template_engine

    def create_directory(self, path: Path) -> Path:
        """Create a directory if it doesn't exist.

        Args:
            path: Path to create

        Returns:
            Created path object

        """
        path.mkdir(exist_ok=True, parents=True)
        return path

    def create_init_file(self, path: Path) -> None:
        """Create an empty __init__.py file in the specified directory.

        Args:
            path: Directory where to create the file

        """
        init_file = path / "__init__.py"
        if not init_file.exists():
            init_file.touch()

    def get_init_path(self, path: Path) -> Path:
        """Return a path to init file.

        Args:
            path: Directory where to create the file

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
        with open(path, "w") as file:
            file.write(content)


class ImportPathGenerator(ABC):
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
        """F."""


class StandardImportPathGenerator(ImportPathGenerator):
    def generate_import_path(
        self,
        root_name: str,
        layer_name: str,
        context_name: str,
        component_type: str,
        module_name: str,
        component_name: str,
    ) -> str:
        """F."""
        if context_name:
            return (
                f"from {root_name}.{layer_name}.{context_name}."
                f"{component_type}.{module_name} import {component_name}"
            )
        return f"from {root_name}.{layer_name}.{component_type}.{module_name} import {component_name}"


class AdvancedImportPathGenerator(ImportPathGenerator):
    def generate_import_path(
        self,
        root_name: str,
        layer_name: str,
        context_name: str,
        component_type: str,
        module_name: str,
        component_name: str,
    ) -> str:
        """F."""
        if context_name:
            import_string = (
                f"from {root_name}.{context_name}.{layer_name}."
                f"{component_type}.{module_name} import {component_name}"
            )
            return import_string

        import_string = f"from {root_name}.{layer_name}.{component_type}.{module_name} import {component_name}"
        return import_string
