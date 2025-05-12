# PyArchitect

## English

### Overview

PyArchitect is a tool designed to generate DDD (Domain-Driven Design) architecture components based on configuration. It allows you to create a structured project with domain, application, infrastructure, and interface layers, all configurable through a YAML file.

### Features

- **Configurable Architecture**: Define your project structure using a YAML configuration file.
- **Layer Generation**: Generate components for domain, application, infrastructure, and interface layers.
- **Bounded Contexts**: Support for bounded contexts to organize your project effectively.
- **Customizable Naming**: Configure naming conventions for components and directories.

### Installation

To install PyArchitect, you can use pip:

```bash
pip install pyarchitect
```

### Usage

1. Create a configuration file (e.g., `ddd-config.yaml`) with your project settings.
2. Run the generator:

```bash
python -m src.main
```

### Configuration Example

Here's an example of a configuration file:

```yaml
settings:
  structure:
    flat_domain: false
    use_contexts: true

  naming:
    root_name: app
    entity_suffix: ""
    repository_suffix: "Repository"
    interface_prefix: "I"

  layer_naming:
    domain_layer: "domain"
    application_layer: "application"
    infrastructure_layer: "infrastructure"
    interface_layer: "interface"

contexts:
  - name: user_context
    domain:
      entities: [User, UserProfile]
      value_objects: [Email, UserId]
      aggregates: [UserAggregate]
      repository_interfaces: [IUserRepository]
      domain_services: [UserDomainService]
      domain_events: [UserCreatedEvent, UserUpdatedEvent]
      factories: [UserFactory]
      specifications: [ActiveUserSpecification]
      exceptions: [UserDomainException, InvalidEmailException]
    application:
      use_cases: [CreateUserUseCase, UpdateUserUseCase]
      commands: [CreateUserCommand, UpdateUserCommand]
      command_handlers: [CreateUserCommandHandler, UpdateUserCommandHandler]
      queries: [GetUserQuery, ListUsersQuery]
      query_handlers: [GetUserQueryHandler, ListUsersQueryHandler]
      event_handlers: [UserCreatedEventHandler]
      validators: [CreateUserValidator]
      exceptions: [UserApplicationException]
    infrastructure:
      repositories: [UserRepository]
      models: [User, UserProfile]
      adapters: [EmailServiceAdapter]
      unit_of_work: [UserUnitOfWork]
      message_bus: [EventBus]
      background_tasks: [EmailNotificationTask]
    interface:
      controllers: [UserController]
      dto: [CreateUserDto, UserResponseDto]
      presenters: [UserPresenter]
      api_routes: [user_routes]
      middleware: [AuthMiddleware]
      api_error_handlers: [UserErrorHandler]
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License
