import logging
import sys
from pathlib import Path

import click
import pydantic

from src.core import container
from src.core.exceptions import YamlParseError
from src.core.parser import YamlParser
from src.generators import ProjectGenerator

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)


logger = logging.getLogger(__name__)


@click.group()
def cli() -> None:
    """Entry point for the app."""


@click.command()
@click.option("-p", "--preset", default="standard", help="Preset selection.")
def init(preset: str) -> None:
    """Generate basic example based on preset."""


@click.command()
@click.option("-f", "--file", help="Path to YAML file.")
def validate(file: str | None = None) -> None:
    """Validate YAML config."""
    click.echo("Starting validation...")
    parser = container.get(YamlParser)
    try:
        if file:
            file_path = Path(file)
            parser.load(file_path)
        else:
            parser.load()
        click.echo("✓ Configuration validated successfully")
    except YamlParseError as error:
        click.echo(f"✗ {error}", err=True)
    except pydantic.ValidationError as error:
        click.echo(f"✗ Configuration invalid: {error}", err=True)
        click.echo("Hint: Check the documentation for correct configuration format")


@click.command()
@click.option("-f", "--file", help="Path to YAML file.")
def preview(file: str | None = None) -> None:
    """Preview future structure."""


@click.command()
@click.option()
def add() -> None:
    """Add component."""


@click.command()
@click.option("-f", "--file", help="Path to YAML file.")
def update(file: str | None = None) -> None:
    """Update structure."""


@click.command()
@click.option("-f", "--file", help="Path to YAML file.")
def run(file: str | None = None) -> None:
    """Generate structure for the app."""
    try:
        path = Path(file) if file else None

        if path and not path.exists():
            click.echo(f"Error: Config file not found: {file}", err=True)
            return

        click.echo("Project generation started.")

        generator = container.get(ProjectGenerator)
        generator.generate()

        click.echo("Project generation completed successfully.")

    except Exception as error:
        logger.error(f"Error during project generation: {error}")
        click.echo(f"Error: {error}", err=True)


cli.add_command(run)
cli.add_command(init)
cli.add_command(validate)
cli.add_command(preview)
cli.add_command(add)
cli.add_command(update)

if __name__ == "__main__":
    cli()
