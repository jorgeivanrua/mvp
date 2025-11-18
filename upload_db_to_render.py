"""
Script para subir la base de datos local a Render
"""
import base64
import requests

# Leer la base de datos local
import os

# Usar la ruta correcta de la BD
db_path = 'instance/electoral.db'

if not os.path.exists(db_path):
    print(f"❌ No se encontró el archivo: {db_path}")
    exit(1)

print(f"📦 Leyendo base de datos desde: {db_path}")

with open(db_path, 'rb') as f:
    db_data = f.read()

print(f"✅ Base de datos leída: {len(db_data)} bytes")

# Convertir a base64
db_base64 = base64.b64encode(db_data).decode('utf-8')

# Subir a Render usando el endpoint especial
url = 'https://dia-d.onrender.com/upload-database-secret-endpoint-2024'

response = requests.post(url, json={'database': db_base64})

if response.status_code == 200:
    print("✅ Base de datos subida exitosamente")
    print(response.json())
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
