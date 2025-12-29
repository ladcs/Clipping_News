from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.sql import func

class TimestampMixin:
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,  # começa NULL
        onupdate=func.now(),  # só preenche quando houver UPDATE
    )
    deleted_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )
