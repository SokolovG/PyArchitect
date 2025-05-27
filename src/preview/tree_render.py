from rich.console import Console
from rich.tree import Tree

from src.preview.base_render import BaseAbstractPreviewRender
from src.preview.objects import PreviewNode


class TreePreviewRender(BaseAbstractPreviewRender):
    def render(self) -> None:
        """Render tree."""
        tree = self._build_tree(self.root_node)  # type: ignore
        console = Console(record=True)
        console.print(tree)
        text = console.export_text()
        with open("structure.md", "w") as f:
            f.write(text)

    def _build_tree(self, node: PreviewNode) -> Tree:
        tree = Tree(node.name)

        for child in node.children:
            child_tree = self._build_tree(child)
            tree.add(child_tree)

        return tree
