from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.mixing import TimestampMixin
from src.base import Base

class Change(Base, TimestampMixin):
    __tablename__ = "changes"

    id = Column(Integer, primary_key=True)
    active_id = Column(
        Integer,
        ForeignKey("actives.id"),
        nullable=False,
        index=True,
    )

    active_value = Column(Float, nullable=False)
    active_value_prev = Column(Float)

    active = relationship("Active", back_populates="changes")
    reasons = relationship("ChangeReason", back_populates="change")
