from app.dao import HolderDao
from app.models import dto
from app.services.notifier import Notifier
from app.utils.exceptions import NoSavedPage


class PageService:
    def __init__(self, dao: HolderDao, notifier: Notifier):
        self.dao = dao
        self.notifier = notifier

    async def upsert_page(self, page: dto.Page):
        try:
            await self.dao.page.get_by_url(page.url)
        except NoSavedPage:
            was_saved = False
        else:
            was_saved = True
        if was_saved:
            await self.notifier.notify_changed(page)

