import asyncio
import logging
from pathlib import Path

from app.config import load_config
from app.config.logging_config import setup_logging
from app.dao import HolderDao
from app.models.config.main import Paths
from app.models.db import create_pool
from app.services.facade import ParserFacade
from app.services.notifier import Notifier
from app.services.use_cases.page import PageService

logger = logging.getLogger(__name__)


async def main():
    paths = Paths(Path(__file__).parent.parent)
    setup_logging(paths)

    config = load_config(paths)

    logger.info("started")

    pool = create_pool(config.db)
    async with pool() as session, Notifier() as notifier:
        await ParserFacade(
            config=config.parser,
            page_use_case=PageService(
                dao=HolderDao(session=session),
                notifier=notifier,
            )
        ).run()


if __name__ == '__main__':
    asyncio.run(main())
