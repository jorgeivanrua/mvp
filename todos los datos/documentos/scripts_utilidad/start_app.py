"""
Script robusto para iniciar la aplicación
"""
import sys
import os

# Asegurar que estamos en el directorio correcto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    print("=" * 60)
    print("INICIANDO SISTEMA ELECTORAL")
    print("=" * 60)
    
    # Importar la aplicación
    print("\n[1/3] Importando módulos...")
    from backend.app import create_app
    print("✓ Módulos importados correctamente")
    
    # Crear la aplicación
    print("\n[2/3] Creando aplicación...")
    app = create_app('development')
    print("✓ Aplicación creada correctamente")
    
    # Iniciar el servidor
    print("\n[3/3] Iniciando servidor...")
    print("\n" + "=" * 60)
    print("SERVIDOR INICIADO EXITOSAMENTE")
    print("=" * 60)
    print(f"\n✓ URL: http://127.0.0.1:5000")
    print(f"✓ Debug: {app.config['DEBUG']}")
    print(f"✓ Templates: {app.template_folder}")
    print(f"✓ Static: {app.static_folder}")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    print("=" * 60 + "\n")
    
    # Ejecutar
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
    
except KeyboardInterrupt:
    print("\n\n" + "=" * 60)
    print("SERVIDOR DETENIDO")
    print("=" * 60)
    sys.exit(0)
    
except Exception as e:
    print("\n\n" + "=" * 60)
    print("ERROR AL INICIAR LA APLICACIÓN")
    print("=" * 60)
    print(f"\nError: {e}")
    print("\nDetalles:")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    sys.exit(1)
