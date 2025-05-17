from logging import getLogger
from pathlib import Path

from src.generators.layer_generator import LayerGenerator
from src.generators.presets.base import AbstractPresetGenerator
from src.generators.utils import GeneratorUtilsMixin
from src.schemas import ConfigModel

logger = getLogger(__name__)


class AdvancedPresetGenerator(AbstractPresetGenerator, GeneratorUtilsMixin):
    """Generator for the advanced preset with custom layout.

    This generator creates a project structure with custom layout options,
    allowing for more flexibility in organizing bounded contexts and layers.
    """

    def generate(self, root_path: Path, config: ConfigModel) -> None:
        """Generate advanced project structure with custom organization.

        This implementation allows for highly customized project layouts,
        supporting both nested contexts (layers inside contexts) and
        other advanced organizational patterns.

        Args:
            root_path: Path to the project root directory
            config: Project configuration model containing settings and layout definitions

        """
