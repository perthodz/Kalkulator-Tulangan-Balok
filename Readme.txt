# 🏗️ Kalkulator Analisis Tulangan Balok Beton Berdasarkan SNI

Aplikasi berbasis web interaktif untuk melakukan pengecekan keamanan desain penampang balok beton bertulang (lentur dan geser) berdasarkan standar perencanaan struktur. Proyek ini dibuat sebagai pemenuhan Tugas Mata Kuliah Aplikasi Komputer Teknik Sipil.

---

## 🚀 Fitur Utama
* **Input Data Fleksibel:** Pengguna dapat memasukkan parameter bahan struktur, dimensi balok, gaya rencana (dari ETABS/SAP2000), hingga rencana tulangan terpasang secara langsung tanpa ribet.
* **Analisis Tulangan Tumpuan & Lapangan:** Menghitung kapasitas momen nominal ($\phi M_n$) dan membandingkannya secara otomatis dengan momen rencana ($M_u$) lengkap dengan indikator status aman/tidak.
* **Pengecekan Kebutuhan & Kapasitas Geser:** Mengecek apakah penampang memerlukan tulangan geser khusus berdasarkan sumbangan kekuatan beton ($\phi V_c$) serta mengevaluasi kapasitas total sengkang terpasang ($\phi V_n$).
* **Antarmuka Modern & Responsif:** Dibangun menggunakan framework **Streamlit** dengan desain *Clean UI/UX* ala kalkulator teknik modern.

---

## 📖 Panduan Penggunaan Aplikasi

Berikut adalah langkah-langkah untuk menggunakan kalkulator ini, khususnya jika Anda menggunakan output data dari *software* analisis struktur seperti **ETABS** atau **SAP2000**:

### 1. Masukkan Data Perencanaan
* **Bahan Struktur:** Tentukan mutu beton ($f_c'$) serta tegangan leleh tulangan baja lentur ($f_y$) dan geser ($f_{ys}$).
* **Dimensi Balok:** Masukkan ukuran penampang (Lebar $b$ dan Tinggi $h$), ukuran tulangan yang akan dianalisis, dan tebal selimut beton.

### 2. Cara Mengambil Data Gaya Rencana dari ETABS / SAP2000
Buka model struktur Anda yang sudah di- *Run Analysis*, lalu ikuti langkah ini:
* **Momen Positif ($M_{u+}$) & Negatif ($M_{u-}$):**
  1. Klik menu `Display` > `Show Forces/Stresses` > `Frame/Pier/Spandrel/Link Forces`.
  2. Pilih kombinasi pembebanan ultimate (misal: `1.2D + 1.6L` atau kombinasi gempa).
  3. Centang bagian **Moment 3-3**.
  4. Lihat diagram momen pada balok yang ditinjau. Masukkan **momen maksimum positif** (biasanya di tengah bentang) ke kolom $M_{u+}$ dan **momen maksimum negatif** (biasanya di tumpuan) ke kolom $M_{u-}$.
* **Gaya Geser ($V_u$):**
  1. Pada menu yang sama, ubah pilihan dari *Moment 3-3* menjadi **Shear 2-2**.
  2. Ambil nilai gaya geser ultimate terbesar (biasanya berada di ujung perletakan balok) dan masukkan ke kolom $V_u$.

### 3. Masukkan Rencana Tulangan & Cek Keamanan
* Input jumlah dan diameter tulangan yang ingin Anda pasang pada area tumpuan, lapangan, dan geser (sengkang).
* Klik tombol **"Hitung & Cek Keamanan"** untuk melihat laporan kapasitas penampang secara detail.

---

## 🛠️ Teknologi yang Digunakan
* **Python** (Bahasa Pemrograman Utama)
* **Streamlit** (Framework Web App)
* **Pandas & Math** (Komputasi dan Analisis Struktur)

---

## ⚙️ Cara Menjalankan Secara Lokal (Local Development)

Jika ingin menjalankan kode ini di komputer lokal melalui VS Code:

1. Clone atau unduh repositori ini.
2. Pastikan Python sudah terinstal di komputer Anda.
3. Instal *library* yang dibutuhkan melalui terminal:
   ```bash
   pip install -r requirements.txt