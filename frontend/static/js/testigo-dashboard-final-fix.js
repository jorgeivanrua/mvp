/**
 * SOLUCIÓN DEFINITIVA para el dashboard de testigo
 * Este archivo REEMPLAZA completamente las funciones problemáticas
 */

console.log('🔧 Aplicando solución definitiva para dashboard de testigo...');

// ============================================================================
// VARIABLES GLOBALES
// ============================================================================
window.presenciaVerificada = false;
window.mesaSeleccionadaDashboard = null;

// ============================================================================
// FUNCIÓN 1: loadUserProfile - SIN VERIFICACIÓN AUTOMÁTICA
// ============================================================================
window.loadUserProfile = async function() {
    try {
        const response = await APIClient.getProfile();
        if (response.success) {
            window.currentUser = response.data.user;
            window.userLocation = response.data.ubicacion;
            const contexto = response.data.contexto;
            
            console.log('✅ User profile loaded:', window.currentUser);
            console.log('✅ User location:', window.userLocation);
            
            // Mostrar estadísticas si existen
            if (contexto && contexto.mis_formularios) {
                const stats = contexto.mis_formularios;
                const updateElement = (id, value) => {
                    const el = document.getElementById(id);
                    if (el) el.textContent = value || 0;
                };
                
                const panel = document.getElementById('estadisticasTestigo');
                if (panel) panel.style.display = 'flex';
                
                updateElement('totalFormularios', stats.total);
                updateElement('formulariosValidados', stats.validados);
                updateElement('formulariosPendientes', stats.pendientes);
                updateElement('formulariosRechazados', stats.rechazados);
            }
            
            // IMPORTANTE: NO verificar presencia automáticamente
            // Solo restaurar estado si YA estaba verificado
            if (window.currentUser.presencia_verificada && window.userLocation && window.userLocation.tipo === 'mesa') {
                window.mesaSeleccionadaDashboard = window.userLocation;
                window.presenciaVerificada = true;
                
                const btnVerificar = document.getElementById('btnVerificarPresencia');
                const alertaVerificada = document.getElementById('alertaPresenciaVerificada');
                
                if (btnVerificar) btnVerificar.classList.add('d-none');
                if (alertaVerificada) {
                    alertaVerificada.classList.remove('d-none');
                    const fechaEl = document.getElementById('presenciaFecha');
                    if (fechaEl && window.currentUser.presencia_verificada_at) {
                        const fecha = new Date(window.currentUser.presencia_verificada_at);
                        fechaEl.textContent = `Verificada el ${fecha.toLocaleDateString()} a las ${fecha.toLocaleTimeString()}`;
                    }
                }
                
                habilitarBotonNuevoFormulario();
            }
            
            // Cargar mesas del puesto
            if (window.userLocation && window.userLocation.puesto_codigo) {
                await loadMesas();
            }
        }
    } catch (error) {
        console.error('❌ Error al cargar perfil:', error);
    }
};

// ============================================================================
// FUNCIÓN 2: cambiarMesa - SIN RESETEAR VERIFICACIÓN
// ============================================================================
window.cambiarMesa = function() {
    const selector = document.getElementById('mesa');
    if (!selector || !selector.value) return;
    
    const selectedOption = selector.options[selector.selectedIndex];
    if (selectedOption && selectedOption.dataset.mesa) {
        window.selectedMesa = JSON.parse(selectedOption.dataset.mesa);
        window.mesaSeleccionadaDashboard = window.selectedMesa;
        
        console.log('✅ Mesa seleccionada:', window.selectedMesa);
        
        // NO resetear presencia - el testigo debe verificar manualmente
        
        // Recargar formularios
        if (typeof loadForms === 'function') {
            loadForms();
        }
        
        // Actualizar panel de mesas
        actualizarPanelMesas();
    }
};

// ============================================================================
// FUNCIÓN NUEVA: Pre-cargar datos del formulario
// ============================================================================
window.precargarDatosFormulario = function() {
    if (!window.mesaSeleccionadaDashboard) {
        console.warn('⚠️ No hay mesa seleccionada para pre-cargar datos');
        return;
    }
    
    const mesa = window.mesaSeleccionadaDashboard;
    console.log('📝 Pre-cargando datos del formulario para mesa:', mesa);
    
    // Pre-cargar votantes registrados
    const votantesInput = document.getElementById('votantesRegistrados');
    if (votantesInput && mesa.total_votantes_registrados) {
        votantesInput.value = mesa.total_votantes_registrados;
        console.log('✅ Votantes registrados cargados:', mesa.total_votantes_registrados);
    }
    
    // Pre-seleccionar la mesa en el formulario
    const mesaSelect = document.getElementById('mesaFormulario');
    if (mesaSelect && mesa.id) {
        mesaSelect.value = mesa.id;
        console.log('✅ Mesa pre-seleccionada en formulario:', mesa.id);
    }
    
    // Calcular totales iniciales
    if (typeof calcularTotales === 'function') {
        calcularTotales();
    }
};

