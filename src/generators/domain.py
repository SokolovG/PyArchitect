from pathlib import Path

from src.generators.base import BaseGenerator
from src.schemas.config_schema import DomainLayer


class DomainGenerator(BaseGenerator):
    """Generator for the domain layer components.

    This class is responsible for generating all components of the domain layer
    based on the configuration.
    """

    def generate_domain_components(
        self, domain_path: Path, domain_layer: DomainLayer, flat: bool = False
    ) -> None:
        """Generate all domain layer components.

        Args:
            domain_path: Path where to generate components
            domain_layer: Configuration for domain components
            flat: Whether to use flat structure instead of nested

        """
        domain_path_obj = domain_path

        if flat:
            self.generate_entities(domain_path, domain_layer.entities)
            self.generate_value_objects(domain_path, domain_layer.value_objects)
            self.generate_aggregates(domain_path, domain_layer.aggregates)
            self.generate_repository_interfaces(domain_path, domain_layer.repository_interfaces)
            self.generate_domain_services(domain_path, domain_layer.domain_services)
            self.generate_domain_events(domain_path, domain_layer.domain_events)
            self.generate_factories(domain_path, domain_layer.factories)
            self.generate_specifications(domain_path, domain_layer.specifications)
            self.generate_exceptions(domain_path, domain_layer.exceptions)
        else:
            # Entities
            if domain_layer.entities:
                entities_path = domain_path_obj / "entities"
                self.create_directory(entities_path)
                self.create_init_file(entities_path)
                self.generate_entities(entities_path, domain_layer.entities)

            # Value Objects
            if domain_layer.value_objects:
                vo_path = domain_path_obj / "value_objects"
                self.create_directory(vo_path)
                self.create_init_file(vo_path)
                self.generate_value_objects(vo_path, domain_layer.value_objects)  # Исправлено

            # Aggregates
            if domain_layer.aggregates:
                agg_path = domain_path_obj / "aggregates"
                self.create_directory(agg_path)
                self.create_init_file(agg_path)
                self.generate_aggregates(agg_path, domain_layer.aggregates)  # Исправлено

            # Repository Interfaces
            if domain_layer.repository_interfaces:
                repo_path = domain_path_obj / "repositories"
                self.create_directory(repo_path)
                self.create_init_file(repo_path)
                self.generate_repository_interfaces(
                    repo_path,
                    domain_layer.repository_interfaces,
                )

            # Domain Services
            if domain_layer.domain_services:
                services_path = domain_path_obj / "services"
                self.create_directory(services_path)
                self.create_init_file(services_path)
                self.generate_domain_services(services_path, domain_layer.domain_services)

            # Domain Events
            if domain_layer.domain_events:
                events_path = domain_path_obj / "events"
                self.create_directory(events_path)
                self.create_init_file(events_path)
                self.generate_domain_events(events_path, domain_layer.domain_events)

            # Factories
            if domain_layer.factories:
                factories_path = domain_path_obj / "factories"
                self.create_directory(factories_path)
                self.create_init_file(factories_path)
                self.generate_factories(factories_path, domain_layer.factories)

            # Specifications
            if domain_layer.specifications:
                specs_path = domain_path_obj / "specifications"
                self.create_directory(specs_path)
                self.create_init_file(specs_path)
                self.generate_specifications(specs_path, domain_layer.specifications)

            # Exceptions
            if domain_layer.exceptions:
                exceptions_path = domain_path_obj / "exceptions"
                self.create_directory(exceptions_path)
                self.create_init_file(exceptions_path)
                self.generate_exceptions(exceptions_path, domain_layer.exceptions)

    def generate_entities(self, path: Path, entities: str | list[str]) -> None:
        """Generate entity classes.

        Args:
            path: Directory where to generate entity files
            entities: Entity names to generate

        """
        entities = self.ensure_list(entities)

        for entity in entities:
            entity_file = path / f"{entity.lower()}.py"
            with open(entity_file, "w"):
                pass

    def generate_value_objects(self, path: Path, value_objects: str | list[str]) -> None:
        """Generate value object classes.

        Args:
            path: Directory where to generate value object files
            value_objects: Value object names to generate

        """
        value_objects = self.ensure_list(value_objects)

        for vo in value_objects:
            vo_file = path / f"{vo.lower()}.py"
            with open(vo_file, "w"):
                pass

    def generate_aggregates(self, path: Path, aggregates: str | list[str]) -> None:
        """Generate aggregate root classes.

        Args:
            path: Directory where to generate aggregate files
            aggregates: Aggregate names to generate

        """
        aggregates = self.ensure_list(aggregates)

        for aggregate in aggregates:
            agg_file = path / f"{aggregate.lower()}.py"
            with open(agg_file, "w"):
                pass

    def generate_repository_interfaces(self, path: Path, repositories: str | list[str]) -> None:
        """Generate repository interface classes.

        Args:
            path: Directory where to generate repository interface files
            repositories: Repository names to generate

        """
        repositories = self.ensure_list(repositories)

        for repo in repositories:
            repo_file = path / f"{repo.lower()}.py"
            with open(repo_file, "w"):
                pass

    def generate_domain_services(self, path: Path, services: str | list[str]) -> None:
        """Generate domain service classes.

        Args:
            path: Directory where to generate domain service files
            services: Service names to generate

        """
        services = self.ensure_list(services)

        for service in services:
            service_file = path / f"{service.lower()}.py"
            with open(service_file, "w"):
                pass

    def generate_domain_events(self, path: Path, events: str | list[str]) -> None:
        """Generate domain event classes.

        Args:
            path: Directory where to generate domain event files
            events: Event names to generate

        """
        events = self.ensure_list(events)

        for event in events:
            event_file = path / f"{event.lower()}.py"
            with open(event_file, "w"):
                pass

    def generate_factories(self, path: Path, factories: str | list[str]) -> None:
        """Generate factory classes.

        Args:
            path: Directory where to generate factory files
            factories: Factory names to generate

        """
        factories = self.ensure_list(factories)

        for factory in factories:
            factory_file = path / f"{factory.lower()}.py"
            with open(factory_file, "w"):
                pass

    def generate_specifications(self, path: Path, specifications: str | list[str]) -> None:
        """Generate specification pattern classes.

        Args:
            path: Directory where to generate specification files
            specifications: Specification names to generate

        """
        specifications = self.ensure_list(specifications)

        for spec in specifications:
            spec_file = path / f"{spec.lower()}.py"
            with open(spec_file, "w"):
                pass

    def generate_exceptions(self, path: Path, exceptions: str | list[str]) -> None:
        """Generate domain exception classes.

        Args:
            path: Directory where to generate exception files
            exceptions: Exception names to generate

        """
        exceptions = self.ensure_list(exceptions)

        for exception in exceptions:
            exception_file = path / f"{exception.lower()}.py"
            with open(exception_file, "w"):
                pass
