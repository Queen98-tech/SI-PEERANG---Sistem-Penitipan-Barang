# SI-PERANG---Sistem-Penitipan-Barang
Panduan untuk menjalankan program :

# *1. Kebutuhan Sistem*

###  a. Python

* Versi *3.x* (rekomendasi: Python 3.8 atau lebih baru).
* Cek versi Python di terminal atau CMD:

  bash
  python --version
  

###  b. Library yang Digunakan

* *tkinter* : Untuk GUI.
* *webbrowser* : Untuk membuka link WhatsApp (juga bawaan Python).
* *urllib.parse* : Untuk encode URL (juga bawaan Python).
* *random* : Untuk membuat ID unik.
* *messagebox* : Termasuk dalam tkinter.

 *Semuanya sudah tersedia di python jadi tidak perlu install library tambahan.

---

##  *2. Cara Menjalankan Kode*

###  a. Simpan kode ke file Python

Simpan kode Python tersebut sebagai file, misalnya:


penitipan_barang.py


###  b. Jalankan file

Buka terminal atau command prompt : arahkan ke folder file tersebut lalu jalankan:

bash
python penitipan_barang.py


Jika kamu menggunakan VSCode : cukup klik kanan file dan pilih (Run) Python File in Terminal*.

---

##  *3. Fungsi Program*

###  Mode admin

* Memasukkan data:

  * Nama siswa
  * Nomor WhatsApp siswa (contoh: 628123456789)
  * Deskripsi barang
* Menekan tombol (Titipkan barang) akan:

  * Menyimpan data
  * Menempatkan barang di salah satu lemari (maksimal 12)
  * Mengirim *simulasi notifikasi WhatsApp* melalui browser (pakai wa.me)

###  Panel Status Lemari

* Menampilkan semua lemari dan statusnya:

  * Kosong (hijau muda)
  * Terisi (merah muda) dengan informasi nama siswa, deskripsi , dan ID barang

###  Panel Siswa

* Siswa dapat memasukkan *ID Barang*
* Klik tombol Ambil barang (Konfirmasi)

  * Jika ID valid dan statusnya "dititipkan", maka akan dikonfirmasi untuk diambil
  * Lemari menjadi kosong lagi dan tersedia untuk barang lain

---

##  *4. Catatan Tambahan*

* Aplikasi ini "Belum Menyimpan di Database" ,jadi data akan hilang jika aplikasi ditutup.
* ID Barang seperti BRG-1234 dihasilkan secara acak untuk tiap penitipan.
* Notifikasi tidak benar-benar memberikan notifikasi ke siswa melainkan membuka whatsapp sesuai nomor siswa.
