import hashlib
import logging
from collections import deque
from app.models import dto
from app.models.config.main import ParserConfig
from app.services.downloader import Downloader
from app.services.use_cases.page import PageService
from app.services.parser import parse_page

logger = logging.getLogger(__name__)


class ParserFacade:
    def __init__(self, config: ParserConfig, page_use_case: PageService):
        self.config = config
        self.page_use_case = page_use_case

    async def run(self):
        async with Downloader() as client:
            await self.parse_links_graph(client)

    async def parse_links_graph(self, client: Downloader):
        visited_url = set()
        queue = deque()
        queue.append(self.config.url)
        while queue:
            url = queue.pop()
            if url in visited_url:
                logger.debug("skip visited url %s", url)
                continue
            page = await client.download_page(url)
            logger.info("downloaded page %s", page)
            if page.is_text_type():
                self.update_page(page)
            await self.page_use_case.upsert_page(page)
            queue.extend(page.links)
            visited_url.add(page.url)
            logger.debug("queue len=%s, visited len=%s", len(queue), len(visited_url))

    def update_page(self, page: dto.Page):
        parsed_data = parse_page(page.content, page.url, self.config)
        page.links = parsed_data.links
        page.target_content = parsed_data.target

        hash_ = hashlib.md5()
        hash_.update(page.target_content.encode())
        page.hash = hash_.hexdigest()

