"""
Crear testigo para I.E. JUAN BAUTISTA LA SALLE
"""
import sys
sys.path.insert(0, '.')

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from werkzeug.security import generate_password_hash

def crear_testigo():
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*70)
        print("CREAR TESTIGO - I.E. JUAN BAUTISTA LA SALLE")
        print("="*70)
        
        # Buscar el puesto por ID
        puesto = Location.query.get(457)
        
        if not puesto:
            print("❌ No se encontró el puesto")
            return
        
        print(f"\n✅ Puesto encontrado:")
        print(f"  ID: {puesto.id}")
        print(f"  Nombre: {puesto.nombre_completo}")
        
        # Buscar mesas
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo
        ).all()
        
        print(f"\n📋 Mesas del puesto: {len(mesas)}")
        
        # Mostrar mesas y verificar testigos
        for mesa in mesas:
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral'
            ).first()
            
            estado = f"❌ Ya tiene testigo ({testigo.nombre})" if testigo else "✅ Disponible"
            print(f"  Mesa {mesa.mesa_codigo}: {estado}")
        
        # Buscar primera mesa sin testigo
        mesa_seleccionada = None
        for mesa in mesas:
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral'
            ).first()
            if not testigo:
                mesa_seleccionada = mesa
                break
        
        if not mesa_seleccionada:
            print("\n⚠️  Todas las mesas ya tienen testigo. Creando testigo adicional en mesa 1...")
            mesa_seleccionada = mesas[0]
        
        print(f"\n📍 Mesa seleccionada:")
        print(f"  ID: {mesa_seleccionada.id}")
        print(f"  Código: {mesa_seleccionada.mesa_codigo}")
        print(f"  Nombre: {mesa_seleccionada.nombre_completo}")
        print(f"  Votantes: {mesa_seleccionada.total_votantes_registrados}")
        
        # Generar nombre único
        base_nombre = f"Testigo La Salle Mesa {mesa_seleccionada.mesa_codigo}"
        nombre = base_nombre
        contador = 1
        
        while User.query.filter_by(nombre=nombre).first():
            nombre = f"{base_nombre} ({contador})"
            contador += 1
        
        # Crear testigo
        testigo = User(
            nombre=nombre,
            rol='testigo_electoral',
            ubicacion_id=mesa_seleccionada.id,
            activo=True,
            presencia_verificada=False
        )
        testigo.set_password('test123')
        
        db.session.add(testigo)
        db.session.commit()
        
        print("\n" + "="*70)
        print("✅ TESTIGO CREADO EXITOSAMENTE")
        print("="*70)
        
        print(f"\n📋 CREDENCIALES DE ACCESO:")
        print(f"  Nombre: {testigo.nombre}")
        print(f"  Contraseña: test123")
        print(f"  Rol: Testigo Electoral")
        
        print(f"\n📍 UBICACIÓN:")
        print(f"  Departamento: CAQUETÁ (código 18)")
        print(f"  Municipio: FLORENCIA (código 01)")
        print(f"  Zona: 01")
        print(f"  Puesto: I.E. JUAN BAUTISTA LA SALLE")
        print(f"  Mesa: {mesa_seleccionada.nombre_completo}")
        
        print("\n" + "="*70)
        print("🎯 LISTO PARA INICIAR SESIÓN")
        print("="*70)
        print("\nEn la pantalla de login, selecciona:")
        print(f"  Rol: Testigo Electoral")
        print(f"  Departamento: CAQUETA")
        print(f"  Municipio: FLORENCIA")
        print(f"  Zona: CAQUETA - FLORENCIA - Zona 01")
        print(f"  Puesto Electoral: I.E. JUAN BAUTISTA LA SALLE")
        print(f"  Contraseña: test123")
        print("\n" + "="*70)

if __name__ == '__main__':
    crear_testigo()
