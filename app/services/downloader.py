import logging

import aiohttp
from aiohttp import ClientResponseError

from app.models import dto


logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self, base_url: str = None):
        self.base_url = base_url
        self.session = aiohttp.ClientSession(
            base_url=base_url,
            raise_for_status=True,
        )

    async def download_index(self) -> dto.Page:
        return await self.download_page("/")

    async def download_page(self, url: str) -> dto.Page:
        try:
            async with self.session.get(url) as resp:
                page = dto.Page(
                    url=str(resp.url),
                    mime_type=resp.content_type,
                    http_status=resp.status,
                )
                binary_content = await resp.content.read()
                if page.is_text_type():
                    page.content = binary_content.decode()
                else:
                    page.binary_content = binary_content
                return page
        except ClientResponseError as e:
            logger.warning(
                "by request to url %s got http status %s with message %s",
                url, e.status, e.message,
            )
            return dto.Page(
                url=url,
                mime_type="application/json",
                http_status=e.status,
                content=e.message,
            )


    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
