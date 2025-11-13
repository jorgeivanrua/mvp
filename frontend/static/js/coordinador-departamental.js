/**
 * Dashboard del Coordinador Departamental
 */

let currentUser = null;
let departamento = null;
let municipiosData = [];
let consolidadoData = null;
let chartPartidos = null;

document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadMunicipios();
    
    // Cargar datos al cambiar de pestaña
    document.getElementById('consolidado-tab').addEventListener('shown.bs.tab', function() {
        loadConsolidado();
    });
    
    document.getElementById('discrepancias-tab').addEventListener('shown.bs.tab', function() {
        loadDiscrepancias();
    });
    
    document.getElementById('reportes-tab').addEventListener('shown.bs.tab', function() {
        loadReportes();
        validarRequisitosReporte();
    });
});

async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        if (response.success) {
            currentUser = response.data.user;
            departamento = response.data.ubicacion;
            
            if (departamento) {
                document.getElementById('departamentoNombre').textContent = 
                    `Departamento: ${departamento.departamento_nombre || departamento.nombre_completo}`;
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        Utils.showError('Error al cargar perfil');
    }
}

async function loadMunicipios(filtro = null) {
    try {
        const params = {};
        if (filtro) {
            params.estado = filtro;
        }
        
        const response = await APIClient.get('/coordinador/departamental/api/municipios', params);
        
        if (response.success) {
            municipiosData = response.data.municipios || [];
            const estadisticas = response.data.estadisticas || {};
            
            // Actualizar estadísticas
            document.getElementById('totalMunicipios').textContent = estadisticas.total_municipios || 0;
            document.getElementById('municipiosCompletos').textContent = estadisticas.municipios_completos || 0;
            document.getElementById('municipiosIncompletos').textContent = estadisticas.municipios_incompletos || 0;
            document.getElementById('municipiosConDiscrepancias').textContent = estadisticas.municipios_con_discrepancias || 0;
            
            // Actualizar tabla
            updateMunicipiosTable(municipiosData);
        }
    } catch (error) {
        console.error('Error loading municipios:', error);
        Utils.showError('Error al cargar municipios');
    }
}

