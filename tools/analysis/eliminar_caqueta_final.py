#!/usr/bin/env python3
"""
Script para eliminar completamente los datos de Caquetá
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.database import db
from backend.app import create_app

def main():
    app = create_app()
    with app.app_context():
        print('=== ELIMINANDO DATOS DE CAQUETÁ - MÉTODO FINAL ===')
        
        try:
            # 1. Eliminar usuarios de Caquetá
            print('🗑️  Eliminando usuarios de Caquetá...')
            result1 = db.session.execute(
                db.text('DELETE FROM users WHERE ubicacion_id IN (SELECT id FROM locations WHERE departamento_codigo = "44")')
            )
            print(f'   - Eliminados {result1.rowcount} usuarios')
            
            # 2. Eliminar ubicaciones de Caquetá
            print('🗑️  Eliminando ubicaciones de Caquetá...')
            result2 = db.session.execute(
                db.text('DELETE FROM locations WHERE departamento_codigo = "44"')
            )
            print(f'   - Eliminadas {result2.rowcount} ubicaciones')
            
            # Commit cambios
            db.session.commit()
            print('✅ Eliminación completada exitosamente')
            
            # Verificar estado final
            print('\n=== VERIFICACIÓN FINAL ===')
            
            # Contar departamentos restantes
            deptos = db.session.execute(
                db.text('SELECT departamento_codigo, departamento_nombre FROM locations WHERE tipo = "departamento" AND activo = 1 GROUP BY departamento_codigo, departamento_nombre')
            ).fetchall()
            
            print(f'📍 Departamentos restantes: {len(deptos)}')
            for codigo, nombre in deptos:
                # Contar por tipo
                municipios = db.session.execute(
                    db.text('SELECT COUNT(*) FROM locations WHERE departamento_codigo = ? AND tipo = "municipio" AND activo = 1'),
                    [codigo]
                ).scalar()
                
                puestos = db.session.execute(
                    db.text('SELECT COUNT(*) FROM locations WHERE departamento_codigo = ? AND tipo = "puesto" AND activo = 1'),
                    [codigo]
                ).scalar()
                
                mesas = db.session.execute(
                    db.text('SELECT COUNT(*) FROM locations WHERE departamento_codigo = ? AND tipo = "mesa" AND activo = 1'),
                    [codigo]
                ).scalar()
                
                print(f'  - {nombre} ({codigo}): {municipios} municipios, {puestos} puestos, {mesas} mesas')
            
            # Contar usuarios totales
            total_usuarios = db.session.execute(
                db.text('SELECT COUNT(*) FROM users WHERE activo = 1')
            ).scalar()
            print(f'👥 Total usuarios activos: {total_usuarios}')
            
            print('\n✅ SISTEMA LIMPIO - Solo Quindío permanece')
            
        except Exception as e:
            print(f'❌ Error: {e}')
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()