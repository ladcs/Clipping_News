from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.mixing import TimestampMixin
from app.db.base import Base

class ChangeReason(Base, TimestampMixin):
    __tablename__ = "change_reasons"

    id = Column(Integer, primary_key=True)

    active_id = Column(
        Integer,
        ForeignKey("actives.id"),
        index=True,
    )
    change_id = Column(
        Integer,
        ForeignKey("changes.id"),
        index=True,
    )
    news_id = Column(
        Integer,
        ForeignKey("news.id"),
        index=True,
    )

    label = Column(Text)
    porcent = Column(Float)

    active = relationship("Active")
    change = relationship("Change", back_populates="reasons")
    news = relationship("News")
