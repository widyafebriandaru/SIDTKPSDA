from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProgramKerjaBase(BaseModel):
    tahun: int | None = None
    kelompok: str | None = None
    program: str | None = None
    status_pleno: str | None = None
    uraian_progres: str | None = None
    output_pembahasan: str | None = None
    kendala: str | None = None
    usulan_masukan: str | None = None
    fisik_persen: float | None = None
    keuangan_persen: float | None = None


class ProgramKerjaCreate(ProgramKerjaBase):
    pass


class ProgramKerjaUpdate(ProgramKerjaBase):
    pass


class ProgramKerjaRead(ProgramKerjaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
