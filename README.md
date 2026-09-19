# MapBiomas ID Style — QGIS Toolbox

Toolbox QGIS untuk simbolisasi otomatis raster **MapBiomas Indonesia** menjadi vektor polygon berlabel dan berwarna sesuai kelas tutupan lahan (LULC).

> **Catatan:** Toolbox ini dibuat sebagai bentuk apresiasi terhadap proyek MapBiomas Indonesia dan untuk memudahkan pengguna QGIS dalam memvisualisasikan data tutupan lahan tanpa perlu setting simbologi manual. Semua kredit data sepenuhnya milik tim **MapBiomas Indonesia**.

---

## Sistem Kerja

Toolbox ini adalah tahap **post-processing dan visualisasi**: input berupa raster klasifikasi MapBiomas yang sudah jadi (nilai piksel = kode kelas / `gridcode`), bukan alat klasifikasi citra. Seluruh proses berjalan sebagai satu algoritma QGIS Processing (`MapBiomasRasterToVectorAlgorithm`).

### 1. Alur kerja lengkap

```mermaid
%%{init: {"theme": "base", "themeVariables": {"background": "transparent"}, "flowchart": {"htmlLabels": true}}, "themeCSS": ".background { fill: none !important; }"}%%
flowchart TB
    subgraph INSTALL["0 · Instalasi (sekali saja)"]
        I1["Processing Toolbox → Add Script to Toolbox<br/>mapbiomas_style_qgis_toolbox.py"]
        I2["startup.py (opsional)<br/>menambah tombol setelah QGIS terbuka ± 3 detik"]
        I3["Tombol toolbar<br/>MapBiomas ID Style"]
        I2 --> I3
    end

    T["Processing Toolbox<br/>MapBiomas ID Custom Visualization Toolbox<br/>→ Simbolisasi Raster MapBiomas"]
    I1 --> T

    PARAM["1 · Dialog parameter<br/>INPUT_RASTER: raster MapBiomas (.tif)<br/>BAND: default 1<br/>OUTPUT_VECTOR: default GeoJSON, bisa .gpkg atau .shp<br/>LOAD_TO_CANVAS: default aktif"]
    T --> PARAM
    I3 -->|"execAlgorithmDialog"| PARAM

    subgraph PROC["2 · processAlgorithm() — MapBiomasRasterToVectorAlgorithm"]
        S1["Langkah 1/5 · Polygonize<br/>gdal:polygonize → field gridcode<br/>progres 20"]
        S2["Langkah 2/5 · Dissolve per kelas<br/>native:dissolve, FIELD = gridcode<br/>GeoPackage sementara, progres 30"]
        S3["Langkah 3/5 · Tambah field<br/>class_id, class_en, class_id_b,<br/>lv1_en, lv1_id, hex_color<br/>progres 38"]
        S4["Langkah 4/5 · Isi atribut tiap fitur<br/>lookup gridcode ke MAPBIOMAS_CLASSES<br/>progres 38 sampai 75"]
        UNK{"gridcode ada di<br/>MAPBIOMAS_CLASSES?"}
        UN["Unknown / Tidak Diketahui<br/>warna abu-abu + peringatan di log"]
        S5["Langkah 5/5 · Simpan<br/>native:savefeatures → OUTPUT_VECTOR<br/>progres 92"]
        S1 --> S2 --> S3 --> S4 --> UNK
        UNK -->|"ya"| S5
        UNK -->|"tidak"| UN --> S5
    end

    PARAM -->|"Run"| S1

    subgraph LOOKUP["Lookup table internal"]
        C["MAPBIOMAS_CLASSES<br/>gridcode → nama EN/ID, level 1, warna hex"]
        D["LEGEND_ORDER<br/>urutan kategori di legenda"]
    end
    C --> S4
    C --> SYM
    D --> SYM

    S5 --> E["3 · Output file<br/>vektor polygon per kelas<br/>+ 7 kolom atribut"]
    S5 --> LOAD{"LOAD_TO_CANVAS<br/>aktif?"}
    LOAD -->|"tidak"| STOP["Selesai<br/>hanya file output"]
    LOAD -->|"ya"| SYM["_apply_symbology()<br/>1. kumpulkan gridcode unik yang ada di data<br/>2. urutkan sesuai LEGEND_ORDER<br/>3. satu QgsRendererCategory per kelas, label = nama kelas<br/>4. QgsCategorizedSymbolRenderer"]
    SYM --> F["Layer MapBiomas Indonesia LULC Map di kanvas<br/>simbologi + legenda dinamis (hanya kelas yang ada)"]
```

