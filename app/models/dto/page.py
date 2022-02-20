from __future__ import annotations

from dataclasses import dataclass

from app.models import db


@dataclass
class Page:
    url: str
    content: str
    mime_type: str
    target_content: str = None
    hash: str = None
    db_id: int = None
    links: list[str] = None

    def __post_init__(self):
        if self.links is None:
            self.links = []

    @classmethod
    def from_db(cls, page: db.Page) -> Page:
        return cls(
            db_id=page.id,
            url=page.url,
            content=page.content,
            hash=page.hash,
            mime_type=page.mime_type,
        )

    def __repr__(self):
        return (
            f"<Page "
            f"url={self.url} "
            f"mime-type={self.mime_type} "
            f"hash={self.hash} "
            f"db_id={self.db_id}"
            f">"
        )
