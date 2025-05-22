import re
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape


class TemplateEngine:
    """Class for managing Jinja2 template rendering."""

    def __init__(self) -> None:
        """Initialize the template engine."""
        templates_dir = Path(__file__).parent

        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=select_autoescape(),
        )
        self._register_filters()

    def render(self, template_path: str, context: dict[str, Any]) -> str:
        """Render template with provided context.

        Args:
            template_path: Path to template relative to templates directory
            context: Variables to pass to the template

        Returns:
            Rendered template as string

        """
        template = self.env.get_template(template_path)
        content: str = template.render(**context)
        return content

    def template_exists(self, template_path: str) -> bool:
        """Check if a template exists.

        Args:
            template_path: Path to the template

        Returns:
            True if the template exists, False otherwise

        """
        try:
            self.env.get_template(template_path)
            return True
        except TemplateNotFound:
            return False

    def get_template_dir(self, layer_name: str = "") -> str:
        """Get a path to template directory for specific layer.

        Args:
            layer_name: Optional layer name (domain, application, etc.)

        Returns:
            Path to template directory as string

        """
        base_dir = Path(__file__).parent
        if layer_name:
            return str(base_dir / layer_name)
        return str(base_dir)

    @staticmethod
    def _get_article(word: str) -> str:
        """Return 'a' or 'an' based on the word."""
        vowels = "aeiouAEIOU"
        return "an" if word and word[0] in vowels else "a"

    def _register_filters(self) -> None:
        """Register custom Jinja2 filters."""
        self.env.filters["article"] = self._get_article
        self.env.filters["camel_to_snake"] = self.camel_to_snake

    def camel_to_snake(self, component_name: str) -> str:
        """Convert camelCase or PascalCase string to snake_case.

        Args:
            component_name: String in camelCase or PascalCase format

        Returns:
            String converted to snake_case format

        """
        clean_names = []
        list_names = component_name.split(",")
        for name in list_names:
            name = name.strip()
            name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
            clean_names.append(name)

        return ", ".join(clean_names)
