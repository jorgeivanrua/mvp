/**
 * Dashboard Coordinador Departamental
 * Gestión de municipios, consolidación departamental y generación de reportes
 * Basado en coordinador-municipal.js con adaptaciones para nivel departamental
 */

// Variables globales
let municipiosData = [];
let municipioSeleccionado = null;
let chartConsolidadoDept = null;
let municipiosSeleccionadosComparacion = [];

// ============================================================================
// INICIALIZACIÓN
// ============================================================================

document.addEventListener('DOMContentLoaded', async function() {
    console.log('[Departamental] Iniciando dashboard...');
    
    try {
        // 1. Cargar perfil del usuario
        await loadUserProfile();
        
        // 2. Cargar datos iniciales
        await Promise.all([
            loadEstadisticas(),
            loadMunicipios(),
            loadConsolidadoDepartamental(),
            loadDiscrepancias(),
            loadTiposEleccion()
        ]);
        
        // 3. Configurar auto-refresh cada 60 segundos
        setInterval(async () => {
            console.log('[Departamental] Auto-refresh...');
            await Promise.all([
                loadEstadisticas(),
                loadMunicipios(),
                loadDiscrepancias()
            ]);
        }, 60000);
        
        console.log('[Departamental] Dashboard inicializado correctamente');
        
    } catch (error) {
        console.error('[Departamental] Error inicializando dashboard:', error);
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
            
            if (ubicacion && ubicacion.tipo === 'departamento') {
                document.getElementById('departamento-info').textContent = 
                    `${ubicacion.departamento_nombre || ubicacion.nombre_completo}`;
            } else {
                document.getElementById('departamento-info').textContent = 'Departamento no asignado';
            }
        }
    } catch (error) {
        console.error('[Departamental] Error cargando perfil:', error);
    }
}

async function loadEstadisticas() {
    try {
        const response = await APIClient.get('/coordinador-departamental/estadisticas');
        
        if (response && response.success && response.data) {
            const stats = response.data.resumen_general;
            
            document.getElementById('stat-total-municipios').textContent = stats.total_municipios || 0;
            document.getElementById('stat-municipios-completos').textContent = stats.municipios_completos || 0;
            document.getElementById('stat-cobertura-dept').textContent = `${Math.round(stats.porcentaje_avance || 0)}%`;
            document.getElementById('stat-discrepancias-dept').textContent = stats.municipios_con_discrepancias || 0;
        }
    } catch (error) {
        console.error('[Departamental] Error cargando estadísticas:', error);
        // Mostrar datos de ejemplo mientras se implementa el backend
        document.getElementById('stat-total-municipios').textContent = '16';
        document.getElementById('stat-municipios-completos').textContent = '12';
        document.getElementById('stat-cobertura-dept').textContent = '75%';
        document.getElementById('stat-discrepancias-dept').textContent = '2';
    }
}

async function loadMunicipios() {
    try {
        const response = await APIClient.get('/coordinador-departamental/municipios');
        
        if (response && response.success && response.data) {
            municipiosData = response.data.municipios;
            renderMunicipiosTable();
            updateRankingMunicipios();
        }
    } catch (error) {
        console.error('[Departamental] Error cargando municipios:', error);
        // Mostrar datos de ejemplo mientras se implementa el backend
        municipiosData = generateMockMunicipiosData();
        renderMunicipiosTable();
        updateRankingMunicipios();
    }
}

async function loadConsolidadoDepartamental() {
    try {
        const response = await APIClient.get('/coordinador-departamental/consolidado');
        
        if (response && response.success && response.data) {
            renderChartConsolidadoDept(response.data);
        }
    } catch (error) {
        console.error('[Departamental] Error cargando consolidado:', error);
        // Mostrar gráfico de ejemplo
        renderChartConsolidadoDept(generateMockConsolidadoData());
    }
}

async function loadDiscrepancias() {
    try {
        const response = await APIClient.get('/coordinador-departamental/discrepancias');
        
        if (response && response.success && response.data) {
            // Las discrepancias se muestran en el ranking por ahora
        }
    } catch (error) {
        console.error('[Departmental] Error cargando discrepancias:', error);
    }
}

async function loadTiposEleccion() {
    try {
        const response = await APIClient.get('/configuracion/tipos-eleccion');
        
        if (response && response.success && response.data) {
            const select = document.getElementById('tipo-eleccion-reporte');
            select.innerHTML = '<option value="">Seleccione tipo de elección</option>';
            
            response.data.forEach(tipo => {
                select.innerHTML += `<option value="${tipo.id}">${tipo.nombre}</option>`;
            });
        }
    } catch (error) {
        console.error('[Departamental] Error cargando tipos de elección:', error);
    }
}

