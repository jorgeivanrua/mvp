# Fix: Error al Enviar Formulario E-14

**Fecha**: 2025-12-09
**Tipo**: Corrección de Bug
**Módulo**: Formularios E-14

## Problema Identificado

Al intentar enviar el formulario E-14, se producía un error que no se mostraba claramente al usuario, dificultando la identificación del problema.

## Causas Posibles

1. **Formulario duplicado**: Ya existe un formulario para la misma mesa y tipo de elección
2. **Validación de coherencia**: Los totales no cuadran correctamente
3. **Campos inválidos**: Algún campo numérico tiene un valor inválido (NaN, null, undefined)
4. **Tipo de elección no seleccionado**: El campo tipo_eleccion está vacío

## Soluciones Implementadas

### 1. Validación de Tipo de Elección

```javascript
// Validar que se haya seleccionado un tipo de elección
const tipoEleccionValue = formData.get('tipo_eleccion');
if (!tipoEleccionValue || tipoEleccionValue === '' || tipoEleccionValue === 'null') {
    Utils.showError('Debe seleccionar un tipo de elección');
    return;
}
```

### 2. Validación de Campos Numéricos

```javascript
// Validar que todos los campos numéricos sean válidos
const camposNumericos = [
    'mesa_id', 'tipo_eleccion_id', 'total_votantes_registrados',
    'total_votos', 'votos_validos', 'votos_nulos', 'votos_blanco',
    'tarjetas_no_marcadas', 'total_tarjetas'
];

for (const campo of camposNumericos) {
    if (isNaN(data[campo]) || data[campo] === null || data[campo] === undefined) {
        Utils.showError(`El campo ${campo} tiene un valor inválido: ${data[campo]}`);
        return;
    }
}
```

### 3. Manejo Mejorado de Error de Duplicado

```javascript
// Si el error menciona que ya existe un formulario, dar opción de editar
if (errorMessage.includes('Ya existe un formulario')) {
    errorMessage += '\n\n¿Desea editar el formulario existente en lugar de crear uno nuevo?';
    if (confirm(errorMessage)) {
        // Cerrar modal y recargar formularios para que pueda editar
        const modalElement = document.getElementById('formModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
        await loadForms();
        return;
    }
    return;
}
```

### 4. Logging Mejorado

Se agregó logging detallado para facilitar el debugging:

```javascript
console.log('[saveForm] tipo_eleccion del FormData:', tipoEleccionValue);
console.log('[saveForm] Objeto completo a enviar:', data);
```

## Validaciones del Backend

El backend realiza las siguientes validaciones:

1. **Campos requeridos**: Todos los campos numéricos deben estar presentes
2. **Mesa válida**: La mesa debe existir y ser del tipo correcto
3. **No duplicados**: No puede haber dos formularios para la misma mesa y tipo de elección
4. **Coherencia de datos**:
   - `votos_validos + votos_nulos + votos_blanco = total_votos`
   - `total_votos + tarjetas_no_marcadas = total_tarjetas`
   - `total_votos <= total_votantes_registrados`
5. **Valores no negativos**: Todos los campos numéricos deben ser >= 0

## Cómo Usar

1. **Seleccionar mesa**: Elegir la mesa del selector
2. **Seleccionar tipo de elección**: IMPORTANTE - Debe seleccionar un tipo de elección antes de continuar
3. **Cargar partidos**: Los partidos se cargan automáticamente al seleccionar el tipo de elección
4. **Ingresar votos**: Completar todos los campos de votación
5. **Verificar totales**: Los totales se calculan automáticamente
6. **Enviar**: Guardar como borrador o enviar para revisión

## Mensajes de Error Comunes

### "Debe seleccionar un tipo de elección"
- **Causa**: No se seleccionó un tipo de elección
- **Solución**: Seleccionar un tipo de elección del dropdown

### "Ya existe un formulario para esta mesa y [tipo de elección]"
- **Causa**: Ya se creó un formulario para esta combinación
- **Solución**: Editar el formulario existente en lugar de crear uno nuevo

### "La suma de votos válidos + nulos + blanco debe ser igual al total de votos"
- **Causa**: Los totales no cuadran
- **Solución**: Verificar que los cálculos sean correctos

### "El campo [campo] tiene un valor inválido"
- **Causa**: Un campo numérico tiene un valor no válido
- **Solución**: Verificar que todos los campos estén completos y sean números válidos

## Archivos Modificados

- `frontend/static/js/testigo-dashboard-v2.js`: Agregadas validaciones y mejor manejo de errores, eliminada referencia a función inexistente `abrirCamara`
- `frontend/static/js/sync-manager-offline.js`: Mejorado manejo de errores de sincronización, eliminación automática de reportes con errores de validación
- `frontend/static/js/indexeddb-service.js`: Agregada función `eliminarReporte` para limpiar reportes con errores

## Correcciones Adicionales

### 1. Error de Referencia: abrirCamara

**Problema**: La función `abrirCamara` estaba siendo exportada globalmente pero no existía, causando un error en la consola.

**Solución**: Eliminada la línea `window.abrirCamara = abrirCamara;` del archivo `testigo-dashboard-v2.js`.

### 2. Reportes con Errores de Validación

**Problema**: Reportes antiguos guardados en IndexedDB con errores de validación (422) intentaban sincronizarse repetidamente sin éxito.

**Solución**: 
- Detectar errores de validación (422) durante la sincronización
- Eliminar automáticamente reportes con errores de validación o más de 3 intentos fallidos
- Agregada función `eliminarReporte` en IndexedDBService

```javascript
// Si es error de validación (422) o el reporte tiene demasiados intentos, eliminarlo
const esErrorValidacion = error.message && error.message.includes('Errores de validación');
const demasiadosIntentos = reporte.intentos_sync >= 3;

if (esErrorValidacion || demasiadosIntentos) {
    console.warn(`Eliminando reporte ${reporte.id} - Error de validación o demasiados intentos`);
    await window.indexedDBService.eliminarReporte(reporte.id);
}
```

## Testing

Para probar el fix:

1. Intentar crear un formulario sin seleccionar tipo de elección → Debe mostrar error
2. Intentar crear un formulario duplicado → Debe ofrecer editar el existente
3. Intentar crear un formulario con totales incorrectos → Debe mostrar error específico
4. Crear un formulario válido → Debe guardarse correctamente

## Notas

- Los errores ahora se muestran de forma clara y específica
- Se agregó opción de editar formulario existente cuando hay duplicado
- El logging mejorado facilita el debugging en caso de problemas
