import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql

# Sidebar select box
select_box = st.sidebar.selectbox('Pilih data yang ingin ditampilkan:', ['Adventure Works', 'IMDb Populer Movies'])

# Function to convert Rating to float and handle errors
def convert_rating(rating_series):
    try:
        # Extract numeric part from 'Rating' column
        return rating_series.str.extract(r'(\d+\.\d+|\d+)').astype(float)
    except ValueError as e:
        st.write(f"Error converting 'Rating' column to float: {e}")
        st.write(rating_series)  # Print the problematic column for inspection
        return None

# Display IMDb Popular Movies
if select_box == 'IMDb Populer Movies':
    # Baca file CSV menggunakan pandas
    fn1 = 'IMDb_Populer.csv'
    df1 = pd.read_csv(fn1, encoding='latin1')

    # Tampilkan judul aplikasi
    st.title("Final Project Data Visualisasi")
    st.markdown("<h1 style='text-align; color: black;'>Scrapping Website IMDb</h1>", unsafe_allow_html=True)
    st.markdown(
    """
     Tabel data berikut merupakan hasil dari scrapping website IMDb Charts : Most Popular Movies. Data ini mencakup judul film, durasi film, rating IMDb, dan tahun rilis untuk film-film populer saat ini menurut IMDb.
    """
)
    # Menampilkan DataFrame sebagai tabel
    st.dataframe(df1)

    # Visualisasi komparasi rating IMDb teratas
    st.subheader('1. Komparasi berdasarkan Rating IMDb dan Tahun 20 Data Teratas')
    st.markdown(
    """
    Visualisasi scatter plot ini menampilkan film-film berdasarkan tahun rilis dari 2015 hingga 2024 dengan judul pada sumbu Y dan tahun pada sumbu X, menunjukkan rating masing-masing film melalui warna titik (biru untuk rating lebih rendah hingga merah untuk rating lebih tinggi), dengan mayoritas film berfokus pada tahun 2023 dan 2024, mengindikasikan variasi rating yang signifikan dari 5.5 hingga 8.5.
    """
)
    data_top_10 = df1.head(20)
    
    # Convert 'Rating' to float
    data_top_10['Rating'] = convert_rating(data_top_10['Rating'])

    # Plot scatter plot untuk menampilkan perbandingan rating IMDb untuk setiap judul pada tahun tertentu
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if pd.api.types.is_numeric_dtype(data_top_10['Rating']):
        scatter = ax.scatter(data_top_10['Tahun'], data_top_10['Judul'], c=data_top_10['Rating'], cmap='coolwarm', alpha=0.7, edgecolors='w', s=100)
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Judul')
        cbar = fig.colorbar(scatter)
        cbar.set_label('Rating')
        ax.set_xticks([2015, 2023, 2024])
        st.pyplot(fig)
    else:
        st.write("Error: 'Rating' column could not be converted to numeric.")

    # Visualisasi hubungan rating IMDb teratas dengan rating dibulatkan
    st.subheader('2. Hubungan Antar Judul Film dan Rating IMDb 20 Data Teratas')
    st.markdown(
    """
    Visualisasi di bawah ini menampilkan hubungan antara judul film dan rating IMDb dari 20 data teratas. Diagram batang ini menunjukkan rating IMDb untuk berbagai film, dengan rating yang bervariasi dari sekitar 5 hingga 8.5, di mana sebagian besar film berada di kisaran rating menengah sekitar 6 hingga 7, dan film "Mad Max: Fury Road" memiliki rating tertinggi mendekati 8.5, menandakan kualitas yang sangat baik dibandingkan dengan film lainnya.
    """
)
    data_top_20 = df1.head(20)
    
    # Convert 'Rating' to float
    data_top_20['Rating'] = convert_rating(data_top_20['Rating'])

    fig, ax = plt.subplots(figsize=(12, 8))  # Ukuran gambar bisa disesuaikan
    ax.bar(data_top_20['Judul'], data_top_20['Rating'], color='skyblue')
    ax.set_xlabel('Judul Film')
    ax.set_ylabel('Rating IMDb')
    ax.set_xticklabels(data_top_20['Judul'], rotation=90)

    st.pyplot(fig)

    # Visualisasi komposisi jumlah film berdasarkan rentang tahun rilis untuk 20 data teratas
    st.subheader('3. Komposisi Jumlah Film Berdasarkan Rentang Tahun Rilis untuk 20 Data Teratas')
    st.markdown(
    """
    Visualisasi ini menunjukkan bahwa jumlah film yang dirilis mengalami peningkatan yang signifikan, terutama dalam dekade 2020 hingga 2030, dengan jumlah film yang jauh lebih banyak dibandingkan dengan periode sebelumnya, di mana hampir tidak ada film yang dirilis antara tahun 1990 hingga 2010 dan hanya sedikit peningkatan pada periode 2010 hingga 2020.
    """
)
    data_top_20 = df1.head(20)
    
    # Pastikan kolom 'Tahun' adalah tipe data integer
    data_top_20['Tahun'] = data_top_20['Tahun'].astype(int)

    # Hitung jumlah film untuk setiap rentang tahun
    year_bins = pd.cut(data_top_20['Tahun'], bins=[1990, 2000, 2010, 2020, 2030], right=False)
    year_counts = year_bins.value_counts().sort_index()

    # Visualisasi komposisi menggunakan line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(year_counts.index.astype(str), year_counts.values, marker='o', linestyle='-', color='b')
    ax.set_xlabel('Rentang Tahun Rilis')
    ax.set_ylabel('Jumlah Film')
    ax.grid(True)
    st.pyplot(fig)

 # Visualisasi distribusi judul film dengan tahun film menggunakan bar plot
    st.subheader('4. Distribusi Judul Film dengan Tahun Rilis untuk 20 Data Teratas')
    st.markdown(
    """
    Grafik batang ini menunjukkan bahwa jumlah judul film yang dirilis mengalami peningkatan bertahap dari sekitar 2 judul pada tahun 2015 menjadi sekitar 3 judul pada tahun 2023, dan kemudian mengalami lonjakan yang sangat signifikan pada tahun 2024 dengan jumlah judul film yang dirilis mencapai sekitar 17 judul, menggambarkan peningkatan yang luar biasa dalam produksi film pada tahun tersebut dibandingkan dengan tahun-tahun sebelumnya.
    """
)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.countplot(data=data_top_20, x='Tahun', palette='viridis')
    ax.set_xlabel('Tahun Rilis')
    ax.set_ylabel('Jumlah Judul Film')
    st.pyplot(fig)

