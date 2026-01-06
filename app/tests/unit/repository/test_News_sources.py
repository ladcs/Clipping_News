import pytest
from unittest.mock import MagicMock
from repositories.news_sources import Repository_News_Source
from models.schemas.news_sources import NewsSource


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def repo():
    return Repository_News_Source()


def test_get_source_by_id(repo, db):
    query = db.query.return_value
    query.filter.return_value.one_or_none.return_value = "SOURCE"

    result = repo.get_source_by_id(db, 1)

    db.query.assert_called_once_with(NewsSource)
    assert result == "SOURCE"


def test_get_source_by_id_soft(repo, db):
    query = db.query.return_value
    query.filter.return_value.one_or_none.return_value = "SOURCE_SOFT"

    result = repo.get_source_by_id_soft(db, 1)

    assert result == "SOURCE_SOFT"


def test_get_source_by_label(repo, db):
    query = db.query.return_value
    query.filter.return_value.all.return_value = ["S1", "S2"]

    result = repo.get_source_by_label(db, "CNN")

    assert len(result) == 2


def test_create_source(repo, db):
    source = MagicMock()

    result = repo.create_source(db, source)

    db.add.assert_called_once_with(source)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(source)
    assert result == source


def test_update_source(repo, db):
    query = db.query.return_value
    query.filter.return_value.update.return_value = 1

    repo.update_source(db, 1, {"label": "NEW"})

    query.filter.assert_called_once()
    db.commit.assert_called_once()


def test_soft_delete(repo, db):
    query = db.query.return_value
    query.filter.return_value.update.return_value = 1

    repo.soft_delete(db, 1, "NOW")

    db.commit.assert_called_once()


def test_delete(repo, db):
    query = db.query.return_value
    query.filter.return_value.delete.return_value = 1

    repo.delete(db, 1)

    db.commit.assert_called_once()
