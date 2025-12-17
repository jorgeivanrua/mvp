#!/usr/bin/env python3
"""
Asignar cédulas temporales a todos los testigos de Quindío
"""
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.app import create_app
import random

def generar_cedula_temporal():
    """Generar una cédula temporal válida"""
    # Generar número de 8-10 dígitos
    cedula = random.randint(10000000, 99999999)
    return str(cedula)

def main():
    app = create_app()
    with app.app_context():
        print('=== ASIGNANDO CÉDULAS TEMPORALES A TESTIGOS DE QUINDÍO ===')
        
        try:
            # Obtener todas las ubicaciones de Quindío
            ubicaciones_quindio = Location.query.filter_by(
                departamento_codigo='26',
                activo=True
            ).all()
            
            ubicaciones_ids = [loc.id for loc in ubicaciones_quindio]
            
            # Obtener testigos de Quindío sin cédula
            testigos_sin_cedula = User.query.filter(
                User.rol == 'testigo_electoral',
                User.ubicacion_id.in_(ubicaciones_ids),
                User.activo == True,
                db.or_(User.cedula == None, User.cedula == '', User.cedula == 'Sin cédula')
            ).all()
            
            print(f'📊 Testigos sin cédula encontrados: {len(testigos_sin_cedula)}')
            
            # Generar cédulas únicas
            cedulas_usadas = set()
            
            # Obtener cédulas ya existentes
            cedulas_existentes = db.session.query(User.cedula).filter(
                User.cedula != None,
                User.cedula != '',
                User.cedula != 'Sin cédula'
            ).all()
            
            for cedula_tuple in cedulas_existentes:
                if cedula_tuple[0]:
                    cedulas_usadas.add(cedula_tuple[0])
            
            print(f'📋 Cédulas ya existentes en el sistema: {len(cedulas_usadas)}')
            
            # Asignar cédulas a testigos
            testigos_actualizados = 0
            
            for testigo in testigos_sin_cedula:
                # Generar cédula única
                while True:
                    cedula_temporal = generar_cedula_temporal()
                    if cedula_temporal not in cedulas_usadas:
                        cedulas_usadas.add(cedula_temporal)
                        break
                
                # Asignar cédula al testigo
                testigo.cedula = cedula_temporal
                testigos_actualizados += 1
                
                # Obtener información de ubicación para el log
                ubicacion = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
                ubicacion_info = ubicacion.nombre_completo if ubicacion else 'Sin ubicación'
                
                print(f'  ✅ {testigo.nombre} → Cédula: {cedula_temporal} | {ubicacion_info}')
                
                # Commit cada 50 registros para evitar problemas
                if testigos_actualizados % 50 == 0:
                    db.session.commit()
                    print(f'    💾 Guardados {testigos_actualizados} testigos...')
            
            # Commit final
            db.session.commit()
            
            print(f'\n✅ PROCESO COMPLETADO')
            print(f'📊 Total testigos actualizados: {testigos_actualizados}')
            
            # Verificar resultado
            testigos_con_cedula = User.query.filter(
                User.rol == 'testigo_electoral',
                User.ubicacion_id.in_(ubicaciones_ids),
                User.activo == True,
                User.cedula != None,
                User.cedula != '',
                User.cedula != 'Sin cédula'
            ).count()
            
            print(f'✅ Testigos con cédula ahora: {testigos_con_cedula}')
            
            # Mostrar algunos ejemplos
            print(f'\n🔍 EJEMPLOS DE TESTIGOS CON CÉDULAS:')
            ejemplos = User.query.filter(
                User.rol == 'testigo_electoral',
                User.ubicacion_id.in_(ubicaciones_ids),
                User.activo == True,
                User.cedula != None,
                User.cedula != '',
                User.cedula != 'Sin cédula'
            ).limit(10).all()
            
            for testigo in ejemplos:
                ubicacion = Location.query.get(testigo.ubicacion_id) if testigo.ubicacion_id else None
                ubicacion_info = ubicacion.nombre_completo if ubicacion else 'Sin ubicación'
                print(f'  • {testigo.nombre} | Cédula: {testigo.cedula} | {ubicacion_info}')
            
        except Exception as e:
            print(f'❌ Error: {e}')
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()