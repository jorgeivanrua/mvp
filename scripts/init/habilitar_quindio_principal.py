"""
Script para habilitar el Quindío como departamento principal
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.services.departamento_service import DepartamentoService
from backend.models.departamento_config import DepartamentoConfig
from backend.database import db

def habilitar_quindio_principal():
    """Habilitar el Quindío como departamento principal"""
    print("=" * 60)
    print("HABILITANDO QUINDÍO COMO DEPARTAMENTO PRINCIPAL")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Código del Quindío
            quindio_codigo = '26'
            
            print(f"🏛️ Habilitando departamento {quindio_codigo} (QUINDÍO)...")
            
            # Habilitar como principal
            resultado = DepartamentoService.habilitar_departamento(
                departamento_codigo=quindio_codigo,
                es_principal=True,
                auto_cargar=True
            )
            
            print("✅ Quindío habilitado como departamento principal")
            
            # Mostrar resultado
            config = resultado['config']
            carga = resultado.get('carga')
            
            print(f"\n📊 CONFIGURACIÓN:")
            print(f"   • Departamento: {config['departamento_nombre']}")
            print(f"   • Código: {config['departamento_codigo']}")
            print(f"   • Habilitado: {'Sí' if config['habilitado'] else 'No'}")
            print(f"   • Principal: {'Sí' if config['es_principal'] else 'No'}")
            
            if carga:
                print(f"\n📍 DATOS CARGADOS:")
                print(f"   • Municipios: {carga['ubicaciones']['municipios']}")
                print(f"   • Puestos: {carga['ubicaciones']['puestos']}")
                print(f"   • Mesas: {carga['ubicaciones']['mesas_creadas']}")
                print(f"   • Usuarios creados:")
                for rol, cantidad in carga['usuarios'].items():
                    print(f"     - {rol}: {cantidad}")
                
                total_usuarios = sum(carga['usuarios'].values())
                print(f"   • Total usuarios: {total_usuarios}")
            
            # Verificar estado final
            config_final = DepartamentoConfig.query.filter_by(
                departamento_codigo=quindio_codigo
            ).first()
            
            if config_final:
                config_final.actualizar_estadisticas()
                db.session.commit()
                
                print(f"\n📈 ESTADÍSTICAS FINALES:")
                print(f"   • Municipios: {config_final.total_municipios}")
                print(f"   • Puestos: {config_final.total_puestos}")
                print(f"   • Mesas: {config_final.total_mesas}")
                print(f"   • Usuarios: {config_final.total_usuarios_creados}")
            
            print("\n" + "=" * 60)
            print("🎉 QUINDÍO HABILITADO EXITOSAMENTE COMO PRINCIPAL")
            print("=" * 60)
            print("\n💡 INSTRUCCIONES:")
            print("1. Reiniciar el servidor web si está ejecutándose")
            print("2. Acceder al dashboard de Super Admin")
            print("3. Ir a la sección 'Departamentos'")
            print("4. Verificar que el Quindío aparece como principal")
            print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

if __name__ == '__main__':
    success = habilitar_quindio_principal()
    sys.exit(0 if success else 1)