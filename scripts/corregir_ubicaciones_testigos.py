#!/usr/bin/env python3
"""
Corregir ubicaciones de testigos - asignarlos a mesas existentes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def corregir_ubicaciones_testigos():
    """Corregir ubicaciones de testigos asignándolos a mesas existentes"""
    print("🔧 CORRIGIENDO UBICACIONES DE TESTIGOS")
    print("=" * 45)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener todos los testigos
            testigos = User.query.filter_by(rol='testigo_electoral').all()
            print(f"📊 Total testigos encontrados: {len(testigos)}")
            
            # Obtener todas las mesas disponibles
            mesas = Location.query.filter_by(tipo='mesa', activo=True).all()
            print(f"📊 Total mesas disponibles: {len(mesas)}")
            
            if not mesas:
                print("❌ No hay mesas disponibles")
                return False
            
            # Asignar testigos a mesas de forma secuencial
            testigos_corregidos = 0
            mesa_index = 0
            
            for testigo in testigos:
                # Verificar si la ubicación actual existe
                ubicacion_actual = None
                if testigo.ubicacion_id:
                    ubicacion_actual = Location.query.get(testigo.ubicacion_id)
                
                if not ubicacion_actual:
                    # Asignar a la siguiente mesa disponible
                    mesa_asignada = mesas[mesa_index % len(mesas)]
                    testigo.ubicacion_id = mesa_asignada.id
                    
                    print(f"✅ {testigo.nombre} → {mesa_asignada.nombre_completo}")
                    
                    testigos_corregidos += 1
                    mesa_index += 1
                else:
                    print(f"✓ {testigo.nombre} ya tiene ubicación válida")
            
            # Guardar cambios
            if testigos_corregidos > 0:
                db.session.commit()
                print(f"\n🎉 {testigos_corregidos} testigos corregidos exitosamente")
            else:
                print(f"\n✅ Todos los testigos ya tienen ubicaciones válidas")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            return False

def verificar_testigos_corregidos():
    """Verificar que los testigos tienen ubicaciones válidas"""
    print("\n🔍 VERIFICANDO TESTIGOS CORREGIDOS")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            testigos = User.query.filter_by(rol='testigo_electoral').all()
            
            testigos_ok = 0
            testigos_error = 0
            
            for testigo in testigos[:5]:  # Verificar primeros 5
                if testigo.ubicacion_id:
                    ubicacion = Location.query.get(testigo.ubicacion_id)
                    if ubicacion:
                        print(f"✅ {testigo.nombre}")
                        print(f"   Cédula: {testigo.cedula}")
                        print(f"   Mesa: {ubicacion.nombre_completo}")
                        print(f"   Códigos: Dept={ubicacion.departamento_codigo}, Mun={ubicacion.municipio_codigo}")
                        print(f"   Zona={ubicacion.zona_codigo}, Puesto={ubicacion.puesto_codigo}, Mesa={ubicacion.mesa_codigo}")
                        testigos_ok += 1
                    else:
                        print(f"❌ {testigo.nombre} - Ubicación ID {testigo.ubicacion_id} no existe")
                        testigos_error += 1
                else:
                    print(f"❌ {testigo.nombre} - Sin ubicación asignada")
                    testigos_error += 1
                print()
            
            print(f"📊 Resumen verificación:")
            print(f"   ✅ Testigos OK: {testigos_ok}")
            print(f"   ❌ Testigos con error: {testigos_error}")
            
            return testigos_error == 0
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def mostrar_instrucciones_login():
    """Mostrar instrucciones de login para testigos"""
    print("\n📋 INSTRUCCIONES DE LOGIN PARA TESTIGOS")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener un testigo de ejemplo
            testigo = User.query.filter_by(rol='testigo_electoral').first()
            
            if testigo and testigo.ubicacion_id:
                ubicacion = Location.query.get(testigo.ubicacion_id)
                if ubicacion:
                    # Encontrar el puesto asociado
                    puesto = Location.query.filter_by(
                        tipo='puesto',
                        departamento_codigo=ubicacion.departamento_codigo,
                        municipio_codigo=ubicacion.municipio_codigo,
                        zona_codigo=ubicacion.zona_codigo,
                        puesto_codigo=ubicacion.puesto_codigo
                    ).first()
                    
                    print("🗳️  EJEMPLO DE LOGIN PARA TESTIGO:")
                    print(f"   • URL: http://localhost:5000/login")
                    print(f"   • Rol: testigo_electoral")
                    print(f"   • Departamento: {ubicacion.departamento_codigo}")
                    print(f"   • Municipio: {ubicacion.municipio_codigo}")
                    print(f"   • Zona: {ubicacion.zona_codigo}")
                    print(f"   • Puesto: {ubicacion.puesto_codigo}")
                    print(f"   • Contraseña: test123")
                    print()
                    print("📝 FLUJO COMPLETO:")
                    print("   1. Testigo hace login con datos de ubicación (puesto)")
                    print("   2. Accede al dashboard de testigo")
                    print("   3. Se verifica en su mesa específica")
                    print("   4. Puede registrar formularios E-14")
                    
                    if puesto:
                        print(f"\n🏢 PUESTO ASOCIADO:")
                        print(f"   • {puesto.nombre_completo}")
                        
                        # Contar mesas del puesto
                        mesas_puesto = Location.query.filter_by(
                            tipo='mesa',
                            departamento_codigo=puesto.departamento_codigo,
                            municipio_codigo=puesto.municipio_codigo,
                            zona_codigo=puesto.zona_codigo,
                            puesto_codigo=puesto.puesto_codigo
                        ).count()
                        
                        print(f"   • Total mesas: {mesas_puesto}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 CORRECCIÓN DE UBICACIONES DE TESTIGOS")
    print("=" * 55)
    
    if corregir_ubicaciones_testigos():
        if verificar_testigos_corregidos():
            mostrar_instrucciones_login()
            print("\n🎉 CORRECCIÓN COMPLETADA EXITOSAMENTE")
            print("✅ Los testigos ahora pueden hacer login con ubicación")
            print("✅ Una vez dentro, se verifican en su mesa específica")
        else:
            print("\n⚠️  VERIFICACIÓN FALLÓ")
            print("Algunos testigos aún tienen problemas de ubicación")
    else:
        print("\n❌ ERROR EN CORRECCIÓN")
        print("No se pudieron corregir las ubicaciones de los testigos")