function updateMunicipiosTable(municipios) {
    const tbody = document.querySelector('#municipiosTable tbody');
    tbody.innerHTML = '';
    
    if (municipios.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4">
                    <p class="text-muted">No hay municipios</p>
                </td>
            </tr>
        `;
        return;
    }
    
    municipios.forEach(municipio => {
        const row = document.createElement('tr');
        
        const estadoBadge = getEstadoBadge(municipio.estado);
        const porcentaje = municipio.porcentaje_avance || 0;
        const progressColor = porcentaje >= 90 ? 'success' : porcentaje >= 50 ? 'warning' : 'danger';
        
        row.innerHTML = `
            <td>
                <strong>${municipio.nombre}</strong>
                <br><small class="text-muted">Código: ${municipio.codigo}</small>
            </td>
            <td>
                ${municipio.coordinador.nombre}
                <br><small class="text-muted">${municipio.coordinador.telefono || 'Sin teléfono'}</small>
            </td>
            <td>
                <span class="badge bg-primary">${municipio.puestos_completos}/${municipio.total_puestos}</span>
            </td>
            <td>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar bg-${progressColor}" role="progressbar" 
                         style="width: ${porcentaje}%;" 
                         aria-valuenow="${porcentaje}" aria-valuemin="0" aria-valuemax="100">
                        ${porcentaje.toFixed(1)}%
                    </div>
                </div>
            </td>
            <td>${estadoBadge}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="verDetalleMunicipio(${municipio.id})">
                    <i class="bi bi-eye"></i> Ver
                </button>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

function getEstadoBadge(estado) {
    const badges = {
        'completo': '<span class="badge bg-success">Completo</span>',
        'incompleto': '<span class="badge bg-warning">Incompleto</span>',
        'con_discrepancias': '<span class="badge bg-danger">Con Discrepancias</span>'
    };
    return badges[estado] || '<span class="badge bg-secondary">Desconocido</span>';
}

function filtrarMunicipios() {
    const filtro = document.getElementById('filtroEstado').value;
    loadMunicipios(filtro || null);
}

function actualizarDatos() {
    loadMunicipios();
    Utils.showSuccess('Datos actualizados');
}

async function verDetalleMunicipio(municipioId) {
    try {
        const response = await APIClient.get(`/coordinador/departamental/api/municipio/${municipioId}`);
        
        if (response.success) {
            const data = response.data;
            
            let html = `
                <h5>${data.municipio.nombre}</h5>
                <hr>
                <h6>Coordinador Municipal</h6>
                <p>
                    <strong>${data.coordinador.nombre}</strong><br>
                    ${data.coordinador.email}<br>
                    ${data.coordinador.telefono || 'Sin teléfono'}
                </p>
                <hr>
                <h6>Estadísticas</h6>
                <div class="row">
                    <div class="col-md-4">
                        <p><strong>Total Puestos:</strong> ${data.estadisticas.total_puestos || 0}</p>
                    </div>
                    <div class="col-md-4">
                        <p><strong>Completos:</strong> ${data.estadisticas.puestos_completos || 0}</p>
                    </div>
                    <div class="col-md-4">
                        <p><strong>Cobertura:</strong> ${(data.estadisticas.cobertura_porcentaje || 0).toFixed(1)}%</p>
                    </div>
                </div>
            `;
            
            if (data.consolidado) {
                html += `
                    <hr>
                    <h6>Consolidado</h6>
                    <p><strong>Total Votos:</strong> ${Utils.formatNumber(data.consolidado.resumen.total_votos)}</p>
                    <p><strong>Participación:</strong> ${data.consolidado.resumen.participacion_porcentaje.toFixed(2)}%</p>
                `;
            }
            
            document.getElementById('municipioDetalle').innerHTML = html;
            new bootstrap.Modal(document.getElementById('municipioModal')).show();
        }
    } catch (error) {
        console.error('Error loading municipio detail:', error);
        Utils.showError('Error al cargar detalle del municipio');
    }
}

async function loadConsolidado() {
    try {
        const response = await APIClient.get('/coordinador/departamental/api/consolidado');
        
        if (response.success) {
            consolidadoData = response.data;
            
            // Actualizar resumen
            const resumen = consolidadoData.resumen;
            const departamentoInfo = consolidadoData.departamento;
            
            document.getElementById('resumenDepartamental').innerHTML = `
                <p><strong>Total Municipios:</strong> ${departamentoInfo.total_municipios}</p>
                <p><strong>Total Puestos:</strong> ${Utils.formatNumber(departamentoInfo.total_puestos)}</p>
                <p><strong>Total Mesas:</strong> ${Utils.formatNumber(departamentoInfo.total_mesas)}</p>
                <hr>
                <p><strong>Votantes Registrados:</strong> ${Utils.formatNumber(resumen.total_votantes_registrados)}</p>
                <p><strong>Total Votos:</strong> ${Utils.formatNumber(resumen.total_votos)}</p>
                <p><strong>Participación:</strong> ${resumen.participacion_porcentaje.toFixed(2)}%</p>
                <hr>
                <p><strong>Votos Válidos:</strong> ${Utils.formatNumber(resumen.votos_validos)}</p>
                <p><strong>Votos Nulos:</strong> ${Utils.formatNumber(resumen.votos_nulos)}</p>
                <p><strong>Votos en Blanco:</strong> ${Utils.formatNumber(resumen.votos_blanco)}</p>
            `;
            
            // Actualizar gráfico
            updateChartPartidos(consolidadoData.votos_por_partido);
        }
    } catch (error) {
        console.error('Error loading consolidado:', error);
        Utils.showError('Error al cargar consolidado');
    }
}

function updateChartPartidos(votosPartidos) {
    const ctx = document.getElementById('chartPartidos');
    
    if (chartPartidos) {
        chartPartidos.destroy();
    }
    
    const labels = votosPartidos.map(vp => vp.partido_nombre_corto);
    const data = votosPartidos.map(vp => vp.total_votos);
    const colors = votosPartidos.map(vp => vp.partido_color || '#6c757d');
    
    chartPartidos = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Votos',
                data: data,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return Utils.formatNumber(context.parsed.y) + ' votos';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return Utils.formatNumber(value);
                        }
                    }
                }
            }
        }
    });
}

