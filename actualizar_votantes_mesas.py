#!/usr/bin/env python3
"""
Script para actualizar los datos de votantes en las mesas desde el archivo CSV
"""

import os
import csv
from backend.app import create_app
from backend.models.location import Location
from backend.database import db

def actualizar_votantes_mesas():
    """Actualizar datos de votantes desde el archivo CSV"""
    print("🔄 ACTUALIZANDO DATOS DE VOTANTES EN MESAS")
    print("=" * 50)
    
    # Buscar archivo CSV
    csv_paths = ['data/divipola.csv', 'divipola.csv']
    csv_path = None
    for path in csv_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if not csv_path:
        print("❌ ERROR: No se encontró divipola.csv")
        return False
    
    print(f"📁 Archivo CSV: {csv_path}")
    
    # Contar mesas actuales
    total_mesas = Location.query.filter_by(tipo='mesa').count()
    print(f"📊 Total mesas en BD: {total_mesas}")
    
    # Verificar mesas con votantes en 0
    mesas_sin_votantes = Location.query.filter_by(
        tipo='mesa',
        total_votantes_registrados=0
    ).count()
    print(f"⚠️  Mesas con 0 votantes: {mesas_sin_votantes}")
    
    if mesas_sin_votantes == 0:
        print("✅ Todas las mesas ya tienen datos de votantes")
        return True
    
    print(f"\n🔄 Procesando archivo CSV...")
    
    actualizadas = 0
    errores = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                dd = row['dd'].strip().zfill(2)
                
                # Solo procesar Quindío (código 26)
                if dd != '26':
                    continue
                
                mm = row['mm'].strip().zfill(2)
                zz = row['zz'].strip().zfill(2)
                pp = row['pp'].strip().zfill(2)
                mesa = row['mesa'].strip().zfill(2)
                
                mesa_codigo = f"{dd}{mm}{zz}{pp}{mesa}"
                
                # Buscar la mesa en la BD
                mesa_location = Location.query.filter_by(
                    tipo='mesa',
                    mesa_codigo=mesa_codigo
                ).first()
                
                if mesa_location:
                    # Obtener datos de votantes del CSV
                    total_votantes = int(row.get('total_mesa', 0) or 0)
                    mujeres = int(row.get('mujeres_mesa', 0) or 0)
                    hombres = int(row.get('hombres_mesa', 0) or 0)
                    
                    # Solo actualizar si los datos actuales están en 0
                    if mesa_location.total_votantes_registrados == 0:
                        mesa_location.total_votantes_registrados = total_votantes
                        mesa_location.mujeres = mujeres
                        mesa_location.hombres = hombres
                        
                        actualizadas += 1
                        
                        if actualizadas <= 5:  # Mostrar primeros 5 ejemplos
                            print(f"   ✅ Mesa {mesa_codigo}: {total_votantes} votantes ({mujeres}M + {hombres}H)")
                        elif actualizadas == 6:
                            print("   ... (continuando actualizaciones)")
                
                # Commit cada 50 registros
                if actualizadas % 50 == 0 and actualizadas > 0:
                    db.session.commit()
                    print(f"   💾 Guardadas {actualizadas} actualizaciones")
        
        # Commit final
        db.session.commit()
        
        print(f"\n✅ ACTUALIZACIÓN COMPLETADA")
        print(f"   📊 Mesas actualizadas: {actualizadas}")
        print(f"   ❌ Errores: {errores}")
        
        # Verificar resultado
        mesas_con_votantes = Location.query.filter(
            Location.tipo == 'mesa',
            Location.total_votantes_registrados > 0
        ).count()
        
        print(f"\n📈 RESULTADO FINAL:")
        print(f"   🗳️  Mesas con votantes: {mesas_con_votantes}")
        print(f"   📊 Total mesas: {total_mesas}")
        
        # Mostrar ejemplos de mesas actualizadas
        ejemplos = Location.query.filter(
            Location.tipo == 'mesa',
            Location.total_votantes_registrados > 0
        ).limit(3).all()
        
        print(f"\n📋 EJEMPLOS DE MESAS ACTUALIZADAS:")
        for mesa in ejemplos:
            print(f"   • Mesa {mesa.mesa_codigo}: {mesa.total_votantes_registrados} votantes")
            print(f"     {mesa.mesa_nombre}")
            print(f"     Mujeres: {mesa.mujeres}, Hombres: {mesa.hombres}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        db.session.rollback()
        return False

def main():
    """Función principal"""
    app = create_app()
    with app.app_context():
        actualizar_votantes_mesas()

if __name__ == "__main__":
    main()