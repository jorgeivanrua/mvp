#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

app = create_app()
with app.app_context():
    print("\n🔍 VERIFICANDO COORDINADOR ESPECÍFICO")
    print("="*60)
    
    # Buscar la ubicación específica que está seleccionando
    ubicacion = Location.query.filter_by(
        tipo='puesto',
        departamento_codigo='26',
        municipio_codigo='2601',
        zona_codigo='260101',
        puesto_codigo='26010103'  # IE INSTITUTO TECNICO INDUSTRIAL
    ).first()
    
    if ubicacion:
        print(f"✅ UBICACIÓN ENCONTRADA:")
        print(f"   - ID: {ubicacion.id}")
        print(f"   - Nombre: {ubicacion.puesto_nombre}")
        print(f"   - Código completo: {ubicacion.departamento_codigo}-{ubicacion.municipio_codigo}-{ubicacion.zona_codigo}-{ubicacion.puesto_codigo}")
        
        # Buscar coordinador para esta ubicación
        coordinador = User.query.filter_by(
            rol='coordinador_puesto',
            ubicacion_id=ubicacion.id,
            activo=True
        ).first()
        
        if coordinador:
            print(f"\n✅ COORDINADOR ENCONTRADO:")
            print(f"   - ID: {coordinador.id}")
            print(f"   - Nombre: {coordinador.nombre}")
            print(f"   - Rol: {coordinador.rol}")
            print(f"   - Activo: {coordinador.activo}")
            print(f"   - Ubicación ID: {coordinador.ubicacion_id}")
            
            # Verificar contraseña
            pwd_ok = coordinador.check_password('test123')
            print(f"   - Password 'test123': {'✅ CORRECTO' if pwd_ok else '❌ INCORRECTO'}")
            
            if not pwd_ok:
                # Probar otras contraseñas comunes
                for pwd in ['admin123', 'password', '123456', coordinador.nombre.lower()]:
                    if coordinador.check_password(pwd):
                        print(f"   - Password '{pwd}': ✅ CORRECTO")
                        break
        else:
            print(f"\n❌ NO HAY COORDINADOR ASIGNADO A ESTA UBICACIÓN")
            print(f"   - Ubicación ID: {ubicacion.id}")
            print(f"   - Nombre: {ubicacion.puesto_nombre}")
            
            # Buscar coordinadores cercanos
            print(f"\n🔍 COORDINADORES EN LA MISMA ZONA:")
            coords_zona = User.query.filter_by(
                rol='coordinador_puesto',
                activo=True
            ).all()
            
            for coord in coords_zona:
                if coord.ubicacion_id:
                    loc = Location.query.get(coord.ubicacion_id)
                    if loc and loc.zona_codigo == '260101':
                        zona_numero = loc.zona_codigo[-2:] if len(loc.zona_codigo) >= 2 else loc.zona_codigo
                        print(f"   - {coord.nombre} → {loc.puesto_nombre} (ID: {loc.id})")
                        print(f"     Código: {loc.puesto_codigo}")
                        pwd_ok = coord.check_password('test123')
                        print(f"     Password: {'✅' if pwd_ok else '❌'}")
    else:
        print(f"❌ UBICACIÓN NO ENCONTRADA")
        print(f"   - Buscando: 26-2601-260101-26010103")
        
        # Buscar ubicaciones similares
        print(f"\n🔍 UBICACIONES EN LA ZONA 260101:")
        ubicaciones_zona = Location.query.filter_by(
            tipo='puesto',
            departamento_codigo='26',
            municipio_codigo='2601',
            zona_codigo='260101'
        ).all()
        
        for ub in ubicaciones_zona:
            print(f"   - {ub.puesto_codigo}: {ub.puesto_nombre}")
    
    print("\n" + "="*60)