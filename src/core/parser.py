from pathlib import Path

import pydantic
import yaml

from src.core.exceptions import ConfigFileNotFoundError, YamlParseError
from src.schemas import ConfigModel


class YamlParser:
    """Parser for YAML configuration files.

    This class is responsible for loading and validating the YAML
    configuration file according to the expected schema.

    Attributes:
        file_path: Path to the configuration file

    """

    DEFAULT_CONFIG_FILENAME = "ddd-config.yaml"

    def load(self, file_path: Path | None = None) -> ConfigModel:
        """Load and parse the YAML configuration file.

        ArgsL
            file_path: Path to YAML config.

        Returns:
            ConfigModel: Validated configuration model

        Raises:
            ConfigFileNotFoundError: If a config file doesn't exist
            YamlParseError: If YAML parsing fails
            ValidationError: If configuration doesn't match the expected schema

        """
        if file_path is None:
            file_path = Path.cwd() / self.DEFAULT_CONFIG_FILENAME

        if not file_path.exists():
            raise ConfigFileNotFoundError(str(file_path))

        with open(file_path, encoding="utf-8") as file:
            try:
                raw_config = yaml.safe_load(file)
                return self.validate(raw_config)
            except yaml.YAMLError as error:
                raise YamlParseError(error) from error

    def validate(self, config: dict) -> ConfigModel:
        """Validate the configuration against the expected schema.

        Args:
            config: raw config

        Returns:
            Validated config model

        """
        if config is None:
            config = {}

        try:
            config_model = ConfigModel.model_validate(config)
            return config_model
        except pydantic.ValidationError as error:
            print(f"Validation error: {error}")
            raise error
