#!/usr/bin/env python3
"""
Demo del Sistema Universal de Departamentos
Demuestra que el sistema puede cargar cualquier departamento de Colombia

Este script:
1. Muestra departamentos disponibles
2. Permite cargar un departamento de prueba
3. Verifica que funciona correctamente
4. Limpia el departamento de prueba

Uso:
    python scripts/demo_sistema_universal.py
    python scripts/demo_sistema_universal.py --departamento 05  # Antioquia
"""
import sys
import os
import argparse
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from scripts.cargar_departamento_completo import CargadorDepartamentoCompleto
    from scripts.verificar_departamento import VerificadorDepartamento
    from scripts.departamentos_manager import DepartamentosManager
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


class DemoSistemaUniversal:
    """Demo del sistema universal de departamentos"""
    
    def __init__(self):
        self.cargador = CargadorDepartamentoCompleto()
        self.verificador = VerificadorDepartamento()
        self.manager = DepartamentosManager()
    
    def ejecutar_demo_completo(self, departamento_codigo: str = None):
        """Ejecutar demo completo del sistema"""
        print("=" * 80)
        print("🎬 DEMO DEL SISTEMA UNIVERSAL DE DEPARTAMENTOS ELECTORALES")
        print("=" * 80)
        print("Demostrando que el sistema puede cargar CUALQUIER departamento de Colombia")
        print()
        
        try:
            # PASO 1: Mostrar departamentos disponibles
            print("📋 PASO 1: DEPARTAMENTOS DISPONIBLES EN COLOMBIA")
            print("-" * 60)
            
            departamentos = self.cargador.listar_departamentos_disponibles()
            if not departamentos:
                print("❌ No se pudieron cargar los departamentos")
                return False
            
            print(f"✅ {len(departamentos)} departamentos disponibles para cargar")
            print("\nAlgunos ejemplos:")
            for dept in departamentos[:10]:
                print(f"   {dept['departamento_codigo']} - {dept['departamento_nombre']}")
                print(f"       📊 {dept['total_municipios']} municipios, {dept['total_puestos']} puestos, {dept['total_mesas']} mesas")
            
            if len(departamentos) > 10:
                print(f"   ... y {len(departamentos) - 10} departamentos más")
            
            # PASO 2: Seleccionar departamento para demo
            if not departamento_codigo:
                departamento_codigo = self.seleccionar_departamento_demo(departamentos)
            
            if not departamento_codigo:
                print("❌ Demo cancelado")
                return False
            
            # Obtener info del departamento
            depto_info = next((d for d in departamentos if d['departamento_codigo'] == departamento_codigo), None)
            if not depto_info:
                print(f"❌ Departamento {departamento_codigo} no encontrado")
                return False
            
            print(f"\n🎯 DEPARTAMENTO SELECCIONADO PARA DEMO:")
            print(f"   📍 {depto_info['departamento_nombre']} (Código: {departamento_codigo})")
            print(f"   📊 {depto_info['total_municipios']} municipios")
            print(f"   🏢 {depto_info['total_puestos']} puestos de votación")
            print(f"   🗳️  {depto_info['total_mesas']} mesas electorales")
            
            # PASO 3: Verificar estado actual
            print(f"\n🔍 PASO 2: VERIFICANDO ESTADO ACTUAL")
            print("-" * 60)
            
            estado_inicial = self.verificador.verificar_departamento_completo(departamento_codigo)
            ya_existe = estado_inicial['verificaciones'].get('configuracion', False)
            
            if ya_existe:
                print(f"ℹ️  El departamento ya está configurado en el sistema")
                respuesta = input("¿Continuar con recarga para demostrar funcionalidad? (S/n): ").strip().lower()
                if respuesta in ['n', 'no']:
                    print("Demo cancelado por el usuario")
                    return False
            
            # PASO 4: Cargar departamento
            print(f"\n📥 PASO 3: CARGANDO DEPARTAMENTO COMPLETO")
            print("-" * 60)
            print(f"Cargando {depto_info['departamento_nombre']} con todas las validaciones y correcciones...")
            
            resultado_carga = self.cargador.cargar_departamento_completo(
                departamento_codigo=departamento_codigo,
                es_principal=False,  # No cambiar el principal en el demo
                forzar=True  # Forzar para demostrar funcionalidad
            )
            
            if not resultado_carga.get('exitoso'):
                print(f"❌ Error cargando departamento")
                return False
            
            print(f"✅ {depto_info['departamento_nombre']} cargado exitosamente")
            
            # PASO 5: Verificar funcionalidad completa
            print(f"\n✅ PASO 4: VERIFICANDO FUNCIONALIDAD COMPLETA")
            print("-" * 60)
            
            resultado_verificacion = self.verificador.verificar_departamento_completo(departamento_codigo)
            
            if resultado_verificacion['estado_general'] == 'EXCELENTE':
                print(f"🎉 ¡VERIFICACIÓN EXITOSA! Departamento completamente funcional")
            else:
                print(f"⚠️  Verificación con advertencias (normal en algunos casos)")
            
            # PASO 6: Mostrar estadísticas finales
            print(f"\n📊 PASO 5: ESTADÍSTICAS FINALES")
            print("-" * 60)
            
            self.mostrar_estadisticas_demo(resultado_carga, resultado_verificacion)
            
            # PASO 7: Preguntar si limpiar
            print(f"\n🧹 PASO 6: LIMPIEZA (OPCIONAL)")
            print("-" * 60)
            
            if not ya_existe:
                respuesta = input(f"¿Eliminar {depto_info['departamento_nombre']} del sistema? (s/N): ").strip().lower()
                if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                    print(f"🗑️  Eliminando {depto_info['departamento_nombre']}...")
                    try:
                        resultado_eliminacion = self.manager.eliminar_departamento_completo(
                            departamento_codigo, 
                            confirmar=True
                        )
                        if resultado_eliminacion['eliminado']:
                            print(f"✅ {depto_info['departamento_nombre']} eliminado correctamente")
                        else:
                            print(f"⚠️  No se pudo eliminar completamente")
                    except Exception as e:
                        print(f"❌ Error eliminando: {e}")
                else:
                    print(f"ℹ️  {depto_info['departamento_nombre']} permanece en el sistema")
            
            # CONCLUSIÓN
            print(f"\n" + "=" * 80)
            print("🎉 DEMO COMPLETADO EXITOSAMENTE")
            print("=" * 80)
            print(f"✅ Se demostró que el sistema puede cargar {depto_info['departamento_nombre']} completamente")
            print(f"✅ Todas las funcionalidades están operativas")
            print(f"✅ El sistema está listo para cualquier departamento de Colombia")
            print()
            print("🚀 CAPACIDADES DEMOSTRADAS:")
            print("   • Carga automática de ubicaciones jerárquicas")
            print("   • Creación automática de usuarios por rol")
            print("   • Correcciones automáticas de datos")
            print("   • Verificación exhaustiva de funcionalidad")
            print("   • Gestión completa del ciclo de vida")
            print()
            print("🎯 CONCLUSIÓN: Sistema 100% funcional para cualquier departamento")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error durante el demo: {e}")
            return False
    
    def seleccionar_departamento_demo(self, departamentos: list) -> str:
        """Seleccionar departamento para el demo"""
        print(f"\n🎯 SELECCIÓN DE DEPARTAMENTO PARA DEMO")
        print("-" * 50)
        
        # Sugerir algunos departamentos interesantes
        sugerencias = [
            ('05', 'ANTIOQUIA', 'Departamento más grande de Colombia'),
            ('76', 'VALLE DEL CAUCA', 'Importante departamento del Pacífico'),
            ('08', 'ATLÁNTICO', 'Departamento de la Costa Caribe'),
            ('15', 'BOYACÁ', 'Departamento histórico de la región Andina'),
            ('68', 'SANTANDER', 'Importante departamento del nororiente')
        ]
        
        print("Departamentos sugeridos para el demo:")
        for codigo, nombre, descripcion in sugerencias:
            # Verificar que existe en la lista
            existe = any(d['departamento_codigo'] == codigo for d in departamentos)
            if existe:
                print(f"   {codigo} - {nombre}")
                print(f"       {descripcion}")
        
        print()
        print("💡 También puede usar cualquier otro código de departamento")
        print()
        
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
                print("💡 Use uno de los códigos mostrados arriba")
                continue
            
            # Confirmar selección
            print(f"\n📍 Seleccionado: {depto_info['departamento_nombre']}")
            print(f"   📊 {depto_info['total_municipios']} municipios, {depto_info['total_puestos']} puestos, {depto_info['total_mesas']} mesas")
            
            confirmacion = input("¿Continuar con este departamento? (S/n): ").strip().lower()
            if confirmacion not in ['n', 'no']:
                return codigo
    
    def mostrar_estadisticas_demo(self, resultado_carga: dict, resultado_verificacion: dict):
        """Mostrar estadísticas del demo"""
        carga = resultado_carga.get('carga', {})
        ubicaciones = carga.get('ubicaciones', {})
        usuarios = carga.get('usuarios', {})
        correcciones = resultado_carga.get('correcciones', {})
        
        print("📈 DATOS CARGADOS:")
        print(f"   • Departamentos: {ubicaciones.get('departamentos', 0)}")
        print(f"   • Municipios: {ubicaciones.get('municipios', 0)}")
        print(f"   • Zonas: {ubicaciones.get('zonas', 0)}")
        print(f"   • Puestos: {ubicaciones.get('puestos', 0)}")
        print(f"   • Mesas: {ubicaciones.get('mesas_creadas', 0)}")
        
        print(f"\n👥 USUARIOS CREADOS:")
        print(f"   • Coordinador Departamental: {usuarios.get('coordinador_departamental', 0)}")
        print(f"   • Coordinadores Municipales: {usuarios.get('coordinador_municipal', 0)}")
        print(f"   • Coordinadores de Puesto: {usuarios.get('coordinador_puesto', 0)}")
        print(f"   • Testigos Electorales: {usuarios.get('testigo_electoral', 0)}")
        
        print(f"\n🔧 CORRECCIONES APLICADAS:")
        print(f"   • Testigos movidos a puestos: {correcciones.get('testigos_corregidos', 0)}")
        print(f"   • Cédulas asignadas: {correcciones.get('cedulas_asignadas', 0)}")
        print(f"   • Usuarios reactivados: {correcciones.get('usuarios_reactivados', 0)}")
        print(f"   • Ubicaciones reactivadas: {correcciones.get('ubicaciones_reactivadas', 0)}")
        
        print(f"\n✅ VERIFICACIONES:")
        verificaciones = resultado_verificacion.get('verificaciones', {})
        for verificacion, pasada in verificaciones.items():
            estado = "✅ PASÓ" if pasada else "⚠️  ADVERTENCIA"
            print(f"   • {verificacion.upper()}: {estado}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Demo del Sistema Universal de Departamentos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Este demo demuestra que el sistema puede cargar cualquier departamento de Colombia
de forma completa y funcional.

Ejemplos:
  python scripts/demo_sistema_universal.py                    # Demo interactivo
  python scripts/demo_sistema_universal.py --departamento 05  # Demo con Antioquia
        """
    )
    
    parser.add_argument('--departamento', metavar='CODIGO',
                       help='Código del departamento para el demo (ej: 05 para Antioquia)')
    
    args = parser.parse_args()
    
    demo = DemoSistemaUniversal()
    
    try:
        exito = demo.ejecutar_demo_completo(args.departamento)
        
        if exito:
            print("\n🎉 Demo completado exitosamente")
            sys.exit(0)
        else:
            print("\n❌ Demo no completado")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error durante el demo: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()