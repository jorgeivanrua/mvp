#!/usr/bin/env python3
"""
Revisar testigos existentes y su configuración
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def revisar_testigos():
    """Revisar testigos existentes"""
    print("👥 REVISANDO TESTIGOS EXISTENTES")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener todos los testigos
            testigos = User.query.filter_by(rol='testigo_electoral').all()
            
            print(f"📊 Total testigos: {len(testigos)}")
            print()
            
            if testigos:
                print("🔍 DETALLES DE LOS PRIMEROS 5 TESTIGOS:")
                print("-" * 50)
                
                for i, testigo in enumerate(testigos[:5]):
                    print(f"Testigo #{i+1}:")
                    print(f"  • ID: {testigo.id}")
                    print(f"  • Nombre: {testigo.nombre}")
                    print(f"  • Cédula: {testigo.cedula}")
                    print(f"  • Activo: {testigo.activo}")
                    print(f"  • Ubicación ID: {testigo.ubicacion_id}")
                    
                    # Obtener información de ubicación
                    if testigo.ubicacion_id:
                        ubicacion = Location.query.get(testigo.ubicacion_id)
                        if ubicacion:
                            print(f"  • Ubicación: {ubicacion.nombre_completo}")
                            print(f"  • Tipo: {ubicacion.tipo}")
                            print(f"  • Departamento: {ubicacion.departamento_codigo}")
                            print(f"  • Municipio: {ubicacion.municipio_codigo}")
                            print(f"  • Zona: {ubicacion.zona_codigo}")
                            print(f"  • Puesto: {ubicacion.puesto_codigo}")
                            print(f"  • Mesa: {ubicacion.mesa_codigo}")
                        else:
                            print(f"  • ❌ Ubicación no encontrada")
                    else:
                        print(f"  • ❌ Sin ubicación asignada")
                    
                    print()
                
                # Analizar distribución por tipo de ubicación
                print("📈 DISTRIBUCIÓN POR TIPO DE UBICACIÓN:")
                print("-" * 40)
                
                ubicaciones_testigos = {}
                for testigo in testigos:
                    if testigo.ubicacion_id:
                        ubicacion = Location.query.get(testigo.ubicacion_id)
                        if ubicacion:
                            tipo = ubicacion.tipo
                            if tipo not in ubicaciones_testigos:
                                ubicaciones_testigos[tipo] = 0
                            ubicaciones_testigos[tipo] += 1
                
                for tipo, cantidad in ubicaciones_testigos.items():
                    print(f"  • {tipo}: {cantidad} testigos")
                
                print()
                
                # Verificar contraseñas
                print("🔐 VERIFICANDO CONTRASEÑAS:")
                print("-" * 30)
                
                testigo_muestra = testigos[0]
                passwords_to_test = ["test123", "admin123", "testigo123", "123456"]
                
                print(f"Probando contraseñas para: {testigo_muestra.nombre}")
                for password in passwords_to_test:
                    if testigo_muestra.check_password(password):
                        print(f"  ✅ Contraseña correcta: {password}")
                        break
                else:
                    print(f"  ❌ Ninguna contraseña de prueba funciona")
                
            else:
                print("⚠️  No hay testigos registrados")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def revisar_ubicaciones_puesto():
    """Revisar ubicaciones de tipo puesto para entender la estructura"""
    print("\n🏢 REVISANDO UBICACIONES DE PUESTO")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener puestos únicos
            puestos = Location.query.filter_by(tipo='puesto').all()
            
            print(f"📊 Total puestos: {len(puestos)}")
            print()
            
            if puestos:
                print("🔍 PRIMEROS 3 PUESTOS:")
                print("-" * 25)
                
                for i, puesto in enumerate(puestos[:3]):
                    print(f"Puesto #{i+1}:")
                    print(f"  • ID: {puesto.id}")
                    print(f"  • Nombre: {puesto.nombre_completo}")
                    print(f"  • Departamento: {puesto.departamento_codigo}")
                    print(f"  • Municipio: {puesto.municipio_codigo}")
                    print(f"  • Zona: {puesto.zona_codigo}")
                    print(f"  • Puesto: {puesto.puesto_codigo}")
                    
                    # Contar mesas en este puesto
                    mesas = Location.query.filter_by(
                        tipo='mesa',
                        departamento_codigo=puesto.departamento_codigo,
                        municipio_codigo=puesto.municipio_codigo,
                        zona_codigo=puesto.zona_codigo,
                        puesto_codigo=puesto.puesto_codigo
                    ).count()
                    
                    print(f"  • Mesas: {mesas}")
                    
                    # Contar testigos en este puesto
                    testigos_puesto = User.query.filter_by(
                        rol='testigo_electoral',
                        ubicacion_id=puesto.id
                    ).count()
                    
                    print(f"  • Testigos: {testigos_puesto}")
                    print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def probar_login_testigo():
    """Probar login de testigo con ubicación"""
    print("\n🔐 PROBANDO LOGIN DE TESTIGO")
    print("=" * 35)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener un testigo de ejemplo
            testigo = User.query.filter_by(rol='testigo_electoral').first()
            
            if not testigo:
                print("❌ No hay testigos para probar")
                return False
            
            print(f"Testigo de prueba: {testigo.nombre}")
            print(f"Cédula: {testigo.cedula}")
            
            # Obtener su ubicación
            if testigo.ubicacion_id:
                ubicacion = Location.query.get(testigo.ubicacion_id)
                if ubicacion:
                    print(f"Ubicación: {ubicacion.nombre_completo}")
                    print(f"Tipo: {ubicacion.tipo}")
                    
                    # Si está asignado a una mesa, necesitamos el puesto
                    if ubicacion.tipo == 'mesa':
                        puesto = Location.query.filter_by(
                            tipo='puesto',
                            departamento_codigo=ubicacion.departamento_codigo,
                            municipio_codigo=ubicacion.municipio_codigo,
                            zona_codigo=ubicacion.zona_codigo,
                            puesto_codigo=ubicacion.puesto_codigo
                        ).first()
                        
                        if puesto:
                            print(f"Puesto asociado: {puesto.nombre_completo}")
                            print()
                            print("📋 DATOS PARA LOGIN:")
                            print(f"  • Rol: testigo_electoral")
                            print(f"  • Departamento: {puesto.departamento_codigo}")
                            print(f"  • Municipio: {puesto.municipio_codigo}")
                            print(f"  • Zona: {puesto.zona_codigo}")
                            print(f"  • Puesto: {puesto.puesto_codigo}")
                            print(f"  • Contraseña: test123 (probablemente)")
                        else:
                            print("❌ No se encontró puesto asociado")
                    else:
                        print("❌ Testigo no está asignado a una mesa")
                else:
                    print("❌ Ubicación no encontrada")
            else:
                print("❌ Testigo sin ubicación asignada")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

if __name__ == "__main__":
    print("🔍 ANÁLISIS COMPLETO DE TESTIGOS")
    print("=" * 50)
    
    revisar_testigos()
    revisar_ubicaciones_puesto()
    probar_login_testigo()
    
    print("\n✅ ANÁLISIS COMPLETADO")