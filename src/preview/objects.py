from dataclasses import dataclass, field
from enum import Enum


class ComponentType(str, Enum):
    DIRECTORY = "directory"
    FILE = "file"
    LAYER = "layer"
    INIT = "init"


@dataclass
class PreviewNode:
    name: str
    type: ComponentType
    path: str
    children: list["PreviewNode"] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
