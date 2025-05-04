from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar

from pydantic import BaseModel

if TYPE_CHECKING:
    from src.schemas.config_schema import PresetType


ConfigT = TypeVar("ConfigT", bound=BaseModel)


class AbstractLayerGenerator(Generic[ConfigT], ABC):
    @abstractmethod
    def generate_components(self, path: Path, config: ConfigT, preset: PresetType) -> None:
        """Генерирует все компоненты слоя."""
