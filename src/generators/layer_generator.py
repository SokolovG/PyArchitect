from pathlib import Path

from src.core import camel_to_snake, single_form_words
from src.generators.base import BaseGenerator
from src.templates.engine import TemplateEngine


class LayerGenerator(BaseGenerator):
    """Базовый генератор для любого слоя."""

    def __init__(self, template_engine: TemplateEngine, layer_name: str = "") -> None:
        """Initialize layer generator.

        Args:
            template_engine: Template engine instance
            layer_name: Optional layer name for template lookup

        """
        super().__init__(template_engine)
        self.template_dir = template_engine.get_template_dir(layer_name)

    def generate_components(self, path: Path, layer_config: dict[str, list[str]]) -> None:
        """Генерация всех компонентов для слоя.

        Args:
            path: Путь, куда генерировать
            layer_config: Конфигурация слоя в виде словаря

        """
        for component_type, components in layer_config.items():
            print(f"First loop - {component_type} {components}")
            if not components:
                continue

            component_dir = path / component_type
            self.create_directory(component_dir)
            self.create_init_file(component_dir)

            if isinstance(components, str):
                components = [components]

            for component_name in components:
                print(f"Second loop - {component_dir} {component_type} {component_name}")
                self._generate_component(component_dir, component_type, component_name)

    def _generate_component(self, path: Path, component_type: str, component_name: str) -> None:
        """Генерация отдельного компонента.

        Args:
            path: Путь, куда генерировать
            component_type: Тип компонента (entities, value_objects и т.д.)
            component_name: Имя компонента (User, Product и т.д.)

        """
        singular_type = single_form_words.get(component_type, component_type.rstrip("s"))
        component_name = camel_to_snake(component_name)
        file_name = f"{component_name}_{singular_type}.py"
        file_path = path / file_name

        template_path = "base_template.py.jinja"
        content = self.template_engine.render(
            template_path, {"name": component_name, "type": component_type}
        )

        self.write_file(file_path, content)
