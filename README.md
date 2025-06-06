# PyConstructor 🏗️

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

PyConstructor is a command-line tool
that helps developers quickly create a project structure following Domain-Driven Design
(DDD) principles.
The tool generates architecture based on a YAML configuration that defines bounded contexts,
entities, repositories, services, use cases, and other DDD elements.

## 🚀 Quick Start

### Installation

```bash
# Install via pip
pip install pyconstructor
# Install via uv
uv add pyconstructor

# Generate YAML file with example data
pyc init

# Edit the generated ddd-config.yaml file
# ...

# Generate structure
pyc run
```

### Basic Usage

1. Initialize a new project with a preset configuration:
```bash
pyc init --preset <PresetType(Optional argument, default to Standard)>
```

2. Validate your configuration  (Optional command):
```bash
pyc validate
```

3. Preview the project structure (Optional command):
```bash
pyc preview --file <file_name> (Optional argument)
```

4. Generate the project:
```bash
pyc run --file <file_name> (Optional argument)
```

## 📋 Available Commands

### Core Commands

| Command    | Description                                            | Example                                  |
|------------|--------------------------------------------------------|------------------------------------------|
| `init`     | Initialize a new project with a preset configuration   | `pyc init --preset standard`             |
| `validate` | Validate your YAML configuration                       | `pyc validate --file custom-config.yaml` |
| `preview`  | Preview the project structure without generating files | `pyc preview --file custom-config.yaml`  |
| `run`      | Generate the project structure                         | `pyc run --file custom-config.yaml`      |

### Command Options

#### `init` Command
```bash
# Create project with standard preset
pyc init --preset standard

# Force overwrite existing config
pyc init --preset standard --force
```

#### `validate` Command
```bash
# Validate default config (ddd-config.yaml)
pyc validate

# Validate specific config file
pyc validate --file custom-config.yaml
```

#### `preview` Command
```bash
# Preview default config
pyc preview

# Preview specific config
pyc preview --file custom-config.yaml
```
**Output:**
- Displays the project structure tree in the console
- Generates a `structure.md` file with the same tree view for future reference

**Example output:**

```aiignore
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
└── infrastructure/
    └── repositories/
        └── user_repository.py
```

#### `run` Command
```bash
# Generate from default config
pyc run

# Generate from specific config
pyc run --file custom-config.yaml
```

## Architecture Presets

PyConstructor comes with three built-in presets:

### Simple Preset
Basic DDD structure without bounded contexts:
```bash
pyc init --preset simple
```

### Standard Preset
Default preset with bounded contexts:
```bash
pyc init --preset standard
```

### Advanced Preset
Complex structure with nested contexts:
```bash
pyc init --preset advanced
```

## Configuration

The tool uses YAML configuration files to define your project structure.
Example configurations are provided in the `src/templates/config_templates` directory.

### Configuration Reference

#### Settings Section
```yaml
settings:
  preset: "standard"  # One of: "simple", "standard", "advanced"
  use_contexts: true  # Whether to use bounded contexts
  contexts_layout: "flat"  # One of: "flat", "nested"
  group_components: true  # Group similar components in directories
  init_imports: false  # Initialize imports in __init__.py files
  root_name: "src"  # Root directory name
```
### Simple Configuration Example
```yaml
settings:
  preset: "simple"

layers:
  domain:
    entities: User, Product
    value_objects: Email, Price
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
      - name: catalog
        entities: [Product, Category]
```

### Advanced Configuration Example (for microservice architecture)

```yaml
settings:
  preset: "advanced"

layers:
  contexts:
    - name: user_context
      domain:
        entities: User
        value_objects: Email
      application:
        use_cases: CreateUser
      infrastructure:
        repositories: UserRepository

    - name: payment_context
      domain:
        entities: Payment
      application:
        use_cases: ProcessPayment
      infrastructure:
        repositories: TransactionRepository

```

### Complete Configuration Example
Here's a complete example showing all available options:

```yaml
settings:
  preset: "advanced"
  use_contexts: true
  contexts_layout: "nested"
  group_components: true
  init_imports: true
  root_name: "src"

layers:
  contexts:
    - name: user_context
      domain:
        entities: User, Profile
        value_objects: Email, Password, UserRole
        aggregates: UserAggregate
        repositories: UserRepository
        services: UserService
      application:
        use_cases: CreateUser, UpdateUser, DeleteUser
        commands: CreateUserCommand, UpdateUserCommand
        queries: GetUserQuery, ListUsersQuery
        events: UserCreatedEvent, UserUpdatedEvent
        dtos: UserDTO, UserCreateDTO
        mappers: UserMapper
      infrastructure:
        repositories: UserRepositoryImpl
        services: UserServiceImpl
      interface:
        controllers: [UserController]
        middleware: AuthMiddleware

    - name: order_context
      domain:
        entities: Order, OrderItem
        value_objects: Money, OrderStatus
        aggregates: OrderAggregate
        repositories: OrderRepository
        services: OrderService
      application:
        use_cases: CreateOrder, UpdateOrder
        commands: CreateOrderCommand
        queries: GetOrderQuery
        events: OrderCreatedEvent
        dtos: OrderDTO
        mappers: OrderMapper
      infrastructure:
        repositories: OrderRepositoryImpl
      interface:
        controllers: OrderController
```

