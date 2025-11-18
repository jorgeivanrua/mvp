"""
Script para verificar login local y en Render
"""
import requests

def test_login(base_url, nombre="Local"):
    print(f"\n{'='*60}")
    print(f"🔐 Verificando login en {nombre}")
    print(f"{'='*60}")
    print(f"URL: {base_url}/api/auth/login")
    print("Contraseña: test123")
    print()
    
    try:
        response = requests.post(
            f"{base_url}/api/auth/login",
            json={
                "rol": "super_admin",
                "password": "test123"
            },
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {data}")
        
        if response.status_code == 200:
            print(f"\n✅ Login exitoso en {nombre} con test123")
            return True
        else:
            print(f"\n❌ Login falló en {nombre}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

# Probar local
local_ok = test_login("http://localhost:5000", "Local")

# Probar Render
render_ok = test_login("https://mvp-b9uv.onrender.com", "Render")

print(f"\n{'='*60}")
print("RESUMEN")
print(f"{'='*60}")
print(f"Local: {'✅ OK' if local_ok else '❌ FALLO'}")
print(f"Render: {'✅ OK' if render_ok else '❌ FALLO'}")
