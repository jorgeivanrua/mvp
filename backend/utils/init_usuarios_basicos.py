"""
Inicialización automática de usuarios básicos
Este módulo se ejecuta al iniciar la aplicación
"""
from backend.models.user import User
from backend.database import db
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)

def init_usuarios_basicos():
    """
    Inicializar usuarios básicos del sistema
    Se ejecuta automáticamente al iniciar la aplicación
    """
    try:
        # Definir usuarios básicos
        usuarios_basicos = [
            {
                'nombre': 'Super Admin',
                'password': 'admin123',
                'rol': 'super_admin',
                'activo': True
            },
            {
                'nombre': 'Monitoreo',
                'password': 'test123',
                'rol': 'monitoreo',
                'activo': True
            },
            {
                'nombre': 'Coordinador Departamental',
                'password': 'test123',
                'rol': 'coordinador_departamental',
                'activo': True
            },
            {
                'nombre': 'Coordinador Municipal',
                'password': 'test123',
                'rol': 'coordinador_municipal',
                'activo': True
            },
            {
                'nombre': 'Coordinador Puesto',
                'password': 'test123',
                'rol': 'coordinador_puesto',
                'activo': True
            },
            {
                'nombre': 'Auditor Electoral',
                'password': 'test123',
                'rol': 'auditor_electoral',
                'activo': True
            }
        ]
        
        usuarios_creados = 0
        
        for usuario_data in usuarios_basicos:
            # Buscar usuario por rol y nombre
            usuario = User.query.filter_by(
                rol=usuario_data['rol'],
                nombre=usuario_data['nombre']
            ).first()
            
            if not usuario:
                # Crear nuevo usuario
                logger.info(f"Creando usuario básico: {usuario_data['nombre']} ({usuario_data['rol']})")
                usuario = User(
                    nombre=usuario_data['nombre'],
                    rol=usuario_data['rol'],
                    activo=usuario_data['activo'],
                    es_usuario_basico=True
                )
                usuario.set_password(usuario_data['password'])
                db.session.add(usuario)
                usuarios_creados += 1
            else:
                # Asegurar que esté activo
                if not usuario.activo:
                    logger.info(f"Activando usuario básico: {usuario_data['nombre']}")
                    usuario.activo = True
        
        if usuarios_creados > 0:
            db.session.commit()
            logger.info(f"✓ {usuarios_creados} usuarios básicos creados")
        
        return True
        
    except Exception as e:
        logger.error(f"Error inicializando usuarios básicos: {str(e)}")
        db.session.rollback()
        return False

def verificar_usuarios_basicos():
    """
    Verificar que todos los usuarios básicos existan
    Retorna True si todos existen, False si falta alguno
    """
    roles_basicos = [
        'super_admin',
        'monitoreo',
        'coordinador_departamental',
        'coordinador_municipal',
        'coordinador_puesto',
        'auditor_electoral'
    ]
    
    for rol in roles_basicos:
        usuario = User.query.filter_by(rol=rol, activo=True).first()
        if not usuario:
            logger.warning(f"Usuario básico faltante: {rol}")
            return False
    
    return True
