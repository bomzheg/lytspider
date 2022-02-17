from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.page import PageDao


@dataclass
class HolderDao:
    session: AsyncSession
    page: PageDao = field(init=False)

    def __post_init__(self):
        self.page = PageDao(self.session)

    async def commit(self):
        await self.session.commit()
