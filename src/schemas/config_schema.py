from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


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

    root_name: str = "app"

    domain_layer: str = "domain"
    application_layer: str = "application"
    infrastructure_layer: str = "infrastructure"
    interface_layer: str = "interface"


class DomainLayerConfig(BaseModel, extra="allow"):
    use_cases: list[str] | None = Field(default_factory=lambda: [])
    commands: list[str] | None = Field(default_factory=lambda: [])
    entities: list[str] | None = Field(default_factory=lambda: [])
    value_objects: list[str] | None = Field(default_factory=lambda: [])
    aggregates: list[str] | None = Field(default_factory=lambda: [])
    repository_interfaces: list[str] | None = Field(default_factory=lambda: [])
    domain_services: list[str] | None = Field(default_factory=lambda: [])
    domain_events: list[str] | None = Field(default_factory=lambda: [])
    factories: list[str] | None = Field(default_factory=lambda: [])
    specifications: list[str] | None = Field(default_factory=lambda: [])
    exceptions: list[str] | None = Field(default_factory=lambda: [])


class ApplicationLayerConfig(BaseModel, extra="allow"):
    command_handlers: list[str] | None = Field(default_factory=lambda: [])
    queries: list[str] | None = Field(default_factory=lambda: [])
    query_handlers: list[str] | None = Field(default_factory=lambda: [])
    event_handlers: list[str] | None = Field(default_factory=lambda: [])
    validators: list[str] | None = Field(default_factory=lambda: [])
    exceptions: list[str] | None = Field(default_factory=lambda: [])


class InfrastructureLayerConfig(BaseModel, extra="allow"):
    repositories: list[str] | None = Field(default_factory=lambda: [])
    models: list[str] | None = Field(default_factory=lambda: [])
    adapters: list[str] | None = Field(default_factory=lambda: [])
    unit_of_work: list[str] | None = Field(default_factory=lambda: [])
    message_bus: list[str] | None = Field(default_factory=lambda: [])
    background_tasks: list[str] | None = Field(default_factory=lambda: [])


class InterfaceLayerConfig(BaseModel, extra="allow"):
    controllers: list[str] | None = Field(default_factory=lambda: [])
    dto: list[str] | None = Field(default_factory=lambda: [])
    presenters: list[str] | None = Field(default_factory=lambda: [])
    api_routes: list[str] | None = Field(default_factory=lambda: [])
    middleware: list[str] | None = Field(default_factory=lambda: [])
    api_error_handlers: list[str] | None = Field(default_factory=lambda: [])


class ContextConfig(BaseModel, extra="allow"):
    name: str
    domain: DomainLayerConfig | None = None
    application: ApplicationLayerConfig | None = None
    infrastructure: InfrastructureLayerConfig | None = None
    interface: InterfaceLayerConfig | None = None


class LayersConfig(BaseModel):
    domain: DomainLayerConfig | None = None
    application: ApplicationLayerConfig | None = None
    infrastructure: InfrastructureLayerConfig | None = None
    interface: InterfaceLayerConfig | None = None


class ConfigModel(BaseModel):
    """The main configuration model.

    Supports all three organization options:
    1. Simple - no contexts (uses the layers field)
    2. Flat - contexts inside layers (uses the layers field)
    3. Nested - layers inside contexts (uses the contexts field)
    """

    settings: Settings = Field(default_factory=Settings)

    layers: LayersConfig | None = None

    contexts: list[ContextConfig] | None

    def model_post_init(self, __context: Any) -> None:  # noqa
        """Apply preset defaults."""
        if self.settings.preset == PresetType.SIMPLE:
            self.settings.use_contexts = False

        elif self.settings.preset == PresetType.STANDARD:
            self.settings.use_contexts = True
            self.settings.contexts_layout = ContextsLayout.FLAT

        elif self.settings.preset == PresetType.ADVANCED:
            pass

    def get_structure_type(self) -> str:
        """Determine the type of structure based on the settings."""
        if not self.settings.use_contexts:
            return "simple"
        elif self.settings.contexts_layout == ContextsLayout.FLAT:
            return "flat"
        else:
            return "nested"
