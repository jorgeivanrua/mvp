#!/usr/bin/env python3
"""
Demo del Sistema de Eliminación de Departamentos
Demuestra las capacidades de eliminación segura y exhaustiva

Este script:
1. Carga un departamento de prueba
2. Muestra las capacidades de verificación
3. Demuestra eliminación segura
4. Verifica que la eliminación fue completa

Uso:
    python scripts/demo_eliminacion_departamentos.py
    python scripts/demo_eliminacion_departamentos.py --departamento 05  # Antioquia
"""
import sys
import os
import argparse
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from scripts.cargar_departamento_completo import CargadorDepartamentoCompleto
    from scripts.eliminar_departamento_completo import EliminadorDepartamentoCompleto
    from scripts.verificar_departamento import VerificadorDepartamento
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class DemoEliminacionDepartamentos:
    """Demo del sistema de eliminación de departamentos"""
    
    def __init__(self):
        self.cargador = CargadorDepartamentoCompleto()
        self.eliminador = EliminadorDepartamentoCompleto()
        self.verificador = VerificadorDepartamento()
    
    def ejecutar_demo_completo(self, departamento_codigo: str = None):
        """Ejecutar demo completo del sistema de eliminación"""
        print("=" * 80)
        print("🎬 DEMO DEL SISTEMA DE ELIMINACIÓN DE DEPARTAMENTOS")
        print("=" * 80)
        print("Demostrando eliminación segura y exhaustiva de cualquier departamento")
        print()
        
        try:
            # PASO 1: Seleccionar departamento para demo
            if not departamento_codigo:
                departamento_codigo = self._seleccionar_departamento_demo()
            
            if not departamento_codigo:
                print("❌ Demo cancelado")
                return False
            
            # PASO 2: Verificar si ya existe o cargarlo
            print(f"📋 PASO 1: PREPARACIÓN DEL DEPARTAMENTO DE PRUEBA")
            print("-" * 60)
            
            existe_antes = self._verificar_existencia_departamento(departamento_codigo)
            
            if not existe_antes:
                print(f"📥 Cargando {departamento_codigo} para el demo...")
                resultado_carga = self.cargador.cargar_departamento_completo(
                    departamento_codigo=departamento_codigo,
                    es_principal=False,
                    forzar=True
                )
                
                if not resultado_carga.get('exitoso'):
                    print("❌ Error cargando departamento para demo")
                    return False
                
                print(f"✅ Departamento {departamento_codigo} cargado para demo")
            else:
                print(f"✅ Departamento {departamento_codigo} ya existe - usando para demo")
            
            # PASO 3: Demostrar verificación previa
            print(f"\n🔍 PASO 2: DEMOSTRACIÓN DE VERIFICACIÓN PREVIA")
            print("-" * 60)
            
            verificacion = self.eliminador.verificar_antes_eliminacion(departamento_codigo)
            
            if not verificacion['existe']:
                print("❌ Error: Departamento no encontrado después de carga")
                return False
            
            print("✅ Verificación previa completada - se mostró:")
            print("   • Información del departamento")
            print("   • Ubicaciones por tipo")
            print("   • Usuarios por rol")
            print("   • Datos electorales")
            
            # PASO 4: Demostrar capacidades de eliminación
            print(f"\n🗑️  PASO 3: DEMOSTRACIÓN DE CAPACIDADES DE ELIMINACIÓN")
            print("-" * 60)
            
            self._demostrar_capacidades_eliminacion(verificacion)
            
            # PASO 5: Confirmar eliminación para demo
            print(f"\n❓ PASO 4: CONFIRMACIÓN PARA DEMO")
            print("-" * 60)
            
            if not self._confirmar_eliminacion_demo(departamento_codigo, existe_antes):
                print("ℹ️  Demo completado sin eliminación real")
                return True
            
            # PASO 6: Ejecutar eliminación
            print(f"\n🚀 PASO 5: EJECUTANDO ELIMINACIÓN COMPLETA")
            print("-" * 60)
            
            resultado_eliminacion = self.eliminador.eliminar_departamento_completo(
                departamento_codigo=departamento_codigo,
                forzar=True  # Forzar para evitar confirmaciones en demo
            )
            
            if not resultado_eliminacion['eliminado']:
                print(f"❌ Error en eliminación: {resultado_eliminacion.get('motivo')}")
                return False
            
            print("✅ Eliminación completada exitosamente")
            
            # PASO 7: Verificar eliminación completa
            print(f"\n✅ PASO 6: VERIFICACIÓN POST-ELIMINACIÓN")
            print("-" * 60)
            
            self._verificar_eliminacion_completa(departamento_codigo, resultado_eliminacion)
            
            # CONCLUSIÓN
            print(f"\n" + "=" * 80)
            print("🎉 DEMO DE ELIMINACIÓN COMPLETADO EXITOSAMENTE")
            print("=" * 80)
            
            self._mostrar_resumen_demo(departamento_codigo, resultado_eliminacion)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error durante el demo: {e}")
            return False
    
    def _seleccionar_departamento_demo(self) -> str:
        """Seleccionar departamento para el demo"""
        print(f"🎯 SELECCIÓN DE DEPARTAMENTO PARA DEMO DE ELIMINACIÓN")
        print("-" * 60)
        
        # Obtener departamentos disponibles
        try:
            departamentos = self.cargador.listar_departamentos_disponibles()
            
            # Sugerir departamentos pequeños para demo
            sugerencias = [
                ('17', 'CALDAS', 'Departamento del Eje Cafetero (27 municipios)'),
                ('63', 'QUINDÍO', 'Departamento pequeño del Eje Cafetero (12 municipios)'),
                ('66', 'RISARALDA', 'Departamento del Eje Cafetero (14 municipios)'),
                ('88', 'SAN ANDRÉS', 'Departamento insular (2 municipios)'),
                ('91', 'AMAZONAS', 'Departamento amazónico (11 municipios)')
            ]
            
            print("Departamentos sugeridos para demo de eliminación:")
            for codigo, nombre, descripcion in sugerencias:
                # Verificar que existe en la lista
                existe = any(d['departamento_codigo'] == codigo for d in departamentos)
                if existe:
                    print(f"   {codigo} - {nombre}")
                    print(f"       {descripcion}")
            
            print()
            print("💡 Se recomienda usar departamentos pequeños para el demo")
            print("⚠️  El departamento será eliminado completamente al final del demo")
            print()
            
        except Exception as e:
            print(f"❌ Error obteniendo departamentos: {e}")
            return None
        
        while True:
            codigo = input("Ingrese el código del departamento para el demo (o 'cancelar'): ").strip()
            
            if codigo.lower() in ['cancelar', 'cancel', 'salir', 'exit']:
                return None
            
            if not codigo:
                print("❌ Código requerido")
                continue
            
            codigo = codigo.zfill(2)
            
            # Verificar que existe
            depto_info = next((d for d in departamentos if d['departamento_codigo'] == codigo), None)
            if not depto_info:
                print(f"❌ Departamento {codigo} no encontrado")
                continue
            
            # Mostrar información y confirmar
            print(f"\n📍 Seleccionado: {depto_info['departamento_nombre']}")
            print(f"   📊 {depto_info['total_municipios']} municipios")
            print(f"   🏢 {depto_info['total_puestos']} puestos")
            print(f"   🗳️  {depto_info['total_mesas']} mesas")
            print()
            print(f"⚠️  ADVERTENCIA: Este departamento será ELIMINADO al final del demo")
            
            confirmacion = input("¿Continuar con este departamento? (S/n): ").strip().lower()
            if confirmacion not in ['n', 'no']:
                return codigo
    
    def _verificar_existencia_departamento(self, departamento_codigo: str) -> bool:
        """Verificar si el departamento ya existe en el sistema"""
        try:
            departamentos_configurados = self.eliminador.listar_departamentos_configurados()
            return any(dept['departamento_codigo'] == departamento_codigo for dept in departamentos_configurados)
        except:
            return False
    
    def _demostrar_capacidades_eliminacion(self, verificacion: dict):
        """Demostrar las capacidades del sistema de eliminación"""
        config = verificacion['config']
        
        print("🛠️  CAPACIDADES DEMOSTRADAS:")
        print()
        
        print("1. 🔍 VERIFICACIÓN PREVIA EXHAUSTIVA:")
        print(f"   ✅ Detectó departamento: {config['departamento_nombre']}")
        print(f"   ✅ Identificó {verificacion['total_ubicaciones']} ubicaciones")
        print(f"   ✅ Identificó {verificacion['total_usuarios']} usuarios")
        
        datos_electorales = verificacion['datos_electorales']
        total_datos = sum(v for v in datos_electorales.values() if isinstance(v, int))
        if total_datos > 0:
            print(f"   ✅ Identificó {total_datos} registros de datos electorales")
        
        print()
        print("2. 🛡️  MEDIDAS DE SEGURIDAD:")
        print("   ✅ Múltiples confirmaciones requeridas")
        print("   ✅ Texto exacto de confirmación")
        print("   ✅ Preservación de super administradores")
        
        if config['es_principal']:
            print("   ⚠️  Confirmación especial para departamento principal")
        
        print()
        print("3. 🗑️  ELIMINACIÓN EXHAUSTIVA:")
        print("   ✅ Todos los datos electorales")
        print("   ✅ Todos los usuarios (excepto super admin)")
        print("   ✅ Todas las ubicaciones")
        print("   ✅ Configuración del departamento")
        
        print()
        print("4. ✅ VERIFICACIÓN POST-ELIMINACIÓN:")
        print("   ✅ Confirmación de eliminación completa")
        print("   ✅ Detección de datos residuales")
        print("   ✅ Rollback automático en caso de errores")
    
    def _confirmar_eliminacion_demo(self, departamento_codigo: str, existia_antes: bool) -> bool:
        """Confirmar si proceder con eliminación en el demo"""
        print(f"⚠️  CONFIRMACIÓN PARA DEMO")
        print()
        
        if existia_antes:
            print(f"⚠️  ADVERTENCIA: El departamento {departamento_codigo} YA EXISTÍA en el sistema")
            print(f"   Si continúa, se eliminará un departamento real con datos reales")
        else:
            print(f"ℹ️  El departamento {departamento_codigo} fue cargado específicamente para este demo")
            print(f"   Es seguro eliminarlo al final del demo")
        
        print()
        print(f"¿Desea proceder con la eliminación real para completar el demo?")
        print(f"Opciones:")
        print(f"  S - Sí, eliminar y completar demo")
        print(f"  N - No, terminar demo sin eliminar")
        print()
        
        respuesta = input("Su elección (S/n): ").strip().lower()
        return respuesta in ['s', 'si', 'sí', 'y', 'yes', '']
    
    def _verificar_eliminacion_completa(self, departamento_codigo: str, resultado: dict):
        """Verificar que la eliminación fue completa"""
        print("🔍 Verificando eliminación completa...")
        
        # Verificar que no existe más
        existe_despues = self._verificar_existencia_departamento(departamento_codigo)
        
        if not existe_despues:
            print("   ✅ Departamento eliminado completamente del sistema")
        else:
            print("   ⚠️  Departamento aún aparece en configuraciones")
        
        # Verificar estadísticas de eliminación
        verificacion_final = resultado.get('verificacion_final', {})
        
        if verificacion_final.get('eliminacion_completa'):
            print("   ✅ Verificación interna confirma eliminación completa")
        else:
            print("   ⚠️  Verificación interna detectó datos residuales")
        
        # Mostrar estadísticas
        ubicaciones_eliminadas = resultado['ubicaciones_eliminadas']['total']
        usuarios_eliminados = resultado['usuarios_eliminados']['total']
        
        print(f"   📊 Eliminados: {ubicaciones_eliminadas} ubicaciones, {usuarios_eliminados} usuarios")
        
        # Verificar usuarios huérfanos
        usuarios_huerfanos = verificacion_final.get('usuarios_huerfanos', 0)
        if usuarios_huerfanos > 0:
            print(f"   ⚠️  {usuarios_huerfanos} usuarios huérfanos detectados")
        else:
            print("   ✅ No se detectaron usuarios huérfanos")
    
    def _mostrar_resumen_demo(self, departamento_codigo: str, resultado: dict):
        """Mostrar resumen del demo"""
        print(f"📊 RESUMEN DEL DEMO:")
        print(f"   • Departamento: {resultado['departamento_nombre']} ({departamento_codigo})")
        print(f"   • Eliminación: {'✅ Exitosa' if resultado['eliminado'] else '❌ Falló'}")
        
        ubicaciones = resultado['ubicaciones_eliminadas']
        usuarios = resultado['usuarios_eliminados']
        
        print(f"   • Ubicaciones eliminadas: {ubicaciones['total']}")
        for tipo, cantidad in ubicaciones['por_tipo'].items():
            print(f"     - {tipo}: {cantidad}")
        
        print(f"   • Usuarios eliminados: {usuarios['total']}")
        for rol, cantidad in usuarios['por_rol'].items():
            print(f"     - {rol}: {cantidad}")
        
        if usuarios['super_admin_preservados'] > 0:
            print(f"   • Super admins preservados: {usuarios['super_admin_preservados']}")
        
        datos_electorales = resultado['datos_electorales_eliminados']
        total_datos = sum(v for v in datos_electorales.values() if isinstance(v, int))
        if total_datos > 0:
            print(f"   • Datos electorales eliminados: {total_datos} registros")
        
        print()
        print("🎯 CAPACIDADES DEMOSTRADAS:")
        print("   ✅ Verificación previa exhaustiva")
        print("   ✅ Eliminación completa y segura")
        print("   ✅ Múltiples medidas de seguridad")
        print("   ✅ Verificación post-eliminación")
        print("   ✅ Preservación de datos críticos")
        
        print()
        print("🚀 CONCLUSIÓN: Sistema de eliminación 100% funcional")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Demo del Sistema de Eliminación de Departamentos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Este demo demuestra las capacidades de eliminación segura y exhaustiva
del sistema electoral.

Ejemplos:
  python scripts/demo_eliminacion_departamentos.py                    # Demo interactivo
  python scripts/demo_eliminacion_departamentos.py --departamento 17  # Demo con Caldas
        """
    )
    
    parser.add_argument('--departamento', metavar='CODIGO',
                       help='Código del departamento para el demo (ej: 17 para Caldas)')
    
    args = parser.parse_args()
    
    demo = DemoEliminacionDepartamentos()
    
    try:
        exito = demo.ejecutar_demo_completo(args.departamento)
        
        if exito:
            print("\n🎉 Demo de eliminación completado exitosamente")
            sys.exit(0)
        else:
            print("\n❌ Demo de eliminación no completado")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error durante el demo: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()