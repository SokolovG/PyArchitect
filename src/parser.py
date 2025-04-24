from pathlib import Path

import pydantic
import yaml

from src.exceptions import ConfigFileNotFoundError, YamlParseError
from src.schemas import ConfigModel


class YamlParser:
    DEFAULT_CONFIG_FILENAME = "ddd-config.yaml"

    def __init__(self, file_path: str | None = None) -> None:
        """Initialize YAML parser.

        Args:
            file_path: Optional specific config file path to use

        """
        self.file_path = Path(file_path) if file_path else Path(self.DEFAULT_CONFIG_FILENAME)

    def load(self) -> ConfigModel:
        """Load and parse the YAML configuration file.

        Returns:
            ConfigModel: Validated configuration model

        Raises:
            ConfigFileNotFoundError: If config file doesn't exist
            YamlParseError: If YAML parsing fails
            ValidationError: If configuration doesn't match the expected schema

        """
        if not self.file_path.exists():
            raise ConfigFileNotFoundError(str(self.file_path))

        with open(self.file_path, encoding="utf-8") as file:
            """Validate the configuration against the expected schema."""
            try:
                return self.validate(yaml.safe_load(file))

            except yaml.YAMLError as error:
                raise YamlParseError(error)  # noqa: B904

            except pydantic.ValidationError as error:
                raise error

    def validate(self, config: dict) -> ConfigModel:
        """Validate the configuration against the expected schema.

        Args:
            config: Raw data from yaml config

        Returns:
            ConfigModel: Validated configuration model

        Raises:
            ValidationError: If configuration doesn't match the expected schema

        """
        try:
            config_model = ConfigModel(**config)

            return config_model

        except pydantic.ValidationError as error:
            raise error

    def _ensure_list(self, value: str | list[str]) -> list[str]:
        """Ensure the value is a list."""
        if isinstance(value, str):
            return [value]

        return value if value is not None else []
