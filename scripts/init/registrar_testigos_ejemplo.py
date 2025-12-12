#!/usr/bin/env python3
"""
Script para registrar testigos de ejemplo
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.app import create_app
from backend.services.testigo_service import TestigoService
from backend.models.partido_politico import PartidoPolitico
from backend.database import db

def main():
    """Registrar testigos de ejemplo"""
    print("🚀 Registrando testigos de ejemplo...")
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener algunos partidos
            partidos = PartidoPolitico.query.limit(3).all()
            
            if not partidos:
                print("❌ No hay partidos políticos registrados")
                return 1
            
            # Testigos de ejemplo
            testigos_ejemplo = [
                {
                    'cedula': '12345678',
                    'nombre_completo': 'Juan Carlos Pérez García',
                    'partido_id': partidos[0].id,
                    'departamento_codigo': '18',  # Caquetá
                    'municipio_codigo': '001',    # Florencia
                },
                {
                    'cedula': '87654321',
                    'nombre_completo': 'María Elena Rodríguez López',
                    'partido_id': partidos[1].id if len(partidos) > 1 else partidos[0].id,
                    'departamento_codigo': '18',  # Caquetá
                    'municipio_codigo': '001',    # Florencia
                },
                {
                    'cedula': '11223344',
                    'nombre_completo': 'Carlos Alberto Gómez Martínez',
                    'partido_id': partidos[2].id if len(partidos) > 2 else partidos[0].id,
                    'departamento_codigo': '18',  # Caquetá
                    'municipio_codigo': '001',    # Florencia
                },
                {
                    'cedula': '55667788',
                    'nombre_completo': 'Ana Patricia Silva Hernández',
                    'partido_id': partidos[0].id,
                    'departamento_codigo': '18',  # Caquetá
                    'municipio_codigo': '029',    # San Vicente del Caguán
                },
                {
                    'cedula': '99887766',
                    'nombre_completo': 'Luis Fernando Torres Vargas',
                    'partido_id': partidos[1].id if len(partidos) > 1 else partidos[0].id,
                    'departamento_codigo': '18',  # Caquetá
                    'municipio_codigo': '029',    # San Vicente del Caguán
                }
            ]
            
            registrados = 0
            for testigo_data in testigos_ejemplo:
                try:
                    testigo = TestigoService.registrar_testigo_partido(
                        cedula=testigo_data['cedula'],
                        nombre_completo=testigo_data['nombre_completo'],
                        partido_id=testigo_data['partido_id'],
                        departamento_codigo=testigo_data['departamento_codigo'],
                        municipio_codigo=testigo_data['municipio_codigo'],
                        registrado_por='Sistema (Ejemplo)'
                    )
                    
                    print(f"✅ Testigo registrado: {testigo.cedula} - {testigo.nombre_completo}")
                    registrados += 1
                    
                except Exception as e:
                    print(f"⚠️ Error registrando testigo {testigo_data['cedula']}: {e}")
            
            print(f"\n🎉 Proceso completado: {registrados} testigos registrados")
            
            # Mostrar instrucciones
            print("\n📋 INSTRUCCIONES PARA PROBAR:")
            print("1. Ve a http://localhost:5000/login-testigo")
            print("2. Usa una de estas cédulas para probar:")
            for testigo_data in testigos_ejemplo:
                print(f"   - {testigo_data['cedula']} ({testigo_data['nombre_completo']})")
            print("3. El sistema validará automáticamente y creará el usuario")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit(main())