#!/usr/bin/env python3
"""
Script para generar lista de testigos electorales con sus cédulas
Útil para distribución y gestión de credenciales
"""
import sys
import os
import csv
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath('.'))

try:
    from backend.app import create_app
    from backend.database import db
    from backend.models.location import Location
    from backend.models.user import User
    from backend.models.departamento_config import DepartamentoConfig
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)


def generar_lista_testigos(departamento_codigo=None, formato='csv'):
    """
    Generar lista de testigos electorales con sus credenciales
    
    Args:
        departamento_codigo: Código del departamento (None para todos)
        formato: 'csv', 'txt' o 'console'
    """
    app = create_app()
    
    with app.app_context():
        print("📋 GENERANDO LISTA DE TESTIGOS ELECTORALES")
        print("=" * 60)
        
        # Construir query base
        query = db.session.query(
            User.nombre,
            User.cedula,
            Location.departamento_nombre,
            Location.municipio_nombre,
            Location.puesto_nombre,
            Location.mesa_nombre,
            Location.mesa_codigo,
            Location.direccion
        ).join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'testigo_electoral',
            User.activo == True,
            Location.tipo == 'mesa'
        )
        
        # Filtrar por departamento si se especifica
        if departamento_codigo:
            query = query.filter(Location.departamento_codigo == departamento_codigo)
            
            # Obtener nombre del departamento
            depto_config = DepartamentoConfig.query.filter_by(
                departamento_codigo=departamento_codigo
            ).first()
            
            if depto_config:
                print(f"📍 Departamento: {depto_config.departamento_nombre}")
            else:
                print(f"📍 Departamento: Código {departamento_codigo}")
        else:
            print("📍 Todos los departamentos")
        
        # Ordenar por ubicación
        testigos = query.order_by(
            Location.departamento_nombre,
            Location.municipio_nombre,
            Location.puesto_nombre,
            Location.mesa_nombre
        ).all()
        
        if not testigos:
            print("❌ No se encontraron testigos electorales")
            return
        
        print(f"👥 Total testigos encontrados: {len(testigos)}")
        print()
        
        # Generar según formato
        if formato == 'console':
            _mostrar_en_consola(testigos)
        elif formato == 'csv':
            archivo = _generar_csv(testigos, departamento_codigo)
            print(f"📄 Lista guardada en: {archivo}")
        elif formato == 'txt':
            archivo = _generar_txt(testigos, departamento_codigo)
            print(f"📄 Lista guardada en: {archivo}")
        else:
            print("❌ Formato no válido. Use: console, csv, txt")


def _mostrar_en_consola(testigos):
    """Mostrar lista en consola"""
    print("📋 LISTA DE TESTIGOS ELECTORALES")
    print("=" * 100)
    print(f"{'CÉDULA':<12} {'USUARIO':<20} {'MUNICIPIO':<20} {'PUESTO':<25} {'MESA':<15}")
    print("-" * 100)
    
    depto_actual = None
    municipio_actual = None
    
    for testigo in testigos:
        # Separador por departamento
        if depto_actual != testigo.departamento_nombre:
            depto_actual = testigo.departamento_nombre
            print(f"\n🏛️  {depto_actual}")
            print("-" * 100)
        
        # Separador por municipio
        if municipio_actual != testigo.municipio_nombre:
            municipio_actual = testigo.municipio_nombre
            print(f"\n📍 {municipio_actual}")
        
        print(f"{testigo.cedula:<12} {testigo.nombre:<20} {testigo.municipio_nombre:<20} {testigo.puesto_nombre:<25} {testigo.mesa_nombre:<15}")
    
    print("\n" + "=" * 100)
    print("🔐 CONTRASEÑA UNIVERSAL: test123")
    print("💡 Los testigos deben usar su cédula como nombre de usuario")


