# Correcciones Formulario E-14

## Problemas Identificados

1. **Mesa no se carga automáticamente**: El testigo tiene que seleccionar manualmente la mesa, cuando debería estar pre-cargada según su asignación
2. **Función `showCreateForm()` no existe**: El botón "Nuevo Formulario" llama a una función que no está definida
3. **Datos de votación confusos**: No está claro qué significa "Votantes Registrados" vs otros campos

## Soluciones

### 1. Cargar Mesa Automáticamente

El testigo está asignado a UNA mesa específica (en `user.ubicacion_id`). Esta mesa debe:
- Cargarse automáticamente al abrir el formulario
- Estar bloqueada (no editable)
- Mostrarse claramente en el dashboard

### 2. Crear función `showCreateForm()`

Esta función debe:
- Abrir el modal del formulario E-14
- Pre-cargar la mesa del testigo automáticamente
- Bloquear el selector de mesa
- Inicializar el formulario limpio

### 3. Clarificar Datos de Votación

**Votantes Registrados**: Total de personas habilitadas para votar en esa mesa (dato de DIVIPOLA, viene de `location.total_votantes_registrados`)

**Campos del Formulario E-14**:
- **Votantes Registrados**: Número total de personas en el censo de esa mesa (auto-completado desde DIVIPOLA)
- **Votos Válidos**: Suma de todos los votos por partidos y candidatos
- **Votos Nulos**: Tarjetas marcadas incorrectamente
- **Votos en Blanco**: Tarjetas sin marcar ninguna opción
- **Total Votos**: Suma de válidos + nulos + en blanco
- **Tarjetas No Marcadas**: Tarjetas que no se usaron
- **Total Tarjetas**: Total votos + tarjetas no marcadas

## Implementación

### Archivo: `frontend/static/js/testigo-dashboard-new.js`

Agregar después de la línea 50:

```javascript
/**
 * Mostrar formulario para crear nuevo E-14
 */
async function showCreateForm() {
    try {
        // Verificar que el usuario tenga una mesa asignada
        if (!userLocation || !userLocation.id) {
            Utils.showError('No tienes una mesa asignada. Contacta al administrador.');
            return;
        }
        
        // Limpiar formulario
        const form = document.getElementById('e14Form');
        form.reset();
        votosData = {};
        
        // Pre-cargar la mesa del testigo
        const mesaSelect = document.getElementById('mesaFormulario');
        mesaSelect.value = userLocation.id;
        mesaSelect.disabled = true; // Bloquear - no se puede cambiar
        
        // Cargar información de la mesa
        await cambiarMesaFormulario();
        
        // Pre-cargar votantes registrados desde DIVIPOLA
        const votantesInput = document.getElementById('votantesRegistrados');
        if (votantesInput && userLocation.total_votantes_registrados) {
            votantesInput.value = userLocation.total_votantes_registrados;
            votantesInput.readOnly = true; // Solo lectura - viene de DIVIPOLA
        }
        
        // Limpiar preview de imagen
        document.getElementById('imagePreview').innerHTML = 
            '<p class="text-muted">Toque el botón para tomar una foto</p>';
        
        // Habilitar tipo de elección
        document.getElementById('tipoEleccion').disabled = false;
        
        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('formModal'));
        modal.show();
        
        // Configurar preview de imagen cuando se muestre el modal
        document.getElementById('formModal').addEventListener('shown.bs.modal', function() {
            setupImagePreview();
        }, { once: true });
        
    } catch (error) {
        console.error('Error al abrir formulario:', error);
        Utils.showError('Error al abrir formulario: ' + error.message);
    }
}
```

### Modificar función `loadUserProfile()`:

Cambiar línea 28-45 por:

