from logging import getLogger
from pathlib import Path

from src.core.exceptions import StructureForPreviewNotFoundError
from src.preview.base_render import BaseAbstractPreviewRender
from src.preview.objects import ComponentType, PreviewNode
from src.preview.tree_render import TreePreviewRender

logger = getLogger(__name__)


class PreviewCollector:
    """Collects information about project structure for preview mode."""

    RENDER_TYPES: dict[str, type[BaseAbstractPreviewRender]] = {
        "tree": TreePreviewRender,
    }

    def __init__(self, render_format: str) -> None:
        """Initialize collector.

        Args:
            render_format: Format for rendering

        """
        self.display_type = render_format
        self.root_node: PreviewNode | None = None
        self.nodes: dict[str, PreviewNode] = {}
        self.renderer = self.RENDER_TYPES.get(render_format, TreePreviewRender)(self.nodes)

    def add_directory(self, path: Path) -> None:
        """Add directory to preview structure.

        Args:
            path: Directory path

        """
        path_str = str(path)

        node = PreviewNode(name=path.name, type=ComponentType.DIRECTORY, path=path_str)
        self.nodes[path_str] = node

        parent_path = str(path.parent)
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
        path_str = str(path)

        node = PreviewNode(name=path.name, type=file_type, path=path_str)

        parent_path = str(path.parent)
        if parent_path in self.nodes:
            parent_node = self.nodes[parent_path]
            if node not in parent_node.children:
                parent_node.children.append(node)

    def add_init_file(self, path: Path) -> None:
        """Add __init__.py a file to preview structure.

        Args:
            path: Init path

        """
        self.add_file(path, ComponentType.INIT)

    def display(self) -> None:
        """Display collected structure using selected renderer."""
        if not self.root_node:
            raise StructureForPreviewNotFoundError()
        self.renderer.root_node = self.root_node

        self.renderer.render()
