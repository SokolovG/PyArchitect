import logging
import sys
from pathlib import Path

import click

from src.core import container
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
@click.option("-f", "--file", help="Path to YAML file.")
def run(file: str) -> None:
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

if __name__ == "__main__":
    cli()
