from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tusi import Tusi
from app.schemas.tusi import TusiCreate, TusiUpdate


class CRUDTusi(CRUDBase[Tusi, TusiCreate, TusiUpdate]):
    def get_by_nama(self, db: Session, nama: str) -> Tusi | None:
        return db.query(Tusi).filter(Tusi.nama == nama).first()


tusi = CRUDTusi(Tusi)
