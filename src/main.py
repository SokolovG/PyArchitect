import asyncio
from logging import getLogger

from src.core import container
from src.generators import ProjectGenerator

logger = getLogger(__name__)


async def main() -> None:
    """Entry point for the application.

    This function initializes the project generator with the
    configuration file and starts the generation process.
    """
    logger.info("Start generate...")
    generator = await container.get(ProjectGenerator)
    generator.generate()


if __name__ == "__main__":
    asyncio.run(main())
