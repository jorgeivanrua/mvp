#!/usr/bin/env python3
"""
Script de inicialización ultra-simple para Render
Carga Quindío usando solo los datos básicos necesarios
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

def main():
    """Inicialización ultra-simple"""
    print("🚀 Inicialización simple para Render...")
    
    try:
        from backend.app import create_app
        from backend.database import db
        from backend.models.location import Location
        from backend.models.user import User
        from backend.models.departamento_config import DepartamentoConfig
        from werkzeug.security import generate_password_hash
        
        app = create_app()
        with app.app_context():
            # Verificar si ya hay datos
            if User.query.count() > 2:
                print("✅ Sistema ya inicializado")
                return
            
            print("📥 Creando datos básicos de Quindío...")
            
            # 1. Crear configuración del departamento
            config = DepartamentoConfig(
                departamento_codigo='26',
                departamento_nombre='QUINDÍO',
                habilitado=True,
                es_principal=True
            )
            db.session.add(config)
            
            # 2. Crear ubicaciones básicas
            # Departamento
            dept = Location(
                codigo='26',
                nombre='QUINDÍO',
                tipo='departamento',
                departamento_codigo='26',
                activo=True
            )
            db.session.add(dept)
            db.session.flush()
            
            # Municipio ejemplo (Armenia)
            municipio = Location(
                codigo='2600100000000',
                nombre='ARMENIA',
                tipo='municipio',
                departamento_codigo='26',
                municipio_codigo='001',
                parent_id=dept.id,
                activo=True
            )
            db.session.add(municipio)
            db.session.flush()
            
            # Puesto ejemplo
            puesto = Location(
                codigo='2600100010001',
                nombre='PUESTO 001 - ARMENIA CENTRO',
                tipo='puesto',
                departamento_codigo='26',
                municipio_codigo='001',
                puesto_codigo='001',
                parent_id=municipio.id,
                activo=True
            )
            db.session.add(puesto)
            db.session.flush()
            
            # Mesa ejemplo
            mesa = Location(
                codigo='260010001000101',
                nombre='MESA 001',
                tipo='mesa',
                departamento_codigo='26',
                municipio_codigo='001',
                puesto_codigo='001',
                mesa_numero='001',
                parent_id=puesto.id,
                activo=True
            )
            db.session.add(mesa)
            db.session.flush()
            
            # 3. Crear usuarios básicos
            password_hash = generate_password_hash('test123')
            
            # Coordinador departamental
            coord_dept = User(
                nombre='Coordinador Departamental Quindío',
                cedula=None,  # Coordinadores no necesitan cédula
                password_hash=generate_password_hash('admin123'),
                rol='coordinador_departamental',
                ubicacion_id=dept.id,
                activo=True
            )
            db.session.add(coord_dept)
            
            # Coordinador municipal
            coord_mun = User(
                nombre='Coordinador Municipal Armenia',
                cedula=None,  # Coordinadores no necesitan cédula
                password_hash=password_hash,
                rol='coordinador_municipal',
                ubicacion_id=municipio.id,
                activo=True
            )
            db.session.add(coord_mun)
            
            # Coordinador de puesto
            coord_puesto = User(
                nombre='Coordinador Puesto 001',
                cedula=None,  # Coordinadores no necesitan cédula
                password_hash=password_hash,
                rol='coordinador_puesto',
                ubicacion_id=puesto.id,
                activo=True
            )
            db.session.add(coord_puesto)
            
            # Testigo electoral (solo estos necesitan cédula)
            testigo = User(
                nombre='Testigo Electoral Mesa 001',
                cedula='12345678',  # Solo testigos necesitan cédula
                password_hash=password_hash,
                rol='testigo_electoral',
                ubicacion_id=puesto.id,  # Testigos van al puesto, no a la mesa
                activo=True
            )
            db.session.add(testigo)
            
            # Actualizar estadísticas de configuración
            config.total_ubicaciones = 4
            config.total_usuarios_creados = 4
            config.total_municipios = 1
            config.total_puestos = 1
            config.total_mesas = 1
            
            # Guardar todo
            db.session.commit()
            
            print("✅ Datos básicos creados:")
            print(f"   • 4 ubicaciones (dept, municipio, puesto, mesa)")
            print(f"   • 4 usuarios (coord dept, coord mun, coord puesto, testigo)")
            print(f"   • Testigo con cédula: 12345678")
            print(f"   • Contraseña coordinadores: admin123 (dept) / test123 (otros)")
            print(f"   • Contraseña testigo: test123")
            print("\n🎉 Sistema listo para usar!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()