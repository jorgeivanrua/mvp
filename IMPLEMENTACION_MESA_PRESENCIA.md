# Implementación: Mesa y Verificación de Presencia

## Objetivo
1. Cuando el testigo selecciona una mesa en el dashboard y verifica presencia, activar el botón "Nuevo Formulario"
2. Cuando abre el formulario E-14, la mesa seleccionada se carga automáticamente

## Cambios Necesarios

### 1. JavaScript - testigo-dashboard-new.js

#### A. Agregar variable global para controlar presencia verificada
```javascript
let presenciaVerificada = false;
let mesaSeleccionadaDashboard = null;
```

#### B. Implementar función verificarPresencia()
```javascript
/**
 * Verificar presencia del testigo en la mesa seleccionada
 */
async function verificarPresencia() {
    try {
        // Verificar que haya una mesa seleccionada
        const selectorMesa = document.getElementById('mesa');
        if (!selectorMesa.value) {
            Utils.showError('Debe seleccionar una mesa primero');
            return;
        }
        
        // Obtener datos de la mesa seleccionada
        const selectedOption = selectorMesa.options[selectorMesa.selectedIndex];
        if (!selectedOption || !selectedOption.dataset.mesa) {
            Utils.showError('Error al obtener datos de la mesa');
            return;
        }
        
        mesaSeleccionadaDashboard = JSON.parse(selectedOption.dataset.mesa);
        
        // Llamar al endpoint de verificación de presencia
        const response = await APIClient.post('/testigo/registrar-presencia', {
            mesa_id: mesaSeleccionadaDashboard.id
        });
        
        if (response.success) {
            presenciaVerificada = true;
            
            // Actualizar UI
            document.getElementById('btnVerificarPresencia').classList.add('d-none');
            document.getElementById('alertaPresenciaVerificada').classList.remove('d-none');
            
            // Mostrar fecha de verificación
            const fechaElement = document.getElementById('presenciaFecha');
            if (fechaElement) {
                const fecha = new Date();
                fechaElement.textContent = `Verificada el ${fecha.toLocaleDateString()} a las ${fecha.toLocaleTimeString()}`;
            }
            
            // Habilitar botón de nuevo formulario
            habilitarBotonNuevoFormulario();
            
            Utils.showSuccess('Presencia verificada exitosamente');
        }
    } catch (error) {
        console.error('Error al verificar presencia:', error);
        Utils.showError('Error al verificar presencia: ' + error.message);
    }
}
```

#### C. Función para habilitar/deshabilitar botón Nuevo Formulario
```javascript
/**
 * Habilitar o deshabilitar el botón de nuevo formulario
 */
function habilitarBotonNuevoFormulario() {
    const btnNuevoFormulario = document.querySelector('[onclick="showCreateForm()"]');
    
    if (presenciaVerificada && mesaSeleccionadaDashboard) {
        // Habilitar botón
        if (btnNuevoFormulario) {
            btnNuevoFormulario.disabled = false;
            btnNuevoFormulario.classList.remove('disabled');
            btnNuevoFormulario.title = 'Crear nuevo formulario E-14';
        }
    } else {
        // Deshabilitar botón
        if (btnNuevoFormulario) {
            btnNuevoFormulario.disabled = true;
            btnNuevoFormulario.classList.add('disabled');
            btnNuevoFormulario.title = 'Debe seleccionar una mesa y verificar presencia primero';
        }
    }
}
```

#### D. Modificar función cambiarMesa()
```javascript
function cambiarMesa() {
    const selector = document.getElementById('mesa');
    const selectedOption = selector.options[selector.selectedIndex];
    
    if (selectedOption && selectedOption.dataset.mesa) {
        selectedMesa = JSON.parse(selectedOption.dataset.mesa);
        mesaSeleccionadaDashboard = selectedMesa;
        
        // Resetear verificación de presencia al cambiar de mesa
        presenciaVerificada = false;
        document.getElementById('btnVerificarPresencia').classList.remove('d-none');
        document.getElementById('alertaPresenciaVerificada').classList.add('d-none');
        
        // Deshabilitar botón de nuevo formulario
        habilitarBotonNuevoFormulario();
        
        // Recargar formularios de esta mesa
        loadForms();
        
        // Actualizar panel lateral con todas las mesas
        actualizarPanelMesas();
    }
}
```

