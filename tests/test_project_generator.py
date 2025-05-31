import tempfile
import os
from pathlib import Path
from unittest.mock import Mock

from src.core.utils import GenerationContext
from src.core.template_engine import TemplateEngine
from src.generators.project_generator import ProjectGenerator
from src.preview.collector import PreviewCollector
from src.schemas.config_schema import ConfigModel, Settings, PresetType, LayerConfig


class TestProjectGenerator:

    def test_create_root_dir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)

                config = ConfigModel(
                    settings=Settings(root_name="test_app"), layers=LayerConfig()
                )
                context = GenerationContext(
                    config=config, engine=Mock(spec=TemplateEngine), preview_mode=False
                )

                generator = ProjectGenerator(context)
                generator.generate()

                root_path = Path(temp_dir) / "test_app"
                assert root_path.exists()
                assert root_path.is_dir()
                assert (root_path / "__init__.py").exists()

            finally:
                os.chdir(original_cwd)

    def test_choose_preset(self) -> None:
        configs = [
            (PresetType.SIMPLE, "SimplePresetGenerator"),
            (PresetType.STANDARD, "StandardPresetGenerator"),
            (PresetType.ADVANCED, "AdvancedPresetGenerator"),
        ]

        for preset_type, expected_class_name in configs:
            config = ConfigModel(
                settings=Settings(preset=preset_type), layers=LayerConfig()
            )
            context = GenerationContext(
                config=config, engine=Mock(spec=TemplateEngine), preview_mode=False
            )

            generator = ProjectGenerator(context)
            assert generator.preset_generator.__class__.__name__ == expected_class_name

    def test_create_init_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = Path.cwd()
            try:
                os.chdir(temp_dir)

                config = ConfigModel(
                    settings=Settings(root_name="myapp", init_imports=True),
                    layers=LayerConfig(),
                )
                context = GenerationContext(
                    config=config, engine=Mock(spec=TemplateEngine), preview_mode=False
                )

                generator = ProjectGenerator(context)
                generator.generate()

                root_path = Path(temp_dir) / "myapp"
                init_file = root_path / "__init__.py"
                assert init_file.exists()
                assert init_file.is_file()

            finally:
                os.chdir(original_cwd)

    def test_normal_and_preview_mode(self) -> None:
        config = ConfigModel(
            settings=Settings(root_name="preview_test"), layers=LayerConfig()
        )

        preview_collector = Mock(spec=PreviewCollector)
        preview_context = GenerationContext(
            config=config,
            engine=Mock(spec=TemplateEngine),
            preview_mode=True,
            preview_collector=preview_collector,
        )

        preview_generator = ProjectGenerator(preview_context)

        normal_context = GenerationContext(
            config=config, engine=Mock(spec=TemplateEngine), preview_mode=False
        )

        normal_generator = ProjectGenerator(normal_context)
        assert preview_generator.context.preview_mode is True
        assert preview_generator.context.preview_collector is not None
        assert normal_generator.context.preview_mode is False
        assert normal_generator.context.preview_collector is None
