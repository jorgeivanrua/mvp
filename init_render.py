#!/usr/bin/env python3
"""
Script de inicialización rápida para Render
Ejecutar manualmente si la aplicación no tiene datos

Uso:
    python init_render.py
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

def main():
    """Inicialización rápida"""
    print("🚀 Inicializando sistema electoral en Render...")
    
    try:
        # Importar y ejecutar cargador
        from scripts.cargar_departamento_completo import CargadorDepartamentoCompleto
        
        cargador = CargadorDepartamentoCompleto()
        
        print("📥 Cargando Quindío...")
        resultado = cargador.cargar_departamento_completo(
            departamento_codigo='26',
            es_principal=True,
            forzar=True  # Forzar para asegurar carga
        )
        
        if resultado.get('exitoso'):
            print("✅ ¡Sistema inicializado exitosamente!")
            print(f"   Usuarios creados: {resultado['estadisticas']['total_usuarios']}")
            print("🎉 Listo para usar")
        else:
            print(f"❌ Error: {resultado.get('motivo')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()