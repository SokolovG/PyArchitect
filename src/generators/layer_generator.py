from pathlib import Path

from src.generators.base import BaseGenerator
from src.templates.engine import TemplateEngine


class LayerGenerator(BaseGenerator):
    """Базовый генератор для любого слоя."""

    def __init__(self, template_engine: TemplateEngine, template_dir: str) -> None:
        """Инициализация генератора слоя.

        Args:
            template_engine: Движок шаблонов
            template_dir: Директория с шаблонами для данного слоя

        """
        super().__init__(template_engine)
        self.template_dir = template_dir

    def generate_components(self, path: Path, layer_config: dict[str, list[str]]) -> None:
        """Генерация всех компонентов для слоя.

        Args:
            path: Путь, куда генерировать
            layer_config: Конфигурация слоя в виде словаря

        """
        # Создаем корневую директорию, если не существует
        self.create_directory(path)
        self.create_init_file(path)

        # Перебираем все типы компонентов
        for component_type, components in layer_config.items():
            if not components:
                continue

            # Создаем директорию для типа компонента
            component_dir = path / component_type
            self.create_directory(component_dir)
            self.create_init_file(component_dir)

            # Генерируем каждый компонент
            for component_name in components:
                self._generate_component(component_dir, component_type, component_name)

    def _generate_component(self, path: Path, component_type: str, component_name: str) -> None:
        """Генерация отдельного компонента.

        Args:
            path: Путь, куда генерировать
            component_type: Тип компонента (entities, value_objects и т.д.)
            component_name: Имя компонента (User, Product и т.д.)

        """
        # Определяем имя файла
        singular_type = component_type.rstrip("s")  # Простое преобразование во ед. число
        file_name = f"{component_name.lower()}_{singular_type}.py"
        file_path = path / file_name

        # Ищем шаблон
        template_path = f"{self.template_dir}/{component_type}.py.jinja"
        if self.template_engine.template_exists(template_path):
            # Если есть шаблон - используем его
            content = self.template_engine.render(
                template_path, {"name": component_name, "type": component_type}
            )
        else:
            # Если шаблона нет - создаем пустой класс
            content = f'class {component_name}:\n    """A {singular_type} component."""\n    pass\n'

        # Записываем файл
        self.write_file(file_path, content)
