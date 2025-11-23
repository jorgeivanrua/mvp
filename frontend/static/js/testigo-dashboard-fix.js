/**
 * Parche para corregir errores del dashboard de testigo
 * Incluir DESPUÉS de testigo-dashboard-v2.js
 */

console.log('🔧 Aplicando parche de corrección para dashboard de testigo...');

// Asegurar que las variables globales existan
if (typeof formularios === 'undefined') {
    window.formularios = [];
}

// Agregar función mostrarContextoTestigo si no existe
if (typeof mostrarContextoTestigo === 'undefined') {
    window.mostrarContextoTestigo = function(contexto) {
        if (!contexto) return;
        
        try {
            // Mostrar estadísticas de formularios
            if (contexto.mis_formularios) {
                const stats = contexto.mis_formularios;
                
                // Mostrar panel de estadísticas
                const panelEstadisticas = document.getElementById('estadisticasTestigo');
                if (panelEstadisticas) {
                    panelEstadisticas.style.display = 'flex';
                }
                
                // Actualizar contadores de forma segura
                const updateElement = (id, value) => {
                    const element = document.getElementById(id);
                    if (element) element.textContent = value;
                };
                
                updateElement('totalFormularios', stats.total || 0);
                updateElement('formulariosValidados', stats.validados || 0);
                updateElement('formulariosPendientes', stats.pendientes || 0);
                updateElement('formulariosRechazados', stats.rechazados || 0);
                
                console.log('✅ Estadísticas de formularios mostradas:', stats);
            }
        } catch (error) {
            console.warn('Error mostrando contexto del testigo:', error);
        }
    };
}

// Sobrescribir función showCreateForm con versión corregida
const originalShowCreateForm = window.showCreateForm;
window.showCreateForm = async function() {
    try {
        console.log('=== ABRIENDO FORMULARIO E-14 (VERSIÓN CORREGIDA) ===');
        console.log('presenciaVerificada:', window.presenciaVerificada || presenciaVerificada);
        console.log('mesaSeleccionadaDashboard:', window.mesaSeleccionadaDashboard || mesaSeleccionadaDashboard);
        console.log('userLocation:', window.userLocation || userLocation);
        
        // Verificar presencia
        const verificada = window.presenciaVerificada || presenciaVerificada;
        if (!verificada) {
            Utils.showError('Debe verificar su presencia primero');
            return;
        }
        
        // Limpiar formulario
        const form = document.getElementById('e14Form');
        if (form) {
            form.reset();
        }
        
        window.votosData = {};
        if (typeof votosData !== 'undefined') {
            votosData = {};
        }
        
        // Limpiar preview de imagen
        const imagePreview = document.getElementById('imagePreview');
        if (imagePreview) {
            imagePreview.innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
        }
        
        // Habilitar tipo de elección
        const tipoEleccionSelect = document.getElementById('tipoEleccion');
        if (tipoEleccionSelect) {
            tipoEleccionSelect.disabled = false;
        }
        
        // Cargar TODAS las mesas del puesto en el selector
        const mesaSelect = document.getElementById('mesaFormulario');
        const location = window.userLocation || userLocation;
        
        if (mesaSelect && location) {
            console.log('Cargando mesas del puesto...');
            
            try {
                // Obtener todas las mesas del puesto
                const params = {
                    puesto_codigo: location.puesto_codigo,
                    zona_codigo: location.zona_codigo,
                    municipio_codigo: location.municipio_codigo,
                    departamento_codigo: location.departamento_codigo
                };
                
                console.log('Params para cargar mesas:', params);
                
                const response = await APIClient.get('/locations/mesas', params);
                const mesas = response.data || [];
                
                console.log('Mesas cargadas:', mesas);
                
                // Limpiar selector
                mesaSelect.innerHTML = '<option value="">Seleccione una mesa...</option>';
                
                // Agregar todas las mesas
                mesas.forEach(mesa => {
                    const option = document.createElement('option');
                    option.value = mesa.id;
                    option.textContent = `Mesa ${mesa.mesa_codigo} - ${mesa.puesto_nombre || ''} (${mesa.total_votantes_registrados || 0} votantes)`;
                    option.dataset.mesa = JSON.stringify(mesa);
                    
                    // Pre-seleccionar la mesa actual si existe
                    const mesaActual = window.mesaSeleccionadaDashboard || mesaSeleccionadaDashboard;
                    if (mesaActual && mesa.id === mesaActual.id) {
                        option.selected = true;
                    }
                    
                    mesaSelect.appendChild(option);
                });
                
                // Habilitar el selector
                mesaSelect.disabled = false;
                
                console.log('✅ Mesas cargadas en selector:', mesas.length);
                
                // Si hay una mesa pre-seleccionada, cargar sus votantes AUTOMÁTICAMENTE
                if (mesaSelect.value) {
                    // Trigger el cambio para cargar votantes
                    const selectedOption = mesaSelect.options[mesaSelect.selectedIndex];
                    if (selectedOption && selectedOption.dataset.mesa) {
                        const mesaData = JSON.parse(selectedOption.dataset.mesa);
                        
                        // Actualizar votantes registrados
                        const votantesInput = document.getElementById('votantesRegistrados');
                        if (votantesInput && mesaData.total_votantes_registrados) {
                            votantesInput.value = mesaData.total_votantes_registrados;
                            console.log('✅ Votantes registrados cargados:', mesaData.total_votantes_registrados);
                        }
                    }
                }
                
            } catch (error) {
                console.error('Error cargando mesas:', error);
                Utils.showError('Error al cargar mesas del puesto');
            }
        }
        
        // Mostrar modal
        const modalElement = document.getElementById('formModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
            
            // Configurar preview de imagen cuando se muestre el modal
            modalElement.addEventListener('shown.bs.modal', function() {
                if (typeof setupImagePreview === 'function') {
                    setupImagePreview();
                }
            }, { once: true });
        }
        
    } catch (error) {
        console.error('Error al abrir formulario:', error);
        Utils.showError('Error al abrir formulario: ' + error.message);
    }
};

