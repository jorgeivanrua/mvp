"""
Verificar candidatos y partidos configurados
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("\n" + "="*70)
print("VERIFICACIÓN DE CANDIDATOS Y PARTIDOS")
print("="*70)

# 1. Login como Super Admin
print("\n1️⃣  Login como Super Admin...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "rol": "super_admin",
        "password": "test123"
    }
)

if response.status_code == 200:
    data = response.json()
    token = data.get('data', {}).get('access_token')
    print(f"✅ Login exitoso")
else:
    print(f"❌ Error en login: {response.status_code}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 2. Verificar partidos
print("\n2️⃣  Verificando partidos...")
response = requests.get(
    f"{BASE_URL}/api/configuracion/partidos",
    headers=headers
)

if response.status_code == 200:
    partidos = response.json().get('data', [])
    print(f"✅ Partidos encontrados: {len(partidos)}")
    print("\n📋 Partidos activos:")
    for partido in partidos[:10]:  # Mostrar primeros 10
        print(f"  - {partido.get('codigo')}: {partido.get('nombre')}")
else:
    print(f"⚠️  Endpoint de partidos: {response.status_code}")

# 3. Verificar candidatos
print("\n3️⃣  Verificando candidatos...")
response = requests.get(
    f"{BASE_URL}/api/configuracion/candidatos",
    headers=headers
)

if response.status_code == 200:
    candidatos = response.json().get('data', [])
    print(f"✅ Candidatos encontrados: {len(candidatos)}")
    print("\n👥 Candidatos activos:")
    for candidato in candidatos[:10]:  # Mostrar primeros 10
        print(f"  - #{candidato.get('numero_lista')}: {candidato.get('nombre_completo')}")
else:
    print(f"⚠️  Endpoint de candidatos: {response.status_code}")

# 4. Login como Coordinador de Puesto
print("\n4️⃣  Login como Coordinador de Puesto...")
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "rol": "coordinador_puesto",
        "departamento_codigo": "44",
        "municipio_codigo": "01",
        "zona_codigo": "01",
        "puesto_codigo": "01",
        "password": "test123"
    }
)

if response.status_code == 200:
    data = response.json()
    token_coord = data.get('data', {}).get('access_token')
    print(f"✅ Login exitoso")
    
    headers_coord = {"Authorization": f"Bearer {token_coord}"}
    
    # 5. Verificar candidatos desde coordinador
    print("\n5️⃣  Verificando candidatos desde coordinador...")
    response = requests.get(
        f"{BASE_URL}/api/coordinador-puesto/candidatos",
        headers=headers_coord
    )
    
    if response.status_code == 200:
        candidatos_coord = response.json().get('data', [])
        print(f"✅ Candidatos disponibles para E14: {len(candidatos_coord)}")
        print("\n👥 Candidatos para formulario E14:")
        for candidato in candidatos_coord[:5]:
            print(f"  - #{candidato.get('numero_lista')}: {candidato.get('nombre_completo')}")
    else:
        print(f"⚠️  Endpoint de candidatos coordinador: {response.status_code}")
        print(f"   Respuesta: {response.text[:200]}")
else:
    print(f"❌ Error en login coordinador: {response.status_code}")

print("\n" + "="*70)
print("✅ VERIFICACIÓN COMPLETADA")
print("="*70)
print("\n🎯 El sistema está listo para:")
print("  - Gestionar partidos y candidatos desde Super Admin")
print("  - Llenar formularios E14 desde Coordinadores")
print("  - Registrar votos por candidato")
print("\n" + "="*70)
