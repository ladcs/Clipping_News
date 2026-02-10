from typing import List
from sqlalchemy.orm import Session, joinedload

from models.schemas.sector import Sector

class Repository_Sectors:
    def get_all(self, db: Session) -> List[Sector]:
        return (
            db.query(Sector)
            .options(joinedload(Sector.active))
            .filter(Sector.deleted_at.is_(None))
            .all()
        )
