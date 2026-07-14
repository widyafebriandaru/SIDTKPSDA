from sqlalchemy import String, Integer, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.mixins import TimestampMixin


class ProgramKerja(Base, TimestampMixin):
    __tablename__ = "program_kerja"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    tahun: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kelompok: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="mis. PEMBAHASAN NON TUSI / PEMBAHASAN TUSI"
    )
    program: Mapped[str | None] = mapped_column(Text, nullable=True)
    status_pleno: Mapped[str | None] = mapped_column(String(100), nullable=True)
    uraian_progres: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_pembahasan: Mapped[str | None] = mapped_column(Text, nullable=True)
    kendala: Mapped[str | None] = mapped_column(Text, nullable=True)
    usulan_masukan: Mapped[str | None] = mapped_column(Text, nullable=True)
    fisik_persen: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    keuangan_persen: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    def __repr__(self) -> str:
        return f"<ProgramKerja id={self.id} tahun={self.tahun}>"
