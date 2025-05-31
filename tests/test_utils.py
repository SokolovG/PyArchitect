from pathlib import Path
from typing import cast
from unittest.mock import Mock

from src.generators.utils import (
    AdvancedImportPathGenerator,
    StandardImportPathGenerator,
    FileOperations,
)
from src.preview.collector import PreviewCollector
from src.preview.objects import ComponentType


class TestFileOperations:

    def test_create_file(self, file_ops: FileOperations) -> None:
        test_path = Path("test_dir")

        file_ops.create_directory(test_path)
        file_ops.create_init_file(test_path)

        parent_node = file_ops.preview_collector.nodes[str(test_path)]  # type: ignore
        assert len(parent_node.children) == 1
        file_node = parent_node.children[0]
        assert file_node.name == "__init__.py"
        assert file_node.type == ComponentType.INIT

    def test_create_directory(self, file_ops: FileOperations) -> None:
        test_path = Path("test_directory")

        result = file_ops.create_directory(test_path)

        assert result == test_path
        assert str(test_path) in file_ops.preview_collector.nodes  # type: ignore
        node = file_ops.preview_collector.nodes[str(test_path)]  # type: ignore
        assert node.type == ComponentType.DIRECTORY
        assert node.name == "test_directory"

    def test_write_file(self, file_ops: FileOperations) -> None:
        test_path = Path("test_dir/test_file.py")
        content = "test content"

        file_ops.create_directory(test_path.parent)
        file_ops.write_file(test_path, content)

        parent_node = file_ops.preview_collector.nodes[str(test_path.parent)]  # type: ignore
        assert len(parent_node.children) == 1
        file_node = parent_node.children[0]
        assert file_node.name == "test_file.py"
        assert file_node.type == ComponentType.FILE


class TestImportPathGenerator:

    def test_generate_flat_imports(
        self, import_tuple: tuple, flat_import_gen: StandardImportPathGenerator
    ) -> None:
        root, layer, cont, comp, mod, comp_name = import_tuple
        import_str = flat_import_gen.generate_import_path(
            root, layer, cont, comp, mod, comp_name
        )
        assert (
            import_str
            == "from src.domain.user_context.entities.customer import Customer"
        )

    def test_generate_nested_imports(
        self,
        import_tuple: tuple,
        nested_import_gen: AdvancedImportPathGenerator,
    ) -> None:
        root, layer, cont, comp, mod, comp_name = import_tuple
        import_str = nested_import_gen.generate_import_path(
            root, layer, cont, comp, mod, comp_name
        )
        assert (
            import_str
            == "from src.user_context.domain.entities.customer import Customer"
        )
