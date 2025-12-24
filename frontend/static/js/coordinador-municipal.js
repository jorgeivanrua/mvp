/**
 * Dashboard Coordinador Municipal
 * Gestión de puestos, consolidación municipal y generación de E-24
 */

// Variables globales
let puestosData = [];
let puestoSeleccionado = null;
let chartConsolidado = null;
let puestosSeleccionadosComparacion = [];

// ============================================================================
// INICIALIZACIÓN
// ============================================================================

document.addEventListener('DOMContentLoaded', async function() {
    console.log('[Municipal] Iniciando dashboard...');
    
    try {
        // 1. Cargar perfil del usuario
        await loadUserProfile();
        
        // 2. Cargar datos iniciales
        await Promise.all([
            loadEstadisticas(),
            loadPuestos(),
            loadConsolidadoMunicipal(),
            loadDiscrepancias(),
            loadTiposEleccion()
        ]);
        
        // 3. Configurar auto-refresh cada 60 segundos
        setInterval(async () => {
            console.log('[Municipal] Auto-refresh...');
            await Promise.all([
                loadEstadisticas(),
                loadPuestos(),
                loadDiscrepancias()
            ]);
        }, 60000);
        
        console.log('[Municipal] Dashboard inicializado correctamente');
        
    } catch (error) {
        console.error('[Municipal] Error inicializando dashboard:', error);
        Utils.showError('Error al cargar el dashboard. Por favor, recargue la página.');
    }
});

// ============================================================================
// CARGA DE DATOS
// ============================================================================

async function loadUserProfile() {
    try {
        const response = await APIClient.get('/auth/profile');
        
        if (response && response.success && response.data) {
            const user = response.data;
            const ubicacion = user.ubicacion;
            
            if (ubicacion && ubicacion.tipo === 'municipio') {
                document.getElementById('municipio-info').textContent = 
                    `${ubicacion.municipio_nombre || ubicacion.nombre_completo} - ${ubicacion.departamento_nombre}`;
            } else {
                document.getElementById('municipio-info').textContent = 'Municipio no asignado';
            }
        }
    } catch (error) {
        console.error('[Municipal] Error cargando perfil:', error);
    }
}

async function loadEstadisticas() {
    try {
        const response = await APIClient.get('/coordinador-municipal/estadisticas');
        
        if (response && response.success && response.data) {
            const stats = response.data.resumen_general;
            
            document.getElementById('stat-total-puestos').textContent = stats.total_puestos || 0;
            document.getElementById('stat-puestos-completos').textContent = stats.puestos_completos || 0;
            document.getElementById('stat-cobertura').textContent = `${Math.round(stats.porcentaje_avance || 0)}%`;
            document.getElementById('stat-discrepancias').textContent = stats.puestos_con_discrepancias || 0;
        }
    } catch (error) {
        console.error('[Municipal] Error cargando estadísticas:', error);
    }
}

