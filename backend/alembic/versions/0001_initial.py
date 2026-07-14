"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


status_pelaksanaan_enum = sa.Enum(
    "belum_dilaksanakan",
    "sedang_dilaksanakan",
    "terlaksana",
    name="status_pelaksanaan_enum",
)


def upgrade() -> None:
    # ---- instansi ----
    op.create_table(
        "instansi",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nama", sa.String(length=255), nullable=False),
        sa.Column("kategori", sa.String(length=50), nullable=True, comment="balai / non-balai"),
        sa.Column("is_balai", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("nama", name="uq_instansi_nama"),
    )

    # ---- tusi ----
    op.create_table(
        "tusi",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nama", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("nama", name="uq_tusi_nama"),
    )

    # ---- rekomendasi ----
    op.create_table(
        "rekomendasi",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("kategori", sa.String(length=50), nullable=True, comment="Penetapan / Kegiatan"),
        sa.Column("tusi_id", sa.Integer(), sa.ForeignKey("tusi.id", ondelete="SET NULL"), nullable=True),
        sa.Column("tahun", sa.Integer(), nullable=True),
        sa.Column("tanggal_sidang", sa.Date(), nullable=True),
        sa.Column("judul_sidang", sa.Text(), nullable=True),
        sa.Column("nomor_rekomendasi", sa.String(length=255), nullable=True),
        sa.Column("judul_rekomendasi", sa.Text(), nullable=True),
        sa.Column("topik_isu", sa.Text(), nullable=True),
        sa.Column("isi_rekomendasi", sa.Text(), nullable=True),
        sa.Column("link_rekomendasi", sa.String(length=500), nullable=True),
        sa.Column("rencana_tahun_pelaksanaan", sa.String(length=50), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_rekomendasi_tahun", "rekomendasi", ["tahun"])
    op.create_index("ix_rekomendasi_tusi_id", "rekomendasi", ["tusi_id"])

    # ---- tindak_lanjut ----
    # Catatan: tipe ENUM postgres (status_pelaksanaan_enum) dibuat otomatis oleh
    # create_table di bawah ini saat pertama kali dipakai sebagai tipe kolom.
    op.create_table(
        "tindak_lanjut",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "rekomendasi_id",
            sa.Integer(),
            sa.ForeignKey("rekomendasi.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "instansi_id",
            sa.Integer(),
            sa.ForeignKey("instansi.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("instansi_utama", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("tindak_lanjut", sa.Text(), nullable=True),
        sa.Column("status_pelaksanaan", status_pelaksanaan_enum, nullable=True),
        sa.Column("capaian_hasil", sa.Text(), nullable=True),
        sa.Column("status_penyampaian", sa.String(length=100), nullable=True),
        sa.Column("tanggal_penyampaian", sa.Date(), nullable=True),
        sa.Column("bukti_penyampaian", sa.String(length=500), nullable=True),
        sa.Column("status_monev", sa.String(length=100), nullable=True),
        sa.Column("link_dokumentasi_monev", sa.String(length=500), nullable=True),
        sa.Column("keterangan", sa.Text(), nullable=True),
        sa.Column("link_dokumen", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_tindak_lanjut_rekomendasi_id", "tindak_lanjut", ["rekomendasi_id"])
    op.create_index("ix_tindak_lanjut_instansi_id", "tindak_lanjut", ["instansi_id"])
    op.create_index("ix_tindak_lanjut_status", "tindak_lanjut", ["status_pelaksanaan"])

    # ---- program_kerja ----
    op.create_table(
        "program_kerja",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tahun", sa.Integer(), nullable=True),
        sa.Column(
            "kelompok",
            sa.String(length=255),
            nullable=True,
            comment="mis. PEMBAHASAN NON TUSI / PEMBAHASAN TUSI",
        ),
        sa.Column("program", sa.Text(), nullable=True),
        sa.Column("status_pleno", sa.String(length=100), nullable=True),
        sa.Column("uraian_progres", sa.Text(), nullable=True),
        sa.Column("output_pembahasan", sa.Text(), nullable=True),
        sa.Column("kendala", sa.Text(), nullable=True),
        sa.Column("usulan_masukan", sa.Text(), nullable=True),
        sa.Column("fisik_persen", sa.Numeric(5, 2), nullable=True),
        sa.Column("keuangan_persen", sa.Numeric(5, 2), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_table("program_kerja")
    op.drop_index("ix_tindak_lanjut_status", table_name="tindak_lanjut")
    op.drop_index("ix_tindak_lanjut_instansi_id", table_name="tindak_lanjut")
    op.drop_index("ix_tindak_lanjut_rekomendasi_id", table_name="tindak_lanjut")
    op.drop_table("tindak_lanjut")
    status_pelaksanaan_enum.drop(op.get_bind(), checkfirst=True)
    op.drop_index("ix_rekomendasi_tusi_id", table_name="rekomendasi")
    op.drop_index("ix_rekomendasi_tahun", table_name="rekomendasi")
    op.drop_table("rekomendasi")
    op.drop_table("tusi")
    op.drop_table("instansi")
