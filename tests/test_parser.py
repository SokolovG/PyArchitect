import os
from pathlib import Path

import pytest

from src.core.exceptions import ConfigFileNotFoundError, YamlParseError
from src.core.parser import YamlParser
from src.schemas import ConfigModel


class TestYamlParser:
    def test_load_valid_yaml_file(self, yaml_parser: YamlParser, valid_yaml_path: Path) -> None:
        config = yaml_parser.load(valid_yaml_path)
        assert isinstance(config, ConfigModel)

    def test_load_not_valid_yaml_file(
        self, yaml_parser: YamlParser, not_valid_yaml_path: Path
    ) -> None:
        with pytest.raises(YamlParseError):
            yaml_parser.load(not_valid_yaml_path)

    def test_load_not_exist_yaml_file(
        self, yaml_parser: YamlParser, not_exist_yaml_path: Path
    ) -> None:
        with pytest.raises(ConfigFileNotFoundError):
            yaml_parser.load(not_exist_yaml_path)

    def test_load_default_file_name(
        self, yaml_parser: YamlParser, tmp_path: Path, valid_yaml_path: Path
    ) -> None:
        config_file = tmp_path / "ddd-config.yaml"
        config_file.write_text(valid_yaml_path.read_text())

        original_cwd = Path.cwd()
        os.chdir(tmp_path)

        try:
            config = yaml_parser.load()
            assert isinstance(config, ConfigModel)
        finally:
            os.chdir(original_cwd)
