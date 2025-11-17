"""
Crear testigo electoral de forma interactiva
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
        print("CREAR TESTIGO ELECTORAL")
        print("="*70)
        
        # Datos del formulario de la imagen
        departamento = "CAQUETA"
        municipio = "FLORENCIA"
        zona_nombre = "CAQUETA - FLORENCIA - Zona 01"
        puesto_nombre = "I.E. JUAN BAUTISTA LA SALLE"
        
        print(f"\nBuscando ubicación:")
        print(f"  Departamento: {departamento}")
        print(f"  Municipio: {municipio}")
        print(f"  Puesto: {puesto_nombre}")
        
        # Buscar el puesto
        puesto = Location.query.filter(
            Location.tipo == 'puesto',
            Location.departamento_codigo == '18',  # Caquetá
            Location.municipio_codigo == '001',     # Florencia
            Location.nombre_completo.like(f'%{puesto_nombre}%')
        ).first()
        
        if not puesto:
            print(f"\n❌ No se encontró el puesto '{puesto_nombre}'")
            print("\nBuscando puestos similares...")
            
            puestos = Location.query.filter(
                Location.tipo == 'puesto',
                Location.departamento_codigo == '18',
                Location.municipio_codigo == '001'
            ).all()
            
            print(f"\n📍 Puestos disponibles en Florencia ({len(puestos)}):")
            for i, p in enumerate(puestos, 1):
                mesas_count = Location.query.filter_by(
                    tipo='mesa',
                    puesto_codigo=p.puesto_codigo,
                    departamento_codigo=p.departamento_codigo,
                    municipio_codigo=p.municipio_codigo,
                    zona_codigo=p.zona_codigo
                ).count()
                print(f"  {i}. ID: {p.id:3d} | {p.nombre_completo} ({mesas_count} mesas)")
            
            if not puestos:
                print("\n❌ No hay puestos en Florencia")
                return
            
            # Seleccionar el primer puesto como ejemplo
            print(f"\n⚠️  Usando el primer puesto como ejemplo")
            puesto = puestos[0]
        
        print(f"\n✅ Puesto seleccionado:")
        print(f"  ID: {puesto.id}")
        print(f"  Nombre: {puesto.nombre_completo}")
        print(f"  Código: {puesto.puesto_codigo}")
        
        # Buscar mesas del puesto
        mesas = Location.query.filter_by(
            tipo='mesa',
            departamento_codigo=puesto.departamento_codigo,
            municipio_codigo=puesto.municipio_codigo,
            zona_codigo=puesto.zona_codigo,
            puesto_codigo=puesto.puesto_codigo
        ).order_by(Location.mesa_codigo).all()
        
        print(f"\n📋 Mesas del puesto: {len(mesas)}")
        
        if not mesas:
            print("❌ No hay mesas en este puesto")
            return
        
        # Mostrar mesas y sus testigos
        mesas_disponibles = []
        for mesa in mesas:
            testigo = User.query.filter_by(
                ubicacion_id=mesa.id,
                rol='testigo_electoral'
            ).first()
            
            if testigo:
                print(f"  Mesa {mesa.mesa_codigo}: ❌ Ya tiene testigo ({testigo.username})")
            else:
                print(f"  Mesa {mesa.mesa_codigo}: ✅ Disponible")
                mesas_disponibles.append(mesa)
        
        if not mesas_disponibles:
            print("\n⚠️  Todas las mesas ya tienen testigo")
            print("Creando testigo adicional en la primera mesa...")
            mesa_seleccionada = mesas[0]
        else:
            mesa_seleccionada = mesas_disponibles[0]
        
        print(f"\n📍 Mesa seleccionada:")
        print(f"  ID: {mesa_seleccionada.id}")
        print(f"  Código: {mesa_seleccionada.mesa_codigo}")
        print(f"  Nombre: {mesa_seleccionada.nombre_completo}")
        
        # Generar username único
        base_username = f"testigo_{puesto.puesto_codigo}_{mesa_seleccionada.mesa_codigo}"
        username = base_username
        contador = 1
        
        while User.query.filter_by(username=username).first():
            username = f"{base_username}_{contador}"
            contador += 1
        
        # Crear testigo
        nombre_testigo = f"Testigo Mesa {mesa_seleccionada.mesa_codigo} - {puesto.nombre_completo[:30]}"
        
        testigo = User(
            username=username,
            password_hash=generate_password_hash('test123'),
            nombre=nombre_testigo,
            email=f"{username}@electoral.com",
            rol='testigo_electoral',
            ubicacion_id=mesa_seleccionada.id,
            activo=True,
            presencia_verificada=False
        )
        
        db.session.add(testigo)
        db.session.commit()
        
        print("\n" + "="*70)
        print("✅ TESTIGO CREADO EXITOSAMENTE")
        print("="*70)
        
        print(f"\n📋 CREDENCIALES DE ACCESO:")
        print(f"  Usuario: {testigo.username}")
        print(f"  Contraseña: test123")
        print(f"  Nombre: {testigo.nombre}")
        print(f"  Rol: Testigo Electoral")
        
        print(f"\n📍 UBICACIÓN:")
        print(f"  Departamento: {puesto.departamento_codigo} - CAQUETÁ")
        print(f"  Municipio: {puesto.municipio_codigo} - FLORENCIA")
        print(f"  Zona: {puesto.zona_codigo}")
        print(f"  Puesto: {puesto.nombre_completo}")
        print(f"  Mesa: {mesa_seleccionada.nombre_completo}")
        
        print("\n" + "="*70)
        print("🎯 LISTO PARA INICIAR SESIÓN")
        print("="*70)
        print("\nEn la pantalla de login, selecciona:")
        print(f"  Rol: Testigo Electoral")
        print(f"  Departamento: CAQUETA")
        print(f"  Municipio: FLORENCIA")
        print(f"  Zona: CAQUETA - FLORENCIA - Zona 01")
        print(f"  Puesto Electoral: {puesto.nombre_completo}")
        print(f"  Contraseña: test123")
        print("\n" + "="*70)

if __name__ == '__main__':
    crear_testigo()
