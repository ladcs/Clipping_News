from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from models.mixing import TimestampMixin
from db.base import Base

class News(Base, TimestampMixin):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    source_id = Column(
        Integer,
        ForeignKey("news_sources.id"),
        nullable=False,
        index=True,
    )

    title = Column(Text, nullable=False)
    link = Column(Text)
    summary = Column(Text, nullable=False)
    content = Column(Text)
    about = Column(Text)
    datetime = Column(TIMESTAMP(timezone=True), index=True)

    source = relationship("NewsSource", back_populates="news")
