# Correcciones Urgentes - Dashboard Testigo

## Problemas Identificados

### 1. ❌ "Mi Mesa Asignada" muestra error
**Causa:** `userLocation` no está definido cuando se llama `actualizarPanelMesas()`
**Solución:** ✅ Agregada validación de `userLocation` antes de usarlo

### 2. ❌ Foto se sale del formulario
**Causa:** El evento `change` del input file no previene el comportamiento por defecto correctamente
**Solución:** Ya corregido en commit anterior con `e.preventDefault()` y `e.stopPropagation()`

### 3. ❌ Guardar borrador muestra "sincronizar" pero no hace nada
**Problema:** El botón de sincronizar aparece pero el usuario no puede continuar
**Solución Necesaria:** 
- Cerrar el modal automáticamente después de guardar
- Mostrar mensaje claro de éxito
- Actualizar la tabla de formularios inmediatamente

### 4. ❌ Enviar no funciona
**Problema:** El formulario no se envía al servidor
**Solución Necesaria:**
- Verificar que APIClient.createFormularioE14() funciona
- Agregar mejor manejo de errores
- Mostrar estado de envío

### 5. ❌ No muestra "enviado" en formularios
**Problema:** Los formularios enviados no muestran su estado correctamente
**Solución Necesaria:**
- Actualizar `getEstadoLabel()` para mostrar todos los estados
- Diferenciar visualmente formularios enviados vs borradores

## Correcciones Aplicadas

### Archivo: frontend/static/js/testigo-dashboard-new.js

#### 1. Función `actualizarPanelMesas()` - CORREGIDA ✅
```javascript
async function actualizarPanelMesas() {
    // Agregada validación de userLocation
    if (!userLocation || !userLocation.puesto_codigo) {
        document.getElementById('assignedLocation').innerHTML = `
            <p class="text-muted">Cargando información de mesas...</p>
        `;
        return;
    }
    // ... resto del código
}
```

#### 2. Función `saveForm()` - NECESITA MEJORAS
**Problemas:**
- No cierra el modal correctamente en todos los casos
- No muestra feedback claro al usuario
- No actualiza el panel de mesas después de guardar

**Correcciones necesarias:**
```javascript
async function saveForm(accion = 'borrador') {
    // ... código existente ...
    
    // MEJORAR: Cerrar modal siempre
    const modal = bootstrap.Modal.getInstance(document.getElementById('formModal'));
    if (modal) {
        modal.hide();
    }
    
    // MEJORAR: Actualizar panel de mesas
    await actualizarPanelMesas();
    
    // MEJORAR: Limpiar formulario
    document.getElementById('e14Form').reset();
}
```

#### 3. Función `getEstadoLabel()` - NECESITA ACTUALIZACIÓN
**Problema:** No muestra todos los estados posibles

**Corrección necesaria:**
```javascript
function getEstadoLabel(estado) {
    const labels = {
        'pendiente': 'Enviado - Pendiente Revisión',
        'validado': 'Validado ✓',
        'rechazado': 'Rechazado',
        'borrador': 'Borrador',
        'local': 'Guardado Localmente'
    };
    return labels[estado] || estado;
}
```

#### 4. Función `getStatusColor()` - ACTUALIZAR
```javascript
function getStatusColor(estado) {
    const colors = {
        'pendiente': 'info',      // Azul para enviado
        'validado': 'success',    // Verde para validado
        'rechazado': 'danger',    // Rojo para rechazado
        'borrador': 'secondary',  // Gris para borrador
        'local': 'warning'        // Amarillo para local
    };
    return colors[estado] || 'secondary';
}
```

## Correcciones Adicionales Necesarias

### 1. Prevenir envío duplicado
**Solución:** Deshabilitar botón de enviar mientras se procesa

```javascript
async function saveForm(accion = 'borrador') {
    // Deshabilitar botones
    const btnGuardar = document.querySelector('[onclick*="saveForm(\'borrador\')"]');
    const btnEnviar = document.querySelector('[onclick*="saveForm(\'enviar\')"]');
    
    if (btnGuardar) btnGuardar.disabled = true;
    if (btnEnviar) btnEnviar.disabled = true;
    
    try {
        // ... código de guardado ...
    } finally {
        // Rehabilitar botones
        if (btnGuardar) btnGuardar.disabled = false;
        if (btnEnviar) btnEnviar.disabled = false;
    }
}
```

### 2. Mostrar indicador de carga
**Solución:** Agregar spinner mientras se envía

```javascript
// En el HTML del modal, agregar:
<div id="loadingIndicator" class="d-none text-center my-3">
    <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Enviando...</span>
    </div>
    <p class="mt-2">Enviando formulario...</p>
</div>
```

### 3. Limpiar formulario después de enviar
**Solución:** Reset completo del formulario

```javascript
function limpiarFormulario() {
    document.getElementById('e14Form').reset();
    document.getElementById('imagePreview').innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
    document.getElementById('votacionContainer').innerHTML = '<p class="text-muted">Seleccione un tipo de elección</p>';
    votosData = {};
}
```

## Plan de Implementación

1. ✅ Corregir `actualizarPanelMesas()` - COMPLETADO
2. ⏳ Mejorar `saveForm()` - EN PROGRESO
3. ⏳ Actualizar labels de estado - PENDIENTE
4. ⏳ Prevenir envío duplicado - PENDIENTE
5. ⏳ Agregar indicadores de carga - PENDIENTE

## Testing Requerido

Después de aplicar correcciones, probar:

1. ✅ Panel "Mi Mesa Asignada" carga correctamente
2. ⏳ Tomar foto no cierra el formulario
3. ⏳ Guardar borrador funciona y cierra modal
4. ⏳ Enviar formulario funciona correctamente
5. ⏳ Formularios enviados muestran estado correcto
6. ⏳ No se puede enviar el mismo formulario dos veces
7. ⏳ Panel de mesas se actualiza después de guardar
