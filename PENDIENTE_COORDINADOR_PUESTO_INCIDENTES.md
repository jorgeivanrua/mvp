# Pendiente: Incidentes y Delitos en Dashboard Coordinador de Puesto

## ✅ Completado

1. ✅ Backend completo de incidentes y delitos
2. ✅ API REST funcional con 15 endpoints
3. ✅ Frontend completo para testigos
4. ✅ Corrección de errores de `telefono` en servicios
5. ✅ Testigos creados para puesto 01

## ⏳ Pendiente

### Dashboard Coordinador de Puesto

El dashboard del coordinador de puesto necesita agregar la funcionalidad de incidentes y delitos.

#### Archivos a Modificar:

1. **frontend/templates/coordinador/puesto.html**
   - Agregar tabs para "Incidentes" y "Delitos"
   - Agregar secciones para visualizar reportes
   - Agregar botones para cambiar estados

2. **frontend/static/js/coordinador-puesto.js**
   - Agregar funciones para cargar incidentes del puesto
   - Agregar funciones para cargar delitos del puesto
   - Agregar funciones para cambiar estados
   - Agregar funciones para agregar notas de resolución
   - Integrar con el módulo `incidentes-delitos.js`

#### Funcionalidades Requeridas:

**Ver Incidentes:**
- Lista de incidentes reportados en el puesto
- Filtros por estado y severidad
- Detalle de cada incidente
- Información del testigo que reportó

**Gestionar Incidentes:**
- Cambiar estado (reportado → en_revision → resuelto)
- Agregar notas de resolución
- Escalar a nivel superior si es necesario

**Ver Delitos:**
- Lista de delitos reportados en el puesto
- Filtros por estado y gravedad
- Detalle de cada delito
- Información del testigo que reportó

**Gestionar Delitos:**
- Cambiar estado (reportado → en_investigacion)
- Agregar comentarios
- Escalar a coordinador municipal o auditor

#### Estructura Sugerida:

```html
<!-- Agregar después de los tabs existentes -->
<li class="nav-item" role="presentation">
    <button class="nav-link" id="incidentes-tab" data-bs-toggle="tab" 
            data-bs-target="#incidentes" type="button" role="tab">
        <i class="bi bi-exclamation-triangle"></i> Incidentes
        <span class="badge bg-warning" id="badge-incidentes">0</span>
    </button>
</li>
<li class="nav-item" role="presentation">
    <button class="nav-link" id="delitos-tab" data-bs-toggle="tab" 
            data-bs-target="#delitos" type="button" role="tab">
        <i class="bi bi-shield-exclamation"></i> Delitos
        <span class="badge bg-danger" id="badge-delitos">0</span>
    </button>
</li>
```

#### JavaScript Sugerido:

```javascript
// Cargar incidentes del puesto
async function cargarIncidentesPuesto() {
    try {
        const response = await APIClient.obtenerIncidentes();
        if (response.incidentes) {
            renderizarIncidentesPuesto(response.incidentes);
            actualizarBadgeIncidentes(response.incidentes.length);
        }
    } catch (error) {
        console.error('Error cargando incidentes:', error);
    }
}

// Cambiar estado de incidente
async function cambiarEstadoIncidente(incidenteId, nuevoEstado, comentario) {
    try {
        const response = await APIClient.actualizarEstadoIncidente(
            incidenteId, nuevoEstado, comentario
        );
        if (response.message) {
            Utils.showSuccess('Estado actualizado');
            await cargarIncidentesPuesto();
        }
    } catch (error) {
        Utils.showError('Error al actualizar estado');
    }
}
```

## 🎯 Prioridad

**Alta** - El coordinador de puesto necesita poder gestionar los incidentes y delitos reportados por los testigos de su puesto.

## 📝 Notas

- El backend ya está completo y funcional
- Los permisos ya están implementados en el servicio
- Solo falta la interfaz de usuario
- Se puede reutilizar mucho código del módulo `incidentes-delitos.js`
- Los testigos ya pueden reportar, pero los coordinadores no pueden gestionar

## ⏱️ Estimación

- Tiempo estimado: 1-2 horas
- Complejidad: Media
- Dependencias: Ninguna (todo el backend está listo)

## 🚀 Siguiente Paso

Implementar los tabs y funcionalidades de incidentes/delitos en el dashboard del coordinador de puesto.
