"""seed news_source_settings

Revision ID: 5c3d23994814
Revises: b3178485b874
Create Date: 2026-01-06 22:58:04.247176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '5c3d23994814'
down_revision: Union[str, Sequence[str], None] = 'b3178485b874'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    table = sa.table(
        "news_source_settings",
        sa.column("source_id", sa.Integer),
        sa.column("settings", postgresql.JSONB),
    )

    op.bulk_insert(
        table,
        [
            {
                "source_id": 1,
                "settings": {
                    "scrapping": [],
                    "content": [],
                    "clear_html": ["content"],
                    "trash": ['summary'],
                    'is_scrath': False,
                    'need_summary': True,
                    'is_summary': True
                },
            },
            {
                "source_id": 2,
                "settings": {
                    "scrapping": [],
                    "content": [],
                    "clear_html": ["summary"],
                    "trash": ['content'],
                    'is_scrath': False,
                    'need_summary': False,
                    'is_summary': True
                },
            },
            {
                "source_id": 3,
                "settings": {
                    "scrapping": [],
                    "content": [],
                    "clear_html": ["summary", "content"],
                    "trash": ["summary"],
                    'is_scrath': False,
                    'need_summary': True,
                    'is_summary': True
                },
            },
            {
                "source_id": 4,
                "settings": {
                    "scrapping": [],
                    "content": [],
                    "clear_html": ["summary", "content"],
                    "trash": ["summary"],
                    'is_scrath': False,
                    'need_summary': True,
                    'is_summary': True
                },
            },
        ],
    )


def downgrade():
    op.execute(
        """
        DELETE FROM news_source_settings
        WHERE source_id IN (1, 2, 3, 4)
        """
    )
