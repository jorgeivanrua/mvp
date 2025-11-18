"""
Ruta especial para inicializar la base de datos
Solo para uso en desarrollo/primera configuración
"""
from flask import Blueprint, jsonify
from backend.database import db
from backend.models.location import Location

init_db_bp = Blueprint('init_db', __name__)

@init_db_bp.route('/init-db-page')
def init_db_page():
    """Página HTML para inicializar la BD"""
    from flask import render_template
    return render_template('init_db.html')

@init_db_bp.route('/upload-database-secret-endpoint-2024', methods=['POST'])
def upload_database():
    """Endpoint para subir la base de datos desde local (con soporte para compresión)"""
    try:
        from flask import request
        import base64
        import gzip
        import os
        
        data = request.get_json()
        db_base64 = data.get('database')
        is_compressed = data.get('compressed', False)
        
        if not db_base64:
            return jsonify({'success': False, 'error': 'No database provided'}), 400
        
        print(f"📥 Recibiendo base de datos (comprimida: {is_compressed})...")
        
        # Decodificar base64
        db_data = base64.b64decode(db_base64)
        print(f"✅ Decodificado: {len(db_data):,} bytes")
        
        # Descomprimir si está comprimida
        if is_compressed:
            print("🗜️  Descomprimiendo...")
            db_data = gzip.decompress(db_data)
            print(f"✅ Descomprimido: {len(db_data):,} bytes")
        
        # Crear directorio instance si no existe
        os.makedirs('instance', exist_ok=True)
        
        # Guardar la base de datos
        db_path = 'instance/electoral.db'
        with open(db_path, 'wb') as f:
            f.write(db_data)
        
        print(f"💾 Guardado en: {db_path}")
        
        # Verificar que se guardó correctamente
        file_size = os.path.getsize(db_path)
        print(f"✅ Tamaño del archivo: {file_size:,} bytes")
        
        # Verificar que tiene datos
        from backend.models.location import Location
        departamentos_count = Location.query.filter_by(tipo='departamento').count()
        print(f"✅ Departamentos en BD: {departamentos_count}")
        
        return jsonify({
            'success': True,
            'message': f'Base de datos subida correctamente',
            'file_size': file_size,
            'departamentos': departamentos_count
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error subiendo BD: {e}")
        print(error_trace)
        
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': error_trace
        }), 500

@init_db_bp.route('/init-database-secret-endpoint-2024', methods=['GET', 'POST'])
def init_database():
    """
    Endpoint especial para inicializar la base de datos
    Acceder a: /init-database-secret-endpoint-2024
    """
    try:
        # Verificar si ya hay datos
        departamentos_count = Location.query.filter_by(tipo='departamento').count()
        
        if departamentos_count > 0:
            return jsonify({
                'success': True,
                'message': f'Base de datos ya tiene datos ({departamentos_count} departamentos)',
                'already_initialized': True
            }), 200
        
        # Crear tablas si no existen
        db.create_all()
        
        # Ejecutar scripts de inicialización en orden
        print("⚠️  Inicializando base de datos...")
        
        import subprocess
        import sys
        
        scripts = [
            'scripts/init_db.py',
            'scripts/load_divipola.py',
            'scripts/create_test_users.py',
            'scripts/init_configuracion_electoral.py',
            'scripts/create_formularios_e14_tables.py'
        ]
        
        for script in scripts:
            print(f"Ejecutando {script}...")
            result = subprocess.run([sys.executable, script], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error en {script}: {result.stderr}")
                raise Exception(f"Error ejecutando {script}: {result.stderr}")
            print(result.stdout)
        
        # Verificar que se cargaron los datos
        departamentos_count = Location.query.filter_by(tipo='departamento').count()
        
        return jsonify({
            'success': True,
            'message': f'Base de datos inicializada correctamente con {departamentos_count} departamentos',
            'departamentos': departamentos_count
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error inicializando BD: {e}")
        print(error_trace)
        
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': error_trace
        }), 500


@init_db_bp.route('/reset-all-passwords-secret-endpoint-2024', methods=['POST'])
def reset_all_passwords():
    """Endpoint para resetear todas las contraseñas a test123"""
    try:
        from backend.models.user import User
        
        # Obtener todos los usuarios
        usuarios = User.query.all()
        
        if not usuarios:
            return jsonify({
                'success': False,
                'error': 'No hay usuarios en la base de datos'
            }), 404
        
        # Resetear contraseñas
        usuarios_actualizados = 0
        usuarios_lista = []
        
        for usuario in usuarios:
            # Contraseña especial para admin
            if usuario.rol == 'super_admin':
                usuario.set_password('admin123')
            else:
                usuario.set_password('test123')
            
            usuarios_actualizados += 1
            usuarios_lista.append({
                'username': usuario.username,
                'nombre': usuario.nombre,
                'rol': usuario.rol,
                'password': 'admin123' if usuario.rol == 'super_admin' else 'test123'
            })
        
        db.session.commit()
        
        print(f"✅ {usuarios_actualizados} contraseñas reseteadas")
        
        return jsonify({
            'success': True,
            'message': f'{usuarios_actualizados} contraseñas reseteadas exitosamente',
            'usuarios_actualizados': usuarios_actualizados,
            'usuarios': usuarios_lista
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error reseteando contraseñas: {e}")
        print(error_trace)
        
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': error_trace
        }), 500
