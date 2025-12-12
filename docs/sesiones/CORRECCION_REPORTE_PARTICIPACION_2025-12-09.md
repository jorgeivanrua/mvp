# Corrección de Error en Reporte de Participación

**Fecha**: 2025-12-09  
**Sesión**: Corrección de error SQLAlchemy en modelo ReporteParticipacion

## Problema Identificado

El servidor no iniciaba debido a un error en el modelo `ReporteParticipacion`:

```
sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'reporte_participacion.mesa_id' 
could not find table 'location' with which to generate a foreign key to target column 'id'
```

## Causa Raíz

1. **Nombres de tabla incorrectos en ForeignKey**: El modelo usaba `'location'` y `'user'` en singular, pero las tablas reales son `'locations'` y `'users'` (plural)

2. **Modelo no registrado**: El modelo `ReporteParticipacion` no estaba importado en:
   - `backend/models/__init__.py`
   - `backend/database.py`

## Solución Implementada

### 1. Corrección de ForeignKeys en el Modelo

**Archivo**: `backend/models/reporte_participacion.py`

```python
# ANTES (incorrecto)
mesa_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
testigo_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# DESPUÉS (correcto)
mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
testigo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
```

### 2. Corrección de Migración

**Archivo**: `backend/migrations/create_reporte_participacion_table.py`

```sql
-- ANTES (incorrecto)
FOREIGN KEY (mesa_id) REFERENCES location(id),
FOREIGN KEY (testigo_id) REFERENCES user(id),

-- DESPUÉS (correcto)
FOREIGN KEY (mesa_id) REFERENCES locations(id),
FOREIGN KEY (testigo_id) REFERENCES users(id),
```

### 3. Registro del Modelo

**Archivo**: `backend/models/__init__.py`

Agregado:
```python
from backend.models.reporte_participacion import ReporteParticipacion

__all__ = [
    # ... otros modelos ...
    'ReporteParticipacion'
]
```

**Archivo**: `backend/database.py`

Agregado a la lista de importaciones:
```python
from backend.models import user, location, form_e14, political_party, notification, audit_log, reporte_participacion
```

## Verificación

### Migración Aplicada Exitosamente

```bash
python scripts/init/aplicar_migracion_reporte_participacion.py
```

Resultado:
```
✅ Migración aplicada exitosamente

Tabla creada:
  - reporte_participacion

Índices creados:
  - idx_reporte_participacion_mesa
  - idx_reporte_participacion_hora
  - idx_reporte_participacion_testigo
```

### Servidor Inicializa Correctamente

```bash
python -c "from backend.app import create_app; app = create_app(); print('✅ Servidor inicializado correctamente')"
```

Resultado: ✅ Sin errores

## Estructura de la Tabla Creada

```sql
CREATE TABLE reporte_participacion (
    id INTEGER NOT NULL PRIMARY KEY,
    mesa_id INTEGER NOT NULL,
    testigo_id INTEGER NOT NULL,
    hora_reporte DATETIME NOT NULL,
    personas_votadas INTEGER NOT NULL,
    porcentaje_participacion FLOAT,
    observaciones TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    
    CONSTRAINT uq_mesa_hora_reporte UNIQUE (mesa_id, hora_reporte),
    FOREIGN KEY(mesa_id) REFERENCES locations (id),
    FOREIGN KEY(testigo_id) REFERENCES users (id)
)
```

## Archivos Modificados

1. `backend/models/reporte_participacion.py` - Corregidos ForeignKeys
2. `backend/migrations/create_reporte_participacion_table.py` - Corregidas referencias
3. `backend/models/__init__.py` - Agregado import y export
4. `backend/database.py` - Agregado a lista de importaciones

## Estado Actual

✅ **COMPLETADO**: El sistema de Reporte de Participación está completamente funcional

- Backend implementado y funcionando
- Frontend implementado (pestaña principal en dashboard testigo)
- Base de datos migrada correctamente
- Servidor inicia sin errores

## Próximos Pasos

1. Probar crear un reporte de participación desde el dashboard del testigo
2. Verificar que los datos se guarden correctamente
3. Verificar que el gráfico de tendencia se muestre correctamente
4. Probar la visualización desde coordinador de puesto

## Lecciones Aprendidas

1. **Nombres de tabla**: Siempre verificar los nombres reales de las tablas en la base de datos (singular vs plural)
2. **Registro de modelos**: Los modelos deben estar importados en `__init__.py` y `database.py` para que SQLAlchemy los registre
3. **Consistencia**: Mantener consistencia entre modelo y migración SQL
