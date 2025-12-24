#!/usr/bin/env python3
"""
Corregir ubicación de testigos: mover de mesas a puestos de votación
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.app import create_app

def main():
    app = create_app()
    with app.app_context():
        print('=== CORRIGIENDO UBICACIÓN DE TESTIGOS ===')
        print('Moviendo testigos de MESAS a PUESTOS de votación')
        
        try:
            # Obtener todos los testigos que están asignados a mesas
            testigos_en_mesas = db.session.query(User, Location).join(
                Location, User.ubicacion_id == Location.id
            ).filter(
                User.rol == 'testigo_electoral',
                User.activo == True,
                Location.tipo == 'mesa',
                Location.departamento_codigo == '26'
            ).all()
            
            print(f'📊 Testigos en mesas encontrados: {len(testigos_en_mesas)}')
            
            testigos_actualizados = 0
            puestos_procesados = set()
            
            for testigo, mesa in testigos_en_mesas:
                # Buscar el puesto correspondiente a esta mesa
                puesto = Location.query.filter_by(
                    tipo='puesto',
                    departamento_codigo=mesa.departamento_codigo,
                    municipio_codigo=mesa.municipio_codigo,
                    zona_codigo=mesa.zona_codigo,
                    puesto_codigo=mesa.puesto_codigo,
                    activo=True
                ).first()
                
                if puesto:
                    # Actualizar la ubicación del testigo al puesto
                    testigo.ubicacion_id = puesto.id
                    testigos_actualizados += 1
                    
                    if puesto.id not in puestos_procesados:
                        puestos_procesados.add(puesto.id)
                        print(f'  ✅ Puesto: {puesto.puesto_nombre}')
                        print(f'     Ubicación: {puesto.nombre_completo}')
                    
                    # Commit cada 50 registros
                    if testigos_actualizados % 50 == 0:
                        db.session.commit()
                        print(f'    💾 Guardados {testigos_actualizados} testigos...')
                else:
                    print(f'  ❌ No se encontró puesto para mesa: {mesa.nombre_completo}')
            
            # Commit final
            db.session.commit()
            
            print(f'\n✅ CORRECCIÓN COMPLETADA')
            print(f'📊 Testigos actualizados: {testigos_actualizados}')
            print(f'🏢 Puestos únicos procesados: {len(puestos_procesados)}')
            
            # Verificar resultado
            print(f'\n=== VERIFICACIÓN POST-CORRECCIÓN ===')
            
            # Contar testigos por tipo de ubicación después de la corrección
            ubicaciones_testigos = db.session.query(Location.tipo, db.func.count(User.id)).join(
                User, User.ubicacion_id == Location.id
            ).filter(
                User.rol == 'testigo_electoral',
                User.activo == True,
                Location.departamento_codigo == '26'
            ).group_by(Location.tipo).all()
            
            print('📋 DISTRIBUCIÓN FINAL POR TIPO DE UBICACIÓN:')
            for tipo, cantidad in ubicaciones_testigos:
                print(f'  - {tipo}: {cantidad} testigos')
            
            # Mostrar algunos ejemplos
            print(f'\n🔍 EJEMPLOS DE TESTIGOS EN PUESTOS:')
            ejemplos = db.session.query(User, Location).join(
                Location, User.ubicacion_id == Location.id
            ).filter(
                User.rol == 'testigo_electoral',
                User.activo == True,
                Location.tipo == 'puesto',
                Location.departamento_codigo == '26'
            ).limit(5).all()
            
            for testigo, puesto in ejemplos:
                print(f'  • {testigo.nombre} | Cédula: {testigo.cedula}')
                print(f'    Puesto: {puesto.puesto_nombre}')
                print(f'    Ubicación: {puesto.nombre_completo}')
                print()
            
        except Exception as e:
            print(f'❌ Error: {e}')
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()