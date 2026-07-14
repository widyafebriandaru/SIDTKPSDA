from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TusiBase(BaseModel):
    nama: str


class TusiCreate(TusiBase):
    pass


class TusiUpdate(BaseModel):
    nama: str | None = None


class TusiRead(TusiBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
