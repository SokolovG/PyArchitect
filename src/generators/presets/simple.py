from logging import getLogger
from pathlib import Path

from src.generators.base import BaseGenerator
from src.generators.presets.base import PresetGenerator
from src.generators.utils import LayerPaths
from src.schemas import ConfigModel
from src.schemas.config_schema import PresetType

logger = getLogger(__name__)


class SimplePresetGenerator(PresetGenerator, BaseGenerator):
    """Generator for the simple preset without contexts."""

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate simple project structure without contexts."""
        logger.info("Starting generate domain")
        layer_paths = LayerPaths.from_config(root_path, config)

        layer_generators = {
            "domain": self.domain_generator,
            "application": self.app_generator,
            "infrastructure": self.infra_generator,
            "interface": self.interface_generator,
        }

        if config.layers:
            for layer_name, layer_config in config.layers.model_dump().items():
                if not layer_config:
                    continue

                layer_path = getattr(layer_paths, layer_name, None)
                if not layer_path:
                    layer_path = root_path / config.settings.root_name / layer_name

                self.create_directory(layer_path)
                self.create_init_file(layer_path)

                generator = layer_generators.get(layer_name)
                if generator:
                    generator.generate_components(layer_path, layer_config, PresetType.SIMPLE)  # type: ignore
                else:
                    logger.warning(f"No generator found for layer: {layer_name}")
