#!/bin/bash
# Script de inicialización para Render

echo "🚀 Iniciando configuración de Render..."

# Verificar si la base de datos existe
if [ ! -f "electoral.db" ]; then
    echo "📦 Base de datos no encontrada. Inicializando..."
    python backend/scripts/load_complete_test_data.py
    echo "✅ Base de datos inicializada con datos de prueba"
else
    echo "✅ Base de datos ya existe"
fi

echo "🎉 Configuración completada"
