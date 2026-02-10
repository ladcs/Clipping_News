from fastapi import APIRouter
from typing import Optional

from services.news import Service_News
from schemas.news import NewsOut, NewsBase, NewsSummaryUpdate

router = APIRouter()

@router.post(
    "/from-rss",
    response_model=list[NewsOut],
    status_code=201,
)
def create_news_from_rss(payload: NewsBase):
    service = Service_News()
    return service.create_news(
        url=payload.url,
        source_id=payload.source_id,
    )

@router.patch(
        "/resume-batch",
        response_model=dict[str, str],
        status_code=200,
)
def resume_news_batch(payload: NewsSummaryUpdate):
    service = Service_News()
    return service.resume_news_batch(ids=payload.ids)


@router.patch(
    "/about-batch",
    response_model=dict[str, str],
    status_code=200,
)
def about_news_batch(source_id: Optional[int] = None):
    service = Service_News()
    return service.about_news_batch(source_id=source_id)
