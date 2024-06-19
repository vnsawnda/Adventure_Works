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

# Query untuk mengambil data dari tabel dimcustomer dan factinternetsales
SELECT d.Gender, COUNT(f.CustomerKey) as CustomerCount
FROM dimcustomer d
JOIN factinternetsales f ON d.CustomerKey = f.CustomerKey
GROUP BY d.Gender

# Eksekusi query
cursor.execute(query)

# Mendapatkan hasil query sebagai tuple
data = cursor.fetchall()

# Menutup cursor dan koneksi database
cursor.close()
conn.close()

# Membaca data dari database
df_gender = pd.read_sql(gender_query, connection)
df_customer = pd.read_sql(customer_query, connection)

# Melakukan join tabel dimcustomer dan factinternetsales berdasarkan CustomerKey
df_merged = pd.merge(df_customer, df_gender, on='CustomerKey')

# Mengagregasi data penjualan per gender
df_aggregated = df_merged.groupby('Gender').agg({
    'CustomerKey': 'count'
}).reset_index()

# Menampilkan hasil agregasi untuk verifikasi
print(df_aggregated)

# Mengatur matplotlib inline untuk menampilkan plot di notebook
%matplotlib inline

# Membuat pie chart untuk visualisasi
plt.figure(figsize=(8, 8))
plt.pie(df_aggregated['CustomerKey'], labels=df_aggregated['Gender'], autopct='%1.1f%%', colors=['blue', 'pink'], startangle=140)

# Menambahkan judul
plt.title('Komparasi Total Customers Berdasarkan Gender')
plt.show()
