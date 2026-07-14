from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.tindak_lanjut import StatusPelaksanaan
from app.schemas.instansi import InstansiRead


class TindakLanjutBase(BaseModel):
    rekomendasi_id: int
    instansi_id: int
    instansi_utama: bool = False
    tindak_lanjut: str | None = None
    status_pelaksanaan: StatusPelaksanaan | None = None
    capaian_hasil: str | None = None
    status_penyampaian: str | None = None
    tanggal_penyampaian: date | None = None
    bukti_penyampaian: str | None = None
    status_monev: str | None = None
    link_dokumentasi_monev: str | None = None
    keterangan: str | None = None
    link_dokumen: str | None = None


class TindakLanjutCreate(TindakLanjutBase):
    pass


class TindakLanjutUpdate(BaseModel):
    instansi_id: int | None = None
    instansi_utama: bool | None = None
    tindak_lanjut: str | None = None
    status_pelaksanaan: StatusPelaksanaan | None = None
    capaian_hasil: str | None = None
    status_penyampaian: str | None = None
    tanggal_penyampaian: date | None = None
    bukti_penyampaian: str | None = None
    status_monev: str | None = None
    link_dokumentasi_monev: str | None = None
    keterangan: str | None = None
    link_dokumen: str | None = None


class TindakLanjutRead(TindakLanjutBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    instansi: InstansiRead | None = None
