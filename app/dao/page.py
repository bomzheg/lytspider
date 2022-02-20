from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao import BaseDAO
from app.models import db, dto
from app.utils.exceptions import NoSavedPage


class PageDao(BaseDAO[db.Page]):
    def __init__(self, session: AsyncSession):
        super().__init__(db.Page, session)

    async def get_by_url(self, url: str) -> dto.Page:
        try:
            return await self._get_by_url(url)
        except NoResultFound as e:
            raise NoSavedPage from e

    async def _get_by_url(self, url: str) -> db.Page:
        result = await self.session.execute(
            select(db.Page).where(db.Page.url == url)
        )
        return result.scalar_one()
