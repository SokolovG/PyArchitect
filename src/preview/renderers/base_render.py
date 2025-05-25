from abc import ABC, abstractmethod


class BaseAbstractPreviewRender(ABC):
    def __init__(self, preview_data: dict) -> None:
        """Init data."""
        self.data = preview_data

    @abstractmethod
    def render(self) -> None:
        """Render preview."""
