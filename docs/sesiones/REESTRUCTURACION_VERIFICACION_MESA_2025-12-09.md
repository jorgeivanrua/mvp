# Reestructuración: Verificación de Mesa como Paso Previo

**Fecha**: 2025-12-09  
**Sesión**: Reestructuración del dashboard del testigo

## Problema Identificado

El usuario señaló que la verificación de mesa debería estar separada de las pestañas y ser un paso previo que habilite todas las funcionalidades.

**Problema anterior:**
- La verificación de mesa estaba dentro de la pestaña "Formularios E-14"
- No era claro que era un paso obligatorio
- Las pestañas estaban siempre habilitadas
- No había una relación clara entre verificar mesa y habilitar funciones

## Solución Implementada

### 1. Sección de Verificación Destacada

Se creó una sección prominente al inicio del dashboard (antes de las pestañas):

```html
<!-- ⭐ SECCIÓN DE VERIFICACIÓN DE MESA (Siempre visible) -->
<div class="card mb-3 border-primary" id="verificacionMesaCard">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0">
            <i class="bi bi-check-circle"></i> Verificación de Mesa
        </h5>
    </div>
    <div class="card-body">
        <div class="row align-items-end">
            <div class="col-md-5">
                <!-- Selector de mesa -->
            </div>
            <div class="col-md-4">
                <!-- Botón verificar presencia -->
            </div>
            <div class="col-md-3">
                <!-- Alertas de estado -->
            </div>
        </div>
    </div>
</div>
```

**Características:**
- Siempre visible al inicio
- Diseño destacado con borde y header azul
- Cambia a verde cuando se verifica
- Muestra claramente el estado de verificación

### 2. Pestañas Deshabilitadas por Defecto

Las pestañas ahora inician deshabilitadas:

```html
<button class="nav-link active disabled" id="participacion-tab" ... disabled>
    <i class="bi bi-people-fill"></i> Participación
</button>
```

Se habilitan automáticamente al verificar la mesa.

### 3. Sistema de Habilitación/Deshabilitación

**Nuevo archivo**: `frontend/static/js/testigo-habilitar-funciones.js`

Funciones principales:
- `habilitarFuncionesTestigo()`: Habilita todas las funciones después de verificar
- `deshabilitarFuncionesTestigo()`: Deshabilita al cambiar de mesa

**Elementos que se habilitan/deshabilitan:**
1. Pestañas desktop (4 pestañas)
2. Navegación móvil (bottom nav)
3. Botones de acción (nuevo formulario, reportar, etc.)
4. Alertas de estado
5. Estilo visual de la card de verificación

### 4. Flujo de Verificación Mejorado

**Paso 1: Seleccionar Mesa**
```javascript
function cambiarMesa() {
    // Habilitar botón de verificar presencia
    btnVerificar.removeAttribute('disabled');
    
    // Resetear verificación anterior
    presenciaVerificada = false;
    localStorage.removeItem('presenciaVerificada');
    
    // Deshabilitar funciones hasta verificar
    deshabilitarFuncionesTestigo();
}
```

**Paso 2: Verificar Presencia**
```javascript
window.verificarPresenciaSimple = async function() {
    // ... verificación ...
    
    // Guardar en localStorage
    localStorage.setItem('presenciaVerificada', 'true');
    localStorage.setItem('mesaVerificadaId', mesaData.id);
    
    // Habilitar todas las funciones
    habilitarFuncionesTestigo();
}
```

**Paso 3: Usar Funciones**
- Todas las pestañas habilitadas
- Todos los botones habilitados
- Todas las acciones ligadas a la mesa verificada

### 5. Persistencia de Estado

El sistema recuerda la verificación al recargar la página:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const presenciaVerificada = localStorage.getItem('presenciaVerificada') === 'true';
    const mesaId = localStorage.getItem('mesaVerificadaId');
    
    if (presenciaVerificada && mesaId) {
        habilitarFuncionesTestigo();
    } else {
        deshabilitarFuncionesTestigo();
    }
});
```

### 6. Integración con Reportes

Los modales de incidentes y delitos ahora muestran automáticamente la mesa verificada:

```javascript
function reportarIncidente() {
    // Verificar que haya una mesa verificada
    if (!window.mesaSeleccionadaDashboard || !window.presenciaVerificada) {
        Utils.showError('Debe seleccionar una mesa y verificar su presencia primero');
        return;
    }
    
    // Mostrar información de la mesa en el modal
    mesaInfoElement.textContent = `Mesa ${mesaData.mesa_codigo} - ${mesaData.puesto_nombre}`;
}
```

## Archivos Modificados

1. **frontend/templates/testigo/dashboard.html**
   - Agregada sección de verificación destacada
   - Eliminada verificación de la pestaña formularios
   - Pestañas deshabilitadas por defecto
   - Agregado script de habilitación

2. **frontend/static/js/testigo-habilitar-funciones.js** (NUEVO)
   - Función `habilitarFuncionesTestigo()`
   - Función `deshabilitarFuncionesTestigo()`
   - Auto-verificación al cargar página

3. **frontend/static/js/testigo-verificacion-simple.js**
   - Llama a `habilitarFuncionesTestigo()` después de verificar
   - Mensaje mejorado de éxito

4. **frontend/static/js/testigo-dashboard-v2.js**
   - Función `cambiarMesa()` actualizada
   - Resetea verificación al cambiar de mesa
   - Habilita/deshabilita botón de verificar según selección

## Beneficios

1. **Claridad**: Es obvio que verificar mesa es el primer paso
2. **Seguridad**: No se pueden hacer acciones sin verificar
3. **Consistencia**: Todas las acciones ligadas a la misma mesa
4. **UX Mejorada**: Feedback visual claro del estado
5. **Persistencia**: Recuerda la verificación al recargar

## Flujo de Usuario

```
1. Usuario entra al dashboard
   ↓
2. Ve sección destacada "Verificación de Mesa"
   ↓
3. Selecciona su mesa del dropdown
   ↓
4. Se habilita botón "Verificar Mi Presencia"
   ↓
5. Hace clic en verificar (con geolocalización)
   ↓
6. ✅ Card cambia a verde
   ↓
7. ✅ Todas las pestañas se habilitan
   ↓
8. ✅ Todos los botones se habilitan
   ↓
9. Puede usar todas las funciones:
   - Reportar participación horaria
   - Crear formularios E-14
   - Reportar incidentes
   - Reportar delitos
```

## Próximos Pasos

1. Probar el flujo completo en el navegador
2. Verificar que la persistencia funcione al recargar
3. Probar en móvil la navegación bottom nav
4. Verificar que los reportes se liguen correctamente a la mesa

## Notas Técnicas

- La verificación se guarda en `localStorage` para persistencia
- Las funciones son globales (`window.habilitarFuncionesTestigo`)
- El orden de carga de scripts es importante (habilitar-funciones antes de verificacion-simple)
- Compatible con modo offline (localStorage)
