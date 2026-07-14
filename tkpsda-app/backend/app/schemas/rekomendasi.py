from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.tusi import TusiRead


class RekomendasiBase(BaseModel):
    kategori: str | None = None
    tusi_id: int | None = None
    tahun: int | None = None
    tanggal_sidang: date | None = None
    judul_sidang: str | None = None
    nomor_rekomendasi: str | None = None
    judul_rekomendasi: str | None = None
    topik_isu: str | None = None
    isi_rekomendasi: str | None = None
    link_rekomendasi: str | None = None
    rencana_tahun_pelaksanaan: str | None = None


class RekomendasiCreate(RekomendasiBase):
    pass


class RekomendasiUpdate(BaseModel):
    kategori: str | None = None
    tusi_id: int | None = None
    tahun: int | None = None
    tanggal_sidang: date | None = None
    judul_sidang: str | None = None
    nomor_rekomendasi: str | None = None
    judul_rekomendasi: str | None = None
    topik_isu: str | None = None
    isi_rekomendasi: str | None = None
    link_rekomendasi: str | None = None
    rencana_tahun_pelaksanaan: str | None = None


class RekomendasiRead(RekomendasiBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    tusi: TusiRead | None = None
