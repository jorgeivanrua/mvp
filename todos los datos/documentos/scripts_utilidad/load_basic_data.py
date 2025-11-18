"""
Script simple para cargar datos básicos de prueba
"""
import sys
from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import Campana, TipoEleccion, Partido, Candidato
from datetime import date, timedelta

def load_basic_data():
    """Cargar datos básicos de prueba"""
    app = create_app()
    
    with app.app_context():
        print("\n🔄 Limpiando base de datos...")
        db.drop_all()
        db.create_all()
        print("✅ Base de datos limpia\n")
        
        # 1. Crear ubicaciones
        print("📍 Creando ubicaciones...")
        dept = Location(
            departamento_codigo='TEST01',
            departamento_nombre='Departamento Test',
            nombre_completo='Departamento Test',
            tipo='departamento'
        )
        db.session.add(dept)
        db.session.flush()
        
        mun = Location(
            departamento_codigo='TEST01',
            municipio_codigo='TEST0101',
            departamento_nombre='Departamento Test',
            municipio_nombre='Municipio Test',
            nombre_completo='Municipio Test',
            tipo='municipio'
        )
        db.session.add(mun)
        db.session.flush()
        
        puesto = Location(
            departamento_codigo='TEST01',
            municipio_codigo='TEST0101',
            zona_codigo='TEST01Z1',
            puesto_codigo='TEST0101001',
            departamento_nombre='Departamento Test',
            municipio_nombre='Municipio Test',
            puesto_nombre='Puesto Test 1',
            nombre_completo='Puesto Test 1',
            tipo='puesto'
        )
        db.session.add(puesto)
        db.session.flush()
        
        mesa = Location(
            departamento_codigo='TEST01',
            municipio_codigo='TEST0101',
            zona_codigo='TEST01Z1',
            puesto_codigo='TEST0101001',
            mesa_codigo='TEST01010010001',
            departamento_nombre='Departamento Test',
            municipio_nombre='Municipio Test',
            puesto_nombre='Puesto Test 1',
            mesa_nombre='Mesa 1',
            nombre_completo='Mesa 1 - Puesto Test 1',
            tipo='mesa',
            total_votantes_registrados=300
        )
        db.session.add(mesa)
        db.session.commit()
        print("✅ Ubicaciones creadas\n")
        
        # 2. Crear usuarios
        print("👥 Creando usuarios...")
        usuarios = [
            ('admin_test', 'super_admin', None),
            ('auditor_test', 'auditor_electoral', None),
            ('coord_dept_test', 'coordinador_departamental', dept.id),
            ('coord_mun_test', 'coordinador_municipal', mun.id),
            ('coord_puesto_test', 'coordinador_puesto', puesto.id),
            ('testigo_test_1', 'testigo_electoral', mesa.id),
        ]
        
        for nombre, rol, ubicacion_id in usuarios:
            user = User(nombre=nombre, rol=rol, ubicacion_id=ubicacion_id, activo=True)
            user.set_password('test123')
            if rol == 'testigo_electoral':
                user.verificar_presencia()
            db.session.add(user)
        
        db.session.commit()
        print("✅ Usuarios creados\n")
        
        # 3. Crear campaña
        print("📅 Creando campaña...")
        campana = Campana(
            codigo='TEST_2024',
            nombre='Campaña Test 2024',
            descripcion='Campaña de prueba',
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=30),
            color_primario='#FF5722',
            color_secundario='#FFC107',
            es_partido_completo=True,
            activa=True
        )
        db.session.add(campana)
        db.session.commit()
        print("✅ Campaña creada\n")
        
        # 4. Crear tipos de elección
        print("🗳️  Creando tipos de elección...")
        tipos = [
            TipoEleccion(codigo='PRESIDENTE', nombre='Presidente', es_uninominal=True, activo=True),
            TipoEleccion(codigo='SENADO', nombre='Senado', es_uninominal=False, permite_lista_cerrada=True, activo=True),
        ]
        for tipo in tipos:
            db.session.add(tipo)
        db.session.commit()
        print("✅ Tipos de elección creados\n")
        
        # 5. Crear partidos
        print("🏛️  Creando partidos...")
        partidos_data = [
            ('PL', 'Partido Liberal', 'PL', '#FF0000'),
            ('PC', 'Partido Conservador', 'PC', '#0000FF'),
            ('PV', 'Partido Verde', 'PV', '#00FF00'),
        ]
        for codigo, nombre, corto, color in partidos_data:
            partido = Partido(codigo=codigo, nombre=nombre, nombre_corto=corto, color=color, activo=True)
            db.session.add(partido)
        db.session.commit()
        print("✅ Partidos creados\n")
        
        print("="*60)
        print("  ✅ DATOS BÁSICOS CARGADOS")
        print("="*60)
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("   • Super Admin: admin_test / test123")
        print("   • Auditor: auditor_test / test123")
        print("   • Coord. Departamental: coord_dept_test / test123")
        print("   • Coord. Municipal: coord_mun_test / test123")
        print("   • Coord. Puesto: coord_puesto_test / test123")
        print("   • Testigo: testigo_test_1 / test123")
        print()

if __name__ == '__main__':
    load_basic_data()
