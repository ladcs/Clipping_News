from sqlalchemy.orm import Session
from datetime import datetime

from models.schemas.news_sources import NewsSource


class Repository_News_Source:
    def get_source_by_id(self, db: Session, source_id: int) -> NewsSource | None:
        return db.query(NewsSource).filter(NewsSource.id == source_id).one_or_none()
    
    def get_source_by_id_soft(self, db: Session, source_id: int) -> NewsSource | None:
        return db.query(NewsSource).filter(NewsSource.id == source_id, NewsSource.deleted_at.is_(None)).one_or_none()
    
    def get_source_by_label_soft(self, db: Session, label: str) -> NewsSource | None:
        return db.query(NewsSource).filter(NewsSource.label == label, NewsSource.deleted_at.is_(None)).one_or_none()
    
    def get_source_by_label(self, db: Session, label: str) -> NewsSource | None:
        return db.query(NewsSource).filter(NewsSource.label == label).one_or_none()
    
    def create_source(self, db: Session, news_source: NewsSource) -> NewsSource:
        try:
            db.add(news_source)
            db.commit()
            db.refresh(news_source)
        except Exception as e:
            raise e
        return news_source
    
    def update_source(
        self,
        db: Session,
        source_id: int,
        source: NewsSource
    ) -> NewsSource:
        db_source = (
            db.query(NewsSource)
            .filter(NewsSource.id == source_id)
            .one()
        )

        for attr, value in vars(source).items():
            if attr.startswith("_") or value is None:
                continue
            setattr(db_source, attr, value)

        db.commit()
        db.refresh(db_source)
        return db_source

    def soft_delete(self, db: Session, source_id: int, datetime: datetime):
        (
            db.query(NewsSource)
            .filter(NewsSource.id == source_id)
            .update({"deleted_at": datetime})
        )
        db.commit()

    def delete(self, db: Session, source_id: int):
        (
            db.query(NewsSource)
            .filter(NewsSource.id == source_id)
            .delete()
        )
        db.commit()