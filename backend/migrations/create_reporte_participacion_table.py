"""
Migración: Crear tabla reporte_participacion
"""
from backend.database import db


def upgrade():
    """Crear tabla reporte_participacion"""
    db.session.execute("""
        CREATE TABLE IF NOT EXISTS reporte_participacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_id INTEGER NOT NULL,
            testigo_id INTEGER NOT NULL,
            hora_reporte DATETIME NOT NULL,
            personas_votadas INTEGER NOT NULL,
            porcentaje_participacion REAL,
            observaciones TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (mesa_id) REFERENCES locations(id),
            FOREIGN KEY (testigo_id) REFERENCES users(id),
            
            UNIQUE(mesa_id, hora_reporte)
        )
    """)
    
    # Crear índices
    db.session.execute("""
        CREATE INDEX IF NOT EXISTS idx_reporte_participacion_mesa 
        ON reporte_participacion(mesa_id)
    """)
    
    db.session.execute("""
        CREATE INDEX IF NOT EXISTS idx_reporte_participacion_hora 
        ON reporte_participacion(hora_reporte)
    """)
    
    db.session.execute("""
        CREATE INDEX IF NOT EXISTS idx_reporte_participacion_testigo 
        ON reporte_participacion(testigo_id)
    """)
    
    db.session.commit()
    print("✅ Tabla reporte_participacion creada exitosamente")


def downgrade():
    """Eliminar tabla reporte_participacion"""
    db.session.execute("DROP TABLE IF EXISTS reporte_participacion")
    db.session.commit()
    print("✅ Tabla reporte_participacion eliminada")


if __name__ == '__main__':
    from backend.app import create_app
    app = create_app()
    
    with app.app_context():
        print("Ejecutando migración: create_reporte_participacion_table")
        upgrade()
