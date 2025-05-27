from dataclasses import dataclass

from src.core.template_engine import TemplateEngine
from src.preview.collector import PreviewCollector
from src.schemas import ConfigModel


@dataclass
class GenerationContext:
    """Context for project generation.

    This class holds all the necessary parts and settings
    required for project generation.

    Attributes:
        config: Project configuration model
        engine: Template engine for rendering
        preview_collector: Collector for preview mode
        preview_mode: Whether generation is in preview mode

    """

    config: ConfigModel
    engine: TemplateEngine
    preview_collector: PreviewCollector
    preview_mode: bool
