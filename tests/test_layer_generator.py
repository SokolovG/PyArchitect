import tempfile
from pathlib import Path

from src.core.template_engine import TemplateEngine
from src.generators.layer_generator import LayerGenerator


class TestLayerGenerator:

    def test_generate_component(self, layer_generator: LayerGenerator) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "entities"
            component_dir.mkdir()
            module_name = layer_generator.generate_component(
                path=component_dir, component_type="entities", component_name="User"
            )

            expected_file = component_dir / "user_entity.py"
            content = expected_file.read_text()

            assert module_name == "user_entity"
            assert expected_file.exists()
            assert expected_file.is_file()

            assert "class User:" in content
            assert "This class represents" in content

    def test_generate_component_with_suffix(
        self, layer_generator: LayerGenerator
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "repositories"
            component_dir.mkdir()

            module_name = layer_generator.generate_component(
                path=component_dir,
                component_type="repositories",
                component_name="UserRepository",
            )
            expected_file = component_dir / "user_repository.py"
            content = expected_file.read_text()

            assert module_name == "user_repository"
            assert expected_file.exists()
            assert "class UserRepository:" in content

    def test_grouped_components(self, grouped_layer_generator: LayerGenerator) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "entities"
            component_dir.mkdir()

            components = ["User", "Admin", "Customer"]
            result = grouped_layer_generator.generate_components(
                component_dir=component_dir,
                component_type="entities",
                components=components,
            )

            expected_result = {
                "User": "entities",
                "Admin": "entities",
                "Customer": "entities",
            }
            expected_file = component_dir / "entities.py"
            content = expected_file.read_text()

            assert result == expected_result
            assert expected_file.exists()

            assert "class User:" in content
            assert "class Admin:" in content
            assert "class Customer:" in content

    def test_individual_components(self, layer_generator: LayerGenerator) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "entities"
            component_dir.mkdir()

            components = ["User", "Product"]
            result = layer_generator.generate_components(
                component_dir=component_dir,
                component_type="entities",
                components=components,
            )

            expected_result = {"User": "user_entity", "Product": "product_entity"}

            user_file = component_dir / "user_entity.py"
            product_file = component_dir / "product_entity.py"
            user_content = user_file.read_text()
            product_content = product_file.read_text()

            assert user_file.exists()
            assert product_file.exists()
            assert result == expected_result

            assert "class User:" in user_content
            assert "class Product:" in product_content

    def test_init_imports(self, grouped_layer_generator: LayerGenerator) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "entities"
            component_dir.mkdir()

            grouped_layer_generator.init_imports = True

            components = ["User", "Product"]
            grouped_layer_generator.generate_components(
                component_dir=component_dir,
                component_type="entities",
                components=components,
            )

            init_file = component_dir / "__init__.py"
            init_content = init_file.read_text()

            assert init_file.exists()
            assert "import" in init_content
            assert "__all__" in init_content
            assert "User" in init_content
            assert "Product" in init_content

    def test_empty_components(self, template_engine: TemplateEngine) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "entities"
            component_dir.mkdir()

            layer_generator = LayerGenerator(
                template_engine=template_engine,
                root_name="test_app",
                layer_name="domain",
                group_components=False,
                init_imports=False,
            )

            test_cases: list = [None, []]

            for empty_components in test_cases:
                for file in component_dir.glob("*.py"):
                    file.unlink()

                result = layer_generator.generate_components(
                    component_dir=component_dir,
                    component_type="entities",
                    components=empty_components,
                )

                files_in_dir = list(component_dir.glob("*.py"))

                assert result == {}
                assert len(files_in_dir) == 0

            for file in component_dir.glob("*.py"):
                file.unlink()

            result = layer_generator.generate_components(
                component_dir=component_dir,
                component_type="entities",
                components="",
            )

            assert result == {}

    def test_string_components_parsing(self, layer_generator: LayerGenerator) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "entities"
            component_dir.mkdir()

            components_string = "User, Product,  Category,   Order"
            result = layer_generator.generate_components(
                component_dir=component_dir,
                component_type="entities",
                components=components_string,
            )
            expected_files = [
                "user_entity.py",
                "product_entity.py",
                "category_entity.py",
                "order_entity.py",
            ]

            assert len(result) == 4
            assert "User" in result
            assert "Product" in result
            assert "Category" in result
            assert "Order" in result

            for file_name in expected_files:
                file_path = component_dir / file_name
                assert file_path.exists(), f"File {file_name} should exist"

    def test_file_naming_edge_cases(self, layer_generator: LayerGenerator) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            test_cases = [
                ("User", "entities", "user_entity", "user_entity.py"),
                ("UserService", "services", "user_service", "user_service.py"),
                ("EmailService", "services", "email_service", "email_service.py"),
                (
                    "Repository",
                    "repositories",
                    "repository_repository",
                    "repository_repository.py",
                ),
                (
                    "UserRepo",
                    "repositories",
                    "user_repo_repository",
                    "user_repo_repository.py",
                ),
            ]

            for (
                component_name,
                component_type,
                expected_module,
                expected_file,
            ) in test_cases:
                component_dir = base_dir / component_type / component_name
                component_dir.mkdir(parents=True)

                result = layer_generator.generate_component(
                    path=component_dir,
                    component_type=component_type,
                    component_name=component_name,
                )
                expected_file_path = component_dir / expected_file
                content = expected_file_path.read_text()

                assert (
                    result == expected_module
                ), f"Failed module name for {component_name} in {component_type}"

                assert (
                    expected_file_path.exists()
                ), f"File {expected_file} should exist for {component_name}"

                assert f"class {component_name}:" in content

    def test_directory_creation(self, layer_generator: LayerGenerator) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            component_dir = Path(temp_dir) / "domain" / "entities"
            component_dir.mkdir(parents=True)

            layer_generator.generate_component(
                path=component_dir, component_type="entities", component_name="User"
            )
            user_file = component_dir / "user_entity.py"

            assert component_dir.exists()
            assert component_dir.is_dir()
            assert user_file.exists()
