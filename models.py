from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List


def now_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_only(value: str) -> str:
    return value[:10] if value else "-"


class StatusSurat(Enum):
    DRAFT = "DRAFT"
    MENUNGGU_BIDANG = "MENUNGGU_BIDANG"
    MENUNGGU_DEPARTEMEN = "MENUNGGU_DEPARTEMEN"
    MENUNGGU_BPH = "MENUNGGU_BPH"
    REVISI = "REVISI"
    DITOLAK = "DITOLAK"
    APPROVED = "APPROVED"

    @property
    def label(self) -> str:
        return {
            StatusSurat.DRAFT: "Draft",
            StatusSurat.MENUNGGU_BIDANG: "Menunggu Bidang",
            StatusSurat.MENUNGGU_DEPARTEMEN: "Menunggu Departemen",
            StatusSurat.MENUNGGU_BPH: "Menunggu BPH",
            StatusSurat.REVISI: "Revisi",
            StatusSurat.DITOLAK: "Ditolak",
            StatusSurat.APPROVED: "Approved",
        }[self]


class TahapApproval(Enum):
    BIDANG = "BIDANG"
    DEPARTEMEN = "DEPARTEMEN"
    BPH = "BPH"
    TU = "TU"


class AksiApproval(Enum):
    SETUJU = "SETUJU"
    REVISI = "REVISI"
    TOLAK = "TOLAK"


@dataclass
class Roles:
    id_role: int
    nama_role: str
    deskripsi: str


@dataclass
class Departemen:
    id_departemen: int
    nama_departemen: str
    deskripsi: str
    created_at: str = field(default_factory=now_datetime)
    updated_at: str = field(default_factory=now_datetime)


@dataclass
class Bidang:
    id_bidang: int
    id_departemen: int
    nama_bidang: str
    deskripsi: str
    created_at: str = field(default_factory=now_datetime)
    updated_at: str = field(default_factory=now_datetime)
    departemen: Optional[Departemen] = None


@dataclass
class Users:
    id_user: int
    role: Roles
    id_departemen: int
    id_bidang: int
    nama: str
    email: str
    password: str
    no_hp: str
    status_aktif: int = 1
    created_at: str = field(default_factory=now_datetime)
    updated_at: str = field(default_factory=now_datetime)
    departemen: Optional[Departemen] = None

    def login(self, email: str, password: str) -> bool:
        return self.status_aktif == 1 and self.email.lower() == email.lower() and self.password == password

    def ubah_password(self, password_lama: str, password_baru: str) -> bool:
        if self.password != password_lama:
            return False
        self.password = password_baru
        self.updated_at = now_datetime()
        return True

    def get_jenis_user(self) -> str:
        return "User Umum"

    def get_hak_akses(self) -> str:
        return "Mengakses fitur umum sistem surat"


class Mahasiswa(Users):
    def get_jenis_user(self) -> str:
        return "Mahasiswa"

    def get_hak_akses(self) -> str:
        return "Mengajukan surat, melihat status, dan mengirim revisi"


class PengurusBidang(Users):
    def get_jenis_user(self) -> str:
        return "Pengurus Bidang"

    def get_hak_akses(self) -> str:
        return "Memeriksa surat tahap bidang sebelum diteruskan"


class PengurusDepartemen(Users):
    def get_jenis_user(self) -> str:
        return "Pengurus Departemen"

    def get_hak_akses(self) -> str:
        return "Memeriksa surat tahap departemen"


class BPH(Users):
    def get_jenis_user(self) -> str:
        return "BPH"

    def get_hak_akses(self) -> str:
        return "Memberi persetujuan tingkat BPH sebelum validasi TU"


class AdminTU(Users):
    def get_jenis_user(self) -> str:
        return "Admin TU"

    def get_hak_akses(self) -> str:
        return "Mengelola user, template, dan validasi akhir surat"


@dataclass
class TemplateSurat:
    id_template: int
    nama_template: str
    deskripsi: str
    isi_template: str
    created_at: str = field(default_factory=now_datetime)
    updated_at: str = field(default_factory=now_datetime)

    def edit_template(self, nama_baru: str, isi_baru: str, deskripsi_baru: Optional[str] = None) -> None:
        self.nama_template = nama_baru
        self.isi_template = isi_baru
        if deskripsi_baru is not None:
            self.deskripsi = deskripsi_baru
        self.updated_at = now_datetime()


@dataclass
class Surat:
    id_surat: int
    nomor_surat: str
    id_template: int
    id_pengaju: int
    judul: str
    perihal: str
    isi: str
    pengaju: Optional[Users] = None
    tanggal_pengajuan: str = field(default_factory=now_datetime)
    status: StatusSurat = StatusSurat.DRAFT
    catatan_pengaju: str = ""
    file_surat: str = ""
    created_at: str = field(default_factory=now_datetime)
    updated_at: str = field(default_factory=now_datetime)
    riwayat_revisi: List["SuratRevisi"] = field(default_factory=list)

    def simpan_surat(self) -> bool:
        self.updated_at = now_datetime()
        return True

    def ubah_status(self, status_baru: StatusSurat) -> bool:
        self.status = status_baru
        self.updated_at = now_datetime()
        return True

    def kirim_surat(self) -> bool:
        if self.status != StatusSurat.DRAFT:
            return False
        return self.ubah_status(StatusSurat.MENUNGGU_BIDANG)


@dataclass
class SuratRevisi:
    id_revisi: int
    id_surat: int
    id_user: int
    catatan_revisi: str
    file_revisi: str
    tanggal_revisi: str = field(default_factory=now_datetime)


@dataclass
class Approval:
    id_approval: int
    id_surat: int
    id_user: int
    tahap: TahapApproval
    urutan: int
    aksi: AksiApproval = AksiApproval.SETUJU
    catatan: str = "-"
    tanggal_aksi: str = field(default_factory=now_datetime)

    def proses(self, surat: Surat, aksi: AksiApproval) -> bool:
        self.aksi = aksi
        self.tanggal_aksi = now_datetime()

        if aksi == AksiApproval.REVISI:
            return surat.ubah_status(StatusSurat.REVISI)
        if aksi == AksiApproval.TOLAK:
            return surat.ubah_status(StatusSurat.DITOLAK)
        if aksi != AksiApproval.SETUJU:
            return False

        if surat.status == StatusSurat.MENUNGGU_BIDANG:
            return surat.ubah_status(StatusSurat.MENUNGGU_DEPARTEMEN)
        if surat.status == StatusSurat.MENUNGGU_DEPARTEMEN:
            return surat.ubah_status(StatusSurat.MENUNGGU_BPH)
        if surat.status == StatusSurat.MENUNGGU_BPH:
            return surat.ubah_status(StatusSurat.APPROVED)
        return False
