from sqlalchemy import Column, Text, BigInteger

from app.models.db.base import Base


class Page(Base):
    __tablename__ = "pages"
    __mapper_args__ = {"eager_defaults": True}
    id = Column(BigInteger, primary_key=True)
    url = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    hash = Column(Text, nullable=True)
    mime_type = Column(Text, nullable=True)

    def __repr__(self):
        rez = (
            f"<Page "
            f"URL={self.url} "
            f"hash={self.hash} "
        )
        return rez + ">"