async function loadDiscrepancias() {
    try {
        const response = await APIClient.get('/coordinador/departamental/api/discrepancias');
        
        if (response.success) {
            const discrepancias = response.data.discrepancias || [];
            
            if (discrepancias.length === 0) {
                document.getElementById('discrepanciasLista').innerHTML = `
                    <div class="alert alert-success">
                        <i class="bi bi-check-circle"></i> No se detectaron discrepancias
                    </div>
                `;
                return;
            }
            
            let html = '';
            discrepancias.forEach(disc => {
                const severidadClass = getSeveridadClass(disc.severidad);
                const severidadIcon = getSeveridadIcon(disc.severidad);
                
                html += `
                    <div class="alert alert-${severidadClass} mb-2">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h6 class="mb-1">
                                    ${severidadIcon} ${disc.tipo_discrepancia.replace(/_/g, ' ').toUpperCase()}
                                </h6>
                                <p class="mb-1">${disc.descripcion}</p>
                                ${disc.municipio_nombre ? `<small><strong>Municipio:</strong> ${disc.municipio_nombre}</small>` : ''}
                            </div>
                            <span class="badge bg-${severidadClass}">${disc.severidad}</span>
                        </div>
                    </div>
                `;
            });
            
            document.getElementById('discrepanciasLista').innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading discrepancias:', error);
        Utils.showError('Error al cargar discrepancias');
    }
}

function getSeveridadClass(severidad) {
    const classes = {
        'critica': 'danger',
        'alta': 'warning',
        'media': 'info',
        'baja': 'secondary'
    };
    return classes[severidad] || 'secondary';
}

function getSeveridadIcon(severidad) {
    const icons = {
        'critica': '<i class="bi bi-exclamation-triangle-fill"></i>',
        'alta': '<i class="bi bi-exclamation-triangle"></i>',
        'media': '<i class="bi bi-info-circle"></i>',
        'baja': '<i class="bi bi-info-circle-fill"></i>'
    };
    return icons[severidad] || '<i class="bi bi-info-circle"></i>';
}

async function loadReportes() {
    try {
        const response = await APIClient.get('/coordinador/departamental/api/reportes');
        
        if (response.success) {
            const reportes = response.data.reportes || [];
            
            if (reportes.length === 0) {
                document.getElementById('reportesLista').innerHTML = `
                    <p class="text-muted">No hay reportes generados</p>
                `;
                return;
            }
            
            let html = '<div class="list-group">';
            reportes.forEach(reporte => {
                html += `
                    <div class="list-group-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-1">Reporte Departamental v${reporte.version}</h6>
                                <small class="text-muted">
                                    Generado el ${Utils.formatDate(reporte.created_at)} por ${reporte.coordinador_nombre}
                                </small>
                                <br>
                                <small>
                                    ${reporte.municipios_incluidos}/${reporte.total_municipios} municipios | 
                                    ${Utils.formatNumber(reporte.total_votos)} votos
                                </small>
                            </div>
                            <a href="${reporte.pdf_url}" class="btn btn-sm btn-primary" target="_blank">
                                <i class="bi bi-download"></i> Descargar PDF
                            </a>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            
            document.getElementById('reportesLista').innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading reportes:', error);
        Utils.showError('Error al cargar reportes');
    }
}

async function validarRequisitosReporte() {
    try {
        const response = await APIClient.get('/coordinador/departamental/api/reporte/validar');
        
        if (response.success) {
            const puedeGenerar = response.data.puede_generar;
            const errores = response.data.errores || [];
            
            let html = '';
            if (puedeGenerar) {
                html = `
                    <div class="alert alert-success">
                        <i class="bi bi-check-circle"></i> Se cumplen todos los requisitos para generar el reporte
                    </div>
                `;
            } else {
                html = `
                    <div class="alert alert-warning">
                        <h6>Requisitos pendientes:</h6>
                        <ul class="mb-0">
                            ${errores.map(error => `<li>${error}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            document.getElementById('requisitosReporte').innerHTML = html;
        }
    } catch (error) {
        console.error('Error validating requisitos:', error);
    }
}

async function generarReporte() {
    if (!confirm('¿Está seguro de generar el reporte departamental?')) {
        return;
    }
    
    try {
        // Por ahora usar tipo_eleccion_id = 1 (debería ser seleccionable)
        const response = await APIClient.post('/coordinador/departamental/api/reporte/generar', {
            tipo_eleccion_id: 1
        });
        
        if (response.success) {
            Utils.showSuccess('Reporte generado exitosamente');
            loadReportes();
        } else {
            Utils.showError(response.error || 'Error al generar reporte');
        }
    } catch (error) {
        console.error('Error generating reporte:', error);
        Utils.showError('Error al generar reporte: ' + error.message);
    }
}

// Función global para logout
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
