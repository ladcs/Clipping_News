from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from models.mixing import TimestampMixin
from db.base import Base

class Active(Base, TimestampMixin):
    __tablename__ = "actives"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    is_cripto = Column(Boolean, nullable=False)

    changes = relationship("Change", back_populates="active")
