from sqlalchemy.orm import Session

from models.schemas.news_source_settings import NewsSourceSettings

class Repository_News_Source_Settings:
    def get_by_source_id(self,db: Session, source_id: int) -> NewsSourceSettings:
        return db.query(NewsSourceSettings).filter(NewsSourceSettings.source_id == source_id).one_or_none()

    def create_new_source_settings(self, db: Session, settings: NewsSourceSettings):
        db.add(settings)
        db.commit()
        db.refresh(settings)