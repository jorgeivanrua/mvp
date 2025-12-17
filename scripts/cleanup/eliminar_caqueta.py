#!/usr/bin/env python3
"""
Script para eliminar todos los datos del departamento del Caquetá
Mantiene solo el Quindío como departamento principal
"""
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app import create_app
from backend.database import db
from backend.models.location import Location
from backend.models.user import User
from backend.models.departamento_config import DepartamentoConfig
from backend.models.formulario_e14 import FormularioE14
from backend.models.reporte_participacion import ReporteParticipacion
from backend.models.incidentes_delitos import IncidenteElectoral
from backend.models.incidentes_delitos_fotos import IncidenteDelitoFoto

def eliminar_datos_caqueta():
    """Eliminar todos los datos relacionados con el departamento del Caquetá"""
    
    print("🗑️ ELIMINANDO DATOS DEL CAQUETÁ")
    print("=" * 50)
    
    # Código del Caquetá
    CAQUETA_CODIGO = '44'
    
    try:
        # 1. Obtener todas las ubicaciones del Caquetá
        print(f"📍 Buscando ubicaciones del Caquetá (código: {CAQUETA_CODIGO})...")
        ubicaciones_caqueta = Location.query.filter_by(
            departamento_codigo=CAQUETA_CODIGO
        ).all()
        
        ubicaciones_ids = [loc.id for loc in ubicaciones_caqueta]
        print(f"   Encontradas {len(ubicaciones_caqueta)} ubicaciones")
        
        if not ubicaciones_caqueta:
            print("   ✅ No se encontraron ubicaciones del Caquetá")
            return
        
        # 2. Eliminar usuarios del Caquetá
        print(f"👥 Eliminando usuarios del Caquetá...")
        usuarios_caqueta = User.query.filter(
            User.ubicacion_id.in_(ubicaciones_ids)
        ).all()
        
        print(f"   Encontrados {len(usuarios_caqueta)} usuarios:")
        for usuario in usuarios_caqueta:
            print(f"   - {usuario.nombre} ({usuario.rol})")
        
        # Eliminar datos electorales de usuarios del Caquetá
        usuarios_ids = [u.id for u in usuarios_caqueta]
        
        if usuarios_ids:
            # 3. Eliminar formularios E-14
            print(f"📋 Eliminando formularios E-14...")
            formularios = FormularioE14.query.filter(
                FormularioE14.testigo_id.in_(usuarios_ids)
            ).all()
            print(f"   Encontrados {len(formularios)} formularios")
            
            # Eliminar formularios directamente (las relaciones se eliminarán en cascada)
            for formulario in formularios:
                db.session.delete(formulario)
            
            # 4. Eliminar reportes de participación
            print(f"📊 Eliminando reportes de participación...")
            reportes = ReporteParticipacion.query.filter(
                ReporteParticipacion.testigo_id.in_(usuarios_ids)
            ).all()
            print(f"   Encontrados {len(reportes)} reportes")
            for reporte in reportes:
                db.session.delete(reporte)
            
            # 5. Eliminar incidentes electorales y sus datos relacionados
            print(f"⚠️ Eliminando incidentes electorales...")
            incidentes = IncidenteElectoral.query.filter(
                IncidenteElectoral.reportado_por_id.in_(usuarios_ids)
            ).all()
            print(f"   Encontrados {len(incidentes)} incidentes")
            
            incidentes_ids = [i.id for i in incidentes]
            
            if incidentes_ids:
                # 5.1. Eliminar fotos de incidentes
                print(f"📸 Eliminando fotos de incidentes...")
                fotos_incidentes = IncidenteDelitoFoto.query.filter(
                    IncidenteDelitoFoto.incidente_id.in_(incidentes_ids)
                ).all()
                print(f"   Encontradas {len(fotos_incidentes)} fotos de incidentes")
                for foto in fotos_incidentes:
                    db.session.delete(foto)
                
                # 5.2. Eliminar seguimiento de incidentes (usando SQL directo)
                print(f"📋 Eliminando seguimiento de incidentes...")
                try:
                    result = db.session.execute(
                        "DELETE FROM seguimiento_reportes WHERE tipo_reporte = 'incidente' AND reporte_id IN ({})".format(
                            ','.join(map(str, incidentes_ids))
                        )
                    )
                    print(f"   Eliminados {result.rowcount} registros de seguimiento de incidentes")
                except Exception as e:
                    print(f"   ⚠️ Error eliminando seguimiento de incidentes: {str(e)}")
                    print(f"   Continuando sin eliminar seguimiento de incidentes...")
            
            # 5.3. Eliminar incidentes
            for incidente in incidentes:
                db.session.delete(incidente)
            
            # 6. Eliminar fotos subidas por usuarios del Caquetá (independientemente del incidente)
            print(f"📸 Eliminando fotos subidas por usuarios del Caquetá...")
            fotos_usuarios = IncidenteDelitoFoto.query.filter(
                IncidenteDelitoFoto.subida_por_id.in_(usuarios_ids)
            ).all()
            print(f"   Encontradas {len(fotos_usuarios)} fotos subidas por usuarios del Caquetá")
            for foto in fotos_usuarios:
                db.session.delete(foto)
            
            # 7. Eliminar seguimiento de acciones de usuarios del Caquetá (usando SQL directo)
            print(f"📋 Eliminando seguimiento de acciones de usuarios del Caquetá...")
            try:
                result = db.session.execute(
                    "DELETE FROM seguimiento_reportes WHERE usuario_id IN ({})".format(
                        ','.join(map(str, usuarios_ids))
                    )
                )
                print(f"   Eliminados {result.rowcount} registros de seguimiento de usuarios")
            except Exception as e:
                print(f"   ⚠️ Error eliminando seguimiento: {str(e)}")
                print(f"   Continuando sin eliminar seguimiento...")
        
        # 8. Eliminar usuarios
        print(f"👥 Eliminando usuarios...")
        for usuario in usuarios_caqueta:
            db.session.delete(usuario)
        
        # 9. Eliminar ubicaciones del Caquetá
        print(f"📍 Eliminando ubicaciones...")
        for ubicacion in ubicaciones_caqueta:
            print(f"   - {ubicacion.tipo}: {ubicacion.nombre_completo}")
            db.session.delete(ubicacion)
        
        # 10. Eliminar configuración del departamento del Caquetá
        print(f"⚙️ Eliminando configuración del departamento...")
        config_caqueta = DepartamentoConfig.query.filter_by(
            departamento_codigo=CAQUETA_CODIGO
        ).first()
        
        if config_caqueta:
            print(f"   Eliminando configuración: {config_caqueta.departamento_nombre}")
            db.session.delete(config_caqueta)
        else:
            print("   No se encontró configuración del Caquetá")
        
        # 11. Confirmar que el Quindío sigue como principal
        print(f"⭐ Verificando departamento principal...")
        quindio_config = DepartamentoConfig.query.filter_by(
            departamento_codigo='26',
            es_principal=True,
            habilitado=True
        ).first()
        
        if quindio_config:
            print(f"   ✅ {quindio_config.departamento_nombre} sigue como principal")
            # Actualizar estadísticas
            quindio_config.actualizar_estadisticas()
        else:
            print("   ⚠️ Advertencia: No se encontró el Quindío como principal")
        
        # Commit de todos los cambios
        db.session.commit()
        
        print("\n" + "=" * 50)
        print("✅ ELIMINACIÓN COMPLETADA")
        print("=" * 50)
        
        # Mostrar estadísticas finales
        print(f"📊 ESTADÍSTICAS FINALES:")
        
        # Contar ubicaciones restantes
        total_ubicaciones = Location.query.filter_by(activo=True).count()
        ubicaciones_quindio = Location.query.filter_by(
            departamento_codigo='26',
            activo=True
        ).count()
        
        print(f"   Ubicaciones totales: {total_ubicaciones}")
        print(f"   Ubicaciones Quindío: {ubicaciones_quindio}")
        
        # Contar usuarios restantes
        total_usuarios = User.query.filter_by(activo=True).count()
        usuarios_quindio = User.query.join(Location).filter(
            Location.departamento_codigo == '26',
            User.activo == True
        ).count()
        
        print(f"   Usuarios totales: {total_usuarios}")
        print(f"   Usuarios Quindío: {usuarios_quindio}")
        
        # Verificar departamentos configurados
        departamentos_config = DepartamentoConfig.query.filter_by(habilitado=True).all()
        print(f"   Departamentos habilitados: {len(departamentos_config)}")
        for config in departamentos_config:
            print(f"   - {config.departamento_nombre} ({'Principal' if config.es_principal else 'Secundario'})")
        
        print(f"\n🎯 RESULTADO: Solo queda el Quindío como departamento principal")
        
    except Exception as e:
        print(f"❌ Error durante la eliminación: {str(e)}")
        db.session.rollback()
        raise

def main():
    """Función principal"""
    app = create_app()
    
    with app.app_context():
        print("🗑️ SCRIPT DE ELIMINACIÓN DEL CAQUETÁ")
        print("=" * 50)
        print("Este script eliminará TODOS los datos del departamento del Caquetá:")
        print("- Ubicaciones (departamento, municipios, zonas, puestos, mesas)")
        print("- Usuarios (coordinadores y testigos)")
        print("- Formularios E-14 y votos")
        print("- Reportes de participación")
        print("- Incidentes y delitos electorales")
        print("- Evidencias fotográficas")
        print("- Configuración del departamento")
        print()
        print("⚠️ ESTA ACCIÓN NO SE PUEDE DESHACER")
        print()
        
        respuesta = input("¿Está seguro de que desea continuar? (escriba 'ELIMINAR CAQUETA' para confirmar): ")
        
        if respuesta != 'ELIMINAR CAQUETA':
            print("❌ Operación cancelada")
            return
        
        print("\n🚀 Iniciando eliminación...")
        eliminar_datos_caqueta()

if __name__ == '__main__':
    main()