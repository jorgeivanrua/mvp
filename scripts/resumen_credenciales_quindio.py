#!/usr/bin/env python3
"""
Script para generar resumen ejecutivo de credenciales del Quindío
Incluye coordinadores y estadísticas de testigos
"""
import sys
import os
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
    sys.exit(1)


def generar_resumen_credenciales():
    """Generar resumen ejecutivo de credenciales del Quindío"""
    app = create_app()
    
    with app.app_context():
        print("🏛️  RESUMEN EJECUTIVO DE CREDENCIALES - QUINDÍO")
        print("=" * 70)
        print(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Obtener configuración del departamento
        config = DepartamentoConfig.query.filter_by(
            departamento_codigo='26'
        ).first()
        
        if not config:
            print("❌ Quindío no está configurado en el sistema")
            return
        
        print(f"📍 Departamento: {config.departamento_nombre}")
        print(f"📊 Estado: {'HABILITADO' if config.habilitado else 'DESHABILITADO'}")
        print(f"⭐ Principal: {'SÍ' if config.es_principal else 'NO'}")
        print()
        
        # COORDINADORES
        print("👥 COORDINADORES DEL SISTEMA")
        print("-" * 70)
        
        # Coordinador Departamental
        coord_depto = User.query.join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'coordinador_departamental',
            Location.departamento_codigo == '26',
            User.activo == True
        ).first()
        
        if coord_depto:
            ubicacion = Location.query.get(coord_depto.ubicacion_id)
            print("🏛️  COORDINADOR DEPARTAMENTAL:")
            print(f"   Usuario: {coord_depto.nombre}")
            print(f"   Contraseña: test123")
            print(f"   Ubicación: {ubicacion.nombre_completo if ubicacion else 'N/A'}")
            print()
        
        # Coordinadores Municipales
        coords_municipales = User.query.join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'coordinador_municipal',
            Location.departamento_codigo == '26',
            User.activo == True
        ).order_by(Location.municipio_nombre).all()
        
        print(f"🏢 COORDINADORES MUNICIPALES ({len(coords_municipales)}):")
        for coord in coords_municipales:
            ubicacion = Location.query.get(coord.ubicacion_id)
            municipio = ubicacion.municipio_nombre if ubicacion else 'N/A'
            print(f"   • {municipio}: {coord.nombre} (test123)")
        print()
        
        # Estadísticas de Coordinadores de Puesto
        coords_puesto = User.query.join(
            Location, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'coordinador_puesto',
            Location.departamento_codigo == '26',
            User.activo == True
        ).count()
        
        print(f"🏪 COORDINADORES DE PUESTO: {coords_puesto}")
        print("   Contraseña universal: test123")
        print("   (Ver lista detallada con: python scripts/generar_lista_testigos.py)")
        print()
        
        # TESTIGOS ELECTORALES
        print("🗳️  TESTIGOS ELECTORALES")
        print("-" * 70)
        
        # Estadísticas por municipio
        testigos_por_municipio = db.session.query(
            Location.municipio_nombre,
            db.func.count(User.id).label('total_testigos')
        ).join(
            User, User.ubicacion_id == Location.id
        ).filter(
            User.rol == 'testigo_electoral',
            Location.departamento_codigo == '26',
            User.activo == True
        ).group_by(
            Location.municipio_nombre
        ).order_by(
            Location.municipio_nombre
        ).all()
        
        total_testigos = sum(t.total_testigos for t in testigos_por_municipio)
        
        print(f"📊 TOTAL TESTIGOS: {total_testigos}")
        print()
        print("📍 DISTRIBUCIÓN POR MUNICIPIO:")
        for municipio in testigos_por_municipio:
            print(f"   • {municipio.municipio_nombre}: {municipio.total_testigos} testigos")
        print()
        
        # Información de acceso
        print("🔐 INFORMACIÓN DE ACCESO")
        print("-" * 70)
        print("• CONTRASEÑA UNIVERSAL: test123")
        print("• Los testigos usan su CÉDULA como nombre de usuario")
        print("• Los coordinadores usan su NOMBRE DE USUARIO asignado")
        print()
        
        # Archivos generados
        print("📄 ARCHIVOS DISPONIBLES")
        print("-" * 70)
        print("• Lista completa CSV: python scripts/generar_lista_testigos.py -d 26 -f csv")
        print("• Lista completa TXT: python scripts/generar_lista_testigos.py -d 26 -f txt")
        print("• Ver en consola: python scripts/generar_lista_testigos.py -d 26 -f console")
        print()
        
        # Instrucciones de distribución
        print("📋 INSTRUCCIONES DE DISTRIBUCIÓN")
        print("-" * 70)
        print("1. Cada testigo debe recibir:")
        print("   - Su número de cédula (usuario)")
        print("   - La contraseña: test123")
        print("   - Su ubicación específica (municipio, puesto, mesa)")
        print()
        print("2. Verificar antes de distribuir:")
        print("   - Que la cédula corresponda a la mesa asignada")
        print("   - Que el testigo conozca su ubicación física")
        print("   - Que tenga acceso al sistema el día de la elección")
        print()
        print("3. Coordinadores deben conocer:")
        print("   - Su nombre de usuario específico")
        print("   - Su área de responsabilidad")
        print("   - Los testigos bajo su supervisión")
        print()
        
        # Contacto de soporte
        print("🆘 SOPORTE TÉCNICO")
        print("-" * 70)
        print("• Para problemas de acceso: Verificar cédula y contraseña")
        print("• Para problemas técnicos: Contactar administrador del sistema")
        print("• Para cambios de asignación: Usar herramientas de administración")
        print()
        
        print("=" * 70)
        print("✅ SISTEMA LISTO PARA OPERACIÓN ELECTORAL")
        print("=" * 70)


if __name__ == '__main__':
    generar_resumen_credenciales()