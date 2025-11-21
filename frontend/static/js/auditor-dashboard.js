/**
 * Dashboard del Auditor Electoral
 */

let currentUser = null;
let departamento = null;
let formularios = [];
let discrepancias = [];
let filtroEstado = '';
let filtroMunicipio = '';
let autoRefreshInterval = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadStats();
    loadFormularios();
    loadDiscrepancias();
    loadMunicipios();
    
    // Auto-refresh cada 60 segundos
    autoRefreshInterval = setInterval(() => {
        loadStats();
        loadFormularios();
        loadDiscrepancias();
    }, 60000);
});

// Limpiar interval al salir
window.addEventListener('beforeunload', function() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});

/**
 * Cargar perfil del auditor
 */
async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        
        if (response.success) {
            currentUser = response.data.user;
            departamento = response.data.ubicacion;
            
            if (departamento) {
                document.getElementById('departamentoNombre').textContent = 
                    departamento.departamento_nombre || departamento.nombre_completo;
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        Utils.showError('Error al cargar perfil');
    }
}

/**
 * Cargar estadísticas de auditoría
 */
async function loadStats() {
    try {
        const response = await APIClient.get('/auditor/stats');
        
        if (response.success) {
            const stats = response.data;
            
            // Actualizar estadísticas
            document.getElementById('statTotalFormularios').textContent = Utils.formatNumber(stats.total_formularios);
            document.getElementById('statCompletados').textContent = Utils.formatNumber(stats.formularios_completados);
            document.getElementById('statPendientes').textContent = Utils.formatNumber(stats.formularios_pendientes);
            document.getElementById('statInconsistencias').textContent = Utils.formatNumber(stats.inconsistencias_detectadas);
            document.getElementById('statPorcentajeAuditado').textContent = stats.porcentaje_auditado.toFixed(1) + '%';
        } else {
            throw new Error(response.error || 'Error al cargar estadísticas');
        }
    } catch (error) {
        console.error('Error loading stats:', error);
        Utils.showError('Error al cargar estadísticas');
    }
}

/**
 * Cargar lista de formularios
 */
async function loadFormularios() {
    try {
        const params = {};
        if (filtroEstado) {
            params.estado = filtroEstado;
        }
        
        const response = await APIClient.get('/auditor/formularios', params);
        
        if (response.success) {
            formularios = response.data || [];
            renderFormulariosTable(formularios);
        } else {
            throw new Error(response.error || 'Error al cargar formularios');
        }
    } catch (error) {
        console.error('Error loading formularios:', error);
        const tbody = document.querySelector('#formulariosTable tbody');
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <p class="text-danger mb-2">❌ Error al cargar formularios</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="loadFormularios()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </td>
            </tr>
        `;
    }
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
                    <p class="text-muted">No hay formularios ${filtroEstado ? 'en estado ' + filtroEstado : ''}</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = formularios.map(form => {
        const estadoBadge = getEstadoBadge(form.estado);
        const fecha = Utils.formatDate(form.updated_at || form.created_at);
        
        return `
            <tr onclick="verDetalleFormulario(${form.id})" style="cursor: pointer;">
                <td><strong>${form.id}</strong></td>
                <td>
                    <strong>${form.mesa_nombre || 'N/A'}</strong>
                </td>
                <td>${form.testigo_nombre || 'N/A'}</td>
                <td class="text-center">${estadoBadge}</td>
                <td><small>${fecha}</small></td>
                <td class="text-center">
                    <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); verDetalleFormulario(${form.id})">
                        <i class="bi bi-eye"></i> Ver
                    </button>
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
        'borrador': '<span class="badge bg-secondary">Borrador</span>',
        'pendiente': '<span class="badge bg-warning text-dark">Pendiente</span>',
        'validado': '<span class="badge bg-success">Validado</span>',
        'rechazado': '<span class="badge bg-danger">Rechazado</span>',
        'en_revision': '<span class="badge bg-info">En Revisión</span>'
    };
    return badges[estado] || `<span class="badge bg-secondary">${estado}</span>`;
}

/**
 * Filtrar formularios por estado
 */
