import sqlite3
from datetime import datetime

DB_NAME = "surat_bem.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nama TEXT NOT NULL,
        role TEXT NOT NULL,
        bidang TEXT,
        departemen TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS template_surat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_template TEXT NOT NULL,
        jenis_surat TEXT NOT NULL,
        isi_template TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS surat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomor_surat TEXT UNIQUE,
        judul TEXT NOT NULL,
        jenis_surat TEXT NOT NULL,
        pemohon TEXT NOT NULL,
        tujuan TEXT,
        isi_surat TEXT,
        status TEXT DEFAULT 'Diajukan',
        tanggal_pengajuan TEXT DEFAULT CURRENT_TIMESTAMP,
        tanggal_selesai TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tahap_approval (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surat_id INTEGER NOT NULL,
        tahap TEXT NOT NULL,
        approver TEXT,
        status TEXT DEFAULT 'Menunggu',
        catatan TEXT,
        tanggal_approval TEXT,
        FOREIGN KEY (surat_id) REFERENCES surat(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS surat_revisi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surat_id INTEGER NOT NULL,
        catatan_revisi TEXT NOT NULL,
        dibuat_oleh TEXT NOT NULL,
        tanggal_revisi TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (surat_id) REFERENCES surat(id)
    )
    """)

    conn.commit()
    conn.close()

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    users = [
        ("mahasiswa", "mahasiswa123", "Mahasiswa", "mahasiswa", None, None),
        ("bidang", "bidang123", "Pengurus Bidang", "bidang", "Akademik", None),
        ("departemen", "departemen123", "Pengurus Departemen", "departemen", None, "Advokesma"),
        ("bph", "bph123", "BPH", "bph", None, None),
        ("admin_tu", "admin123", "Admin TU", "admin_tu", None, None),
    ]

    for user in users:
        cursor.execute("""
        INSERT OR IGNORE INTO users 
        (username, password, nama, role, bidang, departemen)
        VALUES (?, ?, ?, ?, ?, ?)
        """, user)

    templates = [
        (
            "Template Surat Undangan",
            "Undangan",
            "Dengan hormat, kami mengundang Bapak/Ibu/Saudara/i untuk menghadiri kegiatan yang diselenggarakan oleh BEM FASILKOM UPNVJT."
        ),
        (
            "Template Surat Permohonan",
            "Permohonan",
            "Dengan hormat, melalui surat ini kami mengajukan permohonan terkait kebutuhan kegiatan organisasi BEM FASILKOM UPNVJT."
        ),
        (
            "Template Surat Peminjaman",
            "Peminjaman",
            "Dengan hormat, kami mengajukan permohonan peminjaman fasilitas untuk mendukung pelaksanaan kegiatan organisasi."
        )
    ]

    for template in templates:
        cursor.execute("""
        INSERT OR IGNORE INTO template_surat
        (nama_template, jenis_surat, isi_template)
        VALUES (?, ?, ?)
        """, template)

    conn.commit()
    conn.close()

def tambah_surat(judul, jenis_surat, pemohon, tujuan, isi_surat):
    conn = get_connection()
    cursor = conn.cursor()

    nomor_surat = "BEM-" + datetime.now().strftime("%Y%m%d%H%M%S")

    cursor.execute("""
    INSERT INTO surat
    (nomor_surat, judul, jenis_surat, pemohon, tujuan, isi_surat, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nomor_surat, judul, jenis_surat, pemohon, tujuan, isi_surat, "Diajukan"))

    conn.commit()
    conn.close()

def get_all_surat():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, nomor_surat, judul, jenis_surat, pemohon, tujuan, status, tanggal_pengajuan
    FROM surat
    ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def update_status_surat(surat_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE surat
    SET status = ?
    WHERE id = ?
    """, (status, surat_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_data()
    print("Database surat_bem.db berhasil dibuat.")