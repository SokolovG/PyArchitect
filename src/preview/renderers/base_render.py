from abc import ABC, abstractmethod


class BaseAbstractPreviewRender(ABC):
    @abstractmethod
    def render(self) -> None:
        """Render preview."""
