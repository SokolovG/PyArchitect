from typing import TypeVar

T = TypeVar("T")


class BaseExceptionPayload:
    """Base class for storing exception context data.

    This class provides a generic way to store contextual data with exceptions.

    Attributes:
        msg: Optional error message
        value: Value that caused the exception

    """

    def __init__(self, value: T | None = None, msg: str | None = None) -> None:
        """Initialize the exception payload.

        Args:
            value: The value that caused the exception
            msg: Optional error message

        """
        self.msg = msg
        self.value = value


class PyArchitectError(BaseExceptionPayload, Exception):
    """Base exception class for PyArchitect.

    All specific exceptions in the project should inherit from this class.
    """


class ConfigFileNotFoundError(PyArchitectError):
    """Raised when the config file isn't found.

    This exception is raised when the specified configuration file
    doesn't exist or can't be accessed.
    """

    def __str__(self) -> str:
        """Return string representation of the error.

        Returns:
            Error message with a path

        """
        return f"Configuration file not found: {self.value}"


class YamlParseError(BaseExceptionPayload, Exception):
    """Raised when the config file isn't successfully parsed.

    This exception is raised when there are syntax errors or other issues
    with the YAML configuration file.
    """

    def __str__(self) -> str:
        """Return string representation of the error.

        Returns:
            Error message with original YAML error

        """
        return f"Configuration file could not be parsed: {self.value}"


class StructureForPreviewNotFoundError(BaseExceptionPayload, Exception):
    """Raised when the structure for preview not found.

    This exception is raised when attempting to display a preview structure
    without a valid root node.
    """

    def __str__(self) -> str:
        """Return string representation of the error.

        Returns:
            Error message with root node name

        """
        return f"No root node with name {self.value} found."
