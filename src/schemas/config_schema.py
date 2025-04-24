from pydantic import BaseModel, Field


class StructureSettings(BaseModel):
    flat_domain: bool = False


class NamingSettings(BaseModel):
    entity_suffix: str = ""
    repository_suffix: str = "Repository"
    interface_prefix: str = "I"


class Settings(BaseModel):
    structure: StructureSettings
    naming: NamingSettings


class DomainLayer(BaseModel):
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
    use_cases: str | list[str] = Field(default=list())
    commands: str | list[str] = Field(default=list())
    command_handlers: str | list[str] = Field(default=list())
    queries: str | list[str] = Field(default=list())
    query_handlers: str | list[str] = Field(default=list())
    event_handlers: str | list[str] = Field(default=list())
    validators: str | list[str] = Field(default=list())
    exceptions: str | list[str] = Field(default=list())


class InfrastructureLayer(BaseModel):
    repositories: str | list[str] = Field(default=list())
    models: str | list[str] = Field(default=list())
    adapters: str | list[str] = Field(default=list())
    unit_of_work: str | list[str] = Field(default=list())
    message_bus: str | list[str] = Field(default=list())
    background_tasks: str | list[str] = Field(default=list())


class InterfaceLayer(BaseModel):
    controllers: str | list[str] = Field(default=list())
    dto: str | list[str] = Field(default=list())
    presenters: str | list[str] = Field(default=list())
    api_routes: str | list[str] = Field(default=list())
    middleware: str | list[str] = Field(default=list())
    api_error_handlers: str | list[str] = Field(default=list())


class BoundedContext(BaseModel):
    name: str
    domain: DomainLayer = Field(default_factory=DomainLayer)
    application: ApplicationLayer = Field(default_factory=ApplicationLayer)
    infrastructure: InfrastructureLayer = Field(default_factory=InfrastructureLayer)
    interface: InterfaceLayer = Field(default_factory=InterfaceLayer)


class ConfigModel(BaseModel):
    name: str
    settings: Settings
    contexts: list[BoundedContext]
