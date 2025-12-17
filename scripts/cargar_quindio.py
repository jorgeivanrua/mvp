#!/usr/bin/env python3
"""
Script simplificado para cargar el departamento del Quindío
Uso: python scripts/cargar_quindio.py [--principal]
"""
import sys
import os
import argparse

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

from scripts.departamentos_manager import DepartamentosManager


def main():
    """Cargar Quindío de forma simplificada"""
    parser = argparse.ArgumentParser(description='Cargar departamento del Quindío')
    parser.add_argument('--principal', action='store_true', 
                       help='Marcar como departamento principal')
    
    args = parser.parse_args()
    
    print("🏛️  CARGANDO DEPARTAMENTO DEL QUINDÍO")
    print("=" * 50)
    
    if args.principal:
        print("⭐ Se marcará como departamento PRINCIPAL")
        print()
    
    try:
        manager = DepartamentosManager()
        resultado = manager.cargar_departamento_completo('26', es_principal=args.principal)
        
        print("🎉 ¡QUINDÍO CARGADO EXITOSAMENTE!")
        print()
        print("💡 PRÓXIMOS PASOS:")
        print("   1. Los usuarios pueden iniciar sesión con contraseña: test123")
        print("   2. Revisar el dashboard de administración")
        print("   3. Configurar datos adicionales si es necesario")
        print()
        
    except Exception as e:
        print(f"❌ Error cargando Quindío: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()