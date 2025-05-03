from abc import ABC, abstractmethod
from pathlib import Path


class AbstractLayerGenerator(ABC):
    @abstractmethod
    def generate_components(self, path: Path, config: dict) -> None:
        """Генерирует все компоненты слоя."""
