from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas.instansi import InstansiCreate, InstansiRead, InstansiUpdate

router = APIRouter(prefix="/api/instansi", tags=["Instansi"])


@router.get("", response_model=list[InstansiRead])
def list_instansi(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.instansi.get_all(db, skip=skip, limit=limit)


@router.get("/{instansi_id}", response_model=InstansiRead)
def get_instansi(instansi_id: int, db: Session = Depends(get_db)):
    db_obj = crud.instansi.get(db, instansi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Instansi tidak ditemukan")
    return db_obj


@router.post("", response_model=InstansiRead, status_code=201)
def create_instansi(payload: InstansiCreate, db: Session = Depends(get_db)):
    if crud.instansi.get_by_nama(db, payload.nama):
        raise HTTPException(status_code=409, detail="Nama instansi sudah terdaftar")
    return crud.instansi.create(db, payload)


@router.put("/{instansi_id}", response_model=InstansiRead)
def update_instansi(instansi_id: int, payload: InstansiUpdate, db: Session = Depends(get_db)):
    db_obj = crud.instansi.get(db, instansi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Instansi tidak ditemukan")
    return crud.instansi.update(db, db_obj, payload)


@router.delete("/{instansi_id}", status_code=204)
def delete_instansi(instansi_id: int, db: Session = Depends(get_db)):
    db_obj = crud.instansi.get(db, instansi_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Instansi tidak ditemukan")
    crud.instansi.delete(db, db_obj)
