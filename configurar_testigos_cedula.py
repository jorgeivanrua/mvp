#!/usr/bin/env python3
"""
Configurar sistema de testigos con autenticación por cédula
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location

def limpiar_ubicaciones_testigos():
    """Limpiar ubicaciones fijas de testigos - deben ser NULL"""
    print("🧹 LIMPIANDO UBICACIONES FIJAS DE TESTIGOS")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener todos los testigos
            testigos = User.query.filter_by(rol='testigo_electoral').all()
            print(f"📊 Total testigos encontrados: {len(testigos)}")
            
            testigos_limpiados = 0
            
            for testigo in testigos:
                if testigo.ubicacion_id is not None:
                    print(f"🧹 Limpiando ubicación de {testigo.nombre} (cédula: {testigo.cedula})")
                    testigo.ubicacion_id = None
                    testigos_limpiados += 1
                else:
                    print(f"✓ {testigo.nombre} ya sin ubicación fija")
            
            if testigos_limpiados > 0:
                db.session.commit()
                print(f"\n✅ {testigos_limpiados} testigos limpiados exitosamente")
            else:
                print(f"\n✅ Todos los testigos ya estaban sin ubicación fija")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            return False

def verificar_configuracion_testigos():
    """Verificar que los testigos están configurados correctamente"""
    print("\n🔍 VERIFICANDO CONFIGURACIÓN DE TESTIGOS")
    print("=" * 45)
    
    app = create_app()
    
    with app.app_context():
        try:
            testigos = User.query.filter_by(rol='testigo_electoral').all()
            
            print(f"📊 Total testigos: {len(testigos)}")
            print()
            
            # Verificar primeros 5 testigos
            for i, testigo in enumerate(testigos[:5]):
                print(f"Testigo #{i+1}:")
                print(f"  • Nombre: {testigo.nombre}")
                print(f"  • Cédula: {testigo.cedula}")
                print(f"  • Ubicación ID: {testigo.ubicacion_id} {'✅ (NULL - correcto)' if testigo.ubicacion_id is None else '❌ (debe ser NULL)'}")
                print(f"  • Activo: {testigo.activo}")
                print(f"  • Presencia verificada: {testigo.presencia_verificada}")
                print()
            
            # Contar testigos por estado
            sin_ubicacion = sum(1 for t in testigos if t.ubicacion_id is None)
            con_ubicacion = len(testigos) - sin_ubicacion
            
            print(f"📈 RESUMEN:")
            print(f"  • Sin ubicación fija (correcto): {sin_ubicacion}")
            print(f"  • Con ubicación fija (incorrecto): {con_ubicacion}")
            
            return con_ubicacion == 0
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def mostrar_flujo_testigos():
    """Mostrar el flujo correcto para testigos"""
    print("\n📋 FLUJO CORRECTO PARA TESTIGOS")
    print("=" * 40)
    
    print("🔄 FLUJO COMPLETO:")
    print("1. 📥 CARGA INICIAL:")
    print("   • Testigos se cargan por municipio desde CSV")
    print("   • NO tienen ubicación fija (ubicacion_id = NULL)")
    print("   • Tienen cédula como identificador único")
    print()
    
    print("2. 🔐 LOGIN:")
    print("   • URL: http://localhost:5000/login")
    print("   • Rol: testigo_electoral")
    print("   • Cédula: [número de cédula del testigo]")
    print("   • Contraseña: [contraseña asignada]")
    print()
    
    print("3. 📍 VERIFICACIÓN EN MESA:")
    print("   • Una vez logueado, accede al dashboard")
    print("   • Se verifica en una mesa específica")
    print("   • Esta ubicación se guarda para futuras sesiones")
    print("   • Puede registrar formularios E-14 en esa mesa")
    print()
    
    print("4. 🔄 SESIONES FUTURAS:")
    print("   • Si ya se verificó antes, se carga automáticamente en esa mesa")
    print("   • Puede cambiar de mesa si es necesario")
    print()
    
    app = create_app()
    with app.app_context():
        try:
            testigo_ejemplo = User.query.filter_by(rol='testigo_electoral').first()
            if testigo_ejemplo:
                print("🗳️  EJEMPLO DE LOGIN:")
                print(f"   • Cédula: {testigo_ejemplo.cedula}")
                print(f"   • Contraseña: test123")
                print(f"   • Presencia verificada: {testigo_ejemplo.presencia_verificada}")
                if testigo_ejemplo.presencia_verificada_at:
                    print(f"   • Verificado en: {testigo_ejemplo.presencia_verificada_at}")
        except Exception as e:
            print(f"❌ Error obteniendo ejemplo: {e}")

def crear_endpoint_login_cedula():
    """Mostrar cómo debe ser el endpoint de login por cédula"""
    print("\n🔧 MODIFICACIÓN NECESARIA EN AUTH SERVICE")
    print("=" * 50)
    
    print("El sistema necesita modificar backend/services/auth_service.py:")
    print()
    print("```python")
    print("# Para testigos, buscar por cédula en lugar de ubicación")
    print("if rol == 'testigo_electoral':")
    print("    cedula = ubicacion_data.get('cedula')")
    print("    if not cedula:")
    print("        raise AuthenticationException('Cédula requerida para testigos')")
    print("    ")
    print("    user = User.query.filter_by(")
    print("        rol='testigo_electoral',")
    print("        cedula=cedula,")
    print("        activo=True")
    print("    ).first()")
    print("else:")
    print("    # Lógica normal para otros roles...")
    print("```")
    print()
    print("Y modificar backend/routes/auth.py para aceptar 'cedula' en el JSON")

if __name__ == "__main__":
    print("🚀 CONFIGURACIÓN DE TESTIGOS CON CÉDULA")
    print("=" * 55)
    
    if limpiar_ubicaciones_testigos():
        if verificar_configuracion_testigos():
            mostrar_flujo_testigos()
            crear_endpoint_login_cedula()
            print("\n🎉 CONFIGURACIÓN COMPLETADA")
            print("✅ Testigos configurados para login por cédula")
            print("⚠️  PENDIENTE: Modificar auth_service.py para login por cédula")
        else:
            print("\n⚠️  VERIFICACIÓN FALLÓ")
            print("Algunos testigos aún tienen ubicación fija")
    else:
        print("\n❌ ERROR EN CONFIGURACIÓN")
        print("No se pudieron limpiar las ubicaciones de los testigos")