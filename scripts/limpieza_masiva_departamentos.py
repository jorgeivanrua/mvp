#!/usr/bin/env python3
"""
Sistema de limpieza masiva de departamentos
Permite eliminar múltiples departamentos o limpiar completamente el sistema

Uso:
    python scripts/limpieza_masiva_departamentos.py --todos-excepto 26
    python scripts/limpieza_masiva_departamentos.py --limpiar-todo
    python scripts/limpieza_masiva_departamentos.py --departamentos 44,05,76
    python scripts/limpieza_masiva_departamentos.py --inactivos
    
Ejemplos:
    # Eliminar todos excepto Quindío
    python scripts/limpieza_masiva_departamentos.py --todos-excepto 26 --confirmar
    
    # Limpiar sistema completo
    python scripts/limpieza_masiva_departamentos.py --limpiar-todo --confirmar
    
    # Eliminar departamentos específicos
    python scripts/limpieza_masiva_departamentos.py --departamentos 44,05,76 --confirmar
"""
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from scripts.eliminar_departamento_completo import EliminadorDepartamentoCompleto
    from backend.app import create_app
    from backend.database import db
    from backend.models.departamento_config import DepartamentoConfig
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class LimpiadorMasivoDepartamentos:
    """Limpiador masivo para múltiples departamentos"""
    
    def __init__(self):
        self.eliminador = EliminadorDepartamentoCompleto()
        self.app = create_app()
    
    def eliminar_todos_excepto(self, departamentos_preservar: List[str]) -> Dict:
        """
        Eliminar todos los departamentos excepto los especificados
        
        Args:
            departamentos_preservar: Lista de códigos de departamentos a preservar
        """
        print("=" * 80)
        print("🧹 ELIMINACIÓN MASIVA - TODOS EXCEPTO ESPECIFICADOS")
        print("=" * 80)
        
        with self.app.app_context():
            # Obtener todos los departamentos configurados
            departamentos_configurados = self.eliminador.listar_departamentos_configurados()
            
            if not departamentos_configurados:
                print("ℹ️  No hay departamentos configurados para eliminar")
                return {'eliminados': 0, 'preservados': 0, 'errores': 0}
            
            # Filtrar departamentos a eliminar
            departamentos_eliminar = [
                dept for dept in departamentos_configurados 
                if dept['departamento_codigo'] not in departamentos_preservar
            ]
            
            departamentos_preservados = [
                dept for dept in departamentos_configurados 
                if dept['departamento_codigo'] in departamentos_preservar
            ]
            
            print(f"📊 ANÁLISIS:")
            print(f"   • Total configurados: {len(departamentos_configurados)}")
            print(f"   • A eliminar: {len(departamentos_eliminar)}")
            print(f"   • A preservar: {len(departamentos_preservados)}")
            print()
            
            if departamentos_preservados:
                print(f"🛡️  DEPARTAMENTOS A PRESERVAR:")
                for dept in departamentos_preservados:
                    principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                    print(f"   • {dept['departamento_codigo']} - {dept['departamento_nombre']}{principal}")
                print()
            
            if not departamentos_eliminar:
                print("ℹ️  No hay departamentos para eliminar")
                return {'eliminados': 0, 'preservados': len(departamentos_preservados), 'errores': 0}
            
            print(f"🗑️  DEPARTAMENTOS A ELIMINAR:")
            for dept in departamentos_eliminar:
                principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                print(f"   • {dept['departamento_codigo']} - {dept['departamento_nombre']}{principal}")
                print(f"     📊 {dept['total_ubicaciones']} ubicaciones, {dept['total_usuarios']} usuarios")
            print()
            
            # Confirmar operación
            if not self._confirmar_eliminacion_masiva(departamentos_eliminar, "TODOS EXCEPTO"):
                return {'eliminados': 0, 'preservados': len(departamentos_preservados), 'errores': 0, 'cancelado': True}
            
            # Proceder con eliminaciones
            return self._ejecutar_eliminaciones_masivas(departamentos_eliminar, departamentos_preservados)
    
    def eliminar_departamentos_especificos(self, codigos_departamentos: List[str]) -> Dict:
        """
        Eliminar departamentos específicos por código
        
        Args:
            codigos_departamentos: Lista de códigos de departamentos a eliminar
        """
        print("=" * 80)
        print("🗑️  ELIMINACIÓN MASIVA - DEPARTAMENTOS ESPECÍFICOS")
        print("=" * 80)
        
        with self.app.app_context():
            # Obtener departamentos configurados
            departamentos_configurados = self.eliminador.listar_departamentos_configurados()
            
            # Filtrar departamentos a eliminar
            departamentos_eliminar = [
                dept for dept in departamentos_configurados 
                if dept['departamento_codigo'] in codigos_departamentos
            ]
            
            codigos_no_encontrados = [
                codigo for codigo in codigos_departamentos
                if not any(dept['departamento_codigo'] == codigo for dept in departamentos_configurados)
            ]
            
            departamentos_preservados = [
                dept for dept in departamentos_configurados 
                if dept['departamento_codigo'] not in codigos_departamentos
            ]
            
            print(f"📊 ANÁLISIS:")
            print(f"   • Solicitados para eliminar: {len(codigos_departamentos)}")
            print(f"   • Encontrados para eliminar: {len(departamentos_eliminar)}")
            print(f"   • No encontrados: {len(codigos_no_encontrados)}")
            print(f"   • Permanecerán: {len(departamentos_preservados)}")
            print()
            
            if codigos_no_encontrados:
                print(f"⚠️  CÓDIGOS NO ENCONTRADOS:")
                for codigo in codigos_no_encontrados:
                    print(f"   • {codigo}")
                print()
            
            if not departamentos_eliminar:
                print("ℹ️  No hay departamentos válidos para eliminar")
                return {'eliminados': 0, 'preservados': len(departamentos_preservados), 'errores': len(codigos_no_encontrados)}
            
            print(f"🗑️  DEPARTAMENTOS A ELIMINAR:")
            for dept in departamentos_eliminar:
                principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                print(f"   • {dept['departamento_codigo']} - {dept['departamento_nombre']}{principal}")
                print(f"     📊 {dept['total_ubicaciones']} ubicaciones, {dept['total_usuarios']} usuarios")
            print()
            
            # Confirmar operación
            if not self._confirmar_eliminacion_masiva(departamentos_eliminar, "ESPECÍFICOS"):
                return {'eliminados': 0, 'preservados': len(departamentos_preservados), 'errores': 0, 'cancelado': True}
            
            # Proceder con eliminaciones
            return self._ejecutar_eliminaciones_masivas(departamentos_eliminar, departamentos_preservados)
    
    def eliminar_departamentos_inactivos(self) -> Dict:
        """Eliminar todos los departamentos deshabilitados/inactivos"""
        print("=" * 80)
        print("🧹 ELIMINACIÓN MASIVA - DEPARTAMENTOS INACTIVOS")
        print("=" * 80)
        
        with self.app.app_context():
            # Obtener departamentos configurados
            departamentos_configurados = self.eliminador.listar_departamentos_configurados()
            
            # Filtrar departamentos inactivos
            departamentos_eliminar = [
                dept for dept in departamentos_configurados 
                if not dept['habilitado']
            ]
            
            departamentos_activos = [
                dept for dept in departamentos_configurados 
                if dept['habilitado']
            ]
            
            print(f"📊 ANÁLISIS:")
            print(f"   • Total configurados: {len(departamentos_configurados)}")
            print(f"   • Inactivos (a eliminar): {len(departamentos_eliminar)}")
            print(f"   • Activos (a preservar): {len(departamentos_activos)}")
            print()
            
            if not departamentos_eliminar:
                print("ℹ️  No hay departamentos inactivos para eliminar")
                return {'eliminados': 0, 'preservados': len(departamentos_activos), 'errores': 0}
            
            print(f"🗑️  DEPARTAMENTOS INACTIVOS A ELIMINAR:")
            for dept in departamentos_eliminar:
                print(f"   • {dept['departamento_codigo']} - {dept['departamento_nombre']} (DESHABILITADO)")
                print(f"     📊 {dept['total_ubicaciones']} ubicaciones, {dept['total_usuarios']} usuarios")
            print()
            
            if departamentos_activos:
                print(f"🛡️  DEPARTAMENTOS ACTIVOS A PRESERVAR:")
                for dept in departamentos_activos:
                    principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                    print(f"   • {dept['departamento_codigo']} - {dept['departamento_nombre']}{principal}")
                print()
            
            # Confirmar operación
            if not self._confirmar_eliminacion_masiva(departamentos_eliminar, "INACTIVOS"):
                return {'eliminados': 0, 'preservados': len(departamentos_activos), 'errores': 0, 'cancelado': True}
            
            # Proceder con eliminaciones
            return self._ejecutar_eliminaciones_masivas(departamentos_eliminar, departamentos_activos)
    
    def limpiar_sistema_completo(self) -> Dict:
        """Eliminar TODOS los departamentos del sistema (limpieza total)"""
        print("=" * 80)
        print("💀 LIMPIEZA TOTAL DEL SISTEMA")
        print("=" * 80)
        print()
        print("🚨 ADVERTENCIA CRÍTICA:")
        print("Esta operación eliminará TODOS los departamentos y TODOS los datos del sistema")
        print("Esto incluye:")
        print("   - Todos los departamentos configurados")
        print("   - Todas las ubicaciones")
        print("   - Todos los usuarios (excepto super admin)")
        print("   - Todos los formularios y votos")
        print("   - Todos los reportes")
        print("   - Todos los incidentes y delitos")
        print("   - Todas las evidencias fotográficas")
        print()
        print("💀 ESTA ACCIÓN DEJARÁ EL SISTEMA COMPLETAMENTE VACÍO")
        print("🚨 NO SE PUEDE DESHACER")
        print()
        
        with self.app.app_context():
            # Obtener todos los departamentos
            departamentos_configurados = self.eliminador.listar_departamentos_configurados()
            
            if not departamentos_configurados:
                print("ℹ️  No hay departamentos configurados - sistema ya está limpio")
                return {'eliminados': 0, 'preservados': 0, 'errores': 0}
            
            print(f"🗑️  SE ELIMINARÁN {len(departamentos_configurados)} DEPARTAMENTOS:")
            total_ubicaciones = 0
            total_usuarios = 0
            
            for dept in departamentos_configurados:
                principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                print(f"   • {dept['departamento_codigo']} - {dept['departamento_nombre']}{principal}")
                print(f"     📊 {dept['total_ubicaciones']} ubicaciones, {dept['total_usuarios']} usuarios")
                total_ubicaciones += dept['total_ubicaciones']
                total_usuarios += dept['total_usuarios']
            
            print()
            print(f"📊 TOTALES A ELIMINAR:")
            print(f"   • {len(departamentos_configurados)} departamentos")
            print(f"   • {total_ubicaciones} ubicaciones")
            print(f"   • {total_usuarios} usuarios")
            print()
            
            # Confirmaciones extremas para limpieza total
            if not self._confirmar_limpieza_total():
                return {'eliminados': 0, 'preservados': len(departamentos_configurados), 'errores': 0, 'cancelado': True}
            
            # Proceder con eliminación total
            return self._ejecutar_eliminaciones_masivas(departamentos_configurados, [])
    
    def _confirmar_eliminacion_masiva(self, departamentos_eliminar: List[Dict], tipo_operacion: str) -> bool:
        """Confirmar eliminación masiva con el usuario"""
        print(f"⚠️  CONFIRMACIÓN REQUERIDA PARA ELIMINACIÓN MASIVA")
        print(f"Tipo de operación: {tipo_operacion}")
        print(f"Departamentos a eliminar: {len(departamentos_eliminar)}")
        print()
        
        # Verificar si hay departamento principal
        principales = [dept for dept in departamentos_eliminar if dept['es_principal']]
        if principales:
            print(f"🚨 ADVERTENCIA: Se eliminará el departamento PRINCIPAL:")
            for dept in principales:
                print(f"   ⭐ {dept['departamento_codigo']} - {dept['departamento_nombre']}")
            print()
        
        print(f"🚨 ESTA ACCIÓN NO SE PUEDE DESHACER")
        print(f"🚨 TODOS LOS DATOS SE PERDERÁN PERMANENTEMENTE")
        print()
        
        # Primera confirmación
        respuesta1 = input(f"Escriba 'ELIMINAR {tipo_operacion}' para continuar: ").strip()
        if respuesta1 != f'ELIMINAR {tipo_operacion}':
            return False
        
        # Segunda confirmación
        respuesta2 = input("¿Está COMPLETAMENTE seguro? (escriba 'SI ELIMINAR MASIVO'): ").strip()
        if respuesta2 != 'SI ELIMINAR MASIVO':
            return False
        
        # Tercera confirmación si hay departamento principal
        if principales:
            respuesta3 = input("¡SE ELIMINARÁ EL PRINCIPAL! Escriba 'CONFIRMO ELIMINAR PRINCIPAL': ").strip()
            if respuesta3 != 'CONFIRMO ELIMINAR PRINCIPAL':
                return False
        
        return True
    
    def _confirmar_limpieza_total(self) -> bool:
        """Confirmaciones extremas para limpieza total del sistema"""
        print(f"💀 CONFIRMACIONES PARA LIMPIEZA TOTAL DEL SISTEMA")
        print()
        
        # Primera confirmación
        respuesta1 = input("Escriba 'LIMPIAR SISTEMA COMPLETO' para continuar: ").strip()
        if respuesta1 != 'LIMPIAR SISTEMA COMPLETO':
            return False
        
        # Segunda confirmación
        respuesta2 = input("¿Está COMPLETAMENTE seguro? (escriba 'SI ELIMINAR TODO'): ").strip()
        if respuesta2 != 'SI ELIMINAR TODO':
            return False
        
        # Tercera confirmación
        respuesta3 = input("ÚLTIMA CONFIRMACIÓN - Escriba 'CONFIRMO ELIMINACION TOTAL': ").strip()
        if respuesta3 != 'CONFIRMO ELIMINACION TOTAL':
            return False
        
        # Cuarta confirmación con timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        respuesta4 = input(f"Escriba el timestamp actual '{timestamp}' para proceder: ").strip()
        if respuesta4 != timestamp:
            return False
        
        return True
    
    def _ejecutar_eliminaciones_masivas(self, departamentos_eliminar: List[Dict], departamentos_preservados: List[Dict]) -> Dict:
        """Ejecutar las eliminaciones masivas"""
        print(f"\n🚀 INICIANDO ELIMINACIONES MASIVAS")
        print("=" * 60)
        
        resultados = {
            'eliminados': 0,
            'errores': 0,
            'preservados': len(departamentos_preservados),
            'detalles': [],
            'timestamp_inicio': datetime.utcnow().isoformat(),
            'timestamp_fin': None
        }
        
        for i, dept in enumerate(departamentos_eliminar, 1):
            codigo = dept['departamento_codigo']
            nombre = dept['departamento_nombre']
            
            print(f"\n🗑️  [{i}/{len(departamentos_eliminar)}] Eliminando {nombre} ({codigo})")
            print("-" * 50)
            
            try:
                resultado = self.eliminador.eliminar_departamento_completo(
                    departamento_codigo=codigo,
                    forzar=True  # Forzar para evitar confirmaciones individuales
                )
                
                if resultado['eliminado']:
                    resultados['eliminados'] += 1
                    print(f"   ✅ {nombre} eliminado exitosamente")
                    
                    resultados['detalles'].append({
                        'codigo': codigo,
                        'nombre': nombre,
                        'exitoso': True,
                        'ubicaciones_eliminadas': resultado['ubicaciones_eliminadas']['total'],
                        'usuarios_eliminados': resultado['usuarios_eliminados']['total']
                    })
                else:
                    resultados['errores'] += 1
                    print(f"   ❌ Error eliminando {nombre}: {resultado.get('motivo')}")
                    
                    resultados['detalles'].append({
                        'codigo': codigo,
                        'nombre': nombre,
                        'exitoso': False,
                        'error': resultado.get('motivo')
                    })
                
            except Exception as e:
                resultados['errores'] += 1
                print(f"   ❌ Excepción eliminando {nombre}: {str(e)}")
                
                resultados['detalles'].append({
                    'codigo': codigo,
                    'nombre': nombre,
                    'exitoso': False,
                    'error': str(e)
                })
        
        resultados['timestamp_fin'] = datetime.utcnow().isoformat()
        
        # Mostrar resumen final
        self._mostrar_resumen_eliminacion_masiva(resultados)
        
        return resultados
    
    def _mostrar_resumen_eliminacion_masiva(self, resultados: Dict):
        """Mostrar resumen de eliminación masiva"""
        print(f"\n" + "=" * 80)
        print("🎯 RESUMEN DE ELIMINACIÓN MASIVA")
        print("=" * 80)
        
        print(f"📊 ESTADÍSTICAS:")
        print(f"   • Departamentos eliminados: {resultados['eliminados']}")
        print(f"   • Errores: {resultados['errores']}")
        print(f"   • Preservados: {resultados['preservados']}")
        print(f"   • Total procesados: {len(resultados['detalles'])}")
        
        inicio = datetime.fromisoformat(resultados['timestamp_inicio'])
        fin = datetime.fromisoformat(resultados['timestamp_fin'])
        duracion = (fin - inicio).total_seconds()
        print(f"   • Duración: {duracion:.1f} segundos")
        print()
        
        # Mostrar exitosos
        exitosos = [d for d in resultados['detalles'] if d['exitoso']]
        if exitosos:
            print(f"✅ ELIMINACIONES EXITOSAS ({len(exitosos)}):")
            for detalle in exitosos:
                print(f"   • {detalle['codigo']} - {detalle['nombre']}")
                print(f"     📊 {detalle['ubicaciones_eliminadas']} ubicaciones, {detalle['usuarios_eliminados']} usuarios")
            print()
        
        # Mostrar errores
        errores = [d for d in resultados['detalles'] if not d['exitoso']]
        if errores:
            print(f"❌ ERRORES ({len(errores)}):")
            for detalle in errores:
                print(f"   • {detalle['codigo']} - {detalle['nombre']}")
                print(f"     Error: {detalle['error']}")
            print()
        
        if resultados['eliminados'] == len(resultados['detalles']) and resultados['errores'] == 0:
            print("🎉 ELIMINACIÓN MASIVA COMPLETAMENTE EXITOSA")
        elif resultados['eliminados'] > 0:
            print("⚠️  ELIMINACIÓN MASIVA PARCIALMENTE EXITOSA")
        else:
            print("❌ ELIMINACIÓN MASIVA FALLÓ")
        
        print("=" * 80)


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Limpieza masiva de departamentos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Listar departamentos configurados
  python scripts/limpieza_masiva_departamentos.py --listar
  
  # Eliminar todos excepto Quindío
  python scripts/limpieza_masiva_departamentos.py --todos-excepto 26 --confirmar
  
  # Eliminar departamentos específicos
  python scripts/limpieza_masiva_departamentos.py --departamentos 44,05,76 --confirmar
  
  # Eliminar solo los inactivos
  python scripts/limpieza_masiva_departamentos.py --inactivos --confirmar
  
  # Limpiar sistema completo (PELIGROSO)
  python scripts/limpieza_masiva_departamentos.py --limpiar-todo --confirmar
        """
    )
    
    parser.add_argument('--listar', action='store_true',
                       help='Listar departamentos configurados')
    parser.add_argument('--todos-excepto', metavar='CODIGOS',
                       help='Eliminar todos excepto los códigos especificados (separados por coma)')
    parser.add_argument('--departamentos', metavar='CODIGOS',
                       help='Eliminar departamentos específicos (códigos separados por coma)')
    parser.add_argument('--inactivos', action='store_true',
                       help='Eliminar solo departamentos deshabilitados/inactivos')
    parser.add_argument('--limpiar-todo', action='store_true',
                       help='PELIGROSO: Eliminar TODOS los departamentos del sistema')
    parser.add_argument('--confirmar', action='store_true',
                       help='Confirmar que desea proceder con la eliminación masiva')
    
    args = parser.parse_args()
    
    limpiador = LimpiadorMasivoDepartamentos()
    
    try:
        # Listar departamentos
        if args.listar:
            print("📊 DEPARTAMENTOS CONFIGURADOS")
            print("=" * 50)
            
            departamentos = limpiador.eliminador.listar_departamentos_configurados()
            
            if not departamentos:
                print("ℹ️  No hay departamentos configurados")
                return
            
            for dept in departamentos:
                status = "🟢 HABILITADO" if dept['habilitado'] else "🔴 DESHABILITADO"
                principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                
                print(f"📍 {dept['departamento_codigo']} - {dept['departamento_nombre']}")
                print(f"   Estado: {status}{principal}")
                print(f"   📊 {dept['total_ubicaciones']} ubicaciones, {dept['total_usuarios']} usuarios")
                print()
            
            print("💡 Use las opciones de eliminación con --confirmar para proceder")
            return
        
        # Validar que se especificó --confirmar para operaciones destructivas
        operaciones_destructivas = [args.todos_excepto, args.departamentos, args.inactivos, args.limpiar_todo]
        if any(operaciones_destructivas) and not args.confirmar:
            print("❌ Debe usar --confirmar para operaciones de eliminación masiva")
            print("💡 Esta es una medida de seguridad para evitar eliminaciones accidentales")
            sys.exit(1)
        
        # Eliminar todos excepto especificados
        if args.todos_excepto:
            codigos_preservar = [codigo.strip().zfill(2) for codigo in args.todos_excepto.split(',')]
            resultado = limpiador.eliminar_todos_excepto(codigos_preservar)
            
            if resultado.get('cancelado'):
                print("ℹ️  Operación cancelada por el usuario")
                sys.exit(0)
            elif resultado['eliminados'] > 0:
                print(f"\n🎯 Eliminación masiva completada: {resultado['eliminados']} departamentos eliminados")
                sys.exit(0)
            else:
                print(f"\n❌ No se eliminaron departamentos")
                sys.exit(1)
        
        # Eliminar departamentos específicos
        elif args.departamentos:
            codigos_eliminar = [codigo.strip().zfill(2) for codigo in args.departamentos.split(',')]
            resultado = limpiador.eliminar_departamentos_especificos(codigos_eliminar)
            
            if resultado.get('cancelado'):
                print("ℹ️  Operación cancelada por el usuario")
                sys.exit(0)
            elif resultado['eliminados'] > 0:
                print(f"\n🎯 Eliminación específica completada: {resultado['eliminados']} departamentos eliminados")
                sys.exit(0)
            else:
                print(f"\n❌ No se eliminaron departamentos")
                sys.exit(1)
        
        # Eliminar inactivos
        elif args.inactivos:
            resultado = limpiador.eliminar_departamentos_inactivos()
            
            if resultado.get('cancelado'):
                print("ℹ️  Operación cancelada por el usuario")
                sys.exit(0)
            elif resultado['eliminados'] > 0:
                print(f"\n🎯 Limpieza de inactivos completada: {resultado['eliminados']} departamentos eliminados")
                sys.exit(0)
            else:
                print(f"\n❌ No se eliminaron departamentos inactivos")
                sys.exit(1)
        
        # Limpiar todo
        elif args.limpiar_todo:
            resultado = limpiador.limpiar_sistema_completo()
            
            if resultado.get('cancelado'):
                print("ℹ️  Operación cancelada por el usuario")
                sys.exit(0)
            elif resultado['eliminados'] > 0:
                print(f"\n🎯 Limpieza total completada: {resultado['eliminados']} departamentos eliminados")
                print("💀 SISTEMA COMPLETAMENTE LIMPIO")
                sys.exit(0)
            else:
                print(f"\n❌ No se pudo completar la limpieza total")
                sys.exit(1)
        
        else:
            print("❌ Debe especificar una operación")
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