import os
from typing import TypeVar

from src.generator_helper import DomainGenerator, GeneratorHelper
from src.parser import YamlParser

T = TypeVar("T")


class ProjectGenerator:
    def __init__(
        self,
        parser: YamlParser,
        helper: GeneratorHelper,
        domain_helper: DomainGenerator,
    ) -> None:
        """F."""
        self.parser = parser
        self.config = parser.load()
        self.helper = helper
        self.domain_helper = domain_helper

    def generate(self) -> None:
        """Generate the project structure based on the configuration."""
        print("Starting project generation...")
        project_root = os.getcwd()
        src_path = os.path.join(project_root, "src")
        os.mkdir(src_path)

        domain_path = os.path.join(src_path, "domain")
        application_path = os.path.join(src_path, "application")
        infrastructure_path = os.path.join(src_path, "infrastructure")

        os.mkdir(domain_path)
        os.mkdir(application_path)
        os.mkdir(infrastructure_path)

        self.helper._create_init_file(
            (src_path, domain_path, application_path, infrastructure_path)
        )

        for context in self.config.contexts:
            context_path = os.path.join(domain_path, context.name)
            os.mkdir(context_path)
            self.helper._create_init_file((context_path,))

            self.domain_helper.generate_entities(context_path, context.domain.entities)
