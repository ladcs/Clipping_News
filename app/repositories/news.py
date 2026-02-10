from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func, or_

from models.schemas.news import News


class Repository_News:
    def get_by_id_in_list(self, db: Session, source_id: int, news_id_list: List[int]) -> List[News]:
        return db.query(News).filter(News.id.in_(news_id_list), News.source_id == source_id).all()
    
    def get_next_id_for_source(self, db: Session, source_id: int) -> int:
        max_id = (
            db.query(func.max(News.id))
            .filter(News.source_id == source_id)
            .scalar()
        )
        return (max_id or 0) + 1
    
    def get_news_to_about(self, db: Session) -> List[News]:
        return db.query(News).filter(
        News.about.is_(None),
        News.deleted_at.is_(None),
        News.summary.is_not(None), 
        func.lower(News.summary) != 'nenhum impacto relevante').all()
    
    def get_news_to_about_with_source_id(self, db: Session, source_id: int) -> List[News]:
        return db.query(News).filter(
        News.source_id == source_id,
        or_(
        News.about.is_(None),
        News.about == {}
        ),
        News.deleted_at.is_(None),
        News.summary.is_not(None), 
        func.lower(News.summary) != 'nenhum impacto relevante').all()
    
    def get_news_about_null_soft(self, db: Session) -> List[News]:
        return db.query(News).filter(
        News.about.is_(None),
        News.deleted_at.is_(None),
        News.summary.is_not(None)).all()

    def get_news_by_title_soft(self, db: Session, title: str, source_id: int) -> News | None:
        return db.query(News).filter(News.source_id == source_id, News.title == title, News.deleted_at is None).one_or_none()
    
    def get_news_by_source_id(self, db: Session, source_id: int) -> List[News]:
        return db.query(News).filter(News.source_id == source_id).all()

    def get_news_by_title(self, db: Session, title: str, source_id: int) -> News | None:
        return db.query(News).filter(News.source_id == source_id, News.title == title).one_or_none()
    
    def get_news_by_id_soft(self, db: Session, news_id: int) -> News | None:
        return db.query(News).filter(News.id == news_id, News.deleted_at.is_(None)).one_or_none()
    
    def get_news_by_id(self, db: Session, news_id: int) -> News | None:
        return db.query(News).filter(News.id == news_id).one_or_none()
    
    def get_news_by_about_soft(self, db: Session, about: str) -> list[News]:
        return db.query(News).filter(News.about == about, News.deleted_at.is_(None)).all()
    
    def get_news_by_about(self, db: Session, about: str) -> list[News]:
        return db.query(News).filter(News.about == about).all()
    
    def create_news(self, db: Session, news: News) -> News:
        db.add(news)
        db.commit()
        db.refresh(news)

        return news
    
    def create_news_batch(self, db: Session, news: List[News]):
        db.add_all(news)
        db.commit()
        for n in news:
            db.refresh(n)
        
        return news

    
    def update_news_summary(
        self,
        db: Session,
        news_id: int,
        source_id: int,
        summary: str,
    ) -> None:

        (
            db.query(News)
            .filter(News.id == news_id,
                    News.source_id == source_id)
            .update({"summary": summary})
        )
        db.commit()

    def update_news_about(
        self,
        db: Session,
        news_id: int,
        source_id: int,
        about: str,
    ) -> None:

        (
            db.query(News)
            .filter(News.id == news_id, News.source_id == source_id)
            .update({"about": about})
        )
        db.commit()

    
    def update_news_content(
        self,
        db: Session,
        news_id: int,
        content: str
    ) -> None:

        (
            db.query(News)
            .filter(News.id == news_id)
            .update({"content": content})
        )
        db.commit()

    def soft_delete(self, db: Session, new_id: int, datetime: datetime):
        (
            db.query(News)
            .filter(News.id == new_id)
            .update({"deleted_at": datetime})
        )
        db.commit()

    def restore_soft_deleted(self, db: Session, new_id: int):
        (
            db.query(News)
            .filter(News.id == new_id)
            .update({"deleted_at": None})
        )
        db.commit()

    def delete(self, db: Session, new_id: int):
        (
            db.query(News)
            .filter(News.id == new_id)
            .delete()
        )
        db.commit()