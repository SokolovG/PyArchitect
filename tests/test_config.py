from pathlib import Path

from src.core.parser import YamlParser
from src.schemas import ConfigModel
from src.schemas.config_schema import LayerConfig, PresetType, Settings, ContextsLayout


class TestConfigModel:

    def test_preset_choice(self) -> None:
        simple_config = ConfigModel(
            settings=Settings(preset=PresetType.SIMPLE), layers=LayerConfig()
        )
        standard_config = ConfigModel(
            settings=Settings(preset=PresetType.STANDARD), layers=LayerConfig()
        )
        advanced_config = ConfigModel(
            settings=Settings(preset=PresetType.ADVANCED), layers=LayerConfig()
        )
        assert simple_config.settings.preset == "simple"
        assert standard_config.settings.preset == "standard"
        assert advanced_config.settings.preset == "advanced"

    def test_valid_required_fields(self) -> None:
        minimal_config = ConfigModel(layers=LayerConfig())

        assert minimal_config.settings.preset == PresetType.STANDARD
        assert minimal_config.settings.use_contexts is True
        assert minimal_config.settings.root_name == "src"

    def test_model_post_init(self) -> None:
        simple_config = ConfigModel(
            settings=Settings(preset=PresetType.SIMPLE), layers=LayerConfig()
        )
        assert simple_config.settings.use_contexts is False

        standard_config = ConfigModel(
            settings=Settings(preset=PresetType.STANDARD), layers=LayerConfig()
        )
        assert standard_config.settings.use_contexts is True
        assert standard_config.settings.contexts_layout == ContextsLayout.FLAT

        advanced_config = ConfigModel(
            settings=Settings(preset=PresetType.ADVANCED), layers=LayerConfig()
        )
        assert advanced_config.settings.use_contexts is True
        assert advanced_config.settings.contexts_layout == ContextsLayout.NESTED
