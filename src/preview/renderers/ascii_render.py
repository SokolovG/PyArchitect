from src.preview.renderers.base_render import BaseAbstractPreviewRender


class AsciiPreviewRender(BaseAbstractPreviewRender):
    def render(self) -> None:
        """Render ascii."""
