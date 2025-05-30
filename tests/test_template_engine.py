import pytest
from jinja2 import TemplateNotFound

from src.core.template_engine import TemplateEngine


class TestTemplateEngine:

    def test_find_and_load_templates(self, template_engine: TemplateEngine) -> None:
        template = template_engine.env.get_template("base_template.py.jinja")
        assert template is not None
        assert template_engine.env is not None
        assert "article" in template_engine.env.filters
        assert "camel_to_snake" in template_engine.env.filters

    def test_render_template(self, template_engine: TemplateEngine) -> None:
        content = template_engine.render(
            "base_template.py.jinja",
            {
                "name": "UserService",
                "type": "user",
            },
        )
        assert "class UserService" in content

    def test_template_exists(self, template_engine: TemplateEngine) -> None:
        template_path = "base_template.py.jinja"
        template_not_exits_path = "base_template_not_exists.py.jinja"
        assert template_engine.template_exists(template_path) == True
        assert template_engine.template_exists(template_not_exits_path) == False

    def test_template_errors(self, template_engine: TemplateEngine) -> None:
        with pytest.raises(TemplateNotFound):
            template_engine.render("nonexistent.jinja", {})

    def test_camel_to_snake(
        self, camel_snake_tuple: tuple[str, str], template_engine: TemplateEngine
    ) -> None:
        camel_str, snake_str = camel_snake_tuple
        str = template_engine.camel_to_snake(camel_str)
        assert str == snake_str

    def test_articles(self, template_engine: TemplateEngine) -> None:
        vowel_word = "appel"
        consonant_word = "ball"
        vowel_article = template_engine._get_article(vowel_word)
        consonant_article = template_engine._get_article(consonant_word)
        assert vowel_article == "an"
        assert consonant_article == "a"
