import pandas as pd
import streamlit as st
import pymysql
import matplotlib.pyplot as plt

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

# Menutup cursor dan koneksi database
cursor.close()
conn.close()

# Menampilkan judul di halaman web
st.title("Final Project Data Visualisasi")
st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

# Menampilkan data frame di Streamlit
st.dataframe(df_customer)

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

# Membuat pie chart menggunakan Matplotlib untuk total customers berdasarkan gender
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df_customer['TotalCustomers'], labels=df_customer['Gender'], autopct='%1.1f%%', colors=['blue', 'pink'], startangle=140)
ax.set_title('Komparasi Total Customers Berdasarkan Gender')
st.pyplot(fig)

# Membuat pie chart menggunakan Matplotlib untuk komposisi warna produk
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df_color['count'], labels=df_color['Color'], autopct='%1.1f%%', startangle=140)
ax.set_title('Komposisi Warna Produk')
ax.axis('equal')  # Memastikan lingkaran berbentuk lingkaran
st.pyplot(fig)
