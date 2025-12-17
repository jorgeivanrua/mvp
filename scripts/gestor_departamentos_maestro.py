#!/usr/bin/env python3
"""
Gestor Maestro de Departamentos - Sistema Electoral
Herramienta unificada para gestionar cualquier departamento de Colombia

Funcionalidades:
- Listar departamentos disponibles
- Cargar departamentos completos
- Verificar estado y funcionalidad
- Eliminar departamentos
- Gestión de departamento principal

Uso:
    python scripts/gestor_departamentos_maestro.py
    
O con argumentos directos:
    python scripts/gestor_departamentos_maestro.py --listar
    python scripts/gestor_departamentos_maestro.py --cargar 26 --principal
    python scripts/gestor_departamentos_maestro.py --verificar 26
    python scripts/gestor_departamentos_maestro.py --eliminar 44 --confirmar
"""
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from scripts.departamentos_manager import DepartamentosManager
    from scripts.cargar_departamento_completo import CargadorDepartamentoCompleto
    from scripts.verificar_departamento import VerificadorDepartamento
    from scripts.eliminar_departamento_completo import EliminadorDepartamentoCompleto
    from scripts.limpieza_masiva_departamentos import LimpiadorMasivoDepartamentos
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class GestorDepartamentosMaestro:
    """Gestor maestro unificado para todos los departamentos"""
    
    def __init__(self):
        self.manager = DepartamentosManager()
        self.cargador = CargadorDepartamentoCompleto()
        self.verificador = VerificadorDepartamento()
        self.eliminador = EliminadorDepartamentoCompleto()
        self.limpiador = LimpiadorMasivoDepartamentos()
    
    def mostrar_menu_principal(self):
        """Mostrar menú principal interactivo"""
        while True:
            print("\n" + "=" * 80)
            print("🏛️  GESTOR MAESTRO DE DEPARTAMENTOS - SISTEMA ELECTORAL")
            print("=" * 80)
            print()
            print("OPCIONES DISPONIBLES:")
            print()
            print("📋 CONSULTA:")
            print("  1. Listar departamentos disponibles en Colombia")
            print("  2. Ver estado actual de departamentos configurados")
            print("  3. Verificar departamento específico")
            print("  4. Verificar todos los departamentos")
            print()
            print("⚙️  GESTIÓN:")
            print("  5. Cargar departamento completo")
            print("  6. Eliminar departamento específico")
            print("  7. Cambiar departamento principal")
            print()
            print("🔧 MANTENIMIENTO:")
            print("  8. Reparar departamento (recarga forzada)")
            print("  9. Eliminación masiva de departamentos")
            print(" 10. Limpiar sistema completo (eliminar todo)")
            print()
            print("❌ SALIR:")
            print("  0. Salir del sistema")
            print()
            
            try:
                opcion = input("Seleccione una opción (0-10): ").strip()
                
                if opcion == '0':
                    print("\n👋 ¡Hasta luego!")
                    break
                elif opcion == '1':
                    self.listar_departamentos_disponibles()
                elif opcion == '2':
                    self.mostrar_estado_departamentos()
                elif opcion == '3':
                    self.verificar_departamento_interactivo()
                elif opcion == '4':
                    self.verificar_todos_departamentos()
                elif opcion == '5':
                    self.cargar_departamento_interactivo()
                elif opcion == '6':
                    self.eliminar_departamento_interactivo()
                elif opcion == '7':
                    self.cambiar_departamento_principal()
                elif opcion == '8':
                    self.reparar_departamento_interactivo()
                elif opcion == '9':
                    self.eliminacion_masiva_departamentos()
                elif opcion == '10':
                    self.limpiar_sistema_completo()
                else:
                    print("❌ Opción inválida. Seleccione un número del 0 al 10.")
                
                if opcion != '0':
                    input("\nPresione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\nPresione Enter para continuar...")
    
    def listar_departamentos_disponibles(self):
        """Listar todos los departamentos disponibles"""
        print("\n📋 DEPARTAMENTOS DISPONIBLES EN COLOMBIA")
        print("=" * 60)
        
        try:
            departamentos = self.cargador.listar_departamentos_disponibles()
            
            if not departamentos:
                print("❌ No se pudieron cargar los departamentos")
                return
            
            print(f"📊 Total: {len(departamentos)} departamentos")
            print()
            
            for i, dept in enumerate(departamentos, 1):
                print(f"{i:2d}. {dept['departamento_codigo']} - {dept['departamento_nombre']}")
                print(f"     📊 {dept['total_municipios']} municipios, {dept['total_puestos']} puestos, {dept['total_mesas']} mesas")
            
            print()
            print("💡 Cualquiera de estos departamentos puede ser cargado en el sistema")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def mostrar_estado_departamentos(self):
        """Mostrar estado actual de departamentos configurados"""
        print("\n📊 ESTADO ACTUAL DE DEPARTAMENTOS CONFIGURADOS")
        print("=" * 60)
        
        try:
            estados = self.manager.obtener_estado_departamentos()
            
            if not estados:
                print("ℹ️  No hay departamentos configurados en el sistema")
                print("💡 Use la opción 5 para cargar un departamento")
                return
            
            print(f"📈 Total configurados: {len(estados)}")
            print()
            
            for estado in estados:
                status = "🟢 HABILITADO" if estado['habilitado'] else "🔴 DESHABILITADO"
                principal = " ⭐ PRINCIPAL" if estado['es_principal'] else ""
                
                print(f"📍 {estado['departamento_codigo']} - {estado['departamento_nombre']}")
                print(f"   Estado: {status}{principal}")
                print(f"   📊 {estado['total_municipios']} municipios, {estado['total_puestos']} puestos, {estado['total_mesas']} mesas")
                print(f"   👥 {estado['total_usuarios_creados']} usuarios creados")
                
                if estado['ultima_carga_at']:
                    fecha_carga = datetime.fromisoformat(estado['ultima_carga_at']).strftime('%Y-%m-%d %H:%M')
                    print(f"   🕒 Última carga: {fecha_carga}")
                print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def verificar_departamento_interactivo(self):
        """Verificar un departamento específico de forma interactiva"""
        print("\n🔍 VERIFICAR DEPARTAMENTO ESPECÍFICO")
        print("=" * 50)
        
        # Mostrar departamentos configurados
        try:
            estados = self.manager.obtener_estado_departamentos()
            if estados:
                print("Departamentos configurados:")
                for estado in estados:
                    print(f"  {estado['departamento_codigo']} - {estado['departamento_nombre']}")
                print()
        except:
            pass
        
        codigo = input("Ingrese el código del departamento a verificar: ").strip()
        if not codigo:
            print("❌ Código requerido")
            return
        
        codigo = codigo.zfill(2)
        
        try:
            resultado = self.verificador.verificar_departamento_completo(codigo)
            
            if resultado['estado_general'] == 'EXCELENTE':
                print(f"\n🎉 Departamento {codigo} está funcionando perfectamente")
            else:
                print(f"\n⚠️  Departamento {codigo} requiere atención")
                print("💡 Use la opción 8 para reparar el departamento")
                
        except Exception as e:
            print(f"❌ Error verificando departamento: {e}")
    
    def verificar_todos_departamentos(self):
        """Verificar todos los departamentos configurados"""
        print("\n🔍 VERIFICANDO TODOS LOS DEPARTAMENTOS")
        print("=" * 50)
        
        try:
            resultados = self.verificador.verificar_todos_departamentos()
            
            if not resultados:
                print("ℹ️  No hay departamentos para verificar")
                return
            
            # El método ya muestra el resumen completo
            
        except Exception as e:
            print(f"❌ Error verificando departamentos: {e}")
    
    def cargar_departamento_interactivo(self):
        """Cargar un departamento de forma interactiva"""
        print("\n📥 CARGAR DEPARTAMENTO COMPLETO")
        print("=" * 50)
        
        # Mostrar algunos departamentos disponibles
        try:
            departamentos = self.cargador.listar_departamentos_disponibles()
            if departamentos:
                print("Algunos departamentos disponibles:")
                for dept in departamentos[:10]:
                    print(f"  {dept['departamento_codigo']} - {dept['departamento_nombre']}")
                if len(departamentos) > 10:
                    print(f"  ... y {len(departamentos) - 10} más")
                print()
        except:
            pass
        
        codigo = input("Ingrese el código del departamento a cargar: ").strip()
        if not codigo:
            print("❌ Código requerido")
            return
        
        codigo = codigo.zfill(2)
        
        principal = input("¿Marcar como departamento principal? (s/N): ").strip().lower()
        es_principal = principal in ['s', 'si', 'sí', 'y', 'yes']
        
        forzar = input("¿Forzar recarga si ya existe? (s/N): ").strip().lower()
        forzar_recarga = forzar in ['s', 'si', 'sí', 'y', 'yes']
        
        try:
            resultado = self.cargador.cargar_departamento_completo(
                departamento_codigo=codigo,
                es_principal=es_principal,
                forzar=forzar_recarga
            )
            
            if resultado.get('exitoso'):
                print(f"\n🎉 ¡Departamento {codigo} cargado exitosamente!")
                print("💡 Use la opción 3 para verificar que todo esté funcionando")
            elif resultado.get('cancelado'):
                print(f"ℹ️  Carga cancelada: {resultado.get('motivo')}")
                
        except Exception as e:
            print(f"❌ Error cargando departamento: {e}")
    
    def eliminar_departamento_interactivo(self):
        """Eliminar un departamento específico de forma interactiva"""
        print("\n🗑️  ELIMINAR DEPARTAMENTO ESPECÍFICO")
        print("=" * 50)
        
        # Mostrar departamentos configurados
        try:
            departamentos = self.eliminador.listar_departamentos_configurados()
            if departamentos:
                print("Departamentos configurados:")
                for dept in departamentos:
                    status = "🟢" if dept['habilitado'] else "🔴"
                    principal = " ⭐" if dept['es_principal'] else ""
                    print(f"  {dept['departamento_codigo']} - {dept['departamento_nombre']} {status}{principal}")
                    print(f"      📊 {dept['total_ubicaciones']} ubicaciones, {dept['total_usuarios']} usuarios")
                print()
            else:
                print("ℹ️  No hay departamentos configurados para eliminar")
                return
        except Exception as e:
            print(f"❌ Error obteniendo departamentos: {e}")
            return
        
        codigo = input("Ingrese el código del departamento a eliminar (o 'cancelar'): ").strip()
        if not codigo or codigo.lower() in ['cancelar', 'cancel']:
            print("❌ Eliminación cancelada")
            return
        
        codigo = codigo.zfill(2)
        
        # Verificar antes de eliminar
        print(f"\n🔍 Verificando departamento {codigo}...")
        try:
            verificacion = self.eliminador.verificar_antes_eliminacion(codigo)
            
            if not verificacion['existe']:
                print(f"ℹ️  {verificacion['motivo']}")
                return
            
            # Proceder con eliminación
            resultado = self.eliminador.eliminar_departamento_completo(codigo)
            
            if resultado['eliminado']:
                print(f"\n🎯 ¡Departamento {codigo} eliminado exitosamente!")
            else:
                print(f"ℹ️  Eliminación cancelada: {resultado.get('motivo')}")
                
        except Exception as e:
            print(f"❌ Error eliminando departamento: {e}")
    
    def cambiar_departamento_principal(self):
        """Cambiar el departamento principal"""
        print("\n⭐ CAMBIAR DEPARTAMENTO PRINCIPAL")
        print("=" * 50)
        
        try:
            estados = self.manager.obtener_estado_departamentos()
            
            if not estados:
                print("ℹ️  No hay departamentos configurados")
                return
            
            # Mostrar departamentos habilitados
            habilitados = [e for e in estados if e['habilitado']]
            if not habilitados:
                print("ℹ️  No hay departamentos habilitados")
                return
            
            print("Departamentos habilitados:")
            for estado in habilitados:
                principal = " ⭐ ACTUAL PRINCIPAL" if estado['es_principal'] else ""
                print(f"  {estado['departamento_codigo']} - {estado['departamento_nombre']}{principal}")
            print()
            
            codigo = input("Ingrese el código del nuevo departamento principal: ").strip()
            if not codigo:
                print("❌ Código requerido")
                return
            
            codigo = codigo.zfill(2)
            
            # Verificar que existe y está habilitado
            depto_info = next((e for e in habilitados if e['departamento_codigo'] == codigo), None)
            if not depto_info:
                print(f"❌ Departamento {codigo} no encontrado o no está habilitado")
                return
            
            if depto_info['es_principal']:
                print(f"ℹ️  {depto_info['departamento_nombre']} ya es el departamento principal")
                return
            
            # Confirmar cambio
            respuesta = input(f"¿Marcar {depto_info['departamento_nombre']} como principal? (s/N): ").strip().lower()
            if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Cambio cancelado")
                return
            
            # Realizar cambio usando el servicio
            from backend.services.departamento_service import DepartamentoService
            from backend.app import create_app
            
            app = create_app()
            with app.app_context():
                resultado = DepartamentoService.habilitar_departamento(
                    departamento_codigo=codigo,
                    es_principal=True,
                    auto_cargar=False
                )
                
                print(f"\n✅ {depto_info['departamento_nombre']} es ahora el departamento principal")
            
        except Exception as e:
            print(f"❌ Error cambiando departamento principal: {e}")
    
    def reparar_departamento_interactivo(self):
        """Reparar un departamento (recarga forzada)"""
        print("\n🔧 REPARAR DEPARTAMENTO")
        print("=" * 50)
        print("Esta opción recargará completamente el departamento aplicando todas las correcciones")
        print()
        
        # Mostrar departamentos configurados
        try:
            estados = self.manager.obtener_estado_departamentos()
            if estados:
                print("Departamentos configurados:")
                for estado in estados:
                    print(f"  {estado['departamento_codigo']} - {estado['departamento_nombre']}")
                print()
        except:
            pass
        
        codigo = input("Ingrese el código del departamento a reparar: ").strip()
        if not codigo:
            print("❌ Código requerido")
            return
        
        codigo = codigo.zfill(2)
        
        try:
            resultado = self.cargador.cargar_departamento_completo(
                departamento_codigo=codigo,
                es_principal=False,  # Mantener estado actual
                forzar=True
            )
            
            if resultado.get('exitoso'):
                print(f"\n🎉 ¡Departamento {codigo} reparado exitosamente!")
                
                # Verificar automáticamente
                print(f"\n🔍 Verificando reparación...")
                verificacion = self.verificador.verificar_departamento_completo(codigo)
                
                if verificacion['estado_general'] == 'EXCELENTE':
                    print(f"✅ Reparación exitosa - Departamento funcionando perfectamente")
                else:
                    print(f"⚠️  Reparación parcial - Aún hay problemas que requieren atención manual")
                    
        except Exception as e:
            print(f"❌ Error reparando departamento: {e}")
    
    def eliminacion_masiva_departamentos(self):
        """Menú de eliminación masiva de departamentos"""
        print("\n🧹 ELIMINACIÓN MASIVA DE DEPARTAMENTOS")
        print("=" * 50)
        print()
        print("OPCIONES DE ELIMINACIÓN MASIVA:")
        print("1. Eliminar todos excepto uno específico")
        print("2. Eliminar departamentos específicos (lista)")
        print("3. Eliminar solo departamentos inactivos/deshabilitados")
        print("4. Volver al menú principal")
        print()
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == '1':
            self._eliminar_todos_excepto()
        elif opcion == '2':
            self._eliminar_especificos()
        elif opcion == '3':
            self._eliminar_inactivos()
        elif opcion == '4':
            return
        else:
            print("❌ Opción inválida")
    
    def _eliminar_todos_excepto(self):
        """Eliminar todos los departamentos excepto uno específico"""
        print("\n🛡️  ELIMINAR TODOS EXCEPTO UNO")
        print("-" * 40)
        
        # Mostrar departamentos
        try:
            departamentos = self.eliminador.listar_departamentos_configurados()
            if not departamentos:
                print("ℹ️  No hay departamentos configurados")
                return
            
            print("Departamentos configurados:")
            for dept in departamentos:
                principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                print(f"  {dept['departamento_codigo']} - {dept['departamento_nombre']}{principal}")
            print()
            
            codigo_preservar = input("Ingrese el código del departamento a PRESERVAR: ").strip()
            if not codigo_preservar:
                print("❌ Código requerido")
                return
            
            codigo_preservar = codigo_preservar.zfill(2)
            
            # Verificar que existe
            if not any(dept['departamento_codigo'] == codigo_preservar for dept in departamentos):
                print(f"❌ Departamento {codigo_preservar} no encontrado")
                return
            
            resultado = self.limpiador.eliminar_todos_excepto([codigo_preservar])
            
            if resultado.get('cancelado'):
                print("ℹ️  Operación cancelada")
            elif resultado['eliminados'] > 0:
                print(f"\n🎯 Eliminación completada: {resultado['eliminados']} departamentos eliminados")
            else:
                print("ℹ️  No se eliminaron departamentos")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _eliminar_especificos(self):
        """Eliminar departamentos específicos por lista"""
        print("\n📋 ELIMINAR DEPARTAMENTOS ESPECÍFICOS")
        print("-" * 40)
        
        # Mostrar departamentos
        try:
            departamentos = self.eliminador.listar_departamentos_configurados()
            if not departamentos:
                print("ℹ️  No hay departamentos configurados")
                return
            
            print("Departamentos configurados:")
            for dept in departamentos:
                principal = " ⭐ PRINCIPAL" if dept['es_principal'] else ""
                print(f"  {dept['departamento_codigo']} - {dept['departamento_nombre']}{principal}")
            print()
            
            codigos_input = input("Ingrese códigos a eliminar (separados por coma): ").strip()
            if not codigos_input:
                print("❌ Códigos requeridos")
                return
            
            codigos = [codigo.strip().zfill(2) for codigo in codigos_input.split(',')]
            
            resultado = self.limpiador.eliminar_departamentos_especificos(codigos)
            
            if resultado.get('cancelado'):
                print("ℹ️  Operación cancelada")
            elif resultado['eliminados'] > 0:
                print(f"\n🎯 Eliminación completada: {resultado['eliminados']} departamentos eliminados")
            else:
                print("ℹ️  No se eliminaron departamentos")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _eliminar_inactivos(self):
        """Eliminar solo departamentos inactivos"""
        print("\n🔴 ELIMINAR DEPARTAMENTOS INACTIVOS")
        print("-" * 40)
        
        try:
            resultado = self.limpiador.eliminar_departamentos_inactivos()
            
            if resultado.get('cancelado'):
                print("ℹ️  Operación cancelada")
            elif resultado['eliminados'] > 0:
                print(f"\n🎯 Limpieza completada: {resultado['eliminados']} departamentos inactivos eliminados")
            else:
                print("ℹ️  No hay departamentos inactivos para eliminar")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def limpiar_sistema_completo(self):
        """Limpiar completamente el sistema (eliminar todos los departamentos)"""
        print("\n💀 LIMPIAR SISTEMA COMPLETO")
        print("=" * 50)
        
        try:
            resultado = self.limpiador.limpiar_sistema_completo()
            
            if resultado.get('cancelado'):
                print("ℹ️  Operación cancelada")
            elif resultado['eliminados'] > 0:
                print(f"\n🎯 Limpieza total completada: {resultado['eliminados']} departamentos eliminados")
                print("💀 SISTEMA COMPLETAMENTE LIMPIO")
            else:
                print("ℹ️  Sistema ya estaba limpio o no se pudo completar la limpieza")
                
        except Exception as e:
            print(f"❌ Error durante la limpieza total: {e}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Gestor Maestro de Departamentos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/gestor_departamentos_maestro.py                    # Modo interactivo
  python scripts/gestor_departamentos_maestro.py --listar          # Listar disponibles
  python scripts/gestor_departamentos_maestro.py --cargar 26 --principal  # Cargar Quindío
  python scripts/gestor_departamentos_maestro.py --verificar 26    # Verificar Quindío
  python scripts/gestor_departamentos_maestro.py --eliminar 44 --confirmar  # Eliminar Caquetá
        """
    )
    
    parser.add_argument('--listar', action='store_true',
                       help='Listar departamentos disponibles')
    parser.add_argument('--estado', action='store_true',
                       help='Mostrar estado de departamentos configurados')
    parser.add_argument('--cargar', metavar='CODIGO',
                       help='Cargar departamento por código')
    parser.add_argument('--verificar', metavar='CODIGO',
                       help='Verificar departamento por código')
    parser.add_argument('--eliminar', metavar='CODIGO',
                       help='Eliminar departamento por código')
    parser.add_argument('--principal', action='store_true',
                       help='Marcar como principal (usar con --cargar)')
    parser.add_argument('--forzar', action='store_true',
                       help='Forzar operación (usar con --cargar)')
    parser.add_argument('--confirmar', action='store_true',
                       help='Confirmar operación (usar con --eliminar)')
    
    args = parser.parse_args()
    
    gestor = GestorDepartamentosMaestro()
    
    try:
        # Modo no interactivo
        if any([args.listar, args.estado, args.cargar, args.verificar, args.eliminar]):
            
            if args.listar:
                gestor.listar_departamentos_disponibles()
            
            elif args.estado:
                gestor.mostrar_estado_departamentos()
            
            elif args.cargar:
                codigo = args.cargar.strip().zfill(2)
                resultado = gestor.cargador.cargar_departamento_completo(
                    departamento_codigo=codigo,
                    es_principal=args.principal,
                    forzar=args.forzar
                )
                
                if resultado.get('exitoso'):
                    print(f"\n🎉 Departamento {codigo} cargado exitosamente")
                    sys.exit(0)
                else:
                    print(f"\n❌ Error cargando departamento {codigo}")
                    sys.exit(1)
            
            elif args.verificar:
                codigo = args.verificar.strip().zfill(2)
                resultado = gestor.verificador.verificar_departamento_completo(codigo)
                
                if resultado['estado_general'] == 'EXCELENTE':
                    print(f"\n✅ Departamento {codigo} funcionando perfectamente")
                    sys.exit(0)
                else:
                    print(f"\n⚠️  Departamento {codigo} requiere atención")
                    sys.exit(1)
            
            elif args.eliminar:
                if not args.confirmar:
                    print("❌ Debe usar --confirmar para eliminar un departamento")
                    sys.exit(1)
                
                codigo = args.eliminar.strip().zfill(2)
                resultado = gestor.manager.eliminar_departamento_completo(codigo, confirmar=True)
                
                if resultado['eliminado']:
                    print(f"\n✅ Departamento {codigo} eliminado exitosamente")
                    sys.exit(0)
                else:
                    print(f"\n❌ No se pudo eliminar departamento {codigo}")
                    sys.exit(1)
        
        else:
            # Modo interactivo
            gestor.mostrar_menu_principal()
    
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()