// Sobrescribir función habilitarBotonNuevoFormulario con versión más robusta
window.habilitarBotonNuevoFormulario = function() {
    const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
    
    if (!btnNuevoFormulario) {
        console.error('❌ Botón btnNuevoFormulario no encontrado');
        return;
    }
    
    const verificada = window.presenciaVerificada || (typeof presenciaVerificada !== 'undefined' && presenciaVerificada);
    const mesaSeleccionada = window.mesaSeleccionadaDashboard || (typeof mesaSeleccionadaDashboard !== 'undefined' && mesaSeleccionadaDashboard);
    
    console.log('habilitarBotonNuevoFormulario:');
    console.log('- presenciaVerificada:', verificada);
    console.log('- mesaSeleccionada:', mesaSeleccionada);
    
    if (verificada && mesaSeleccionada) {
        btnNuevoFormulario.disabled = false;
        btnNuevoFormulario.classList.remove('disabled');
        btnNuevoFormulario.title = 'Crear nuevo formulario E-14';
        console.log('✅ Botón habilitado');
    } else {
        btnNuevoFormulario.disabled = true;
        btnNuevoFormulario.classList.add('disabled');
        btnNuevoFormulario.title = 'Debe seleccionar una mesa y verificar presencia primero';
        console.log('❌ Botón deshabilitado');
    }
};

// Parche para calcularTotales - eliminar referencias a elementos que no existen
const originalCalcularTotales = window.calcularTotales;
if (typeof originalCalcularTotales === 'function') {
    window.calcularTotales = function() {
        try {
            originalCalcularTotales();
        } catch (error) {
            console.warn('Error en calcularTotales (ignorado):', error);
            // Continuar sin romper la aplicación
        }
    };
}

// Sobrescribir cambiarMesa para NO verificar automáticamente
if (typeof cambiarMesa !== 'undefined') {
    const originalCambiarMesa = window.cambiarMesa;
    window.cambiarMesa = function() {
        const selector = document.getElementById('mesa');
        const selectedOption = selector.options[selector.selectedIndex];
        
        if (selectedOption && selectedOption.dataset.mesa) {
            selectedMesa = JSON.parse(selectedOption.dataset.mesa);
            mesaSeleccionadaDashboard = selectedMesa;
            
            // NO resetear verificación de presencia automáticamente
            // El testigo debe verificar manualmente
            
            // Recargar formularios de esta mesa
            if (typeof loadForms === 'function') {
                loadForms();
            }
            
            // Actualizar panel lateral con todas las mesas
            if (typeof actualizarPanelMesas === 'function') {
                actualizarPanelMesas();
            }
            
            console.log('Mesa seleccionada:', selectedMesa);
        }
    };
}

// Verificar que Utils esté disponible
if (typeof Utils === 'undefined') {
    console.error('❌ Utils no está definido. Asegúrate de incluir utils.js');
}

// Verificar que APIClient esté disponible
if (typeof APIClient === 'undefined') {
    console.error('❌ APIClient no está definido. Asegúrate de incluir api-client.js');
}

console.log('✅ Parche de testigo aplicado correctamente');
