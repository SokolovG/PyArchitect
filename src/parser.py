from pathlib import Path
from typing import Any

import yaml

from src.exceptions import ConfigFileNotFoundError, YamlParseError


class YamlParser:
    DEFAULT_CONFIG_FILENAME = "ddd-config.yaml"

    def __init__(self, file_path: str | None = None) -> None:
        """Initialize YAML parser.

        Args:
            file_path: Optional specific config file path to use

        """
        self.file_path = Path(file_path) if file_path else Path(self.DEFAULT_CONFIG_FILENAME)
        self.config: dict[str, Any] = {}

    def load(self) -> dict[str, Any]:
        """Load and parse the YAML configuration file.

        Returns:
            dict: Parsed configuration

        Raises:
            ConfigFileNotFoundError: If config file doesn't exist
            YamlParseError: If YAML parsing fails

        """
        if not self.file_path.exists():
            raise ConfigFileNotFoundError(str(self.file_path))

        with open(self.file_path, encoding="utf-8") as file:
            """Validate the configuration against the expected schema."""
            try:
                self.config = yaml.safe_load(file)
                print(self.config)
                return self.config

            except yaml.YAMLError as error:
                raise YamlParseError(error)  # noqa: B904

    def validate(self) -> None:
        """Validate the configuration against the expected schema."""
        pass

    def migrate(self) -> None:
        """Migrate configuration from older versions if needed."""
        pass
