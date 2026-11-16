from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

BLUE = "#5B9BD5"
DARK_BLUE = "#1F4E78"
LIGHT_BLUE = "#A9D18E"
sns.set_theme(style="whitegrid")

st.markdown("""
<style>
    .stApp { background-color: #F4F9FD; color: #17365D; }
    [data-testid="stSidebar"] { background-color: #E3F1FA; }
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #D6E8F5;
    }
    h1, h2, h3, h4 { color: #17365D !important; }
    [data-testid="stMetricValue"] { color: #17365D !important; font-weight: 700; }
    [data-testid="stMetricLabel"] { color: #1F4E78 !important; }
    .stAlert {
        background-color: #FFFFFF !important;
        border: 1px solid #D6E8F5 !important;
    }
    .stAlert p {
        color: #17365D !important;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

@st.cache_data
def load_data():
    daily_df = pd.read_csv(BASE_DIR / "main_data.csv")
    hourly_df = pd.read_csv(DATA_DIR / "data_2.csv")

    daily_df["dteday"] = pd.to_datetime(daily_df["dteday"])
    hourly_df["dteday"] = pd.to_datetime(hourly_df["dteday"])

    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {
        1: "Clear/Partly Cloudy",
        2: "Misty/Cloudy",
        3: "Light Snow/Rain",
        4: "Severe Weather"
    }

    daily_df["season_label"] = daily_df["season"].map(season_map)
    daily_df["weathersit_label"] = daily_df["weathersit"].map(weather_map)
    return daily_df, hourly_df

daily_df, hourly_df = load_data()

logo_svg = """
<div style="text-align: center; margin-bottom: 15px;">
<svg width="170" height="170" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <path id="textArc" d="M 35,95 A 65,65 0 1,1 165,95" />
  </defs>
  <text font-family="sans-serif" font-size="16" font-weight="bold" letter-spacing="1">
    <textPath href="#textArc" startOffset="50%" text-anchor="middle">
      <tspan fill="#2D74DA">Dicoding</tspan> <tspan fill="#333333">Asah</tspan>
    </textPath>
  </text>
  <ellipse cx="100" cy="112" rx="58" ry="68" fill="#DCE9F9" stroke="#FFFFFF" stroke-width="4"/>
  <path d="M 94,65 C 94,55 106,55 106,63 C 106,68 100,70 100,74" fill="none" stroke="#2D74DA" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M 76,78 L 56,92 L 66,106 L 76,99 L 76,142 C 92,147 108,147 124,142 L 124,99 L 134,106 L 144,92 L 124,78 L 110,75 L 90,75 Z" fill="#FBC02D"/>
  <polygon points="90,75 100,82 93,90 85,81" fill="#1E2B37"/>
  <polygon points="110,75 100,82 107,90 115,81" fill="#1E2B37"/>
  <polygon points="100,96 103,104 112,104 105,109 107,117 100,112 93,117 95,109 88,104 97,104" fill="#FFFFFF"/>
</svg>
</div>
"""
st.sidebar.markdown(logo_svg, unsafe_allow_html=True)

min_date = daily_df["dteday"].min().date()
max_date = daily_df["dteday"].max().date()

date_range = st.sidebar.date_input(
    "Rentang Waktu",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

start_date, end_date = date_range if len(date_range) == 2 else (min_date, max_date)

main_df = daily_df[
    (daily_df["dteday"].dt.date >= start_date) & 
    (daily_df["dteday"].dt.date <= end_date)
]
hour_df = hourly_df[
    (hourly_df["dteday"].dt.date >= start_date) & 
    (hourly_df["dteday"].dt.date <= end_date)
]

st.title("BIKE SHARING ANALYSIS")
st.caption(f"Periode: {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')} | {len(main_df):,} hari pengamatan")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rata-rata Penyewaan / Hari", f"{main_df['cnt'].mean():,.0f}")
c2.metric("Pengguna Terdaftar / Hari", f"{main_df['registered'].mean():,.0f}")
c3.metric("Pengguna Kasual / Hari", f"{main_df['casual'].mean():,.0f}")
c4.metric("Korelasi Suhu dan Penyewaan", f"{main_df['temp'].corr(main_df['cnt']):.3f}")

st.subheader("Pola Penyewaan Berdasarkan Kondisi")
col1, col2 = st.columns(2)

with col1:
    season_df = main_df.groupby("season_label", as_index=False)["cnt"].mean().sort_values("cnt")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=season_df, x="season_label", y="cnt",
        order=["Spring", "Summer", "Fall", "Winter"],
        color=BLUE, ax=ax
    )
    ax.set_title("Rata-rata Penyewaan per Musim", color=DARK_BLUE)
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata Penyewaan")
    sns.despine()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

with col2:
    weather_df = main_df.groupby("weathersit_label", as_index=False)["cnt"].mean().sort_values("cnt")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=weather_df, x="cnt", y="weathersit_label",
        color=BLUE, ax=ax
    )
    ax.set_title("Rata-rata Penyewaan per Kondisi Cuaca", color=DARK_BLUE)
    ax.set_xlabel("Rata-rata Penyewaan")
    ax.set_ylabel("")
    sns.despine()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

st.subheader("Pola Waktu dan Hubungan Suhu")
col3, col4 = st.columns(2)

with col3:
    hour_summary = hour_df.groupby(["workingday", "hr"], as_index=False)["cnt"].mean()
    hour_summary["Kategori"] = hour_summary["workingday"].map({0: "Akhir Pekan / Libur", 1: "Hari Kerja"})
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(
        data=hour_summary, x="hr", y="cnt", hue="Kategori",
        palette=[BLUE, DARK_BLUE], linewidth=2.2, ax=ax
    )
    ax.set_title("Pola Penyewaan per Jam", color=DARK_BLUE)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticks(range(0, 24, 2))
    ax.legend(title="", frameon=False)
    sns.despine()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

with col4:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(
        data=main_df, x="temp", y="cnt",
        color=BLUE, alpha=0.5, s=30, ax=ax
    )
    sns.regplot(
        data=main_df, x="temp", y="cnt",
        scatter=False, color=DARK_BLUE,
        line_kws={"linewidth": 2}, ax=ax
    )
    ax.set_title("Korelasi Suhu dan Total Penyewaan", color=DARK_BLUE)
    ax.set_xlabel("Suhu (Normalisasi)")
    ax.set_ylabel("Total Penyewaan")
    sns.despine()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

st.subheader("Aktivitas Pengguna")
col5, col6 = st.columns(2)

with col5:
    day_map = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
    weekday_df = main_df.groupby("weekday", as_index=False)["cnt"].mean()
    weekday_df["Hari"] = weekday_df["weekday"].map(day_map)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=weekday_df, x="Hari", y="cnt",
        order=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"],
        color=BLUE, ax=ax
    )
    ax.set_title("Rata-rata Penyewaan per Hari", color=DARK_BLUE)
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata Penyewaan")
    sns.despine()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

with col6:
    user_df = main_df.groupby("workingday", as_index=False)[["casual", "registered"]].mean()
    user_df["Kategori"] = user_df["workingday"].map({0: "Akhir Pekan / Libur", 1: "Hari Kerja"})
    user_melted = user_df.melt(
        id_vars="Kategori",
        value_vars=["casual", "registered"],
        var_name="Tipe",
        value_name="Rata-rata"
    )
    user_melted["Tipe"] = user_melted["Tipe"].map({"casual": "Kasual", "registered": "Terdaftar"})
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=user_melted, x="Kategori", y="Rata-rata", hue="Tipe",
        palette=[BLUE, DARK_BLUE], ax=ax
    )
    ax.set_title("Perbandingan Pengguna Kasual dan Terdaftar", color=DARK_BLUE)
    ax.set_xlabel("")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.legend(title="", frameon=False)
    sns.despine()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

best_season = season_df.loc[season_df["cnt"].idxmax(), "season_label"]
best_weather = weather_df.loc[weather_df["cnt"].idxmax(), "weathersit_label"]
peak_hour = hour_summary.loc[hour_summary["cnt"].idxmax(), "hr"]

st.subheader("Insight Utama")
i1, i2, i3 = st.columns(3)
i1.info(f"Musim {best_season} mencatat rata-rata penyewaan tertinggi pada periode terpilih.")
i2.info(f"Kondisi cuaca {best_weather} menghasilkan rata-rata penyewaan tertinggi.")
i3.info(f"Puncak penyewaan terjadi pada pukul {int(peak_hour):02d}.00.")

st.caption("Copyright © 2026 Grace Vies Angel")