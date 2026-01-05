from db.session import engine
from db.session import get_db
from sqlalchemy.orm import Session


def test_engine_is_created():
    assert engine is not None

def test_get_db_returns_session():
    gen = get_db()
    session = next(gen)

    assert isinstance(session, Session)

    # fecha corretamente
    try:
        next(gen)
    except StopIteration:
        pass
