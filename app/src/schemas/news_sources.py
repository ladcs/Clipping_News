from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from src.mixing import TimestampMixin
from src.base import Base


class NewsSource(Base, TimestampMixin):
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True)
    label = Column(Text, nullable=False, unique=True)
    source_link = Column(Text, nullable=False, unique=True)
    is_scratch = Column(Boolean, nullable=False, default=False)
    need_summary = Column(Boolean, nullable=False, default=False)
    is_summary = Column(Boolean, nullable=False, default=True)

    news = relationship("News", back_populates="source")
