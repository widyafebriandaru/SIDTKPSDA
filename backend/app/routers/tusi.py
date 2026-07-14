from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas.tusi import TusiCreate, TusiRead, TusiUpdate

router = APIRouter(prefix="/api/tusi", tags=["Tusi"])


@router.get("", response_model=list[TusiRead])
def list_tusi(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.tusi.get_all(db, skip=skip, limit=limit)


@router.get("/{tusi_id}", response_model=TusiRead)
def get_tusi(tusi_id: int, db: Session = Depends(get_db)):
    db_obj = crud.tusi.get(db, tusi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tusi tidak ditemukan")
    return db_obj


@router.post("", response_model=TusiRead, status_code=201)
def create_tusi(payload: TusiCreate, db: Session = Depends(get_db)):
    if crud.tusi.get_by_nama(db, payload.nama):
        raise HTTPException(status_code=409, detail="Nama tusi sudah terdaftar")
    return crud.tusi.create(db, payload)


@router.put("/{tusi_id}", response_model=TusiRead)
def update_tusi(tusi_id: int, payload: TusiUpdate, db: Session = Depends(get_db)):
    db_obj = crud.tusi.get(db, tusi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tusi tidak ditemukan")
    return crud.tusi.update(db, db_obj, payload)


@router.delete("/{tusi_id}", status_code=204)
def delete_tusi(tusi_id: int, db: Session = Depends(get_db)):
    db_obj = crud.tusi.get(db, tusi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Tusi tidak ditemukan")
    crud.tusi.delete(db, db_obj)
