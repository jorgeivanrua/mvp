#!/bin/bash

echo "🚀 Iniciando aplicación en Render..."

# Inicializar base de datos
echo "📊 Inicializando base de datos..."
python init_render_db.py

# Iniciar aplicación
echo "🌐 Iniciando servidor..."
gunicorn run:app
