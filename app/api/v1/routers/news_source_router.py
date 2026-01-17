from fastapi import APIRouter, Path
from schemas.news_sources import (
    SourceCreate,
    SourceNewsOut,
    SourceUpdateUrl,
)
from services.source_news import Service_News_Source

router = APIRouter()

@router.post(
    "/",
    response_model=SourceNewsOut,
    status_code=201,
)
def create_source(source: SourceCreate):
    service = Service_News_Source()
    return service.create_Source(source)


@router.get(
    "/{source_id}",
    response_model=SourceNewsOut,
)
def get_source_by_id(
    source_id: int = Path(..., gt=0),
):
    service = Service_News_Source()
    return service.read_by_id(source_id)


@router.get(
    "/by-label/{label}",
    response_model=list[SourceNewsOut],
)
def get_source_by_label(label: str):
    service = Service_News_Source()
    return service.read_by_label(label)


@router.patch(
    "/{source_id}/url",
    response_model=SourceNewsOut,
)
def update_source_url(
    source_id: int,
    payload: SourceUpdateUrl,
):
    service = Service_News_Source()
    return service.update_source_url(source_id, payload)
