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
    print('Connected to MySQL database')

# Query SQL untuk mengambil data (apa)
query = """
    (masukin query mu)
"""

# Eksekusi query
cursor.execute(query)

# Mendapatkan hasil query sebagai tuple
data = cursor.fetchall()

# Menutup cursor dan koneksi database
cursor.close()
conn.close()

# Membuat DataFrame dari hasil query
return df_customer
