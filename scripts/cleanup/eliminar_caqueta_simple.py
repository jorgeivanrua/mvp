#!/usr/bin/env python3
"""
Script simple para eliminar todos los datos del departamento del Caquetá
Usa SQL directo para evitar conflictos con modelos ORM
"""
import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app import create_app
from backend.database import db

def eliminar_datos_caqueta():
    """Eliminar todos los datos relacionados con el departamento del Caquetá usando SQL directo"""
    
    print("🗑️ ELIMINANDO DATOS DEL CAQUETÁ")
    print("=" * 50)
    
    # Código del Caquetá
    CAQUETA_CODIGO = '44'
    
    try:
        # 1. Obtener IDs de ubicaciones del Caquetá
        print(f"📍 Obteniendo ubicaciones del Caquetá (código: {CAQUETA_CODIGO})...")
        result = db.session.execute(
            f"SELECT id FROM locations WHERE departamento_codigo = '{CAQUETA_CODIGO}'"
        )
        ubicaciones_ids = [row[0] for row in result.fetchall()]
        print(f"   Encontradas {len(ubicaciones_ids)} ubicaciones")
        
        if not ubicaciones_ids:
            print("   ✅ No se encontraron ubicaciones del Caquetá")
            return
        
        # 2. Obtener IDs de usuarios del Caquetá
        print(f"👥 Obteniendo usuarios del Caquetá...")
        ubicaciones_str = ','.join(map(str, ubicaciones_ids))
        result = db.session.execute(
            f"SELECT id FROM users WHERE ubicacion_id IN ({ubicaciones_str})"
        )
        usuarios_ids = [row[0] for row in result.fetchall()]
        print(f"   Encontrados {len(usuarios_ids)} usuarios")
        
        if usuarios_ids:
            usuarios_str = ','.join(map(str, usuarios_ids))
            
            # 3. Eliminar formularios E-14 y datos relacionados
            print(f"📋 Eliminando formularios E-14...")
            result = db.session.execute(
                f"DELETE FROM votos_candidatos WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
            )
            print(f"   Eliminados {result.rowcount} votos de candidatos")
            
            result = db.session.execute(
                f"DELETE FROM votos_partidos WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
            )
            print(f"   Eliminados {result.rowcount} votos de partidos")
            
            result = db.session.execute(
                f"DELETE FROM historial_formularios WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
            )
            print(f"   Eliminados {result.rowcount} registros de historial")
            
            result = db.session.execute(
                f"DELETE FROM formularios_e14 WHERE testigo_id IN ({usuarios_str})"
            )
            print(f"   Eliminados {result.rowcount} formularios E-14")
            
            # 4. Eliminar reportes de participación
            print(f"📊 Eliminando reportes de participación...")
            result = db.session.execute(
                f"DELETE FROM reporte_participacion WHERE testigo_id IN ({usuarios_str})"
            )
            print(f"   Eliminados {result.rowcount} reportes de participación")
            
            # 5. Eliminar incidentes electorales y datos relacionados
            print(f"⚠️ Eliminando incidentes electorales...")
            
            # 5.1. Obtener IDs de incidentes
            result = db.session.execute(
                f"SELECT id FROM incidentes_electorales WHERE reportado_por_id IN ({usuarios_str})"
            )
            incidentes_ids = [row[0] for row in result.fetchall()]
            print(f"   Encontrados {len(incidentes_ids)} incidentes")
            
            if incidentes_ids:
                incidentes_str = ','.join(map(str, incidentes_ids))
                
                # 5.2. Eliminar evidencias fotográficas de incidentes
                result = db.session.execute(
                    f"DELETE FROM evidencias_fotograficas WHERE incidente_id IN ({incidentes_str})"
                )
                print(f"   Eliminadas {result.rowcount} evidencias fotográficas de incidentes")
                
                # 5.3. Eliminar seguimiento de incidentes
                result = db.session.execute(
                    f"DELETE FROM seguimiento_reportes WHERE tipo_reporte = 'incidente' AND reporte_id IN ({incidentes_str})"
                )
                print(f"   Eliminados {result.rowcount} registros de seguimiento de incidentes")
                
                # 5.4. Eliminar notificaciones de incidentes
                result = db.session.execute(
                    f"DELETE FROM notificaciones_reportes WHERE incidente_id IN ({incidentes_str})"
                )
                print(f"   Eliminadas {result.rowcount} notificaciones de incidentes")
            
            # 5.5. Eliminar incidentes
            result = db.session.execute(
                f"DELETE FROM incidentes_electorales WHERE reportado_por_id IN ({usuarios_str})"
            )
            print(f"   Eliminados {result.rowcount} incidentes electorales")
            
            # 6. Eliminar delitos electorales y datos relacionados
            print(f"🚨 Eliminando delitos electorales...")
            
            # 6.1. Obtener IDs de delitos
            result = db.session.execute(
                f"SELECT id FROM delitos_electorales WHERE reportado_por_id IN ({usuarios_str})"
            )
            delitos_ids = [row[0] for row in result.fetchall()]
            print(f"   Encontrados {len(delitos_ids)} delitos")
            
            if delitos_ids:
                delitos_str = ','.join(map(str, delitos_ids))
                
                # 6.2. Eliminar evidencias fotográficas de delitos
                result = db.session.execute(
                    f"DELETE FROM evidencias_fotograficas WHERE delito_id IN ({delitos_str})"
                )
                print(f"   Eliminadas {result.rowcount} evidencias fotográficas de delitos")
                
                # 6.3. Eliminar seguimiento de delitos
                result = db.session.execute(
                    f"DELETE FROM seguimiento_reportes WHERE tipo_reporte = 'delito' AND reporte_id IN ({delitos_str})"
                )
                print(f"   Eliminados {result.rowcount} registros de seguimiento de delitos")
                
                # 6.4. Eliminar notificaciones de delitos
                result = db.session.execute(
                    f"DELETE FROM notificaciones_reportes WHERE delito_id IN ({delitos_str})"
                )
                print(f"   Eliminadas {result.rowcount} notificaciones de delitos")
            
            # 6.5. Eliminar delitos
            result = db.session.execute(
                f"DELETE FROM delitos_electorales WHERE reportado_por_id IN ({usuarios_str})"
            )
            print(f"   Eliminados {result.rowcount} delitos electorales")
            
            # 7. Eliminar evidencias fotográficas subidas por usuarios del Caquetá
            print(f"📸 Eliminando evidencias fotográficas...")
            result = db.session.execute(
                f"DELETE FROM evidencias_fotograficas WHERE subido_por_id IN ({usuarios_str})"
            )
            print(f"   Eliminadas {result.rowcount} evidencias fotográficas")
            
            # 8. Eliminar fotos de incidentes/delitos (nueva tabla)
            print(f"📷 Eliminando fotos de incidentes/delitos...")
            result = db.session.execute(
                f"DELETE FROM incidentes_delitos_fotos WHERE subida_por_id IN ({usuarios_str})"
            )
            print(f"   Eliminadas {result.rowcount} fotos de incidentes/delitos")
            
            # 9. Eliminar seguimiento de usuarios
            print(f"📋 Eliminando seguimiento de usuarios...")
            result = db.session.execute(
                f"DELETE FROM seguimiento_reportes WHERE usuario_id IN ({usuarios_str})"
            )
            print(f"   Eliminados {result.rowcount} registros de seguimiento")
            
            # 10. Eliminar notificaciones de coordinadores
            print(f"🔔 Eliminando notificaciones...")
            result = db.session.execute(
                f"DELETE FROM notificaciones_coordinadores WHERE usuario_id IN ({usuarios_str})"
            )
            print(f"   Eliminadas {result.rowcount} notificaciones de coordinadores")
            
            # 11. Eliminar logs de auditoría
            print(f"📝 Eliminando logs de auditoría...")
            result = db.session.execute(
                f"DELETE FROM audit_logs WHERE usuario_id IN ({usuarios_str})"
            )
            print(f"   Eliminados {result.rowcount} logs de auditoría")
        
        # 12. Eliminar usuarios
        print(f"👥 Eliminando usuarios...")
        result = db.session.execute(
            f"DELETE FROM users WHERE ubicacion_id IN ({ubicaciones_str})"
        )
        print(f"   Eliminados {result.rowcount} usuarios")
        
        # 13. Eliminar ubicaciones del Caquetá
        print(f"📍 Eliminando ubicaciones...")
        result = db.session.execute(
            f"DELETE FROM locations WHERE departamento_codigo = '{CAQUETA_CODIGO}'"
        )
        print(f"   Eliminadas {result.rowcount} ubicaciones")
        
        # 14. Eliminar configuración del departamento del Caquetá
        print(f"⚙️ Eliminando configuración del departamento...")
        result = db.session.execute(
            f"DELETE FROM departamentos_config WHERE departamento_codigo = '{CAQUETA_CODIGO}'"
        )
        print(f"   Eliminadas {result.rowcount} configuraciones de departamento")
        
        # Commit de todos los cambios
        db.session.commit()
        
        print("\n" + "=" * 50)
        print("✅ ELIMINACIÓN COMPLETADA")
        print("=" * 50)
        
        # Mostrar estadísticas finales
        print(f"📊 ESTADÍSTICAS FINALES:")
        
        # Contar ubicaciones restantes
        result = db.session.execute("SELECT COUNT(*) FROM locations WHERE activo = 1")
        total_ubicaciones = result.fetchone()[0]
        
        result = db.session.execute("SELECT COUNT(*) FROM locations WHERE departamento_codigo = '26' AND activo = 1")
        ubicaciones_quindio = result.fetchone()[0]
        
        print(f"   Ubicaciones totales: {total_ubicaciones}")
        print(f"   Ubicaciones Quindío: {ubicaciones_quindio}")
        
        # Contar usuarios restantes
        result = db.session.execute("SELECT COUNT(*) FROM users WHERE activo = 1")
        total_usuarios = result.fetchone()[0]
        
        result = db.session.execute("""
            SELECT COUNT(*) FROM users u 
            JOIN locations l ON u.ubicacion_id = l.id 
            WHERE l.departamento_codigo = '26' AND u.activo = 1
        """)
        usuarios_quindio = result.fetchone()[0]
        
        print(f"   Usuarios totales: {total_usuarios}")
        print(f"   Usuarios Quindío: {usuarios_quindio}")
        
        # Verificar departamentos configurados
        result = db.session.execute("SELECT departamento_nombre, es_principal FROM departamentos_config WHERE habilitado = 1")
        departamentos = result.fetchall()
        print(f"   Departamentos habilitados: {len(departamentos)}")
        for dept in departamentos:
            print(f"   - {dept[0]} ({'Principal' if dept[1] else 'Secundario'})")
        
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