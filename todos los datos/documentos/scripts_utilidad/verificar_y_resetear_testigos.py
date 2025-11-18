"""
Verificar y resetear contraseñas de testigos a test123
"""
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.app import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("VERIFICACIÓN Y RESETEO DE TESTIGOS")
    print("="*70)
    
    # Buscar todos los testigos
    testigos = User.query.filter_by(rol='testigo_electoral').all()
    
    print(f"\n📋 Testigos encontrados: {len(testigos)}")
    
    if not testigos:
        print("\n⚠️  No hay testigos en el sistema")
    else:
        print("\n" + "-"*70)
        for testigo in testigos:
            print(f"\n👤 Testigo: {testigo.nombre}")
            print(f"   ID: {testigo.id}")
            print(f"   Ubicación ID: {testigo.ubicacion_id}")
            print(f"   Activo: {testigo.activo}")
            
            # Obtener ubicación
            if testigo.ubicacion_id:
                ubicacion = Location.query.get(testigo.ubicacion_id)
                if ubicacion:
                    print(f"   Ubicación: {ubicacion.nombre_completo}")
                    print(f"   Tipo: {ubicacion.tipo}")
            
            # Verificar contraseña actual
            if testigo.check_password('test123'):
                print(f"   ✅ Contraseña actual: test123 (ya configurada)")
            else:
                print(f"   ❌ Contraseña actual: NO es test123")
                print(f"   🔧 Reseteando a test123...")
                testigo.set_password('test123')
                testigo.intentos_fallidos = 0
                testigo.bloqueado_hasta = None
                print(f"   ✅ Contraseña reseteada a: test123")
        
        # Guardar cambios
        db.session.commit()
        print("\n" + "="*70)
        print("✅ CAMBIOS GUARDADOS")
        print("="*70)
        
        # Verificar que funcionó
        print("\n🔍 VERIFICACIÓN FINAL:")
        print("-"*70)
        for testigo in testigos:
            if testigo.check_password('test123'):
                print(f"✅ {testigo.nombre}: Contraseña test123 funciona")
            else:
                print(f"❌ {testigo.nombre}: Contraseña test123 NO funciona")
        
        print("\n" + "="*70)
        print("📝 CREDENCIALES DE TESTIGOS")
        print("="*70)
        print("\nTodos los testigos ahora usan:")
        print("  Password: test123")
        print("\nPara hacer login:")
        print("  1. Seleccionar rol: testigo_electoral")
        print("  2. Seleccionar ubicación (departamento, municipio, zona, puesto)")
        print("  3. Password: test123")
        print("="*70)
