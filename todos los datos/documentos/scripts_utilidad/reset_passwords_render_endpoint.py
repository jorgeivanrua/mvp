"""
Script para resetear contraseñas en Render
"""
import requests

url = 'https://dia-d.onrender.com/reset-all-passwords-secret-endpoint-2024'

print("🔑 Reseteando contraseñas en Render...")
print("⏳ Esto puede tardar unos segundos...")

try:
    response = requests.post(url, timeout=60)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Contraseñas reseteadas exitosamente!")
        print(f"Usuarios actualizados: {result.get('usuarios_actualizados', 0)}")
        print("\n🔑 Nuevas contraseñas:")
        print("   Todos los usuarios: test123")
        print("\n📝 Usuarios disponibles:")
        for usuario in result.get('usuarios', []):
            print(f"   - {usuario}")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n❌ Error: {e}")
