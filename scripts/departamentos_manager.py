#!/usr/bin/env python3
"""
Gestor unificado para carga y eliminación completa de departamentos
Permite cargar o eliminar cualquier departamento de forma fácil, fluida y completa
"""
import sys
import os
import csv
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
    from backend.services.departamento_service import DepartamentoService
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class DepartamentosManager:
    """Gestor unificado para departamentos"""
    
    def __init__(self):
        self.app = create_app()
        self.csv_file = 'data/divipola.csv'
    
    def listar_departamentos_disponibles(self) -> List[Dict]:
        """Listar todos los departamentos disponibles en el CSV"""
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(f"Archivo {self.csv_file} no encontrado")
        
        departamentos = {}
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dd = row['dd'].strip().zfill(2)
                depto_nombre = row['departamento'].strip().upper()
                
                if dd not in departamentos:
                    departamentos[dd] = {
                        'codigo': dd,
                        'nombre': depto_nombre,
                        'municipios': set(),
                        'total_registros': 0
                    }
                
                departamentos[dd]['municipios'].add(row['municipio'].strip())
                departamentos[dd]['total_registros'] += 1
        
        # Convertir a lista
        resultado = []
        for codigo, info in departamentos.items():
            resultado.append({
                'departamento_codigo': codigo,
                'departamento_nombre': info['nombre'],
                'total_municipios': len(info['municipios']),
                'total_registros': info['total_registros']
            })
        
        return sorted(resultado, key=lambda x: x['departamento_nombre'])
    
    def obtener_estado_departamentos(self) -> List[Dict]:
        """Obtener estado actual de departamentos en el sistema"""
        with self.app.app_context():
            configs = DepartamentoConfig.query.all()
            
            # Actualizar estadísticas
            for config in configs:
                config.actualizar_estadisticas()
            db.session.commit()
            
            return [config.to_dict() for config in configs]
    
    def cargar_departamento_completo(self, departamento_codigo: str, es_principal: bool = False) -> Dict:
        """
        Cargar un departamento completo con todas sus ubicaciones y usuarios
        
        Args:
            departamento_codigo: Código del departamento (ej: '26' para Quindío)
            es_principal: Si debe ser el departamento principal
        """
        print("=" * 80)
        print(f"CARGANDO DEPARTAMENTO COMPLETO - CÓDIGO: {departamento_codigo}")
        print("=" * 80)
        
        # Verificar que el departamento existe
        departamentos_disponibles = self.listar_departamentos_disponibles()
        depto_info = next((d for d in departamentos_disponibles 
                          if d['departamento_codigo'] == departamento_codigo), None)
        
        if not depto_info:
            raise ValueError(f"Departamento con código {departamento_codigo} no encontrado")
        
        print(f"📍 Departamento: {depto_info['departamento_nombre']}")
        print(f"📊 Municipios: {depto_info['total_municipios']}")
        print(f"📈 Total registros: {depto_info['total_registros']}")
        print()
        
        with self.app.app_context():
            try:
                # Usar el servicio de departamentos
                resultado = DepartamentoService.habilitar_departamento(
                    departamento_codigo=departamento_codigo,
                    es_principal=es_principal,
                    auto_cargar=True
                )
                
                print("✅ CARGA COMPLETADA EXITOSAMENTE")
                print("=" * 80)
                print()
                print("📊 RESUMEN:")
                
                carga = resultado.get('carga', {})
                ubicaciones = carga.get('ubicaciones', {})
                usuarios = carga.get('usuarios', {})
                
                print(f"   • Departamento: {carga.get('departamento_nombre', 'N/A')}")
                print(f"   • Municipios: {ubicaciones.get('municipios', 0)}")
                print(f"   • Zonas: {ubicaciones.get('zonas', 0)}")
                print(f"   • Puestos: {ubicaciones.get('puestos', 0)}")
                print(f"   • Mesas: {ubicaciones.get('mesas_creadas', 0)}")
                print()
                print("👥 USUARIOS CREADOS:")
                print(f"   • Coordinador Departamental: {usuarios.get('coordinador_departamental', 0)}")
                print(f"   • Coordinadores Municipales: {usuarios.get('coordinador_municipal', 0)}")
                print(f"   • Coordinadores de Puesto: {usuarios.get('coordinador_puesto', 0)}")
                print(f"   • Testigos Electorales: {usuarios.get('testigo_electoral', 0)}")
                print()
                print("🔐 CONTRASEÑA PARA TODOS LOS USUARIOS: test123")
                print()
                
                if es_principal:
                    print("⭐ DEPARTAMENTO MARCADO COMO PRINCIPAL")
                    print()
                
                return resultado
                
            except Exception as e:
                print(f"❌ Error durante la carga: {str(e)}")
                db.session.rollback()
                raise
    
    def eliminar_departamento_completo(self, departamento_codigo: str, confirmar: bool = False) -> Dict:
        """
        Eliminar un departamento completo con todos sus datos
        
        Args:
            departamento_codigo: Código del departamento a eliminar
            confirmar: Si se ha confirmado la eliminación
        """
        if not confirmar:
            raise ValueError("Debe confirmar la eliminación explícitamente")
        
        print("=" * 80)
        print(f"ELIMINANDO DEPARTAMENTO COMPLETO - CÓDIGO: {departamento_codigo}")
        print("=" * 80)
        
        with self.app.app_context():
            try:
                # Verificar que el departamento existe
                ubicaciones = Location.query.filter_by(
                    departamento_codigo=departamento_codigo
                ).all()
                
                if not ubicaciones:
                    print("ℹ️  No se encontraron ubicaciones para este departamento")
                    return {'eliminado': False, 'motivo': 'No existe'}
                
                depto_nombre = ubicaciones[0].departamento_nombre
                print(f"📍 Departamento: {depto_nombre}")
                print(f"📊 Ubicaciones encontradas: {len(ubicaciones)}")
                
                # Obtener IDs de ubicaciones
                ubicaciones_ids = [loc.id for loc in ubicaciones]
                
                # Obtener usuarios del departamento
                usuarios = User.query.filter(
                    User.ubicacion_id.in_(ubicaciones_ids)
                ).all()
                
                print(f"👥 Usuarios encontrados: {len(usuarios)}")
                print()
                
                # Estadísticas antes de eliminar
                stats_antes = self._obtener_estadisticas_departamento(departamento_codigo)
                
                # PASO 1: Eliminar datos electorales
                print("🗑️  PASO 1: Eliminando datos electorales...")
                self._eliminar_datos_electorales(ubicaciones_ids)
                
                # PASO 2: Eliminar usuarios
                print("🗑️  PASO 2: Eliminando usuarios...")
                usuarios_eliminados = self._eliminar_usuarios_departamento(usuarios)
                
                # PASO 3: Eliminar ubicaciones
                print("🗑️  PASO 3: Eliminando ubicaciones...")
                ubicaciones_eliminadas = self._eliminar_ubicaciones_departamento(ubicaciones)
                
                # PASO 4: Eliminar configuración
                print("🗑️  PASO 4: Eliminando configuración...")
                config_eliminada = self._eliminar_configuracion_departamento(departamento_codigo)
                
                # Commit final
                db.session.commit()
                
                print("✅ ELIMINACIÓN COMPLETADA EXITOSAMENTE")
                print("=" * 80)
                print()
                print("📊 RESUMEN DE ELIMINACIÓN:")
                print(f"   • Departamento: {depto_nombre}")
                print(f"   • Ubicaciones eliminadas: {ubicaciones_eliminadas}")
                print(f"   • Usuarios eliminados: {usuarios_eliminados}")
                print(f"   • Configuración eliminada: {'Sí' if config_eliminada else 'No'}")
                print()
                
                # Estadísticas después
                stats_despues = self._obtener_estadisticas_sistema()
                print("📈 ESTADÍSTICAS DEL SISTEMA:")
                print(f"   • Ubicaciones restantes: {stats_despues['ubicaciones']}")
                print(f"   • Usuarios restantes: {stats_despues['usuarios']}")
                print(f"   • Departamentos habilitados: {stats_despues['departamentos_habilitados']}")
                print()
                
                return {
                    'eliminado': True,
                    'departamento_nombre': depto_nombre,
                    'ubicaciones_eliminadas': ubicaciones_eliminadas,
                    'usuarios_eliminados': usuarios_eliminados,
                    'config_eliminada': config_eliminada,
                    'estadisticas_antes': stats_antes,
                    'estadisticas_despues': stats_despues
                }
                
            except Exception as e:
                print(f"❌ Error durante la eliminación: {str(e)}")
                db.session.rollback()
                raise
    
    def _eliminar_datos_electorales(self, ubicaciones_ids: List[int]):
        """Eliminar todos los datos electorales de las ubicaciones"""
        if not ubicaciones_ids:
            return
        
        ubicaciones_str = ','.join(map(str, ubicaciones_ids))
        
        # Obtener usuarios de estas ubicaciones
        result = db.session.execute(
            f"SELECT id FROM users WHERE ubicacion_id IN ({ubicaciones_str})"
        )
        usuarios_ids = [row[0] for row in result.fetchall()]
        
        if not usuarios_ids:
            print("   No hay usuarios para eliminar datos electorales")
            return
        
        usuarios_str = ','.join(map(str, usuarios_ids))
        
        # Eliminar formularios E-14 y datos relacionados
        eliminaciones = []
        
        # Votos de candidatos
        result = db.session.execute(
            f"DELETE FROM votos_candidatos WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
        )
        eliminaciones.append(f"Votos candidatos: {result.rowcount}")
        
        # Votos de partidos
        result = db.session.execute(
            f"DELETE FROM votos_partidos WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
        )
        eliminaciones.append(f"Votos partidos: {result.rowcount}")
        
        # Historial de formularios
        result = db.session.execute(
            f"DELETE FROM historial_formularios WHERE formulario_id IN (SELECT id FROM formularios_e14 WHERE testigo_id IN ({usuarios_str}))"
        )
        eliminaciones.append(f"Historial formularios: {result.rowcount}")
        
        # Formularios E-14
        result = db.session.execute(
            f"DELETE FROM formularios_e14 WHERE testigo_id IN ({usuarios_str})"
        )
        eliminaciones.append(f"Formularios E-14: {result.rowcount}")
        
        # Reportes de participación
        result = db.session.execute(
            f"DELETE FROM reporte_participacion WHERE testigo_id IN ({usuarios_str})"
        )
        eliminaciones.append(f"Reportes participación: {result.rowcount}")
        
        # Incidentes y delitos electorales
        self._eliminar_incidentes_delitos(usuarios_str)
        
        # Seguimiento y notificaciones
        result = db.session.execute(
            f"DELETE FROM seguimiento_reportes WHERE usuario_id IN ({usuarios_str})"
        )
        eliminaciones.append(f"Seguimiento reportes: {result.rowcount}")
        
        result = db.session.execute(
            f"DELETE FROM notificaciones_coordinadores WHERE usuario_id IN ({usuarios_str})"
        )
        eliminaciones.append(f"Notificaciones: {result.rowcount}")
        
        # Logs de auditoría
        result = db.session.execute(
            f"DELETE FROM audit_logs WHERE usuario_id IN ({usuarios_str})"
        )
        eliminaciones.append(f"Logs auditoría: {result.rowcount}")
        
        for eliminacion in eliminaciones:
            print(f"   ✅ {eliminacion}")
    
    def _eliminar_incidentes_delitos(self, usuarios_str: str):
        """Eliminar incidentes y delitos electorales"""
        # Obtener IDs de incidentes
        result = db.session.execute(
            f"SELECT id FROM incidentes_electorales WHERE reportado_por_id IN ({usuarios_str})"
        )
        incidentes_ids = [row[0] for row in result.fetchall()]
        
        if incidentes_ids:
            incidentes_str = ','.join(map(str, incidentes_ids))
            
            # Eliminar fotos de incidentes (tabla nueva)
            result = db.session.execute(
                f"DELETE FROM incidentes_delitos_fotos WHERE incidente_id IN ({incidentes_str})"
            )
            print(f"   ✅ Fotos incidentes: {result.rowcount}")
            
            # Eliminar evidencias fotográficas (tabla antigua)
            result = db.session.execute(
                f"DELETE FROM evidencias_fotograficas WHERE incidente_id IN ({incidentes_str})"
            )
            print(f"   ✅ Evidencias fotográficas incidentes: {result.rowcount}")
            
            # Eliminar seguimiento de incidentes
            result = db.session.execute(
                f"DELETE FROM seguimiento_reportes WHERE tipo_reporte = 'incidente' AND reporte_id IN ({incidentes_str})"
            )
            print(f"   ✅ Seguimiento incidentes: {result.rowcount}")
        
        # Eliminar incidentes
        result = db.session.execute(
            f"DELETE FROM incidentes_electorales WHERE reportado_por_id IN ({usuarios_str})"
        )
        print(f"   ✅ Incidentes electorales: {result.rowcount}")
        
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
            print(f"   ✅ Fotos delitos: {result.rowcount}")
            
            # Eliminar evidencias fotográficas de delitos
            result = db.session.execute(
                f"DELETE FROM evidencias_fotograficas WHERE delito_id IN ({delitos_str})"
            )
            print(f"   ✅ Evidencias fotográficas delitos: {result.rowcount}")
            
            # Eliminar seguimiento de delitos
            result = db.session.execute(
                f"DELETE FROM seguimiento_reportes WHERE tipo_reporte = 'delito' AND reporte_id IN ({delitos_str})"
            )
            print(f"   ✅ Seguimiento delitos: {result.rowcount}")
        
        # Eliminar delitos
        result = db.session.execute(
            f"DELETE FROM delitos_electorales WHERE reportado_por_id IN ({usuarios_str})"
        )
        print(f"   ✅ Delitos electorales: {result.rowcount}")
        
        # Eliminar fotos subidas por usuarios (independientemente del incidente/delito)
        result = db.session.execute(
            f"DELETE FROM incidentes_delitos_fotos WHERE subida_por_id IN ({usuarios_str})"
        )
        print(f"   ✅ Fotos subidas por usuarios: {result.rowcount}")
        
        result = db.session.execute(
            f"DELETE FROM evidencias_fotograficas WHERE subido_por_id IN ({usuarios_str})"
        )
        print(f"   ✅ Evidencias subidas por usuarios: {result.rowcount}")
    
    def _eliminar_usuarios_departamento(self, usuarios: List) -> int:
        """Eliminar usuarios del departamento"""
        count = 0
        for usuario in usuarios:
            if usuario.rol != 'super_admin':  # No eliminar super admin
                db.session.delete(usuario)
                count += 1
        
        print(f"   ✅ Usuarios eliminados: {count}")
        return count
    
    def _eliminar_ubicaciones_departamento(self, ubicaciones: List) -> int:
        """Eliminar ubicaciones del departamento"""
        count = len(ubicaciones)
        for ubicacion in ubicaciones:
            db.session.delete(ubicacion)
        
        print(f"   ✅ Ubicaciones eliminadas: {count}")
        return count
    
    def _eliminar_configuracion_departamento(self, departamento_codigo: str) -> bool:
        """Eliminar configuración del departamento"""
        config = DepartamentoConfig.query.filter_by(
            departamento_codigo=departamento_codigo
        ).first()
        
        if config:
            db.session.delete(config)
            print(f"   ✅ Configuración eliminada: {config.departamento_nombre}")
            return True
        else:
            print("   ℹ️  No se encontró configuración para eliminar")
            return False
    
    def _obtener_estadisticas_departamento(self, departamento_codigo: str) -> Dict:
        """Obtener estadísticas de un departamento específico"""
        ubicaciones = Location.query.filter_by(
            departamento_codigo=departamento_codigo
        ).count()
        
        ubicaciones_ids = [loc.id for loc in Location.query.filter_by(
            departamento_codigo=departamento_codigo
        ).all()]
        
        usuarios = 0
        if ubicaciones_ids:
            usuarios = User.query.filter(
                User.ubicacion_id.in_(ubicaciones_ids)
            ).count()
        
        return {
            'ubicaciones': ubicaciones,
            'usuarios': usuarios
        }
    
    def _obtener_estadisticas_sistema(self) -> Dict:
        """Obtener estadísticas generales del sistema"""
        ubicaciones = Location.query.filter_by(activo=True).count()
        usuarios = User.query.filter_by(activo=True).count()
        departamentos_habilitados = DepartamentoConfig.query.filter_by(habilitado=True).count()
        
        return {
            'ubicaciones': ubicaciones,
            'usuarios': usuarios,
            'departamentos_habilitados': departamentos_habilitados
        }