### Generated Structure
When using the advanced configuration above, the tool will generate a structure like this:

```
src/
├── user_context/
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── user.py
│   │   │   └── profile.py
│   │   ├── value_objects/
│   │   │   ├── email.py
│   │   │   ├── password.py
│   │   │   └── user_role.py
│   │   ├── aggregates/
│   │   │   └── user_aggregate.py
│   │   ├── repositories/
│   │   │   └── user_repository.py
│   │   └── services/
│   │       └── user_service.py
│   ├── application/
│   │   ├── use_cases/
│   │   │   ├── create_user.py
│   │   │   ├── update_user.py
│   │   │   └── delete_user.py
│   │   ├── commands/
│   │   │   ├── create_user_command.py
│   │   │   └── update_user_command.py
│   │   ├── queries/
│   │   │   ├── get_user_query.py
│   │   │   └── list_users_query.py
│   │   ├── events/
│   │   │   ├── user_created_event.py
│   │   │   └── user_updated_event.py
│   │   ├── dtos/
│   │   │   ├── user_dto.py
│   │   │   └── user_create_dto.py
│   │   └── mappers/
│   │       └── user_mapper.py
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   └── user_repository_impl.py
│   │   └── services/
│   │       └── user_service_impl.py
│   └── interface/
│       ├── controllers/
│       │   └── user_controller.py
│       └── middleware/
│           └── auth_middleware.py
└── order_context/
    └── ... (similar structure)
```

### Customizing Templates
You can customize the generated files by modifying the templates in the `src/templates` directory. Each component type has its own template file that you can modify to suit your needs.

### FAQ

## Getting Started

**Q: Which preset should I choose for my project?**
A:
- **Simple**: Perfect for learning DDD or small projects without complex contexts
- **Standard**: Best for most real-world projects with clear bounded contexts
- **Advanced**: Use for microservices architecture or when you need maximum flexibility

**Q: What happens if files already exist in my project?**
A: PyConstructor **adds new files and directories** to your existing structure without touching existing files. This means:
- New components will be created alongside existing ones
- Existing `__init__.py` files won't be modified
- You can safely run it on existing projects

**Q: Can I see what will be generated before actually creating files?**
A: Yes! Use the preview command:
```bash
pyc preview
# or
pyc preview --file your-config.yaml

```
This shows the complete directory structure in console and generates a `structure.md` file.

## Configuration

**Q: How do I add more components after initial generation?**
A: Simply:
1. Edit your YAML configuration file to add new components
2. Run `pyc run` again - it will add only the new components
3. Existing files remain untouched

**Q: Can I customize the generated code templates?**
A: Yes, but it's not officially supported yet. Templates are located in `src/templates/`. Modifying them directly will affect all generations. Official template customization API is planned.

**Q: What's the difference between 'flat' and 'nested' context layouts?**
A:
- **Flat**: `src/domain/user_context/entities/` (contexts inside layers)
- **Nested**: `src/user_context/domain/entities/` (layers inside contexts)

## Troubleshooting

**Q: I get "Configuration file not found" error**
A: Make sure you have a `ddd-config.yaml` file in your current directory, or specify the path:
```bash
pyc run --file path/to/your/config.yaml
```

**Q: YAML validation fails with cryptic errors**
A: Common issues:
- Incorrect indentation (use spaces, not tabs)
- Missing quotes around special characters
- Empty values should be written as `[]` or omitted entirely

**Q: Generated code doesn't follow my coding standards**
A: Currently, PyConstructor generates basic templates. You can:
- Modify templates in `src/templates/` (advanced users)
- Use code formatters (black, ruff) after generation

## Integration

**Q: Can I use this with existing projects?**
A: Yes! PyConstructor safely adds new structure to existing projects:
- Creates new directories and files without touching existing ones
- Preserves your current codebase
- Perfect for gradually introducing DDD structure
- Just make sure your config doesn't conflict with existing file names

## Roadmap & Limitations

**Q: What features are planned for future releases?**
A:
- Custom template support
- Framework-specific generators (FastAPI, Django)
- Interactive configuration builder
- Migration tools for existing codebases
- Advanced DDD patterns support

## 🤝 Contributing

Contributions are welcome. Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git switch -c feature/amazing-feature`)
3. Run tests (`pytest`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License—see the [LICENSE](LICENSE) file for details.

## 👤 Author

Grigoriy Sokolov (Sokolov_Gr@proton.me)
