from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from db.base import Base

class Sector(Base):
    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True)

    actives_id = Column(
        Integer,
        ForeignKey("actives.id"),
        primary_key=True,
        nullable=False,
        index=True,
    )

    label = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    active = relationship("Active", back_populates="sectors")
