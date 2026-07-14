from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.tindak_lanjut import TindakLanjut, StatusPelaksanaan
from app.schemas.tindak_lanjut import TindakLanjutCreate, TindakLanjutUpdate


class CRUDTindakLanjut(CRUDBase[TindakLanjut, TindakLanjutCreate, TindakLanjutUpdate]):
    def get(self, db: Session, id: int) -> TindakLanjut | None:
        return (
            db.query(TindakLanjut)
            .options(joinedload(TindakLanjut.instansi), joinedload(TindakLanjut.rekomendasi))
            .filter(TindakLanjut.id == id)
            .first()
        )

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        rekomendasi_id: int | None = None,
        instansi_id: int | None = None,
        status_pelaksanaan: StatusPelaksanaan | None = None,
    ) -> list[TindakLanjut]:
        query = db.query(TindakLanjut).options(
            joinedload(TindakLanjut.instansi), joinedload(TindakLanjut.rekomendasi)
        )
        if rekomendasi_id is not None:
            query = query.filter(TindakLanjut.rekomendasi_id == rekomendasi_id)
        if instansi_id is not None:
            query = query.filter(TindakLanjut.instansi_id == instansi_id)
        if status_pelaksanaan is not None:
            query = query.filter(TindakLanjut.status_pelaksanaan == status_pelaksanaan)
        return query.order_by(TindakLanjut.id).offset(skip).limit(limit).all()


tindak_lanjut = CRUDTindakLanjut(TindakLanjut)
