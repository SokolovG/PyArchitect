from pathlib import Path
from pprint import pprint

from src.core import single_form_words
from src.generators.base import BaseGenerator
from src.generators.layer_generators.base_layer_generator import AbstractLayerGenerator
from src.schemas.config_schema import DomainLayerConfig, PresetType


class DomainGenerator(BaseGenerator, AbstractLayerGenerator[DomainLayerConfig]):
    """Generator for the domain layer components.

    This class is responsible for generating all components of the domain layer
    based on the configuration.
    """

    def generate_components(self, path: Path, config: dict, preset: PresetType) -> None:
        """Generate all domain layer components.

        Args:
            path: Path where to generate components
            config: Configuration for domain components
            preset: Selected preset in the settings

        """
        flat = preset == PresetType.SIMPLE
        self._generate_components(path, config, flat)

    def _generate_components(
        self, domain_path: Path, domain_layer: dict, flat: bool = False
    ) -> None:
        """Generate domain components based on configuration.

        Args:
            domain_path: Path where to generate components
            domain_layer: Configuration for domain components
            flat: Whether to use flat structure instead of nested

        """
        pprint(domain_layer.items())
        for component_type, components in domain_layer.items():
            print(component_type, components)
            if not components or not isinstance(components, list):
                continue

            component_dir = domain_path

            if not flat:
                component_dir = domain_path / component_type
                self.create_directory(component_dir)
                self.create_init_file(component_dir)

            for component_name in components:
                self._generate_component(component_dir, component_type, component_name, flat)

    def _generate_component(
        self, path: Path, component_type: str, component_name: str, flat: bool
    ) -> None:
        """Generate a single domain component.

        Args:
            path: Directory where to generate the component
            component_type: Type of component (entities, value_objects, etc.)
            component_name: Name of the component
            flat: Whether using flat structure

        """
        clean_type = single_form_words.get(component_type)
        file_path = path / f"{component_name.lower()}_{clean_type}.py"
        template = self._get_template_for_component(component_type, component_name)

        self.write_file(file_path, template)

    def _get_template_for_component(self, component_type: str, component_name: str) -> str:
        """Get template content for specific component type.

        Args:
            component_type: Type of component (entities, value_objects, etc.)
            component_name: Name of the component

        Returns:
            Rendered template content as string

        """
        template_mapping = {
            "entities": "domain/entity.py.jinja",
            "value_objects": "domain/value_object.py.jinja",
            "aggregates": "domain/aggregate.py.jinja",
            "repository_interfaces": "domain/repository_interface.py.jinja",
            "domain_services": "domain/domain_service.py.jinja",
            "domain_events": "domain/domain_event.py.jinja",
            "factories": "domain/factory.py.jinja",
            "specifications": "domain/specification.py.jinja",
            "exceptions": "domain/exception.py.jinja",
        }
        template_path = template_mapping.get(component_type)
        if not template_path:
            return ""
        context: dict = {}
        template = self.template_engine.render(template_path, context)
        return template
