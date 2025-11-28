"""
Script simple para inicializar la base de datos SQLite
"""
import os
from sqlalchemy import create_engine, text

# Crear directorio instance si no existe
if not os.path.exists('instance'):
    os.makedirs('instance')

# Conectar a la base de datos
database_url = 'sqlite:///instance/electoral.db'
engine = create_engine(database_url)

# Crear tabla locations
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departamento_codigo VARCHAR(10) NOT NULL,
            municipio_codigo VARCHAR(10),
            zona_codigo VARCHAR(10),
            puesto_codigo VARCHAR(10),
            mesa_codigo VARCHAR(10),
            departamento_nombre VARCHAR(100) NOT NULL,
            municipio_nombre VARCHAR(100),
            puesto_nombre VARCHAR(200),
            mesa_nombre VARCHAR(200),
            nombre_completo VARCHAR(500) NOT NULL,
            tipo VARCHAR(50) NOT NULL,
            total_votantes_registrados INTEGER DEFAULT 0,
            mujeres INTEGER DEFAULT 0,
            hombres INTEGER DEFAULT 0,
            comuna VARCHAR(100),
            direccion VARCHAR(500),
            latitud FLOAT,
            longitud FLOAT,
            activo BOOLEAN DEFAULT 1 NOT NULL,
            parent_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES locations (id),
            CHECK (tipo IN ('departamento', 'municipio', 'zona', 'puesto', 'mesa'))
        )
    """))
    
    # Crear índices
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_departamento_codigo ON locations (departamento_codigo)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_municipio_codigo ON locations (municipio_codigo)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_zona_codigo ON locations (zona_codigo)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_puesto_codigo ON locations (puesto_codigo)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_mesa_codigo ON locations (mesa_codigo)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_location_hierarchy 
        ON locations (departamento_codigo, municipio_codigo, zona_codigo, puesto_codigo, mesa_codigo)
    """))

print("✅ Base de datos inicializada correctamente")
print(f"📁 Ubicación: {os.path.abspath('instance/electoral.db')}")
