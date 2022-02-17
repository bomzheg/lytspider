import aiohttp


class Downloader:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = aiohttp.ClientSession(
            base_url=base_url,
            raise_for_status=True,
        )

    async def download_index(self):
        async with self.session.get("/") as resp:
            if resp.content_type == "text/html":
                return resp.content
            else:
                return resp.url

    async def close(self):
        await self.session.close()
