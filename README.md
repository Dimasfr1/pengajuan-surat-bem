# Sistem Manajemen Surat BEM - Python Streamlit

Program ini adalah hasil konversi dari versi C++ OOP menjadi Python OOP dengan GUI Streamlit.

## Cara Menjalankan

1. Install library:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

## Akun Default

- Admin TU: `admin@bem.com` / `admin123`
- Bidang: `bidang@bem.com` / `123`
- Departemen: `departemen@bem.com` / `123`
- BPH: `bph@bem.com` / `123`

Mahasiswa bisa dibuat lewat menu **Daftar Akun Baru**.

## Fitur

- Login dan daftar akun
- OOP dengan inheritance: Mahasiswa, PengurusBidang, PengurusDepartemen, BPH, AdminTU
- Buat surat sebagai draft
- Kirim surat dari mahasiswa ke alur approval
- Approval bidang, departemen, BPH, dan admin TU
- Minta revisi dan upload revisi
- Kelola template surat
- Kelola user aktif/nonaktif
- Ubah password

Catatan: Data tersimpan di `st.session_state`, jadi data akan reset saat aplikasi direstart.
