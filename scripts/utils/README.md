# Scripts de Utilidades

Scripts de utilidades generales y herramientas.

## Uso Común

### Actualización de Datos
```bash
# Actualizar votantes por mesa
python scripts/utils/actualizar_votantes_mesas.py

# Actualizar coordenadas de puestos
python scripts/utils/actualizar_coordenadas_puestos_v2.py

# Actualizar logos de partidos
python scripts/utils/actualizar_logos_partidos.py
```

### Listar Datos
```bash
# Listar municipios de Caquetá
python scripts/utils/listar_municipios_caqueta.py

# Listar testigos
python scripts/utils/listar_testigos.py
```

## Categorías

### Actualización de Datos
- `actualizar_candidatos_completos.py` - Candidatos
- `actualizar_coordenadas_puestos.py` - Coordenadas de puestos
- `actualizar_coordenadas_puestos_v2.py` - Coordenadas v2
- `actualizar_logos_partidos.py` - Logos de partidos
- `actualizar_votantes_mesas.py` - Votantes por mesa

### Agregar Datos
- `add_citrep_tipo_eleccion.py` - Tipo de elección CITREP

### Listar Datos
- `listar_municipios_caqueta.py` - Municipios de Caquetá
- `listar_testigos.py` - Testigos

### Asignación
- `asignar_ubicacion_testigos.py` - Ubicación a testigos

### Upload/Download
- `upload_db_to_render.py` - Subir BD a Render

### Archivos SQL
- `crear_indices_monitoreo.sql` - Índices de monitoreo
- `optimizar_bd_monitoreo.sql` - Optimizar BD monitoreo
- `verificar_y_corregir_roles.sql` - Verificar y corregir roles

### Batch Scripts (Windows)
- `actualizar_logos.bat` - Actualizar logos
- `crear_usuario_monitoreo.bat` - Crear usuario monitoreo
- `inicializar_datos.bat` - Inicializar datos
- `instalar_monitoreo_completo.bat` - Instalar monitoreo

## Uso de Archivos SQL

```bash
# Ejecutar SQL en SQLite
sqlite3 instance/electoral.db < scripts/utils/crear_indices_monitoreo.sql
```

## Uso de Batch Scripts

```cmd
# Windows
scripts\utils\actualizar_logos.bat
```

## Notas

- Scripts de actualización modifican datos existentes
- Hacer backup antes de actualizar datos importantes
- Scripts de listado son solo lectura (seguros)
- Archivos .bat solo funcionan en Windows
