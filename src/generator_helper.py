import os


class GeneratorHelper:
    def _create_init_file(self, directory: tuple) -> None:
        for _dir in directory:
            init_path = os.path.join(_dir, "__init__.py")
            with open(init_path, "w"):
                pass


class DomainGenerator:
    def generate_entities(self, path: str, entities: str | list) -> None:
        """Generate entity classes for a bounded context.

        Args:
            path: Path to the domain context directory
            entities: List of entity names or single entity name

        """
        if not entities:
            return

        entities_dir = os.path.join(path, "entities")
        os.makedirs(entities_dir, exist_ok=True)

        entities = [entities] if isinstance(entities, str) else entities
        for entity in entities:
            snake_case_name = "".join(
                ["_" + c.lower() if c.isupper() else c.lower() for c in entity]
            ).lstrip("_")

            entity_file = os.path.join(entities_dir, f"{snake_case_name}.py")

            with open(entity_file, "w") as file:
                file.write(f"class {entity}:\n")
                file.write(f'    """Entity class for {entity}."""\n')
