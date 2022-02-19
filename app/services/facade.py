import logging
from collections import deque

from sqlalchemy.orm import sessionmaker

from app.dao import HolderDao
from app.services.downloader import Downloader
from app.services.notifier import Notifier
from app.services.page import upsert_page
from app.services.parser import parse_links, parse_content

logger = logging.getLogger(__name__)


async def facade(pool: sessionmaker):
    visited_url = set()
    queue = deque()
    queue.append("/")
    async with Downloader("http://lytkarino.com") as client, Notifier() as notifier, pool() as session:
        dao = HolderDao(session)
        while queue:
            page = await client.download_index(queue.pop())
            logger.info("downloaded page %s", page)
            update_page(page)
            was_changed = await upsert_page(page, dao)
            if was_changed:
                await notifier.notify_changed(page)
            queue.extend(page.links)
            visited_url.add(page.url)


def update_page(page):
    page.links = parse_links(page.content)
    logger.debug("found links %s", page.links)
    page.target_content = parse_content(page.content)
    page.hash = hex(hash(page.target_content))

