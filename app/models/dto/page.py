from __future__ import annotations

from dataclasses import dataclass

from app.models import db


@dataclass
class Page:
    db_id: int
    url: str
    content: str
    hash: str

    @classmethod
    def from_db(cls, page: db.Page) -> Page:
        return cls(
            db_id=page.id,
            url=page.url,
            content=page.content,
            hash=page.hash,
        )
