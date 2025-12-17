#!/usr/bin/env python3
"""
Generar lista completa de usuarios de Quindío con credenciales
"""
from backend.database import db
from backend.models.user import User
from backend.models.location import Location
from backend.app import create_app
import csv
from datetime import datetime

def main():
    app = create_app()
    with app.app_context():
        print('=== GENERANDO LISTA DE USUARIOS DE QUINDÍO ===')
        
        try:
            # Obtener todas las ubicaciones de Quindío
            ubicaciones_quindio = Location.query.filter_by(
                departamento_codigo='26',
                activo=True
            ).all()
            
            ubicaciones_ids = [loc.id for loc in ubicaciones_quindio]
            
            # Obtener usuarios de Quindío + super admins
            usuarios_quindio = User.query.filter(
                db.or_(
                    User.ubicacion_id.in_(ubicaciones_ids),
                    User.rol == 'super_admin'
                ),
                User.activo == True
            ).order_by(User.rol, User.nombre).all()
            
            print(f'📊 Total usuarios encontrados: {len(usuarios_quindio)}')
            
            # Crear archivo CSV
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'usuarios_quindio_{timestamp}.csv'
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Encabezados
                writer.writerow([
                    'ID',
                    'Nombre',
                    'Cédula',
                    'Rol',
                    'Contraseña',
                    'Departamento',
                    'Municipio',
                    'Zona',
                    'Puesto',
                    'Mesa',
                    'Ubicación Completa',
                    'Activo',
                    'Presencia Verificada',
                    'Último Acceso'
                ])
                
                # Contadores por rol
                contadores = {}
                
                for user in usuarios_quindio:
                    # Obtener ubicación
                    if user.ubicacion_id:
                        ubicacion = Location.query.get(user.ubicacion_id)
                        if ubicacion:
                            departamento = ubicacion.departamento_nombre or ''
                            municipio = ubicacion.municipio_nombre or ''
                            zona = f"Zona {ubicacion.zona_codigo[-2:]}" if ubicacion.zona_codigo else ''
                            puesto = ubicacion.puesto_nombre or ''
                            mesa = ubicacion.mesa_nombre or ''
                            ubicacion_completa = ubicacion.nombre_completo or ''
                        else:
                            departamento = municipio = zona = puesto = mesa = ubicacion_completa = 'Sin ubicación'
                    else:
                        departamento = municipio = zona = puesto = mesa = ubicacion_completa = 'Sin ubicación'
                    
                    # Contraseña por defecto
                    if user.rol == 'super_admin':
                        password = 'admin123'
                    else:
                        password = 'test123'
                    
                    # Contar por rol
                    contadores[user.rol] = contadores.get(user.rol, 0) + 1
                    
                    writer.writerow([
                        user.id,
                        user.nombre,
                        user.cedula or 'Sin cédula',
                        user.rol,
                        password,
                        departamento,
                        municipio,
                        zona,
                        puesto,
                        mesa,
                        ubicacion_completa,
                        'Sí' if user.activo else 'No',
                        'Sí' if user.presencia_verificada else 'No',
                        user.ultimo_acceso.strftime('%Y-%m-%d %H:%M:%S') if user.ultimo_acceso else 'Nunca'
                    ])
            
            print(f'✅ Archivo generado: {filename}')
            
            # Mostrar resumen por rol
            print('\n📋 RESUMEN POR ROL:')
            total = 0
            for rol, cantidad in sorted(contadores.items()):
                print(f'  - {rol}: {cantidad} usuarios')
                total += cantidad
            
            print(f'\n👥 TOTAL: {total} usuarios')
            
            # Mostrar algunos ejemplos por rol
            print('\n🔍 EJEMPLOS DE USUARIOS POR ROL:')
            
            roles_ejemplos = {}
            for user in usuarios_quindio:
                if user.rol not in roles_ejemplos:
                    roles_ejemplos[user.rol] = []
                if len(roles_ejemplos[user.rol]) < 3:  # Máximo 3 ejemplos por rol
                    roles_ejemplos[user.rol].append(user)
            
            for rol, usuarios in roles_ejemplos.items():
                print(f'\n  📌 {rol.upper()}:')
                for user in usuarios:
                    if user.ubicacion_id:
                        ubicacion = Location.query.get(user.ubicacion_id)
                        ubicacion_info = ubicacion.nombre_completo if ubicacion else 'Sin ubicación'
                    else:
                        ubicacion_info = 'Sin ubicación'
                    
                    password = 'admin123' if user.rol == 'super_admin' else 'test123'
                    print(f'    • {user.nombre} | Contraseña: {password} | {ubicacion_info}')
            
            print(f'\n✅ Lista completa guardada en: {filename}')
            
        except Exception as e:
            print(f'❌ Error: {e}')
            raise

if __name__ == '__main__':
    main()