#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test detallado del testigo"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

BASE_URL = "http://localhost:5000"

print("\n=== TEST DETALLADO TESTIGO ===\n")

# 1. Login
print("1. Login...")
response = requests.post(f"{BASE_URL}/api/auth/login", json={
    "rol": "testigo_electoral",
    "departamento_codigo": "44",
    "municipio_codigo": "01",
    "puesto_codigo": "001",
    "password": "test123"
})

print(f"Status: {response.status_code}")
response_data = response.json()
print(f"Response: {json.dumps(response_data, indent=2)}")

if response.status_code != 200:
    print("\n✗ Login fallido")
    exit(1)

# El token está en data.access_token
token = response_data.get('data', {}).get('access_token')
if not token:
    # Fallback: buscar directamente
    token = response_data.get('access_token')

print(f"\nToken obtenido: {token[:50]}...")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
print("✓ Login exitoso\n")

# 2. Verificar presencia
print("2. Verificar presencia...")
response = requests.post(f"{BASE_URL}/api/auth/verificar-presencia", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")

# 3. Obtener mesa
print("3. Obtener información de mesa...")
response = requests.get(f"{BASE_URL}/api/testigo/mesa", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")

# 4. Tipos de elección
print("4. Obtener tipos de elección...")
response = requests.get(f"{BASE_URL}/api/testigo/tipos-eleccion", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Tipos: {len(data.get('data', data))}")
print(f"Response: {response.text[:200]}...\n")

# 5. Partidos
print("5. Obtener partidos...")
response = requests.get(f"{BASE_URL}/api/testigo/partidos", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Partidos: {len(data.get('data', data))}")
print(f"Response: {response.text[:200]}...\n")

# 6. Candidatos
print("6. Obtener candidatos...")
response = requests.get(f"{BASE_URL}/api/testigo/candidatos?tipo_eleccion_id=1", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Candidatos: {len(data.get('data', data))}")
print(f"Response: {response.text[:200]}...\n")

# 7. Registrar formulario
print("7. Registrar formulario E-14...")
# Datos corregidos: total_votos debe ser <= votantes_registrados (300)
# total_tarjetas = total_votos + tarjetas_no_marcadas
formulario = {
    "mesa_id": 403,
    "tipo_eleccion_id": 1,
    "total_votantes_registrados": 300,
    "total_votos": 285,  # 150 + 120 + 10 + 5
    "votos_validos": 270,  # 150 + 120
    "votos_nulos": 5,
    "votos_blanco": 10,
    "tarjetas_no_marcadas": 15,  # 300 - 285
    "total_tarjetas": 300,  # total_votos + tarjetas_no_marcadas
    "estado": "pendiente",
    "votos_partidos": [
        {"partido_id": 1, "votos": 150},
        {"partido_id": 2, "votos": 120}
    ],
    "votos_candidatos": [
        {"candidato_id": 1, "votos": 150},
        {"candidato_id": 2, "votos": 120}
    ]
}
response = requests.post(f"{BASE_URL}/api/formularios", json=formulario, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")

# 8. Registrar incidente
print("8. Registrar incidente...")
incidente = {
    "tipo_incidente": "retraso_apertura",
    "titulo": "Retraso en apertura de mesa",
    "descripcion": "La mesa abrió 30 minutos tarde debido a la ausencia inicial de jurados",
    "severidad": "media",
    "mesa_id": 403,
    "fecha_incidente": "2025-11-16T08:30:00"
}
response = requests.post(f"{BASE_URL}/api/incidentes", json=incidente, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")

# 9. Registrar delito
print("9. Registrar delito...")
delito = {
    "tipo_delito": "compra_votos",
    "titulo": "Compra de votos detectada",
    "descripcion": "Se observó entrega de dinero a votantes cerca del puesto de votación",
    "severidad": "alta",
    "mesa_id": 403,
    "evidencia_url": None,
    "requiere_denuncia_formal": True,
    "fecha_delito": "2025-11-16T10:00:00"
}
response = requests.post(f"{BASE_URL}/api/delitos", json=delito, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}\n")

print("=== TEST COMPLETADO ===")
