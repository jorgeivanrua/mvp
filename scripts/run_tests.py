#!/usr/bin/env python3
"""
Script para ejecutar tests de manera organizada
"""
import subprocess
import sys
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🧪 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Ejecutar tests del sistema electoral")
    parser.add_argument("--type", choices=["unit", "integration", "frontend", "all"], 
                       default="all", help="Tipo de tests a ejecutar")
    parser.add_argument("--coverage", action="store_true", help="Generar reporte de cobertura")
    parser.add_argument("--verbose", "-v", action="store_true", help="Salida verbose")
    parser.add_argument("--file", help="Archivo específico de test")
    
    args = parser.parse_args()
    
    # Verificar que estamos en el directorio correcto
    if not Path("pytest.ini").exists():
        print("❌ Error: Ejecutar desde la raíz del proyecto")
        sys.exit(1)
    
    # Construir comando base
    base_cmd = "pytest"
    
    if args.verbose:
        base_cmd += " -v"
    
    if args.coverage:
        base_cmd += " --cov=backend --cov-report=html --cov-report=term-missing"
    
    # Ejecutar tests según el tipo
    success = True
    
    if args.file:
        # Test específico
        cmd = f"{base_cmd} {args.file}"
        success = run_command(cmd, f"Ejecutando test específico: {args.file}")
    
    elif args.type == "unit":
        cmd = f"{base_cmd} tests/unit/"
        success = run_command(cmd, "Ejecutando tests unitarios")
    
    elif args.type == "integration":
        cmd = f"{base_cmd} tests/integration/"
        success = run_command(cmd, "Ejecutando tests de integración")
    
    elif args.type == "frontend":
        print("\n🌐 Tests de Frontend")
        print("=" * 50)
        print("Los tests de frontend se ejecutan con herramientas específicas:")
        print("- Jest para JavaScript")
        print("- Cypress para E2E")
        print("- Selenium para automatización")
        
    elif args.type == "all":
        # Ejecutar todos los tests
        tests = [
            ("tests/unit/", "Tests Unitarios"),
            ("tests/integration/", "Tests de Integración"),
        ]
        
        for test_path, description in tests:
            if Path(test_path).exists():
                cmd = f"{base_cmd} {test_path}"
                if not run_command(cmd, description):
                    success = False
    
    # Mostrar resumen
    print("\n" + "=" * 50)
    if success:
        print("✅ Todos los tests pasaron exitosamente")
        if args.coverage:
            print("📊 Reporte de cobertura generado en htmlcov/")
    else:
        print("❌ Algunos tests fallaron")
        sys.exit(1)

if __name__ == "__main__":
    main()