function filtrarPorEstado(estado) {
    filtroEstado = estado;
    
    // Actualizar botones activos
    document.querySelectorAll('#filterButtons button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Recargar formularios
    loadFormularios();
}

/**
 * Ver detalle de formulario
 */
async function verDetalleFormulario(formularioId) {
    try {
        const response = await APIClient.get(`/formularios/${formularioId}`);
        
        if (response.success) {
            mostrarModalDetalle(response.data);
        }
    } catch (error) {
        console.error('Error loading formulario:', error);
        Utils.showError('Error al cargar formulario: ' + error.message);
    }
}

/**
 * Mostrar modal con detalle del formulario
 */
function mostrarModalDetalle(formulario) {
    const modal = new bootstrap.Modal(document.getElementById('detalleModal'));
    
    let html = `
        <h6>Formulario #${formulario.id}</h6>
        <hr>
        <p><strong>Mesa:</strong> ${formulario.mesa.nombre}</p>
        <p><strong>Testigo:</strong> ${formulario.testigo ? formulario.testigo.nombre : 'N/A'}</p>
        <p><strong>Estado:</strong> ${getEstadoBadge(formulario.estado)}</p>
        <hr>
        <h6>Datos de Votación</h6>
        <p><strong>Votantes Registrados:</strong> ${Utils.formatNumber(formulario.total_votantes_registrados)}</p>
        <p><strong>Total Votos:</strong> ${Utils.formatNumber(formulario.total_votos)}</p>
        <p><strong>Votos Válidos:</strong> ${Utils.formatNumber(formulario.votos_validos)}</p>
        <p><strong>Votos Nulos:</strong> ${Utils.formatNumber(formulario.votos_nulos)}</p>
        <p><strong>Votos en Blanco:</strong> ${Utils.formatNumber(formulario.votos_blanco)}</p>
    `;
    
    // Validaciones
    if (formulario.validaciones) {
        html += '<hr><h6>Validaciones</h6>';
        const val = formulario.validaciones;
        
        if (val.coincide_votos_validos && val.coincide_total_votos && val.coincide_total_tarjetas) {
            html += '<p class="text-success"><i class="bi bi-check-circle"></i> Todos los totales coinciden</p>';
        } else {
            if (!val.coincide_votos_validos) {
                html += '<p class="text-danger"><i class="bi bi-x-circle"></i> Discrepancia en votos válidos</p>';
            }
            if (!val.coincide_total_votos) {
                html += '<p class="text-danger"><i class="bi bi-x-circle"></i> Discrepancia en total de votos</p>';
            }
        }
    }
    
    // Imagen
    if (formulario.imagen_url) {
        html += `<hr><h6>Imagen del Acta</h6><img src="${formulario.imagen_url}" class="img-fluid" alt="Acta E-14">`;
    }
    
    document.getElementById('detalleFormularioContent').innerHTML = html;
    modal.show();
}

/**
 * Cargar discrepancias
 */
async function loadDiscrepancias() {
    try {
        const response = await APIClient.get('/auditor/discrepancias');
        
        if (response.success) {
            discrepancias = response.data || [];
            renderDiscrepancias(discrepancias);
        } else {
            throw new Error(response.error || 'Error al cargar discrepancias');
        }
    } catch (error) {
        console.error('Error loading discrepancias:', error);
        document.getElementById('discrepanciasPanel').innerHTML = `
            <div class="text-center py-3">
                <p class="text-danger mb-2">❌ Error al cargar discrepancias</p>
                <button class="btn btn-sm btn-outline-primary" onclick="loadDiscrepancias()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    }
}

/**
 * Renderizar discrepancias
 */
function renderDiscrepancias(discrepancias) {
    const container = document.getElementById('discrepanciasPanel');
    
    if (discrepancias.length === 0) {
        container.innerHTML = `
            <div class="text-center py-3">
                <i class="bi bi-check-circle text-success" style="font-size: 2rem;"></i>
                <p class="text-muted mb-0">No hay discrepancias detectadas</p>
            </div>
        `;
        return;
    }
    
    // Agrupar por severidad
    const criticas = discrepancias.filter(d => d.severidad === 'critica');
    const altas = discrepancias.filter(d => d.severidad === 'alta');
    const medias = discrepancias.filter(d => d.severidad === 'media');
    
    let html = '';
    
    // Mostrar críticas
    if (criticas.length > 0) {
        html += '<h6 class="text-danger mb-2"><i class="bi bi-exclamation-octagon"></i> Críticas</h6>';
        criticas.slice(0, 5).forEach(d => {
            html += renderDiscrepanciaItem(d);
        });
    }
    
    // Mostrar altas
    if (altas.length > 0) {
        html += '<h6 class="text-warning mb-2 mt-3"><i class="bi bi-exclamation-triangle"></i> Altas</h6>';
        altas.slice(0, 5).forEach(d => {
            html += renderDiscrepanciaItem(d);
        });
    }
    
    // Total
    html += `
        <div class="mt-3 text-center">
            <small class="text-muted">
                Total: ${discrepancias.length} discrepancia(s) detectada(s)
            </small>
        </div>
    `;
    
    container.innerHTML = html;
}

/**
 * Renderizar item de discrepancia
 */
function renderDiscrepanciaItem(discrepancia) {
    const severidadClass = {
        'critica': 'danger',
        'alta': 'warning',
        'media': 'info'
    };
    
    const badgeClass = severidadClass[discrepancia.severidad] || 'secondary';
    
    return `
        <div class="alert alert-${badgeClass} py-2 px-2 mb-2" role="alert" 
             style="cursor: pointer;" onclick="verDetalleFormulario(${discrepancia.formulario_id})">
            <small>
                <strong>${discrepancia.mesa_codigo}</strong> - ${discrepancia.mesa_nombre}<br>
                ${discrepancia.descripcion}
            </small>
        </div>
    `;
}

/**
 * Cargar municipios con estadísticas
 */
async function loadMunicipios() {
    try {
        const response = await APIClient.get('/auditor/municipios');
        
        if (response.success) {
            renderMunicipios(response.data || []);
        } else {
            throw new Error(response.error || 'Error al cargar municipios');
        }
    } catch (error) {
        console.error('Error loading municipios:', error);
        document.getElementById('municipiosPanel').innerHTML = `
            <div class="text-center py-3">
                <p class="text-danger mb-2">❌ Error al cargar municipios</p>
                <button class="btn btn-sm btn-outline-primary" onclick="loadMunicipios()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    }
}

/**
 * Renderizar municipios
 */
function renderMunicipios(municipios) {
    const container = document.getElementById('municipiosPanel');
    
    if (municipios.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay municipios</p>';
        return;
    }
    
    let html = '<div class="table-responsive"><table class="table table-sm">';
    html += '<thead class="table-light"><tr><th>Municipio</th><th>Mesas</th><th>Validados</th><th>Pendientes</th><th>Avance</th></tr></thead>';
    html += '<tbody>';
    
    municipios.forEach(municipio => {
        const progressColor = municipio.porcentaje_avance >= 90 ? 'success' : municipio.porcentaje_avance >= 50 ? 'warning' : 'danger';
        
        html += `
            <tr>
                <td><strong>${municipio.nombre}</strong></td>
                <td>${municipio.total_mesas}</td>
                <td><span class="badge bg-success">${municipio.formularios_validados}</span></td>
                <td><span class="badge bg-warning">${municipio.formularios_pendientes}</span></td>
                <td>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar bg-${progressColor}" style="width: ${municipio.porcentaje_avance}%;">
                            ${municipio.porcentaje_avance.toFixed(1)}%
                        </div>
                    </div>
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

/**
 * Cargar consolidado
 */
async function loadConsolidado() {
    try {
        const response = await APIClient.get('/auditor/consolidado');
        
        if (response.success) {
            renderConsolidado(response.data);
        } else {
            throw new Error(response.error || 'Error al cargar consolidado');
        }
    } catch (error) {
        console.error('Error loading consolidado:', error);
        document.getElementById('consolidadoPanel').innerHTML = `
            <div class="text-center py-3">
                <p class="text-danger mb-2">❌ Error al cargar consolidado</p>
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
        container.innerHTML = '<p class="text-muted">No hay datos consolidados</p>';
        return;
    }
    
    let html = `
        <div class="mb-3">
            <h6>Resumen Departamental</h6>
            <p><strong>Total Formularios:</strong> ${Utils.formatNumber(data.total_formularios)}</p>
            <p><strong>Total Votos:</strong> ${Utils.formatNumber(data.total_votos)}</p>
            <p><strong>Participación:</strong> ${data.porcentaje_participacion.toFixed(2)}%</p>
        </div>
        <hr>
        <h6 class="mb-3">Votos por Partido</h6>
    `;
    
    data.votos_por_partido.forEach(partido => {
        html += `
            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <div>
                        <span style="display: inline-block; width: 12px; height: 12px; background-color: ${partido.partido_color}; border-radius: 2px; margin-right: 8px;"></span>
                        <strong>${partido.partido_nombre}</strong>
                    </div>
                    <strong>${Utils.formatNumber(partido.total_votos)}</strong>
                </div>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar" style="width: ${partido.porcentaje}%; background-color: ${partido.partido_color};">
                        ${partido.porcentaje.toFixed(2)}%
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

/**
 * Exportar datos de auditoría
 */
async function exportarDatos() {
    try {
        const formato = 'csv';
        const url = `/api/auditor/exportar?formato=${formato}`;
        const token = localStorage.getItem('access_token');
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `auditoria_${new Date().getTime()}.csv`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            
            Utils.showSuccess('Datos exportados exitosamente');
        } else {
            throw new Error('Error al exportar datos');
        }
    } catch (error) {
        console.error('Error exporting data:', error);
        Utils.showError('Error al exportar datos: ' + error.message);
    }
}

/**
 * Generar reporte de auditoría
 */
function generarReporte() {
    Utils.showInfo('Funcionalidad de generación de reportes en desarrollo');
}

/**
 * Actualizar datos
 */
function actualizarDatos() {
    loadStats();
    loadFormularios();
    loadDiscrepancias();
    loadMunicipios();
    Utils.showSuccess('Datos actualizados');
}

/**
 * Logout
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
        window.location.href = '/auth/login';
    }
}

// Event listener para cargar consolidado al cambiar de pestaña
document.addEventListener('DOMContentLoaded', function() {
    const consolidadoTab = document.getElementById('consolidado-tab');
    if (consolidadoTab) {
        consolidadoTab.addEventListener('shown.bs.tab', function() {
            loadConsolidado();
        });
    }
});
