import pytest
from unittest.mock import MagicMock
from repositories.news import Repository_News
from models.schemas.news import News


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def repo():
    return Repository_News()


def test_get_news_by_id(repo, db):
    query = db.query.return_value
    query.filter.return_value.one_or_none.return_value = "NEWS"

    result = repo.get_news_by_id(db, 1)

    db.query.assert_called_once_with(News)
    assert result == "NEWS"


def test_create_news(repo, db):
    news = MagicMock()

    result = repo.create_news(db, news)

    db.add.assert_called_once_with(news)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(news)
    assert result == news


def test_update_news_summary(repo, db):
    query = db.query.return_value
    query.filter.return_value.update.return_value = 1

    repo.update_news_summary(db, 1, "summary")

    db.commit.assert_called_once()


def test_delete(repo, db):
    query = db.query.return_value
    query.filter.return_value.delete.return_value = 1

    repo.delete(db, 1)

    db.commit.assert_called_once()
