import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql

# Sidebar select box
select_box = st.sidebar.selectbox('Pilih data yang ingin ditampilkan:', ['Adventure Works', 'IMDb Populer Movies'])

# Display IMDb Popular Movies
if select_box == 'IMDb Populer Movies':
    # Baca file CSV menggunakan pandas
    fn1 = 'IMDb_Populer.csv'
    df1 = pd.read_csv(fn1, encoding='latin1')

    # Tampilkan judul aplikasi
    st.title("Scrapping Website IMDb")
    # Menampilkan DataFrame sebagai tabel
    st.dataframe(df1)

    # Visualisasi komparasi rating IMDb teratas
    st.subheader('Komparasi Rating IMDb untuk Data Teratas')
    data_top_10 = df1.head(20)
    
    # Coba ubah 'Rating' menjadi float, dengan penanganan khusus karakter non-numeric
    try:
        # Extract numeric part from 'Rating' column
        data_top_10['Rating'] = data_top_10['Rating'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    except ValueError as e:
        st.write(f"Error converting 'Rating' column to float: {e}")
        st.write(data_top_10['Rating'])  # Print the problematic column for inspection

    # Plot scatter plot untuk menampilkan perbandingan rating IMDb untuk setiap judul pada tahun tertentu
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Ensure 'Rating' column is numeric before plotting
    if 'Rating' in data_top_10.columns and pd.api.types.is_numeric_dtype(data_top_10['Rating']):
        scatter = ax.scatter(data_top_10['Tahun'], data_top_10['Judul'], c=data_top_10['Rating'], cmap='coolwarm', alpha=0.7, edgecolors='w', s=100)
        ax.set_title('Komparasi berdasarkan Rating IMDb dan Tahun 20 Data Teratas')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Judul')
        cbar = fig.colorbar(scatter)
        cbar.set_label('Rating')
        ax.set_xticks([2015, 2023, 2024])
        st.pyplot(fig)
    else:
        st.write("Error: 'Rating' column could not be converted to numeric.")

 # Plot scatter plot untuk menampilkan hubungan antara judul film dan rating IMDb
    fig, ax = plt.subplots(figsize=(12, 8))  # Ukuran gambar bisa disesuaikan
    ax.scatter(data_top_10['Judul'], data_top_10['Rating'], s=100, alpha=0.7, color='blue', edgecolors='w')
    ax.set_xlabel('Judul Film')
    ax.set_ylabel('Rating IMDb')
    ax.set_title('Hubungan Antar Judul Film dan Rating IMDb 20 Data Teratas')
    ax.tick_params(axis='x', rotation=90)  # Rotasi label sumbu x untuk memudahkan pembacaan

    # Menambahkan nilai rating pada masing-masing titik
    for i, txt in enumerate(data_top_10['Rating']):
        ax.annotate(txt, (data_top_10['Judul'].iloc[i], data_top_10['Rating'].iloc[i]), fontsize=8, ha='center', va='bottom')

    st.pyplot(fig)

# Display Adventure Works Data
else:
    # Membuat koneksi ke database MySQL
    conn = pymysql.connect(
        host="kubela.id",
        port=3306,
        user="davis2024irwan",
        password="wh451n9m@ch1n3",
        database="aw"
    )

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
    st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

    # Menampilkan data frame df_customer di Streamlit
    st.subheader("1. Total Customers Berdasarkan Gender")
    st.dataframe(df_customer)

    # Membuat pie chart menggunakan Matplotlib untuk total customers berdasarkan gender
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df_customer['TotalCustomers'], labels=df_customer['Gender'], autopct='%1.1f%%', colors=['blue', 'pink'], startangle=140)
    ax.set_title('Komparasi Total Customers Berdasarkan Gender')
    st.pyplot(fig)

    # Menampilkan data frame df_product di Streamlit
    st.subheader("2. Harga List dan Berat Produk")
    st.dataframe(df_product)

    # Membuat line plot untuk memvisualisasikan hubungan antara harga list dan berat produk
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_product['ListPrice'], color='blue', label='Harga List')
    ax.plot(df_product['Weight'], color='green', label='Berat')
    ax.set_xlabel('Indeks Produk')
    ax.set_ylabel('Nilai')
    ax.set_title('Hubungan Antara Harga List dan Berat Produk')
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    # Menampilkan data frame df_color di Streamlit
    st.subheader("3. Komposisi Warna Produk")
    st.dataframe(df_color)

    # Membuat pie chart menggunakan Matplotlib untuk komposisi warna produk
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df_color['count'], labels=df_color['Color'], autopct='%1.1f%%', startangle=140)
    ax.set_title('Komposisi Warna Produk')
    ax.axis('equal')  # Memastikan lingkaran berbentuk lingkaran
    st.pyplot(fig)

    # Menampilkan data frame df_sales di Streamlit
    st.subheader("4. Distribusi Jumlah Penjualan")
    st.dataframe(df_sales)

    # Membuat histogram untuk visualisasi distribusi jumlah penjualan
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_sales['SalesAmount'], kde=False, color='skyblue', bins=30, ax=ax)
    ax.set_xlabel('Sales Amount')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribusi Jumlah Penjualan')
    st.pyplot(fig)
