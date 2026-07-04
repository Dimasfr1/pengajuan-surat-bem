from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

import pandas as pd
import streamlit as st

from models import (
    AdminTU,
    AksiApproval,
    Approval,
    BPH,
    Bidang,
    Departemen,
    Mahasiswa,
    PengurusBidang,
    PengurusDepartemen,
    Roles,
    StatusSurat,
    Surat,
    SuratRevisi,
    TahapApproval,
    TemplateSurat,
    Users,
    date_only,
)

st.set_page_config(
    page_title="Sistem Surat BEM",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


LOGO_PATH = "logo_upn.png"


ROLE_CLASS: Dict[str, Type[Users]] = {
    "mahasiswa": Mahasiswa,
    "bidang": PengurusBidang,
    "departemen": PengurusDepartemen,
    "bph": BPH,
    "admin_tu": AdminTU,
}



def apply_custom_css() -> None:
    st.markdown(
        """
        <style>
        /* Hilangkan menu bawaan dan tombol Deploy saja */
        #MainMenu, footer, .stDeployButton {
            display: none !important;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #242838 0%, #1b1f2d 100%);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }

        .login-logo-wrap {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 10px;
            margin-bottom: 12px;
        }

        .login-title {
            text-align: center;
            font-size: 42px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 28px;
        }

        .sidebar-logo-title {
            text-align: center;
            font-size: 30px;
            font-weight: 800;
            color: #ffffff;
            background: #2d3650;
            border-radius: 16px;
            padding: 15px 10px;
            margin-bottom: 20px;
        }

        .sidebar-title {
            font-size: 31px;
            font-weight: 800;
            color: #ffffff;
            margin-top: 8px;
            margin-bottom: 20px;
        }

        .sidebar-name {
            font-size: 28px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 18px;
        }

        .sidebar-label {
            font-size: 24px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 4px;
        }

        .sidebar-value {
            font-size: 24px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 22px;
        }

        .sidebar-info {
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.4;
            margin-bottom: 18px;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            font-size: 20px !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            padding: 0.55rem 1rem !important;
        }

        [data-testid="stSidebar"] .stRadio > label {
            font-size: 23px !important;
            font-weight: 800 !important;
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .stRadio label p {
            font-size: 21px !important;
            font-weight: 700 !important;
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_logo(width: int = 135) -> None:
    if os.path.exists(LOGO_PATH):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image(LOGO_PATH, width=width)
    else:
        st.markdown('<div class="sidebar-logo-title">UPN</div>', unsafe_allow_html=True)

def init_state() -> None:
    if "initialized" in st.session_state:
        return

    r_mhs = Roles(1, "mahasiswa", "Pengaju surat")
    r_bid = Roles(2, "bidang", "Pengurus bidang")
    r_dep = Roles(3, "departemen", "Pengurus departemen")
    r_bph = Roles(4, "bph", "Badan Pengurus Harian")
    r_admin = Roles(5, "admin_tu", "Tata Usaha / approver")

    dep = Departemen(1, "Departemen Akademik", "Urusan akademik kampus")
    bidang = Bidang(1, 1, "Bidang Kemahasiswaan", "Kegiatan kemahasiswaan", departemen=dep)

    users: List[Users] = [
        AdminTU(99, r_admin, 1, 1, "Admin TU", "admin@bem.com", "admin123", "08000000000", departemen=dep),
        PengurusBidang(100, r_bid, 1, 1, "Bidang Kemahasiswaan", "bidang@bem.com", "123", "08111111111", departemen=dep),
        PengurusDepartemen(101, r_dep, 1, 1, "Departemen Akademik", "departemen@bem.com", "123", "08222222222", departemen=dep),
        BPH(102, r_bph, 1, 1, "BPH", "bph@bem.com", "123", "08333333333", departemen=dep),
    ]

    templates = [
        TemplateSurat(
            1,
            "Surat Keterangan Aktif",
            "SKA untuk keperluan beasiswa/instansi",
            "Yang bertanda tangan menerangkan bahwa {nama} adalah mahasiswa aktif.",
        ),
        TemplateSurat(
            2,
            "Surat Izin Kegiatan",
            "Permohonan izin pelaksanaan kegiatan BEM",
            "Dengan hormat kami mengajukan izin kegiatan {nama_kegiatan} pada tanggal {tanggal}.",
        ),
    ]

    st.session_state.roles = [r_mhs, r_bid, r_dep, r_bph, r_admin]
    st.session_state.departemen = [dep]
    st.session_state.bidang = [bidang]
    st.session_state.users = users
    st.session_state.templates = templates
    st.session_state.surat = []
    st.session_state.revisi = []
    st.session_state.approvals = []
    st.session_state.user_seq = 103
    st.session_state.surat_seq = 1
    st.session_state.revisi_seq = 1
    st.session_state.approval_seq = 1
    st.session_state.template_seq = 3
    st.session_state.login_user_id = None
    st.session_state.initialized = True


def get_current_user() -> Optional[Users]:
    user_id = st.session_state.get("login_user_id")
    if user_id is None:
        return None
    return find_user(user_id)


def find_user(user_id: int) -> Optional[Users]:
    return next((u for u in st.session_state.users if u.id_user == user_id), None)


def find_role(role_id: int) -> Optional[Roles]:
    return next((r for r in st.session_state.roles if r.id_role == role_id), None)


def find_surat(surat_id: int) -> Optional[Surat]:
    return next((s for s in st.session_state.surat if s.id_surat == surat_id), None)


def find_template(template_id: int) -> Optional[TemplateSurat]:
    return next((t for t in st.session_state.templates if t.id_template == template_id), None)


def is_pending(status: StatusSurat) -> bool:
    return status in {StatusSurat.MENUNGGU_BIDANG, StatusSurat.MENUNGGU_DEPARTEMEN, StatusSurat.MENUNGGU_BPH}


def status_badge(status: StatusSurat) -> str:
    return status.label


def surat_to_rows(surat_list: List[Surat]) -> List[Dict[str, Any]]:
    rows = []
    for s in surat_list:
        rows.append(
            {
                "ID": s.id_surat,
                "Nomor": s.nomor_surat,
                "Judul": s.judul,
                "Perihal": s.perihal,
                "Pengaju": s.pengaju.nama if s.pengaju else "-",
                "Tanggal": date_only(s.tanggal_pengajuan),
                "Status": s.status.label,
            }
        )
    return rows


def user_to_rows() -> List[Dict[str, Any]]:
    return [
        {
            "ID": u.id_user,
            "Nama": u.nama,
            "Email": u.email,
            "Role": u.role.nama_role,
            "Jenis": u.get_jenis_user(),
            "Status": "AKTIF" if u.status_aktif == 1 else "NONAKTIF",
        }
        for u in st.session_state.users
    ]


def template_to_rows() -> List[Dict[str, Any]]:
    return [
        {
            "ID": t.id_template,
            "Nama Template": t.nama_template,
            "Deskripsi": t.deskripsi,
            "Isi Template": t.isi_template,
        }
        for t in st.session_state.templates
    ]


def show_surat_detail(s: Surat) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**ID Surat:** {s.id_surat}")
        st.write(f"**Nomor:** {s.nomor_surat}")
        st.write(f"**Judul:** {s.judul}")
        st.write(f"**Perihal:** {s.perihal}")
    with col2:
        st.write(f"**Pengaju:** {s.pengaju.nama if s.pengaju else '-'}")
        st.write(f"**Tanggal Pengajuan:** {date_only(s.tanggal_pengajuan)}")
        st.write(f"**Status:** {s.status.label}")
        st.write(f"**Catatan Pengaju:** {s.catatan_pengaju or '-'}")
    st.text_area("Isi Surat", value=s.isi, height=140, disabled=True)

    approval_rows = [
        {
            "Tahap": ap.tahap.value,
            "Aksi": ap.aksi.value,
            "Tanggal": date_only(ap.tanggal_aksi),
            "Catatan": ap.catatan,
        }
        for ap in st.session_state.approvals
        if ap.id_surat == s.id_surat
    ]
    revisi_rows = [
        {
            "ID Revisi": r.id_revisi,
            "Tanggal": date_only(r.tanggal_revisi),
            "Catatan": r.catatan_revisi,
            "File": r.file_revisi,
        }
        for r in st.session_state.revisi
        if r.id_surat == s.id_surat
    ]

    st.subheader("Riwayat Approval")
    if approval_rows:
        st.dataframe(pd.DataFrame(approval_rows), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada riwayat approval.")

    st.subheader("Riwayat Revisi")
    if revisi_rows:
        st.dataframe(pd.DataFrame(revisi_rows), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada riwayat revisi.")


def login_page() -> None:
    show_logo(width=145)
    st.markdown('<div class="login-title">Sistem Manajemen Surat BEM</div>', unsafe_allow_html=True)

    tab_login, tab_daftar = st.tabs(["Login", "Daftar Akun Baru"])

    with tab_login:
        with st.form("form_login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            user = next((u for u in st.session_state.users if u.login(email.strip(), password)), None)
            if user:
                st.session_state.login_user_id = user.id_user
                st.success(f"Selamat datang, {user.nama}!")
                st.rerun()
            else:
                inactive = next((u for u in st.session_state.users if u.email.lower() == email.strip().lower() and u.status_aktif == 0), None)
                if inactive:
                    st.error("Akun Anda dinonaktifkan. Hubungi Admin TU.")
                else:
                    st.error("Email atau password salah.")

        st.info("Akun contoh: admin@bem.com / admin123, bidang@bem.com / 123, departemen@bem.com / 123, bph@bem.com / 123")

    with tab_daftar:
        with st.form("form_register"):
            nama = st.text_input("Nama lengkap")
            email = st.text_input("Email baru")
            password = st.text_input("Password baru", type="password")
            no_hp = st.text_input("No HP")
            role_options = {f"{r.id_role} - {r.nama_role}": r for r in st.session_state.roles}
            selected_role_label = st.selectbox("Pilih Role", list(role_options.keys()))
            submitted = st.form_submit_button("Daftar")

        if submitted:
            role = role_options[selected_role_label]
            if not nama.strip() or not email.strip() or not password.strip():
                st.error("Nama, email, dan password wajib diisi.")
            elif any(u.email.lower() == email.strip().lower() for u in st.session_state.users):
                st.error("Email sudah terdaftar.")
            else:
                user_cls = ROLE_CLASS.get(role.nama_role, Mahasiswa)
                new_user = user_cls(
                    st.session_state.user_seq,
                    role,
                    1,
                    1,
                    nama.strip(),
                    email.strip(),
                    password,
                    no_hp.strip(),
                    departemen=st.session_state.departemen[0],
                )
                st.session_state.user_seq += 1
                st.session_state.users.append(new_user)
                st.success(f"Akun berhasil dibuat sebagai {role.nama_role}.")

def sidebar_user(user: Users) -> None:
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=120)
        else:
            st.markdown('<div class="sidebar-logo-title">UPN</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-title">Menu</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-name">{user.nama}</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">Divisi</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-value">{user.get_jenis_user()}</div>', unsafe_allow_html=True)

        if st.button("Logout", use_container_width=True):
            st.session_state.login_user_id = None
            st.rerun()


def guest_sidebar() -> None:
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=120)
        else:
            st.markdown('<div class="sidebar-logo-title">UPN</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-title">Menu</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-name">Sistem Surat BEM</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">Divisi</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-value">Login</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-info">Silakan login atau daftar akun baru untuk menggunakan sistem.</div>', unsafe_allow_html=True)

def mahasiswa_page(user: Users) -> None:
    menu = st.sidebar.radio("Pilih menu", ["Buat Surat", "Surat Saya", "Kirim Surat", "Upload Revisi", "Detail Surat", "Ubah Password"])

    if menu == "Buat Surat":
        st.header("Buat Surat Baru")
        if not st.session_state.templates:
            st.warning("Belum ada template surat.")
            return
        template_options = {f"{t.id_template} - {t.nama_template}": t for t in st.session_state.templates}
        with st.form("buat_surat"):
            tmpl = template_options[st.selectbox("Template", list(template_options.keys()))]
            st.text_area("Isi Template", value=tmpl.isi_template, height=90, disabled=True)
            judul = st.text_input("Judul surat")
            perihal = st.text_input("Perihal")
            isi = st.text_area("Isi surat", value=tmpl.isi_template, height=160)
            catatan = st.text_area("Catatan pengaju (opsional)", height=80)
            submitted = st.form_submit_button("Simpan Draft")
        if submitted:
            if not judul.strip() or not perihal.strip() or not isi.strip():
                st.error("Judul, perihal, dan isi surat wajib diisi.")
            else:
                sid = st.session_state.surat_seq
                nomor = f"BEM/{datetime.now().year}/{sid:03d}"
                surat = Surat(sid, nomor, tmpl.id_template, user.id_user, judul.strip(), perihal.strip(), isi.strip(), pengaju=user, catatan_pengaju=catatan.strip())
                surat.simpan_surat()
                st.session_state.surat_seq += 1
                st.session_state.surat.append(surat)
                st.success(f"Surat berhasil disimpan sebagai DRAFT. Nomor: {nomor}")

    elif menu == "Surat Saya":
        st.header("Surat Saya")
        data = [s for s in st.session_state.surat if s.id_pengaju == user.id_user]
        if data:
            st.dataframe(pd.DataFrame(surat_to_rows(data)), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada surat.")

    elif menu == "Kirim Surat":
        st.header("Kirim Surat")
        drafts = [s for s in st.session_state.surat if s.id_pengaju == user.id_user and s.status == StatusSurat.DRAFT]
        if not drafts:
            st.info("Tidak ada surat berstatus DRAFT.")
        else:
            options = {f"{s.id_surat} - {s.judul}": s for s in drafts}
            selected = options[st.selectbox("Pilih draft", list(options.keys()))]
            show_surat_detail(selected)
            if st.button("Kirim ke Bidang"):
                if selected.kirim_surat():
                    st.success("Surat berhasil dikirim. Status sekarang: Menunggu Bidang.")
                    st.rerun()
                else:
                    st.error("Surat gagal dikirim karena bukan status DRAFT.")

    elif menu == "Upload Revisi":
        st.header("Upload Revisi Surat")
        revisi_items = [s for s in st.session_state.surat if s.id_pengaju == user.id_user and s.status == StatusSurat.REVISI]
        if not revisi_items:
            st.info("Tidak ada surat berstatus REVISI.")
        else:
            options = {f"{s.id_surat} - {s.judul}": s for s in revisi_items}
            selected = options[st.selectbox("Pilih surat", list(options.keys()))]
            last_note = next((ap.catatan for ap in reversed(st.session_state.approvals) if ap.id_surat == selected.id_surat and ap.aksi == AksiApproval.REVISI), "-")
            st.warning(f"Catatan revisi terakhir: {last_note}")
            with st.form("form_revisi"):
                catatan = st.text_area("Catatan revisi Anda")
                file_name = st.text_input("Nama file revisi", placeholder="contoh: revisi_surat.pdf")
                submitted = st.form_submit_button("Kirim Revisi")
            if submitted:
                if not catatan.strip():
                    st.error("Catatan revisi wajib diisi.")
                else:
                    rev = SuratRevisi(st.session_state.revisi_seq, selected.id_surat, user.id_user, catatan.strip(), f"uploads/{file_name.strip() or 'revisi.pdf'}")
                    st.session_state.revisi_seq += 1
                    st.session_state.revisi.append(rev)
                    selected.riwayat_revisi.append(rev)
                    selected.ubah_status(StatusSurat.MENUNGGU_BIDANG)
                    st.success("Revisi berhasil dikirim. Status kembali ke Menunggu Bidang.")
                    st.rerun()

    elif menu == "Detail Surat":
        st.header("Detail Surat")
        mine = [s for s in st.session_state.surat if s.id_pengaju == user.id_user]
        if not mine:
            st.info("Belum ada surat.")
        else:
            options = {f"{s.id_surat} - {s.judul}": s for s in mine}
            show_surat_detail(options[st.selectbox("Pilih surat", list(options.keys()))])

    elif menu == "Ubah Password":
        password_page(user)


def approval_page(user: Users, role_name: str) -> None:
    stage_map = {
        "bidang": (StatusSurat.MENUNGGU_BIDANG, TahapApproval.BIDANG, "Bidang", StatusSurat.MENUNGGU_DEPARTEMEN),
        "departemen": (StatusSurat.MENUNGGU_DEPARTEMEN, TahapApproval.DEPARTEMEN, "Departemen", StatusSurat.MENUNGGU_BPH),
        "bph": (StatusSurat.MENUNGGU_BPH, TahapApproval.BPH, "BPH", StatusSurat.APPROVED),
    }
    target_status, tahap, label, _ = stage_map[role_name]
    st.header(f"Menu {label} - Cek Surat")
    items = [s for s in st.session_state.surat if s.status == target_status]
    if not items:
        st.info("Tidak ada surat yang perlu diproses.")
        return
    st.dataframe(pd.DataFrame(surat_to_rows(items)), use_container_width=True, hide_index=True)
    options = {f"{s.id_surat} - {s.judul}": s for s in items}
    selected = options[st.selectbox("Pilih surat", list(options.keys()))]
    show_surat_detail(selected)
    catatan = st.text_area("Catatan", key=f"catatan_{role_name}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Setujui", type="primary"):
            ap = Approval(st.session_state.approval_seq, selected.id_surat, user.id_user, tahap, st.session_state.approval_seq, catatan=catatan.strip() or "-")
            st.session_state.approval_seq += 1
            ap.proses(selected, AksiApproval.SETUJU)
            st.session_state.approvals.append(ap)
            st.success("Surat berhasil disetujui dan diteruskan.")
            st.rerun()
    with col2:
        if st.button("Minta Revisi"):
            ap = Approval(st.session_state.approval_seq, selected.id_surat, user.id_user, tahap, st.session_state.approval_seq, catatan=catatan.strip() or "Perlu revisi")
            st.session_state.approval_seq += 1
            ap.proses(selected, AksiApproval.REVISI)
            st.session_state.approvals.append(ap)
            st.warning("Surat dikembalikan untuk revisi.")
            st.rerun()


def admin_page(user: Users) -> None:
    menu = st.sidebar.radio(
        "Pilih menu",
        ["Dashboard Surat", "Proses Surat", "Detail Surat", "Kelola Template", "Kelola User", "Ubah Password"],
    )

    if menu == "Dashboard Surat":
        st.header("Semua Surat")
        if st.session_state.surat:
            st.dataframe(pd.DataFrame(surat_to_rows(st.session_state.surat)), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada surat.")

    elif menu == "Proses Surat":
        st.header("Proses Surat Admin TU")
        pending = [s for s in st.session_state.surat if is_pending(s.status)]
        if not pending:
            st.info("Tidak ada surat berstatus menunggu.")
            return
        st.dataframe(pd.DataFrame(surat_to_rows(pending)), use_container_width=True, hide_index=True)
        options = {f"{s.id_surat} - {s.judul} ({s.status.label})": s for s in pending}
        selected = options[st.selectbox("Pilih surat", list(options.keys()))]
        show_surat_detail(selected)
        tahap = st.selectbox("Tahap approval", list(TahapApproval), format_func=lambda x: x.value)
        catatan = st.text_area("Catatan", height=80)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Approve", type="primary"):
                proses_admin(user, selected, tahap, AksiApproval.SETUJU, catatan)
        with col2:
            if st.button("Minta Revisi"):
                proses_admin(user, selected, tahap, AksiApproval.REVISI, catatan or "Perlu revisi")
        with col3:
            if st.button("Tolak"):
                proses_admin(user, selected, tahap, AksiApproval.TOLAK, catatan or "Ditolak")

    elif menu == "Detail Surat":
        st.header("Detail Surat")
        if not st.session_state.surat:
            st.info("Belum ada surat.")
        else:
            options = {f"{s.id_surat} - {s.judul}": s for s in st.session_state.surat}
            show_surat_detail(options[st.selectbox("Pilih surat", list(options.keys()))])

    elif menu == "Kelola Template":
        st.header("Kelola Template Surat")
        st.dataframe(pd.DataFrame(template_to_rows()), use_container_width=True, hide_index=True)
        tab_add, tab_edit = st.tabs(["Tambah Template", "Edit Template"])
        with tab_add:
            with st.form("add_template"):
                nama = st.text_input("Nama template")
                deskripsi = st.text_input("Deskripsi")
                isi = st.text_area("Isi template", height=120)
                submitted = st.form_submit_button("Tambah")
            if submitted:
                if not nama.strip() or not isi.strip():
                    st.error("Nama dan isi template wajib diisi.")
                else:
                    st.session_state.templates.append(TemplateSurat(st.session_state.template_seq, nama.strip(), deskripsi.strip(), isi.strip()))
                    st.session_state.template_seq += 1
                    st.success("Template berhasil ditambahkan.")
                    st.rerun()
        with tab_edit:
            if st.session_state.templates:
                options = {f"{t.id_template} - {t.nama_template}": t for t in st.session_state.templates}
                selected = options[st.selectbox("Pilih template", list(options.keys()))]
                with st.form("edit_template"):
                    nama = st.text_input("Nama baru", value=selected.nama_template)
                    deskripsi = st.text_input("Deskripsi baru", value=selected.deskripsi)
                    isi = st.text_area("Isi baru", value=selected.isi_template, height=120)
                    submitted = st.form_submit_button("Simpan Perubahan")
                if submitted:
                    selected.edit_template(nama.strip(), isi.strip(), deskripsi.strip())
                    st.success("Template berhasil diperbarui.")
                    st.rerun()

    elif menu == "Kelola User":
        st.header("Kelola User")
        st.dataframe(pd.DataFrame(user_to_rows()), use_container_width=True, hide_index=True)
        target_options = {f"{u.id_user} - {u.nama} ({u.email})": u for u in st.session_state.users if u.id_user != user.id_user}
        if target_options:
            target = target_options[st.selectbox("Pilih user", list(target_options.keys()))]
            if st.button("Aktifkan / Nonaktifkan User"):
                target.status_aktif = 0 if target.status_aktif == 1 else 1
                st.success(f"Status {target.nama} sekarang: {'AKTIF' if target.status_aktif == 1 else 'NONAKTIF'}")
                st.rerun()
        else:
            st.info("Tidak ada user lain.")

    elif menu == "Ubah Password":
        password_page(user)


def proses_admin(user: Users, surat: Surat, tahap: TahapApproval, aksi: AksiApproval, catatan: str) -> None:
    if not is_pending(surat.status):
        st.error("Surat harus berstatus menunggu untuk diproses.")
        return
    ap = Approval(st.session_state.approval_seq, surat.id_surat, user.id_user, tahap, st.session_state.approval_seq, catatan=catatan.strip() or "-")
    st.session_state.approval_seq += 1
    ok = ap.proses(surat, aksi)
    st.session_state.approvals.append(ap)
    if ok:
        st.success(f"Aksi {aksi.value} berhasil. Status surat sekarang: {surat.status.label}")
        st.rerun()
    else:
        st.error("Gagal memproses surat. Cek status surat.")


def password_page(user: Users) -> None:
    st.header("Ubah Password")
    with st.form("change_password"):
        old = st.text_input("Password lama", type="password")
        new = st.text_input("Password baru", type="password")
        confirm = st.text_input("Konfirmasi password", type="password")
        submitted = st.form_submit_button("Ubah Password")
    if submitted:
        if not new:
            st.error("Password baru tidak boleh kosong.")
        elif new != confirm:
            st.error("Konfirmasi password tidak cocok.")
        elif user.ubah_password(old, new):
            st.success("Password berhasil diubah.")
        else:
            st.error("Password lama salah.")


def main() -> None:
    apply_custom_css()
    init_state()
    user = get_current_user()
    if not user:
        guest_sidebar()
        login_page()
        return

    sidebar_user(user)
    role = user.role.nama_role
    if role == "mahasiswa":
        mahasiswa_page(user)
    elif role in {"bidang", "departemen", "bph"}:
        approval_page(user, role)
    elif role == "admin_tu":
        admin_page(user)
    else:
        st.error("Role tidak dikenali.")


if __name__ == "__main__":
    main()
