from typing import List
from sqlalchemy.orm import Session, joinedload

from models.schemas.actives import Active

class Repository_Actives:
    def get_all_actives(self, db: Session) -> List[Active]:
        return (
            db.query(Active)
            .options(joinedload(Active.sectors))
            .filter(Active.deleted_at.is_(None)).all()
        )