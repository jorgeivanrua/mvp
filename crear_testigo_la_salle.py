"""
Crear testigo electoral para I.E. JUAN BAUTISTA LA SALLE
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from werkzeug.security import generate_password_hash

def crear_testigo_la_salle():
    """Crear testigo para el puesto La Salle"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("CREAR TESTIGO ELECTORAL - I.E. JUAN BAUTISTA LA SALLE")
        print("="*70)
        
        # Buscar el puesto La Salle
        puesto = Location.query.filter(
            Location.tipo == 'puesto',
            Location.nombre_completo.like('%JUAN BAUTISTA LA SALLE%')
        ).first()
        
        if not puesto:
            print("❌ No se encontró el puesto I.E. JUAN BAUTISTA LA SALLE")
            print("\nBuscando puestos disponibles en Florencia...")
            
            puestos = Location.query.filter_by(
                tipo='puesto',
                municipio_codigo='001',
                departamento_codigo='18'
            ).all()
            
            print(f"\n📍 Puestos encontrados: {len(puestos)}")
            for p in puestos:
                print(f"  - ID: {p.id} | {p.nombre_completo}")
            return
        
        print(f"\n✅ Puesto encontrado:")
        print(f"  ID: {puesto.id}")
        print(f"  Nombre: {puesto.nombre_completo}")
        print(f"  Código: {puesto.puesto_codigo}")
        print(f"  Departamento: {puesto.departamento_codigo}")
        print(f"  Municipio: {puesto.municipio_codigo}")
        print(f"  Zona: {puesto.zona_codigo}")
        
        # Buscar mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo
        ).all()
        
        print(f"\n📋 Mesas del puesto: {len(mesas)}")
        
        if not mesas:
            print("❌ No hay mesas en este puesto")
            return
        
        # Mostrar mesas disponibles
        print("\nMesas disponibles:")
        for mesa in mesas:
            # Verificar si ya tiene testigo
            testigo_existente = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral'
            ).first()
            
            estado = "❌ Ya tiene testigo" if testigo_existente else "✅ Disponible"
            print(f"  Mesa {mesa.mesa_codigo}: {mesa.nombre_completo} - {estado}")
        
        # Buscar primera mesa sin testigo
        mesa_sin_testigo = None
        for mesa in mesas:
            testigo_existente = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral'
            ).first()
            if not testigo_existente:
                mesa_sin_testigo = mesa
                break
        
        if not mesa_sin_testigo:
            print("\n⚠️  Todas las mesas ya tienen testigo asignado")
            print("\n¿Deseas crear un testigo adicional? (se asignará a la primera mesa)")
            mesa_sin_testigo = mesas[0]
        
        print(f"\n📍 Mesa seleccionada:")
        print(f"  ID: {mesa_sin_testigo.id}")
        print(f"  Código: {mesa_sin_testigo.mesa_codigo}")
        print(f"  Nombre: {mesa_sin_testigo.nombre_completo}")
        
        # Generar username único
        base_username = f"testigo_lasalle_{mesa_sin_testigo.mesa_codigo}"
        username = base_username
        contador = 1
        
        while User.query.filter_by(username=username).first():
            username = f"{base_username}_{contador}"
            contador += 1
        
        # Crear testigo
        testigo = User(
            username=username,
            password_hash=generate_password_hash('test123'),
            nombre=f"Testigo La Salle Mesa {mesa_sin_testigo.mesa_codigo}",
            email=f"{username}@electoral.com",
            rol='testigo_electoral',
            ubicacion_id=mesa_sin_testigo.id,
            activo=True,
            presencia_verificada=False
        )
        
        db.session.add(testigo)
        db.session.commit()
        
        print(f"\n✅ Testigo creado exitosamente!")
        print(f"\n📋 CREDENCIALES:")
        print(f"  Username: {testigo.username}")
        print(f"  Password: test123")
        print(f"  Nombre: {testigo.nombre}")
        print(f"  Rol: {testigo.rol}")
        print(f"  Mesa ID: {testigo.ubicacion_id}")
        print(f"  Mesa: {mesa_sin_testigo.nombre_completo}")
        
        print("\n" + "="*70)
        print("✅ TESTIGO LISTO PARA USAR")
        print("="*70)
        print("\nPuedes iniciar sesión con:")
        print(f"  Usuario: {testigo.username}")
        print(f"  Contraseña: test123")
        print("\n" + "="*70)

if __name__ == '__main__':
    crear_testigo_la_salle()
