"""
Script de prueba para verificar que la ubicación del Quindío funciona correctamente
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.app import create_app
from backend.models.user import User
from backend.models.location import Location

def test_ubicacion_quindio():
    """Prueba completa de la ubicación del Quindío"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("PRUEBA COMPLETA - UBICACIÓN DEL QUINDÍO")
        print("=" * 70)
        
        # 1. Verificar usuario testigo
        print("\n1. VERIFICANDO USUARIO TESTIGO")
        print("-" * 40)
        
        user = User.query.filter_by(cedula='12345678').first()
        if not user:
            print("❌ Usuario testigo_12345678 no encontrado")
            return False
        
        print(f"✅ Usuario: {user.nombre} (ID: {user.id})")
        print(f"   Cédula: {user.cedula}")
        print(f"   Rol: {user.rol}")
        
        # 2. Verificar ubicación del usuario
        print("\n2. VERIFICANDO UBICACIÓN DEL USUARIO")
        print("-" * 40)
        
        if not user.ubicacion_id:
            print("❌ Usuario sin ubicación asignada")
            return False
        
        location = Location.query.get(user.ubicacion_id)
        if not location:
            print("❌ Ubicación no encontrada")
            return False
        
        print(f"✅ Ubicación: {location.nombre_completo}")
        print(f"   Departamento: {location.departamento_nombre}")
        print(f"   Municipio: {location.municipio_nombre}")
        print(f"   Puesto: {location.puesto_nombre}")
        print(f"   Mesa: {location.mesa_nombre}")
        print(f"   Tipo: {location.tipo}")
        
        # 3. Verificar que es del Quindío
        print("\n3. VERIFICANDO DEPARTAMENTO")
        print("-" * 40)
        
        if location.departamento_nombre != 'QUINDIO':
            print(f"❌ Departamento incorrecto: {location.departamento_nombre}")
            print("   Esperado: QUINDIO")
            return False
        
        print("✅ Departamento correcto: QUINDIO")
        
        # 4. Verificar estructura del Quindío
        print("\n4. VERIFICANDO ESTRUCTURA DEL QUINDÍO")
        print("-" * 40)
        
        # Contar ubicaciones del Quindío
        departamento = Location.query.filter_by(
            departamento_nombre='QUINDIO',
            tipo='departamento'
        ).first()
        
        if not departamento:
            print("❌ Departamento QUINDIO no encontrado")
            return False
        
        municipios = Location.query.filter_by(
            departamento_codigo=departamento.departamento_codigo,
            tipo='municipio'
        ).count()
        
        puestos = Location.query.filter_by(
            departamento_codigo=departamento.departamento_codigo,
            tipo='puesto'
        ).count()
        
        mesas = Location.query.filter_by(
            departamento_codigo=departamento.departamento_codigo,
            tipo='mesa'
        ).count()
        
        print(f"✅ Departamento: {departamento.nombre_completo}")
        print(f"   Código: {departamento.departamento_codigo}")
        print(f"   Municipios: {municipios}")
        print(f"   Puestos: {puestos}")
        print(f"   Mesas: {mesas}")
        
        # Verificar números esperados
        if municipios < 10:
            print(f"⚠️  Pocos municipios: {municipios} (esperado: ~12)")
        
        if puestos < 100:
            print(f"⚠️  Pocos puestos: {puestos} (esperado: ~129)")
        
        if mesas < 200:
            print(f"⚠️  Pocas mesas: {mesas} (esperado: ~212)")
        
        # 5. Verificar usuarios del Quindío
        print("\n5. VERIFICANDO USUARIOS DEL QUINDÍO")
        print("-" * 40)
        
        # Coordinador departamental
        coord_depto = User.query.filter_by(
            rol='coordinador_departamental',
            ubicacion_id=departamento.id
        ).first()
        
        if coord_depto:
            print(f"✅ Coordinador Departamental: {coord_depto.nombre}")
        else:
            print("❌ Coordinador Departamental no encontrado")
        
        # Coordinadores municipales (simplificado)
        municipios_ids = [m.id for m in Location.query.filter_by(
            departamento_codigo=departamento.departamento_codigo,
            tipo='municipio'
        ).all()]
        
        coords_muni = User.query.filter(
            User.rol == 'coordinador_municipal',
            User.ubicacion_id.in_(municipios_ids)
        ).count()
        
        print(f"✅ Coordinadores Municipales: {coords_muni}")
        
        # Coordinadores de puesto (simplificado)
        puestos_ids = [p.id for p in Location.query.filter_by(
            departamento_codigo=departamento.departamento_codigo,
            tipo='puesto'
        ).all()]
        
        coords_puesto = User.query.filter(
            User.rol == 'coordinador_puesto',
            User.ubicacion_id.in_(puestos_ids)
        ).count()
        
        print(f"✅ Coordinadores de Puesto: {coords_puesto}")
        
        # Testigos (simplificado)
        mesas_ids = [m.id for m in Location.query.filter_by(
            departamento_codigo=departamento.departamento_codigo,
            tipo='mesa'
        ).all()]
        
        testigos = User.query.filter(
            User.rol == 'testigo_electoral',
            User.ubicacion_id.in_(mesas_ids)
        ).count()
        
        print(f"✅ Testigos Electorales: {testigos}")
        
        # 6. Resultado final
        print("\n" + "=" * 70)
        print("RESULTADO DE LA PRUEBA")
        print("=" * 70)
        
        if (location.departamento_nombre == 'QUINDIO' and 
            municipios >= 10 and 
            puestos >= 100 and 
            mesas >= 200 and
            coord_depto and
            coords_muni >= 10 and
            coords_puesto >= 100 and
            testigos >= 200):
            
            print("🎉 ¡PRUEBA EXITOSA!")
            print("✅ El usuario testigo está correctamente asignado al QUINDÍO")
            print("✅ La estructura del Quindío está completa")
            print("✅ Los usuarios están correctamente creados")
            print()
            print("📋 DATOS PARA LOGIN:")
            print(f"   Usuario: {user.cedula}")
            print("   Contraseña: test123")
            print(f"   Ubicación: {location.nombre_completo}")
            print()
            print("🌐 INSTRUCCIONES PARA EL USUARIO:")
            print("1. Recargar la página con Ctrl+F5")
            print("2. O usar el botón 'Actualizar Ubicación' en el dashboard")
            print("3. Verificar que muestre QUINDÍO en lugar de CAQUETA")
            
            return True
        else:
            print("❌ PRUEBA FALLIDA")
            print("   Algunos datos no están correctos")
            return False

if __name__ == '__main__':
    success = test_ubicacion_quindio()
    sys.exit(0 if success else 1)