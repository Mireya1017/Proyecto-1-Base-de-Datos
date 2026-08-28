import psycopg2

conexion = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cursor = conexion.cursor()

cursor.execute("SELECT current_database();")

base_datos = cursor.fetchone()

print("Conexión exitosa.")
print("Base de datos:", base_datos[0])

cursor.close()
conexion.close()