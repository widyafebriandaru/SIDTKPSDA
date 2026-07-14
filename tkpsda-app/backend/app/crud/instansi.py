from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.instansi import Instansi
from app.schemas.instansi import InstansiCreate, InstansiUpdate


class CRUDInstansi(CRUDBase[Instansi, InstansiCreate, InstansiUpdate]):
    def get_by_nama(self, db: Session, nama: str) -> Instansi | None:
        return db.query(Instansi).filter(Instansi.nama == nama).first()


instansi = CRUDInstansi(Instansi)
