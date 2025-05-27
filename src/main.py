import logging
import shutil
import sys
from pathlib import Path

import click
import pydantic

from src.core import container
from src.core.exceptions import YamlParseError
from src.core.parser import YamlParser
from src.generators import ProjectGenerator
from src.preview.collector import PreviewCollector

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
@click.option("-f", "--force", is_flag=True, help="Overwrite existing config file.")
def init(preset: str, force: bool) -> None:
    """Generate basic example based on preset."""
    config_path = Path("ddd-config.yaml")
    if config_path.exists() and not force:
        click.echo(
            click.style("✗ Config file already exists. Use --force to overwrite.", fg="red"),
            err=True,
        )
        return
    if force and config_path.exists():
        click.echo(click.style("⚠ Overwriting existing config file", fg="yellow"))

    examples_dir = Path(__file__).parent / "templates" / "config_templates"
    source_file = examples_dir / f"ddd-config-{preset}.yaml"

    if not source_file.exists():
        click.echo(click.style(f"✗ Unknown preset: {preset}", fg="red"), err=True)
        return

    try:
        shutil.copy(source_file, config_path)
        click.echo(click.style(f"✓ Generated {preset} config: {config_path}", fg="green"))
    except OSError as error:
        click.echo(click.style(f"✗ Failed to create config file: {error}", fg="red"), err=True)


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
        click.echo(
            click.style("✓ Configuration validated successfully", fg="green"),
            color=True,
        )
    except YamlParseError as error:
        click.echo(click.style(f"✗ {error}", fg="red"), err=True)
    except pydantic.ValidationError as error:
        click.echo(
            click.style(f"✗ Configuration invalid: {error}", fg="red"),
            err=True,
            color=True,
        )
        click.echo(
            click.style(
                "Hint: Check the documentation for correct configuration format",
                fg="red",
            )
        )


@click.command()
@click.option("-f", "--file", help="Path to YAML file.")
def preview(file: str | None = None) -> None:
    """Preview future structure."""
    try:
        path = Path(file) if file else None

        if path and not path.exists():
            click.echo(click.style(f"Error: Config file not found: {file}", fg="red"), err=True)
            return

        click.echo("Project generation started.", color=True)

        container.provider.set_file_path(path)
        container.provider.set_preview_mode(preview_mode=True)
        generator: ProjectGenerator = container.get(ProjectGenerator)
        generator.generate()

        collector: PreviewCollector = container.get(PreviewCollector)
        collector.display()

    except Exception as error:
        click.echo(click.style(f"Error: {error}", fg="red"), err=True)


@click.command()
@click.option("-f", "--file", help="Path to YAML file.")
def run(file: str | None = None) -> None:
    """Generate structure for the app."""
    try:
        path = Path(file) if file else None

        if path and not path.exists():
            click.echo(click.style(f"Error: Config file not found: {file}", fg="red"), err=True)
            return

        click.echo("Project generation started.", color=True)

        container.provider.set_file_path(path)
        generator = container.get(ProjectGenerator)
        generator.generate()

        click.echo(click.style("Project generation completed successfully.", fg="green"))

    except Exception as error:
        click.echo(click.style(f"Error: {error}", fg="red"), err=True)


cli.add_command(run)
cli.add_command(init)
cli.add_command(validate)
cli.add_command(preview)

if __name__ == "__main__":
    cli()