### 2. Urutan eksekusi

```mermaid
%%{init: {"theme": "base", "themeVariables": {"background": "transparent"}}, "themeCSS": ".background { fill: none !important; }"}%%
sequenceDiagram
    autonumber
    actor User
    participant QGIS as QGIS (Toolbox / toolbar)
    participant Alg as MapBiomasRasterToVectorAlgorithm
    participant GDAL as gdal:polygonize
    participant Native as native:dissolve / savefeatures
    participant Sym as _apply_symbology()

    opt Lewat tombol toolbar (startup.py)
        User->>QGIS: klik MapBiomas ID Style
        QGIS->>QGIS: cari algoritma mapbiomas_raster_to_vector, lalu execAlgorithmDialog
    end
    User->>QGIS: pilih raster, band, output, opsi kanvas, lalu Run
    QGIS->>Alg: processAlgorithm(parameters)
    Alg->>GDAL: polygonize(raster, band, FIELD = gridcode)
    GDAL-->>Alg: polygon hasil konversi piksel (temporary)
    Alg->>Native: dissolve(FIELD = gridcode) ke GeoPackage sementara
    Native-->>Alg: polygon per kelas
    Alg->>Alg: tambah 6 field (class_id, class_en, class_id_b, lv1_en, lv1_id, hex_color)
    loop Tiap fitur
        Alg->>Alg: isi atribut dari MAPBIOMAS_CLASSES (tidak ada: Unknown + warna abu-abu)
    end
    Alg->>Native: savefeatures(OUTPUT_VECTOR)
    Native-->>Alg: file vektor final
    alt LOAD_TO_CANVAS aktif
        Alg->>Sym: _apply_symbology(layer)
        Sym->>Sym: kumpulkan gridcode unik yang ada di data
        Sym->>Sym: urutkan sesuai LEGEND_ORDER
        Sym->>Sym: buat kategori warna, label = nama kelas tanpa kode angka
        Sym-->>Alg: QgsCategorizedSymbolRenderer terpasang
        Alg->>QGIS: QgsProject.addMapLayer
    end
    QGIS-->>User: layer tampil dengan simbologi + legenda dinamis
```

### 3. Posisi toolbox dalam pipeline MapBiomas

Toolbox berada **di luar** pipeline klasifikasi MapBiomas dan baru bekerja setelah raster final diunduh.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"background": "transparent"}}, "themeCSS": ".background { fill: none !important; }"}%%
flowchart LR
    subgraph GEE["Pipeline MapBiomas (Google Earth Engine) — di luar scope toolbox"]
        M1["Mosaik Landsat"]
        M2["Feature space"]
        M3["Klasifikasi<br/>Random Forest + U-Net"]
        M4["Post-classification<br/>gap fill dan filter spasial, temporal, frekuensi"]
        M5["Integrasi<br/>tema dasar + lintas tema"]
        M6["Raster final<br/>gridcode per piksel"]
        M1 --> M2 --> M3 --> M4 --> M5 --> M6
    end

    subgraph TOOLKIT["QGIS MapBiomas Toolbox — scope repositori ini"]
        T1["Input raster .tif"]
        T2["Polygonize"]
        T3["Dissolve per kelas"]
        T4["Isi atribut ATBD"]
        T5["Simbologi dan legenda"]
        T6["Vektor siap analisis dan layout peta"]
        T1 --> T2 --> T3 --> T4 --> T5 --> T6
    end

    M6 -.->|"file .tif diunduh"| T1
```

Penjelasan tech stack, struktur kelas, dan fungsi tiap komponen kode ada di [`docs/sistem-kerja-mapbiomas-toolbox.md`](docs/sistem-kerja-mapbiomas-toolbox.md).

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

Buka menu processing toolbox > pilih logo python >add script to toolbox 
   <img width="634" height="227" alt="Screenshot 2026-06-06 190217" src="https://github.com/user-attachments/assets/2bfb0210-3deb-4556-9ad8-58eecb2ef6a6" />
   
>masukan semua file
<img width="367" height="481" alt="Screenshot 2026-06-06 190235" src="https://github.com/user-attachments/assets/751cd222-2bfd-4cea-bcf0-07dd480958c8" />

setelah instalasi selesai maka akan muncul menu di panel atas

## Cara Pakai


https://github.com/user-attachments/assets/7d267b43-4b51-413e-911f-1232596b2055


MapBiomas**
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
