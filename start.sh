#!/bin/bash

echo "========================================"
echo "  Sistema Electoral - Inicio Render"
echo "========================================"
echo ""

# Configurar variables de entorno para producción
export FLASK_ENV=production
export DEBUG=False

# Inicializar base de datos
echo "📊 Inicializando base de datos..."
python init_render_db.py

if [ $? -ne 0 ]; then
    echo "❌ Error al inicializar base de datos"
    exit 1
fi

echo "✅ Base de datos inicializada"
echo ""

# Iniciar aplicación con Gunicorn
echo "🌐 Iniciando servidor con Gunicorn..."
echo "Workers: 4"
echo "Timeout: 120s"
echo ""

gunicorn run:app \
    --workers 4 \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
