import tkinter as tk
from tkinter import messagebox
import random
import webbrowser
import urllib.parse  # Untuk encode pesan WhatsApp

class PenitipanBarangApp:
    def __init__(self, master):
        self.master = master
        master.title("Aplikasi Penitipan Barang Sekolah")
        master.geometry("900x700")

        self.data_barang = {}
        self.lemari_tersedia = [f"LMR-{i:03d}" for i in range(1, 13)]

        self.create_widgets()
        self.update_status_lemari()

    def create_widgets(self):
        self.frame_admin = tk.LabelFrame(self.master, text="Panel Admin: Penitipan Barang", padx=20, pady=20, bg="#e0ffe0")
        self.frame_admin.pack(pady=15, padx=15, fill="x")

        tk.Label(self.frame_admin, text="Nama Siswa:", bg="#e0ffe0").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nama_siswa = tk.Entry(self.frame_admin, width=40, font=("Arial", 10))
        self.entry_nama_siswa.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(self.frame_admin, text="Nomor WA Siswa (cth: 628123456789):", bg="#e0ffe0").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nomor_wa = tk.Entry(self.frame_admin, width=40, font=("Arial", 10))
        self.entry_nomor_wa.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.frame_admin, text="Deskripsi Barang (cth: Tas Sekolah, Buku Matematika):", bg="#e0ffe0").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_deskripsi_barang = tk.Entry(self.frame_admin, width=40, font=("Arial", 10))
        self.entry_deskripsi_barang.grid(row=2, column=1, pady=5, padx=5)

        self.btn_titip = tk.Button(self.frame_admin, text="Titipkan Barang", command=self.titipkan_barang,
                                   bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), relief="raised", padx=10, pady=5)
        self.btn_titip.grid(row=3, column=0, columnspan=2, pady=15)

        self.frame_status = tk.LabelFrame(self.master, text="Status Lemari", padx=10, pady=10, bg="#f0f8ff")
        self.frame_status.pack(pady=15, padx=15, fill="both", expand=True)

        self.canvas_lemari = tk.Canvas(self.frame_status, borderwidth=0, background="#f0f8ff")
        self.vsb_lemari = tk.Scrollbar(self.frame_status, orient="vertical", command=self.canvas_lemari.yview)
        self.canvas_lemari.configure(yscrollcommand=self.vsb_lemari.set)

        self.vsb_lemari.pack(side="right", fill="y")
        self.canvas_lemari.pack(side="left", fill="both", expand=True)

        self.inner_frame_lemari = tk.Frame(self.canvas_lemari, background="#f0f8ff")
        self.canvas_lemari.create_window((0, 0), window=self.inner_frame_lemari, anchor="nw")
        self.inner_frame_lemari.bind("<Configure>", self.on_frame_configure)

        self.frame_siswa = tk.LabelFrame(self.master, text="Simulasi Antarmuka Siswa: Pengambilan Barang", padx=20, pady=20, bg="#fff0e0")
        self.frame_siswa.pack(pady=15, padx=15, fill="x")

        tk.Label(self.frame_siswa, text="Masukkan ID Barang yang akan diambil:", bg="#fff0e0").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_id_barang_ambil = tk.Entry(self.frame_siswa, width=30, font=("Arial", 10))
        self.entry_id_barang_ambil.grid(row=0, column=1, pady=5, padx=5)

        self.btn_ambil = tk.Button(self.frame_siswa, text="Ambil Barang (Konfirmasi)", command=self.ambil_barang,
                                   bg="#FFC107", fg="black", font=("Arial", 10, "bold"), relief="raised", padx=10, pady=5)
        self.btn_ambil.grid(row=0, column=2, padx=10)

    def on_frame_configure(self, event):
        self.canvas_lemari.configure(scrollregion=self.canvas_lemari.bbox("all"))

    def update_status_lemari(self):
        for widget in self.inner_frame_lemari.winfo_children():
            widget.destroy()

        row, col = 0, 0
        max_cols = 4

        all_lemari_nums = sorted(list(set(self.lemari_tersedia + [d['lemari'] for d in self.data_barang.values() if d['status'] == 'dititipkan'])))

        for lemari in all_lemari_nums:
            status = "Kosong"
            info_barang = ""
            bg_color = "#e0ffe0"

            for id_barang, data in self.data_barang.items():
                if data['lemari'] == lemari and data['status'] == 'dititipkan':
                    status = "Terisi"
                    info_barang = f"Barang: {data['deskripsi']}\nSiswa: {data['siswa']}\nID: {id_barang}"
                    bg_color = "#ffdddd"
                    break

            frame_lemari = tk.Frame(self.inner_frame_lemari, borderwidth=1, relief="solid", bg=bg_color, padx=10, pady=10)
            frame_lemari.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            tk.Label(frame_lemari, text=f"Lemari: {lemari}", font=("Arial", 10, "bold"), bg=bg_color).pack()
            tk.Label(frame_lemari, text=f"Status: {status}", bg=bg_color).pack()
            if info_barang:
                tk.Label(frame_lemari, text=info_barang, font=("Arial", 9), bg=bg_color).pack()

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        for i in range(max_cols):
            self.inner_frame_lemari.grid_columnconfigure(i, weight=1)

    def titipkan_barang(self):
        nama_siswa = self.entry_nama_siswa.get().strip()
        nomor_wa = self.entry_nomor_wa.get().strip()
        deskripsi_barang = self.entry_deskripsi_barang.get().strip()

        if not nama_siswa or not nomor_wa or not deskripsi_barang:
            messagebox.showwarning("Input Kurang", "Mohon lengkapi semua kolom: Nama Siswa, Nomor WA, dan Deskripsi Barang.")
            return

        if not (nomor_wa.isdigit() and len(nomor_wa) >= 10):
            messagebox.showwarning("Format Nomor WA Salah", "Nomor WA harus angka dan minimal 10 digit.")
            return

        if not self.lemari_tersedia:
            messagebox.showerror("Lemari Penuh", "Maaf, semua lemari sedang terisi. Tidak bisa penitipan baru.")
            return

        while True:
            id_barang = f"BRG-{random.randint(1000, 9999)}"
            if id_barang not in self.data_barang:
                break

        no_lemari = self.lemari_tersedia.pop(0)

        self.data_barang[id_barang] = {
            'siswa': nama_siswa,
            'lemari': no_lemari,
            'status': 'dititipkan',
            'deskripsi': deskripsi_barang,
            'nomor_wa': nomor_wa
        }

        messagebox.showinfo("Berhasil", f"Barang '{deskripsi_barang}' untuk '{nama_siswa}' telah dititipkan di lemari {no_lemari}.\nID Barang Anda: {id_barang}")
        self.kirim_notifikasi_wa(id_barang, nama_siswa, no_lemari, nomor_wa)

        self.entry_nama_siswa.delete(0, tk.END)
        self.entry_nomor_wa.delete(0, tk.END)
        self.entry_deskripsi_barang.delete(0, tk.END)
        self.update_status_lemari()

    def kirim_notifikasi_wa(self, id_barang, nama_siswa, no_lemari, nomor_wa):
        pesan_wa = (
            f"Halo {nama_siswa},\n\n"
            f"Barang Anda dengan ID {id_barang} ({self.data_barang[id_barang]['deskripsi']}) "
            f"telah dititipkan di lemari {no_lemari}.\n\n"
            f"Anda bisa mengambilnya sekarang. Mohon masukkan ID barang Anda ({id_barang}) "
            f"di aplikasi penitipan barang untuk konfirmasi pengambilan.\n\n"
            f"Terima kasih."
        )

        if messagebox.askyesno("Simulasi Notifikasi WhatsApp",
                               f"Sebuah notifikasi WA akan dikirim ke {nama_siswa} ({nomor_wa}).\n\n"
                               f"Isi Pesan:\n{pesan_wa}\n\n"
                               f"Kirim notifikasi ini sekarang (akan membuka browser/aplikasi WA)?"):

            if nomor_wa.startswith("0"):
                nomor_wa_formatted = "62" + nomor_wa[1:]
            elif not nomor_wa.startswith("62"):
                nomor_wa_formatted = "62" + nomor_wa
            else:
                nomor_wa_formatted = nomor_wa

            encoded_pesan = urllib.parse.quote(pesan_wa)
            wa_link = f"https://wa.me/{nomor_wa_formatted}?text={encoded_pesan}"

            try:
                webbrowser.open(wa_link)
                messagebox.showinfo("Notifikasi Terkirim", "Tautan WhatsApp telah dibuka di browser/aplikasi WA Anda.")
            except Exception as e:
                messagebox.showerror("Gagal Membuka WhatsApp", f"Tidak dapat membuka tautan WhatsApp: {e}")
        else:
            messagebox.showinfo("Info Notifikasi", "Notifikasi WA tidak dikirim (dibatalkan oleh admin).")

    def ambil_barang(self):
        id_barang_input = self.entry_id_barang_ambil.get().strip()

        if not id_barang_input:
            messagebox.showwarning("Input Kosong", "Mohon masukkan ID Barang yang akan diambil.")
            return

        if id_barang_input in self.data_barang:
            barang = self.data_barang[id_barang_input]
            if barang['status'] == 'dititipkan':
                konfirmasi = messagebox.askyesno("Konfirmasi Pengambilan",
                                                 f"Anda yakin ingin mengambil barang '{barang['deskripsi']}' milik {barang['siswa']} dari lemari {barang['lemari']}?")
                if konfirmasi:
                    barang['status'] = 'diambil'
                    self.lemari_tersedia.append(barang['lemari'])
                    self.lemari_tersedia.sort()
                    messagebox.showinfo("Berhasil", f"Barang '{barang['deskripsi']}' telah berhasil diambil dari lemari {barang['lemari']}.")
                    self.entry_id_barang_ambil.delete(0, tk.END)
                    self.update_status_lemari()
            else:
                messagebox.showinfo("Status Barang", "Barang ini sudah diambil sebelumnya atau tidak dititipkan.")
        else:
            messagebox.showerror("Barang Tidak Ditemukan", "ID Barang tidak ditemukan. Pastikan Anda memasukkan ID yang benar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PenitipanBarangApp(root)
    root.mainloop()
