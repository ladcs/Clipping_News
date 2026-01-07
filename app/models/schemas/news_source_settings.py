from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from db.base import Base


class NewsSourceSettings(Base):
    __tablename__ = "news_source_settings"

    source_id = Column(
        Integer,
        ForeignKey("news_sources.id", ondelete="CASCADE"),
        primary_key=True
    )

    settings = Column(JSONB, nullable=False)

    source = relationship(
        "NewsSource",
        back_populates="settings"
    )