#### E. Modificar función showCreateForm()
```javascript
async function showCreateForm() {
    try {
        // Verificar que se haya verificado presencia
        if (!presenciaVerificada) {
            Utils.showError('Debe verificar su presencia en la mesa antes de crear un formulario');
            return;
        }
        
        // Verificar que haya una mesa seleccionada
        if (!mesaSeleccionadaDashboard) {
            Utils.showError('Debe seleccionar una mesa primero');
            return;
        }
        
        // Limpiar formulario
        const form = document.getElementById('e14Form');
        form.reset();
        votosData = {};
        
        // Limpiar preview de imagen
        document.getElementById('imagePreview').innerHTML = 
            '<p class="text-muted">Toque el botón para tomar una foto</p>';
        
        // Habilitar tipo de elección
        const tipoEleccionSelect = document.getElementById('tipoEleccion');
        if (tipoEleccionSelect) {
            tipoEleccionSelect.disabled = false;
        }
        
        // Cargar la mesa seleccionada en el dashboard automáticamente
        const mesaSelect = document.getElementById('mesaFormulario');
        if (mesaSelect && mesaSeleccionadaDashboard) {
            // Limpiar y agregar la mesa seleccionada
            mesaSelect.innerHTML = '';
            const option = document.createElement('option');
            option.value = mesaSeleccionadaDashboard.id;
            option.textContent = `Mesa ${mesaSeleccionadaDashboard.mesa_codigo} - ${mesaSeleccionadaDashboard.puesto_nombre}`;
            option.dataset.mesa = JSON.stringify(mesaSeleccionadaDashboard);
            mesaSelect.appendChild(option);
            
            // Pre-seleccionar la mesa
            mesaSelect.value = mesaSeleccionadaDashboard.id;
            
            // Cargar votantes registrados
            const votantesInput = document.getElementById('votantesRegistrados');
            if (votantesInput && mesaSeleccionadaDashboard.total_votantes_registrados) {
                votantesInput.value = mesaSeleccionadaDashboard.total_votantes_registrados;
                votantesInput.readOnly = true;
                votantesInput.title = 'Total de personas habilitadas para votar en esta mesa según el censo electoral (DIVIPOLA)';
            }
            
            console.log('Mesa cargada automáticamente:', mesaSeleccionadaDashboard);
        }
        
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

#### F. Inicializar estado al cargar la página
```javascript
document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadForms();
    loadTiposEleccion();
    loadTiposIncidentes();
    loadTiposDelitos();
    
    // Deshabilitar botón de nuevo formulario inicialmente
    habilitarBotonNuevoFormulario();
    
    // Inicializar SyncManager para sincronización automática
    if (window.syncManager) {
        window.syncManager.init();
    }
});
```

### 2. Backend - Endpoint de verificación de presencia

#### Archivo: backend/routes/testigo.py

```python
@testigo_bp.route('/registrar-presencia', methods=['POST'])
@jwt_required()
def registrar_presencia():
    """
    Registrar presencia del testigo en la mesa
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        if user.rol != 'testigo_electoral':
            return jsonify({
                'success': False,
                'error': 'Solo los testigos pueden verificar presencia'
            }), 403
        
        data = request.get_json()
        mesa_id = data.get('mesa_id')
        
        # Verificar que la mesa pertenezca al puesto del testigo
        mesa = Location.query.get(mesa_id)
        if not mesa:
            return jsonify({
                'success': False,
                'error': 'Mesa no encontrada'
            }), 404
        
        # Obtener el puesto del testigo
        puesto_testigo = Location.query.get(user.ubicacion_id)
        if not puesto_testigo:
            return jsonify({
                'success': False,
                'error': 'No tienes un puesto asignado'
            }), 400
        
        # Verificar que la mesa pertenezca al puesto del testigo
        if (mesa.departamento_codigo != puesto_testigo.departamento_codigo or
            mesa.municipio_codigo != puesto_testigo.municipio_codigo or
            mesa.zona_codigo != puesto_testigo.zona_codigo or
            mesa.puesto_codigo != puesto_testigo.puesto_codigo):
            return jsonify({
                'success': False,
                'error': 'Esta mesa no pertenece a tu puesto asignado'
            }), 403
        
        # Registrar presencia
        user.presencia_verificada = True
        user.presencia_verificada_at = datetime.now()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Presencia verificada exitosamente',
            'data': {
                'presencia_verificada': True,
                'presencia_verificada_at': user.presencia_verificada_at.isoformat(),
                'mesa_id': mesa_id
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

## Resumen de Cambios

1. ✅ Se agrega verificación de presencia obligatoria antes de crear formulario
2. ✅ El botón "Nuevo Formulario" se habilita solo después de verificar presencia
3. ✅ La mesa seleccionada en el dashboard se carga automáticamente en el formulario
4. ✅ Al cambiar de mesa, se resetea la verificación de presencia
5. ✅ El campo de votantes registrados se carga automáticamente desde DIVIPOLA

## Flujo de Usuario

1. Testigo selecciona una mesa del dropdown
2. Testigo hace clic en "Verificar Mi Presencia en la Mesa"
3. Sistema verifica y habilita el botón "Nuevo Formulario"
4. Testigo hace clic en "Nuevo Formulario"
5. Modal se abre con la mesa ya seleccionada y votantes registrados cargados
6. Testigo completa el formulario E-14
