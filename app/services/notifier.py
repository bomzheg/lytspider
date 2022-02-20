import logging

from app.models import dto


class Notifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def notify_changed(self, new: dto.Page, old: dto.Page):
        self.logger.critical("page was changed %s", new)

    async def notify_created(self, page: dto.Page):
        self.logger.warning("page was created %s", page)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
