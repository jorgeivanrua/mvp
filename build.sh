#!/usr/bin/env bash
# Script de build para Render

set -o errexit

echo "🔧 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ Inicializando base de datos..."
python scripts/init_db.py

echo "📍 Cargando ubicaciones..."
python scripts/load_divipola.py

echo "👥 Creando usuarios de prueba..."
python scripts/create_test_users.py

echo "⚙️ Configurando sistema electoral..."
# Recrear tablas de configuración electoral para agregar nuevos campos
python -c "
from backend.app import create_app
from backend.database import db
from backend.models.configuracion_electoral import TipoEleccion, Partido, Candidato, Coalicion, PartidoCoalicion
import os

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

with app.app_context():
    # Eliminar y recrear tablas de configuración
    db.session.execute('DROP TABLE IF EXISTS candidatos CASCADE')
    db.session.execute('DROP TABLE IF EXISTS partidos_coaliciones CASCADE')
    db.session.execute('DROP TABLE IF EXISTS coaliciones CASCADE')
    db.session.execute('DROP TABLE IF EXISTS partidos CASCADE')
    db.session.execute('DROP TABLE IF EXISTS tipos_eleccion CASCADE')
    db.session.commit()
    
    # Recrear tablas
    db.create_all()
    print('Tablas de configuración electoral recreadas')
"

python scripts/init_configuracion_electoral.py

echo "📋 Creando tablas de formularios..."
python scripts/create_formularios_e14_tables.py

echo "✅ Build completado exitosamente"
