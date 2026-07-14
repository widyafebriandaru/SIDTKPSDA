from datetime import date

from sqlalchemy import String, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin


class Rekomendasi(Base, TimestampMixin):
    __tablename__ = "rekomendasi"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    kategori: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="Penetapan / Kegiatan"
    )
    tusi_id: Mapped[int | None] = mapped_column(
        ForeignKey("tusi.id", ondelete="SET NULL"), nullable=True
    )
    tahun: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tanggal_sidang: Mapped[date | None] = mapped_column(Date, nullable=True)
    judul_sidang: Mapped[str | None] = mapped_column(Text, nullable=True)
    nomor_rekomendasi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    judul_rekomendasi: Mapped[str | None] = mapped_column(Text, nullable=True)
    topik_isu: Mapped[str | None] = mapped_column(Text, nullable=True)
    isi_rekomendasi: Mapped[str | None] = mapped_column(Text, nullable=True)
    link_rekomendasi: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rencana_tahun_pelaksanaan: Mapped[str | None] = mapped_column(String(50), nullable=True)

    tusi: Mapped["Tusi"] = relationship(back_populates="rekomendasi")
    tindak_lanjut: Mapped[list["TindakLanjut"]] = relationship(
        back_populates="rekomendasi", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Rekomendasi id={self.id} nomor={self.nomor_rekomendasi!r}>"
