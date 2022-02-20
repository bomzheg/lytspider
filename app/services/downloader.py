import aiohttp

from app.models import dto


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
        async with self.session.get(url) as resp:
            page = dto.Page(url=str(resp.url), mime_type=resp.content_type)
            binary_content = await resp.content.read()
            if page.is_text_type():
                page.content = binary_content.decode()
            else:
                page.binary_content = binary_content
            return page

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
