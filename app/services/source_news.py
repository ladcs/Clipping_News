from fastapi import HTTPException

from pydantic import HttpUrl

from db.session import get_db
from schemas.news_sources import SourceCreate
from models.schemas.news_sources import NewsSource
from repositories.news_sources import Repository_News_Source

class Service_News_Source:
    def create_Source(self, source: SourceCreate) -> NewsSource:
        with get_db() as db:
            repository = Repository_News_Source()
            label_exist = repository.get_source_by_label(db, source.label)
    
            if label_exist is not None:
                if label_exist.deleted_at is not None:
                        label_exist.deleted_at = None
                        new_source = label_exist
                        repository.update_source(db, new_source.id, new_source)
                else:
                    raise HTTPException(status_code= 409, detail='already exist')
            else:
                new_source = NewsSource(**source.model_dump())
                new_source = repository.create_source(db, new_source)
        return new_source
    
    def read_by_id(self, source_id: int) -> NewsSource:
        with get_db() as db:
            repository = Repository_News_Source()
            source_db = repository.get_source_by_id_soft(db, source_id)
        return source_db
    
    def read_by_label(self, label: str) -> NewsSource:
        with get_db() as db:
            repository = Repository_News_Source()
            source_db = repository.get_source_by_label_soft(db, label)
        return source_db
    
    def update_source_url(sellf, source_id: int, source_link: HttpUrl) -> NewsSource:
        with get_db() as db:
            repository = Repository_News_Source()
            source_db = repository.get_source_by_id(db, source_id)
            if source_db is None:
                raise HTTPException(status_code=400, detail='source news do not exist')
            source_db.source_link = source_link
            new_source = repository.update_source(db, source_id, source_db)
        return new_source