def main():
    """Función principal con menú interactivo"""
    manager = DepartamentosManager()
    
    print("🏛️  GESTOR DE DEPARTAMENTOS ELECTORALES")
    print("=" * 50)
    print()
    
    while True:
        print("OPCIONES DISPONIBLES:")
        print("1. Listar departamentos disponibles en CSV")
        print("2. Ver estado actual de departamentos")
        print("3. Cargar departamento completo")
        print("4. Eliminar departamento completo")
        print("5. Salir")
        print()
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == '1':
            print("\n📋 DEPARTAMENTOS DISPONIBLES EN CSV:")
            print("-" * 50)
            try:
                departamentos = manager.listar_departamentos_disponibles()
                for dept in departamentos:
                    print(f"  {dept['departamento_codigo']} - {dept['departamento_nombre']}")
                    print(f"      Municipios: {dept['total_municipios']}, Registros: {dept['total_registros']}")
                print()
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
        
        elif opcion == '2':
            print("\n📊 ESTADO ACTUAL DE DEPARTAMENTOS:")
            print("-" * 50)
            try:
                estados = manager.obtener_estado_departamentos()
                if not estados:
                    print("  No hay departamentos configurados")
                else:
                    for estado in estados:
                        status = "HABILITADO" if estado['habilitado'] else "DESHABILITADO"
                        principal = " (PRINCIPAL)" if estado['es_principal'] else ""
                        print(f"  {estado['departamento_codigo']} - {estado['departamento_nombre']} - {status}{principal}")
                        print(f"      Municipios: {estado['total_municipios']}, Puestos: {estado['total_puestos']}, Mesas: {estado['total_mesas']}")
                        print(f"      Usuarios: {estado['total_usuarios_creados']}")
                print()
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
        
        elif opcion == '3':
            print("\n📥 CARGAR DEPARTAMENTO COMPLETO:")
            print("-" * 50)
            codigo = input("Ingrese el código del departamento (ej: 26 para Quindío): ").strip()
            if not codigo:
                print("❌ Código requerido")
                print()
                continue
            
            principal = input("¿Marcar como departamento principal? (s/N): ").strip().lower()
            es_principal = principal in ['s', 'si', 'sí', 'y', 'yes']
            
            try:
                resultado = manager.cargar_departamento_completo(codigo, es_principal)
                print("🎉 ¡Departamento cargado exitosamente!")
                print()
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
        
        elif opcion == '4':
            print("\n🗑️  ELIMINAR DEPARTAMENTO COMPLETO:")
            print("-" * 50)
            print("⚠️  ADVERTENCIA: Esta acción eliminará TODOS los datos del departamento:")
            print("   - Ubicaciones (departamento, municipios, zonas, puestos, mesas)")
            print("   - Usuarios (coordinadores y testigos)")
            print("   - Formularios E-14 y votos")
            print("   - Reportes de participación")
            print("   - Incidentes y delitos electorales")
            print("   - Evidencias fotográficas")
            print("   - Configuración del departamento")
            print()
            print("🚨 ESTA ACCIÓN NO SE PUEDE DESHACER")
            print()
            
            codigo = input("Ingrese el código del departamento a eliminar: ").strip()
            if not codigo:
                print("❌ Código requerido")
                print()
                continue
            
            confirmacion = input(f"Escriba 'ELIMINAR {codigo}' para confirmar: ").strip()
            if confirmacion != f'ELIMINAR {codigo}':
                print("❌ Eliminación cancelada")
                print()
                continue
            
            try:
                resultado = manager.eliminar_departamento_completo(codigo, confirmar=True)
                if resultado['eliminado']:
                    print("🎯 ¡Departamento eliminado exitosamente!")
                else:
                    print(f"ℹ️  {resultado['motivo']}")
                print()
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
        
        elif opcion == '5':
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida")
            print()


if __name__ == '__main__':
    main()