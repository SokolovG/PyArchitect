import re
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape


class TemplateEngine:
    """Manages Jinja2 template rendering and custom filters.

    This class handles template loading, rendering, and provides custom filters
    for template processing.
    """

    def __init__(self) -> None:
        """Initialize the template engine with default configuration.

        Sets up the Jinja2 environment with template directory and custom filters.
        """
        templates_dir = Path(__file__).parent.parent / "templates"

        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=select_autoescape(),
        )
        self._register_filters()

    def render(self, template_path: str, context: dict[str, Any]) -> str:
        """Render a template with the provided context.

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
        """Check if a template exists in the template directory.

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
        """Get the path to template directory for a specific layer.

        Args:
            layer_name: Optional layer name (domain, app, etc.)

        Returns:
            Path to template directory as string

        """
        base_dir = Path(__file__).parent
        if layer_name:
            return str(base_dir / layer_name)
        return str(base_dir)

    @staticmethod
    def _get_article(word: str) -> str:
        """Determine the appropriate article ('an' or 'an') for a word.

        Args:
            word: Word to determine article for

        Returns:
            'an' if word starts with a vowel, 'a' otherwise

        """
        vowels = "aeiouAEIOU"
        return "an" if word and word[0] in vowels else "a"

    def _register_filters(self) -> None:
        """Register custom Jinja2 filters for template processing.

        Registers filters for article determination and case conversion.
        """
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
