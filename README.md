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
pybuilder init --preset standard
```

### Advanced Preset
Complex structure with nested contexts:
```bash
pyc init --preset advanced
```

## Configuration

The tool uses YAML configuration files to define your project structure.
Example configurations are provided in the `src/templates/config_templates` directory.

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
