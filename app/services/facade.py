import logging
from collections import deque

from app.services.downloader import Downloader
from app.services.parser import parse_content


logger = logging.getLogger(__name__)


async def facade():
    visited_url = set()
    queue = deque()
    async with Downloader("http://lytkarino.com") as client:
        page = await client.download_index()
        logger.info("downloaded page %s", page)
        page.links = parse_content(page.content)
        logger.info("found links %s")
        queue.append(page)

