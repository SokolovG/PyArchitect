from pathlib import Path

from src.templates.engine import TemplateEngine


class BaseGenerator:
    """Base class for all code generators.

    This class provides common utility methods used by all specific
    generator implementations.
    """

    def __init__(self, template_engine: TemplateEngine) -> None:
        """F."""
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

    def create_init_file(self, path: Path) -> Path:
        """Create an empty __init__.py file in the specified directory.

        Args:
            path: Directory where to create the file

        Returns:
            Path to the created file

        """
        init_file = path / "__init__.py"
        if not init_file.exists():
            init_file.touch()
        return init_file

    def write_file(self, path: Path, content: str) -> None:
        """Write content to a file.

        Args:
        path: Path where to write the file
        content: Content to write to the file

        """
        with open(path, "w") as file:
            file.write(content)
