# PyArchitect

PyArchitect is a CLI tool that helps developers quickly create a project structure that follows Domain-Driven Design (DDD) principles. The tool generates architecture based on a YAML configuration that defines bounded contexts, entities, repositories, services, use cases, and other DDD elements.

## Overview

PyArchitect simplifies the process of setting up a DDD architecture in Python projects. It allows you to create a structured project with domain, application, infrastructure, and interface layers, all configurable through a YAML file.

### Features

- **Configurable Architecture**: Define your project structure using a YAML configuration file.
- **Layer Generation**: Generate components for domain, application, infrastructure, and interface layers.
- **Bounded Contexts**: Support for bounded contexts to organize your project effectively.
- **Customizable Naming**: Configure naming conventions for components and directories.
- **Multiple Presets**: Choose from Simple, Standard, or Advanced presets based on your project needs.
- **Component Addition**: Add new components to an existing project structure.

## Installation

To install PyArchitect, you can use pip:

```bash
pip install pyarchitect
```

### Installation from source

```bash
git clone https://github.com/yourusername/pyarchitect.git
cd pyarchitect
```

## Usage

### Initialize a new project

```bash
pyarchitect init --config ddd-config.yaml
```


## Configuration

PyArchitect uses YAML configuration files to define the structure of your project. Here are some examples for different presets:

### Simple Configuration Example

```yaml
settings:
  preset: "simple"
  generate_all_exports: True

layers:
  domain:
    entities: User, Admin
    value_objects: Email, Password
  application:
    exceptions: UserNotFoundException, UserBlockedException
  infrastructure:
    repositories: UserRepository, AdminRepository
  interface:
    controllers: UserController, AdminController
```

### Advanced Configuration Example

```yaml
settings:
  preset: "advanced"
  structure:
    use_contexts: true
    contexts_layout: "nested"

contexts:
  - name: user_context
    domain:
      entities: [User]
      value_objects: [Email]
    application:
      use_cases: [CreateUser]
    infrastructure:
      repositories: [UserRepository]

  - name: payment_context
    domain:
      entities: [Payment]
    application:
      use_cases: [ProcessPayment]
```

### Standard Configuration Example

```yaml
settings:
  preset: "standard"

layers:
  domain:
    contexts:
      - name: user
        entities: [User, Profile]
        value_objects: [Email, Password]
        repositories: [UserRepository]
      - name: catalog
        entities: [Product, Category]
        repositories: [ProductRepository]

  application:
    contexts:
      - name: user
        use_cases: [RegisterUser, LoginUser]
      - name: catalog
        use_cases: [ListProducts, SearchProducts]
```

## Presets

PyArchitect offers three different presets to accommodate various project sizes and complexity levels:

### Simple Preset

The Simple preset creates a flat structure without bounded contexts. It's ideal for smaller projects or when you're just getting started with DDD. All components are organized directly under their respective layers.

Structure example:
```
app/
├── domain/
│   ├── entities/
│   │   └── user.py
│   └── value_objects/
│       └── email.py
├── application/
│   └── exceptions/
│       └── user_not_found_exception.py
├── infrastructure/
│   └── repositories/
│       └── user_repository.py
└── interface/
    └── controllers/
        └── user_controller.py
```

### Standard Preset

The Standard preset organizes components with bounded contexts in a flat layout. Contexts are organized within layers, making it suitable for medium-sized projects with clear domain boundaries.

Structure example:
```
app/
├── domain/
│   ├── user/
│   │   ├── entities/
│   │   │   └── user.py
│   │   └── value_objects/
│   │       └── email.py
│   └── catalog/
│       └── entities/
│           └── product.py
├── application/
│   └── user/
│       └── use_cases/
│           └── register_user.py
└── ...
```

### Advanced Preset

The Advanced preset provides flexible organization options, including nested contexts with layers inside each context. This is ideal for complex projects with many bounded contexts that need clear separation.

Structure example:
```
app/
├── user_context/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── user.py
│   │   └── value_objects/
│   │       └── email.py
│   ├── application/
│   │   └── use_cases/
│   │       └── create_user.py
│   └── infrastructure/
│       └── repositories/
│           └── user_repository.py
└── payment_context/
    ├── domain/
    │   └── entities/
    │       └── payment.py
    └── ...
```


## Generated Structure

Here's a comprehensive example of what PyArchitect can generate for a standard DDD architecture:

```
app/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── aggregates/
│   ├── repositories/  # interfaces
│   ├── services/
│   ├── exceptions/
│   ├── events/
│   ├── factories/
│   └── specifications/
├── application/
│   ├── use_cases/
│   ├── commands/
│   ├── command_handlers/
│   ├── queries/
│   ├── query_handlers/
│   ├── event_handlers/
│   ├── validators/
│   └── exceptions/
├── infrastructure/
│   ├── repositories/  # implementations
│   ├── models/
│   ├── adapters/
│   ├── unit_of_work/
│   ├── message_bus/
│   └── background_tasks/
└── interface/
    ├── controllers/
    ├── dto/
    ├── presenters/
    ├── api_routes/
    ├── middleware/
    └── api_error_handlers/
```

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Create a new Pull Request


## License

This project is licensed under the MIT License - see the LICENSE file for details.
