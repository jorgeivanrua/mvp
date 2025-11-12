"""
Script para cargar datos de prueba en el MVP
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models.user import User
from app.models.location import Location
from app.models.form_e14 import FormE14, FormE14History
from app.models.enums import UserRole, LocationType, FormStatus

def load_sample_data():
    """Cargar datos de prueba"""
    print("📦 Cargando datos de prueba...")
    
    app = create_app('development')
    
    with app.app_context():
        # 1. Crear ubicaciones de prueba
        print("\n📍 Creando ubicaciones...")
        
        # Departamento Antioquia
        depto_antioquia = Location(
            departamento_codigo='05',
            nombre_completo='Antioquia',
            tipo=LocationType.DEPARTAMENTO,
            activo=True
        )
        depto_antioquia.save()
        
        # Municipio Medellín
        mun_medellin = Location(
            departamento_codigo='05',
            municipio_codigo='001',
            nombre_completo='Medellín',
            tipo=LocationType.MUNICIPIO,
            activo=True
        )
        mun_medellin.save()
        
        # Puesto de votación 1
        puesto_1 = Location(
            departamento_codigo='05',
            municipio_codigo='001',
            puesto_codigo='001',
            nombre_completo='Colegio San José',
            tipo=LocationType.PUESTO,
            activo=True
        )
        puesto_1.save()
        
        # Mesas del puesto 1
        mesas_puesto_1 = []
        for i in range(1, 4):
            mesa = Location(
                departamento_codigo='05',
                municipio_codigo='001',
                puesto_codigo='001',
                mesa_codigo=f'{i:03d}',
                nombre_completo=f'Mesa {i} - Colegio San José',
                tipo=LocationType.MESA,
                total_votantes_registrados=300,
                activo=True
            )
            mesa.save()
            mesas_puesto_1.append(mesa)
        
        # Departamento Cundinamarca
        depto_cundinamarca = Location(
            departamento_codigo='25',
            nombre_completo='Cundinamarca',
            tipo=LocationType.DEPARTAMENTO,
            activo=True
        )
        depto_cundinamarca.save()
        
        # Municipio Bogotá
        mun_bogota = Location(
            departamento_codigo='25',
            municipio_codigo='001',
            nombre_completo='Bogotá D.C.',
            tipo=LocationType.MUNICIPIO,
            activo=True
        )
        mun_bogota.save()
        
        # Puesto de votación 2
        puesto_2 = Location(
            departamento_codigo='25',
            municipio_codigo='001',
            puesto_codigo='001',
            nombre_completo='Universidad Nacional',
            tipo=LocationType.PUESTO,
            activo=True
        )
        puesto_2.save()
        
        # Mesas del puesto 2
        mesas_puesto_2 = []
        for i in range(1, 3):
            mesa = Location(
                departamento_codigo='25',
                municipio_codigo='001',
                puesto_codigo='001',
                mesa_codigo=f'{i:03d}',
                nombre_completo=f'Mesa {i} - Universidad Nacional',
                tipo=LocationType.MESA,
                total_votantes_registrados=350,
                activo=True
            )
            mesa.save()
            mesas_puesto_2.append(mesa)
        
        print(f"✅ Creadas {Location.query.count()} ubicaciones")
        
        # 2. Crear usuarios de prueba
        print("\n👥 Creando usuarios...")
        
        # Coordinador Puesto 1
        coord_puesto_1 = User(
            nombre="María García",
            email="coord.puesto1@sistema.com",
            rol=UserRole.COORDINADOR_PUESTO,
            ubicacion_id=puesto_1.id,
            activo=True
        )
        coord_puesto_1.set_password("Coord123!")
        coord_puesto_1.save()
        
        # Coordinador Puesto 2
        coord_puesto_2 = User(
            nombre="Carlos Rodríguez",
            email="coord.puesto2@sistema.com",
            rol=UserRole.COORDINADOR_PUESTO,
            ubicacion_id=puesto_2.id,
            activo=True
        )
        coord_puesto_2.set_password("Coord123!")
        coord_puesto_2.save()
        
        # Testigos para mesas del puesto 1
        testigos_puesto_1 = []
        for i, mesa in enumerate(mesas_puesto_1, 1):
            testigo = User(
                nombre=f"Testigo Mesa {i} - Puesto 1",
                email=f"testigo.p1m{i}@sistema.com",
                rol=UserRole.TESTIGO_ELECTORAL,
                ubicacion_id=mesa.id,
                activo=True
            )
            testigo.set_password("Testigo123!")
            testigo.save()
            testigos_puesto_1.append(testigo)
        
        # Testigos para mesas del puesto 2
        testigos_puesto_2 = []
        for i, mesa in enumerate(mesas_puesto_2, 1):
            testigo = User(
                nombre=f"Testigo Mesa {i} - Puesto 2",
                email=f"testigo.p2m{i}@sistema.com",
                rol=UserRole.TESTIGO_ELECTORAL,
                ubicacion_id=mesa.id,
                activo=True
            )
            testigo.set_password("Testigo123!")
            testigo.save()
            testigos_puesto_2.append(testigo)
        
        print(f"✅ Creados {User.query.count()} usuarios")
        
        # 3. Crear formularios E-14 de prueba
        print("\n📋 Creando formularios E-14 de prueba...")
        
        # Formulario 1: Borrador
        form1 = FormE14(
            mesa_id=mesas_puesto_1[0].id,
            testigo_id=testigos_puesto_1[0].id,
            total_votos=250,
            votos_partido_1=100,
            votos_partido_2=80,
            votos_partido_3=50,
            votos_nulos=15,
            votos_no_marcados=5,
            estado=FormStatus.BORRADOR,
            observaciones="Formulario en proceso de captura"
        )
        form1.save()
        
        # Formulario 2: Enviado
        form2 = FormE14(
            mesa_id=mesas_puesto_1[1].id,
            testigo_id=testigos_puesto_1[1].id,
            total_votos=280,
            votos_partido_1=120,
            votos_partido_2=90,
            votos_partido_3=50,
            votos_nulos=15,
            votos_no_marcados=5,
            estado=FormStatus.ENVIADO,
            foto_url="/uploads/e14/sample_form_2.jpg",
            observaciones="Formulario completo y enviado"
        )
        form2.save()
        
        # Formulario 3: Enviado
        form3 = FormE14(
            mesa_id=mesas_puesto_1[2].id,
            testigo_id=testigos_puesto_1[2].id,
            total_votos=290,
            votos_partido_1=130,
            votos_partido_2=85,
            votos_partido_3=55,
            votos_nulos=15,
            votos_no_marcados=5,
            estado=FormStatus.ENVIADO,
            foto_url="/uploads/e14/sample_form_3.jpg"
        )
        form3.save()
        
        # Formulario 4: Aprobado
        from datetime import datetime
        form4 = FormE14(
            mesa_id=mesas_puesto_2[0].id,
            testigo_id=testigos_puesto_2[0].id,
            total_votos=320,
            votos_partido_1=150,
            votos_partido_2=100,
            votos_partido_3=50,
            votos_nulos=15,
            votos_no_marcados=5,
            estado=FormStatus.APROBADO,
            foto_url="/uploads/e14/sample_form_4.jpg",
            aprobado_por=coord_puesto_2.id,
            aprobado_en=datetime.utcnow(),
            observaciones="Datos verificados y correctos"
        )
        form4.save()
        
        # Formulario 5: Rechazado
        form5 = FormE14(
            mesa_id=mesas_puesto_2[1].id,
            testigo_id=testigos_puesto_2[1].id,
            total_votos=300,
            votos_partido_1=140,
            votos_partido_2=90,
            votos_partido_3=50,
            votos_nulos=15,
            votos_no_marcados=5,
            estado=FormStatus.RECHAZADO,
            foto_url="/uploads/e14/sample_form_5.jpg",
            observaciones="Suma de votos no coincide con el total"
        )
        form5.save()
        
        print(f"✅ Creados {FormE14.query.count()} formularios E-14")
        
        # 4. Crear historial para los formularios
        print("\n📜 Creando historial...")
        
        for form in [form1, form2, form3, form4, form5]:
            history = FormE14History(
                form_id=form.id,
                usuario_id=form.testigo_id,
                accion='crear',
                estado_nuevo=form.estado.value,
                timestamp=form.created_at
            )
            history.save()
        
        print(f"✅ Creadas {FormE14History.query.count()} entradas de historial")
        
        # Resumen
        print("\n" + "="*60)
        print("✨ DATOS DE PRUEBA CARGADOS EXITOSAMENTE")
        print("="*60)
        
        print("\n📊 RESUMEN:")
        print(f"  • Departamentos: 2")
        print(f"  • Municipios: 2")
        print(f"  • Puestos: 2")
        print(f"  • Mesas: 5")
        print(f"  • Usuarios: {User.query.count()}")
        print(f"  • Formularios E-14: {FormE14.query.count()}")
        
        print("\n👤 USUARIOS DE PRUEBA:")
        print("\n  Superadmin:")
        print("    Email: admin@sistema.com")
        print("    Password: Admin123!")
        
        print("\n  Coordinadores:")
        print("    Email: coord.puesto1@sistema.com")
        print("    Password: Coord123!")
        print("    Email: coord.puesto2@sistema.com")
        print("    Password: Coord123!")
        
        print("\n  Testigos:")
        print("    Email: testigo.p1m1@sistema.com")
        print("    Password: Testigo123!")
        print("    (y más testigos con patrón similar)")
        
        print("\n📋 FORMULARIOS E-14:")
        print(f"  • Borrador: {FormE14.query.filter_by(estado=FormStatus.BORRADOR).count()}")
        print(f"  • Enviados: {FormE14.query.filter_by(estado=FormStatus.ENVIADO).count()}")
        print(f"  • Aprobados: {FormE14.query.filter_by(estado=FormStatus.APROBADO).count()}")
        print(f"  • Rechazados: {FormE14.query.filter_by(estado=FormStatus.RECHAZADO).count()}")
        
        print("\n🚀 LISTO PARA USAR:")
        print("  1. Ejecutar: python run.py")
        print("  2. Acceder a: http://localhost:5000")
        print("  3. Login con cualquiera de los usuarios de prueba")
        print("\n" + "="*60)

if __name__ == '__main__':
    load_sample_data()
