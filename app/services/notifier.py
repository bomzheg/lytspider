from app.models import dto


class Notifier:
    async def notify_changed(self, page: dto.Page):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
