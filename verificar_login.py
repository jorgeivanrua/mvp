"""
Script para verificar que el login funciona con test123
"""
import requests

RENDER_URL = "https://mvp-b9uv.onrender.com"

# Intentar login con Super Admin
print("🔐 Verificando login con Super Admin...")
print(f"URL: {RENDER_URL}/api/auth/login")
print("Contraseña: test123")
print()

try:
    response = requests.post(
        f"{RENDER_URL}/api/auth/login",
        json={
            "rol": "super_admin",
            "password": "test123"
        },
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ Login exitoso con test123")
    else:
        print("\n❌ Login falló")
        print("Puede que la contraseña no sea test123")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
