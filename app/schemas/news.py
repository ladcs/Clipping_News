from datetime import datetime
from typing import Optional
from typing import List
from pydantic import BaseModel, Field, HttpUrl


class NewsBase(BaseModel):
    url: HttpUrl
    source_id: int

class NewsId(BaseModel):
    id: int
    source_id: int

class NewsSummaryUpdate(BaseModel):
    ids: List[NewsId]

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

class NewsOut(BaseModel):
    id: int
    content: str

    link: Optional[str] = None
    summary: Optional[str] = None
    about: Optional[str] = None

    created_at: datetime
    model_config = {
        "from_attributes": True 
    }
