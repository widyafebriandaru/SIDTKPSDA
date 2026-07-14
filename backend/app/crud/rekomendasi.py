from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.rekomendasi import Rekomendasi
from app.schemas.rekomendasi import RekomendasiCreate, RekomendasiUpdate


class CRUDRekomendasi(CRUDBase[Rekomendasi, RekomendasiCreate, RekomendasiUpdate]):
    def get(self, db: Session, id: int) -> Rekomendasi | None:
        return (
            db.query(Rekomendasi)
            .options(joinedload(Rekomendasi.tusi))
            .filter(Rekomendasi.id == id)
            .first()
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        tahun: int | None = None,
        tusi_id: int | None = None,
    ) -> list[Rekomendasi]:
        query = db.query(Rekomendasi).options(joinedload(Rekomendasi.tusi))
        if tahun is not None:
            query = query.filter(Rekomendasi.tahun == tahun)
        if tusi_id is not None:
            query = query.filter(Rekomendasi.tusi_id == tusi_id)
        return query.order_by(Rekomendasi.id).offset(skip).limit(limit).all()


rekomendasi = CRUDRekomendasi(Rekomendasi)
