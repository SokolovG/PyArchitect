from logging import getLogger
from pathlib import Path

from icecream import ic

from src.preview.objects import ComponentType, PreviewNode

logger = getLogger(__name__)


class PreviewCollector:
    """Collects information about project structure for preview mode."""

    def __init__(self, render_format: str = "tree") -> None:
        """Initialize collector.

        Args:
            render_format: Format for rendering

        """
        self.render_format = render_format
        self.root_node: PreviewNode | None = None
        self.nodes: dict[str, PreviewNode] = {}

    def add_directory(self, path: Path) -> None:
        """Add directory to preview structure.

        Args:
            path: Directory path

        """
        logger.critical(f"Creating preview directory with path - {path}")
        path_str = str(path)

        node = PreviewNode(name=path.name, type=ComponentType.DIRECTORY, path=path_str)
        ic(node)
        self.nodes[path_str] = node

        parent_path = str(path.parent)
        ic(parent_path)
        ic(self.nodes)
        if parent_path in self.nodes:
            parent_node = self.nodes[parent_path]
            if node not in parent_node.children:
                parent_node.children.append(node)
        elif self.root_node is None:
            self.root_node = node

    def add_file(self, path: Path, file_type: ComponentType = ComponentType.FILE) -> None:
        """Add a file to preview structure.

        Args:
            path: File path
            file_type: Type of file

        """
        ic(path)
        path_str = str(path)

        node = PreviewNode(name=path.name, type=file_type, path=path_str)
        ic(node)

        parent_path = str(path.parent)
        ic(parent_path)
        if parent_path in self.nodes:
            parent_node = self.nodes[parent_path]
            if node not in parent_node.children:
                parent_node.children.append(node)
            ic(parent_node)

    def add_init_file(self, path: Path) -> None:
        """Add __init__.py a file to preview structure.

        Args:
            path: Init path

        """
        self.add_file(path, ComponentType.INIT)

    def render(self) -> None:
        """Render collected structure using selected renderer."""
        if not self.root_node:
            print("No structure to preview")
            return
