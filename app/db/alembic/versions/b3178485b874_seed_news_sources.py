"""seed news_sources

Revision ID: b3178485b874
Revises: 9a3404de9d75
Create Date: 2025-12-29 15:19:51.864919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.schemas.news_sources import NewsSource

# revision identifiers, used by Alembic.
revision: str = 'b3178485b874'
down_revision: Union[str, Sequence[str], None] = '9a3404de9d75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    seeds = [
        NewsSource(
            label="invest news",
            source_link="https://investnews.com.br/feed/",
            need_summary=True,
        ),
        NewsSource(
            label="globo",
            source_link="https://g1.globo.com/rss/g1/economia",
            need_summary=True,
            is_summary=False,
        ),
        NewsSource(
            label="portal da economia",
            source_link="https://portaldaeconomia.com/feed",
            need_summary=True,
        ),
        NewsSource(
            label="my business brazil",
            source_link="https://mybusinessbrazil.com/feed/",
        ),
    ]

    for seed in seeds:
        exists = (
            session.query(NewsSource)
            .filter(NewsSource.label == seed.label)
            .first()
        )
        if not exists:
            session.add(seed)

    session.commit()

def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.query(NewsSource).filter(
        NewsSource.label.in_([
            "invest news",
            "globo",
            "portal da economia",
            "my business brazil",
        ])
    ).delete(synchronize_session=False)

    session.commit()
