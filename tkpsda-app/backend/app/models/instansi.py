from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin


class Instansi(Base, TimestampMixin):
    __tablename__ = "instansi"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nama: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    kategori: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="balai / non-balai"
    )
    is_balai: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    tindak_lanjut: Mapped[list["TindakLanjut"]] = relationship(
        back_populates="instansi", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Instansi id={self.id} nama={self.nama!r}>"
