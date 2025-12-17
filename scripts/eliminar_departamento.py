#!/usr/bin/env python3
"""
Script genérico para eliminar cualquier departamento
Uso: python scripts/eliminar_departamento.py <codigo> --confirmar
Ejemplo: python scripts/eliminar_departamento.py 44 --confirmar
"""
import sys
import os
import argparse

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

from scripts.departamentos_manager import DepartamentosManager


def main():
    """Eliminar cualquier departamento"""
    parser = argparse.ArgumentParser(description='Eliminar departamento por código')
    parser.add_argument('codigo', nargs='?', help='Código del departamento (ej: 44 para Caquetá)')
    parser.add_argument('--confirmar', action='store_true', required=False,
                       help='Confirmar que desea eliminar TODOS los datos del departamento')
    parser.add_argument('--estado', action='store_true',
                       help='Ver estado actual de departamentos')
    
    args = parser.parse_args()
    
    manager = DepartamentosManager()
    
    # Si se solicita estado, mostrar departamentos configurados
    if args.estado:
        print("📊 ESTADO ACTUAL DE DEPARTAMENTOS:")
        print("=" * 50)
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
            print("💡 Uso: python scripts/eliminar_departamento.py <codigo> --confirmar")
            print("   Ejemplo: python scripts/eliminar_departamento.py 44 --confirmar")
        except Exception as e:
            print(f"❌ Error: {e}")
        return
    
    # Validar código
    if not args.codigo:
        print("❌ Código de departamento requerido")
        print("💡 Use --estado para ver departamentos configurados")
        sys.exit(1)
    
    # Validar confirmación
    if not args.confirmar:
        print("❌ Debe usar --confirmar para eliminar un departamento")
        print("💡 Esta es una medida de seguridad para evitar eliminaciones accidentales")
        sys.exit(1)
    
    # Normalizar código
    codigo = args.codigo.strip().zfill(2)
    
    print(f"🗑️  ELIMINANDO DEPARTAMENTO - CÓDIGO: {codigo}")
    print("=" * 50)
    print()
    print("⚠️  ADVERTENCIA: Se eliminarán TODOS los datos del departamento:")
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
    
    try:
        # Verificar que el departamento existe en el sistema
        estados = manager.obtener_estado_departamentos()
        depto_info = next((d for d in estados if d['departamento_codigo'] == codigo), None)
        
        if depto_info:
            print(f"📍 Departamento encontrado: {depto_info['departamento_nombre']}")
            print(f"📊 Ubicaciones: {depto_info['total_municipios']} municipios, {depto_info['total_puestos']} puestos, {depto_info['total_mesas']} mesas")
            print(f"👥 Usuarios: {depto_info['total_usuarios_creados']}")
            print()
        else:
            print(f"ℹ️  Departamento {codigo} no está configurado en el sistema")
            print("   Verificando si existen datos residuales...")
            print()
        
        # Confirmación adicional
        respuesta = input(f"Escriba 'ELIMINAR {codigo}' para confirmar: ").strip()
        if respuesta != f'ELIMINAR {codigo}':
            print("❌ Eliminación cancelada")
            sys.exit(0)
        
        # Eliminar departamento
        resultado = manager.eliminar_departamento_completo(codigo, confirmar=True)
        
        if resultado['eliminado']:
            print(f"🎯 ¡DEPARTAMENTO {codigo} ELIMINADO EXITOSAMENTE!")
            print()
            print("💡 RESULTADO:")
            print(f"   - Departamento: {resultado['departamento_nombre']}")
            print(f"   - {resultado['ubicaciones_eliminadas']} ubicaciones eliminadas")
            print(f"   - {resultado['usuarios_eliminados']} usuarios eliminados")
            print(f"   - Configuración eliminada: {'Sí' if resultado['config_eliminada'] else 'No'}")
            print()
            print("📈 ESTADÍSTICAS DEL SISTEMA:")
            stats = resultado['estadisticas_despues']
            print(f"   - Ubicaciones restantes: {stats['ubicaciones']}")
            print(f"   - Usuarios restantes: {stats['usuarios']}")
            print(f"   - Departamentos habilitados: {stats['departamentos_habilitados']}")
        else:
            print(f"ℹ️  No se pudo eliminar: {resultado.get('motivo', 'Motivo desconocido')}")
        
        print()
        
    except Exception as e:
        print(f"❌ Error eliminando departamento: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()