// ============================================================================
// FUNCIÓN: cambiarMesaFormulario - Actualizar votantes al cambiar mesa
// ============================================================================
window.cambiarMesaFormulario = function() {
    const mesaSelect = document.getElementById('mesaFormulario');
    if (!mesaSelect || !mesaSelect.value) return;
    
    const selectedOption = mesaSelect.options[mesaSelect.selectedIndex];
    if (selectedOption && selectedOption.dataset.mesa) {
        const mesaData = JSON.parse(selectedOption.dataset.mesa);
        
        // Actualizar votantes registrados
        const votantesInput = document.getElementById('votantesRegistrados');
        if (votantesInput && mesaData.total_votantes_registrados) {
            votantesInput.value = mesaData.total_votantes_registrados;
            console.log('✅ Votantes actualizados para mesa:', mesaData.mesa_codigo, '-', mesaData.total_votantes_registrados);
        }
        
        // Recalcular totales
        if (typeof calcularTotales === 'function') {
            calcularTotales();
        }
    }
};

// ============================================================================
// FUNCIÓN 3: verificarPresencia - MANUAL
// ============================================================================
window.verificarPresencia = async function() {
    try {
        console.log('🔍 Verificando presencia...');
        
        const selectorMesa = document.getElementById('mesa');
        if (!selectorMesa || !selectorMesa.value) {
            Utils.showError('Debe seleccionar una mesa primero');
            return;
        }
        
        const selectedOption = selectorMesa.options[selectorMesa.selectedIndex];
        if (!selectedOption || !selectedOption.dataset.mesa) {
            Utils.showError('Error al obtener datos de la mesa');
            return;
        }
        
        window.mesaSeleccionadaDashboard = JSON.parse(selectedOption.dataset.mesa);
        
        const response = await APIClient.post('/testigo/registrar-presencia', {
            mesa_id: window.mesaSeleccionadaDashboard.id
        });
        
        if (response.success) {
            console.log('✅ Presencia verificada');
            
            // Actualizar estado
            window.presenciaVerificada = true;
            
            // Actualizar UI
            const btnVerificar = document.getElementById('btnVerificarPresencia');
            const alertaVerificada = document.getElementById('alertaPresenciaVerificada');
            
            if (btnVerificar) btnVerificar.classList.add('d-none');
            if (alertaVerificada) {
                alertaVerificada.classList.remove('d-none');
                const fechaEl = document.getElementById('presenciaFecha');
                if (fechaEl) {
                    const fecha = new Date();
                    fechaEl.textContent = `Verificada el ${fecha.toLocaleDateString()} a las ${fecha.toLocaleTimeString()}`;
                }
            }
            
            // Habilitar botón
            habilitarBotonNuevoFormulario();
            
            Utils.showSuccess('Presencia verificada exitosamente');
        }
    } catch (error) {
        console.error('❌ Error al verificar presencia:', error);
        Utils.showError('Error al verificar presencia: ' + error.message);
    }
};

// ============================================================================
// FUNCIÓN 4: habilitarBotonNuevoFormulario
// ============================================================================
window.habilitarBotonNuevoFormulario = function() {
    const btn = document.getElementById('btnNuevoFormulario');
    if (!btn) return;
    
    console.log('🔍 Verificando condiciones para habilitar botón:');
    console.log('  - presenciaVerificada:', window.presenciaVerificada);
    console.log('  - mesaSeleccionadaDashboard:', window.mesaSeleccionadaDashboard);
    
    if (window.presenciaVerificada && window.mesaSeleccionadaDashboard) {
        btn.disabled = false;
        btn.classList.remove('disabled');
        btn.title = 'Crear nuevo formulario E-14';
        console.log('✅ Botón HABILITADO');
    } else {
        btn.disabled = true;
        btn.classList.add('disabled');
        btn.title = 'Debe seleccionar una mesa y verificar presencia primero';
        console.log('❌ Botón DESHABILITADO');
    }
};

