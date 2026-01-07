from datetime import datetime
from repositories.news_sources import Repository_News_Source
from models.schemas.news_sources import NewsSource


def create_source(db, label="CNN"):
    source = NewsSource(
        label=label,
        source_link="https://cnn.com",
        is_scrath=0,
        need_summary=False,
        is_summary=False
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def test_create_and_get_by_id(db_session):
    repo = Repository_News_Source()
    source = create_source(db_session)

    result = repo.get_source_by_id(db_session, source.id)

    assert result is not None
    assert result.id == source.id


def test_get_by_label_soft(db_session):
    repo = Repository_News_Source()
    source = create_source(db_session, label="BBC")

    result = repo.get_source_by_label_soft(db_session, "BBC")

    assert len(result) == 1
    assert result[0].label == "BBC"


def test_soft_delete(db_session):
    repo = Repository_News_Source()
    source = create_source(db_session)

    repo.soft_delete(db_session, source.id, datetime.utcnow())

    assert repo.get_source_by_id_soft(db_session, source.id) is None
    assert repo.get_source_by_id(db_session, source.id) is not None


def test_update_source(db_session):
    repo = Repository_News_Source()
    source = create_source(db_session)

    repo.update_source(
        db_session,
        source.id,
        {"label": "UPDATED"}
    )

    updated = repo.get_source_by_id(db_session, source.id)
    assert updated.label == "UPDATED"


def test_delete(db_session):
    repo = Repository_News_Source()
    source = create_source(db_session)

    repo.delete(db_session, source.id)

    assert repo.get_source_by_id(db_session, source.id) is None
