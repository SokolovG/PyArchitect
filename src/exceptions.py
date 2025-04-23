from typing import Generic, TypeVar

import yaml

T = TypeVar("T")


class BaseExceptionPayload(Generic[T]):
    """Base class for storing exception context data."""

    def __init__(self, value: T, msg: str | None = None) -> None:
        """F."""
        self.msg = msg
        self.value = value


class PyArchitectError(BaseExceptionPayload[T], Exception, Generic[T]):
    """Base exception class for PyArchitect."""

    pass


class ConfigFileNotFoundError(PyArchitectError[str]):
    """Raised when the config file is not found."""

    def __str__(self) -> str:
        return f"Configuration file not found: {self.value}"


class YamlParseError(BaseExceptionPayload[yaml.YAMLError], Exception):
    """Raised when the config file is not successfully parsed."""

    def __str__(self) -> str:
        return f"Configuration file could not be parsed: {self.value}"
