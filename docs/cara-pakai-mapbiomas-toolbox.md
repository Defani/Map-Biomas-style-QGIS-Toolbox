# Cara Pakai MapBiomas ID Custom Visualization Toolbox (QGIS)

Toolbox ini mengubah raster tutupan lahan MapBiomas Indonesia menjadi **vektor polygon** yang sudah di-*dissolve* per kelas, lengkap dengan atribut nama kelas dan simbologi warna sesuai ATBD — tanpa perlu klasifikasi ulang manual.

## 0. Sumber Data Raster MapBiomas

Raster input (`.tif`) bisa didapat dari beberapa cara berikut:

**a. Jelajah online (dashboard)**
- https://plataforma.mapbiomas.org

**b. Unduh langsung — Collection 4 / 4.1 (1990–2024)**
- Portal: https://landy.mapbiomas.id/en/collectionmap

**c. Unduh langsung — Collection 3 (2000–2023), format GeoTIFF per tahun**
- Pola URL: `https://storage.googleapis.com/mapbiomas-public/initiatives/indonesia/collection_3/coverage/indonesia_coverage_<TAHUN>.tif`
- Contoh tahun 2022: https://storage.googleapis.com/mapbiomas-public/initiatives/indonesia/collection_3/coverage/indonesia_coverage_2022.tif
- Ganti `<TAHUN>` (2000–2023) sesuai kebutuhan.

**d. Unduh langsung — Collection 2 (2000–2022), format GeoTIFF per tahun**
- Pola URL: `https://storage.googleapis.com/mapbiomas-public/initiatives/indonesia/collection_2/coverage/indonesia_coverage_<TAHUN>.tif`
- Contoh tahun 2022: https://storage.googleapis.com/mapbiomas-public/initiatives/indonesia/collection_2/coverage/indonesia_coverage_2022.tif
- Ganti `<TAHUN>` (2000–2022) sesuai kebutuhan.

> **Catatan kompatibilitas:** tabel kelas (`MAPBIOMAS_CLASSES`) di dalam skrip toolbox ini mengacu pada legenda **Collection 4.1** (13 kelas, termasuk kode 76 untuk *Peat Swamp Forest*). Raster dari **Collection 2** kemungkinan memakai skema kelas yang lebih lama/berbeda, jadi sebagian kode kelas bisa muncul sebagai **"Tidak Diketahui"** di legenda bila tidak cocok. Untuk hasil paling akurat, gunakan raster **Collection 3, 4, atau 4.1**.

## 1. Persiapan

- Pastikan **QGIS** sudah terpasang (versi 3.x).
- Siapkan file raster MapBiomas Indonesia (format `.tif`) yang nilai pixel-nya berupa kode kelas (`gridcode`), misalnya 1, 3, 5, 18, dst.
- Salin file `mapbiomas_style_qgis_toolbox.py` ke folder skrip Processing QGIS, atau tambahkan sebagai *script* di Processing Toolbox.

## 2. Instalasi Skrip ke QGIS

1. Buka QGIS → menu **Processing** → **Toolbox**.
2. Klik ikon **Scripts** (gambar ular Python kecil) di bagian atas panel Toolbox.
3. Pilih **Add Script to Toolbox...**
4. Arahkan ke file `mapbiomas_style_qgis_toolbox.py`, lalu klik **Open**.
5. Skrip akan muncul di grup **MapBiomas ID Custom Visualization Toolbox** dengan nama **Simbolisasi Raster MapBiomas**.

> Alternatif: taruh file `startup.py` di folder profil QGIS (`~/.local/share/QGIS/QGIS3/profiles/default/python/startup.py`) agar skrip otomatis termuat setiap QGIS dibuka.

## 3. Menjalankan Tool

1. Cari **Simbolisasi Raster MapBiomas** di Processing Toolbox (bisa juga diketik di kolom pencarian).
2. Double-click untuk membuka jendela parameter.
3. Isi parameter:

| Parameter | Keterangan |
|---|---|
| **Raster MapBiomas Indonesia** | Pilih layer raster yang sudah dimuat di QGIS, atau browse file `.tif`. |
| **Band** | Band raster yang berisi kode kelas (default: Band 1). |
| **Output Vektor Polygon** | Lokasi & nama file output (`.shp` / `.gpkg`). Bisa juga "Save to temporary file". |
| **Muat ke kanvas dengan simbologi ATBD** | Centang agar hasil otomatis tampil di kanvas dengan warna resmi. |

4. Klik **Run**.

## 4. Apa yang Terjadi di Belakang Layar

Tool ini menjalankan 5 langkah otomatis:

1. **Polygonize** — raster diubah jadi vektor polygon, tiap pixel/cluster mendapat atribut `gridcode`.
2. **Dissolve** — polygon-polygon dengan `gridcode` yang sama digabung jadi satu (multipart) per kelas, sehingga hasil vektor lebih ringkas dan rapi (tidak pecah-pecah).
3. **Isi atribut** — ditambahkan kolom nama kelas (Inggris & Indonesia), kategori level 1, dan kode warna:
   - `class_id` (kode angka)
   - `class_en` (nama kelas — Inggris)
   - `class_id_b` (nama kelas — Indonesia)
   - `lv1_en`, `lv1_id` (kategori level atas)
   - `hex_color` (kode warna ATBD)
4. **Simbologi warna** — layer diwarnai otomatis sesuai standar ATBD MapBiomas.
5. **Legenda otomatis** — hanya menampilkan kelas yang benar-benar ada di data, dengan **teks nama kelas saja** (tanpa kode angka di depan).

## 5. Membaca Hasil

- Layer hasil bernama **"MapBiomas Indonesia LULC Map"** akan muncul di panel Layers.
- Buka **Layer Properties → Symbology** untuk melihat/mengubah kategori warna.
- Buka tabel atribut (klik kanan layer → **Open Attribute Table**) untuk melihat kolom `class_id`, `class_en`, `class_id_b`, `lv1_en`, `lv1_id`, `hex_color`.
- Jika ada kode kelas yang tidak dikenali di ATBD, akan muncul kategori **"Tidak Diketahui"** di legenda, dan peringatan di log Processing.

## 6. Tips

- Kalau raster berukuran besar, proses polygonize + dissolve bisa memakan waktu — biarkan progress bar berjalan sampai selesai.
- Simpan output sebagai `.gpkg` jika ingin menyimpan banyak layer dalam satu file.
- Warna dan nama kelas bisa disesuaikan langsung di bagian `MAPBIOMAS_CLASSES` pada skrip jika ATBD berubah.

## Kredit

Skrip asli oleh **Defani Arman Alfitriansyah** ([github.com/Defani](https://github.com/Defani)).
