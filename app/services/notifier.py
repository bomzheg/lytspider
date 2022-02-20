import logging

from app.models import dto


class Notifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def notify_changed(self, page: dto.Page):
        self.logger.critical("page was changed %s", page)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
