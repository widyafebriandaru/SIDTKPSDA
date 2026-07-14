import enum
from datetime import date

from sqlalchemy import String, Text, Date, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.mixins import TimestampMixin


class StatusPelaksanaan(str, enum.Enum):
    belum_dilaksanakan = "Belum Dilaksanakan"
    sedang_dilaksanakan = "Sedang Dilaksanakan"
    terlaksana = "Terlaksana"


class TindakLanjut(Base, TimestampMixin):
    """
    Satu baris = tindak lanjut satu rekomendasi oleh satu instansi.
    Satu rekomendasi bisa punya banyak instansi pelaksana (many-to-many
    diwujudkan lewat tabel ini, bukan tabel pivot murni, karena tiap
    pasangan rekomendasi-instansi punya status & catatan sendiri-sendiri).
    """

    __tablename__ = "tindak_lanjut"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    rekomendasi_id: Mapped[int] = mapped_column(
        ForeignKey("rekomendasi.id", ondelete="CASCADE"), nullable=False
    )
    instansi_id: Mapped[int] = mapped_column(
        ForeignKey("instansi.id", ondelete="CASCADE"), nullable=False
    )
    instansi_utama: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    tindak_lanjut: Mapped[str | None] = mapped_column(Text, nullable=True)
    status_pelaksanaan: Mapped[StatusPelaksanaan | None] = mapped_column(
        Enum(StatusPelaksanaan, name="status_pelaksanaan_enum"), nullable=True
    )
    capaian_hasil: Mapped[str | None] = mapped_column(Text, nullable=True)

    status_penyampaian: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tanggal_penyampaian: Mapped[date | None] = mapped_column(Date, nullable=True)
    bukti_penyampaian: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status_monev: Mapped[str | None] = mapped_column(String(100), nullable=True)
    link_dokumentasi_monev: Mapped[str | None] = mapped_column(String(500), nullable=True)

    keterangan: Mapped[str | None] = mapped_column(Text, nullable=True)
    link_dokumen: Mapped[str | None] = mapped_column(String(500), nullable=True)

    rekomendasi: Mapped["Rekomendasi"] = relationship(back_populates="tindak_lanjut")
    instansi: Mapped["Instansi"] = relationship(back_populates="tindak_lanjut")

    def __repr__(self) -> str:
        return (
            f"<TindakLanjut id={self.id} rekomendasi_id={self.rekomendasi_id} "
            f"instansi_id={self.instansi_id} status={self.status_pelaksanaan}>"
        )
