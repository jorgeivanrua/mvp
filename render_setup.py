#!/usr/bin/env python
"""
Setup para Render.com
Inicializa la base de datos y carga datos iniciales
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "="*70)
    print("INICIALIZACIÓN EN RENDER")
    print("="*70)
    
    try:
        # Importar después de agregar al path
        from backend.app import create_app
        from backend.database import db
        
        # Crear aplicación
        app = create_app()
        
        with app.app_context():
            print("\n📦 Creando tablas de base de datos...")
            db.create_all()
            print("   ✅ Tablas creadas")
            
            # Ejecutar script de inicialización automática
            print("\n🚀 Ejecutando inicialización automática de datos...")
            
            # Importar y ejecutar el script de inicialización
            from scripts.inicializar_datos_automatico import (
                cargar_divipola_basico,
                cargar_tipos_eleccion,
                cargar_partidos_basicos,
                cargar_candidatos_basicos,
                cargar_usuarios_basicos
            )
            
            # Cargar datos en orden
            resultados = {
                'divipola': cargar_divipola_basico(),
                'tipos_eleccion': cargar_tipos_eleccion(),
                'partidos': cargar_partidos_basicos(),
                'candidatos': cargar_candidatos_basicos(),
                'usuarios': cargar_usuarios_basicos(),
            }
            
            print("\n" + "="*70)
            print("RESUMEN DE INICIALIZACIÓN")
            print("="*70)
            
            print("\n📊 Estado:")
            for nombre, estado in resultados.items():
                icono = "✅" if estado else "❌"
                print(f"  {icono} {nombre.capitalize()}: {'OK' if estado else 'ERROR'}")
            
            todos_ok = all(resultados.values())
            
            if todos_ok:
                print("\n🎉 ¡RENDER INICIALIZADO CORRECTAMENTE!")
                print("\n📝 Credenciales de acceso:")
                print("   Monitoreo: monitoreo / Monitoreo2025!")
                print("   Auditor: auditor / test123")
                print("   Coordinadores: coord_dept, coord_mun, coord_puesto / test123")
                print("   Testigo: testigo1 / test123")
            else:
                print("\n⚠️  ALGUNOS DATOS NO SE PUDIERON CARGAR")
                sys.exit(1)
            
            print("\n" + "="*70)
            print("✅ Setup completado exitosamente")
            print("="*70 + "\n")
            
    except Exception as e:
        print(f"\n❌ Error durante el setup: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
