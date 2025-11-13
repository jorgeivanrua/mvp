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
    loadTestigos();
    
    // Auto-refresh cada 30 segundos
    autoRefreshInterval = setInterval(() => {
        loadFormularios();
        loadConsolidado();
        loadMesas();
        loadTestigos();
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
        container.innerHTML = '<p class="text-muted">No hay mesas asignadas a este puesto</p>';
        return;
    }
    
    // Agrupar mesas por estado
    const mesasConTestigo = mesas.filter(m => m.testigo_id);
    const mesasSinTestigo = mesas.filter(m => !m.testigo_id);
    const mesasValidadas = mesas.filter(m => m.estado_formulario === 'validado');
    const mesasPendientes = mesas.filter(m => m.tiene_formulario && m.estado_formulario === 'pendiente');
    const mesasSinReporte = mesas.filter(m => !m.tiene_formulario && m.testigo_id);
    
    let html = `
        <div class="mb-3">
            <div class="row g-2 text-center">
                <div class="col-6">
                    <div class="p-2 bg-success bg-opacity-10 rounded">
                        <h5 class="mb-0">${mesasValidadas.length}</h5>
                        <small class="text-muted">Validadas</small>
                    </div>
                </div>
                <div class="col-6">
                    <div class="p-2 bg-warning bg-opacity-10 rounded">
                        <h5 class="mb-0">${mesasPendientes.length}</h5>
                        <small class="text-muted">Pendientes</small>
                    </div>
                </div>
                <div class="col-6">
                    <div class="p-2 bg-secondary bg-opacity-10 rounded">
                        <h5 class="mb-0">${mesasSinReporte.length}</h5>
                        <small class="text-muted">Sin reporte</small>
                    </div>
                </div>
                <div class="col-6">
                    <div class="p-2 bg-danger bg-opacity-10 rounded">
                        <h5 class="mb-0">${mesasSinTestigo.length}</h5>
                        <small class="text-muted">Sin testigo</small>
                    </div>
                </div>
            </div>
        </div>
        <hr>
    `;
    
    // Mostrar mesas sin testigo primero (alerta)
    if (mesasSinTestigo.length > 0) {
        html += `
            <div class="alert alert-danger py-2 mb-2">
                <strong>⚠️ ${mesasSinTestigo.length} mesa(s) sin testigo asignado</strong>
            </div>
        `;
    }
    
    html += '<div class="list-group list-group-flush" style="max-height: 400px; overflow-y: auto;">';
    
    // Ordenar mesas: sin testigo primero, luego sin reporte, luego pendientes, luego validadas
    const mesasOrdenadas = [
        ...mesasSinTestigo.map(m => ({...m, prioridad: 1})),
        ...mesasSinReporte.map(m => ({...m, prioridad: 2})),
        ...mesasPendientes.map(m => ({...m, prioridad: 3})),
        ...mesasValidadas.map(m => ({...m, prioridad: 4}))
    ];
    
    mesasOrdenadas.forEach(mesa => {
        let icon, estadoText, badgeClass, testigoInfo;
        
        if (!mesa.testigo_id) {
            icon = '❌';
            estadoText = 'Sin testigo';
            badgeClass = 'bg-danger';
            testigoInfo = '<small class="text-danger"><i class="bi bi-exclamation-triangle"></i> Sin testigo asignado</small>';
        } else if (!mesa.tiene_formulario) {
            icon = '⏸️';
            estadoText = 'Sin reporte';
            badgeClass = 'bg-secondary';
            let presenciaInfo = '';
            if (mesa.testigo_presente) {
                const tiempoPresencia = mesa.testigo_presente_desde ? 
                    ` desde ${Utils.formatDate(mesa.testigo_presente_desde)}` : '';
                presenciaInfo = `<i class="bi bi-check-circle-fill text-success" title="Presente${tiempoPresencia}"></i>`;
            } else {
                presenciaInfo = '<i class="bi bi-person text-warning" title="No ha verificado presencia"></i>';
            }
            testigoInfo = `<small class="text-muted">${presenciaInfo} ${mesa.testigo_nombre}</small>`;
        } else if (mesa.estado_formulario === 'validado') {
            icon = '✅';
            estadoText = 'Validado';
            badgeClass = 'bg-success';
            testigoInfo = `<small class="text-muted"><i class="bi bi-person-check"></i> ${mesa.testigo_nombre}</small>`;
        } else if (mesa.estado_formulario === 'pendiente') {
            icon = '⏳';
            estadoText = 'Pendiente Validación';
            badgeClass = 'bg-warning text-dark';
            let presenciaInfo = '';
            if (mesa.testigo_presente) {
                presenciaInfo = '<i class="bi bi-check-circle-fill text-success" title="Testigo presente"></i>';
            } else {
                presenciaInfo = '<i class="bi bi-person text-muted"></i>';
            }
            testigoInfo = `<small class="text-muted">${presenciaInfo} ${mesa.testigo_nombre} - <strong>Formulario enviado</strong></small>`;
        } else if (mesa.estado_formulario === 'rechazado') {
            icon = '🔄';
            estadoText = 'Rechazado';
            badgeClass = 'bg-danger';
            testigoInfo = `<small class="text-danger"><i class="bi bi-person-x"></i> ${mesa.testigo_nombre}</small>`;
        } else {
            icon = '📋';
            estadoText = 'Borrador';
            badgeClass = 'bg-info';
            let presenciaInfo = '';
            if (mesa.testigo_presente) {
                presenciaInfo = '<i class="bi bi-check-circle-fill text-success" title="Testigo presente"></i>';
            } else {
                presenciaInfo = '<i class="bi bi-person text-muted"></i>';
            }
            testigoInfo = `<small class="text-muted">${presenciaInfo} ${mesa.testigo_nombre}</small>`;
        }
        
        html += `
            <div class="list-group-item px-2 py-2 ${!mesa.testigo_id ? 'border-danger border-start border-3' : ''}">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-1">
                            <span class="me-2">${icon}</span>
                            <strong>Mesa ${mesa.mesa_codigo}</strong>
                        </div>
                        ${testigoInfo}
                        ${mesa.total_votantes_registrados ? 
                            `<small class="text-muted d-block"><i class="bi bi-people"></i> ${Utils.formatNumber(mesa.total_votantes_registrados)} votantes</small>` 
                            : ''}
                    </div>
                    <span class="badge ${badgeClass} ms-2">${estadoText}</span>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

/**
 * Habilitar modo de edición
 */
function habilitarEdicion() {
    // Mostrar inputs y ocultar valores
    document.querySelectorAll('.data-field .value').forEach(el => el.classList.add('d-none'));
    document.querySelectorAll('.data-field input').forEach(el => el.classList.remove('d-none'));
    
    // Copiar valores actuales a los inputs
    document.getElementById('editVotantesRegistrados').value = formularioActual.total_votantes_registrados;
    document.getElementById('editTotalVotos').value = formularioActual.total_votos;
    document.getElementById('editVotosValidos').value = formularioActual.votos_validos;
    document.getElementById('editVotosNulos').value = formularioActual.votos_nulos;
    document.getElementById('editVotosBlanco').value = formularioActual.votos_blanco;
    document.getElementById('editTarjetasNoMarcadas').value = formularioActual.tarjetas_no_marcadas;
    
    // Mostrar alerta de edición
    document.getElementById('alertaEdicion').classList.remove('d-none');
    
    // Cambiar botones
    document.getElementById('btnEditarDatos').classList.add('d-none');
    document.getElementById('btnValidar').classList.add('d-none');
    document.getElementById('btnRechazar').classList.add('d-none');
    document.getElementById('btnCancelarEdicion').classList.remove('d-none');
    document.getElementById('btnValidarConCambios').classList.remove('d-none');
}

/**
 * Cancelar edición
 */
function cancelarEdicion() {
    // Ocultar inputs y mostrar valores
    document.querySelectorAll('.data-field .value').forEach(el => el.classList.remove('d-none'));
    document.querySelectorAll('.data-field input').forEach(el => el.classList.add('d-none'));
    
    // Ocultar alerta de edición
    document.getElementById('alertaEdicion').classList.add('d-none');
    
    // Restaurar botones
    document.getElementById('btnEditarDatos').classList.remove('d-none');
    document.getElementById('btnValidar').classList.remove('d-none');
    document.getElementById('btnRechazar').classList.remove('d-none');
    document.getElementById('btnCancelarEdicion').classList.add('d-none');
    document.getElementById('btnValidarConCambios').classList.add('d-none');
}

/**
 * Validar con cambios
 */
async function validarConCambios() {
    if (!formularioActual) return;
    
    // Obtener valores editados
    const cambios = {
        total_votos: parseInt(document.getElementById('editTotalVotos').value),
        votos_validos: parseInt(document.getElementById('editVotosValidos').value),
        votos_nulos: parseInt(document.getElementById('editVotosNulos').value),
        votos_blanco: parseInt(document.getElementById('editVotosBlanco').value),
        tarjetas_no_marcadas: parseInt(document.getElementById('editTarjetasNoMarcadas').value)
    };
    
    // Calcular total de tarjetas
    cambios.total_tarjetas = cambios.total_votos + cambios.tarjetas_no_marcadas;
    
    // Validar coherencia básica
    const sumaVotos = cambios.votos_validos + cambios.votos_nulos + cambios.votos_blanco;
    if (sumaVotos !== cambios.total_votos) {
        Utils.showError(`La suma de votos válidos (${cambios.votos_validos}) + nulos (${cambios.votos_nulos}) + blanco (${cambios.votos_blanco}) debe ser igual al total de votos (${cambios.total_votos})`);
        return;
    }
    
    if (!confirm('¿Está seguro de validar este formulario con los cambios realizados? Los cambios quedarán registrados en el historial.')) {
        return;
    }
    
    try {
        const response = await APIClient.put(`/formularios/${formularioActual.id}/validar`, {
            cambios: cambios,
            comentario: 'Formulario editado y validado por coordinador'
        });
        
        if (response.success) {
            Utils.showSuccess('Formulario validado exitosamente con cambios registrados');
            
            // Cerrar modal
            bootstrap.Modal.getInstance(document.getElementById('validacionModal')).hide();
            
            // Recargar datos
            loadFormularios();
            loadConsolidado();
            
            // Resetear modo de edición
            cancelarEdicion();
        }
    } catch (error) {
        console.error('Error validating formulario with changes:', error);
        Utils.showError('Error al validar formulario: ' + error.message);
    }
}

/**
 * Cargar datos del E-24
 */
async function loadE24Data() {
    try {
        // Cargar mesas y consolidado
        const [mesasResponse, consolidadoResponse] = await Promise.all([
            APIClient.get('/formularios/mesas'),
            APIClient.get('/formularios/consolidado')
        ]);
        
        if (mesasResponse.success && consolidadoResponse.success) {
            renderE24Table(mesasResponse.data, consolidadoResponse.data);
        }
    } catch (error) {
        console.error('Error loading E-24 data:', error);
        const tbody = document.querySelector('#e24Table tbody');
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4">
                    <p class="text-danger">Error al cargar datos del E-24</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="loadE24Data()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </td>
            </tr>
        `;
    }
}

/**
 * Renderizar tabla E-24
 */
function renderE24Table(mesas, consolidado) {
    const tbody = document.querySelector('#e24Table tbody');
    
    if (!mesas || mesas.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center py-4">No hay mesas en este puesto</td></tr>';
        return;
    }
    
    // Calcular totales
    let totalVotantes = 0;
    let totalVotos = 0;
    let totalValidos = 0;
    let totalNulos = 0;
    let totalBlanco = 0;
    let mesasValidadas = 0;
    
    // Renderizar filas
    tbody.innerHTML = mesas.map(mesa => {
        const votantes = mesa.total_votantes_registrados || 0;
        totalVotantes += votantes;
        
        let votos = mesa.total_votos || 0;
        let validos = mesa.votos_validos || 0;
        let nulos = mesa.votos_nulos || 0;
        let blanco = mesa.votos_blanco || 0;
        let participacion = 0;
        let estadoBadge = '<span class="badge bg-secondary">Sin reporte</span>';
        
        if (mesa.tiene_formulario && mesa.estado_formulario === 'validado') {
            estadoBadge = '<span class="badge bg-success">Validado</span>';
            mesasValidadas++;
        } else if (mesa.tiene_formulario && mesa.estado_formulario === 'pendiente') {
            estadoBadge = '<span class="badge bg-warning text-dark">Pendiente</span>';
        } else if (mesa.tiene_formulario && mesa.estado_formulario === 'rechazado') {
            estadoBadge = '<span class="badge bg-danger">Rechazado</span>';
        }
        
        if (votantes > 0 && votos > 0) {
            participacion = ((votos / votantes) * 100).toFixed(2);
        }
        
        totalVotos += votos;
        totalValidos += validos;
        totalNulos += nulos;
        totalBlanco += blanco;
        
        return `
            <tr>
                <td><strong>${mesa.mesa_codigo}</strong></td>
                <td><small>${mesa.testigo_nombre || 'Sin asignar'}</small></td>
                <td>${estadoBadge}</td>
                <td class="text-end">${Utils.formatNumber(votantes)}</td>
                <td class="text-end">${votos > 0 ? Utils.formatNumber(votos) : '-'}</td>
                <td class="text-end">${validos > 0 ? Utils.formatNumber(validos) : '-'}</td>
                <td class="text-end">${nulos > 0 ? Utils.formatNumber(nulos) : '-'}</td>
                <td class="text-end">${blanco > 0 ? Utils.formatNumber(blanco) : '-'}</td>
                <td class="text-end">${participacion > 0 ? participacion + '%' : '-'}</td>
            </tr>
        `;
    }).join('');
    
    // Actualizar totales
    const participacionTotal = totalVotantes > 0 ? ((totalVotos / totalVotantes) * 100).toFixed(2) : 0;
    
    document.getElementById('e24TotalMesas').textContent = mesas.length;
    document.getElementById('e24MesasValidadas').textContent = mesasValidadas;
    document.getElementById('e24TotalVotos').textContent = Utils.formatNumber(totalVotos);
    document.getElementById('e24Participacion').textContent = participacionTotal + '%';
    
    document.getElementById('e24FooterVotantes').textContent = Utils.formatNumber(totalVotantes);
    document.getElementById('e24FooterVotos').textContent = Utils.formatNumber(totalVotos);
    document.getElementById('e24FooterValidos').textContent = Utils.formatNumber(totalValidos);
    document.getElementById('e24FooterNulos').textContent = Utils.formatNumber(totalNulos);
    document.getElementById('e24FooterBlanco').textContent = Utils.formatNumber(totalBlanco);
    document.getElementById('e24FooterParticipacion').textContent = participacionTotal + '%';
    
    // Renderizar votos por partido
    if (consolidado && consolidado.votos_por_partido) {
        renderE24VotosPartidos(consolidado.votos_por_partido);
    }
}

/**
 * Renderizar votos por partido en E-24
 */
function renderE24VotosPartidos(votosPartidos) {
    const container = document.getElementById('e24VotosPartidos');
    
    if (!votosPartidos || votosPartidos.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay votos consolidados aún</p>';
        return;
    }
    
    let html = '<div class="table-responsive"><table class="table table-bordered">';
    html += '<thead class="table-light"><tr><th>Partido</th><th class="text-end">Votos</th><th class="text-end">Porcentaje</th></tr></thead>';
    html += '<tbody>';
    
    votosPartidos.forEach(partido => {
        html += `
            <tr>
                <td>
                    <span style="display: inline-block; width: 12px; height: 12px; background-color: ${partido.partido_color}; border-radius: 2px; margin-right: 8px;"></span>
                    <strong>${partido.partido_nombre}</strong>
                </td>
                <td class="text-end">${Utils.formatNumber(partido.total_votos)}</td>
                <td class="text-end">${partido.porcentaje.toFixed(2)}%</td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

/**
 * Generar PDF del E-24
 */
function generarPDFE24() {
    Utils.showInfo('Funcionalidad de generación de PDF en desarrollo');
    // TODO: Implementar generación de PDF
}

// Event listener para cambio de pestaña
document.addEventListener('DOMContentLoaded', function() {
    const e24Tab = document.getElementById('e24-tab');
    if (e24Tab) {
        e24Tab.addEventListener('shown.bs.tab', function() {
            loadE24Data();
        });
    }
});

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


/**
 * Cargar lista de testigos del puesto
 */
async function loadTestigos() {
    try {
        const response = await APIClient.get('/formularios/testigos-puesto');
        
        if (response.success) {
            renderTestigos(response.data || []);
        } else {
            throw new Error(response.error || 'Error al cargar testigos');
        }
    } catch (error) {
        console.error('Error loading testigos:', error);
        document.getElementById('testigosPanel').innerHTML = `
            <div class="text-center py-2">
                <p class="text-muted mb-2">Error al cargar testigos</p>
                <button class="btn btn-sm btn-outline-primary" onclick="loadTestigos()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    }
}

/**
 * Renderizar lista de testigos
 */
function renderTestigos(testigos) {
    const container = document.getElementById('testigosPanel');
    
    if (!testigos || testigos.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay testigos asignados a este puesto</p>';
        return;
    }
    
    // Separar testigos presentes y ausentes
    const testigosPresentes = testigos.filter(t => t.presencia_verificada);
    const testigosAusentes = testigos.filter(t => !t.presencia_verificada);
    
    let html = `
        <div class="mb-2">
            <small class="text-muted">
                <i class="bi bi-check-circle-fill text-success"></i> ${testigosPresentes.length} presente(s) | 
                <i class="bi bi-circle text-secondary"></i> ${testigosAusentes.length} ausente(s)
            </small>
        </div>
        <div class="list-group list-group-flush">
    `;
    
    // Mostrar testigos presentes primero
    testigosPresentes.forEach(testigo => {
        const tiempoPresencia = testigo.presencia_verificada_at ? 
            Utils.formatDate(testigo.presencia_verificada_at) : '';
        
        html += `
            <div class="list-group-item px-2 py-2 border-start border-success border-3">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <i class="bi bi-check-circle-fill text-success"></i>
                        <strong>${testigo.nombre}</strong>
                        <br>
                        <small class="text-muted">
                            <i class="bi bi-telephone"></i> ${testigo.telefono || 'Sin teléfono'}
                        </small>
                        ${tiempoPresencia ? 
                            `<br><small class="text-success">Presente desde ${tiempoPresencia}</small>` : 
                            ''
                        }
                    </div>
                    <span class="badge bg-success">Presente</span>
                </div>
            </div>
        `;
    });
    
    // Mostrar testigos ausentes
    testigosAusentes.forEach(testigo => {
        const ultimoAcceso = testigo.last_login ? 
            `Último acceso: ${Utils.formatDate(testigo.last_login)}` : 
            'Nunca ha ingresado';
        
        html += `
            <div class="list-group-item px-2 py-2">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <i class="bi bi-circle text-secondary"></i>
                        <strong>${testigo.nombre}</strong>
                        <br>
                        <small class="text-muted">
                            <i class="bi bi-telephone"></i> ${testigo.telefono || 'Sin teléfono'}
                        </small>
                        <br>
                        <small class="text-muted">${ultimoAcceso}</small>
                    </div>
                    <span class="badge bg-secondary">Ausente</span>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}
