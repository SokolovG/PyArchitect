from logging import getLogger
from pathlib import Path

from icecream import ic

from src.core import single_form_words
from src.generators.base import BaseGenerator
from src.generators.utils import camel_to_snake
from src.templates.engine import TemplateEngine

logger = getLogger(__name__)


class LayerGenerator(BaseGenerator):
    """Base generator for any architectural layer.

    This class handles the generation of components within a specific
    architectural layer (domain, application, etc.).
    """

    def __init__(
        self,
        template_engine: TemplateEngine,
        root_name: str,
        layer_name: str = "",
        group_components: bool = True,
        generate_all_exports: bool = False,
    ) -> None:
        """Initialize layer generator.

        Args:
            template_engine: Template engine instance
            root_name: Root name
            layer_name: Optional layer name for template lookup
            group_components: single/group strategy
            generate_all_exports: create __all__ list in __init__.py

        """
        super().__init__(template_engine)
        self.template_dir = template_engine.get_template_dir(layer_name)
        self.group_components = group_components
        self.generate_all_exports = generate_all_exports
        self.root_name = root_name

    def generate_components(self, path: Path, layer_config: dict[str, list[str] | str]) -> None:
        """Generate all components for a layer.

        Args:
            path: Path to generate
            layer_config: Configure a layer as a dictionary

        """
        for component_type, components in layer_config.items():
            if not components:
                continue

            component_dir = path / component_type
            self.create_directory(component_dir)
            init_path = self.create_init_file(component_dir)

            if isinstance(components, str):
                components = [comp.strip() for comp in components.split(",")]

            if self.generate_all_exports:
                singular_type = single_form_words.get(component_type, component_type.rstrip("s"))
                template_path = "init.py.jinja"
                content = self.template_engine.render(
                    template_path,
                    {
                        "components": components,
                        "component_type": component_type,
                        "singular_type": singular_type,
                        "module_path": self.root_name,
                    },
                )
                ic(init_path)
                self.write_file(init_path, content)

            if self.group_components:
                self._generate_grouped_components(component_dir, component_type, components)
            else:
                for component_name in components:
                    self._generate_component(component_dir, component_type, component_name)

    def _generate_component(self, path: Path, component_type: str, component_name: str) -> None:
        """Generate of a single component.

        Args:
            path: The path where to generate
            component_type: Component type (entities, value_objects, etc.)
            component_name: Component name (User, Product, etc.)

        """
        singular_type = single_form_words.get(component_type, component_type.rstrip("s"))
        snake_name = camel_to_snake(component_name)

        if snake_name.endswith(f"_{singular_type}"):
            file_name = f"{snake_name}.py"
        else:
            file_name = f"{snake_name}_{singular_type}.py"

        file_path = path / file_name

        template_path = "base_template.py.jinja"
        content = self.template_engine.render(
            template_path,
            {
                "name": component_name,
                "type": singular_type,
            },
        )

        self.write_file(file_path, content)

    def _generate_grouped_components(
        self, path: Path, component_type: str, components: list[str]
    ) -> None:
        """Generate all components in a single file.

        Args:
            path: The path where to generate
            component_type: Component type (entities, value_objects, etc.)
            components: List of component names

        """
        file_name = f"{component_type}.py"
        file_path = path / file_name

        template_path = "multi_component_template.py.jinja"
        if not self.template_engine.template_exists(template_path):
            template_path = "base_template.py.jinja"

        content = self.template_engine.render(
            template_path,
            {
                "component_type": component_type,
                "components": components,
                "single_form": single_form_words.get(component_type, component_type.rstrip("s")),
            },
        )

        self.write_file(file_path, content)
