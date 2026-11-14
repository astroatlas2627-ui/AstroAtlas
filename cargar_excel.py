import os
import sqlite3
import pandas as pd

# 1. Rutas
EXCEL_FILE = "observatorios_astronomicos_mundo_categorizados (BASE_DE _DATOS).xlsx"
DB_DIR = os.path.join("data_base", "observatorios")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "observatorios.db")

# 2. Conectar a SQLite y crear la tabla con la estructura del Excel
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS observatorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT,
    pais TEXT NOT NULL,
    continente TEXT,
    coordenadas TEXT,
    instrumentos TEXT,
    hallazgos TEXT,
    ano_inicio TEXT
)
""")

# 3. Leer la hoja 'Observatorios' del Excel
print("Leyendo archivo Excel...")
df = pd.read_excel(EXCEL_FILE, sheet_name='Observatorios')

# 4. Formatear y limpiar datos
# Unimos Latitud y Longitud para el campo de coordenadas
df['coordenadas'] = df['Latitud (°)'].astype(str) + ", " + df['Longitud (°)'].astype(str)

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

# 5. Insertar los registros en la base de datos
cursor.executemany("""
INSERT INTO observatorios (nombre, categoria, pais, continente, coordenadas, instrumentos, hallazgos, ano_inicio)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", registros)

conn.commit()
conn.close()
print(f"¡Éxito! Se importaron {len(registros)} observatorios en {DB_PATH}.")

import os
import sqlite3
import pandas as pd

# Rutas directas en tu proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "observatorios_astronomicos_mundo_categorizados (BASE_DE _DATOS).xlsx")
DB_DIR = os.path.join(BASE_DIR, "data_base", "observatorios")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "observatorios.db")

print(f"Cargando Excel desde: {EXCEL_FILE}")
df = pd.read_excel(EXCEL_FILE, sheet_name='Observatorios')

# Unir coordenadas latitud y longitud
df['coordenadas'] = df['Latitud (°)'].astype(str) + ", " + df['Longitud (°)'].astype(str)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Crear la tabla limpia
cursor.execute("""
CREATE TABLE IF NOT EXISTS observatorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT,
    pais TEXT NOT NULL,
    continente TEXT,
    coordenadas TEXT,
    instrumentos TEXT,
    hallazgos TEXT,
    ano_inicio TEXT
)
""")

# Limpiar registros previos si hubiera alguno corrupto
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

cursor.executemany("""
INSERT INTO observatorios (nombre, categoria, pais, continente, coordenadas, instrumentos, hallazgos, ano_inicio)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", registros)

conn.commit()
conn.close()

print(f"--> ¡Listo! Se insertaron {len(registros)} observatorios en {DB_PATH}")