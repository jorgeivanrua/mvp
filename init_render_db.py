"""
Script de inicialización de base de datos para Render
Se ejecuta automáticamente al desplegar
"""
import os
from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import Campana, TipoEleccion, Partido

def init_database():
    """Inicializar base de datos con datos básicos"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Inicializando base de datos...")
        
        # Crear todas las tablas
        db.create_all()
        print("✓ Tablas creadas")
        
        # Verificar si ya hay datos
        if User.query.first() is not None:
            print("✓ Base de datos ya tiene datos, saltando inicialización")
            return
        
        print("📊 Cargando datos iniciales...")
        
        # 1. Crear ubicaciones básicas
        print("  - Creando ubicaciones...")
        
        # Departamento
        dept = Location(
            departamento_codigo='44',
            municipio_codigo=None,
            zona_codigo=None,
            puesto_codigo=None,
            mesa_codigo=None,
            departamento_nombre='CAQUETA',
            municipio_nombre=None,
            puesto_nombre=None,
            mesa_nombre=None,
            nombre_completo='CAQUETA',
            tipo='departamento',
            total_votantes_registrados=0,
            mujeres=0,
            hombres=0,
            activo=True
        )
        db.session.add(dept)
        db.session.flush()
        
        # Municipio
        muni = Location(
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo=None,
            puesto_codigo=None,
            mesa_codigo=None,
            departamento_nombre='CAQUETA',
            municipio_nombre='FLORENCIA',
            puesto_nombre=None,
            mesa_nombre=None,
            nombre_completo='CAQUETA - FLORENCIA',
            tipo='municipio',
            total_votantes_registrados=0,
            mujeres=0,
            hombres=0,
            activo=True
        )
        db.session.add(muni)
        db.session.flush()
        
        # Zona
        zona = Location(
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo='01',
            puesto_codigo=None,
            mesa_codigo=None,
            departamento_nombre='CAQUETA',
            municipio_nombre='FLORENCIA',
            puesto_nombre=None,
            mesa_nombre=None,
            nombre_completo='CAQUETA - FLORENCIA - Zona 01',
            tipo='zona',
            total_votantes_registrados=0,
            mujeres=0,
            hombres=0,
            activo=True
        )
        db.session.add(zona)
        db.session.flush()
        
        # Puesto
        puesto = Location(
            departamento_codigo='44',
            municipio_codigo='01',
            zona_codigo='01',
            puesto_codigo='01',
            mesa_codigo=None,
            departamento_nombre='CAQUETA',
            municipio_nombre='FLORENCIA',
            puesto_nombre='I.E. JUAN BAUTISTA LA SALLE',
            mesa_nombre=None,
            nombre_completo='CAQUETA - FLORENCIA - Zona 01 - I.E. JUAN BAUTISTA LA SALLE',
            tipo='puesto',
            total_votantes_registrados=0,
            mujeres=0,
            hombres=0,
            direccion='Calle Principal',
            activo=True
        )
        db.session.add(puesto)
        db.session.flush()
        
        db.session.commit()
        print("  ✓ 4 ubicaciones creadas")
        
        # 2. Crear usuarios
        print("  - Creando usuarios...")
        
        usuarios = [
            {
                'nombre': 'Super Admin',
                'rol': 'super_admin',
                'ubicacion_id': None
            },
            {
                'nombre': 'Admin Departamental Caquetá',
                'rol': 'admin_departamental',
                'ubicacion_id': dept.id
            },
            {
                'nombre': 'Admin Municipal Florencia',
                'rol': 'admin_municipal',
                'ubicacion_id': muni.id
            },
            {
                'nombre': 'Coordinador Departamental Caquetá',
                'rol': 'coordinador_departamental',
                'ubicacion_id': dept.id
            },
            {
                'nombre': 'Coordinador Municipal Florencia',
                'rol': 'coordinador_municipal',
                'ubicacion_id': muni.id
            },
            {
                'nombre': 'Coordinador Puesto 01',
                'rol': 'coordinador_puesto',
                'ubicacion_id': puesto.id
            },
            {
                'nombre': 'Auditor Electoral Caquetá',
                'rol': 'auditor_electoral',
                'ubicacion_id': dept.id
            },
            {
                'nombre': 'Testigo Electoral Puesto 01',
                'rol': 'testigo_electoral',
                'ubicacion_id': puesto.id
            }
        ]
        
        for user_data in usuarios:
            user = User(
                nombre=user_data['nombre'],
                rol=user_data['rol'],
                ubicacion_id=user_data['ubicacion_id'],
                activo=True
            )
            user.set_password('test123')
            db.session.add(user)
        
        db.session.commit()
        print(f"  ✓ {len(usuarios)} usuarios creados (contraseña: test123)")
        
        # 3. Crear tipos de elección
        print("  - Creando tipos de elección...")
        
        tipos = [
            {'codigo': 'presidencia', 'nombre': 'Presidencia de la República', 'es_uninominal': True},
            {'codigo': 'senado', 'nombre': 'Senado de la República', 'es_uninominal': False},
            {'codigo': 'camara', 'nombre': 'Cámara de Representantes', 'es_uninominal': False},
            {'codigo': 'gobernacion', 'nombre': 'Gobernación Departamental', 'es_uninominal': True},
            {'codigo': 'asamblea', 'nombre': 'Asamblea Departamental', 'es_uninominal': False},
            {'codigo': 'alcaldia', 'nombre': 'Alcaldía Municipal', 'es_uninominal': True},
            {'codigo': 'concejo', 'nombre': 'Concejo Municipal', 'es_uninominal': False},
        ]
        
        for tipo_data in tipos:
            tipo_dict = {
                'codigo': tipo_data['codigo'],
                'nombre': tipo_data['nombre'],
                'activo': True
            }
            
            # Agregar campos opcionales si existen en el modelo
            if hasattr(TipoEleccion, 'es_uninominal'):
                tipo_dict['es_uninominal'] = tipo_data.get('es_uninominal', False)
            if hasattr(TipoEleccion, 'permite_lista_cerrada'):
                tipo_dict['permite_lista_cerrada'] = True
            if hasattr(TipoEleccion, 'permite_lista_abierta'):
                tipo_dict['permite_lista_abierta'] = False
            
            tipo = TipoEleccion(**tipo_dict)
            db.session.add(tipo)
        
        db.session.commit()
        print(f"  ✓ {len(tipos)} tipos de elección creados")
        
        # 4. Crear partidos
        print("  - Creando partidos...")
        
        partidos = [
            {'codigo': 'LIBERAL', 'nombre': 'Partido Liberal Colombiano', 'nombre_corto': 'Liberal', 'color': '#FF0000'},
            {'codigo': 'CONSERVADOR', 'nombre': 'Partido Conservador Colombiano', 'nombre_corto': 'Conservador', 'color': '#0000FF'},
            {'codigo': 'VERDE', 'nombre': 'Partido Alianza Verde', 'nombre_corto': 'Verde', 'color': '#00FF00'},
        ]
        
        for partido_data in partidos:
            partido = Partido(
                codigo=partido_data['codigo'],
                nombre=partido_data['nombre'],
                nombre_corto=partido_data['nombre_corto'],
                color=partido_data['color'],
                activo=True
            )
            db.session.add(partido)
        
        db.session.commit()
        print(f"  ✓ {len(partidos)} partidos creados")
        
        print("\n✅ Base de datos inicializada correctamente")
        print("\n📊 Resumen:")
        print(f"  - Ubicaciones: {Location.query.count()}")
        print(f"  - Usuarios: {User.query.count()}")
        print(f"  - Tipos de elección: {TipoEleccion.query.count()}")
        print(f"  - Partidos: {Partido.query.count()}")
        print("\n🔑 Contraseña para todos los usuarios: test123")

if __name__ == '__main__':
    init_database()
