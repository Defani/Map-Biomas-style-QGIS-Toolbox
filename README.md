# MapBiomas ID Style — QGIS Toolbox

Toolbox QGIS untuk simbolisasi otomatis raster **MapBiomas Indonesia** menjadi vektor polygon berlabel dan berwarna sesuai kelas tutupan lahan (LULC).

> **Catatan:** Toolbox ini dibuat sebagai bentuk apresiasi terhadap proyek MapBiomas Indonesia dan untuk memudahkan pengguna QGIS dalam memvisualisasikan data tutupan lahan tanpa perlu setting simbologi manual. Semua kredit data sepenuhnya milik tim **MapBiomas Indonesia**.

---

## Fitur

- Konversi raster MapBiomas ke vektor polygon secara otomatis (*polygonize*)
- Pengisian atribut lengkap: kode kelas, nama kelas (EN/ID), level 1, dan warna hex
- Simbologi warna otomatis sesuai ATBD MapBiomas Indonesia
- **Legenda dinamis** — hanya kelas yang benar-benar ada di data yang ditampilkan
- Tombol cepat **MapBiomas ID Style** langsung di toolbar QGIS

---

## Struktur File

```
Map-Biomas-style-QGIS-Toolbox/
├── mapbiomas_style_qgis_toolbox.py   # Script Processing utama
├── startup.py                         # Script auto-load tombol toolbar
└── README.md
```

---

## Instalasi

### 0. Download Toolbox

Download semua file dari repository ini:

```
mapbiomas_01_raster_to_vector.py   ← script utama
startup.py                         ← tombol toolbar (opsional)
```

Klik tombol **Code → Download ZIP** di halaman GitHub ini, lalu ekstrak.

---

### 1. Script Processing

Salin `mapbiomas_01_raster_to_vector.py` ke folder Scripts Processing QGIS:

