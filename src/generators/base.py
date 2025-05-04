from pathlib import Path


class BaseGenerator:
    """Base class for all code generators.

    This class provides common utility methods used by all specific
    generator implementations.
    """

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

    def ensure_list(self, value: str | list[str]) -> list[str]:
        """Convert a value to a list if it's a string or return as is if it's already a list.

        Args:
            value: String or list of strings

        Returns:
            List of strings

        """
        if isinstance(value, str):
            return [value]
        return value if value is not None else []
