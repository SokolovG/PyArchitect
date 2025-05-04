import asyncio
import logging
import sys

from src.core import container
from src.generators import ProjectGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)


logger = logging.getLogger(__name__)


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
