# Correcciones de Geolocalización - 22 Nov 2025

## 🔴 Problemas Detectados en Producción

Al revisar los logs de Render, se detectaron dos errores recurrentes que impedían el funcionamiento del mapa de geolocalización:

### Error 1: Campo `zona_nombre` no existe
```
AttributeError: 'Location' object has no attribute 'zona_nombre'
File: backend/routes/locations_geo.py, line 121
```

**Causa**: El modelo `Location` solo tiene `zona_codigo`, no `zona_nombre`.

### Error 2: Campos de geolocalización en User
```
AttributeError: type object 'User' has no attribute 'ultima_latitud'
File: backend/routes/verificacion_presencia.py, line 330
```

**Causa**: El modelo `User` no tenía los campos necesarios para almacenar la geolocalización de los usuarios.

---

## ✅ Soluciones Implementadas

### 1. Modelo User - Campos de Geolocalización

**Archivo**: `backend/models/user.py`

Se agregaron los siguientes campos al modelo User:

```python
# Geolocalización
ultima_latitud = db.Column(db.Float, nullable=True)
ultima_longitud = db.Column(db.Float, nullable=True)
ultima_geolocalizacion_at = db.Column(db.DateTime, nullable=True)
precision_geolocalizacion = db.Column(db.Float, nullable=True)
```

**Propósito**:
- `ultima_latitud`: Última latitud reportada por el usuario
- `ultima_longitud`: Última longitud reportada por el usuario
- `ultima_geolocalizacion_at`: Timestamp de la última geolocalización
- `precision_geolocalizacion`: Precisión en metros de la geolocalización

### 2. Migración SQL

**Archivo**: `backend/migrations/add_user_geolocation_fields.sql`

Script SQL que agrega los campos de geolocalización a la tabla `users`:

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_latitud FLOAT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_longitud FLOAT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS ultima_geolocalizacion_at TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS precision_geolocalizacion FLOAT;

CREATE INDEX IF NOT EXISTS idx_users_geolocation 
ON users(ultima_latitud, ultima_longitud) 
WHERE ultima_latitud IS NOT NULL AND ultima_longitud IS NOT NULL;
```

### 3. Script de Aplicación de Migración

**Archivo**: `backend/migrations/apply_user_geolocation.py`

Script Python que ejecuta la migración SQL automáticamente durante el despliegue.

### 4. Corrección en locations_geo.py

**Archivo**: `backend/routes/locations_geo.py`

Se eliminó la referencia al campo inexistente `zona_nombre`:

```python
# ANTES (causaba error)
'zona_nombre': puesto.zona_nombre,

# DESPUÉS (corregido)
# Campo eliminado, solo se usa zona_codigo
```

### 5. Actualización de run.py

**Archivo**: `run.py`

Se agregó la migración a la lista de scripts que se ejecutan automáticamente:

```python
scripts = [
    'scripts/init_db.py',
    'scripts/load_divipola.py',
    'scripts/create_fixed_users.py',
    'scripts/init_configuracion_electoral.py',
    'backend/migrations/apply_user_geolocation.py'  # ← NUEVO
]
```

---

## 🚀 Despliegue

Los cambios fueron desplegados a producción mediante:

```bash
git add -A
git commit -m "Fix: Corregir errores de geolocalización en producción"
git push origin main
```

Render detectará automáticamente los cambios y:
1. Reconstruirá la aplicación
2. Ejecutará las migraciones automáticamente
3. Reiniciará el servicio

---

## 📊 Resultado Esperado

Después del despliegue:

✅ **Endpoint `/api/locations/puestos-geolocalizados`**
- Ya no generará error 500
- Retornará correctamente la lista de puestos con coordenadas
- El mapa podrá mostrar los puestos de votación

✅ **Endpoint `/api/verificacion/usuarios-geolocalizados`**
- Ya no generará error 500
- Retornará lista vacía inicialmente (hasta que los usuarios reporten su ubicación)
- El mapa podrá mostrar usuarios cuando estén geolocalizados

✅ **Dashboard de Super Admin**
- El mapa de geolocalización cargará sin errores
- Se podrán visualizar los puestos de votación
- Se podrán visualizar usuarios cuando reporten su ubicación

---

## 🔄 Próximos Pasos

1. **Verificar el despliegue**: Esperar a que Render complete el build
2. **Probar el mapa**: Acceder al dashboard y verificar que el mapa carga
3. **Implementar reporte de ubicación**: Agregar funcionalidad para que los usuarios reporten su ubicación GPS
4. **Monitorear logs**: Verificar que no haya más errores 500 en los endpoints de geolocalización

---

## 📝 Notas Técnicas

### Índice de Geolocalización
Se creó un índice parcial para optimizar las búsquedas de usuarios geolocalizados:

```sql
CREATE INDEX idx_users_geolocation 
ON users(ultima_latitud, ultima_longitud) 
WHERE ultima_latitud IS NOT NULL AND ultima_longitud IS NOT NULL;
```

Este índice solo incluye registros con coordenadas válidas, mejorando el rendimiento.

### Compatibilidad con SQLite
La migración usa `IF NOT EXISTS` para evitar errores si los campos ya existen, permitiendo ejecutar el script múltiples veces de forma segura.

### Precisión de Geolocalización
El campo `precision_geolocalizacion` almacena la precisión en metros reportada por el GPS del dispositivo, útil para:
- Validar la calidad de la geolocalización
- Filtrar ubicaciones imprecisas
- Mostrar indicadores de confianza en el mapa

---

## ✅ Estado Final

- ✅ Modelo User actualizado con campos de geolocalización
- ✅ Migración SQL creada y lista para ejecutar
- ✅ Script de migración automática implementado
- ✅ Errores de `zona_nombre` corregidos
- ✅ Errores de `ultima_latitud` corregidos
- ✅ Cambios desplegados a producción
- ⏳ Esperando confirmación de Render

**Fecha**: 22 de Noviembre de 2025
**Commit**: `6916fe2`
