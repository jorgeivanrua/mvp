"""
Script para resetear contraseñas en Render via API
Se puede ejecutar desde cualquier lugar con acceso a la URL de Render
"""
import requests
import json

# URL de Render
RENDER_URL = "https://mvp-b9uv.onrender.com"

def reset_passwords_via_script():
    """
    Este script debe ejecutarse directamente en Render
    """
    print("="*60)
    print("SCRIPT PARA RESETEAR CONTRASEÑAS EN RENDER")
    print("="*60)
    print("\nEste script debe ejecutarse EN EL SERVIDOR de Render")
    print("No se puede ejecutar remotamente por seguridad")
    print("\nPasos para ejecutar en Render:")
    print("1. Ir al dashboard de Render")
    print("2. Seleccionar el servicio 'mvp'")
    print("3. Ir a 'Shell'")
    print("4. Ejecutar: python reset_all_passwords.py")
    print("\nO crear un endpoint temporal en el backend")
    print("="*60)

if __name__ == '__main__':
    reset_passwords_via_script()
