#!/usr/bin/env python3
"""
Script para verificar el estado de los departamentos
"""
import sys
import os
sys.path.append('backend')

try:
    from models.departamento_config import DepartamentoConfig
    from database import db
    from app import create_app
    
    def main():
        print("🏛️ Verificando estado de departamentos...")
        
        app = create_app()
        with app.app_context():
            try:
                configs = DepartamentoConfig.query.all()
                print(f'📊 Departamentos configurados: {len(configs)}')
                
                if len(configs) == 0:
                    print("⚠️  No hay departamentos configurados")
                    return
                
                for config in configs:
                    estado = "HABILITADO" if config.habilitado else "DESHABILITADO"
                    principal = " (PRINCIPAL)" if config.es_principal else ""
                    print(f'🏛️  {config.departamento_nombre} ({config.departamento_codigo}): {estado}{principal}')
                    print(f'   📍 Municipios: {config.total_municipios}, Puestos: {config.total_puestos}, Mesas: {config.total_mesas}')
                    print(f'   👥 Usuarios: {config.total_usuarios_creados}')
                    if config.ultima_carga_at:
                        print(f'   📅 Última carga: {config.ultima_carga_at}')
                    print()
                    
            except Exception as e:
                print(f"❌ Error consultando departamentos: {e}")
                
    if __name__ == '__main__':
        main()
        
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")