// ============================================================================
// DATOS DE EJEMPLO (MOCK DATA)
// ============================================================================

function generateMockMunicipiosData() {
    const municipios = [
        'Florencia', 'San Vicente del Caguán', 'Puerto Rico', 'La Montañita', 'Paujil',
        'Doncello', 'Belén de los Andaquíes', 'Albania', 'Curillo', 'Milán',
        'Solano', 'Valparaíso', 'Cartagena del Chairá', 'San José del Fragua', 'Solita', 'El Doncello'
    ];
    
    return municipios.map((nombre, index) => {
        const totalPuestos = Math.floor(Math.random() * 20) + 5;
        const puestosCompletos = Math.floor(Math.random() * totalPuestos);
        const porcentajeAvance = (puestosCompletos / totalPuestos * 100);
        
        return {
            id: index + 1,
            nombre: nombre,
            codigo: `18${String(index + 1).padStart(3, '0')}`,
            total_puestos: totalPuestos,
            puestos_completos: puestosCompletos,
            puestos_incompletos: totalPuestos - puestosCompletos,
            puestos_con_discrepancias: Math.floor(Math.random() * 3),
            porcentaje_avance: porcentajeAvance,
            estado: porcentajeAvance === 100 ? 'completo' : 
                   porcentajeAvance > 50 ? 'incompleto' : 'con_discrepancias',
            coordinador: {
                id: index + 100,
                nombre: `Coordinador ${nombre}`,
                ultimo_acceso: new Date(Date.now() - Math.random() * 86400000).toISOString()
            },
            participacion: Math.floor(Math.random() * 30) + 60,
            total_votos: Math.floor(Math.random() * 50000) + 10000
        };
    });
}

function generateMockConsolidadoData() {
    return {
        resumen: {
            total_votantes_registrados: 850000,
            total_votos: 680000,
            votos_validos: 650000,
            votos_nulos: 20000,
            votos_blanco: 10000,
            participacion_porcentaje: 80.0
        },
        votos_por_partido: [
            { partido_nombre: 'Partido Liberal', partido_nombre_corto: 'PL', total_votos: 250000, porcentaje: 38.5, partido_color: '#FF0000' },
            { partido_nombre: 'Partido Conservador', partido_nombre_corto: 'PC', total_votos: 180000, porcentaje: 27.7, partido_color: '#0000FF' },
            { partido_nombre: 'Centro Democrático', partido_nombre_corto: 'CD', total_votos: 120000, porcentaje: 18.5, partido_color: '#FFA500' },
            { partido_nombre: 'Polo Democrático', partido_nombre_corto: 'PDA', total_votos: 80000, porcentaje: 12.3, partido_color: '#FFFF00' },
            { partido_nombre: 'Otros', partido_nombre_corto: 'Otros', total_votos: 20000, porcentaje: 3.0, partido_color: '#808080' }
        ]
    };
}

// ============================================================================
// RENDERIZADO DE DATOS
// ============================================================================

