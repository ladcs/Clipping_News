from sqlalchemy.orm import Session
from datetime import datetime

from models.schemas.news import News


class Repository_News:
    def get_news_by_id_soft(self, db: Session, news_id: int) -> News | None:
        return db.query(News).filter(News.id == news_id, News.deleted_at.is_(None)).one_or_none()
    
    def get_news_by_id(self, db: Session, news_id: int) -> News | None:
        return db.query(News).filter(News.id == news_id).one_or_none()
    
    def get_news_by_about_soft(self, db: Session, about: str) -> list[News]:
        return db.query(News).filter(News.about == about, News.deleted_at.is_(None)).all()
    
    def get_news_by_about(self, db: Session, about: str) -> list[News]:
        return db.query(News).filter(News.about == about).all()
    
    def create_news(self, db: Session, news: News) -> News:
        try:
            db.add(news)
            db.commit()
            db.refresh(news)
        except Exception as e:
            raise e
        return news
    
    def update_news_summary(
        self,
        db: Session,
        news_id: int,
        summary: str
    ) -> None:

        (
            db.query(News)
            .filter(News.id == news_id)
            .update({"summary": summary})
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

    def delete(self, db: Session, new_id: int):
        (
            db.query(News)
            .filter(News.id == new_id)
            .delete()
        )
        db.commit()