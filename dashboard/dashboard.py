
# Mengimport library yang akan digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengread dataset dari file hasil pemrosesan
df = pd.read_csv("dashboard/main_data.csv")

# Menyiapkan fungsi untuk penampilan dataset setiap kondisi
# Dataset pertanggal
def perday_df(df):
    df_perday = df.groupby(by='date').agg({'count': 'sum'}).reset_index()
    return df_perday

# Dataset pertanggal untuk casual user
def perday_casual_df(df):
    df_perday = df.groupby(by='date').agg({'casual_user': 'sum'}).reset_index()
    return df_perday

# Dataset pertanggal untuk registered user
def perday_registered_df(df):
    df_perday = df.groupby(by='date').agg({'registered_user': 'sum'}).reset_index()
    return df_perday

# Dataset permusim
def musim_df(df):
    df_musim = df.groupby(by=['season']).agg({'count' : 'sum'}).reset_index()
    return df_musim

# Dataset perjam
def jam_df(df):
    df_jam = df.groupby(by=['hour']).agg({'count' : 'sum'}).reset_index()
    return df_jam
    
# Pemfilteran data tanggal minimum dan maksimum
df['date'] = pd.to_datetime(df['date'])
min_date = df["date"].min()
max_date = df["date"].max()

# Pembuatan sidebar untuk mengambil data per inputan tanggal
with st.sidebar:
    # Menambahkan logo untuk sidebar
    st.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTA1Y3Byb3FwZDJ4ZTkycmk0eWVwcjVyMG01dmFsZDg4cHl2YjdocSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2Jhxg4TFEwBlyrVC/giphy.gif")
    
    # Mengambil Start_date & End_date dari date_input
    start_date, end_date = st.date_input(
        label = 'Rentang Waktu',
        min_value = min_date,
        max_value = max_date,
        value=[min_date, max_date]
    )
    
    # Pembuatan Slider untuk range Suhu
    suhu_awal, suhu_akhir = st.slider('Tentukan range suhu (1.00 = 38°C)', 0.00, 1.00, (0.00, 1.00))
    suhu_awal_hitung = suhu_awal * ((38 - (-8)) + (-8))
    suhu_akhir_hitung = suhu_akhir * ((38 - (-8)) + (-8))
    st.write('Suhu awal :', suhu_awal, "Suhu akhir :", suhu_akhir)
    st.write('Suhu awal setelah perhitungan :', round(suhu_awal_hitung,2))
    st.write("Suhu akhir setelah perhitungan :", round(suhu_akhir_hitung,2))
    
    # Pembuatan Toggle untuk melihat dataset
    toggle_dataset = st.toggle('Cek Dataset')
    
# Penyesuaian dataset sesuai range date dan suhu
main_df = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]
main_df = main_df[(main_df["temp"] >= suhu_awal) & (main_df["temp"] <= suhu_akhir)]

 # Pembuatan dataset per setiap fungsi
df_perday = perday_df(main_df)
df_perday_casual = perday_casual_df(main_df)
df_perday_registered = perday_registered_df(main_df)
df_musim = musim_df(main_df)
df_jam = jam_df(main_df)

# Membuat judul dashboard
st.header("Bike Sharing Rentals :bike: :sparkles:")

# Membuat jumlah penyewaan tiap hari untuk casual, registered, dan total user
st.subheader("Total Rented Bike Count")
col1, col2, col3 = st.columns(3)

# Menampilkan jumlah casual user
with col1:
    casual_perday = df_perday_casual['casual_user'].sum()
    st.metric('Casual User', value = casual_perday)

# Menampilkan jumlah registered user    
with col2:
    registered_perday = df_perday_registered['registered_user'].sum()
    st.metric('Registered User', value = registered_perday)

# Menampilkan jumlah casual user
with col3:
    total_perday = df_perday['count'].sum()
    st.metric('Total', value = total_perday)

# Pengecekan toggle dataset
if toggle_dataset:
    st.subheader("Main Dataset")
    st.dataframe(main_df)

# Membagi menjadi dua bagian, satu pengaruh hari, satu pengaruh bulan
col1, col2 = st.columns(2)
with col1:
    st.subheader("Pengaruh hari terhadap jumlah peminjaman sepeda")
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.boxplot(x = "weekday", y = "count", data = main_df, palette="Pastel1")
    plt.title("Distribution of bike rentals by day")
    st.pyplot(fig)

with col2:
    st.subheader("Pengaruh bulan terhadap jumlah peminjaman sepeda")
    fig, ax = plt.subplots(figsize=(20,10))
    sns.boxplot(x = "month", y = "count", data = main_df, palette="summer")
    plt.title('Distribution of bike rentals per month')
    st.pyplot(fig)


# Pembuatan Subplot untuk menjawab Pertanyaan 1
st.subheader("Bagaimana Pengaruh Cuaca dan Musim terhadap jumlah peminjaman sepeda? Apakah ada pola peningkatan atau penurunan terhadap hal-hal tersebut?")
fig, ax = plt.subplots(figsize=(16,8))
sns.barplot(x = "season", y = "count", data = main_df, palette = "flare_r", hue = 'weather', ax=ax)
plt.title('Distribution of bike rentals in each seasons and weather')
st.pyplot(fig)
with st.expander("Penjelasan"):
    st.caption("Terdapat korelasi antara Cuaca dan Musim dengan Jumlah peminjaman sepeda. Cuaca cerah (Clear) memiliki jumlah peminjaman sepeda paling banyak dibandingkan cuaca-cuaca lainnya. Hal ini disebabkan bahwa, untuk peminjaman sepeda biasanya banyak disaat cuaca tidak ada apa apa. Apabila cuaca sedang hujan atau salju, maka akan mengurang jumlah peminjamannya. Sedangkan untuk musim, musim gugur (Fall) lah yang memiliki jumlah peminjaman terbanyak dibandingkan dengan musim-musim lainnya. Hal ini disebabkan karena peminjaman sepeda biasanya banyak pada musim-musim yang tidak banyak halangan, salju seperti musim gugur dan musim panas.")

# Pembuatan Subplot untuk menjawab Pertanyaan 2
st.subheader("Apakah terdapat perbedaan pola penggunaan sepeda terhadap berdasarkan jam?")
fig, ax = plt.subplots(figsize=(16,8))
sns.barplot(x = 'hour', y = 'count', data = df_jam, palette='crest_r')
plt.title('Distribution of bike rentals for each hour')
st.pyplot(fig)
with st.expander("Penjelasan"):
    st.caption("Seperti yang dapat dilihat dari hasil visualisasi tersebut, dapat disimpulkan bahwa terdapat pengaruh antara jam dengan jumlah peminjaman sepeda. Jumlah peminjaman disaat pagi hari (0 - 6) sangat sedikit karena kebanyakan orang sedang beristirahat atau tidur. Disaat sedang memulai kegiatan di pagi hari (Dari jam 7), mulai terdapat peningkatan dari jumlah peminjaman. Titik puncak jumlah peminjaman sepeda terdapat pada jam 17. Setelah itu, mengalami penurunan sampai akhir hari.")
