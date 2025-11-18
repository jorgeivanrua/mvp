"""
Script simple para cargar datos básicos
"""
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato
from datetime import datetime

def load_basic_data_simple():
    """Cargar datos básicos mínimos"""
    print("\n🚀 Iniciando carga de datos básicos...")
    
    try:
        # 1. Crear ubicaciones básicas
        print("📍 Creando ubicaciones...")
        
        # Departamento
        dept = Location(
            departamento_codigo='05',
            departamento_nombre='Antioquia',
            nombre_completo='Antioquia',
            tipo='departamento'
        )
        db.session.add(dept)
        db.session.flush()
        
        # Municipio
        mun = Location(
            departamento_codigo='05',
            municipio_codigo='05001',
            departamento_nombre='Antioquia',
            municipio_nombre='Medellín',
            nombre_completo='Medellín - Antioquia',
            tipo='municipio'
        )
        db.session.add(mun)
        db.session.flush()
        
        # Zona
        zona = Location(
            departamento_codigo='05',
            municipio_codigo='05001',
            zona_codigo='0500101',
            departamento_nombre='Antioquia',
            municipio_nombre='Medellín',
            zona_nombre='Zona 1',
            nombre_completo='Zona 1 - Medellín - Antioquia',
            tipo='zona'
        )
        db.session.add(zona)
        db.session.flush()
        
        # Puesto
        puesto = Location(
            departamento_codigo='05',
            municipio_codigo='05001',
            zona_codigo='0500101',
            puesto_codigo='050010101',
            departamento_nombre='Antioquia',
            municipio_nombre='Medellín',
            zona_nombre='Zona 1',
            puesto_nombre='Puesto 1',
            nombre_completo='Puesto 1 - Zona 1 - Medellín - Antioquia',
            tipo='puesto'
        )
        db.session.add(puesto)
        db.session.flush()
        
        # Mesa
        mesa = Location(
            departamento_codigo='05',
            municipio_codigo='05001',
            zona_codigo='0500101',
            puesto_codigo='050010101',
            mesa_codigo='001',
            departamento_nombre='Antioquia',
            municipio_nombre='Medellín',
            zona_nombre='Zona 1',
            puesto_nombre='Puesto 1',
            nombre_completo='Mesa 001 - Puesto 1 - Zona 1 - Medellín - Antioquia',
            tipo='mesa',
            total_votantes_registrados=300
        )
        db.session.add(mesa)
        
        print("✅ Ubicaciones creadas")
        
        # 2. Crear usuarios básicos
        print("👥 Creando usuarios...")
        
        # Super Admin
        admin = User(
            username='admin',
            nombre='Administrador',
            email='admin@sistema.com',
            rol='super_admin',
            activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Testigo
        testigo = User(
            username='testigo1',
            nombre='Testigo 1',
            email='testigo1@sistema.com',
            rol='testigo_electoral',
            activo=True,
            departamento_codigo='05',
            municipio_codigo='05001',
            zona_codigo='0500101',
            puesto_codigo='050010101'
        )
        testigo.set_password('test123')
        db.session.add(testigo)
        
        print("✅ Usuarios creados")
        
        # 3. Crear tipos de elección
        print("🗳️  Creando tipos de elección...")
        
        tipos = [
            TipoEleccion(
                codigo='PRESIDENTE',
                nombre='Presidente',
                descripcion='Elección de Presidente de la República',
                es_uninominal=True,
                permite_lista_cerrada=False,
                permite_lista_abierta=False,
                permite_coaliciones=True,
                activo=True,
                orden=1
            ),
            TipoEleccion(
                codigo='ALCALDE',
                nombre='Alcaldía Municipal',
                descripcion='Elección de Alcalde Municipal',
                es_uninominal=True,
                permite_lista_cerrada=False,
                permite_lista_abierta=False,
                permite_coaliciones=True,
                activo=True,
                orden=2
            )
        ]
        
        for tipo in tipos:
            db.session.add(tipo)
        
        print("✅ Tipos de elección creados")
        
        # 4. Crear partidos
        print("🎨 Creando partidos...")
        
        partidos = [
            Partido(
                codigo='PL',
                nombre='Partido Liberal',
                nombre_corto='Liberal',
                color='#FF0000',
                activo=True,
                orden=1
            ),
            Partido(
                codigo='PC',
                nombre='Partido Conservador',
                nombre_corto='Conservador',
                color='#0000FF',
                activo=True,
                orden=2
            ),
            Partido(
                codigo='PV',
                nombre='Partido Verde',
                nombre_corto='Verde',
                color='#00FF00',
                activo=True,
                orden=3
            )
        ]
        
        for partido in partidos:
            db.session.add(partido)
        
        db.session.flush()
        
        print("✅ Partidos creados")
        
        # 5. Crear candidatos
        print("👤 Creando candidatos...")
        
        for i, partido in enumerate(partidos, 1):
            candidato = Candidato(
                codigo=f'CAND{i}',
                nombre_completo=f'Candidato {partido.nombre_corto}',
                partido_id=partido.id,
                tipo_eleccion_id=tipos[1].id,  # Alcaldía
                numero_lista=i,
                es_independiente=False,
                es_cabeza_lista=True,
                activo=True,
                orden=i
            )
            db.session.add(candidato)
        
        print("✅ Candidatos creados")
        
        # Commit final
        db.session.commit()
        
        print("\n✅ ¡Datos básicos cargados exitosamente!")
        print("\n🔑 Credenciales:")
        print("   Admin: admin / admin123")
        print("   Testigo: testigo1 / test123")
        
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
