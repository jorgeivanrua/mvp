/**
 * Dashboard del Coordinador de Puesto
 */

let currentUser = null;
let userLocation = null;
let formularios = [];
let formularioActual = null;
let estadoFiltro = '';
let autoRefreshInterval = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadFormularios();
    loadConsolidado();
    loadMesas();
    
    // Auto-refresh cada 30 segundos
    autoRefreshInterval = setInterval(() => {
        loadFormularios();
        loadConsolidado();
        loadMesas();
    }, 30000);
});

// Limpiar interval al salir
window.addEventListener('beforeunload', function() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});

/**
 * Cargar perfil del coordinador
 */
async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        
        if (response.success) {
            currentUser = response.data.user;
            userLocation = response.data.ubicacion;
            
            console.log('User profile loaded:', currentUser);
            console.log('User location:', userLocation);
            
            // Mostrar información del puesto
            if (userLocation) {
                document.getElementById('puestoInfo').textContent = 
                    `${userLocation.puesto_nombre || userLocation.nombre_completo} - Código: ${userLocation.puesto_codigo || 'N/A'}`;
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        Utils.showError('Error al cargar perfil: ' + error.message);
    }
}

/**
 * Cargar lista de formularios
 */
async function loadFormularios() {
    try {
        const params = {};
        if (estadoFiltro) {
            params.estado = estadoFiltro;
        }
        
        const response = await APIClient.get('/formularios/puesto', params);
        
        if (response.success) {
            formularios = response.data.formularios || [];
            const stats = response.data.estadisticas || {
                total: 0,
                pendientes: 0,
                validados: 0,
                rechazados: 0,
                mesas_reportadas: 0,
                total_mesas: 0
            };
            
            // Actualizar estadísticas
            updateEstadisticas(stats);
            
            // Renderizar tabla
            renderFormulariosTable(formularios);
        } else {
            throw new Error(response.error || 'Error desconocido');
        }
    } catch (error) {
        console.error('Error loading formularios:', error);
        const tbody = document.querySelector('#formulariosTable tbody');
        const errorMsg = error.message || 'Error al cargar formularios';
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <p class="text-danger">❌ ${errorMsg}</p>
                    <button class="btn btn-sm btn-outline-primary mt-2" onclick="loadFormularios()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </td>
            </tr>
        `;
    }
}

/**
 * Actualizar estadísticas
 */
function updateEstadisticas(stats) {
    document.getElementById('statPendientes').textContent = stats.pendientes || 0;
    document.getElementById('statValidados').textContent = stats.validados || 0;
    document.getElementById('statRechazados').textContent = stats.rechazados || 0;
    
    const porcentaje = stats.total_mesas > 0 
        ? Math.round((stats.mesas_reportadas / stats.total_mesas) * 100) 
        : 0;
    
    document.getElementById('statProgreso').textContent = `${porcentaje}%`;
    document.getElementById('statMesas').textContent = 
        `${stats.mesas_reportadas} de ${stats.total_mesas} mesas`;
}

/**
 * Renderizar tabla de formularios
 */
function renderFormulariosTable(formularios) {
    const tbody = document.querySelector('#formulariosTable tbody');
    
    if (formularios.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <p class="text-muted">No hay formularios ${estadoFiltro ? 'en estado ' + estadoFiltro : ''}</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = formularios.map(form => {
        const estadoBadge = getEstadoBadge(form.estado);
        const fecha = Utils.formatDate(form.created_at);
        const puedeValidar = form.estado === 'pendiente';
        
        return `
            <tr style="cursor: ${puedeValidar ? 'pointer' : 'default'};" 
                ${puedeValidar ? `onclick="abrirModalValidacion(${form.id})"` : ''}>
                <td>
                    <strong>${form.mesa_codigo || 'N/A'}</strong><br>
                    <small class="text-muted">${form.mesa_nombre || ''}</small>
                </td>
                <td>${form.testigo_nombre || 'N/A'}</td>
                <td>${estadoBadge}</td>
                <td><strong>${Utils.formatNumber(form.total_votos)}</strong></td>
                <td>
                    <small>${fecha}</small>
                </td>
                <td>
                    ${puedeValidar ? 
                        `<button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); abrirModalValidacion(${form.id})">
                            <i class="bi bi-eye"></i> Revisar
                        </button>` :
                        `<button class="btn btn-sm btn-outline-secondary" onclick="event.stopPropagation(); verDetalles(${form.id})">
                            <i class="bi bi-info-circle"></i> Ver
                        </button>`
                    }
                </td>
            </tr>
        `;
    }).join('');
}

/**
 * Obtener badge de estado
 */
function getEstadoBadge(estado) {
    const badges = {
        'borrador': '<span class="badge badge-status bg-secondary">Borrador</span>',
        'pendiente': '<span class="badge badge-status bg-warning text-dark">Pendiente</span>',
        'validado': '<span class="badge badge-status bg-success">Validado</span>',
        'rechazado': '<span class="badge badge-status bg-danger">Rechazado</span>'
    };
    return badges[estado] || `<span class="badge badge-status bg-secondary">${estado}</span>`;
}

/**
 * Filtrar por estado
 */
function filtrarPorEstado(estado) {
    estadoFiltro = estado;
    
    // Actualizar botones activos
    document.querySelectorAll('#filterButtons button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Recargar formularios
    loadFormularios();
}

/**
 * Abrir modal de validación
 */
async function abrirModalValidacion(formularioId) {
    try {
        const response = await APIClient.get(`/formularios/${formularioId}`);
        
        if (response.success) {
            formularioActual = response.data;
            mostrarDatosValidacion(formularioActual);
            
            const modal = new bootstrap.Modal(document.getElementById('validacionModal'));
            modal.show();
        }
    } catch (error) {
        console.error('Error loading formulario:', error);
        Utils.showError('Error al cargar formulario: ' + error.message);
    }
}

/**
 * Mostrar datos en modal de validación
 */
function mostrarDatosValidacion(formulario) {
    // Información de la mesa
    document.getElementById('valMesa').textContent = 
        `${formulario.mesa.codigo} - ${formulario.mesa.nombre}`;
    document.getElementById('valTestigo').textContent = 
        formulario.testigo ? formulario.testigo.nombre : 'N/A';
    
    // Datos de votación
    document.getElementById('valVotantesRegistrados').textContent = 
        Utils.formatNumber(formulario.total_votantes_registrados);
    document.getElementById('valTotalVotos').textContent = 
        Utils.formatNumber(formulario.total_votos);
    document.getElementById('valVotosValidos').textContent = 
        Utils.formatNumber(formulario.votos_validos);
    document.getElementById('valVotosNulos').textContent = 
        Utils.formatNumber(formulario.votos_nulos);
    document.getElementById('valVotosBlanco').textContent = 
        Utils.formatNumber(formulario.votos_blanco);
    document.getElementById('valTarjetasNoMarcadas').textContent = 
        Utils.formatNumber(formulario.tarjetas_no_marcadas);
    
    // Imagen del formulario
    const imagenContainer = document.getElementById('imagenFormulario');
    if (formulario.imagen_url) {
        imagenContainer.innerHTML = `
            <img src="${formulario.imagen_url}" alt="Formulario E-14" 
                 onclick="this.requestFullscreen()" style="cursor: zoom-in;">
        `;
    } else {
        imagenContainer.innerHTML = '<p class="text-muted">No hay imagen disponible</p>';
    }
    
    // Validaciones automáticas
    mostrarValidaciones(formulario.validaciones);
    
    // Votos por partido
    mostrarVotosPartidos(formulario.votos_partidos);
    
    // Observaciones
    document.getElementById('valObservaciones').textContent = 
        formulario.observaciones || 'Sin observaciones';
}

/**
 * Mostrar validaciones automáticas
 */
function mostrarValidaciones(validaciones) {
    const container = document.getElementById('validacionesAutomaticas');
    
    if (!validaciones) {
        container.innerHTML = '<p class="text-muted">No hay validaciones disponibles</p>';
        return;
    }
    
    let html = '';
    
    // Verificar coherencia
    if (validaciones.coincide_votos_validos && validaciones.coincide_total_votos && validaciones.coincide_total_tarjetas) {
        html += `
            <div class="validation-alert success">
                <i class="bi bi-check-circle"></i> Todos los totales coinciden correctamente
            </div>
        `;
    } else {
        if (!validaciones.coincide_votos_validos) {
            html += `
                <div class="validation-alert error">
                    <i class="bi bi-x-circle"></i> La suma de votos por partido (${validaciones.total_votos_calculado}) 
                    no coincide con votos válidos (${validaciones.votos_validos})
                </div>
            `;
        }
        if (!validaciones.coincide_total_votos) {
            html += `
                <div class="validation-alert error">
                    <i class="bi bi-x-circle"></i> La suma de votos válidos + nulos + blanco no coincide con el total de votos
                </div>
            `;
        }
        if (!validaciones.coincide_total_tarjetas) {
            html += `
                <div class="validation-alert error">
                    <i class="bi bi-x-circle"></i> La suma de votos + tarjetas no marcadas no coincide con el total de tarjetas
                </div>
            `;
        }
    }
    
    // Verificar discrepancias
    if (validaciones.discrepancia_porcentaje > 5) {
        html += `
            <div class="validation-alert warning">
                <i class="bi bi-exclamation-triangle"></i> Discrepancia del ${validaciones.discrepancia_porcentaje}% 
                entre votantes registrados y votos emitidos
            </div>
        `;
    }
    
    container.innerHTML = html;
}

/**
 * Mostrar votos por partido
 */
function mostrarVotosPartidos(votosPartidos) {
    const container = document.getElementById('votosPartidosList');
    
    if (!votosPartidos || votosPartidos.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay votos registrados</p>';
        return;
    }
    
    container.innerHTML = votosPartidos.map(vp => `
        <div class="data-field">
            <label>
                <span style="display: inline-block; width: 12px; height: 12px; background-color: ${vp.partido_color}; border-radius: 2px; margin-right: 4px;"></span>
                ${vp.partido_nombre}
            </label>
            <div class="value">${Utils.formatNumber(vp.votos)} votos</div>
        </div>
    `).join('');
}

/**
 * Validar formulario
 */
async function validarFormulario() {
    if (!formularioActual) return;
    
    if (!confirm('¿Está seguro de validar este formulario? Esta acción no se puede deshacer.')) {
        return;
    }
    
    try {
        const response = await APIClient.put(`/formularios/${formularioActual.id}/validar`, {
            comentario: 'Formulario validado por coordinador'
        });
        
        if (response.success) {
            Utils.showSuccess('Formulario validado exitosamente');
            
            // Cerrar modal
            bootstrap.Modal.getInstance(document.getElementById('validacionModal')).hide();
            
            // Recargar datos
            loadFormularios();
            loadConsolidado();
        }
    } catch (error) {
        console.error('Error validating formulario:', error);
        Utils.showError('Error al validar formulario: ' + error.message);
    }
}

/**
 * Mostrar modal de rechazo
 */
function mostrarModalRechazo() {
    // Cerrar modal de validación
    bootstrap.Modal.getInstance(document.getElementById('validacionModal')).hide();
    
    // Limpiar campo de motivo
    document.getElementById('motivoRechazo').value = '';
    
    // Mostrar modal de rechazo
    const modal = new bootstrap.Modal(document.getElementById('rechazoModal'));
    modal.show();
}

/**
 * Seleccionar motivo común
 */
function seleccionarMotivo(motivo) {
    document.getElementById('motivoRechazo').value = motivo;
}

/**
 * Confirmar rechazo
 */
async function confirmarRechazo() {
    if (!formularioActual) return;
    
    const motivo = document.getElementById('motivoRechazo').value.trim();
    
    if (!motivo) {
        Utils.showError('Debe ingresar un motivo de rechazo');
        return;
    }
    
    try {
        const response = await APIClient.put(`/formularios/${formularioActual.id}/rechazar`, {
            motivo: motivo
        });
        
        if (response.success) {
            Utils.showSuccess('Formulario rechazado. El testigo será notificado.');
            
            // Cerrar modal
            bootstrap.Modal.getInstance(document.getElementById('rechazoModal')).hide();
            
            // Recargar datos
            loadFormularios();
        }
    } catch (error) {
        console.error('Error rejecting formulario:', error);
        Utils.showError('Error al rechazar formulario: ' + error.message);
    }
}

/**
 * Ver detalles de formulario (solo lectura)
 */
async function verDetalles(formularioId) {
    await abrirModalValidacion(formularioId);
    
    // Deshabilitar botones de acción
    const modal = document.getElementById('validacionModal');
    modal.querySelector('.modal-footer .btn-danger').style.display = 'none';
    modal.querySelector('.modal-footer .btn-success').style.display = 'none';
}

/**
 * Cargar consolidado del puesto
 */
async function loadConsolidado() {
    try {
        const response = await APIClient.get('/formularios/consolidado');
        
        if (response.success) {
            renderConsolidado(response.data);
        } else {
            throw new Error(response.error || 'Error al cargar consolidado');
        }
    } catch (error) {
        console.error('Error loading consolidado:', error);
        const errorMsg = error.message || 'Error al cargar consolidado';
        document.getElementById('consolidadoPanel').innerHTML = `
            <div class="text-center py-3">
                <p class="text-danger mb-2">❌ ${errorMsg}</p>
                <button class="btn btn-sm btn-outline-primary" onclick="loadConsolidado()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    }
}

/**
 * Renderizar consolidado
 */
function renderConsolidado(data) {
    const container = document.getElementById('consolidadoPanel');
    
    if (!data || !data.votos_por_partido || data.votos_por_partido.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay datos consolidados aún</p>';
        return;
    }
    
    const resumen = data.resumen;
    const participacion = resumen.participacion_porcentaje || 0;
    
    let html = `
        <div class="mb-3">
            <small class="text-muted">Total Votos</small>
            <h4>${Utils.formatNumber(resumen.total_votos)}</h4>
            <small class="text-muted">Participación: ${participacion.toFixed(2)}%</small>
        </div>
        <hr>
        <h6 class="mb-2">Votos por Partido</h6>
    `;
    
    data.votos_por_partido.forEach(partido => {
        html += `
            <div class="mb-2">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <small>
                        <span style="display: inline-block; width: 10px; height: 10px; background-color: ${partido.partido_color}; border-radius: 2px; margin-right: 4px;"></span>
                        ${partido.partido_nombre_corto}
                    </small>
                    <strong>${Utils.formatNumber(partido.total_votos)}</strong>
                </div>
                <div class="progress" style="height: 8px;">
                    <div class="progress-bar" role="progressbar" 
                         style="width: ${partido.porcentaje}%; background-color: ${partido.partido_color};"
                         aria-valuenow="${partido.porcentaje}" aria-valuemin="0" aria-valuemax="100">
                    </div>
                </div>
                <small class="text-muted">${partido.porcentaje.toFixed(2)}%</small>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

/**
 * Cargar lista de mesas
 */
async function loadMesas() {
    try {
        const response = await APIClient.get('/formularios/mesas');
        
        if (response.success) {
            renderMesas(response.data || []);
        } else {
            throw new Error(response.error || 'Error al cargar mesas');
        }
    } catch (error) {
        console.error('Error loading mesas:', error);
        const errorMsg = error.message || 'Error al cargar mesas';
        document.getElementById('mesasPanel').innerHTML = `
            <div class="text-center py-3">
                <p class="text-danger mb-2">❌ ${errorMsg}</p>
                <button class="btn btn-sm btn-outline-primary" onclick="loadMesas()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    }
}

/**
 * Renderizar lista de mesas
 */
function renderMesas(mesas) {
    const container = document.getElementById('mesasPanel');
    
    if (!mesas || mesas.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay mesas asignadas</p>';
        return;
    }
    
    let html = '<div class="list-group list-group-flush">';
    
    mesas.forEach(mesa => {
        const icon = mesa.tiene_formulario ? 
            (mesa.estado_formulario === 'validado' ? '✅' : '⏳') : '❌';
        const estadoText = mesa.tiene_formulario ? 
            (mesa.estado_formulario === 'validado' ? 'Validado' : 'Pendiente') : 'Sin reporte';
        
        html += `
            <div class="list-group-item px-2 py-2">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${icon} Mesa ${mesa.mesa_codigo}</strong><br>
                        <small class="text-muted">${mesa.testigo_nombre || 'Sin testigo'}</small>
                    </div>
                    <small class="badge bg-${mesa.tiene_formulario ? (mesa.estado_formulario === 'validado' ? 'success' : 'warning') : 'secondary'}">
                        ${estadoText}
                    </small>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

/**
 * Función global para logout
 */
async function logout() {
    try {
        await APIClient.logout();
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
        window.location.href = '/login';
    }
}
