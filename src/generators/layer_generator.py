from logging import getLogger
from pathlib import Path

from src.core.template_engine import TemplateEngine
from src.generators.utils import (
    FileOperations,
    ImportPathGenerator,
    StandardImportPathGenerator,
    single_form_words,
)
from src.preview.collector import PreviewCollector

logger = getLogger(__name__)


class LayerGenerator:
    """Generator for components within a specific architectural layer.

    This class is responsible for generating Python files for specific components
    within existing directories.
    """

    def __init__(
        self,
        template_engine: TemplateEngine,
        root_name: str,
        layer_name: str = "",
        group_components: bool = True,
        init_imports: bool = False,
        context_name: str | None = None,
        import_path_generator: ImportPathGenerator | None = None,
        preview_collector: PreviewCollector | None = None,
    ) -> None:
        """Initialize layer generator.

        Args:
            template_engine: Template engine instance
            root_name: Root package name for imports
            layer_name: Layer name for namespace/imports
            group_components: Whether to group components in single files
            init_imports: Whether to generate imports in __init__.py
            context_name: Name of context
            import_path_generator: What kind imports
            preview_collector: Preview collector for dry generation

        """
        self.file_ops = FileOperations(template_engine, preview_collector)
        self.template_engine = template_engine
        self.preview_collector = preview_collector
        self.layer_name = layer_name
        self.template_dir = template_engine.get_template_dir(self.layer_name)
        self.group_components = group_components
        self.init_imports = init_imports
        self.root_name = root_name
        self.context_name = context_name if context_name else ""
        self.import_path_generator = import_path_generator or StandardImportPathGenerator()

    def generate_component(self, path: Path, component_type: str, component_name: str) -> str:
        """Generate a single component file.

        Args:
            path: Path where to create the file
            component_type: Type of component
            component_name: Name of the component

        Returns:
            Name of the generated module

        """
        singular_type = single_form_words.get(component_type, component_type.rstrip("s"))
        snake_name = self.template_engine.camel_to_snake(component_name)

        suffix = singular_type.lower()
        if snake_name.lower().endswith(f"_{suffix}"):
            file_name = f"{snake_name}.py"
            module_name = snake_name
        else:
            file_name = f"{snake_name}_{singular_type.lower()}.py"
            module_name = f"{snake_name}_{singular_type.lower()}"

        file_path = path / file_name
        if self.preview_collector:
            self.preview_collector.add_file(file_path)
        else:
            template_path = "base_template.py.jinja"
            content = self.template_engine.render(
                template_path,
                {
                    "name": component_name,
                    "type": singular_type,
                },
            )

            self.file_ops.write_file(file_path, content)
        return module_name

    def generate_components(  # noqa: D417
        self, component_dir: Path, component_type: str, components: list[str] | str
    ) -> dict[str, str]:
        """Generate all components of a specific type.

        This method handles the generation of component files based on the provided configuration.
        It supports both grouped and individual component generation modes,
        and can handle
        both string and list inputs for components.

        Args:
            component_dir: Directory where to create components
            component_type: Type of components
            components:
            List of component names or comma-separated string of component names.
                      Empty lists will still create the directory structure.

        Returns:
            Dictionary mapping component names to their module names.

        """
        if components is None:
            return {}

        if isinstance(components, str):
            components = [comp.strip() for comp in components.split(",")]

        generated_modules = {}

        if self.group_components:
            self._generate_grouped_components(component_dir, component_type, components)
            for component in components:
                generated_modules[component] = component_type
        else:
            for component_name in components:
                module_name = self.generate_component(component_dir, component_type, component_name)
                generated_modules[component_name] = module_name

        if self.init_imports and components:
            init_path = self.file_ops.get_init_path(component_dir)
            self._generate_init_imports(
                init_path=init_path,
                component_type=component_type,
                components=components,
                generated_modules=generated_modules,
            )

        return generated_modules

    def _generate_grouped_components(  # noqa: D417
        self, path: Path, component_type: str, components: list[str]
    ) -> None:
        """Generate all components in a single file.

        This private method is used when group_components are True.
        It creates a single
        Python file containing all components of the specified type.
        Each component
        is generated as a class with basic structure and docstring.

        Args:
            path: The path where to generate the file
            component_type:
            Component type
            components: List of component names to generate

        Note:
            This method is called internally by generate_components when
            self.group_components is True.

        """
        file_name = f"{component_type}.py"
        file_path = path / file_name
        if self.preview_collector:
            self.preview_collector.add_file(file_path)
            return None

        template_path = "multi_component_template.py.jinja"

        content = self.template_engine.render(
            template_path,
            {
                "component_type": component_type,
                "components": components,
                "single_form": single_form_words.get(component_type, component_type.rstrip("s")),
            },
        )

        self.file_ops.write_file(file_path, content)
        return None

    def _generate_init_imports(
        self,
        init_path: Path,
        component_type: str,
        components: list[str],
        generated_modules: dict[str, str],
    ) -> None:
        """Generate __init__.py with import for components.

        This private method generates an __init__.py file that exports all components
        of the specified type.
        It creates import statements and __all__ list for
        proper module exports.

        Args:
            init_path: Path to the __init__.py file
            component_type: Type of components
            components: List of component names to export
            generated_modules: Dictionary mapping component names to their module names

        """
        imports = []
        for component in components:
            module_name = generated_modules[component]
            import_path = self.import_path_generator.generate_import_path(
                self.root_name,
                self.layer_name,
                self.context_name,
                component_type,
                module_name,
                component,
            )
            imports.append(import_path)
        template_path = "init.py.jinja"
        content = self.template_engine.render(
            template_path,
            {
                "imports": imports,
                "components": components,
            },
        )

        self.file_ops.write_file(init_path, content)
