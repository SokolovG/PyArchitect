from pydantic import BaseModel, Field


class StructureSettings(BaseModel):
    """Structure settings for the DDD architecture.

    Attributes:
        flat_domain: Whether to use flat domain structure instead of nested
        use_contexts: Whether to use bounded contexts

    """

    flat_domain: bool = False
    use_contexts: bool = True


class LayerNamingSettings(BaseModel):
    """Settings for layer naming in the project.

    Attributes:
        domain_layer: Name for the domain layer directory
        application_layer: Name for the application layer directory
        infrastructure_layer: Name for the infrastructure layer directory
        interface_layer: Name for the interface layer directory

    """

    domain_layer: str = "domain"
    application_layer: str = "application"
    infrastructure_layer: str = "infrastructure"
    interface_layer: str = "interface"


class NamingSettings(BaseModel):
    """General naming settings for project components.

    Attributes:
        root_name: Name of the root directory for generated code
        entity_suffix: Suffix for entity classes
        repository_suffix: Suffix for repository classes
        interface_prefix: Prefix for interface classes

    """

    root_name: str = "src"
    entity_suffix: str = ""
    repository_suffix: str = "Repository"
    interface_prefix: str = "I"


class Settings(BaseModel):
    """Combined settings for the project generation.

    Attributes:
        structure: Settings for project structure
        naming: Settings for component naming
        layer_naming: Settings for layer directories naming

    """

    structure: StructureSettings
    naming: NamingSettings
    layer_naming: LayerNamingSettings = Field(default_factory=LayerNamingSettings)


class DomainLayer(BaseModel):
    """Configuration for the domain layer components.

    Attributes:
        entities: Entity classes to generate
        value_objects: Value object classes to generate
        aggregates: Aggregate root classes to generate
        repository_interfaces: Repository interface classes to generate
        domain_services: Domain service classes to generate
        domain_events: Domain event classes to generate
        factories: Factory classes to generate
        specifications: Specification pattern classes to generate
        exceptions: Domain exception classes to generate

    """

    entities: str | list[str] = Field(default=list())
    value_objects: str | list[str] = Field(default=list())
    aggregates: str | list[str] = Field(default=list())
    repository_interfaces: str | list[str] = Field(default=list())
    domain_services: str | list[str] = Field(default=list())
    domain_events: str | list[str] = Field(default=list())
    factories: str | list[str] = Field(default=list())
    specifications: str | list[str] = Field(default=list())
    exceptions: str | list[str] = Field(default=list())


class ApplicationLayer(BaseModel):
    """Configuration for the application layer components.

    Attributes:
        use_cases: Use case classes to generate
        commands: Command classes to generate
        command_handlers: Command handler classes to generate
        queries: Query classes to generate
        query_handlers: Query handler classes to generate
        event_handlers: Event handler classes to generate
        validators: Validator classes to generate
        exceptions: Application exception classes to generate

    """

    use_cases: str | list[str] = Field(default=list())
    commands: str | list[str] = Field(default=list())
    command_handlers: str | list[str] = Field(default=list())
    queries: str | list[str] = Field(default=list())
    query_handlers: str | list[str] = Field(default=list())
    event_handlers: str | list[str] = Field(default=list())
    validators: str | list[str] = Field(default=list())
    exceptions: str | list[str] = Field(default=list())


class InfrastructureLayer(BaseModel):
    """Configuration for the infrastructure layer components.

    Attributes:
        repositories: Repository implementation classes to generate
        models: ORM model classes to generate
        adapters: Adapter pattern implementation classes to generate
        unit_of_work: Unit of work implementation classes to generate
        message_bus: Message bus implementation classes to generate
        background_tasks: Background task classes to generate

    """

    repositories: str | list[str] = Field(default=list())
    models: str | list[str] = Field(default=list())
    adapters: str | list[str] = Field(default=list())
    unit_of_work: str | list[str] = Field(default=list())
    message_bus: str | list[str] = Field(default=list())
    background_tasks: str | list[str] = Field(default=list())


class InterfaceLayer(BaseModel):
    """Configuration for the interface layer components.

    Attributes:
        controllers: Controller classes to generate
        dto: Data Transfer Object classes to generate
        presenters: Presenter classes to generate
        api_routes: API route definitions to generate
        middleware: Middleware classes to generate
        api_error_handlers: Error handler classes to generate

    """

    controllers: str | list[str] = Field(default=list())
    dto: str | list[str] = Field(default=list())
    presenters: str | list[str] = Field(default=list())
    api_routes: str | list[str] = Field(default=list())
    middleware: str | list[str] = Field(default=list())
    api_error_handlers: str | list[str] = Field(default=list())


class BoundedContext(BaseModel):
    """Configuration for a bounded context.

    Attributes:
        name: Name of the bounded context
        domain: Domain layer configuration for this context
        application: Application layer configuration for this context
        infrastructure: Infrastructure layer configuration for this context
        interface: Interface layer configuration for this context

    """

    name: str
    domain: DomainLayer = Field(default_factory=DomainLayer)
    application: ApplicationLayer = Field(default_factory=ApplicationLayer)
    infrastructure: InfrastructureLayer = Field(default_factory=InfrastructureLayer)
    interface: InterfaceLayer = Field(default_factory=InterfaceLayer)


class ConfigModel(BaseModel):
    """Main configuration model for the PyArchitect.

    Attributes:
        settings: Project generation settings
        contexts: List of bounded contexts to generate
        layer_naming: Custom naming for architecture layers

    """

    settings: Settings
    contexts: list[BoundedContext]
    layer_naming: LayerNamingSettings = Field(default_factory=LayerNamingSettings)