// ============================================================================
// FUNCIÓN 5: actualizarPanelMesas - SIN ERRORES
// ============================================================================
window.actualizarPanelMesas = async function() {
    const panel = document.getElementById('panelMesasPuesto');
    if (!panel) return;
    
    try {
        if (!window.userLocation || !window.userLocation.puesto_codigo) {
            panel.innerHTML = '<p class="text-muted text-center py-3">Cargando mesas...</p>';
            return;
        }
        
        const params = {
            puesto_codigo: window.userLocation.puesto_codigo,
            zona_codigo: window.userLocation.zona_codigo,
            municipio_codigo: window.userLocation.municipio_codigo,
            departamento_codigo: window.userLocation.departamento_codigo
        };
        
        const response = await APIClient.get('/locations/mesas', params);
        const mesas = response.data || [];
        
        const totalBadge = document.getElementById('totalMesasPuesto');
        if (totalBadge) totalBadge.textContent = mesas.length;
        
        if (mesas.length === 0) {
            panel.innerHTML = '<p class="text-muted text-center py-3">No hay mesas en este puesto</p>';
            return;
        }
        
        let html = '<div class="list-group list-group-flush">';
        
        mesas.forEach(mesa => {
            const esMiMesa = window.mesaSeleccionadaDashboard && window.mesaSeleccionadaDashboard.id === mesa.id;
            const borderClass = esMiMesa && window.presenciaVerificada ? 'border-start border-primary border-3' : '';
            const icon = esMiMesa && window.presenciaVerificada ? '<i class="bi bi-check-circle-fill text-primary"></i>' : '';
            
            html += `
                <div class="list-group-item ${borderClass} p-2">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <div class="d-flex align-items-center mb-1">
                                ${icon}
                                <strong class="ms-1">Mesa ${mesa.mesa_codigo}</strong>
                            </div>
                            <small class="text-muted d-block">
                                <i class="bi bi-people"></i> ${mesa.total_votantes_registrados || 0} votantes
                            </small>
                            ${esMiMesa ? '<small class="text-primary"><i class="bi bi-geo-alt-fill"></i> Mi mesa actual</small>' : ''}
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        panel.innerHTML = html;
        
        console.log('✅ Panel de mesas actualizado:', mesas.length, 'mesas');
        
    } catch (error) {
        console.error('❌ Error actualizando panel de mesas:', error);
        if (panel) {
            panel.innerHTML = `
                <div class="text-center py-3">
                    <p class="text-danger mb-2">Error al cargar mesas</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="actualizarPanelMesas()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </div>
            `;
        }
    }
};

// ============================================================================
// FUNCIÓN 6: showCreateForm - CON CARGA AUTOMÁTICA
// ============================================================================
window.showCreateForm = async function() {
    try {
        console.log('📝 Abriendo formulario E-14...');
        
        if (!window.presenciaVerificada) {
            Utils.showError('Debe verificar su presencia primero');
            return;
        }
        
        const form = document.getElementById('e14Form');
        if (form) form.reset();
        
        window.votosData = {};
        
        const imagePreview = document.getElementById('imagePreview');
        if (imagePreview) {
            imagePreview.innerHTML = '<p class="text-muted">Toque el botón para tomar una foto</p>';
        }
        
        const tipoEleccionSelect = document.getElementById('tipoEleccion');
        if (tipoEleccionSelect) tipoEleccionSelect.disabled = false;
        
        // Cargar mesas
        const mesaSelect = document.getElementById('mesaFormulario');
        if (mesaSelect && window.userLocation) {
            const params = {
                puesto_codigo: window.userLocation.puesto_codigo,
                zona_codigo: window.userLocation.zona_codigo,
                municipio_codigo: window.userLocation.municipio_codigo,
                departamento_codigo: window.userLocation.departamento_codigo
            };
            
            const response = await APIClient.get('/locations/mesas', params);
            const mesas = response.data || [];
            
            mesaSelect.innerHTML = '<option value="">Seleccione una mesa...</option>';
            
            mesas.forEach(mesa => {
                const option = document.createElement('option');
                option.value = mesa.id;
                option.textContent = `Mesa ${mesa.mesa_codigo} - ${mesa.puesto_nombre || ''} (${mesa.total_votantes_registrados || 0} votantes)`;
                option.dataset.mesa = JSON.stringify(mesa);
                
                if (window.mesaSeleccionadaDashboard && mesa.id === window.mesaSeleccionadaDashboard.id) {
                    option.selected = true;
                }
                
                mesaSelect.appendChild(option);
            });
            
            mesaSelect.disabled = false;
            
            // Cargar votantes automáticamente
            if (mesaSelect.value) {
                const selectedOption = mesaSelect.options[mesaSelect.selectedIndex];
                if (selectedOption && selectedOption.dataset.mesa) {
                    const mesaData = JSON.parse(selectedOption.dataset.mesa);
                    const votantesInput = document.getElementById('votantesRegistrados');
                    if (votantesInput && mesaData.total_votantes_registrados) {
                        votantesInput.value = mesaData.total_votantes_registrados;
                        console.log('✅ Votantes cargados:', mesaData.total_votantes_registrados);
                    }
                }
            }
        }
        
        const modalElement = document.getElementById('formModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
            
            modalElement.addEventListener('shown.bs.modal', function() {
                if (typeof setupImagePreview === 'function') {
                    setupImagePreview();
                }
            }, { once: true });
        }
        
    } catch (error) {
        console.error('❌ Error al abrir formulario:', error);
        Utils.showError('Error al abrir formulario: ' + error.message);
    }
};

// ============================================================================
// INICIALIZACIÓN
// ============================================================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando dashboard de testigo (versión corregida)...');
    
    // Deshabilitar botón inicialmente
    const btn = document.getElementById('btnNuevoFormulario');
    if (btn) {
        btn.disabled = true;
        btn.classList.add('disabled');
    }
    
    // Cargar perfil
    loadUserProfile();
    
    // Cargar formularios
    if (typeof loadForms === 'function') {
        loadForms();
    }
    
    // Cargar tipos de elección
    if (typeof loadTiposEleccion === 'function') {
        loadTiposEleccion();
    }
    
    console.log('✅ Dashboard de testigo inicializado correctamente');
});

console.log('✅ Solución definitiva aplicada correctamente');
