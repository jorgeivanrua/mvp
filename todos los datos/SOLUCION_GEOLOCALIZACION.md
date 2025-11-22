# Solución: Geolocalización y Mapas

## Problemas Identificados

### 1. Error: `L is not defined`
**Causa:** Leaflet.js no está cargado cuando se intenta usar.

**Solución Aplicada:**
- Leaflet.js está incluido en `base.html`
- Se carga antes de `mapa-geolocalizacion.js`

### 2. Error: `Canvas is already in use`
**Causa:** Chart.js se inicializaba múltiples veces sin destruir instancias previas.

**Solución Aplicada:**
- Usar `window.charts` en lugar de variable local
- Destruir charts antes de recrear
- ✅ CORREGIDO en commit 5f91514

## Cómo Verificar la Geolocalización

### Paso 1: Acceder al Dashboard del Coordinador de Puesto

1. Ir a: https://dia-d.onrender.com
2. Iniciar sesión con:
   - Usuario: `coord_puesto_01`
   - Password: `coord123`

### Paso 2: Navegar a la Pestaña de Mapa

1. En el dashboard, buscar las pestañas superiores
2. Hacer clic en la pestaña: **"Mapa en Tiempo Real"**
3. El mapa debería cargar automáticamente

### Paso 3: Verificar Funcionalidad

El mapa debería mostrar:
- 🔵 **Markers azules**: Puestos de votación
- 🟢 **Markers verdes**: Usuarios activos
- 🟡 **Markers amarillos**: Usuarios inactivos
- 🔴 **Markers rojos**: Usuarios ausentes

### Botones Disponibles:
- **Centrar en Puesto**: Enfoca el puesto del coordinador
- **Ver Todo**: Ajusta zoom para ver todos los markers
- **Actualizar**: Refresca datos manualmente

## Requisitos para que Funcione

### 1. Datos de Geolocalización en BD

Los puestos deben tener coordenadas en la tabla `locations`:
```sql
SELECT id, puesto_codigo, puesto_nombre, latitud, longitud 
FROM locations 
WHERE tipo = 'puesto' AND latitud IS NOT NULL;
```

### 2. Usuarios con Geolocalización

Los usuarios deben tener coordenadas cuando verifican presencia:
```sql
SELECT id, nombre, rol, ultima_latitud, ultima_longitud 
FROM users 
WHERE ultima_latitud IS NOT NULL;
```

## Solución si No Aparece el Mapa

### Opción 1: Verificar Consola del Navegador

1. Abrir DevTools (F12)
2. Ir a la pestaña "Console"
3. Buscar errores relacionados con:
   - `L is not defined`
   - `Leaflet`
   - `MapaGeolocalizacion`

### Opción 2: Verificar que Leaflet Cargó

En la consola del navegador, ejecutar:
```javascript
console.log(typeof L);
// Debería mostrar: "object"
```

Si muestra `"undefined"`, Leaflet no cargó.

### Opción 3: Forzar Recarga

1. Presionar `Ctrl + Shift + R` (Windows/Linux)
2. O `Cmd + Shift + R` (Mac)
3. Esto fuerza la recarga de todos los archivos

## Agregar Coordenadas a Puestos Manualmente

Si los puestos no tienen coordenadas, puedes agregarlas:

```sql
-- Ejemplo: Agregar coordenadas a un puesto
UPDATE locations 
SET latitud = 1.6144, longitud = -75.6062 
WHERE puesto_codigo = '001' AND tipo = 'puesto';

-- Florencia, Caquetá está aproximadamente en:
-- Latitud: 1.6144
-- Longitud: -75.6062
```

## Verificar Presencia con Geolocalización

Para que los usuarios aparezcan en el mapa, deben:

1. Iniciar sesión
2. El sistema automáticamente:
   - Solicita permiso de geolocalización
   - Guarda las coordenadas en `users.ultima_latitud` y `users.ultima_longitud`
   - Actualiza cada 5 minutos con ping automático

## Endpoints de Geolocalización

### Obtener Puestos Geolocalizados:
```
GET /api/locations/puestos-geolocalizados
```

### Obtener Usuarios Geolocalizados:
```
GET /api/verificacion/usuarios-geolocalizados
```

### Verificar Presencia con Coordenadas:
```
POST /api/verificacion/presencia
Body: {
  "latitud": 1.6144,
  "longitud": -75.6062
}
```

## Estado Actual

✅ **Corregido:**
- Error de Canvas en Chart.js
- Estructura de código de mapas
- Endpoints de geolocalización

⏳ **Pendiente de Verificar:**
- Que Leaflet.js cargue correctamente en producción
- Que los puestos tengan coordenadas en BD
- Que los usuarios permitan geolocalización

## Próximos Pasos

1. Esperar a que Render redeploy con los cambios
2. Acceder al dashboard del coordinador
3. Ir a la pestaña "Mapa en Tiempo Real"
4. Verificar que el mapa carga
5. Si no carga, revisar consola del navegador

## Contacto

Si el problema persiste después del redeploy:
1. Tomar screenshot de la consola del navegador
2. Verificar que la URL sea: https://dia-d.onrender.com
3. Confirmar que estás en la pestaña "Mapa en Tiempo Real"
