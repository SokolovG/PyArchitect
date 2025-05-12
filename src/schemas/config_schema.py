from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class PresetType(str, Enum):
    """Types of configuration presets."""

    SIMPLE = "simple"  # No contexts, simple layers
    STANDARD = "standard"  # Contexts in flat layout
    ADVANCED = "advanced"  # Custom layout


class ContextsLayout(str, Enum):
    """Options for organizing contexts."""

    FLAT = "flat"  # Contexts inside layers
    NESTED = "nested"  # Layers inside contexts


class Settings(BaseModel):
    """Basic Project Settings."""

    preset: PresetType = PresetType.STANDARD

    use_contexts: bool = True
    contexts_layout: ContextsLayout = ContextsLayout.FLAT
    group_components: bool = True
    init_imports: bool = False

    root_name: str = "app"

    domain_layer: str = "domain"
    application_layer: str = "application"
    infrastructure_layer: str = "infrastructure"
    interface_layer: str = "interface"


class LayerConfig(BaseModel):
    """Flexible configuration for any layer.

    This class allows for configuring components of any architectural layer
    with support for dynamic component types and lists.
    """

    model_config = {"extra": "allow"}

    @model_validator(mode="before")
    @classmethod
    def convert_strings_to_lists(cls, values: dict) -> dict:
        """Convert string values to lists.

        Args:
            values: Dictionary with configuration values

        Returns:
            Dictionary with string values converted to single-item lists

        """
        if isinstance(values, dict):
            for key, value in values.items():
                if isinstance(value, str):
                    values[key] = [value]
        return values

    def get_components(self) -> dict[str, list[str]]:
        """Get all components as a dictionary.

        Returns:
            Dictionary mapping component types to lists of component names

        """
        return self.model_dump()


class ConfigModel(BaseModel):
    """The main configuration model.

    Supports all three organization options:
    1. Simple - no contexts (uses the layers field)
    2. Flat - contexts inside layers (uses the layers field)
    3. Nested - layers inside contexts (uses the contexts field)
    """

    settings: Settings = Field(default_factory=Settings)
    layers: LayerConfig

    def model_post_init(self, __context: Any) -> None:  # noqa
        """Apply preset defaults after model initialization.

        This method sets appropriate configuration defaults based on the
        selected preset type, ensuring consistency in the configuration.

        Args:
            __context: Context data from Pydantic (not used)

        """
        if self.layers is None:
            self.layers = LayerConfig()

        if self.settings.preset == PresetType.SIMPLE:
            self.settings.use_contexts = False

        elif self.settings.preset == PresetType.STANDARD:
            self.settings.use_contexts = True
            self.settings.contexts_layout = ContextsLayout.FLAT

        elif self.settings.preset == PresetType.ADVANCED:
            pass
