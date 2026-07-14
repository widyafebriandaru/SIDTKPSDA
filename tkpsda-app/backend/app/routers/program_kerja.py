from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas.program_kerja import ProgramKerjaCreate, ProgramKerjaRead, ProgramKerjaUpdate

router = APIRouter(prefix="/api/program-kerja", tags=["Program Kerja"])


@router.get("", response_model=list[ProgramKerjaRead])
def list_program_kerja(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.program_kerja.get_all(db, skip=skip, limit=limit)


@router.get("/{program_kerja_id}", response_model=ProgramKerjaRead)
def get_program_kerja(program_kerja_id: int, db: Session = Depends(get_db)):
    db_obj = crud.program_kerja.get(db, program_kerja_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Program kerja tidak ditemukan")
    return db_obj


@router.post("", response_model=ProgramKerjaRead, status_code=201)
def create_program_kerja(payload: ProgramKerjaCreate, db: Session = Depends(get_db)):
    return crud.program_kerja.create(db, payload)


@router.put("/{program_kerja_id}", response_model=ProgramKerjaRead)
def update_program_kerja(
    program_kerja_id: int, payload: ProgramKerjaUpdate, db: Session = Depends(get_db)
):
    db_obj = crud.program_kerja.get(db, program_kerja_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Program kerja tidak ditemukan")
    return crud.program_kerja.update(db, db_obj, payload)


@router.delete("/{program_kerja_id}", status_code=204)
def delete_program_kerja(program_kerja_id: int, db: Session = Depends(get_db)):
    db_obj = crud.program_kerja.get(db, program_kerja_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Program kerja tidak ditemukan")
    crud.program_kerja.delete(db, db_obj)