| OS | Path |
|---|---|
| Windows | `C:\Users\<nama>\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\scripts\` |
| Linux / macOS | `~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts/` |

Atau buka langsung dari QGIS:
**Processing Toolbox → Scripts (ikon roda gigi) → Open Scripts Folder**

### 2. Tombol Toolbar (Opsional)

Salin `startup.py` ke folder Python startup QGIS:

| OS | Path |
|---|---|
| Windows | `C:\Users\<nama>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\startup.py` |
| Linux / macOS | `~/.local/share/QGIS/QGIS3/profiles/default/python/startup.py` |

Setelah QGIS dibuka ulang, tombol **MapBiomas ID Style** akan muncul otomatis di toolbar.

---

## Cara Pakai

1. Buka QGIS dan muat raster MapBiomas Indonesia
2. Jalankan tool melalui salah satu cara:
   - Klik tombol **MapBiomas ID Style** di toolbar, atau
   - Buka **Processing Toolbox → MapBiomas ID Custom Visualization Toolbox → Simbolisasi Raster MapBiomas**
3. Isi parameter:

| Parameter | Keterangan |
|---|---|
| Raster MapBiomas Indonesia | Layer raster input |
| Band | Band yang digunakan (default: Band 1) |
| Output Vektor Polygon | Lokasi simpan file output |
| Muat ke kanvas | Centang untuk langsung tampil dengan simbologi |

4. Klik **Run** — layer vektor akan otomatis dimuat ke kanvas dengan simbologi dan legenda sesuai kelas yang ada di data.

---

## Kelas Tutupan Lahan (LULC)

Skema kelas dan warna mengacu pada **MapBiomas Indonesia Collection 4**.
Sumber: [Integration and Layers MB Indonesia - Col 4 - EN.pdf](https://landy.mapbiomas.id/assets/legendcode/Integration%20and%20Layers%20MB%20Indonesia%20-%20Col%204%20-%20EN%20.pdf)

| ID | Kelas (EN) | Kelas (ID) | Level 1 | Hex | Warna |
|:---:|---|---|---|:---:|:---:|
| **1** | **Forest** | **Hutan** | — | `#1f8d49` | ![](https://img.shields.io/badge/■-1f8d49?style=flat&color=1f8d49) |
| 3 | Forest Formation | Formasi Hutan | Forest | `#1f8d49` | ![](https://img.shields.io/badge/■-1f8d49?style=flat&color=1f8d49) |
| 5 | Mangrove | Mangrove | Forest | `#04381d` | ![](https://img.shields.io/badge/■-04381d?style=flat&color=04381d) |
| 76 | Peat Swamp Forest | Hutan Rawa Gambut | Forest | `#2f7360` | ![](https://img.shields.io/badge/■-2f7360?style=flat&color=2f7360) |
| **10** | **Non-Forest Natural Formation** | **Tumbuhan Non-Hutan** | — | `#d6bc74` | ![](https://img.shields.io/badge/■-d6bc74?style=flat&color=d6bc74) |
| 13 | Non-Forest Natural Vegetation | Tumbuhan Non-Hutan Lainnya | Non-Forest Natural Formation | `#d89f5c` | ![](https://img.shields.io/badge/■-d89f5c?style=flat&color=d89f5c) |
| **18** | **Agriculture** | **Pertanian** | — | `#E974ED` | ![](https://img.shields.io/badge/■-E974ED?style=flat&color=E974ED) |
| 40 | Rice Paddy | Sawah | Agriculture | `#f272c2` | ![](https://img.shields.io/badge/■-f272c2?style=flat&color=f272c2) |
| 35 | Oil Palm | Sawit | Agriculture | `#9065d0` | ![](https://img.shields.io/badge/■-9065d0?style=flat&color=9065d0) |
| 9 | Pulpwood Plantation | Kebun Kayu | Agriculture | `#7a5900` | ![](https://img.shields.io/badge/■-7a5900?style=flat&color=7a5900) |
| 21 | Other Agriculture | Pertanian Lainnya | Agriculture | `#ffefc3` | ![](https://img.shields.io/badge/■-ffefc3?style=flat&color=ffefc3) |
| **22** | **Non-Vegetated Area** | **Non-Vegetasi** | — | `#d4271e` | ![](https://img.shields.io/badge/■-d4271e?style=flat&color=d4271e) |
| 30 | Mining Pit | Lubang Tambang | Non-Vegetated Area | `#9c0027` | ![](https://img.shields.io/badge/■-9c0027?style=flat&color=9c0027) |
| 24 | Urban Area | Permukiman | Non-Vegetated Area | `#d4271e` | ![](https://img.shields.io/badge/■-d4271e?style=flat&color=d4271e) |
| 25 | Other Non-Vegetation | Non-Vegetasi Lainnya | Non-Vegetated Area | `#db4d4f` | ![](https://img.shields.io/badge/■-db4d4f?style=flat&color=db4d4f) |
| **26** | **Water Body** | **Tubuh Air** | — | `#2532e4` | ![](https://img.shields.io/badge/■-2532e4?style=flat&color=2532e4) |
| 31 | Aquaculture | Tambak | Water Body | `#091077` | ![](https://img.shields.io/badge/■-091077?style=flat&color=091077) |
| 33 | River, Lake, Ocean | Sungai, Danau, Laut | Water Body | `#2532e4` | ![](https://img.shields.io/badge/■-2532e4?style=flat&color=2532e4) |
| **27** | **Not Observed** | **Citra Tertutup Awan** | — | `#ffffff` | ![](https://img.shields.io/badge/■-ffffff?style=flat&color=ffffff) |

---

## Atribut Output

Layer vektor hasil proses memiliki kolom berikut:

| Field | Tipe | Keterangan |
|---|---|---|
| `gridcode` | Integer | Kode kelas dari raster (hasil polygonize) |
| `class_id` | Integer | Kode kelas MapBiomas |
| `class_en` | String | Nama kelas dalam Bahasa Inggris |
| `class_id_b` | String | Nama kelas dalam Bahasa Indonesia |
| `lv1_en` | String | Nama Level 1 (EN) |
| `lv1_id` | String | Nama Level 1 (ID) |
| `hex_color` | String | Kode warna hex kelas |

---

## Download Data MapBiomas

Data raster tutupan lahan MapBiomas Indonesia dapat diunduh langsung dari platform resmi MapBiomas:

**[Klik di sini — MapBiomas Platform Indonesia LULC](https://plataforma.mapbiomas.org/coverage/coverage_lclu?t[regionKey]=indonesia&t[ids][]=4-1-1&t[divisionCategoryId]=2&tl[id]=4&tl[themeKey]=coverage&tl[subthemeKey]=coverage_lclu&tl[legendKey]=default&tl[year]=2024&tl[pixelValues][]=3&tl[pixelValues][]=5&tl[pixelValues][]=76&tl[pixelValues][]=13&tl[pixelValues][]=40&tl[pixelValues][]=35&tl[pixelValues][]=9&tl[pixelValues][]=21&tl[pixelValues][]=30&tl[pixelValues][]=24&tl[pixelValues][]=25&tl[pixelValues][]=31&tl[pixelValues][]=33&tl[pixelValues][]=27)**

Link di atas sudah dikonfigurasi untuk wilayah Indonesia dengan seluruh kelas LULC yang didukung toolbox ini. Pilih tahun yang diinginkan lalu unduh dalam format GeoTIFF.

> Data, metodologi, dan seluruh hak cipta sepenuhnya milik **MapBiomas Indonesia**. Toolbox ini hanya alat bantu visualisasi di QGIS dan tidak berafiliasi secara resmi dengan MapBiomas.

---

## Persyaratan

- QGIS 3.x
- Plugin **GDAL** (sudah termasuk di instalasi QGIS standar)
- Data raster MapBiomas Indonesia (lihat bagian **Download Data** di atas)

---

## Daftar Pustaka

Toolbox ini menggunakan skema warna dan klasifikasi kelas yang mengacu pada dokumen metodologi resmi MapBiomas Indonesia:

1. **MapBiomas Indonesia** (2023). *Algorithm Theoretical Basis Document (ATBD) MapBiomas Indonesia Koleksi 3.0*. MapBiomas Indonesia. Tersedia di: [landy.mapbiomas.id/assets/files/ATBD%20MapBiomas%20ID%20Col%203.0.pdf](https://landy.mapbiomas.id/assets/files/ATBD%20MapBiomas%20ID%20Col%203.0.pdf)

2. **MapBiomas Network** (2025). *MapBiomas General "Handbook" Algorithm Theoretical Basis Document (ATBD)*. MapBiomas. Tersedia di: [brasil.mapbiomas.org](https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/02/ATBD-Collection-9-versao2-v2.pdf)

3. **MapBiomas Indonesia Platform**. *Methodology — Land Use and Land Cover Mapping*. Tersedia di: [nusantara.earth/methodologymosaic](https://nusantara.earth/methodologymosaic)

4. **MapBiomas Indonesia**. *Platform Tutupan dan Penggunaan Lahan Indonesia*. Tersedia di: [mapbiomas.nusantara.earth](https://mapbiomas.nusantara.earth/)

---

## Penulis

**Defani Arman Alfitriansyah**
[github.com/Defani](https://github.com/Defani)

---

## Lisensi

Proyek ini bersifat open source dan bebas digunakan untuk keperluan riset, pendidikan, dan pemetaan tutupan lahan.
