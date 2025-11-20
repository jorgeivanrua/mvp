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

echo "👥 Creando usuarios fijos del sistema..."
python scripts/create_fixed_users.py

echo "⚙️ Configurando sistema electoral..."
python scripts/init_configuracion_electoral.py

echo "📋 Creando tablas de formularios..."
python scripts/create_formularios_e14_tables.py

echo "✅ Build completado exitosamente"
