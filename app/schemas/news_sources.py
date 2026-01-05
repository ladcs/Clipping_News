from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class SourceBase(BaseModel):
    label: str = Field(..., min_length=3, max_length=255)
    source_link: HttpUrl
    is_scrath: bool
    need_summary: bool
    is_summary: bool

class SourceCreate(SourceBase):
    pass

class SourceUpdateUrl(BaseModel):
    source_link: str
    pass

class NewsUpdateLabel(BaseModel):
    label: str
    pass

class NewsUpdateScrath(BaseModel):
    pass

class NewsUpdateNeedSummary(BaseModel):
    pass

class NewsUpdateIsSummary(BaseModel):
    pass

class NewsOut(SourceBase):
    model_config = {
        "from_attributes": True  # <- importante p/ ORM (SQLAlchemy)
    }
