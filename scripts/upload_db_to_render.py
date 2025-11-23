"""
Script para subir la base de datos local a Render (comprimida)
"""
import base64
import requests
import gzip
import os

# Usar la ruta correcta de la BD
db_path = 'instance/electoral.db'

if not os.path.exists(db_path):
    print(f"❌ No se encontró el archivo: {db_path}")
    exit(1)

print(f"📦 Leyendo base de datos desde: {db_path}")

with open(db_path, 'rb') as f:
    db_data = f.read()

print(f"✅ Base de datos leída: {len(db_data):,} bytes ({len(db_data)/1024/1024:.2f} MB)")

# Comprimir con gzip
print("🗜️  Comprimiendo...")
db_compressed = gzip.compress(db_data, compresslevel=9)
print(f"✅ Comprimida: {len(db_compressed):,} bytes ({len(db_compressed)/1024/1024:.2f} MB)")
print(f"📊 Reducción: {(1 - len(db_compressed)/len(db_data))*100:.1f}%")

# Convertir a base64
print("🔄 Convirtiendo a base64...")
db_base64 = base64.b64encode(db_compressed).decode('utf-8')
print(f"✅ Base64: {len(db_base64):,} caracteres")

# Subir a Render usando el endpoint especial
url = 'https://dia-d.onrender.com/upload-database-secret-endpoint-2024'

print(f"\n📤 Subiendo a Render...")
print("⏳ Esto puede tardar 1-2 minutos...")

try:
    response = requests.post(url, json={'database': db_base64, 'compressed': True}, timeout=120)
    
    if response.status_code == 200:
        print("\n✅ Base de datos subida exitosamente!")
        print(response.json())
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n❌ Error: {e}")
