"""
Script para importar datos de Render a la base de datos local
Ejecutar DESPUÉS de haber exportado los datos de Render
"""
import json
from datetime import datetime, date
from backend.app import create_app
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.configuracion_electoral import Campana, TipoEleccion, Partido, Candidato

def import_data():
    """Importar datos desde JSON"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("IMPORTANDO DATOS DE RENDER A LOCAL")
        print("="*60)
        
        # Leer archivo JSON
        try:
            with open('render_data_export.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("\n❌ Error: No se encontró el archivo render_data_export.json")
            print("\nPasos para obtener el archivo:")
            print("1. Ir a Render Shell")
            print("2. Ejecutar: python export_data_from_render.py")
            print("3. Descargar el archivo render_data_export.json")
            print("4. Copiarlo a la raíz del proyecto")
            print("5. Ejecutar este script nuevamente")
            return
        
        # Confirmar antes de proceder
        print(f"\n📊 Datos a importar:")
        print(f"  - Ubicaciones: {len(data['locations'])}")
        print(f"  - Usuarios: {len(data['users'])}")
        print(f"  - Campañas: {len(data['campanas'])}")
        print(f"  - Tipos de elección: {len(data['tipos_eleccion'])}")
        print(f"  - Partidos: {len(data['partidos'])}")
        
        print(f"\n⚠️  ADVERTENCIA: Esto eliminará todos los datos actuales en la BD local")
        respuesta = input("\n¿Continuar? (si/no): ")
        
        if respuesta.lower() != 'si':
            print("\n❌ Importación cancelada")
            return
        
        # Limpiar base de datos
        print("\n🔄 Limpiando base de datos local...")
        db.drop_all()
        db.create_all()
        print("✓ Base de datos limpia")
        
        # Importar ubicaciones
        print("\n📍 Importando ubicaciones...")
        location_map = {}  # Para mapear ubicaciones a IDs
        for loc_data in data['locations']:
            loc = Location(
                departamento_codigo=loc_data['departamento_codigo'],
                municipio_codigo=loc_data['municipio_codigo'],
                zona_codigo=loc_data['zona_codigo'],
                puesto_codigo=loc_data['puesto_codigo'],
                mesa_codigo=loc_data['mesa_codigo'],
                departamento_nombre=loc_data['departamento_nombre'],
                municipio_nombre=loc_data['municipio_nombre'],
                puesto_nombre=loc_data['puesto_nombre'],
                mesa_nombre=loc_data['mesa_nombre'],
                nombre_completo=loc_data['nombre_completo'],
                tipo=loc_data['tipo'],
                total_votantes_registrados=loc_data['total_votantes_registrados'],
                mujeres=loc_data['mujeres'],
                hombres=loc_data['hombres'],
                comuna=loc_data['comuna'],
                direccion=loc_data['direccion'],
                latitud=loc_data['latitud'],
                longitud=loc_data['longitud'],
                activo=loc_data['activo']
            )
            db.session.add(loc)
            db.session.flush()
            
            # Guardar mapeo
            key = f"{loc_data['departamento_codigo']}_{loc_data['municipio_codigo']}_{loc_data['zona_codigo']}_{loc_data['puesto_codigo']}_{loc_data['mesa_codigo']}_{loc_data['tipo']}"
            location_map[key] = loc.id
        
        db.session.commit()
        print(f"✓ {len(data['locations'])} ubicaciones importadas")
        
        # Importar usuarios
        print("\n👥 Importando usuarios...")
        for user_data in data['users']:
            # Buscar ubicación
            ubicacion_id = None
            if user_data['ubicacion_info']:
                info = user_data['ubicacion_info']
                key = f"{info['departamento_codigo']}_{info['municipio_codigo']}_{info['zona_codigo']}_{info['puesto_codigo']}_{info['mesa_codigo']}_{info['tipo']}"
                ubicacion_id = location_map.get(key)
            
            user = User(
                nombre=user_data['nombre'],
                rol=user_data['rol'],
                ubicacion_id=ubicacion_id,
                activo=user_data['activo']
            )
            # Establecer contraseña por defecto: test123
            user.set_password('test123')
            db.session.add(user)
        
        db.session.commit()
        print(f"✓ {len(data['users'])} usuarios importados (contraseña: test123)")
        
        # Importar campañas
        print("\n📅 Importando campañas...")
        for campana_data in data['campanas']:
            campana = Campana(
                codigo=campana_data['codigo'],
                nombre=campana_data['nombre'],
                descripcion=campana_data['descripcion'],
                fecha_inicio=datetime.fromisoformat(campana_data['fecha_inicio']).date() if campana_data['fecha_inicio'] else None,
                fecha_fin=datetime.fromisoformat(campana_data['fecha_fin']).date() if campana_data['fecha_fin'] else None,
                color_primario=campana_data['color_primario'],
                color_secundario=campana_data['color_secundario'],
                es_partido_completo=campana_data['es_partido_completo'],
                activa=campana_data['activa']
            )
            db.session.add(campana)
        
        db.session.commit()
        print(f"✓ {len(data['campanas'])} campañas importadas")
        
        # Importar tipos de elección
        print("\n🗳️  Importando tipos de elección...")
        for tipo_data in data['tipos_eleccion']:
            tipo = TipoEleccion(
                codigo=tipo_data['codigo'],
                nombre=tipo_data['nombre'],
                es_uninominal=tipo_data['es_uninominal'],
                permite_lista_cerrada=tipo_data['permite_lista_cerrada'],
                permite_lista_abierta=tipo_data['permite_lista_abierta'],
                permite_voto_preferente=tipo_data['permite_voto_preferente'],
                activo=tipo_data['activo']
            )
            db.session.add(tipo)
        
        db.session.commit()
        print(f"✓ {len(data['tipos_eleccion'])} tipos de elección importados")
        
        # Importar partidos
        print("\n🏛️  Importando partidos...")
        for partido_data in data['partidos']:
            partido = Partido(
                codigo=partido_data['codigo'],
                nombre=partido_data['nombre'],
                nombre_corto=partido_data['nombre_corto'],
                color=partido_data['color'],
                activo=partido_data['activo']
            )
            db.session.add(partido)
        
        db.session.commit()
        print(f"✓ {len(data['partidos'])} partidos importados")
        
        print("\n" + "="*60)
        print("✅ IMPORTACIÓN COMPLETADA")
        print("="*60)
        print("\n🎉 Tu base de datos local ahora tiene los mismos datos que Render")
        print("\n🔑 Todos los usuarios tienen la contraseña: test123")
        print("\n💡 Puedes verificar los datos en:")
        print("   http://localhost:5000/auth/login")
        print("\n📊 Resumen:")
        print(f"  - Ubicaciones: {len(data['locations'])}")
        print(f"  - Usuarios: {len(data['users'])}")
        print(f"  - Campañas: {len(data['campanas'])}")
        print(f"  - Tipos de elección: {len(data['tipos_eleccion'])}")
        print(f"  - Partidos: {len(data['partidos'])}")
        print()

if __name__ == '__main__':
    import_data()
