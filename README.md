# Bike Sharing Data Analytics Dashboard

## Deskripsi Proyek
Proyek ini merupakan implementasi siklus analisis data secara menyeluruh menggunakan **Bike Sharing Dataset** (periode 2011–2012). Analisis difokuskan untuk mengidentifikasi pola penyewaan sepeda berdasarkan faktor musim, kondisi cuaca, distribusi jam sibuk, serta pengaruh suhu udara terhadap aktivitas pengguna kasual maupun terdaftar. Hasil analisis disajikan dalam bentuk *dashboard* interaktif berbasis Streamlit.

## Struktur Direktori
- **`dashboard/`**: Berisi skrip utama aplikasi Streamlit (`dashboard.py`) dan dataset harian yang telah dibersihkan (`main_data.csv`).
- **`data/`**: Berisi dataset pendukung yang digunakan dalam proses analisis (`data_1.csv` dan `data_2.csv`).
- **`notebook.ipynb`**: Dokumentasi proses analisis data mulai dari *Data Wrangling*, *Exploratory Data Analysis (EDA)*, hingga visualisasi data.
- **`requirements.txt`**: Daftar pustaka (*libraries*) Python yang dibutuhkan untuk menjalankan proyek.
- **`README.md`**: Dokumentasi utama dan panduan penggunaan proyek.
- **`url.txt`**: Tautan menuju *dashboard* publik yang telah di-*deploy* ke Streamlit Cloud.

## Panduan Instalasi dan Menjalankan Aplikasi

### 1. Menggunakan Virtual Environment (venv)
```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

### 2. Menggunakan Anaconda
```bash
conda create --name bike-sharing-analysis python=3.9
conda activate bike-sharing-analysis
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard secara Lokal
```bash
cd dashboard
streamlit run dashboard.py
```

## Ringkasan Hasil Analisis (Key Insights)
- **Pengaruh Musim dan Cuaca:** Musim gugur (*Fall*) dan kondisi cuaca cerah (*Clear/Partly Cloudy*) mencatatkan rata-rata penyewaan sepeda tertinggi dibandingkan kondisi lainnya.
- **Pola Jam Sibuk:** Pada hari kerja (*working day*), lonjakan penyewaan terjadi pada jam berangkat kerja (sekitar pukul 08.00) dan jam pulang kerja (sekitar pukul 17.00). Sebaliknya, pada akhir pekan penyewaan lebih merata pada siang hingga sore hari.
- **Korelasi Suhu:** Terdapat hubungan positif antara peningkatan suhu udara dengan jumlah total penyewaan sepeda harian.
- **Karakteristik Pengguna:** Pengguna terdaftar (*registered*) mendominasi penyewaan pada hari kerja, sedangkan aktivitas pengguna kasual (*casual*) meningkat signifikan pada akhir pekan atau hari libur.

## Rekomendasi Strategis
- **Penyesuaian Armada:** Menambah ketersediaan unit sepeda pada jam-jam sibuk hari kerja serta saat memasuki musim gugur dan musim panas.
- **Jadwal Perawatan Rutin:** Memfokuskan pemeliharaan armada pada musim semi (*Spring*) atau saat kondisi cuaca buruk ketika volume penyewaan cenderung menurun.