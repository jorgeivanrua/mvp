#!/usr/bin/env python3
"""
Script para probar la funcionalidad de carga masiva de testigos
"""
import sys
import json
import requests
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
ADMIN_CREDENTIALS = {
    "rol": "super_admin",
    "password": "admin123"
}

def login_admin():
    """Login como administrador"""
    print("🔐 Iniciando sesión como administrador...")
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=ADMIN_CREDENTIALS)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('data', {}).get('access_token')
        if token:
            print(f"✅ Login exitoso. Token obtenido.")
            return token
        else:
            print(f"❌ No se encontró token en respuesta: {data}")
            return None
    else:
        print(f"❌ Error en login: {response.status_code} - {response.text}")
        return None

def test_csv_template(token):
    """Probar descarga de plantilla CSV"""
    print("\n📄 Probando descarga de plantilla CSV...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/testigos-registrados/plantilla-csv", headers=headers)
    
    if response.status_code == 200:
        print("✅ Plantilla CSV descargada exitosamente")
        print(f"Contenido: {response.text[:100]}...")
        return True
    else:
        print(f"❌ Error descargando plantilla: {response.status_code} - {response.text}")
        return False

def test_bulk_loading(token):
    """Probar carga masiva de testigos"""
    print("\n📋 Probando carga masiva de testigos...")
    
    # Datos de prueba
    test_data = {
        "departamento_codigo": "44",  # Caquetá
        "municipio_codigo": "01",     # Florencia
        "testigos": [
            {
                "cedula": "12345678",
                "nombre_completo": "Juan Pérez García"
            },
            {
                "cedula": "87654321", 
                "nombre_completo": "María López Rodríguez"
            },
            {
                "cedula": "11223344",
                "nombre_completo": "Carlos Martínez Silva"
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/testigos-registrados/cargar-masivo", 
        json=test_data,
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Carga masiva exitosa")
        print(f"Exitosos: {data['data']['exitosos']}")
        print(f"Errores: {data['data']['errores']}")
        print(f"Total procesados: {data['data']['total_procesados']}")
        return True
    else:
        print(f"❌ Error en carga masiva: {response.status_code} - {response.text}")
        return False

def test_testigo_login():
    """Probar login de testigo con cédula"""
    print("\n🔑 Probando login de testigo con cédula...")
    
    # Probar login simplificado con solo cédula
    login_data = {
        "cedula": "12345678"
    }
    
    response = requests.post(f"{BASE_URL}/api/testigos-registrados/login-cedula-simple", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login de testigo exitoso")
        print(f"Testigo: {data.get('user', {}).get('nombre', 'N/A')}")
        return True
    else:
        print(f"❌ Error en login de testigo: {response.status_code} - {response.text}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del sistema de carga masiva de testigos")
    print("=" * 60)
    
    # 1. Login como admin
    token = login_admin()
    if not token:
        print("❌ No se pudo obtener token de administrador")
        return False
    
    # 2. Probar plantilla CSV
    if not test_csv_template(token):
        print("❌ Falló la prueba de plantilla CSV")
        return False
    
    # 3. Probar carga masiva
    if not test_bulk_loading(token):
        print("❌ Falló la prueba de carga masiva")
        return False
    
    # 4. Probar login de testigo
    if not test_testigo_login():
        print("❌ Falló la prueba de login de testigo")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ¡Todas las pruebas pasaron exitosamente!")
    print("✅ Sistema de carga masiva funcionando correctamente")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)