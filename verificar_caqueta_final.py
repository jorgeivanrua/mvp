import sqlite3

conn = sqlite3.connect('instance/electoral.db')
cursor = conn.cursor()

print("=" * 80)
print("VERIFICACION DE DATOS DE CAQUETA")
print("=" * 80)
print()

# Verificar departamento
cursor.execute("SELECT departamento_nombre FROM locations WHERE tipo='departamento' AND departamento_codigo='44'")
result = cursor.fetchone()
print(f"Departamento: {result[0] if result else 'NO ENCONTRADO'}")
print()

# Contar municipios
cursor.execute("SELECT COUNT(*) FROM locations WHERE tipo='municipio' AND departamento_codigo='44'")
count = cursor.fetchone()[0]
print(f"Municipios de Caqueta: {count}")

# Listar municipios
cursor.execute("SELECT municipio_nombre FROM locations WHERE tipo='municipio' AND departamento_codigo='44' ORDER BY municipio_nombre")
municipios = cursor.fetchall()
print("\nMunicipios:")
for m in municipios:
    print(f"  - {m[0]}")

print()

# Contar zonas
cursor.execute("SELECT COUNT(*) FROM locations WHERE tipo='zona' AND departamento_codigo='44'")
count = cursor.fetchone()[0]
print(f"Zonas: {count}")

# Contar puestos
cursor.execute("SELECT COUNT(*) FROM locations WHERE tipo='puesto' AND departamento_codigo='44'")
count = cursor.fetchone()[0]
print(f"Puestos: {count}")

# Contar mesas
cursor.execute("SELECT COUNT(*) FROM locations WHERE tipo='mesa' AND departamento_codigo='44'")
count = cursor.fetchone()[0]
print(f"Mesas: {count}")

print()
print("=" * 80)

conn.close()
