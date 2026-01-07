import pytest
from sqlalchemy import text, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from db.base import Base
from core.config import DB_USER, DB_PASS

from db.session import SessionLocal


# ==========================
# Fixture: sessão de banco
# ==========================
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost:5432/mydb_test"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Cria todas as tabelas antes do teste
    e remove tudo após o teste.
    """
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine)


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
