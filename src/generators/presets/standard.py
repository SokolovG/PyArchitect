from pathlib import Path

from src.generators.base import PresetGenerator
from src.generators.utils import LayerPaths
from src.schemas import ConfigModel


class StandardPresetGenerator(PresetGenerator):
    """Generator for the standard preset with contexts in layers."""

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate standard project structure with contexts organized by layers."""
        layer_paths = LayerPaths.from_config(root_path, config)

        self._generate_domain_layer(layer_paths.layer_1, config)

    def _generate_domain_layer(self, domain_path: Path, config: ConfigModel) -> None:
        """Generate domain layer with contexts."""
        if not config.layers:
            return

        domain_layer = config.layers.domain
        if not domain_layer:
            return

        contexts = config.contexts or []

        for context in contexts:
            context_name = context.name
            context_path = domain_path / context_name
            self.domain_generator.create_directory(context_path)
            self.domain_generator.create_init_file(context_path)

            # Generate context components
            self.domain_generator.generate_components(context_path, context.model_dump())
