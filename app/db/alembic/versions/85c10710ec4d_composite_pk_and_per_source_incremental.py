"""composite pk and per-source incremental id for news

Revision ID: 85c10710ec4d
Revises: 5c3d23994814
Create Date: 2026-01-18 10:32:09.374373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85c10710ec4d'
down_revision: Union[str, Sequence[str], None] = '5c3d23994814'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION news_next_id_per_source()
        RETURNS trigger AS $$
        BEGIN
            IF NEW.id IS NULL THEN
                SELECT COALESCE(MAX(id), 0) + 1
                INTO NEW.id
                FROM news
                WHERE source_id = NEW.source_id;
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    # ⚡ Trigger
    op.execute(
        """
        CREATE TRIGGER trg_news_next_id
        BEFORE INSERT ON news
        FOR EACH ROW
        EXECUTE FUNCTION news_next_id_per_source();
        """
    )


def downgrade():
    # 🔥 Remove trigger
    op.execute("DROP TRIGGER IF EXISTS trg_news_next_id ON news;")

    # 🔥 Remove função
    op.execute("DROP FUNCTION IF EXISTS news_next_id_per_source;")

    # 🔴 Remove PK composta
    op.drop_constraint("news_pkey", "news", type_="primary")

    # 🟢 Volta PK simples
    op.create_primary_key(
        "news_pkey",
        "news",
        ["id"],
    )
