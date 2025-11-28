# 📊 Datos del Sistema

Esta carpeta contiene archivos de datos utilizados por el sistema electoral.

## 📋 Contenido

### Datos DIVIPOLA
- `divipola.csv` - Datos de División Político-Administrativa de Colombia
  - Departamentos, municipios, zonas y puestos de votación
  - Formato: CSV
  - Uso: Carga inicial de ubicaciones

### Datos de Logos
- `logos_update.sql` - Script SQL para actualizar logos de partidos políticos
  - Contiene URLs de logos
  - Formato: SQL
  - Uso: Actualización de logos en BD

## 🔧 Scripts Relacionados

Para cargar estos datos, usa:
- `../scripts/cargar_divipola_v2.py` - Cargar datos DIVIPOLA
- `../scripts/cargar_logos_bd.py` - Cargar logos de partidos
- `../scripts/actualizar_logos_partidos.py` - Actualizar logos

## 📌 Nota

Estos archivos son datos estáticos que se cargan una vez durante la inicialización del sistema.
