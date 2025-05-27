from dataclasses import dataclass

from src.core.template_engine import TemplateEngine
from src.preview.collector import PreviewCollector
from src.schemas import ConfigModel


@dataclass
class GenerationContext:
    config: ConfigModel
    engine: TemplateEngine
    preview_collector: PreviewCollector
    preview_mode: bool
