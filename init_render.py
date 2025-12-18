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

def verificar_estado():
    """Verificar si ya hay datos cargados"""
    try:
        from backend.app import create_app
        from backend.models.user import User
        from backend.models.location import Location
        
        app = create_app()
        with app.app_context():
            usuarios = User.query.count()
            ubicaciones_quindio = Location.query.filter_by(
                departamento_codigo='26'
            ).count()
            
            print(f"📊 Estado actual: {usuarios} usuarios, {ubicaciones_quindio} ubicaciones de Quindío")
            
            if usuarios > 2 and ubicaciones_quindio > 0:
                print("✅ Sistema ya inicializado")
                return True
            return False
    except Exception as e:
        print(f"⚠️  Error verificando estado: {e}")
        return False

def cargar_quindio_simple():
    """Cargar Quindío de forma simple y robusta"""
    try:
        from backend.app import create_app
        from backend.database import db
        from backend.models.location import Location
        from backend.models.user import User
        from backend.models.departamento_config import DepartamentoConfig
        from backend.services.departamento_service import DepartamentoService
        
        app = create_app()
        with app.app_context():
            print("📥 Cargando departamento de Quindío...")
            
            # Usar el servicio de departamentos
            resultado = DepartamentoService.habilitar_departamento(
                departamento_codigo='26',
                es_principal=True,
                auto_cargar=True
            )
            
            if resultado['success']:
                print("✅ Quindío cargado exitosamente")
                
                # Verificar resultados
                usuarios = User.query.count()
                ubicaciones = Location.query.filter_by(
                    departamento_codigo='26'
                ).count()
                
                print(f"📊 Resultado: {usuarios} usuarios, {ubicaciones} ubicaciones")
                return True
            else:
                print(f"❌ Error: {resultado['message']}")
                return False
                
    except Exception as e:
        print(f"❌ Error cargando Quindío: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Inicialización rápida"""
    print("🚀 Inicializando sistema electoral en Render...")
    print("=" * 50)
    
    # Verificar estado actual
    if verificar_estado():
        print("ℹ️  No se requiere inicialización")
        return
    
    # Cargar Quindío
    if cargar_quindio_simple():
        print("\n🎉 ¡Sistema inicializado exitosamente!")
        print("🔗 Listo para usar en Render")
    else:
        print("\n❌ Error en la inicialización")
        sys.exit(1)

if __name__ == '__main__':
    main()