```javascript
async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        if (response.success) {
            currentUser = response.data.user;
            userLocation = response.data.ubicacion;
            
            console.log('User profile loaded:', currentUser);
            console.log('User location (mesa asignada):', userLocation);
            
            // Si el testigo tiene una mesa asignada, cargarla automáticamente
            if (userLocation && userLocation.tipo === 'mesa') {
                // Esta ES la mesa del testigo
                selectedMesa = userLocation;
                
                // Actualizar panel lateral
                await actualizarPanelMesas();
                
                // Mostrar mesa asignada
                document.getElementById('assignedLocation').innerHTML = `
                    <div class="alert alert-info">
                        <h6><i class="bi bi-geo-alt-fill"></i> ${userLocation.puesto_nombre}</h6>
                        <p class="mb-1"><strong>Mesa ${userLocation.mesa_codigo}</strong></p>
                        <p class="mb-1 small">
                            ${userLocation.departamento_nombre} - ${userLocation.municipio_nombre}
                        </p>
                        <hr>
                        <p class="mb-0 small">
                            <i class="bi bi-people-fill"></i> 
                            <strong>${userLocation.total_votantes_registrados || 0}</strong> votantes registrados
                        </p>
                    </div>
                `;
                
                // Ocultar selector de mesa (ya está asignada)
                const mesaSelector = document.getElementById('mesa');
                if (mesaSelector) {
                    mesaSelector.value = userLocation.id;
                    mesaSelector.disabled = true;
                    mesaSelector.closest('.form-group').style.display = 'none';
                }
            } else {
                document.getElementById('assignedLocation').innerHTML = `
                    <p class="text-muted">No hay mesa asignada</p>
                `;
            }
        }
    } catch (error) {
        console.error('Error al cargar perfil:', error);
        Utils.showError('Error al cargar perfil: ' + error.message);
    }
}
```

### Actualizar HTML del formulario

En `frontend/templates/testigo/dashboard.html`, buscar el campo "Votantes Registrados" y agregar tooltip:

```html
<div class="col-md-6">
    <label class="form-label">
        <i class="bi bi-people-fill"></i> Votantes Registrados
        <i class="bi bi-info-circle" data-bs-toggle="tooltip" 
           title="Total de personas habilitadas para votar en esta mesa según el censo electoral (DIVIPOLA)"></i>
    </label>
    <input type="number" class="form-control" id="votantesRegistrados" 
           name="total_votantes_registrados" readonly required>
    <small class="text-muted">Dato automático del censo electoral</small>
</div>
```

## Flujo Correcto

1. **Testigo inicia sesión** → Sistema carga su mesa asignada automáticamente
2. **Click en "Nuevo Formulario"** → Modal se abre con:
   - Mesa pre-cargada y bloqueada
   - Votantes registrados pre-cargados desde DIVIPOLA
   - Solo debe seleccionar tipo de elección y llenar votos
3. **Llenar formulario**:
   - Seleccionar tipo de elección (Senado, Cámara, etc.)
   - Tomar foto del formulario físico
   - Ingresar votos por partido/candidato
   - Ingresar votos nulos, blancos, tarjetas no marcadas
   - Sistema calcula automáticamente los totales
4. **Guardar o Enviar**:
   - Guardar como borrador (local o servidor)
   - Enviar para validación (requiere conexión)

## Beneficios

✅ **Menos errores**: El testigo no puede equivocarse de mesa
✅ **Más rápido**: No tiene que buscar y seleccionar su mesa
✅ **Más claro**: Los datos de DIVIPOLA están claramente identificados
✅ **Mejor UX**: Flujo más intuitivo y directo

## Archivos a Modificar

1. `frontend/static/js/testigo-dashboard-new.js` - Agregar función `showCreateForm()` y modificar `loadUserProfile()`
2. `frontend/templates/testigo/dashboard.html` - Agregar tooltips explicativos (opcional)

## Pruebas

1. Login como testigo
2. Verificar que se muestra la mesa asignada
3. Click en "Nuevo Formulario"
4. Verificar que la mesa está pre-cargada y bloqueada
5. Verificar que votantes registrados está pre-cargado
6. Completar y enviar formulario
