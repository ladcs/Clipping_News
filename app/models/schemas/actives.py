from sqlalchemy import TIMESTAMP, Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from models.mixing import TimestampMixin
from db.base import Base

class Active(Base, TimestampMixin):
    __tablename__ = "actives"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    is_cripto = Column(Boolean, nullable=False)
    is_equity = Column(Boolean, nullable=False, default=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    changes = relationship("Change", back_populates="active")

    sectors = relationship("Sector", back_populates="active")
