from abc import ABC, abstractmethod

from src.core.template_engine import TemplateEngine
from src.preview.objects import PreviewNode


class BaseAbstractPreviewRender(ABC):
    def __init__(self, preview_data: dict, root_node: PreviewNode | None = None) -> None:
        """Init data."""
        self.data = preview_data
        self.root_node = root_node
        self.template_engine = TemplateEngine()

    @abstractmethod
    def render(self) -> None:
        """Render preview."""
