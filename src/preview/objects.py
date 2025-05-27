from dataclasses import dataclass, field
from enum import Enum


class ComponentType(str, Enum):
    """Enumeration of possible component types in the preview structure.

    This enum defines the types of nodes that can exist in the preview tree.
    """

    DIRECTORY = "directory"
    FILE = "file"
    LAYER = "layer"
    INIT = "init"


@dataclass
class PreviewNode:
    """Node in the preview structure tree.

    This class represents a single node in the preview structure tree,
    which can be a directory, file, layer, or init file.

    Attributes:
        name: Name of the component
        type: Type of the component
        path: Full path to the component
        children: List of child nodes
        metadata: Additional metadata for the node

    """

    name: str
    type: ComponentType
    path: str
    children: list["PreviewNode"] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
