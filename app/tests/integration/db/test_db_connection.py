# tests/integration/db/test_database_connection.py
import pytest
from sqlalchemy import text


@pytest.mark.integration
def test_database_connection(db_session):
    result = db_session.execute(text("SELECT 1")).scalar()
    assert result == 1
