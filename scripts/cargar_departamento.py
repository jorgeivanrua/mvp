#!/usr/bin/env python3
"""
Script genérico para cargar cualquier departamento
Uso: python scripts/cargar_departamento.py <codigo> [--principal]
Ejemplo: python scripts/cargar_departamento.py 26 --principal
"""
import sys
import os
import argparse

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

from scripts.departamentos_manager import DepartamentosManager


def main():
    """Cargar cualquier departamento"""
    parser = argparse.ArgumentParser(description='Cargar departamento por código')
    parser.add_argument('codigo', help='Código del departamento (ej: 26 para Quindío)')
    parser.add_argument('--principal', action='store_true', 
                       help='Marcar como departamento principal')
    parser.add_argument('--listar', action='store_true',
                       help='Listar departamentos disponibles')
    
    args = parser.parse_args()
    
    manager = DepartamentosManager()
    
    # Si se solicita listar, mostrar departamentos disponibles
    if args.listar:
        print("📋 DEPARTAMENTOS DISPONIBLES:")
        print("=" * 50)
        try:
            departamentos = manager.listar_departamentos_disponibles()
            for dept in departamentos:
                print(f"  {dept['departamento_codigo']} - {dept['departamento_nombre']}")
                print(f"      Municipios: {dept['total_municipios']}, Registros: {dept['total_registros']}")
            print()
            print("💡 Uso: python scripts/cargar_departamento.py <codigo> [--principal]")
            print("   Ejemplo: python scripts/cargar_departamento.py 26 --principal")
        except Exception as e:
            print(f"❌ Error: {e}")
        return
    
    # Validar código
    if not args.codigo:
        print("❌ Código de departamento requerido")
        print("💡 Use --listar para ver departamentos disponibles")
        sys.exit(1)
    
    # Normalizar código
    codigo = args.codigo.strip().zfill(2)
    
    print(f"🏛️  CARGANDO DEPARTAMENTO - CÓDIGO: {codigo}")
    print("=" * 50)
    
    if args.principal:
        print("⭐ Se marcará como departamento PRINCIPAL")
        print()
    
    try:
        # Verificar que el departamento existe
        departamentos = manager.listar_departamentos_disponibles()
        depto_info = next((d for d in departamentos if d['departamento_codigo'] == codigo), None)
        
        if not depto_info:
            print(f"❌ Departamento con código {codigo} no encontrado")
            print("💡 Use --listar para ver departamentos disponibles")
            sys.exit(1)
        
        print(f"📍 Departamento: {depto_info['departamento_nombre']}")
        print(f"📊 Municipios: {depto_info['total_municipios']}")
        print(f"📈 Total registros: {depto_info['total_registros']}")
        print()
        
        # Confirmar carga
        respuesta = input("¿Continuar con la carga? (S/n): ").strip().lower()
        if respuesta in ['n', 'no']:
            print("❌ Carga cancelada")
            sys.exit(0)
        
        # Cargar departamento
        resultado = manager.cargar_departamento_completo(codigo, es_principal=args.principal)
        
        print(f"🎉 ¡{depto_info['departamento_nombre'].upper()} CARGADO EXITOSAMENTE!")
        print()
        print("💡 PRÓXIMOS PASOS:")
        print("   1. Los usuarios pueden iniciar sesión con contraseña: test123")
        print("   2. Revisar el dashboard de administración")
        print("   3. Configurar datos adicionales si es necesario")
        print()
        
    except Exception as e:
        print(f"❌ Error cargando departamento: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()