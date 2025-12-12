#!/usr/bin/env python3
"""
Script para aplicar migración de cédula y asignar cédulas a testigos existentes
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.app import create_app
from backend.migrations.add_cedula_to_users import upgrade
from backend.models.user import User
from backend.database import db

def main():
    """Aplicar migración y asignar cédulas"""
    print("🚀 Aplicando migración de cédula para testigos...")
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Ejecutar migración
            upgrade()
            
            # Asignar cédulas a testigos existentes que no las tengan
            testigos_sin_cedula = User.query.filter_by(
                rol='testigo_electoral',
                cedula=None,
                activo=True
            ).all()
            
            print(f"📋 Encontrados {len(testigos_sin_cedula)} testigos sin cédula")
            
            cedula_base = 10000000  # Empezar desde 10 millones
            
            for i, testigo in enumerate(testigos_sin_cedula):
                cedula_generada = str(cedula_base + i)
                testigo.cedula = cedula_generada
                
                print(f"✅ Testigo {testigo.nombre} -> Cédula: {cedula_generada}")
            
            db.session.commit()
            
            print(f"\n🎉 Migración completada:")
            print(f"   - Campo cédula agregado a la tabla users")
            print(f"   - {len(testigos_sin_cedula)} testigos actualizados con cédulas")
            
            # Mostrar instrucciones
            print("\n📋 INSTRUCCIONES PARA PROBAR:")
            print("1. Ve a http://localhost:5000/login-testigo")
            print("2. Usa una de estas cédulas para probar:")
            
            # Mostrar algunos ejemplos
            testigos_ejemplo = User.query.filter_by(
                rol='testigo_electoral',
                activo=True
            ).filter(User.cedula.isnot(None)).limit(5).all()
            
            for testigo in testigos_ejemplo:
                print(f"   - {testigo.cedula} ({testigo.nombre})")
            
            print("3. El sistema te llevará al dashboard del testigo")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(main())