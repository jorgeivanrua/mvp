#!/usr/bin/env python3
"""
Script simplificado para eliminar el departamento del Quindío
Uso: python scripts/eliminar_quindio.py --confirmar
"""
import sys
import os
import argparse

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

from scripts.departamentos_manager import DepartamentosManager


def main():
    """Eliminar Quindío de forma simplificada"""
    parser = argparse.ArgumentParser(description='Eliminar departamento del Quindío')
    parser.add_argument('--confirmar', action='store_true', required=True,
                       help='Confirmar que desea eliminar TODOS los datos del Quindío')
    
    args = parser.parse_args()
    
    print("🗑️  ELIMINANDO DEPARTAMENTO DEL QUINDÍO")
    print("=" * 50)
    print()
    print("⚠️  ADVERTENCIA: Se eliminarán TODOS los datos del Quindío:")
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
    
    # Confirmación adicional
    respuesta = input("Escriba 'ELIMINAR QUINDIO' para confirmar: ").strip()
    if respuesta != 'ELIMINAR QUINDIO':
        print("❌ Eliminación cancelada")
        sys.exit(0)
    
    try:
        manager = DepartamentosManager()
        resultado = manager.eliminar_departamento_completo('26', confirmar=True)
        
        if resultado['eliminado']:
            print("🎯 ¡QUINDÍO ELIMINADO EXITOSAMENTE!")
            print()
            print("💡 RESULTADO:")
            print(f"   - {resultado['ubicaciones_eliminadas']} ubicaciones eliminadas")
            print(f"   - {resultado['usuarios_eliminados']} usuarios eliminados")
            print(f"   - Configuración eliminada: {'Sí' if resultado['config_eliminada'] else 'No'}")
        else:
            print(f"ℹ️  No se pudo eliminar: {resultado.get('motivo', 'Motivo desconocido')}")
        
        print()
        
    except Exception as e:
        print(f"❌ Error eliminando Quindío: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()