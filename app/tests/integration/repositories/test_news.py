from datetime import datetime
from repositories.news import Repository_News
from models.schemas.news import News


def create_news(db, about="test"):
    news = News(
        title="Title",
        about=about,
        content="Content",
        summary="Summary"
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


def test_create_and_get_by_id(db_session):
    repo = Repository_News()

    news = create_news(db_session)

    result = repo.get_news_by_id(db_session, news.id)

    assert result is not None
    assert result.id == news.id


def test_soft_delete(db_session):
    repo = Repository_News()
    news = create_news(db_session)

    repo.soft_delete(db_session, news.id, datetime.utcnow())

    soft = repo.get_news_by_id_soft(db_session, news.id)
    hard = repo.get_news_by_id(db_session, news.id)

    assert soft is None
    assert hard is not None


def test_update_summary(db_session):
    repo = Repository_News()
    news = create_news(db_session)

    repo.update_news_summary(db_session, news.id, "NEW SUMMARY")

    updated = repo.get_news_by_id(db_session, news.id)
    assert updated.summary == "NEW SUMMARY"


def test_delete(db_session):
    repo = Repository_News()
    news = create_news(db_session)

    repo.delete(db_session, news.id)

    assert repo.get_news_by_id(db_session, news.id) is None
