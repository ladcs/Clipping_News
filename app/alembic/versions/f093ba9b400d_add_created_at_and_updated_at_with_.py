"""add updated_at trigger for all tables

Revision ID: f093ba9b400d
Revises: b3178485b874
Create Date: 2025-12-29 15:32:03
"""

from typing import Sequence, Union
from alembic import op

# revision identifiers
revision: str = "f093ba9b400d"
down_revision: Union[str, Sequence[str], None] = "b3178485b874"
branch_labels = None
depends_on = None


tables = [
        "news_sources",
        "news",
        "actives",
        "changes",
        "change_reasons",
    ]

def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    for table in tables:
        op.execute(f"""
            CREATE TRIGGER trg_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW
            EXECUTE FUNCTION set_updated_at();
        """)


def downgrade() -> None:

    for table in tables:
        op.execute(
            f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table};"
        )

    op.execute("DROP FUNCTION IF EXISTS set_updated_at;")
