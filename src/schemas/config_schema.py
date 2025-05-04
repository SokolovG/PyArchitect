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

    root_name: str = "src"

    domain_layer: str = "domain"
    application_layer: str = "application"
    infrastructure_layer: str = "infrastructure"
    interface_layer: str = "interface"


class ComponentConfig(BaseModel):
    """Base class for component configurations with string-to-list conversion."""

    @model_validator(mode="before")
    def convert_strings_to_lists(self, values: dict) -> dict:
        """F."""
        if isinstance(values, dict):
            for key, value in values.items():
                if isinstance(value, str):
                    values[key] = [value]
        return values


class DomainLayerConfig(ComponentConfig, extra="allow"):
    use_cases: list[str] = Field(default_factory=lambda: [])
    commands: list[str] = Field(default_factory=lambda: [])
    entities: list[str] = Field(default_factory=lambda: [])
    value_objects: list[str] = Field(default_factory=lambda: [])
    aggregates: list[str] = Field(default_factory=lambda: [])
    repository_interfaces: list[str] = Field(default_factory=lambda: [])
    domain_services: list[str] = Field(default_factory=lambda: [])
    domain_events: list[str] = Field(default_factory=lambda: [])
    factories: list[str] = Field(default_factory=lambda: [])
    specifications: list[str] = Field(default_factory=lambda: [])
    exceptions: list[str] = Field(default_factory=lambda: [])


class ApplicationLayerConfig(ComponentConfig, extra="allow"):
    command_handlers: list[str] = Field(default_factory=lambda: [])
    queries: list[str] = Field(default_factory=lambda: [])
    query_handlers: list[str] = Field(default_factory=lambda: [])
    event_handlers: list[str] = Field(default_factory=lambda: [])
    validators: list[str] = Field(default_factory=lambda: [])
    exceptions: list[str] = Field(default_factory=lambda: [])


class InfrastructureLayerConfig(ComponentConfig, extra="allow"):
    repositories: list[str] = Field(default_factory=lambda: [])
    models: list[str] = Field(default_factory=lambda: [])
    adapters: list[str] = Field(default_factory=lambda: [])
    unit_of_work: list[str] = Field(default_factory=lambda: [])
    message_bus: list[str] = Field(default_factory=lambda: [])
    background_tasks: list[str] = Field(default_factory=lambda: [])


class InterfaceLayerConfig(ComponentConfig, extra="allow"):
    controllers: list[str] = Field(default_factory=lambda: [])
    dto: list[str] = Field(default_factory=lambda: [])
    presenters: list[str] = Field(default_factory=lambda: [])
    api_routes: list[str] = Field(default_factory=lambda: [])
    middleware: list[str] = Field(default_factory=lambda: [])
    api_error_handlers: list[str] = Field(default_factory=lambda: [])


class LayersConfig(BaseModel):
    domain: DomainLayerConfig = Field(default_factory=DomainLayerConfig)
    application: ApplicationLayerConfig = Field(default_factory=ApplicationLayerConfig)
    infrastructure: InfrastructureLayerConfig = Field(default_factory=InfrastructureLayerConfig)
    interface: InterfaceLayerConfig = Field(default_factory=InterfaceLayerConfig)


class ConfigModel(BaseModel):
    """The main configuration model.

    Supports all three organization options:
    1. Simple - no contexts (uses the layers field)
    2. Flat - contexts inside layers (uses the layers field)
    3. Nested - layers inside contexts (uses the contexts field)
    """

    settings: Settings = Field(default_factory=Settings)

    layers: LayersConfig | None = None

    def model_post_init(self, __context: Any) -> None:  # noqa
        """Apply preset defaults."""
        if self.layers is None:
            self.layers = LayersConfig()

        if self.settings.preset == PresetType.SIMPLE:
            self.settings.use_contexts = False

        elif self.settings.preset == PresetType.STANDARD:
            self.settings.use_contexts = True
            self.settings.contexts_layout = ContextsLayout.FLAT

        elif self.settings.preset == PresetType.ADVANCED:
            pass
