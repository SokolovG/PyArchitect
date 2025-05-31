from pathlib import Path
from unittest.mock import Mock

import pytest

from src.core.parser import YamlParser
from src.core.template_engine import TemplateEngine
from src.generators.utils import (
    StandardImportPathGenerator,
    AdvancedImportPathGenerator,
    FileOperations,
)
from src.preview.collector import PreviewCollector

IMPORT_DATA = (
    "src",
    "domain",
    "user_context",
    "entities",
    "customer",
    "Customer",
)
DEFAULT_CONFIG_FILENAME = "ddd-config.yaml"
DEFAULT_CONFIG_NOT_VALID_FILENAME = "ddd-config-not-valid.yaml"


@pytest.fixture
def yaml_parser() -> YamlParser:
    return YamlParser()


@pytest.fixture
def valid_yaml_path() -> Path:
    test_dir = Path(__file__).parent
    file_path = test_dir / "fixtures" / DEFAULT_CONFIG_FILENAME
    return Path(file_path)


@pytest.fixture
def not_valid_yaml_path() -> Path:
    test_dir = Path(__file__).parent
    file_path = test_dir / "fixtures" / DEFAULT_CONFIG_NOT_VALID_FILENAME
    return Path(file_path)


@pytest.fixture
def not_exist_yaml_path() -> Path:
    test_dir = Path(__file__).parent
    file_path = test_dir / "fixtures" / DEFAULT_CONFIG_NOT_VALID_FILENAME / "not_exist"
    return Path(file_path)


@pytest.fixture
def camel_snake_tuple() -> tuple[str, str]:
    return ("UserService", "user_service")


@pytest.fixture
def template_engine() -> TemplateEngine:
    return TemplateEngine()


@pytest.fixture
def template_dir() -> Path:
    path = Path(__file__).parent.parent / "templates"
    return path


@pytest.fixture
def import_tuple() -> tuple:
    return IMPORT_DATA


@pytest.fixture
def flat_import_gen() -> StandardImportPathGenerator:
    return StandardImportPathGenerator()


@pytest.fixture
def nested_import_gen() -> AdvancedImportPathGenerator:
    return AdvancedImportPathGenerator()


@pytest.fixture
def file_ops() -> FileOperations:
    mock_template_engine = Mock()
    preview_collector = PreviewCollector()
    file_ops = FileOperations(mock_template_engine, preview_collector)
    return file_ops
