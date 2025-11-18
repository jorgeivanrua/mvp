"""
Script para subir la base de datos local a Render
"""
import base64
import requests

# Leer la base de datos local
with open('electoral.db', 'rb') as f:
    db_data = f.read()

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
