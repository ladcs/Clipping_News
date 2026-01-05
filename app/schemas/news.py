from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class NewsBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    url: HttpUrl
    source_id: int
    published_at: Optional[datetime] = None

class NewsCreate(NewsBase):
    content: Optional[str]
    summary: Optional[str]

class NewsUpdateContent(BaseModel):
    source_label: Optional[str]
    source_id: Optional[int]
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    id: Optional[int]
    content: str

class NewsUpdateSummary(BaseModel):
    source_label: Optional[str]
    source_id: Optional[int]
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    id: Optional[int]
    summary: str

class NewsOut(NewsBase):
    id: int
    created_at: datetime
    content: str
    summary: str
    about: str
    model_config = {
        "from_attributes": True  # <- importante p/ ORM (SQLAlchemy)
    }
