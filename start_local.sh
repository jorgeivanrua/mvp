#!/bin/bash

echo "========================================"
echo "  Sistema Electoral - Inicio Local"
echo "========================================"
echo ""

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "Advertencia: No se encontró entorno virtual"
fi

# Configurar variables de entorno para desarrollo
export FLASK_ENV=development
export DEBUG=True

echo ""
echo "Iniciando aplicación en modo desarrollo..."
echo "URL: http://localhost:5000"
echo ""

# Iniciar aplicación
python run.py
