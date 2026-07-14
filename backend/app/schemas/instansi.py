from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InstansiBase(BaseModel):
    nama: str
    kategori: str | None = None
    is_balai: bool = False


class InstansiCreate(InstansiBase):
    pass


class InstansiUpdate(BaseModel):
    nama: str | None = None
    kategori: str | None = None
    is_balai: bool | None = None


class InstansiRead(InstansiBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
