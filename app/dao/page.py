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
            saved_page = await self._get_by_url(url)
            return dto.Page.from_db(saved_page)
        except NoResultFound as e:
            raise NoSavedPage from e

    def save_page(self, page: dto.Page):
        db_page = db_from_dto(page)
        self.save(db_page)

    async def update_page(self, page: dto.Page, db_id: int = None):
        if (id_ := db_id or page.db_id) is not None:
            saved_page = await self.session.get(db.Page, id_)
        else:
            saved_page = await self._get_by_url(page.url)
        update_page(source=page, target=saved_page)
        self.save(saved_page)

    async def _get_by_url(self, url: str) -> db.Page:
        result = await self.session.execute(
            select(db.Page).where(db.Page.url == url)
        )
        return result.scalar_one()


def update_page(source: dto.Page, target: db.Page):
    assert target.url == source.url
    target.content = source.content
    target.hash = source.hash


def db_from_dto(page: dto.Page) -> db.Page:
    db_page = db.Page(
        url=page.url,
        mime_type=page.mime_type,
        hash=page.hash,
    )
    if page.is_text_type():
        db_page.content = page.target_content
    return db_page

