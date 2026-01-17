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
    source_id: int
    source_link: HttpUrl

class SourceNewsOut(SourceBase):
    model_config = {
        "from_attributes": True
    }
