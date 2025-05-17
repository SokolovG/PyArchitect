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
        DEFAULT_CONFIG_PATH: Default filename for config file
        file_path: Path to the configuration file

    """

    def __init__(self, file_path: Path | None = None) -> None:
        """Initialize YAML parser.

        Args:
            file_path: Optional specific config file path to use

        """
        if file_path:
            self.file_path = file_path
        else:
            package_dir = Path(__file__).parent.parent.parent / "examples"
            self.file_path = package_dir / "ddd-config-advanced.yaml"

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
            try:
                return self.validate(yaml.safe_load(file))

            except yaml.YAMLError as error:
                raise YamlParseError(error)  # noqa: B904

            except pydantic.ValidationError as error:
                raise error

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
            print(f"Ошибка валидации: {error}")
            raise error
