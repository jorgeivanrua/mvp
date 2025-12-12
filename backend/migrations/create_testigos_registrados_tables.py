"""
Migración: Crear tablas para el nuevo sistema de testigos registrados
Fecha: 2025-12-12
Descripción: Sistema de testigos por cédula según requerimientos de Registraduría
"""

from backend.database import db


def upgrade():
    """Crear tablas del nuevo sistema de testigos"""
    
    # Tabla de testigos registrados por partidos
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS testigos_registrados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula VARCHAR(20) NOT NULL UNIQUE,
            nombre_completo VARCHAR(200) NOT NULL,
            partido_id INTEGER NOT NULL,
            departamento_codigo VARCHAR(10) NOT NULL,
            municipio_codigo VARCHAR(10) NOT NULL,
            activo BOOLEAN NOT NULL DEFAULT 1,
            validado BOOLEAN NOT NULL DEFAULT 0,
            mesa_validacion_id INTEGER,
            puesto_validacion_codigo VARCHAR(20),
            fecha_validacion DATETIME,
            user_id INTEGER,
            registrado_por VARCHAR(100),
            fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (partido_id) REFERENCES partidos_politicos (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Índices para optimizar consultas
    db.engine.execute("CREATE INDEX IF NOT EXISTS idx_testigo_cedula ON testigos_registrados (cedula)")
    db.engine.execute("CREATE INDEX IF NOT EXISTS idx_testigo_municipio ON testigos_registrados (departamento_codigo, municipio_codigo)")
    db.engine.execute("CREATE INDEX IF NOT EXISTS idx_testigo_partido ON testigos_registrados (partido_id)")
    
    # Tabla de logs de validación
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS log_validacion_testigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula_ingresada VARCHAR(20) NOT NULL,
            nombre_ingresado VARCHAR(200),
            exitoso BOOLEAN NOT NULL,
            testigo_encontrado_id INTEGER,
            mesa_id INTEGER,
            puesto_codigo VARCHAR(20),
            ip_address VARCHAR(45),
            user_agent TEXT,
            motivo_fallo VARCHAR(200),
            fecha_intento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (testigo_encontrado_id) REFERENCES testigos_registrados (id)
        )
    """)
    
    # Índices para logs
    db.engine.execute("CREATE INDEX IF NOT EXISTS idx_log_cedula ON log_validacion_testigos (cedula_ingresada)")
    db.engine.execute("CREATE INDEX IF NOT EXISTS idx_log_fecha ON log_validacion_testigos (fecha_intento)")
    
    print("✅ Tablas de testigos registrados creadas exitosamente")


def downgrade():
    """Eliminar tablas del sistema de testigos registrados"""
    
    db.engine.execute("DROP TABLE IF EXISTS log_validacion_testigos")
    db.engine.execute("DROP TABLE IF EXISTS testigos_registrados")
    
    print("✅ Tablas de testigos registrados eliminadas")


if __name__ == '__main__':
    print("Ejecutando migración de testigos registrados...")
    upgrade()