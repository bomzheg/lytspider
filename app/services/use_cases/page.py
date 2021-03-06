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
            saved_page = await self.dao.page.get_by_url(page.url)
        except NoSavedPage:
            await self.notifier.notify_created(page)
            self.dao.page.save_page(page)
            await self.dao.commit()
        else:
            was_saved = saved_page == page
            if not was_saved:
                await self.notifier.notify_changed(page, saved_page)
                await self.dao.page.update_page(page)
                await self.dao.commit()
