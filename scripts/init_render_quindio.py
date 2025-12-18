#!/usr/bin/env python3
"""
Script de inicialización para Render - Cargar Quindío automáticamente
Este script se ejecuta en Render para cargar el departamento de Quindío con todos sus datos

Uso en Render:
    python scripts/init_render_quindio.py
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from backend.app import create_app
    from backend.database import db
    from backend.models.departamento_config import DepartamentoConfig
    from scripts.cargar_departamento_completo import CargadorDepartamentoCompleto
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)


def verificar_si_ya_cargado():
    """Verificar si Quindío ya está cargado"""
    app = create_app()
    with app.app_context():
        config = DepartamentoConfig.query.filter_by(
            departamento_codigo='26'
        ).first()
        
        if config and config.total_usuarios_creados > 0:
            print(f"✅ Quindío ya está cargado con {config.total_usuarios_creados} usuarios")
            return True
        return False


def cargar_quindio_render():
    """Cargar Quindío en Render automáticamente"""
    print("=" * 80)
    print("🚀 INICIALIZACIÓN DE RENDER - CARGANDO QUINDÍO")
    print("=" * 80)
    
    # Verificar si ya está cargado
    if verificar_si_ya_cargado():
        print("ℹ️  Sistema ya inicializado - no se requiere carga")
        return True
    
    print("\n📥 Cargando departamento de Quindío...")
    print("   Esto puede tomar unos minutos...")
    
    try:
        cargador = CargadorDepartamentoCompleto()
        
        resultado = cargador.cargar_departamento_completo(
            departamento_codigo='26',
            es_principal=True,
            forzar=False
        )
        
        if resultado.get('exitoso'):
            print("\n✅ QUINDÍO CARGADO EXITOSAMENTE EN RENDER")
            print(f"   • Ubicaciones: {resultado['estadisticas']['total_ubicaciones']}")
            print(f"   • Usuarios: {resultado['estadisticas']['total_usuarios']}")
            print(f"   • Municipios: {resultado['estadisticas']['total_municipios']}")
            print(f"   • Puestos: {resultado['estadisticas']['total_puestos']}")
            print(f"   • Mesas: {resultado['estadisticas']['total_mesas']}")
            print("\n🎉 Sistema listo para usar en Render")
            return True
        else:
            print(f"\n❌ Error cargando Quindío: {resultado.get('motivo')}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error durante la carga: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    try:
        exitoso = cargar_quindio_render()
        sys.exit(0 if exitoso else 1)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)
