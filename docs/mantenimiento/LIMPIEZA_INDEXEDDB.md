# Limpieza de IndexedDB

## Descripción

IndexedDB se usa para almacenar datos offline (formularios, incidentes, delitos) cuando no hay conexión. A veces, reportes con errores pueden quedar atascados intentando sincronizarse repetidamente.

## Limpieza Automática

El sistema ahora limpia automáticamente:
- ✅ Reportes con errores de validación (422)
- ✅ Reportes con más de 3 intentos fallidos
- ✅ Reportes que no pueden sincronizarse

## Limpieza Manual

Si necesitas limpiar manualmente los datos de IndexedDB, usa los siguientes comandos en la **Consola del Navegador** (F12 → Console):

### 1. Ver Estado Actual

```javascript
verEstadoIndexedDB()
```

Muestra:
- Total de reportes pendientes
- Reportes por tipo (formulario_e14, incidente, delito)
- Reportes por número de intentos
- Reportes problemáticos (3+ intentos)

**Ejemplo de salida:**
```
📊 Estado de IndexedDB:
==================================================

📋 Reportes pendientes: 5

📊 Por tipo:
  - formulario_e14: 3
  - incidente: 2

🔄 Por intentos de sincronización:
  - 0 intentos: 2 reportes
  - 3 intentos: 3 reportes

⚠️ Reportes problemáticos (3+ intentos): 3
  - ID 1: formulario_e14, 3 intentos
  - ID 2: formulario_e14, 3 intentos
  - ID 3: incidente, 3 intentos
```

### 2. Limpiar Reportes Problemáticos

```javascript
limpiarReportesProblematicos()
```

Elimina automáticamente:
- Reportes con 3 o más intentos fallidos
- Reportes con más de 7 días de antigüedad

**Ejemplo de salida:**
```
🧹 Iniciando limpieza de reportes problemáticos...
📊 Total de reportes pendientes: 5
🗑️ Eliminando reporte 1: { tipo: 'formulario_e14', intentos: 3, dias: 2, motivo: 'Demasiados intentos' }
🗑️ Eliminando reporte 2: { tipo: 'formulario_e14', intentos: 3, dias: 2, motivo: 'Demasiados intentos' }
🗑️ Eliminando reporte 3: { tipo: 'incidente', intentos: 3, dias: 1, motivo: 'Demasiados intentos' }
✅ Limpieza completada: 3 reportes eliminados
📊 Reportes restantes: 2
```

### 3. Limpiar TODO (⚠️ PELIGROSO)

```javascript
limpiarTodoIndexedDB()
```

**⚠️ ADVERTENCIA**: Esto eliminará TODOS los datos offline, incluyendo:
- Formularios E-14 no sincronizados
- Incidentes no sincronizados
- Delitos no sincronizados
- Configuración offline
- Datos de referencia

**Solo usar si:**
- Hay problemas graves con IndexedDB
- Se necesita empezar desde cero
- Se ha confirmado que no hay datos importantes sin sincronizar

El sistema pedirá confirmación antes de ejecutar.

## Cuándo Usar Limpieza Manual

### Usar `limpiarReportesProblematicos()` cuando:
- ✅ Ves errores repetidos en la consola
- ✅ Hay reportes que no se sincronizan después de varios intentos
- ✅ El sistema está lento por demasiados reportes pendientes

### Usar `limpiarTodoIndexedDB()` cuando:
- ⚠️ IndexedDB está corrupto
- ⚠️ Hay errores graves que no se pueden resolver
- ⚠️ Se necesita resetear completamente el almacenamiento offline

### NO usar limpieza cuando:
- ❌ Hay formularios importantes sin sincronizar
- ❌ No hay conexión a internet (esperar a tener conexión)
- ❌ Los reportes son recientes (< 24 horas)

## Prevención de Problemas

Para evitar que se acumulen reportes problemáticos:

1. **Mantener conexión estable**: Los reportes se sincronizan automáticamente cuando hay conexión
2. **Validar datos antes de enviar**: El sistema ahora valida todos los campos antes de guardar
3. **No crear duplicados**: Si ya existe un formulario para una mesa, editarlo en lugar de crear uno nuevo
4. **Revisar errores**: Si un reporte falla, revisar el error y corregir antes de reintentar

## Monitoreo

El sistema registra en la consola:
- ✅ Sincronizaciones exitosas
- ⚠️ Reportes con errores
- 🗑️ Reportes eliminados automáticamente
- 📊 Estado de sincronización

Para ver los logs, abrir la consola del navegador (F12 → Console).

## Soporte

Si los problemas persisten después de la limpieza:

1. Tomar captura de pantalla de la consola con los errores
2. Ejecutar `verEstadoIndexedDB()` y copiar la salida
3. Reportar al equipo de desarrollo con:
   - Capturas de pantalla
   - Estado de IndexedDB
   - Descripción del problema
   - Pasos para reproducir

## Notas Técnicas

- IndexedDB se reinicializa automáticamente al recargar la página
- Los datos sincronizados exitosamente se marcan como "sincronizado" pero no se eliminan inmediatamente
- La limpieza automática se ejecuta durante cada sincronización
- Los reportes eliminados no se pueden recuperar
