import logging
from collections import deque
from app.dao import HolderDao
from app.models import dto
from app.services.downloader import Downloader
from app.services.notifier import Notifier
from app.services.page import upsert_page
from app.services.parser import parse_links, parse_content

logger = logging.getLogger(__name__)


class ParserFacade:
    def __init__(self, url: str, xpath: str, notifier: Notifier, dao: HolderDao):
        self.url = url
        self.xpath = xpath
        self.notifier = notifier
        self.dao = dao

    async def run(self):
        async with Downloader(self.url) as client:
            await self.parse_links_graph(client)

    async def parse_links_graph(self, client: Downloader):
        visited_url = set()
        queue = deque()
        queue.append("/")
        while queue:
            page = await client.download_page(queue.pop())
            logger.info("downloaded page %s", page)
            self.update_page(page)
            was_changed = await upsert_page(page, self.dao)
            if was_changed:
                await self.notifier.notify_changed(page)
            queue.extend(page.links)
            visited_url.add(page.url)

    def update_page(self, page: dto.Page):
        page.links = parse_links(page.content, self.url)
        logger.debug("found links %s", page.links)
        page.target_content = parse_content(page.content, self.xpath)
        page.hash = hex(hash(page.target_content))

