import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from db.session import SessionLocal


# ==========================
# Fixture: sessão de banco
# ==========================
@pytest.fixture(scope="function")
def db_session():
    """
    Cria uma sessão real com o banco.
    Usar APENAS em testes de integração.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# ======================================
# Fixture: valida se o banco está ativo
# ======================================
@pytest.fixture(scope="session", autouse=True)
def check_database_connection(request):
    """
    Se existir qualquer teste marcado como 'integration',
    valida se o banco está acessível antes de rodar.
    """
    if not request.session.items:
        return

    needs_db = any(
        "integration" in item.keywords
        for item in request.session.items
    )

    if not needs_db:
        return

    try:
        session = SessionLocal()
        session.execute(text("SELECT 1"))
        session.close()
    except OperationalError:
        pytest.exit(
            "❌ Banco de dados não está acessível. "
            "Suba o banco antes de rodar testes de integração.",
            returncode=1,
        )
