#!/usr/bin/env python3
"""
Actualizar cédulas de testigos a 10 cifras
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.user import User

def generar_cedula_10_cifras(index):
    """Generar cédula de 10 cifras basada en el índice"""
    # Formato: 1234567890 (empezando desde 1000000001)
    base = 1000000000
    return str(base + index + 1)

def actualizar_cedulas_testigos():
    """Actualizar todas las cédulas de testigos a 10 cifras"""
    print("🔄 ACTUALIZANDO CÉDULAS DE TESTIGOS A 10 CIFRAS")
    print("=" * 55)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener todos los testigos ordenados por ID
            testigos = User.query.filter_by(rol='testigo_electoral').order_by(User.id).all()
            print(f"📊 Total testigos encontrados: {len(testigos)}")
            print()
            
            print("🔄 ACTUALIZANDO CÉDULAS:")
            print("-" * 40)
            
            for i, testigo in enumerate(testigos):
                cedula_anterior = testigo.cedula
                cedula_nueva = generar_cedula_10_cifras(i)
                
                # Actualizar cédula
                testigo.cedula = cedula_nueva
                
                # También actualizar el nombre para que coincida
                testigo.nombre = f"testigo_{cedula_nueva}"
                
                print(f"{i+1:3d}. {cedula_anterior} → {cedula_nueva}")
                
                # Commit cada 50 registros para evitar problemas
                if (i + 1) % 50 == 0:
                    db.session.commit()
                    print(f"    ✅ Guardados {i+1} registros...")
            
            # Commit final
            db.session.commit()
            
            print()
            print("✅ ACTUALIZACIÓN COMPLETADA")
            print(f"📊 {len(testigos)} testigos actualizados exitosamente")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            return False

def verificar_cedulas_actualizadas():
    """Verificar que las cédulas se actualizaron correctamente"""
    print("\n🔍 VERIFICANDO CÉDULAS ACTUALIZADAS")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            testigos = User.query.filter_by(rol='testigo_electoral').order_by(User.id).limit(10).all()
            
            print("📋 PRIMERAS 10 CÉDULAS ACTUALIZADAS:")
            print("-" * 35)
            
            for i, testigo in enumerate(testigos, 1):
                print(f"{i:2d}. Cédula: {testigo.cedula} | Nombre: {testigo.nombre}")
            
            total = User.query.filter_by(rol='testigo_electoral').count()
            print(f"\n📊 Total testigos: {total}")
            
            # Verificar que todas las cédulas tienen 10 cifras
            cedulas_incorrectas = User.query.filter(
                User.rol == 'testigo_electoral',
                db.func.length(User.cedula) != 10
            ).count()
            
            if cedulas_incorrectas == 0:
                print("✅ Todas las cédulas tienen exactamente 10 cifras")
                return True
            else:
                print(f"❌ {cedulas_incorrectas} cédulas no tienen 10 cifras")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def mostrar_ejemplos_login():
    """Mostrar ejemplos de login con las nuevas cédulas"""
    print("\n🔐 EJEMPLOS DE LOGIN CON CÉDULAS DE 10 CIFRAS")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            testigos = User.query.filter_by(rol='testigo_electoral').limit(5).all()
            
            print("📱 CREDENCIALES PARA PRUEBAS:")
            print("-" * 30)
            
            for i, testigo in enumerate(testigos, 1):
                print(f"Testigo {i}:")
                print(f"  • Cédula: {testigo.cedula}")
                print(f"  • Contraseña: test123")
                print()
            
            print("🌐 URL de Login: http://localhost:5000/login")
            print("📝 Rol: testigo_electoral")
            print("🔑 Contraseña: test123 (para todos)")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 ACTUALIZACIÓN DE CÉDULAS A 10 CIFRAS")
    print("=" * 60)
    
    if actualizar_cedulas_testigos():
        if verificar_cedulas_actualizadas():
            mostrar_ejemplos_login()
            print("\n🎉 ACTUALIZACIÓN EXITOSA")
            print("✅ Todas las cédulas ahora tienen 10 cifras")
            print("✅ Sistema listo para usar con cédulas más cortas")
        else:
            print("\n⚠️  VERIFICACIÓN FALLÓ")
            print("Algunas cédulas no se actualizaron correctamente")
    else:
        print("\n❌ ERROR EN ACTUALIZACIÓN")
        print("No se pudieron actualizar las cédulas")