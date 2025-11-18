"""
Script para exportar datos de Render a formato JSON
Ejecutar este script EN RENDER SHELL
"""
import json
from backend.app import create_app
from backend.models.location import Location
from backend.models.user import User
from backend.models.configuracion_electoral import Campana, TipoEleccion, Partido, Candidato

def export_data():
    """Exportar todos los datos a JSON"""
    app = create_app()
    
    with app.app_context():
        print("Exportando datos de Render...")
        
        data = {
            'locations': [],
            'users': [],
            'campanas': [],
            'tipos_eleccion': [],
            'partidos': [],
            'candidatos': []
        }
        
        # Exportar ubicaciones
        print("Exportando ubicaciones...")
        locations = Location.query.all()
        for loc in locations:
            data['locations'].append({
                'departamento_codigo': loc.departamento_codigo,
                'municipio_codigo': loc.municipio_codigo,
                'zona_codigo': loc.zona_codigo,
                'puesto_codigo': loc.puesto_codigo,
                'mesa_codigo': loc.mesa_codigo,
                'departamento_nombre': loc.departamento_nombre,
                'municipio_nombre': loc.municipio_nombre,
                'puesto_nombre': loc.puesto_nombre,
                'mesa_nombre': loc.mesa_nombre,
                'nombre_completo': loc.nombre_completo,
                'tipo': loc.tipo,
                'total_votantes_registrados': loc.total_votantes_registrados,
                'mujeres': loc.mujeres,
                'hombres': loc.hombres,
                'comuna': loc.comuna,
                'direccion': loc.direccion,
                'latitud': loc.latitud,
                'longitud': loc.longitud,
                'activo': loc.activo
            })
        print(f"✓ {len(data['locations'])} ubicaciones exportadas")
        
        # Exportar usuarios (sin contraseñas por seguridad)
        print("Exportando usuarios...")
        users = User.query.all()
        for user in users:
            # Buscar ubicación
            ubicacion_info = None
            if user.ubicacion_id:
                loc = Location.query.get(user.ubicacion_id)
                if loc:
                    ubicacion_info = {
                        'departamento_codigo': loc.departamento_codigo,
                        'municipio_codigo': loc.municipio_codigo,
                        'zona_codigo': loc.zona_codigo,
                        'puesto_codigo': loc.puesto_codigo,
                        'mesa_codigo': loc.mesa_codigo,
                        'tipo': loc.tipo
                    }
            
            data['users'].append({
                'nombre': user.nombre,
                'rol': user.rol,
                'ubicacion_info': ubicacion_info,
                'activo': user.activo
            })
        print(f"✓ {len(data['users'])} usuarios exportados")
        
        # Exportar campañas
        print("Exportando campañas...")
        campanas = Campana.query.all()
        for campana in campanas:
            data['campanas'].append({
                'codigo': campana.codigo,
                'nombre': campana.nombre,
                'descripcion': campana.descripcion,
                'fecha_inicio': campana.fecha_inicio.isoformat() if campana.fecha_inicio else None,
                'fecha_fin': campana.fecha_fin.isoformat() if campana.fecha_fin else None,
                'color_primario': campana.color_primario,
                'color_secundario': campana.color_secundario,
                'es_partido_completo': campana.es_partido_completo,
                'activa': campana.activa
            })
        print(f"✓ {len(data['campanas'])} campañas exportadas")
        
        # Exportar tipos de elección
        print("Exportando tipos de elección...")
        tipos = TipoEleccion.query.all()
        for tipo in tipos:
            data['tipos_eleccion'].append({
                'codigo': tipo.codigo,
                'nombre': tipo.nombre,
                'es_uninominal': tipo.es_uninominal,
                'permite_lista_cerrada': tipo.permite_lista_cerrada,
                'permite_lista_abierta': tipo.permite_lista_abierta,
                'permite_voto_preferente': tipo.permite_voto_preferente,
                'activo': tipo.activo
            })
        print(f"✓ {len(data['tipos_eleccion'])} tipos de elección exportados")
        
        # Exportar partidos
        print("Exportando partidos...")
        partidos = Partido.query.all()
        for partido in partidos:
            data['partidos'].append({
                'codigo': partido.codigo,
                'nombre': partido.nombre,
                'nombre_corto': partido.nombre_corto,
                'color': partido.color,
                'activo': partido.activo
            })
        print(f"✓ {len(data['partidos'])} partidos exportados")
        
        # Guardar a archivo JSON
        with open('render_data_export.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*60)
        print("✅ EXPORTACIÓN COMPLETADA")
        print("="*60)
        print(f"\nArchivo generado: render_data_export.json")
        print(f"\nResumen:")
        print(f"  - Ubicaciones: {len(data['locations'])}")
        print(f"  - Usuarios: {len(data['users'])}")
        print(f"  - Campañas: {len(data['campanas'])}")
        print(f"  - Tipos de elección: {len(data['tipos_eleccion'])}")
        print(f"  - Partidos: {len(data['partidos'])}")
        print(f"\nPróximo paso:")
        print("  1. Descargar el archivo render_data_export.json")
        print("  2. Copiarlo a tu proyecto local")
        print("  3. Ejecutar: python import_data_to_local.py")

if __name__ == '__main__':
    export_data()