async function loadPuestos() {
    try {
        const response = await APIClient.get('/coordinador-municipal/puestos');
        
        if (response && response.success && response.data) {
            puestosData = response.data.puestos;
            renderPuestosTable();
            updateFiltroZonas();
        }
    } catch (error) {
        console.error('[Municipal] Error cargando puestos:', error);
        document.getElementById('lista-puestos').innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle"></i> Error al cargar puestos
            </div>
        `;
    }
}

async function loadConsolidadoMunicipal() {
    try {
        const response = await APIClient.get('/coordinador-municipal/consolidado');
        
        if (response && response.success && response.data) {
            renderChartConsolidado(response.data);
        }
    } catch (error) {
        console.error('[Municipal] Error cargando consolidado:', error);
    }
}

async function loadDiscrepancias() {
    try {
        const response = await APIClient.get('/coordinador-municipal/discrepancias');
        
        if (response && response.success && response.data) {
            renderAlertas(response.data);
        }
    } catch (error) {
        console.error('[Municipal] Error cargando discrepancias:', error);
    }
}

async function loadTiposEleccion() {
    try {
        const response = await APIClient.get('/configuracion/tipos-eleccion');
        
        if (response && response.success && response.data) {
            const select = document.getElementById('tipo-eleccion-e24');
            select.innerHTML = '<option value="">Seleccione tipo de elección</option>';
            
            response.data.forEach(tipo => {
                select.innerHTML += `<option value="${tipo.id}">${tipo.nombre}</option>`;
            });
        }
    } catch (error) {
        console.error('[Municipal] Error cargando tipos de elección:', error);
    }
}

// ============================================================================
// RENDERIZADO DE DATOS
// ============================================================================

function renderPuestosTable() {
    const container = document.getElementById('lista-puestos');
    
    if (!puestosData || puestosData.length === 0) {
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-inbox text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted mt-3">No hay puestos registrados</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    puestosData.forEach(puesto => {
        const estadoBadge = getEstadoBadge(puesto.estado);
        const porcentaje = puesto.porcentaje_avance || 0;
        
        html += `
            <div class="puesto-item ${puestoSeleccionado?.id === puesto.id ? 'selected' : ''}" 
                 onclick="seleccionarPuesto(${puesto.id})">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h6 class="mb-1">${puesto.nombre}</h6>
                        <small class="text-muted">Código: ${puesto.codigo} | Zona: ${puesto.zona_codigo}</small>
                    </div>
                    <span class="badge ${estadoBadge.class}">${estadoBadge.text}</span>
                </div>
                
                <div class="row text-center mb-2">
                    <div class="col-3">
                        <small class="text-muted d-block">Mesas</small>
                        <strong>${puesto.total_mesas}</strong>
                    </div>
                    <div class="col-3">
                        <small class="text-muted d-block">Validados</small>
                        <strong class="text-success">${puesto.formularios_validados}</strong>
                    </div>
                    <div class="col-3">
                        <small class="text-muted d-block">Pendientes</small>
                        <strong class="text-warning">${puesto.formularios_pendientes}</strong>
                    </div>
                    <div class="col-3">
                        <small class="text-muted d-block">Rechazados</small>
                        <strong class="text-danger">${puesto.formularios_rechazados}</strong>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${porcentaje}%"></div>
                </div>
                <small class="text-muted">${porcentaje.toFixed(1)}% completado</small>
                
                ${puesto.coordinador ? `
                    <div class="mt-2">
                        <small class="text-muted">
                            <i class="bi bi-person"></i> ${puesto.coordinador.nombre}
                            ${puesto.coordinador.ultimo_acceso ? 
                                `<span class="text-success">● Online</span>` : 
                                `<span class="text-secondary">● Offline</span>`
                            }
                        </small>
                    </div>
                ` : `
                    <div class="mt-2">
                        <small class="text-warning">
                            <i class="bi bi-exclamation-triangle"></i> Sin coordinador asignado
                        </small>
                    </div>
                `}
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function renderChartConsolidado(data) {
    const ctx = document.getElementById('chart-consolidado');
    
    if (chartConsolidado) {
        chartConsolidado.destroy();
    }
    
    if (!data.votos_por_partido || data.votos_por_partido.length === 0) {
        ctx.parentElement.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-pie-chart text-muted" style="font-size: 2rem;"></i>
                <p class="text-muted mt-2">No hay datos de consolidado</p>
            </div>
        `;
        return;
    }
    
    const labels = data.votos_por_partido.map(vp => vp.partido_nombre_corto || vp.partido_nombre);
    const votos = data.votos_por_partido.map(vp => vp.total_votos);
    const colores = data.votos_por_partido.map(vp => vp.partido_color || '#6c757d');
    
    chartConsolidado = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: votos,
                backgroundColor: colores,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true,
                        font: {
                            size: 11
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const partido = data.votos_por_partido[context.dataIndex];
                            return `${partido.partido_nombre}: ${partido.total_votos.toLocaleString()} votos (${partido.porcentaje.toFixed(1)}%)`;
                        }
                    }
                }
            }
        }
    });
}

function renderAlertas(discrepancias) {
    const container = document.getElementById('lista-alertas');
    const contador = document.getElementById('contador-alertas');
    
    contador.textContent = discrepancias.length;
    
    if (discrepancias.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No hay alertas</p>';
        return;
    }
    
    let html = '';
    
    discrepancias.forEach(disc => {
        const severidadClass = disc.severidad === 'critica' ? 'critica' : '';
        
        html += `
            <div class="alert-item ${severidadClass}" onclick="seleccionarPuestoPorId(${disc.puesto_id})">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <strong>${disc.puesto_nombre}</strong>
                        <p class="mb-1 small">${disc.descripcion}</p>
                        <small class="text-muted">Severidad: ${disc.severidad}</small>
                    </div>
                    <span class="badge bg-${disc.severidad === 'critica' ? 'danger' : 'warning'}">
                        ${disc.severidad}
                    </span>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// ============================================================================
// INTERACCIONES
// ============================================================================

async function seleccionarPuesto(puestoId) {
    try {
        // Actualizar selección visual
        document.querySelectorAll('.puesto-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        event.currentTarget.classList.add('selected');
        
        // Cargar detalles del puesto
        const response = await APIClient.get(`/coordinador-municipal/puesto/${puestoId}`);
        
        if (response && response.success && response.data) {
            puestoSeleccionado = response.data;
            renderDetallePuesto(response.data);
            document.getElementById('btn-comparar').disabled = false;
        }
    } catch (error) {
        console.error('[Municipal] Error cargando detalle de puesto:', error);
        Utils.showError('Error al cargar detalles del puesto');
    }
}

function seleccionarPuestoPorId(puestoId) {
    const puestoElement = document.querySelector(`[onclick="seleccionarPuesto(${puestoId})"]`);
    if (puestoElement) {
        puestoElement.click();
        puestoElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function renderDetallePuesto(puesto) {
    const container = document.getElementById('detalle-puesto');
    
    const coordinadorInfo = puesto.coordinador ? `
        <div class="mb-3">
            <h6 class="text-muted mb-2">
                <i class="bi bi-person"></i> Coordinador
            </h6>
            <p class="mb-1"><strong>${puesto.coordinador.nombre}</strong></p>
            <small class="text-muted">
                Último acceso: ${puesto.coordinador.ultimo_acceso ? 
                    new Date(puesto.coordinador.ultimo_acceso).toLocaleString('es-CO') : 
                    'Nunca'
                }
            </small>
        </div>
    ` : `
        <div class="mb-3">
            <div class="alert alert-warning">
                <i class="bi bi-exclamation-triangle"></i> Sin coordinador asignado
            </div>
        </div>
    `;
    
    container.innerHTML = `
        <div class="mb-3">
            <h6 class="text-primary">${puesto.puesto.nombre}</h6>
            <p class="text-muted mb-1">Código: ${puesto.puesto.codigo}</p>
            <p class="text-muted mb-1">Zona: ${puesto.puesto.zona_codigo}</p>
            <p class="text-muted">Total Mesas: ${puesto.puesto.total_mesas}</p>
        </div>
        
        ${coordinadorInfo}
        
        <div class="mb-3">
            <h6 class="text-muted mb-2">
                <i class="bi bi-bar-chart"></i> Estadísticas
            </h6>
            <div class="row text-center">
                <div class="col-6 mb-2">
                    <div class="border rounded p-2">
                        <strong class="text-success d-block">${puesto.estadisticas.formularios_validados}</strong>
                        <small class="text-muted">Validados</small>
                    </div>
                </div>
                <div class="col-6 mb-2">
                    <div class="border rounded p-2">
                        <strong class="text-warning d-block">${puesto.estadisticas.formularios_pendientes}</strong>
                        <small class="text-muted">Pendientes</small>
                    </div>
                </div>
                <div class="col-6 mb-2">
                    <div class="border rounded p-2">
                        <strong class="text-danger d-block">${puesto.estadisticas.formularios_rechazados}</strong>
                        <small class="text-muted">Rechazados</small>
                    </div>
                </div>
                <div class="col-6 mb-2">
                    <div class="border rounded p-2">
                        <strong class="text-primary d-block">${puesto.estadisticas.porcentaje_avance.toFixed(1)}%</strong>
                        <small class="text-muted">Avance</small>
                    </div>
                </div>
            </div>
        </div>
        
        ${puesto.estadisticas.incidentes > 0 || puesto.estadisticas.delitos > 0 ? `
            <div class="mb-3">
                <h6 class="text-muted mb-2">
                    <i class="bi bi-exclamation-triangle"></i> Reportes
                </h6>
                <div class="row text-center">
                    <div class="col-6">
                        <div class="border rounded p-2">
                            <strong class="text-info d-block">${puesto.estadisticas.incidentes}</strong>
                            <small class="text-muted">Incidentes</small>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="border rounded p-2">
                            <strong class="text-danger d-block">${puesto.estadisticas.delitos}</strong>
                            <small class="text-muted">Delitos</small>
                        </div>
                    </div>
                </div>
            </div>
        ` : ''}
        
        <div class="mb-3">
            <h6 class="text-muted mb-2">
                <i class="bi bi-list"></i> Mesas (Muestra)
            </h6>
            <div style="max-height: 200px; overflow-y: auto;">
                ${puesto.mesas.map(mesa => `
                    <div class="d-flex justify-content-between align-items-center py-1 border-bottom">
                        <div>
                            <small><strong>${mesa.codigo}</strong></small>
                            <br>
                            <small class="text-muted">${mesa.votantes} votantes</small>
                        </div>
                        <span class="badge ${getEstadoBadge(mesa.estado).class}">
                            ${getEstadoBadge(mesa.estado).text}
                        </span>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="d-grid gap-2">
            <button class="btn btn-outline-primary btn-sm" onclick="enviarNotificacionPuesto(${puesto.puesto.id})">
                <i class="bi bi-bell"></i> Notificar Coordinador
            </button>
            <button class="btn btn-outline-info btn-sm" onclick="verDetalleCompleto(${puesto.puesto.id})">
                <i class="bi bi-eye"></i> Ver Detalle Completo
            </button>
        </div>
    `;
}

// ============================================================================
// FILTROS Y BÚSQUEDA
// ============================================================================

function filtrarPuestos() {
    const filtroEstado = document.getElementById('filtro-estado').value;
    const filtroZona = document.getElementById('filtro-zona').value;
    
    let puestosFiltrados = [...puestosData];
    
    if (filtroEstado) {
        puestosFiltrados = puestosFiltrados.filter(p => p.estado === filtroEstado);
    }
    
    if (filtroZona) {
        puestosFiltrados = puestosFiltrados.filter(p => p.zona_codigo === filtroZona);
    }
    
    // Actualizar datos temporalmente para renderizado
    const puestosOriginal = [...puestosData];
    puestosData = puestosFiltrados;
    renderPuestosTable();
    puestosData = puestosOriginal;
}

function buscarPuesto() {
    const termino = document.getElementById('buscar-puesto').value.toLowerCase();
    
    if (!termino) {
        renderPuestosTable();
        return;
    }
    
    const puestosFiltrados = puestosData.filter(p => 
        p.nombre.toLowerCase().includes(termino) ||
        p.codigo.toLowerCase().includes(termino) ||
        p.zona_codigo.toLowerCase().includes(termino)
    );
    
    // Actualizar datos temporalmente para renderizado
    const puestosOriginal = [...puestosData];
    puestosData = puestosFiltrados;
    renderPuestosTable();
    puestosData = puestosOriginal;
}

function updateFiltroZonas() {
    const select = document.getElementById('filtro-zona');
    const zonas = [...new Set(puestosData.map(p => p.zona_codigo))].sort();
    
    select.innerHTML = '<option value="">Todas las zonas</option>';
    zonas.forEach(zona => {
        select.innerHTML += `<option value="${zona}">Zona ${zona}</option>`;
    });
}

// ============================================================================
// GENERACIÓN DE E-24 MUNICIPAL
// ============================================================================

async function generarE24Municipal() {
    const modal = new bootstrap.Modal(document.getElementById('modalE24Municipal'));
    modal.show();
    
    // Validar requisitos
    await validarRequisitosE24();
}

async function validarRequisitosE24() {
    const container = document.getElementById('validacion-requisitos');
    
    try {
        const response = await APIClient.get('/coordinador-municipal/estadisticas');
        
        if (response && response.success && response.data) {
            const stats = response.data.resumen_general;
            const porcentajeCompletos = (stats.puestos_completos / stats.total_puestos * 100) || 0;
            
            const cumpleRequisitos = porcentajeCompletos >= 80 && stats.puestos_con_discrepancias === 0;
            
            container.innerHTML = `
                <div class="alert ${cumpleRequisitos ? 'alert-success' : 'alert-warning'}">
                    <div class="d-flex align-items-center mb-2">
                        <i class="bi bi-${cumpleRequisitos ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                        <strong>${cumpleRequisitos ? 'Requisitos Cumplidos' : 'Requisitos Pendientes'}</strong>
                    </div>
                    <ul class="mb-0">
                        <li class="${porcentajeCompletos >= 80 ? 'text-success' : 'text-warning'}">
                            Puestos completos: ${porcentajeCompletos.toFixed(1)}% (mín. 80%)
                        </li>
                        <li class="${stats.puestos_con_discrepancias === 0 ? 'text-success' : 'text-warning'}">
                            Discrepancias críticas: ${stats.puestos_con_discrepancias} (máx. 0)
                        </li>
                    </ul>
                </div>
            `;
            
            document.getElementById('btn-generar-e24').disabled = !cumpleRequisitos;
        }
    } catch (error) {
        console.error('[Municipal] Error validando requisitos:', error);
        container.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle"></i> Error al validar requisitos
            </div>
        `;
    }
}

async function confirmarGenerarE24() {
    const tipoEleccionId = document.getElementById('tipo-eleccion-e24').value;
    
    if (!tipoEleccionId) {
        Utils.showError('Debe seleccionar un tipo de elección');
        return;
    }
    
    try {
        Utils.showLoading('Generando E-24 Municipal...');
        
        const response = await APIClient.post('/coordinador-municipal/e24-municipal', {
            tipo_eleccion_id: parseInt(tipoEleccionId)
        });
        
        Utils.hideLoading();
        
        if (response && response.success) {
            Utils.showSuccess('E-24 Municipal generado exitosamente');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalE24Municipal'));
            modal.hide();
            
            // Actualizar datos
            await loadEstadisticas();
        } else {
            Utils.showError(response?.error || 'Error al generar E-24 Municipal');
        }
    } catch (error) {
        Utils.hideLoading();
        console.error('[Municipal] Error generando E-24:', error);
        Utils.showError('Error al generar E-24 Municipal');
    }
}

// ============================================================================
// COMPARACIÓN DE PUESTOS
// ============================================================================

async function abrirComparacion() {
    const modal = new bootstrap.Modal(document.getElementById('modalComparacion'));
    modal.show();
    
    // Cargar lista de puestos para comparación
    renderListaPuestosComparacion();
}

function renderListaPuestosComparacion() {
    const container = document.getElementById('lista-puestos-comparacion');
    
    let html = '';
    
    puestosData.forEach(puesto => {
        const isSelected = puestosSeleccionadosComparacion.includes(puesto.id);
        
        html += `
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" value="${puesto.id}" 
                       id="comp-${puesto.id}" ${isSelected ? 'checked' : ''}
                       onchange="togglePuestoComparacion(${puesto.id})">
                <label class="form-check-label" for="comp-${puesto.id}">
                    <strong>${puesto.nombre}</strong><br>
                    <small class="text-muted">
                        ${puesto.formularios_validados}/${puesto.total_mesas} mesas 
                        (${puesto.porcentaje_avance.toFixed(1)}%)
                    </small>
                </label>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function togglePuestoComparacion(puestoId) {
    const index = puestosSeleccionadosComparacion.indexOf(puestoId);
    
    if (index > -1) {
        puestosSeleccionadosComparacion.splice(index, 1);
    } else {
        if (puestosSeleccionadosComparacion.length >= 5) {
            Utils.showWarning('Máximo 5 puestos para comparar');
            document.getElementById(`comp-${puestoId}`).checked = false;
            return;
        }
        puestosSeleccionadosComparacion.push(puestoId);
    }
    
    document.getElementById('btn-ejecutar-comparacion').disabled = 
        puestosSeleccionadosComparacion.length < 2;
}

async function ejecutarComparacion() {
    if (puestosSeleccionadosComparacion.length < 2) {
        Utils.showError('Seleccione al menos 2 puestos para comparar');
        return;
    }
    
    try {
        const response = await APIClient.get('/coordinador-municipal/comparacion', {
            puesto_ids: puestosSeleccionadosComparacion.join(',')
        });
        
        if (response && response.success && response.data) {
            renderResultadoComparacion(response.data);
        }
    } catch (error) {
        console.error('[Municipal] Error en comparación:', error);
        Utils.showError('Error al comparar puestos');
    }
}

function renderResultadoComparacion(data) {
    const container = document.getElementById('resultado-comparacion');
    
    // Aquí se implementaría la visualización de la comparación
    // Por ahora, mostrar datos básicos
    container.innerHTML = `
        <div class="alert alert-info">
            <i class="bi bi-info-circle"></i>
            Comparación de ${data.puestos?.length || 0} puestos completada.
            <br>
            <small>Funcionalidad de visualización en desarrollo.</small>
        </div>
    `;
}

// ============================================================================
// NOTIFICACIONES
// ============================================================================

async function enviarNotificacionPuesto(puestoId) {
    // Implementar modal de notificación específica para un puesto
    Utils.showInfo('Funcionalidad de notificaciones en desarrollo');
}

// ============================================================================
// EXPORTACIÓN
// ============================================================================

async function exportarDatos() {
    try {
        Utils.showLoading('Generando exportación...');
        
        const response = await fetch('/api/coordinador-municipal/exportar?formato=csv', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        
        Utils.hideLoading();
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `consolidado_municipal_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            Utils.showSuccess('Datos exportados correctamente');
        } else {
            Utils.showError('Error al exportar datos');
        }
    } catch (error) {
        Utils.hideLoading();
        console.error('[Municipal] Error exportando:', error);
        Utils.showError('Error al exportar datos');
    }
}

// ============================================================================
// UTILIDADES
// ============================================================================

function getEstadoBadge(estado) {
    switch (estado) {
        case 'completo':
            return { class: 'bg-success', text: 'Completo' };
        case 'con_discrepancias':
            return { class: 'bg-danger', text: 'Con Discrepancias' };
        case 'incompleto':
            return { class: 'bg-warning', text: 'Incompleto' };
        case 'validado':
            return { class: 'bg-success', text: 'Validado' };
        case 'pendiente':
            return { class: 'bg-warning', text: 'Pendiente' };
        case 'rechazado':
            return { class: 'bg-danger', text: 'Rechazado' };
        case 'sin_reporte':
            return { class: 'bg-secondary', text: 'Sin Reporte' };
        default:
            return { class: 'bg-secondary', text: estado };
    }
}

function verDetalleCompleto(puestoId) {
    // Redirigir a vista detallada del puesto
    window.open(`/coordinador/puesto?puesto_id=${puestoId}`, '_blank');
}

async function logout() {
    try {
        await APIClient.logout();
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
    } finally {
        localStorage.clear();
        window.location.href = '/auth/login';
    }
}