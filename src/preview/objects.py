from dataclasses import dataclass, field


@dataclass
class PreviewNode:
    name: str
    type: str  # "directory", "file", "layer", "component"
    path: str
    children: list["PreviewNode"] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