# Initialize connection.
# conn = st.connection('mysql', type='sql', username=st.secrets["DB_USER"], password=st.secrets["DB_PASSWORD"])
# conn = st.connection(**st.secrets.db_credentials)
conn = st.connection("mydb", type="sql", autocommit=True)
# st.write(st.secrets["connections.mydb"]["username"])

    # Membuat cursor
    cursor = conn.cursor()

    # Cek koneksi berhasil
    if conn:
        st.sidebar.success('Connected to MySQL database')

    # Query untuk mengambil data dari tabel dimcustomer dan factinternetsales
    query1 = """ 
            SELECT dc.Gender, COUNT(fs.CustomerKey) AS TotalCustomers
            FROM dimcustomer dc
            LEFT JOIN factinternetsales fs ON dc.CustomerKey = fs.CustomerKey
            GROUP BY dc.Gender;
    """

    # Eksekusi query
    cursor.execute(query1)

    # Mendapatkan hasil query sebagai tuple
    data1 = cursor.fetchall()

    # Membaca data dari database
    df_customer = pd.DataFrame(data1, columns=['Gender', 'TotalCustomers'])

    # Query untuk mengambil data harga list (ListPrice) dan berat (Weight) dari tabel dimproduct
    query2 = """
        SELECT 
            ListPrice,
            Weight
        FROM 
            dimproduct
    """

    # Membaca data dari database menjadi dataframe menggunakan pandas
    df_product = pd.read_sql(query2, conn)

    # Query untuk mengambil data warna produk dari tabel dimproduct
    query3 = """
        SELECT 
            Color,
            COUNT(*) AS count
        FROM 
            dimproduct
        GROUP BY 
            Color
    """

    # Membaca data dari database menjadi dataframe menggunakan pandas
    df_color = pd.read_sql(query3, conn)

    # Query untuk mengambil data total penjualan dari tabel factinternetsales
    query4 = """
        SELECT SalesAmount
        FROM factinternetsales
    """

    # Membaca data dari database menjadi dataframe menggunakan pandas
    df_sales = pd.read_sql(query4, conn)

    # Menutup cursor dan koneksi database
    cursor.close()
    conn.close()

    # Menampilkan judul di halaman web
    st.title("Final Project Data Visualisasi")
    st.markdown("<h1 style='text-align; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

  # Menampilkan data frame df_customer di Streamlit
    st.subheader("1. Komparasi Total Customers Berdasarkan Gender")
    st.markdown(
    """
    Visualisasi ini digunakan untuk membandingkan jumlah pelanggan berdasarkan gender, sehingga memudahkan untuk mengetahui berapa banyak pelanggan wanita dan berapa banyak pelanggan pria. Dari visualisasi yang telah dibuat terlihat bahwa jumlah pelanggan laki-laki sedikit lebih banyak dibandingkan dengan pelanggan perempuan. 
    Jumlah pelanggan laki-laki adalah 30.381, sedangkan jumlah pelanggan perempuan adalah 30.017. Terlihat bahwa perbedaannya tidak terlalu signifikan, dengan selisih hanya 364 pelanggan lebih banyak pada pelanggan laki-laki dibandingkan dengan pelanggan perempuan.
    """
)
    st.dataframe(df_customer)
    
    # Membuat pie chart menggunakan Matplotlib untuk total customers berdasarkan gender
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df_customer['TotalCustomers'], labels=df_customer['Gender'], autopct='%1.1f%%', colors=['blue', 'pink'], startangle=140)
    st.pyplot(fig)

    # Menampilkan data frame df_product di Streamlit
    st.subheader("2. Hubungan Antara Harga List dan Berat Produk")
    st.markdown(
    """
    Visualisasi ini menampilkan perbandingan antara harga list dan berat produk berdasarkan indeks produk. 
    Harga list (garis biru) bervariasi signifikan dengan beberapa kenaikan tajam hingga 3500 dan penurunan drastis di beberapa titik. 
    Sebaliknya, berat produk (garis hijau) tetap hampir konstan di seluruh rentang indeks produk, menunjukkan variabilitas yang sangat rendah dibandingkan dengan harga list.
    """
)
    st.dataframe(df_product)

    # Membuat line plot untuk memvisualisasikan hubungan antara harga list dan berat produk
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_product['ListPrice'], color='blue', label='Harga List')
    ax.plot(df_product['Weight'], color='green', label='Berat')
    ax.set_xlabel('Indeks Produk')
    ax.set_ylabel('Nilai')
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    # Menampilkan data frame df_color di Streamlit
    st.subheader("3. Komposisi Warna Produk")
    st.markdown(
    """
    Visualisasi ini digunakan untuk melihat berbagai warna produk terdistribusi, mendapatkan wawasan lebih dalam tentang preferensi warna dalam penjualan produk, dan mengidentifikasi tren warna yang tersedia. 
    Diagram pai ini menunjukkan bahwa warna Black mendominasi produk dengan 29.1%, diikuti oleh Yellow (17.1%), Red (14.6%), Silver (12.7%), NA (11.4%), Blue (10.8%), Multi (3.2%), dan White (1.3%), yang merupakan warna paling jarang ditemukan.
    """
)
    st.dataframe(df_color)

    # Membuat pie chart menggunakan Matplotlib untuk komposisi warna produk
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df_color['count'], labels=df_color['Color'], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Memastikan lingkaran berbentuk lingkaran
    st.pyplot(fig)

    # Menampilkan data frame df_sales di Streamlit
    st.subheader("4. Distribusi Jumlah Penjualan")
    st.markdown(
    """
     Visualisasi ini digunakan untuk melihat bagaimana jumlah penjualan terdistribusi di antara berbagai produk dan untuk mengoptimalkan strategi pemasaran dan pengelolaan persediaan, sehingga dapat meningkatkan efisiensi operasional danprofitabilitas perusahaan.
     Histogram ini menunjukkan distribusi jumlah penjualan yang didominasi oleh transaksi dengan nilai penjualan 0, dengan sebagian kecil transaksi tersebar secara sporadis di nilai penjualan yang lebih tinggi hingga sekitar 3500.
    """
)
    st.dataframe(df_sales)

    # Membuat histogram untuk visualisasi distribusi jumlah penjualan
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_sales['SalesAmount'], kde=False, color='skyblue', bins=30, ax=ax)
    ax.set_xlabel('Sales Amount')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
