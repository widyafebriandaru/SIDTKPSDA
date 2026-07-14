"""
Script untuk mengisi beberapa data contoh ke database.
Dijalankan SETELAH migrasi (alembic upgrade head) selesai.

Cara pakai:
    docker compose exec backend python seed.py
"""
from datetime import date

from app.database import SessionLocal
from app.models.instansi import Instansi
from app.models.tusi import Tusi
from app.models.rekomendasi import Rekomendasi
from app.models.tindak_lanjut import TindakLanjut, StatusPelaksanaan
from app.models.program_kerja import ProgramKerja


def seed():
    db = SessionLocal()
    try:
        # ---- Instansi ----
        instansi_data = [
            {"nama": "BBWS Mesuji Sekampung", "kategori": "balai", "is_balai": True},
            {"nama": "Dinas PSDA Provinsi Lampung", "kategori": "non-balai", "is_balai": False},
            {"nama": "BMKG Stasiun Klimatologi Lampung", "kategori": "non-balai", "is_balai": False},
        ]
        instansi_map = {}
        for item in instansi_data:
            obj = db.query(Instansi).filter_by(nama=item["nama"]).first()
            if not obj:
                obj = Instansi(**item)
                db.add(obj)
                db.flush()
            instansi_map[item["nama"]] = obj

        # ---- Tusi ----
        tusi_data = ["PEMBAHASAN RAAT", "SIH3", "ISU STRATEGIS"]
        tusi_map = {}
        for nama in tusi_data:
            obj = db.query(Tusi).filter_by(nama=nama).first()
            if not obj:
                obj = Tusi(nama=nama)
                db.add(obj)
                db.flush()
            tusi_map[nama] = obj

        db.commit()

        # ---- Rekomendasi + Tindak Lanjut contoh ----
        rekom1 = Rekomendasi(
            kategori="Penetapan",
            tusi_id=tusi_map["PEMBAHASAN RAAT"].id,
            tahun=2025,
            tanggal_sidang=date(2025, 11, 20),
            judul_sidang="Pembahasan Monitoring dan Evaluasi SIH3 serta RAAT 2025/2026 WS Seputih Sekampung",
            nomor_rekomendasi="01/SR/TKPSDA/WS-SS/2025",
            judul_rekomendasi="Rekomendasi TKPSDA WS Seputih Sekampung tentang RAAT Tahun 2025/2026",
            isi_rekomendasi="Kesepakatan dokumen RAAT WS Seputih Sekampung Tahun 2025-2026, DAS Seputih dan DAS Sekampung",
            rencana_tahun_pelaksanaan="2025-2026",
        )
        rekom2 = Rekomendasi(
            kategori="Kegiatan",
            tusi_id=tusi_map["SIH3"].id,
            tahun=2024,
            tanggal_sidang=date(2024, 6, 12),
            judul_sidang="Sidang Pleno 1 TKPSDA WS SS 2024",
            nomor_rekomendasi="02/SR/TKPSDA/WS-SS/2024",
            judul_rekomendasi="Penataan Sistem Informasi Hidrologi, Hidrometeorologi, dan Hidrogeologi",
            isi_rekomendasi="Penetapan Peraturan Gubernur sebagai dasar pelaksanaan SIH3",
            rencana_tahun_pelaksanaan="2024-2025",
        )
        rekom3 = Rekomendasi(
            kategori="Penetapan",
            tusi_id=tusi_map["ISU STRATEGIS"].id,
            tahun=2025,
            tanggal_sidang=date(2025, 6, 13),
            judul_sidang="Sidang Pleno 1 TKPSDA WS SS 2025",
            nomor_rekomendasi="03/SR/TKPSDA/WS-SS/2025",
            judul_rekomendasi="Strategi Penanganan Banjir di Wilayah Kota Bandar Lampung",
            isi_rekomendasi="Upaya strategi penanganan banjir di wilayah Kota Bandar Lampung",
            rencana_tahun_pelaksanaan="2025",
        )
        db.add_all([rekom1, rekom2, rekom3])
        db.flush()

        tindak_lanjut_data = [
            TindakLanjut(
                rekomendasi_id=rekom1.id,
                instansi_id=instansi_map["BBWS Mesuji Sekampung"].id,
                instansi_utama=True,
                tindak_lanjut="Penetapan RAAT WS Seputih Sekampung Tahun 2025/2026",
                status_pelaksanaan=StatusPelaksanaan.terlaksana,
                capaian_hasil="Kepmen PUPR tentang RAAT WS Seputih Sekampung Tahun 2025-2026",
                status_penyampaian="Sudah Disampaikan",
                tanggal_penyampaian=date(2025, 11, 25),
                status_monev="Sudah Monev",
            ),
            TindakLanjut(
                rekomendasi_id=rekom2.id,
                instansi_id=instansi_map["BMKG Stasiun Klimatologi Lampung"].id,
                instansi_utama=True,
                tindak_lanjut="Koordinasi terkait MOU data dan Penetapan Peraturan Gubernur",
                status_pelaksanaan=StatusPelaksanaan.sedang_dilaksanakan,
                capaian_hasil=None,
                status_penyampaian="Sudah Disampaikan",
                status_monev="Belum Monev",
                keterangan="Menunggu koordinasi lintas instansi",
            ),
            TindakLanjut(
                rekomendasi_id=rekom3.id,
                instansi_id=instansi_map["Dinas PSDA Provinsi Lampung"].id,
                instansi_utama=True,
                tindak_lanjut="Belum ada tindak lanjut dari instansi terkait",
                status_pelaksanaan=StatusPelaksanaan.belum_dilaksanakan,
                status_penyampaian="Sudah Disampaikan",
                status_monev="Belum Monev",
            ),
        ]
        db.add_all(tindak_lanjut_data)

        # ---- Program Kerja contoh ----
        program = ProgramKerja(
            tahun=2025,
            kelompok="PEMBAHASAN TUSI",
            program="Pembahasan Rencana Alokasi Air Tahunan (RAAT)",
            status_pleno="sudah dilaksanakan",
            uraian_progres="Sidang Pleno 1 dilaksanakan 12-13 Juni 2025",
            output_pembahasan="Rekomendasi penetapan dokumen RAAT",
            kendala="Monitoring dan evaluasi belum selesai dilakukan",
            fisik_persen=33.5,
            keuangan_persen=8.13,
        )
        db.add(program)

        db.commit()
        print("Seed data berhasil dimasukkan.")
        print(f"- Instansi: {db.query(Instansi).count()} baris")
        print(f"- Tusi: {db.query(Tusi).count()} baris")
        print(f"- Rekomendasi: {db.query(Rekomendasi).count()} baris")
        print(f"- Tindak Lanjut: {db.query(TindakLanjut).count()} baris")
        print(f"- Program Kerja: {db.query(ProgramKerja).count()} baris")
    except Exception as e:
        db.rollback()
        print(f"Gagal seed data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
