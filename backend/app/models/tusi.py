from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin


class Tusi(Base, TimestampMixin):
    __tablename__ = "tusi"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nama: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    rekomendasi: Mapped[list["Rekomendasi"]] = relationship(back_populates="tusi")

    def __repr__(self) -> str:
        return f"<Tusi id={self.id} nama={self.nama!r}>"
