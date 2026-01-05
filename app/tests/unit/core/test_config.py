import importlib
import pytest


def test_database_url_is_built(monkeypatch):
    monkeypatch.setenv("DB_USER", "user")
    monkeypatch.setenv("DB_PASS", "pass")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "test_db")

    # força reload do módulo
    config = importlib.import_module("core.config")
    importlib.reload(config)

    assert config.DATABASE_URL == (
        "postgresql+psycopg2://user:pass@localhost:5432/test_db"
    )
