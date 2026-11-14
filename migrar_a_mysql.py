import os
import pandas as pd
import mysql.connector

# 1. Conexión a MySQL en XAMPP
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",           # En XAMPP viene vacía por defecto
    database="astroatlas_db"
)
cursor = conexion.cursor()

# 2. Cargar el archivo Excel
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "observatorios_astronomicos_mundo_categorizados (BASE_DE _DATOS).xlsx")

print("Leyendo archivo Excel...")
df = pd.read_excel(EXCEL_FILE, sheet_name='Observatorios')

# Unir Latitud y Longitud
df['coordenadas'] = df['Latitud (°)'].astype(str) + ", " + df['Longitud (°)'].astype(str)

# Limpiar tabla si ya tuviera datos previos
cursor.execute("DELETE FROM observatorios")

registros = []
for _, fila in df.iterrows():
    registros.append((
        str(fila['Observatorio / instalación']),
        str(fila['Categoría']) if pd.notna(fila['Categoría']) else "General",
        str(fila['País / territorio']),
        str(fila['Continente / región']) if pd.notna(fila['Continente / región']) else "",
        str(fila['coordenadas']),
        str(fila['Tipo de instrumento']) if pd.notna(fila['Tipo de instrumento']) else "No especificado",
        str(fila['Principales hallazgos / contribuciones']) if pd.notna(fila['Principales hallazgos / contribuciones']) else "En recopilación",
        str(fila['Año construcción / inicio']) if pd.notna(fila['Año construcción / inicio']) else ""
    ))

query = """
INSERT INTO observatorios (nombre, categoria, pais, continente, coordenadas, instrumentos, hallazgos, ano_inicio)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(query, registros)
conexion.commit()

print(f"¡Éxito! Se insertaron {cursor.rowcount} observatorios en la base de datos MySQL (astroatlas_db) en XAMPP.")

cursor.close()
conexion.close()