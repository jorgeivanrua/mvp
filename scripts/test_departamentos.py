#!/usr/bin/env python3
"""
Script de prueba para verificar el sistema de gestión de departamentos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from scripts.departamentos_manager import DepartamentosManager
    print("✅ Importación exitosa de DepartamentosManager")
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)


def test_listar_departamentos():
    """Probar listado de departamentos"""
    print("\n🧪 PRUEBA: Listar departamentos disponibles")
    print("-" * 50)
    
    try:
        manager = DepartamentosManager()
        departamentos = manager.listar_departamentos_disponibles()
        
        print(f"✅ Se encontraron {len(departamentos)} departamentos")
        
        # Buscar Quindío específicamente
        quindio = next((d for d in departamentos if d['departamento_codigo'] == '26'), None)
        if quindio:
            print(f"✅ Quindío encontrado: {quindio['departamento_nombre']}")
            print(f"   Municipios: {quindio['total_municipios']}")
            print(f"   Registros: {quindio['total_registros']}")
        else:
            print("❌ Quindío no encontrado en el CSV")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_estado_departamentos():
    """Probar obtención de estado de departamentos"""
    print("\n🧪 PRUEBA: Obtener estado de departamentos")
    print("-" * 50)
    
    try:
        manager = DepartamentosManager()
        estados = manager.obtener_estado_departamentos()
        
        print(f"✅ Se encontraron {len(estados)} departamentos configurados")
        
        for estado in estados:
            status = "HABILITADO" if estado['habilitado'] else "DESHABILITADO"
            principal = " (PRINCIPAL)" if estado['es_principal'] else ""
            print(f"   {estado['departamento_codigo']} - {estado['departamento_nombre']} - {status}{principal}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_validaciones():
    """Probar validaciones del sistema"""
    print("\n🧪 PRUEBA: Validaciones del sistema")
    print("-" * 50)
    
    try:
        manager = DepartamentosManager()
        
        # Probar departamento inexistente
        try:
            manager.cargar_departamento_completo('99')  # Código inexistente
            print("❌ No se validó departamento inexistente")
            return False
        except ValueError as e:
            print("✅ Validación de departamento inexistente funciona")
        
        # Probar eliminación sin confirmación
        try:
            manager.eliminar_departamento_completo('26', confirmar=False)
            print("❌ No se validó eliminación sin confirmación")
            return False
        except ValueError as e:
            print("✅ Validación de confirmación funciona")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def main():
    """Ejecutar todas las pruebas"""
    print("🧪 PRUEBAS DEL SISTEMA DE GESTIÓN DE DEPARTAMENTOS")
    print("=" * 60)
    
    pruebas = [
        ("Listar departamentos", test_listar_departamentos),
        ("Estado departamentos", test_estado_departamentos),
        ("Validaciones", test_validaciones),
    ]
    
    resultados = []
    
    for nombre, prueba in pruebas:
        try:
            resultado = prueba()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ Error en prueba '{nombre}': {e}")
            resultados.append((nombre, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    exitosas = 0
    for nombre, resultado in resultados:
        status = "✅ EXITOSA" if resultado else "❌ FALLIDA"
        print(f"   {nombre}: {status}")
        if resultado:
            exitosas += 1
    
    print(f"\n🎯 RESULTADO: {exitosas}/{len(resultados)} pruebas exitosas")
    
    if exitosas == len(resultados):
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo para usar.")
        print()
        print("💡 PRÓXIMOS PASOS:")
        print("   1. Cargar Quindío: python scripts/cargar_quindio.py --principal")
        print("   2. Ver estado: python scripts/eliminar_departamento.py --estado")
        print("   3. Usar gestor: python scripts/departamentos_manager.py")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar errores antes de usar el sistema.")
        sys.exit(1)


if __name__ == '__main__':
    main()