from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from models.mixing import TimestampMixin
from db.base import Base


class NewsSource(Base, TimestampMixin):
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True)
    label = Column(Text, nullable=False, unique=True)
    source_link = Column(Text, nullable=False, unique=True)

    news = relationship("News", back_populates="source")

    settings = relationship(
        "NewsSourceSettings",
        back_populates="source",
        uselist=False,
        cascade="all, delete-orphan"
    )
