from sqlalchemy import (
    Column,
    Integer,
    Text,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship
from models.mixing import TimestampMixin
from db.base import Base


class ChangeReason(Base, TimestampMixin):
    __tablename__ = "change_reasons"

    id = Column(Integer, primary_key=True)

    active_id = Column(Integer, ForeignKey("actives.id"), index=True)
    change_id = Column(Integer, ForeignKey("changes.id"), index=True)

    # FK COMPOSTA para news
    news_id = Column(Integer, nullable=False)
    news_source_id = Column(Integer, nullable=False)

    label = Column(Text)
    porcent = Column(Float)

    __table_args__ = (
        ForeignKeyConstraint(
            ["news_source_id", "news_id"],
            ["news.source_id", "news.id"],
            ondelete="CASCADE",
        ),
    )

    active = relationship("Active")
    change = relationship("Change", back_populates="reasons")
    news = relationship("News")
