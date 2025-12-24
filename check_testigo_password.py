#!/usr/bin/env python3
"""
Verificar contraseña de testigos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.models.user import User

def check_testigo_password():
    app = create_app()
    with app.app_context():
        testigo = User.query.filter_by(rol='testigo_electoral').first()
        if not testigo:
            print("No se encontraron testigos")
            return
        
        print(f"Testigo: {testigo.nombre}")
        print(f"Cédula: {testigo.cedula}")
        print(f"Password hash: {testigo.password_hash[:50]}...")
        
        # Probar diferentes contraseñas
        passwords_to_try = ["test123", "testigo123", "123456", "password", testigo.cedula]
        
        for pwd in passwords_to_try:
            result = testigo.check_password(pwd)
            print(f"Password '{pwd}': {'✅ CORRECTO' if result else '❌ Incorrecto'}")
            if result:
                return pwd
        
        return None

if __name__ == "__main__":
    correct_password = check_testigo_password()
    if correct_password:
        print(f"\n🎉 Contraseña correcta encontrada: {correct_password}")
    else:
        print("\n❌ No se encontró la contraseña correcta")