from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models.tindak_lanjut import StatusPelaksanaan
from app.schemas.tindak_lanjut import TindakLanjutCreate, TindakLanjutRead, TindakLanjutUpdate

router = APIRouter(prefix="/api/tindak-lanjut", tags=["Tindak Lanjut"])


@router.get("", response_model=list[TindakLanjutRead])
def list_tindak_lanjut(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    rekomendasi_id: int | None = None,
    instansi_id: int | None = None,
    status_pelaksanaan: StatusPelaksanaan | None = None,
    db: Session = Depends(get_db),
):
    return crud.tindak_lanjut.get_all(
        db,
        skip=skip,
        limit=limit,
        rekomendasi_id=rekomendasi_id,
        instansi_id=instansi_id,
        status_pelaksanaan=status_pelaksanaan,
    )


@router.get("/{tindak_lanjut_id}", response_model=TindakLanjutRead)
def get_tindak_lanjut(tindak_lanjut_id: int, db: Session = Depends(get_db)):
    db_obj = crud.tindak_lanjut.get(db, tindak_lanjut_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tindak lanjut tidak ditemukan")
    return db_obj


@router.post("", response_model=TindakLanjutRead, status_code=201)
def create_tindak_lanjut(payload: TindakLanjutCreate, db: Session = Depends(get_db)):
    if not crud.rekomendasi.get(db, payload.rekomendasi_id):
        raise HTTPException(status_code=400, detail="rekomendasi_id tidak valid")
    if not crud.instansi.get(db, payload.instansi_id):
        raise HTTPException(status_code=400, detail="instansi_id tidak valid")
    return crud.tindak_lanjut.create(db, payload)


@router.put("/{tindak_lanjut_id}", response_model=TindakLanjutRead)
def update_tindak_lanjut(
    tindak_lanjut_id: int, payload: TindakLanjutUpdate, db: Session = Depends(get_db)
):
    db_obj = crud.tindak_lanjut.get(db, tindak_lanjut_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tindak lanjut tidak ditemukan")
    if payload.instansi_id is not None and not crud.instansi.get(db, payload.instansi_id):
        raise HTTPException(status_code=400, detail="instansi_id tidak valid")
    return crud.tindak_lanjut.update(db, db_obj, payload)


@router.delete("/{tindak_lanjut_id}", status_code=204)
def delete_tindak_lanjut(tindak_lanjut_id: int, db: Session = Depends(get_db)):
    db_obj = crud.tindak_lanjut.get(db, tindak_lanjut_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tindak lanjut tidak ditemukan")
    crud.tindak_lanjut.delete(db, db_obj)
