import logging
from collections import deque
from app.models import dto
from app.services.downloader import Downloader
from app.services.use_cases.page import PageService
from app.services.parser import parse_page

logger = logging.getLogger(__name__)


class ParserFacade:
    def __init__(self, url: str, xpath: str, page_use_case: PageService):
        self.url = url
        self.xpath = xpath
        self.page_use_case = page_use_case

    async def run(self):
        async with Downloader() as client:
            await self.parse_links_graph(client)

    async def parse_links_graph(self, client: Downloader):
        visited_url = set()
        queue = deque()
        queue.append(self.url)
        while queue:
            url = queue.pop()
            if url in visited_url:
                continue
            page = await client.download_page(url)
            logger.info("downloaded page %s", page)
            if page.is_text_type():
                self.update_page(page)
            await self.page_use_case.upsert_page(page)
            queue.extend(page.links)
            visited_url.add(page.url)

    def update_page(self, page: dto.Page):
        parsed_data = parse_page(page.content, page.url, self.xpath)
        page.links = parsed_data.links
        logger.debug("found links %s", page.links)
        page.target_content = parsed_data.target
        page.hash = hex(hash(page.target_content))

