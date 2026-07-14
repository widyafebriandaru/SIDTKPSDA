from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas.rekomendasi import RekomendasiCreate, RekomendasiRead, RekomendasiUpdate

router = APIRouter(prefix="/api/rekomendasi", tags=["Rekomendasi"])


@router.get("", response_model=list[RekomendasiRead])
def list_rekomendasi(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    tahun: int | None = None,
    tusi_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.rekomendasi.get_all(db, skip=skip, limit=limit, tahun=tahun, tusi_id=tusi_id)


@router.get("/{rekomendasi_id}", response_model=RekomendasiRead)
def get_rekomendasi(rekomendasi_id: int, db: Session = Depends(get_db)):
    db_obj = crud.rekomendasi.get(db, rekomendasi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Rekomendasi tidak ditemukan")
    return db_obj


@router.post("", response_model=RekomendasiRead, status_code=201)
def create_rekomendasi(payload: RekomendasiCreate, db: Session = Depends(get_db)):
    return crud.rekomendasi.create(db, payload)


@router.put("/{rekomendasi_id}", response_model=RekomendasiRead)
def update_rekomendasi(
    rekomendasi_id: int, payload: RekomendasiUpdate, db: Session = Depends(get_db)
):
    db_obj = crud.rekomendasi.get(db, rekomendasi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Rekomendasi tidak ditemukan")
    return crud.rekomendasi.update(db, db_obj, payload)


@router.delete("/{rekomendasi_id}", status_code=204)
def delete_rekomendasi(rekomendasi_id: int, db: Session = Depends(get_db)):
    db_obj = crud.rekomendasi.get(db, rekomendasi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Rekomendasi tidak ditemukan")
    crud.rekomendasi.delete(db, db_obj)
