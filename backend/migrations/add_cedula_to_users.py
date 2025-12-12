"""
Migración: Agregar campo cédula a la tabla users
Fecha: 2025-12-12
Descripción: Agregar campo cédula como ID único para testigos
"""

from backend.database import db


def upgrade():
    """Agregar campo cédula a users"""
    
    try:
        # Agregar columna cédula
        db.engine.execute("""
            ALTER TABLE users 
            ADD COLUMN cedula VARCHAR(20)
        """)
        
        # Crear índice único para cédula
        db.engine.execute("""
            CREATE UNIQUE INDEX idx_users_cedula 
            ON users (cedula) 
            WHERE cedula IS NOT NULL
        """)
        
        print("✅ Campo cédula agregado a la tabla users")
        
    except Exception as e:
        print(f"⚠️ Error agregando campo cédula (puede que ya exista): {e}")


def downgrade():
    """Eliminar campo cédula de users"""
    
    try:
        # Eliminar índice
        db.engine.execute("DROP INDEX IF EXISTS idx_users_cedula")
        
        # Eliminar columna (SQLite no soporta DROP COLUMN directamente)
        print("⚠️ SQLite no soporta DROP COLUMN. El campo cédula permanecerá.")
        
    except Exception as e:
        print(f"Error eliminando campo cédula: {e}")


if __name__ == '__main__':
    print("Ejecutando migración de cédula...")
    upgrade()