import aiohttp

from app.models import dto


class Downloader:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = aiohttp.ClientSession(
            base_url=base_url,
            raise_for_status=True,
        )

    async def download_index(self) -> dto.Page:
        return await self.download_page("/")

    async def download_page(self, url: str) -> dto.Page:
        async with self.session.get(url) as resp:
            content = (await resp.content.read()).decode()
            return dto.Page(
                url=str(resp.url),
                content=content,
                mime_type=resp.content_type,
            )

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