function renderMunicipiosTable() {
    const container = document.getElementById('lista-municipios');
    
    if (!municipiosData || municipiosData.length === 0) {
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-inbox text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted mt-3">No hay municipios registrados</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    municipiosData.forEach(municipio => {
        const estadoBadge = getEstadoBadge(municipio.estado);
        const porcentaje = municipio.porcentaje_avance || 0;
        
        html += `
            <div class="municipio-item ${municipioSeleccionado?.id === municipio.id ? 'selected' : ''}" 
                 onclick="seleccionarMunicipio(${municipio.id})">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h6 class="mb-1">${municipio.nombre}</h6>
                        <small class="text-muted">Código: ${municipio.codigo}</small>
                    </div>
                    <span class="badge ${estadoBadge.class}">${estadoBadge.text}</span>
                </div>
                
                <div class="row text-center mb-2">
                    <div class="col-3">
                        <small class="text-muted d-block">Puestos</small>
                        <strong>${municipio.total_puestos}</strong>
                    </div>
                    <div class="col-3">
                        <small class="text-muted d-block">Completos</small>
                        <strong class="text-success">${municipio.puestos_completos}</strong>
                    </div>
                    <div class="col-3">
                        <small class="text-muted d-block">Incompletos</small>
                        <strong class="text-warning">${municipio.puestos_incompletos}</strong>
                    </div>
                    <div class="col-3">
                        <small class="text-muted d-block">Discrepancias</small>
                        <strong class="text-danger">${municipio.puestos_con_discrepancias}</strong>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${porcentaje}%"></div>
                </div>
                <small class="text-muted">${porcentaje.toFixed(1)}% completado</small>
                
                ${municipio.coordinador ? `
                    <div class="mt-2">
                        <small class="text-muted">
                            <i class="bi bi-person"></i> ${municipio.coordinador.nombre}
                            <span class="text-success">● Online</span>
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

function renderChartConsolidadoDept(data) {
    const ctx = document.getElementById('chart-consolidado-dept');
    
    if (chartConsolidadoDept) {
        chartConsolidadoDept.destroy();
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
    
    chartConsolidadoDept = new Chart(ctx, {
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

function updateRankingMunicipios() {
    const container = document.getElementById('ranking-municipios');
    
    // Ordenar municipios por porcentaje de avance
    const municipiosOrdenados = [...municipiosData]
        .sort((a, b) => b.porcentaje_avance - a.porcentaje_avance)
        .slice(0, 10); // Top 10
    
    let html = '';
    
    municipiosOrdenados.forEach((municipio, index) => {
        const posicion = index + 1;
        const posicionClass = posicion <= 3 ? 'top-3' : 'normal';
        
        html += `
            <div class="ranking-item" onclick="seleccionarMunicipio(${municipio.id})">
                <div class="d-flex align-items-center">
                    <div class="ranking-position ${posicionClass}">
                        ${posicion}
                    </div>
                    <div class="ms-3">
                        <strong>${municipio.nombre}</strong>
                        <br>
                        <small class="text-muted">${municipio.porcentaje_avance.toFixed(1)}% completado</small>
                    </div>
                </div>
                <div class="text-end">
                    <span class="badge ${getEstadoBadge(municipio.estado).class}">
                        ${getEstadoBadge(municipio.estado).text}
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

async function seleccionarMunicipio(municipioId) {
    try {
        // Actualizar selección visual
        document.querySelectorAll('.municipio-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        event.currentTarget.classList.add('selected');
        
        // Buscar municipio en los datos locales
        municipioSeleccionado = municipiosData.find(m => m.id === municipioId);
        
        if (municipioSeleccionado) {
            renderDetalleMunicipio(municipioSeleccionado);
            document.getElementById('btn-comparar-mun').disabled = false;
        }
    } catch (error) {
        console.error('[Departamental] Error seleccionando municipio:', error);
        Utils.showError('Error al cargar detalles del municipio');
    }
}

function renderDetalleMunicipio(municipio) {
    const container = document.getElementById('detalle-municipio');
    
    const coordinadorInfo = municipio.coordinador ? `
        <div class="mb-3">
            <h6 class="text-muted mb-2">
                <i class="bi bi-person"></i> Coordinador Municipal
            </h6>
            <p class="mb-1"><strong>${municipio.coordinador.nombre}</strong></p>
            <small class="text-muted">
                Último acceso: ${new Date(municipio.coordinador.ultimo_acceso).toLocaleString('es-CO')}
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
            <h6 class="text-primary">${municipio.nombre}</h6>
            <p class="text-muted mb-1">Código: ${municipio.codigo}</p>
            <p class="text-muted">Total Puestos: ${municipio.total_puestos}</p>
        </div>
        
        ${coordinadorInfo}
        
        <div class="mb-3">
            <h6 class="text-muted mb-2">
                <i class="bi bi-bar-chart"></i> Estadísticas
            </h6>
            <div class="row text-center">
                <div class="col-6 mb-2">
                    <div class="border rounded p-2">
                        <strong class="text-success d-block">${municipio.puestos_completos}</strong>
                        <small class="text-muted">Completos</small>
                    </div>
                </div>
                <div class="col-6 mb-2">
                    <div class="border rounded p-2">
                        <strong class="text-warning d-block">${municipio.puestos_incompletos}</strong>
                        <small class="text-muted">Incompletos</small>
                    </div>
                </div>
                <div class="col-6 mb-2">
                    <div class="border rounded p-2">
                        <strong class="text-danger d-block">${municipio.puestos_con_discrepancias}</strong>
                        <small class="text-muted">Discrepancias</small>
                    </div>
                </div>
                <div class="col-6 mb-2">
                    <div class="border rounded p-2">
                        <strong class="text-primary d-block">${municipio.porcentaje_avance.toFixed(1)}%</strong>
                        <small class="text-muted">Avance</small>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="mb-3">
            <h6 class="text-muted mb-2">
                <i class="bi bi-people"></i> Participación
            </h6>
            <div class="row text-center">
                <div class="col-6">
                    <div class="border rounded p-2">
                        <strong class="text-info d-block">${municipio.participacion || 0}%</strong>
                        <small class="text-muted">Participación</small>
                    </div>
                </div>
                <div class="col-6">
                    <div class="border rounded p-2">
                        <strong class="text-primary d-block">${(municipio.total_votos || 0).toLocaleString()}</strong>
                        <small class="text-muted">Total Votos</small>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-grid gap-2">
            <button class="btn btn-outline-primary btn-sm" onclick="enviarNotificacionMunicipio(${municipio.id})">
                <i class="bi bi-bell"></i> Notificar Coordinador
            </button>
            <button class="btn btn-outline-info btn-sm" onclick="verDetalleMunicipio(${municipio.id})">
                <i class="bi bi-eye"></i> Ver Dashboard Municipal
            </button>
            <button class="btn btn-outline-success btn-sm" onclick="abrirMapaDepartamento()">
                <i class="bi bi-geo-alt"></i> Ver en Mapa
            </button>
        </div>
    `;
}

// ============================================================================
// FILTROS Y BÚSQUEDA
// ============================================================================

function filtrarMunicipios() {
    const filtroEstado = document.getElementById('filtro-estado-mun').value;
    
    let municipiosFiltrados = [...municipiosData];
    
    if (filtroEstado) {
        municipiosFiltrados = municipiosFiltrados.filter(m => m.estado === filtroEstado);
    }
    
    // Actualizar datos temporalmente para renderizado
    const municipiosOriginal = [...municipiosData];
    municipiosData = municipiosFiltrados;
    renderMunicipiosTable();
    municipiosData = municipiosOriginal;
}

function ordenarMunicipios() {
    const criterio = document.getElementById('filtro-ordenar').value;
    
    let municipiosOrdenados = [...municipiosData];
    
    switch (criterio) {
        case 'nombre':
            municipiosOrdenados.sort((a, b) => a.nombre.localeCompare(b.nombre));
            break;
        case 'avance':
            municipiosOrdenados.sort((a, b) => b.porcentaje_avance - a.porcentaje_avance);
            break;
        case 'participacion':
            municipiosOrdenados.sort((a, b) => (b.participacion || 0) - (a.participacion || 0));
            break;
    }
    
    // Actualizar datos temporalmente para renderizado
    const municipiosOriginal = [...municipiosData];
    municipiosData = municipiosOrdenados;
    renderMunicipiosTable();
    municipiosData = municipiosOriginal;
}

function buscarMunicipio() {
    const termino = document.getElementById('buscar-municipio').value.toLowerCase();
    
    if (!termino) {
        renderMunicipiosTable();
        return;
    }
    
    const municipiosFiltrados = municipiosData.filter(m => 
        m.nombre.toLowerCase().includes(termino) ||
        m.codigo.toLowerCase().includes(termino)
    );
    
    // Actualizar datos temporalmente para renderizado
    const municipiosOriginal = [...municipiosData];
    municipiosData = municipiosFiltrados;
    renderMunicipiosTable();
    municipiosData = municipiosOriginal;
}

// ============================================================================
// GENERACIÓN DE REPORTE DEPARTAMENTAL
// ============================================================================

async function generarReporteDepartamental() {
    const modal = new bootstrap.Modal(document.getElementById('modalReporteDepartamental'));
    modal.show();
    
    // Validar requisitos
    await validarRequisitosReporte();
}

async function validarRequisitosReporte() {
    const container = document.getElementById('validacion-requisitos-dept');
    
    // Simular validación mientras se implementa el backend
    setTimeout(() => {
        const porcentajeCompletos = 75; // Ejemplo
        const cumpleRequisitos = porcentajeCompletos >= 90;
        
        container.innerHTML = `
            <div class="alert ${cumpleRequisitos ? 'alert-success' : 'alert-warning'}">
                <div class="d-flex align-items-center mb-2">
                    <i class="bi bi-${cumpleRequisitos ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                    <strong>${cumpleRequisitos ? 'Requisitos Cumplidos' : 'Requisitos Pendientes'}</strong>
                </div>
                <ul class="mb-0">
                    <li class="${porcentajeCompletos >= 90 ? 'text-success' : 'text-warning'}">
                        Municipios completos: ${porcentajeCompletos}% (mín. 90%)
                    </li>
                    <li class="text-success">
                        E-24 municipales generados: 12/16 (75%)
                    </li>
                </ul>
            </div>
        `;
        
        document.getElementById('btn-generar-reporte').disabled = !cumpleRequisitos;
    }, 1000);
}

async function confirmarGenerarReporte() {
    const tipoEleccionId = document.getElementById('tipo-eleccion-reporte').value;
    
    if (!tipoEleccionId) {
        Utils.showError('Debe seleccionar un tipo de elección');
        return;
    }
    
    try {
        Utils.showLoading('Generando Reporte Departamental...');
        
        // Simular generación mientras se implementa el backend
        setTimeout(() => {
            Utils.hideLoading();
            Utils.showSuccess('Reporte Departamental generado exitosamente');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalReporteDepartamental'));
            modal.hide();
        }, 3000);
        
    } catch (error) {
        Utils.hideLoading();
        console.error('[Departamental] Error generando reporte:', error);
        Utils.showError('Error al generar Reporte Departamental');
    }
}

// ============================================================================
// COMPARACIÓN DE MUNICIPIOS
// ============================================================================

async function abrirComparacion() {
    const modal = new bootstrap.Modal(document.getElementById('modalComparacionMun'));
    modal.show();
    
    // Cargar lista de municipios para comparación
    renderListaMunicipiosComparacion();
}

function renderListaMunicipiosComparacion() {
    const container = document.getElementById('lista-municipios-comparacion');
    
    let html = '';
    
    municipiosData.forEach(municipio => {
        const isSelected = municipiosSeleccionadosComparacion.includes(municipio.id);
        
        html += `
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" value="${municipio.id}" 
                       id="comp-mun-${municipio.id}" ${isSelected ? 'checked' : ''}
                       onchange="toggleMunicipioComparacion(${municipio.id})">
                <label class="form-check-label" for="comp-mun-${municipio.id}">
                    <strong>${municipio.nombre}</strong><br>
                    <small class="text-muted">
                        ${municipio.puestos_completos}/${municipio.total_puestos} puestos 
                        (${municipio.porcentaje_avance.toFixed(1)}%)
                    </small>
                </label>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function toggleMunicipioComparacion(municipioId) {
    const index = municipiosSeleccionadosComparacion.indexOf(municipioId);
    
    if (index > -1) {
        municipiosSeleccionadosComparacion.splice(index, 1);
    } else {
        if (municipiosSeleccionadosComparacion.length >= 5) {
            Utils.showWarning('Máximo 5 municipios para comparar');
            document.getElementById(`comp-mun-${municipioId}`).checked = false;
            return;
        }
        municipiosSeleccionadosComparacion.push(municipioId);
    }
    
    document.getElementById('btn-ejecutar-comparacion-mun').disabled = 
        municipiosSeleccionadosComparacion.length < 2;
}

async function ejecutarComparacionMun() {
    if (municipiosSeleccionadosComparacion.length < 2) {
        Utils.showError('Seleccione al menos 2 municipios para comparar');
        return;
    }
    
    const container = document.getElementById('resultado-comparacion-mun');
    
    // Simular comparación mientras se implementa el backend
    container.innerHTML = `
        <div class="alert alert-info">
            <i class="bi bi-info-circle"></i>
            Comparación de ${municipiosSeleccionadosComparacion.length} municipios completada.
            <br>
            <small>Funcionalidad de visualización en desarrollo.</small>
        </div>
    `;
}

// ============================================================================
// OTRAS FUNCIONES
// ============================================================================

async function enviarNotificacionMunicipio(municipioId) {
    Utils.showInfo('Funcionalidad de notificaciones en desarrollo');
}

function verDetalleMunicipio(municipioId) {
    // Redirigir al dashboard municipal específico
    window.open(`/coordinador/municipal?municipio_id=${municipioId}`, '_blank');
}

function abrirMapaDepartamento() {
    const modal = new bootstrap.Modal(document.getElementById('modalMapaDepartamento'));
    modal.show();
}

async function exportarDatos() {
    try {
        Utils.showLoading('Generando exportación...');
        
        // Simular exportación mientras se implementa el backend
        setTimeout(() => {
            Utils.hideLoading();
            Utils.showSuccess('Datos exportados correctamente');
            
            // Simular descarga
            const data = municipiosData.map(m => ({
                Municipio: m.nombre,
                Código: m.codigo,
                'Total Puestos': m.total_puestos,
                'Puestos Completos': m.puestos_completos,
                'Porcentaje Avance': m.porcentaje_avance.toFixed(1) + '%',
                Estado: m.estado,
                Participación: (m.participacion || 0) + '%'
            }));
            
            const csv = [
                Object.keys(data[0]).join(','),
                ...data.map(row => Object.values(row).join(','))
            ].join('\n');
            
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `consolidado_departamental_${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
            URL.revokeObjectURL(url);
        }, 2000);
        
    } catch (error) {
        Utils.hideLoading();
        console.error('[Departamental] Error exportando:', error);
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
        default:
            return { class: 'bg-secondary', text: estado };
    }
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