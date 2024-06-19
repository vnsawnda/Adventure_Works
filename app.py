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
query = """ 
        SELECT dc.Gender, COUNT(fs.CustomerKey) AS TotalCustomers
        FROM dimcustomer dc
        LEFT JOIN factinternetsales fs ON dc.CustomerKey = fs.CustomerKey
        GROUP BY dc.Gender;
"""

# Eksekusi query
cursor.execute(query)

# Mendapatkan hasil query sebagai tuple
data = cursor.fetchall()

# Menutup cursor dan koneksi database
cursor.close()
conn.close()

# Membaca data dari database
df_customer = pd.DataFrame(data, columns=['Gender', 'TotalCustomers'])

# Menampilkan judul di halaman web
st.title("Dashboard Adventure Works")
st.markdown("<h1 style='text-align: center; color: black;'>Dashboard Adventure Works</h1>", unsafe_allow_html=True)

# Menampilkan data frame di Streamlit
st.dataframe(df_customer)

# Membuat pie chart menggunakan Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df_customer['TotalCustomers'], labels=df_customer['Gender'], autopct='%1.1f%%', colors=['blue', 'pink'], startangle=140)
ax.set_title('Komparasi Total Customers Berdasarkan Gender')
st.pyplot(fig)
