from fastapi import APIRouter

from services.news import Service_News
from schemas.news import NewsOut, NewsBase

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