def _generar_csv(testigos, departamento_codigo):
    """Generar archivo CSV"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if departamento_codigo:
        filename = f"testigos_{departamento_codigo}_{timestamp}.csv"
    else:
        filename = f"testigos_todos_{timestamp}.csv"
    
    filepath = os.path.join('data', filename)
    
    # Crear directorio si no existe
    os.makedirs('data', exist_ok=True)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Encabezados
        writer.writerow([
            'CEDULA',
            'USUARIO',
            'DEPARTAMENTO',
            'MUNICIPIO', 
            'PUESTO',
            'MESA',
            'CODIGO_MESA',
            'DIRECCION',
            'CONTRASEÑA'
        ])
        
        # Datos
        for testigo in testigos:
            writer.writerow([
                testigo.cedula,
                testigo.nombre,
                testigo.departamento_nombre,
                testigo.municipio_nombre,
                testigo.puesto_nombre,
                testigo.mesa_nombre,
                testigo.mesa_codigo,
                testigo.direccion or '',
                'test123'
            ])
    
    return filepath


def _generar_txt(testigos, departamento_codigo):
    """Generar archivo de texto formateado"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if departamento_codigo:
        filename = f"testigos_{departamento_codigo}_{timestamp}.txt"
    else:
        filename = f"testigos_todos_{timestamp}.txt"
    
    filepath = os.path.join('data', filename)
    
    # Crear directorio si no existe
    os.makedirs('data', exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as txtfile:
        txtfile.write("LISTA DE TESTIGOS ELECTORALES\n")
        txtfile.write("=" * 80 + "\n")
        txtfile.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        txtfile.write(f"Total testigos: {len(testigos)}\n")
        txtfile.write("=" * 80 + "\n\n")
        
        depto_actual = None
        municipio_actual = None
        contador_depto = 0
        contador_municipio = 0
        
        for testigo in testigos:
            # Separador por departamento
            if depto_actual != testigo.departamento_nombre:
                if depto_actual is not None:
                    txtfile.write(f"\nSubtotal {depto_actual}: {contador_depto} testigos\n")
                
                depto_actual = testigo.departamento_nombre
                contador_depto = 0
                txtfile.write(f"\n🏛️  DEPARTAMENTO: {depto_actual}\n")
                txtfile.write("-" * 80 + "\n")
            
            # Separador por municipio
            if municipio_actual != testigo.municipio_nombre:
                if municipio_actual is not None and contador_municipio > 0:
                    txtfile.write(f"   Subtotal {municipio_actual}: {contador_municipio} testigos\n\n")
                
                municipio_actual = testigo.municipio_nombre
                contador_municipio = 0
                txtfile.write(f"\n📍 MUNICIPIO: {municipio_actual}\n")
            
            # Datos del testigo
            txtfile.write(f"   Cédula: {testigo.cedula}\n")
            txtfile.write(f"   Usuario: {testigo.nombre}\n")
            txtfile.write(f"   Puesto: {testigo.puesto_nombre}\n")
            txtfile.write(f"   Mesa: {testigo.mesa_nombre} ({testigo.mesa_codigo})\n")
            if testigo.direccion:
                txtfile.write(f"   Dirección: {testigo.direccion}\n")
            txtfile.write(f"   Contraseña: test123\n")
            txtfile.write("   " + "-" * 40 + "\n")
            
            contador_depto += 1
            contador_municipio += 1
        
        # Totales finales
        if municipio_actual and contador_municipio > 0:
            txtfile.write(f"   Subtotal {municipio_actual}: {contador_municipio} testigos\n\n")
        
        if depto_actual and contador_depto > 0:
            txtfile.write(f"Subtotal {depto_actual}: {contador_depto} testigos\n")
        
        txtfile.write("\n" + "=" * 80 + "\n")
        txtfile.write("INSTRUCCIONES DE USO:\n")
        txtfile.write("- Los testigos deben usar su CÉDULA como nombre de usuario\n")
        txtfile.write("- La contraseña universal es: test123\n")
        txtfile.write("- Cada testigo está asignado a una mesa específica\n")
        txtfile.write("- Verificar la ubicación antes de distribuir credenciales\n")
    
    return filepath


def main():
    """Función principal con opciones de línea de comandos"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generar lista de testigos electorales')
    parser.add_argument('--departamento', '-d', help='Código del departamento (ej: 26 para Quindío)')
    parser.add_argument('--formato', '-f', choices=['console', 'csv', 'txt'], 
                       default='console', help='Formato de salida')
    parser.add_argument('--todos', action='store_true', 
                       help='Generar para todos los departamentos')
    
    args = parser.parse_args()
    
    # Determinar departamento
    departamento_codigo = None
    if not args.todos and args.departamento:
        departamento_codigo = args.departamento.strip().zfill(2)
    
    try:
        generar_lista_testigos(departamento_codigo, args.formato)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()