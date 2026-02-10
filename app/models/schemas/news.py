from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from models.mixing import TimestampMixin
from db.base import Base

class News(Base, TimestampMixin):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    source_id = Column(
        Integer,
        ForeignKey("news_sources.id"),
        primary_key=True,
        nullable=False,
        index=True,
    )

    title = Column(Text, nullable=False)
    link = Column(Text)
    summary = Column(Text)
    content = Column(Text)
    about = Column(JSONB, nullable=True)
    datetime = Column(TIMESTAMP(timezone=True), index=True)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    source = relationship("NewsSource", back_populates="news")