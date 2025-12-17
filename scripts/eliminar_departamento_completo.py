#!/usr/bin/env python3
"""
Sistema completo para eliminar cualquier departamento de Colombia con todos sus datos
Eliminación exhaustiva y segura de coordinadores, testigos y todos los datos relacionados

Uso:
    python scripts/eliminar_departamento_completo.py <codigo> --confirmar
    python scripts/eliminar_departamento_completo.py --listar-configurados
    python scripts/eliminar_departamento_completo.py --verificar-antes <codigo>
    
Ejemplos:
    python scripts/eliminar_departamento_completo.py 44 --confirmar  # Eliminar Caquetá
    python scripts/eliminar_departamento_completo.py 05 --confirmar --forzar  # Forzar eliminación
    python scripts/eliminar_departamento_completo.py --listar-configurados  # Ver departamentos
"""
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from backend.app import create_app
    from backend.database import db
    from backend.models.location import Location
    from backend.models.user import User
    from backend.models.departamento_config import DepartamentoConfig
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class EliminadorDepartamentoCompleto:
    """Eliminador completo y seguro para cualquier departamento"""
    
    def __init__(self):
        self.app = create_app()
    
    def listar_departamentos_configurados(self) -> List[Dict]:
        """Listar todos los departamentos configurados en el sistema"""
        with self.app.app_context():
            configs = DepartamentoConfig.query.all()
            
            departamentos = []
            for config in configs:
                # Actualizar estadísticas
                config.actualizar_estadisticas()
                
                # Obtener datos adicionales
                ubicaciones = Location.query.filter_by(
                    departamento_codigo=config.departamento_codigo,
                    activo=True
                ).count()
                
                ubicaciones_ids = [loc.id for loc in Location.query.filter_by(
                    departamento_codigo=config.departamento_codigo,
                    activo=True
                ).all()]
                
                usuarios = 0
                if ubicaciones_ids:
                    usuarios = User.query.filter(
                        User.ubicacion_id.in_(ubicaciones_ids),
                        User.activo == True
                    ).count()
                
                departamentos.append({
                    'departamento_codigo': config.departamento_codigo,
                    'departamento_nombre': config.departamento_nombre,
                    'habilitado': config.habilitado,
                    'es_principal': config.es_principal,
                    'total_ubicaciones': ubicaciones,
                    'total_usuarios': usuarios,
                    'ultima_carga': config.ultima_carga_at.isoformat() if config.ultima_carga_at else None
                })
            
            db.session.commit()
            return sorted(departamentos, key=lambda x: x['departamento_nombre'])
    
    def verificar_antes_eliminacion(self, departamento_codigo: str) -> Dict:
        """Verificar qué se va a eliminar antes de proceder"""
        print("=" * 80)
        print(f"🔍 VERIFICACIÓN PRE-ELIMINACIÓN - DEPARTAMENTO: {departamento_codigo}")
        print("=" * 80)
        
        with self.app.app_context():
            # Verificar configuración
            config = DepartamentoConfig.query.filter_by(
                departamento_codigo=departamento_codigo
            ).first()
            
            if not config:
                print("ℹ️  No existe configuración para este departamento")
                return {'existe': False, 'motivo': 'Sin configuración'}
            
            # Obtener ubicaciones
            ubicaciones = Location.query.filter_by(
                departamento_codigo=departamento_codigo
            ).all()
            
            ubicaciones_activas = [loc for loc in ubicaciones if loc.activo]
            ubicaciones_inactivas = [loc for loc in ubicaciones if not loc.activo]
            
            # Contar por tipo
            ubicaciones_por_tipo = {}
            for ubicacion in ubicaciones:
                tipo = ubicacion.tipo
                if tipo not in ubicaciones_por_tipo:
                    ubicaciones_por_tipo[tipo] = {'activas': 0, 'inactivas': 0}
                
                if ubicacion.activo:
                    ubicaciones_por_tipo[tipo]['activas'] += 1
                else:
                    ubicaciones_por_tipo[tipo]['inactivas'] += 1
            
            # Obtener usuarios
            ubicaciones_ids = [loc.id for loc in ubicaciones]
            usuarios = []
            if ubicaciones_ids:
                usuarios = User.query.filter(
                    User.ubicacion_id.in_(ubicaciones_ids)
                ).all()
            
            usuarios_activos = [usr for usr in usuarios if usr.activo]
            usuarios_inactivos = [usr for usr in usuarios if not usr.activo]
            
            # Contar por rol
            usuarios_por_rol = {}
            for usuario in usuarios:
                rol = usuario.rol
                if rol not in usuarios_por_rol:
                    usuarios_por_rol[rol] = {'activos': 0, 'inactivos': 0}
                
                if usuario.activo:
                    usuarios_por_rol[rol]['activos'] += 1
                else:
                    usuarios_por_rol[rol]['inactivos'] += 1
            
            # Obtener datos electorales
            datos_electorales = self._contar_datos_electorales(ubicaciones_ids)
            
            # Mostrar resumen
            print(f"📍 DEPARTAMENTO: {config.departamento_nombre}")
            print(f"   Estado: {'🟢 HABILITADO' if config.habilitado else '🔴 DESHABILITADO'}")
            if config.es_principal:
                print(f"   ⭐ DEPARTAMENTO PRINCIPAL")
            print()
            
            print(f"📊 UBICACIONES A ELIMINAR: {len(ubicaciones)}")
            print(f"   • Activas: {len(ubicaciones_activas)}")
            print(f"   • Inactivas: {len(ubicaciones_inactivas)}")
            
            if ubicaciones_por_tipo:
                print(f"   Por tipo:")
                for tipo, counts in ubicaciones_por_tipo.items():
                    total = counts['activas'] + counts['inactivas']
                    print(f"     - {tipo}: {total} ({counts['activas']} activas, {counts['inactivas']} inactivas)")
            print()
            
            print(f"👥 USUARIOS A ELIMINAR: {len(usuarios)}")
            print(f"   • Activos: {len(usuarios_activos)}")
            print(f"   • Inactivos: {len(usuarios_inactivos)}")
            
            if usuarios_por_rol:
                print(f"   Por rol:")
                for rol, counts in usuarios_por_rol.items():
                    total = counts['activos'] + counts['inactivos']
                    print(f"     - {rol}: {total} ({counts['activos']} activos, {counts['inactivos']} inactivos)")
            print()
            
            print(f"🗳️  DATOS ELECTORALES A ELIMINAR:")
            for tipo, cantidad in datos_electorales.items():
                if cantidad > 0:
                    print(f"   • {tipo}: {cantidad}")
            print()
            
            return {
                'existe': True,
                'config': config.to_dict(),
                'total_ubicaciones': len(ubicaciones),
                'ubicaciones_activas': len(ubicaciones_activas),
                'ubicaciones_inactivas': len(ubicaciones_inactivas),
                'ubicaciones_por_tipo': ubicaciones_por_tipo,
                'total_usuarios': len(usuarios),
                'usuarios_activos': len(usuarios_activos),
                'usuarios_inactivos': len(usuarios_inactivos),
                'usuarios_por_rol': usuarios_por_rol,
                'datos_electorales': datos_electorales
            }
    
    def eliminar_departamento_completo(self, departamento_codigo: str, forzar: bool = False) -> Dict:
        """
        Eliminar un departamento completo con todos sus datos de forma exhaustiva
        
        Args:
            departamento_codigo: Código del departamento a eliminar
            forzar: Si debe forzar la eliminación sin confirmaciones adicionales
        """
        print("=" * 80)
        print(f"🗑️  ELIMINACIÓN COMPLETA DE DEPARTAMENTO - CÓDIGO: {departamento_codigo}")
        print("=" * 80)
        
        with self.app.app_context():
            try:
                # PASO 1: Verificación inicial
                print("🔍 PASO 1: VERIFICACIÓN INICIAL")
                print("-" * 40)
                
                verificacion = self.verificar_antes_eliminacion(departamento_codigo)
                
                if not verificacion['existe']:
                    print(f"ℹ️  {verificacion['motivo']}")
                    return {'eliminado': False, 'motivo': verificacion['motivo']}
                
                # PASO 2: Confirmaciones de seguridad
                if not forzar:
                    print("🚨 PASO 2: CONFIRMACIONES DE SEGURIDAD")
                    print("-" * 40)
                    
                    if not self._confirmar_eliminacion(verificacion):
                        print("❌ Eliminación cancelada por el usuario")
                        return {'eliminado': False, 'motivo': 'Cancelado por usuario'}
                
                # PASO 3: Obtener datos para eliminación
                print("\n📋 PASO 3: PREPARANDO ELIMINACIÓN")
                print("-" * 40)
                
                ubicaciones = Location.query.filter_by(
                    departamento_codigo=departamento_codigo
                ).all()
                
                ubicaciones_ids = [loc.id for loc in ubicaciones]
                
                usuarios = []
                if ubicaciones_ids:
                    usuarios = User.query.filter(
                        User.ubicacion_id.in_(ubicaciones_ids)
                    ).all()
                
                print(f"✅ Preparado para eliminar:")
                print(f"   • {len(ubicaciones)} ubicaciones")
                print(f"   • {len(usuarios)} usuarios")
                
                # PASO 4: Eliminación de datos electorales
                print(f"\n🗑️  PASO 4: ELIMINANDO DATOS ELECTORALES")
                print("-" * 40)
                
                datos_eliminados = self._eliminar_datos_electorales_completos(ubicaciones_ids)
                
                # PASO 5: Eliminación de usuarios
                print(f"\n🗑️  PASO 5: ELIMINANDO USUARIOS")
                print("-" * 40)
                
                usuarios_eliminados = self._eliminar_usuarios_completos(usuarios)
                
                # PASO 6: Eliminación de ubicaciones
                print(f"\n🗑️  PASO 6: ELIMINANDO UBICACIONES")
                print("-" * 40)
                
                ubicaciones_eliminadas = self._eliminar_ubicaciones_completas(ubicaciones)
                
                # PASO 7: Eliminación de configuración
                print(f"\n🗑️  PASO 7: ELIMINANDO CONFIGURACIÓN")
                print("-" * 40)
                
                config_eliminada = self._eliminar_configuracion_completa(departamento_codigo)
                
                # PASO 8: Commit y verificación final
                print(f"\n💾 PASO 8: CONFIRMANDO CAMBIOS")
                print("-" * 40)
                
                db.session.commit()
                
                # Verificar eliminación completa
                verificacion_final = self._verificar_eliminacion_completa(departamento_codigo)
                
                # RESUMEN FINAL
                print(f"\n✅ ELIMINACIÓN COMPLETADA EXITOSAMENTE")
                print("=" * 80)
                
                resultado = {
                    'eliminado': True,
                    'departamento_codigo': departamento_codigo,
                    'departamento_nombre': verificacion['config']['departamento_nombre'],
                    'ubicaciones_eliminadas': ubicaciones_eliminadas,
                    'usuarios_eliminados': usuarios_eliminados,
                    'datos_electorales_eliminados': datos_eliminados,
                    'config_eliminada': config_eliminada,
                    'verificacion_final': verificacion_final,
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                self._mostrar_resumen_eliminacion(resultado)
                
                return resultado
                
            except Exception as e:
                print(f"\n❌ ERROR DURANTE LA ELIMINACIÓN: {str(e)}")
                print("🔄 Realizando rollback...")
                db.session.rollback()
                raise
    
    def _contar_datos_electorales(self, ubicaciones_ids: List[int]) -> Dict:
        """Contar todos los datos electorales que se van a eliminar"""
        if not ubicaciones_ids:
            return {}
        
        ubicaciones_str = ','.join(map(str, ubicaciones_ids))
        
        # Obtener usuarios de estas ubicaciones
        result = db.session.execute(
            f"SELECT id FROM users WHERE ubicacion_id IN ({ubicaciones_str})"
        )
        usuarios_ids = [row[0] for row in result.fetchall()]
        
        datos = {}
        
        if usuarios_ids:
            usuarios_str = ','.join(map(str, usuarios_ids))
            
            # Contar formularios E-14
            result = db.session.execute(
                f"SELECT COUNT(*) FROM formularios_e14 WHERE testigo_id IN ({usuarios_str})"
            )
            datos['formularios_e14'] = result.fetchone()[0]
            
            # Contar votos de candidatos
            result = db.session.execute(
                f"SELECT COUNT(*) FROM votos_candidatos WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
            )
            datos['votos_candidatos'] = result.fetchone()[0]
            
            # Contar votos de partidos
            result = db.session.execute(
                f"SELECT COUNT(*) FROM votos_partidos WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
            )
            datos['votos_partidos'] = result.fetchone()[0]
            
            # Contar reportes de participación
            result = db.session.execute(
                f"SELECT COUNT(*) FROM reporte_participacion WHERE testigo_id IN ({usuarios_str})"
            )
            datos['reportes_participacion'] = result.fetchone()[0]
            
            # Contar incidentes electorales
            result = db.session.execute(
                f"SELECT COUNT(*) FROM incidentes_electorales WHERE reportado_por_id IN ({usuarios_str})"
            )
            datos['incidentes_electorales'] = result.fetchone()[0]
            
            # Contar delitos electorales
            result = db.session.execute(
                f"SELECT COUNT(*) FROM delitos_electorales WHERE reportado_por_id IN ({usuarios_str})"
            )
            datos['delitos_electorales'] = result.fetchone()[0]
            
            # Contar evidencias fotográficas
            result = db.session.execute(
                f"SELECT COUNT(*) FROM evidencias_fotograficas WHERE subido_por_id IN ({usuarios_str})"
            )
            datos['evidencias_fotograficas'] = result.fetchone()[0]
            
            # Contar fotos de incidentes/delitos (nueva tabla)
            result = db.session.execute(
                f"SELECT COUNT(*) FROM incidentes_delitos_fotos WHERE subida_por_id IN ({usuarios_str})"
            )
            datos['fotos_incidentes_delitos'] = result.fetchone()[0]
            
            # Contar logs de auditoría
            result = db.session.execute(
                f"SELECT COUNT(*) FROM audit_logs WHERE usuario_id IN ({usuarios_str})"
            )
            datos['logs_auditoria'] = result.fetchone()[0]
        
        return datos
    
    def _confirmar_eliminacion(self, verificacion: Dict) -> bool:
        """Confirmar la eliminación con el usuario"""
        config = verificacion['config']
        
        print(f"⚠️  ADVERTENCIA: Se eliminará COMPLETAMENTE el departamento:")
        print(f"   📍 {config['departamento_nombre']} (Código: {config['departamento_codigo']})")
        
        if config['es_principal']:
            print(f"   ⭐ ¡ES EL DEPARTAMENTO PRINCIPAL!")
        
        print(f"\n🗑️  DATOS QUE SE ELIMINARÁN:")
        print(f"   • {verificacion['total_ubicaciones']} ubicaciones")
        print(f"   • {verificacion['total_usuarios']} usuarios")
        
        datos_electorales = verificacion['datos_electorales']
        total_datos = sum(datos_electorales.values())
        if total_datos > 0:
            print(f"   • {total_datos} registros de datos electorales")
        
        print(f"\n🚨 ESTA ACCIÓN NO SE PUEDE DESHACER")
        print(f"🚨 TODOS LOS DATOS SE PERDERÁN PERMANENTEMENTE")
        print()
        
        # Primera confirmación
        respuesta1 = input(f"Escriba 'ELIMINAR {config['departamento_codigo']}' para continuar: ").strip()
        if respuesta1 != f"ELIMINAR {config['departamento_codigo']}":
            return False
        
        # Segunda confirmación
        respuesta2 = input("¿Está COMPLETAMENTE seguro? (escriba 'SI ELIMINAR TODO'): ").strip()
        if respuesta2 != 'SI ELIMINAR TODO':
            return False
        
        # Tercera confirmación si es departamento principal
        if config['es_principal']:
            respuesta3 = input("¡ES EL DEPARTAMENTO PRINCIPAL! Escriba 'CONFIRMO ELIMINAR PRINCIPAL': ").strip()
            if respuesta3 != 'CONFIRMO ELIMINAR PRINCIPAL':
                return False
        
        return True
    
    def _eliminar_datos_electorales_completos(self, ubicaciones_ids: List[int]) -> Dict:
        """Eliminar todos los datos electorales de forma exhaustiva"""
        if not ubicaciones_ids:
            return {}
        
        ubicaciones_str = ','.join(map(str, ubicaciones_ids))
        
        # Obtener usuarios de estas ubicaciones
        result = db.session.execute(
            f"SELECT id FROM users WHERE ubicacion_id IN ({ubicaciones_str})"
        )
        usuarios_ids = [row[0] for row in result.fetchall()]
        
        eliminados = {}
        
        if not usuarios_ids:
            print("   ℹ️  No hay usuarios para eliminar datos electorales")
            return eliminados
        
        usuarios_str = ','.join(map(str, usuarios_ids))
        
        print("   🗑️  Eliminando datos electorales...")
        
        # 1. Eliminar votos de candidatos
        result = db.session.execute(
            f"DELETE FROM votos_candidatos WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
        )
        eliminados['votos_candidatos'] = result.rowcount
        print(f"      ✅ Votos candidatos: {eliminados['votos_candidatos']}")
        
        # 2. Eliminar votos de partidos
        result = db.session.execute(
            f"DELETE FROM votos_partidos WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
        )
        eliminados['votos_partidos'] = result.rowcount
        print(f"      ✅ Votos partidos: {eliminados['votos_partidos']}")
        
        # 3. Eliminar historial de formularios
        result = db.session.execute(
            f"DELETE FROM historial_formularios WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
        )
        eliminados['historial_formularios'] = result.rowcount
        print(f"      ✅ Historial formularios: {eliminados['historial_formularios']}")
        
        # 4. Eliminar formularios E-14
        result = db.session.execute(
            f"DELETE FROM formularios_e14 WHERE testigo_id IN ({usuarios_str})"
        )
        eliminados['formularios_e14'] = result.rowcount
        print(f"      ✅ Formularios E-14: {eliminados['formularios_e14']}")
        
        # 5. Eliminar reportes de participación
        result = db.session.execute(
            f"DELETE FROM reporte_participacion WHERE testigo_id IN ({usuarios_str})"
        )
        eliminados['reportes_participacion'] = result.rowcount
        print(f"      ✅ Reportes participación: {eliminados['reportes_participacion']}")
        
        # 6. Eliminar incidentes y delitos electorales
        eliminados_incidentes = self._eliminar_incidentes_delitos_completos(usuarios_str)
        eliminados.update(eliminados_incidentes)
        
        # 7. Eliminar formularios E-24 (puesto y municipal)
        eliminados_e24 = self._eliminar_formularios_e24(usuarios_str)
        eliminados.update(eliminados_e24)
        
        # 8. Eliminar seguimiento y notificaciones
        result = db.session.execute(
            f"DELETE FROM seguimiento_reportes WHERE usuario_id IN ({usuarios_str})"
        )
        eliminados['seguimiento_reportes'] = result.rowcount
        print(f"      ✅ Seguimiento reportes: {eliminados['seguimiento_reportes']}")
        
        result = db.session.execute(
            f"DELETE FROM notificaciones_coordinadores WHERE usuario_id IN ({usuarios_str})"
        )
        eliminados['notificaciones'] = result.rowcount
        print(f"      ✅ Notificaciones: {eliminados['notificaciones']}")
        
        # 9. Eliminar logs de auditoría
        result = db.session.execute(
            f"DELETE FROM audit_logs WHERE usuario_id IN ({usuarios_str})"
        )
        eliminados['logs_auditoria'] = result.rowcount
        print(f"      ✅ Logs auditoría: {eliminados['logs_auditoria']}")
        
        # 10. Eliminar reportes departamentales
        result = db.session.execute(
            f"DELETE FROM votos_partidos_reporte_departamental WHERE reporte_id IN (SELECT id FROM reportes_departamentales WHERE departamento_codigo = (SELECT DISTINCT departamento_codigo FROM locations WHERE id IN ({ubicaciones_str}) LIMIT 1))"
        )
        eliminados['votos_reportes_departamentales'] = result.rowcount
        
        result = db.session.execute(
            f"DELETE FROM reportes_departamentales WHERE departamento_codigo = (SELECT DISTINCT departamento_codigo FROM locations WHERE id IN ({ubicaciones_str}) LIMIT 1)"
        )
        eliminados['reportes_departamentales'] = result.rowcount
        print(f"      ✅ Reportes departamentales: {eliminados['reportes_departamentales']}")
        
        return eliminados
    
    def _eliminar_incidentes_delitos_completos(self, usuarios_str: str) -> Dict:
        """Eliminar incidentes y delitos electorales de forma exhaustiva"""
        eliminados = {}
        
        # Obtener IDs de incidentes
        result = db.session.execute(
            f"SELECT id FROM incidentes_electorales WHERE reportado_por_id IN ({usuarios_str})"
        )
        incidentes_ids = [row[0] for row in result.fetchall()]
        
        if incidentes_ids:
            incidentes_str = ','.join(map(str, incidentes_ids))
            
            # Eliminar fotos de incidentes (nueva tabla)
            result = db.session.execute(
                f"DELETE FROM incidentes_delitos_fotos WHERE incidente_id IN ({incidentes_str})"
            )
            eliminados['fotos_incidentes'] = result.rowcount
            print(f"      ✅ Fotos incidentes: {eliminados['fotos_incidentes']}")
            
            # Eliminar evidencias fotográficas de incidentes (tabla antigua)
            result = db.session.execute(
                f"DELETE FROM evidencias_fotograficas WHERE incidente_id IN ({incidentes_str})"
            )
            eliminados['evidencias_incidentes'] = result.rowcount
            print(f"      ✅ Evidencias incidentes: {eliminados['evidencias_incidentes']}")
        
        # Eliminar incidentes
        result = db.session.execute(
            f"DELETE FROM incidentes_electorales WHERE reportado_por_id IN ({usuarios_str})"
        )
        eliminados['incidentes_electorales'] = result.rowcount
        print(f"      ✅ Incidentes electorales: {eliminados['incidentes_electorales']}")
        
        # Obtener IDs de delitos
        result = db.session.execute(
            f"SELECT id FROM delitos_electorales WHERE reportado_por_id IN ({usuarios_str})"
        )
        delitos_ids = [row[0] for row in result.fetchall()]
        
        if delitos_ids:
            delitos_str = ','.join(map(str, delitos_ids))
            
            # Eliminar fotos de delitos
            result = db.session.execute(
                f"DELETE FROM incidentes_delitos_fotos WHERE delito_id IN ({delitos_str})"
            )
            eliminados['fotos_delitos'] = result.rowcount
            print(f"      ✅ Fotos delitos: {eliminados['fotos_delitos']}")
            
            # Eliminar evidencias fotográficas de delitos
            result = db.session.execute(
                f"DELETE FROM evidencias_fotograficas WHERE delito_id IN ({delitos_str})"
            )
            eliminados['evidencias_delitos'] = result.rowcount
            print(f"      ✅ Evidencias delitos: {eliminados['evidencias_delitos']}")
        
        # Eliminar delitos
        result = db.session.execute(
            f"DELETE FROM delitos_electorales WHERE reportado_por_id IN ({usuarios_str})"
        )
        eliminados['delitos_electorales'] = result.rowcount
        print(f"      ✅ Delitos electorales: {eliminados['delitos_electorales']}")
        
        # Eliminar fotos subidas por usuarios (independientemente del incidente/delito)
        result = db.session.execute(
            f"DELETE FROM incidentes_delitos_fotos WHERE subida_por_id IN ({usuarios_str})"
        )
        eliminados['fotos_usuarios'] = result.rowcount
        print(f"      ✅ Fotos subidas por usuarios: {eliminados['fotos_usuarios']}")
        
        result = db.session.execute(
            f"DELETE FROM evidencias_fotograficas WHERE subido_por_id IN ({usuarios_str})"
        )
        eliminados['evidencias_usuarios'] = result.rowcount
        print(f"      ✅ Evidencias subidas por usuarios: {eliminados['evidencias_usuarios']}")
        
        return eliminados
    
    def _eliminar_formularios_e24(self, usuarios_str: str) -> Dict:
        """Eliminar formularios E-24 de puesto y municipal"""
        eliminados = {}
        
        # Formularios E-24 de puesto
        result = db.session.execute(
            f"DELETE FROM votos_partidos_e24_puesto WHERE formulario_id IN (SELECT id FROM formularios_e24_puesto WHERE coordinador_id IN ({usuarios_str}))"
        )
        eliminados['votos_e24_puesto'] = result.rowcount
        
        result = db.session.execute(
            f"DELETE FROM formularios_e24_puesto WHERE coordinador_id IN ({usuarios_str})"
        )
        eliminados['formularios_e24_puesto'] = result.rowcount
        print(f"      ✅ Formularios E-24 puesto: {eliminados['formularios_e24_puesto']}")
        
        # Formularios E-24 municipal
        result = db.session.execute(
            f"DELETE FROM votos_partidos_e24_municipal WHERE formulario_id IN (SELECT id FROM formularios_e24_municipal WHERE coordinador_id IN ({usuarios_str}))"
        )
        eliminados['votos_e24_municipal'] = result.rowcount
        
        result = db.session.execute(
            f"DELETE FROM formularios_e24_municipal WHERE coordinador_id IN ({usuarios_str})"
        )
        eliminados['formularios_e24_municipal'] = result.rowcount
        print(f"      ✅ Formularios E-24 municipal: {eliminados['formularios_e24_municipal']}")
        
        return eliminados
    
    def _eliminar_usuarios_completos(self, usuarios: List) -> Dict:
        """Eliminar usuarios de forma completa"""
        eliminados = {
            'total': 0,
            'por_rol': {},
            'super_admin_preservados': 0
        }
        
        print("   🗑️  Eliminando usuarios...")
        
        for usuario in usuarios:
            if usuario.rol == 'super_admin':
                eliminados['super_admin_preservados'] += 1
                print(f"      ⚠️  Preservando super admin: {usuario.nombre}")
                continue
            
            rol = usuario.rol
            if rol not in eliminados['por_rol']:
                eliminados['por_rol'][rol] = 0
            
            eliminados['por_rol'][rol] += 1
            eliminados['total'] += 1
            
            db.session.delete(usuario)
        
        print(f"      ✅ Usuarios eliminados: {eliminados['total']}")
        for rol, cantidad in eliminados['por_rol'].items():
            print(f"         - {rol}: {cantidad}")
        
        if eliminados['super_admin_preservados'] > 0:
            print(f"      ⚠️  Super admins preservados: {eliminados['super_admin_preservados']}")
        
        return eliminados
    
    def _eliminar_ubicaciones_completas(self, ubicaciones: List) -> Dict:
        """Eliminar ubicaciones de forma completa"""
        eliminados = {
            'total': len(ubicaciones),
            'por_tipo': {}
        }
        
        print("   🗑️  Eliminando ubicaciones...")
        
        for ubicacion in ubicaciones:
            tipo = ubicacion.tipo
            if tipo not in eliminados['por_tipo']:
                eliminados['por_tipo'][tipo] = 0
            
            eliminados['por_tipo'][tipo] += 1
            db.session.delete(ubicacion)
        
        print(f"      ✅ Ubicaciones eliminadas: {eliminados['total']}")
        for tipo, cantidad in eliminados['por_tipo'].items():
            print(f"         - {tipo}: {cantidad}")
        
        return eliminados
    
    def _eliminar_configuracion_completa(self, departamento_codigo: str) -> bool:
        """Eliminar configuración del departamento"""
        config = DepartamentoConfig.query.filter_by(
            departamento_codigo=departamento_codigo
        ).first()
        
        if config:
            nombre = config.departamento_nombre
            db.session.delete(config)
            print(f"      ✅ Configuración eliminada: {nombre}")
            return True
        else:
            print("      ℹ️  No se encontró configuración para eliminar")
            return False
    
    def _verificar_eliminacion_completa(self, departamento_codigo: str) -> Dict:
        """Verificar que la eliminación fue completa"""
        print("   🔍 Verificando eliminación completa...")
        
        # Verificar ubicaciones restantes
        ubicaciones_restantes = Location.query.filter_by(
            departamento_codigo=departamento_codigo
        ).count()
        
        # Verificar configuración restante
        config_restante = DepartamentoConfig.query.filter_by(
            departamento_codigo=departamento_codigo
        ).first()
        
        # Verificar usuarios huérfanos (sin ubicación válida)
        usuarios_huerfanos = db.session.query(User).outerjoin(
            Location, User.ubicacion_id == Location.id
        ).filter(
            Location.id.is_(None),
            User.rol != 'super_admin'
        ).count()
        
        verificacion = {
            'ubicaciones_restantes': ubicaciones_restantes,
            'config_restante': config_restante is not None,
            'usuarios_huerfanos': usuarios_huerfanos,
            'eliminacion_completa': ubicaciones_restantes == 0 and config_restante is None
        }
        
        if verificacion['eliminacion_completa']:
            print("      ✅ Eliminación verificada como completa")
        else:
            print("      ⚠️  Eliminación incompleta detectada")
            if ubicaciones_restantes > 0:
                print(f"         - {ubicaciones_restantes} ubicaciones restantes")
            if config_restante:
                print(f"         - Configuración aún presente")
        
        if usuarios_huerfanos > 0:
            print(f"      ⚠️  {usuarios_huerfanos} usuarios huérfanos detectados")
        
        return verificacion
    
    def _mostrar_resumen_eliminacion(self, resultado: Dict):
        """Mostrar resumen completo de la eliminación"""
        print(f"\n📊 RESUMEN COMPLETO DE ELIMINACIÓN:")
        print(f"   • Departamento: {resultado['departamento_nombre']} ({resultado['departamento_codigo']})")
        print(f"   • Timestamp: {resultado['timestamp']}")
        print()
        
        print(f"🗑️  ELEMENTOS ELIMINADOS:")
        print(f"   • Ubicaciones: {resultado['ubicaciones_eliminadas']['total']}")
        for tipo, cantidad in resultado['ubicaciones_eliminadas']['por_tipo'].items():
            print(f"     - {tipo}: {cantidad}")
        
        print(f"   • Usuarios: {resultado['usuarios_eliminados']['total']}")
        for rol, cantidad in resultado['usuarios_eliminados']['por_rol'].items():
            print(f"     - {rol}: {cantidad}")
        
        if resultado['usuarios_eliminados']['super_admin_preservados'] > 0:
            print(f"   • Super admins preservados: {resultado['usuarios_eliminados']['super_admin_preservados']}")
        
        print(f"   • Configuración: {'Sí' if resultado['config_eliminada'] else 'No'}")
        
        datos_electorales = resultado['datos_electorales_eliminados']
        total_datos = sum(v for v in datos_electorales.values() if isinstance(v, int))
        if total_datos > 0:
            print(f"   • Datos electorales: {total_datos} registros")
        
        verificacion = resultado['verificacion_final']
        if verificacion['eliminacion_completa']:
            print(f"\n✅ ELIMINACIÓN COMPLETAMENTE EXITOSA")
        else:
            print(f"\n⚠️  ELIMINACIÓN CON ADVERTENCIAS")
            if verificacion['ubicaciones_restantes'] > 0:
                print(f"   - {verificacion['ubicaciones_restantes']} ubicaciones no eliminadas")
            if verificacion['config_restante']:
                print(f"   - Configuración no eliminada")
        
        if verificacion['usuarios_huerfanos'] > 0:
            print(f"   ⚠️  {verificacion['usuarios_huerfanos']} usuarios huérfanos detectados")
        
        print(f"\n🎯 ESTADO FINAL: Departamento {resultado['departamento_codigo']} eliminado del sistema")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Eliminar departamento completo con todos sus datos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/eliminar_departamento_completo.py --listar-configurados
  python scripts/eliminar_departamento_completo.py --verificar-antes 44
  python scripts/eliminar_departamento_completo.py 44 --confirmar
  python scripts/eliminar_departamento_completo.py 05 --confirmar --forzar
        """
    )
    
    parser.add_argument('codigo', nargs='?', help='Código del departamento a eliminar')
    parser.add_argument('--confirmar', action='store_true', required=False,
                       help='Confirmar que desea eliminar TODOS los datos del departamento')
    parser.add_argument('--forzar', action='store_true',
                       help='Forzar eliminación sin confirmaciones adicionales')
    parser.add_argument('--listar-configurados', action='store_true',
                       help='Listar departamentos configurados en el sistema')
    parser.add_argument('--verificar-antes', metavar='CODIGO',
                       help='Verificar qué se eliminará antes de proceder')
    
    args = parser.parse_args()
    
    eliminador = EliminadorDepartamentoCompleto()
    
    try:
        # Listar departamentos configurados
        if args.listar_configurados:
            print("📊 DEPARTAMENTOS CONFIGURADOS EN EL SISTEMA")
            print("=" * 60)
            
            departamentos = eliminador.listar_departamentos_configurados()
            
            if not departamentos:
                print("ℹ️  No hay departamentos configurados")
                return
            
            for dept in departamentos:
                status = "🟢 HABILITADO" if dept['habilitado'] else "🔴 DESHABILITADO"
                principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                
                print(f"📍 {dept['departamento_codigo']} - {dept['departamento_nombre']}")
                print(f"   Estado: {status}{principal}")
                print(f"   📊 {dept['total_ubicaciones']} ubicaciones, {dept['total_usuarios']} usuarios")
                
                if dept['ultima_carga']:
                    fecha = datetime.fromisoformat(dept['ultima_carga']).strftime('%Y-%m-%d %H:%M')
                    print(f"   🕒 Última carga: {fecha}")
                print()
            
            print("💡 Use --verificar-antes <codigo> para ver qué se eliminará")
            print("💡 Use <codigo> --confirmar para eliminar un departamento")
            return
        
        # Verificar antes de eliminar
        if args.verificar_antes:
            codigo = args.verificar_antes.strip().zfill(2)
            verificacion = eliminador.verificar_antes_eliminacion(codigo)
            
            if verificacion['existe']:
                print("💡 Use este mismo código con --confirmar para proceder con la eliminación")
            else:
                print("ℹ️  No hay nada que eliminar para este departamento")
            return
        
        # Eliminar departamento
        if args.codigo:
            if not args.confirmar:
                print("❌ Debe usar --confirmar para eliminar un departamento")
                print("💡 Esta es una medida de seguridad para evitar eliminaciones accidentales")
                print(f"💡 Use --verificar-antes {args.codigo} para ver qué se eliminará")
                sys.exit(1)
            
            codigo = args.codigo.strip().zfill(2)
            
            resultado = eliminador.eliminar_departamento_completo(
                departamento_codigo=codigo,
                forzar=args.forzar
            )
            
            if resultado['eliminado']:
                print(f"\n🎯 ¡DEPARTAMENTO {codigo} ELIMINADO EXITOSAMENTE!")
                sys.exit(0)
            else:
                print(f"\n❌ No se pudo eliminar departamento {codigo}: {resultado.get('motivo')}")
                sys.exit(1)
        
        else:
            print("❌ Debe especificar una acción")
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()