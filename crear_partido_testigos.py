#!/usr/bin/env python3
"""
Crear partido testigos directamente en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models.partido_politico import PartidoPolitico

def crear_partido_testigos():
    """Crear el partido testigos directamente en la BD"""
    print("🔧 CREANDO PARTIDO TESTIGOS EN LA BASE DE DATOS")
    print("=" * 55)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si ya existe
            partido_existente = PartidoPolitico.query.filter(
                (PartidoPolitico.sigla.ilike('testigos')) |
                (PartidoPolitico.nombre.ilike('%testigos%'))
            ).first()
            
            if partido_existente:
                print(f"✅ Partido testigos ya existe:")
                print(f"   • ID: {partido_existente.id}")
                print(f"   • Nombre: {partido_existente.nombre}")
                print(f"   • Sigla: {partido_existente.sigla}")
                print(f"   • Color: {partido_existente.color}")
                return True
            
            # Crear nuevo partido testigos
            nuevo_partido = PartidoPolitico(
                nombre="Testigos Electorales",
                sigla="TESTIGOS",
                color="#28a745",  # Verde
                descripcion="Partido especial para testigos electorales del sistema",
                orden=999,  # Al final de la lista
                activo=True
            )
            
            db.session.add(nuevo_partido)
            db.session.commit()
            
            print(f"✅ Partido testigos creado exitosamente:")
            print(f"   • ID: {nuevo_partido.id}")
            print(f"   • Nombre: {nuevo_partido.nombre}")
            print(f"   • Sigla: {nuevo_partido.sigla}")
            print(f"   • Color: {nuevo_partido.color}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando partido testigos: {e}")
            db.session.rollback()
            return False

def verificar_partidos_existentes():
    """Verificar todos los partidos existentes"""
    print("\n📊 PARTIDOS POLÍTICOS EXISTENTES")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            partidos = PartidoPolitico.query.order_by(PartidoPolitico.orden, PartidoPolitico.nombre).all()
            
            print(f"Total partidos: {len(partidos)}")
            print()
            
            for partido in partidos:
                print(f"• {partido.sigla}: {partido.nombre}")
                print(f"  Color: {partido.color} | Orden: {partido.orden} | Activo: {partido.activo}")
                print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error obteniendo partidos: {e}")
            return False

def verificar_usuarios_testigos():
    """Verificar usuarios testigos existentes"""
    print("\n👥 USUARIOS TESTIGOS EXISTENTES")
    print("=" * 35)
    
    app = create_app()
    
    with app.app_context():
        try:
            from backend.models.user import User
            
            testigos = User.query.filter_by(rol='testigo_electoral').all()
            
            print(f"Total testigos: {len(testigos)}")
            
            if testigos:
                print("\nTestigos registrados:")
                for testigo in testigos:
                    print(f"• {testigo.nombre}")
                    print(f"  Cédula: {testigo.cedula}")
                    print(f"  Activo: {testigo.activo}")
                    print(f"  Ubicación ID: {testigo.ubicacion_id}")
                    print()
            else:
                print("\n⚠️  No hay testigos registrados")
                print("Los testigos se deben crear desde el Super Admin")
            
            return True
            
        except Exception as e:
            print(f"❌ Error obteniendo testigos: {e}")
            return False

def mostrar_instrucciones_completas():
    """Mostrar instrucciones completas para el uso de testigos"""
    print("\n📋 INSTRUCCIONES COMPLETAS PARA TESTIGOS")
    print("=" * 50)
    
    print("🔧 1. CONFIGURACIÓN INICIAL (YA COMPLETADA)")
    print("   ✅ Partido 'TESTIGOS' creado en la base de datos")
    print("   ✅ Sistema configurado para manejar testigos")
    print()
    
    print("👨‍💼 2. CREAR TESTIGOS (Super Admin)")
    print("   • Accede: http://localhost:5000/login")
    print("   • Rol: super_admin")
    print("   • Contraseña: admin123")
    print("   • Ve a gestión de usuarios")
    print("   • Crea testigos con:")
    print("     - Rol: testigo_electoral")
    print("     - Cédula: número real del testigo")
    print("     - Nombre: nombre completo")
    print("     - Contraseña: contraseña segura")
    print("     - Mesa: mesa donde votará")
    print()
    
    print("🗳️  3. LOGIN DE TESTIGOS")
    print("   • URL: http://localhost:5000/login")
    print("   • Seleccionar rol: testigo_electoral")
    print("   • Ingresar cédula (aparece campo automáticamente)")
    print("   • Ingresar contraseña")
    print("   • Acceder al dashboard de testigo")
    print()
    
    print("📝 4. FUNCIONES DEL TESTIGO")
    print("   • Registrar formularios E-14")
    print("   • Subir fotos de formularios")
    print("   • Ver estado de sus formularios")
    print("   • Reportar incidentes/delitos")
    print()
    
    print("🔄 5. FLUJO COMPLETO")
    print("   Testigo → Registra E-14 → Coordinador valida → Sistema consolida")

if __name__ == "__main__":
    print("⏰ Configurando sistema de testigos...")
    print()
    
    # Crear partido testigos
    if crear_partido_testigos():
        # Verificar partidos existentes
        verificar_partidos_existentes()
        
        # Verificar testigos existentes
        verificar_usuarios_testigos()
        
        # Mostrar instrucciones
        mostrar_instrucciones_completas()
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print("✅ El sistema está listo para manejar testigos electorales")
        print("✅ Partido 'TESTIGOS' configurado correctamente")
        print()
        print("🚀 PRÓXIMO PASO:")
        print("   Crear testigos desde el Super Admin en:")
        print("   http://localhost:5000/login")
    else:
        print("\n❌ ERROR EN CONFIGURACIÓN")
        print("No se pudo configurar el sistema de testigos")