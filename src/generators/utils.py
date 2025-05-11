import re
from pathlib import Path


def camel_to_snake(component_name: str) -> str:
    """Convert camelCase or PascalCase string to snake_case.

    Args:
        component_name: String in camelCase or PascalCase format

    Returns:
        String converted to snake_case format

    """
    clean_names = []
    list_names = component_name.split(",")
    for name in list_names:
        name = name.strip()
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        clean_names.append(name)

    return ", ".join(clean_names)
