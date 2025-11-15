"""
Script automático para sincronizar datos de Render a Local
"""
import requests
import json
from datetime import datetime
from backend.app import create_app
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.configuracion_electoral import Campana, TipoEleccion, Partido

# Configuración
RENDER_URL = "https://mvp-b9uv.onrender.com"
ADMIN_KEY = "temp_admin_key_2024"

def download_data():
    """Descargar datos de Render"""
    print("\n🌐 Descargando datos de Render...")
    
    try:
        url = f"{RENDER_URL}/api/admin-tools/export-data"
        params = {'admin_key': ADMIN_KEY}
        
        response = requests.get(url, params=params, timeout=120)
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Detalle: {error_data.get('error', 'Sin detalles')}")
            except:
                print(f"   Respuesta: {response.text[:200]}")
            return None
        
        data = response.json()
        
        if not data.get('success'):
            print(f"❌ Error: {data.get('error')}")
            return None
        
        print("✅ Datos descargados")
        summary = data.get('summary', {})
        print(f"   Ubicaciones: {summary.get('locations', 0)}")
        print(f"   Usuarios: {summary.get('users', 0)}")
        
        return data['data']
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def import_data(data):
    """Importar datos a local"""
    app = create_app()
    
    with app.app_context():
        print("\n🔄 Importando datos...")
        
        try:
            # Limpiar BD
            print("   Limpiando BD...")
            db.drop_all()
            db.create_all()
            
            # Importar ubicaciones
            print(f"   Importando {len(data['locations'])} ubicaciones...")
            location_map = {}
            
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
                
                key = f"{loc_data['departamento_codigo']}_{loc_data['municipio_codigo']}_{loc_data['zona_codigo']}_{loc_data['puesto_codigo']}_{loc_data['mesa_codigo']}_{loc_data['tipo']}"
                location_map[key] = loc.id
            
            db.session.commit()
            print(f"   ✓ {len(data['locations'])} ubicaciones")
            
            # Importar usuarios
            print(f"   Importando {len(data['users'])} usuarios...")
            for user_data in data['users']:
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
                user.set_password('test123')
                db.session.add(user)
            
            db.session.commit()
            print(f"   ✓ {len(data['users'])} usuarios")
            
            # Importar campañas
            print(f"   Importando {len(data['campanas'])} campañas...")
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
            print(f"   ✓ {len(data['campanas'])} campañas")
            
            # Importar tipos de elección
            print(f"   Importando {len(data['tipos_eleccion'])} tipos de elección...")
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
            print(f"   ✓ {len(data['tipos_eleccion'])} tipos")
            
            # Importar partidos
            print(f"   Importando {len(data['partidos'])} partidos...")
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
            print(f"   ✓ {len(data['partidos'])} partidos")
            
            print("\n✅ SINCRONIZACIÓN COMPLETADA")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("="*60)
    print("SINCRONIZACIÓN AUTOMÁTICA RENDER → LOCAL")
    print("="*60)
    
    data = download_data()
    if data:
        import_data(data)
