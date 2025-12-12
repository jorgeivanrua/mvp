/**
 * Gestión de Reportes de Participación Horaria (E-11)
 */

/**
 * Obtener ventana de tiempo actual para reportes
 */
function obtenerVentanaTiempo() {
    const ahora = new Date();
    const hora = ahora.getHours();
    const minutos = ahora.getMinutes();
    
    // Determinar la hora del reporte (redondear a la hora en punto)
    let horaReporte = hora;
    
    // Si estamos en los primeros 30 minutos, es la ventana de esa hora
    // Si estamos después de los 30 minutos, ya pasó la ventana
    
    return {
        horaReporte: horaReporte,
        enVentana: minutos <= 30,
        minutosRestantes: minutos <= 30 ? 30 - minutos : 0,
        proximaVentana: minutos > 30 ? horaReporte + 1 : horaReporte
    };
}

/**
 * Formatear hora en formato 12 horas
 */
function formatearHora12(hora) {
    const ampm = hora >= 12 ? 'PM' : 'AM';
    const hora12 = hora % 12 || 12;
    return `${hora12}:00 ${ampm}`;
}

/**
 * Abrir modal para reportar participación
 */
function reportarParticipacion() {
    console.log('=== REPORTAR PARTICIPACIÓN ===');
    
    // Verificar que haya presencia verificada
    const verificada = localStorage.getItem('presenciaVerificada') === 'true';
    const mesaData = localStorage.getItem('mesaVerificadaData');
    
    if (!verificada || !mesaData) {
        Utils.showError('Debe verificar su presencia en una mesa primero');
        return;
    }
    
    const mesa = JSON.parse(mesaData);
    console.log('Mesa verificada:', mesa);
    
    // Verificar ventana de tiempo
    const ventana = obtenerVentanaTiempo();
    
    if (!ventana.enVentana) {
        const proximaHora = formatearHora12(ventana.proximaVentana);
        const proximaHoraFin = formatearHora12(ventana.proximaVentana);
        Utils.showWarning(
            `La ventana de tiempo para reportar ha cerrado.\n\n` +
            `Próxima ventana: ${proximaHora} - ${proximaHora.replace(':00', ':30')}`
        );
        return;
    }
    
    // Establecer hora del reporte (hora en punto)
    const ahora = new Date();
    const horaReporte = new Date(ahora);
    horaReporte.setMinutes(0, 0, 0);
    const horaLocal = new Date(horaReporte.getTime() - (horaReporte.getTimezoneOffset() * 60000));
    const horaFormateada = horaLocal.toISOString().slice(0, 16);
    document.getElementById('horaReporte').value = horaFormateada;
    
    // Mostrar información de ventana de tiempo
    const horaReporteStr = formatearHora12(ventana.horaReporte);
    const alertVentana = document.getElementById('alertVentanaTiempo');
    if (alertVentana) {
        alertVentana.innerHTML = `
            <i class="bi bi-clock"></i>
            <strong>Ventana de tiempo:</strong> ${horaReporteStr} - ${horaReporteStr.replace(':00', ':30')}<br>
            <small>Tiempo restante: ${ventana.minutosRestantes} minutos</small>
        `;
        alertVentana.classList.remove('d-none');
    }
    
    // Limpiar formulario
    document.getElementById('personasVotadas').value = '';
    document.getElementById('observacionesParticipacion').value = '';
    document.getElementById('participacionInfo').classList.add('d-none');
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('participacionModal'));
    modal.show();
    
    // Calcular información al cambiar personas votadas (reporte independiente)
    document.getElementById('personasVotadas').addEventListener('input', function() {
        const personasVotadasHora = parseInt(this.value) || 0;
        const votantesRegistrados = mesa.total_votantes_registrados || 0;
        
        if (votantesRegistrados > 0 && personasVotadasHora >= 0) {
            // Calcular porcentaje de flujo para esta hora
            const porcentajeFlujo = (personasVotadasHora / votantesRegistrados * 100).toFixed(2);
            
            document.getElementById('infoVotantesRegistrados').textContent = votantesRegistrados;
            document.getElementById('infoPorcentaje').textContent = porcentajeFlujo + '%';
            
            // Mostrar información del reporte independiente
            const infoElement = document.getElementById('participacionInfo');
            infoElement.innerHTML = `
                <small>
                    <strong>Votantes Registrados en la Mesa:</strong> ${votantesRegistrados}<br>
                    <strong>Personas que Votaron en Esta Hora:</strong> ${personasVotadasHora}<br>
                    <strong>Porcentaje de Flujo Horario:</strong> ${porcentajeFlujo}%<br>
                    <br>
                    <em>Este reporte es independiente. Los coordinadores verán la suma de todos los reportes por hora para obtener totales por puesto/zona/municipio.</em>
                </small>
            `;
            infoElement.classList.remove('d-none');
        } else {
            document.getElementById('participacionInfo').classList.add('d-none');
        }
    });
}

/**
 * Enviar reporte de participación a coordinadores
 */
async function enviarReporteParticipacion() {
    try {
        console.log('=== ENVIAR REPORTE PARTICIPACIÓN ===');
        
        // Verificar ventana de tiempo nuevamente
        const ventana = obtenerVentanaTiempo();
        if (!ventana.enVentana) {
            const proximaHora = formatearHora12(ventana.proximaVentana);
            Utils.showError(
                `La ventana de tiempo ha cerrado. ` +
                `Próxima ventana: ${proximaHora} - ${proximaHora.replace(':00', ':30')}`
            );
            return;
        }
        
        // Obtener datos del formulario
        const horaReporte = document.getElementById('horaReporte').value;
        const personasVotadas = parseInt(document.getElementById('personasVotadas').value);
        const observaciones = document.getElementById('observacionesParticipacion').value;
        
        // Validar
        if (!horaReporte || isNaN(personasVotadas)) {
            Utils.showError('Complete todos los campos requeridos');
            return;
        }
        
        if (personasVotadas < 0) {
            Utils.showError('El número de personas votadas no puede ser negativo');
            return;
        }
        
        // Obtener mesa
        const mesaData = localStorage.getItem('mesaVerificadaData');
        if (!mesaData) {
            Utils.showError('No se encontró información de la mesa');
            return;
        }
        
        const mesa = JSON.parse(mesaData);
        
        // Validar que no exceda votantes registrados
        if (mesa.total_votantes_registrados && personasVotadas > mesa.total_votantes_registrados) {
            const confirmar = confirm(
                `El número de personas votadas (${personasVotadas}) excede los votantes registrados (${mesa.total_votantes_registrados}).\n\n` +
                `¿Está seguro de que desea enviar este reporte?`
            );
            if (!confirmar) return;
        }
        
        // Construir datos
        const data = {
            mesa_id: mesa.id,
            hora_reporte: new Date(horaReporte).toISOString(),
            personas_votadas: personasVotadas,
            observaciones: observaciones
        };
        
        console.log('Datos a enviar:', data);
        
        // Enviar al servidor
        Utils.showInfo('Enviando reporte a coordinadores...');
        
        const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
        if (!token) {
            Utils.showError('No hay token de autenticación. Por favor, inicie sesión nuevamente.');
            return;
        }
        
        const response = await fetch('/api/reporte-participacion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            Utils.showSuccess('✅ Reporte enviado exitosamente a los coordinadores');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('participacionModal'));
            modal.hide();
            
            // Recargar reportes
            await cargarReportesParticipacion();
            
            // Actualizar estadísticas
            actualizarEstadisticasParticipacion();
        } else {
            throw new Error(result.error || 'Error al enviar reporte');
        }
        
    } catch (error) {
        console.error('Error enviando reporte:', error);
        Utils.showError('Error al enviar reporte: ' + error.message);
    }
}

/**
 * Actualizar estadísticas de participación en el dashboard
 */
function actualizarEstadisticasParticipacion() {
    // Esta función se puede expandir para mostrar estadísticas en tiempo real
    console.log('Actualizando estadísticas de participación...');
}

/**
 * Cargar reportes de participación
 */
async function cargarReportesParticipacion() {
    try {
        console.log('=== CARGAR REPORTES PARTICIPACIÓN ===');
        
        // Obtener mesa
        const mesaData = localStorage.getItem('mesaVerificadaData');
        if (!mesaData) {
            console.log('No hay mesa verificada');
            return;
        }
        
        const mesa = JSON.parse(mesaData);
        
        // Obtener reportes del servidor
        const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
        if (!token) {
            console.warn('No hay token de autenticación');
            return;
        }
        
        const response = await fetch(`/api/reporte-participacion/mesa/${mesa.id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            const data = result.data;
            console.log('Reportes cargados:', data);
            
            mostrarReportesParticipacion(data);
        } else {
            throw new Error(result.error || 'Error al cargar reportes');
        }
        
    } catch (error) {
        console.error('Error cargando reportes:', error);
        // No mostrar error al usuario, solo en consola
    }
}

/**
 * Mostrar reportes de participación
 */
function mostrarReportesParticipacion(data) {
    const container = document.getElementById('participacionLista');
    const reportes = data.reportes || [];
    
    if (reportes.length === 0) {
        container.innerHTML = `
            <div class="text-center py-4 text-muted">
                <i class="bi bi-people" style="font-size: 3rem;"></i>
                <p class="mt-2">No hay reportes de participación</p>
                <small>Reporte cada hora cuántas personas han votado</small>
            </div>
        `;
        return;
    }
    
    // Calcular total histórico para referencia
    let totalHistorico = 0;
    const reportesConHistorico = reportes.map(reporte => {
        totalHistorico += reporte.personas_votadas;
        return {
            ...reporte,
            total_historico_hasta_hora: totalHistorico
        };
    });
    
    // Mostrar tabla de reportes
    let html = `
        <div class="alert alert-success mb-3">
            <i class="bi bi-clock"></i>
            <strong>Reportes Independientes por Hora:</strong> Cada reporte es una "fotografía" del flujo en esa hora específica.
            Los coordinadores suman estos reportes por puesto/zona/municipio para ver el flujo total.
        </div>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Hora</th>
                        <th>Flujo en la Hora</th>
                        <th>Total Histórico</th>
                        <th>% Flujo Horario</th>
                        <th>Observaciones</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    reportesConHistorico.forEach(reporte => {
        const hora = new Date(reporte.hora_reporte);
        const horaFormateada = hora.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' });
        
        html += `
            <tr>
                <td><strong>${horaFormateada}</strong></td>
                <td>
                    <span class="badge bg-primary fs-6">${reporte.personas_votadas}</span>
                    <small class="text-muted d-block">personas en esta hora</small>
                </td>
                <td>
                    <span class="text-success fw-bold">${reporte.total_historico_hasta_hora}</span>
                    <small class="text-muted d-block">suma histórica</small>
                </td>
                <td>
                    <span class="badge bg-info">${reporte.porcentaje_participacion}%</span>
                    <small class="text-muted d-block">de la mesa</small>
                </td>
                <td><small>${reporte.observaciones || '-'}</small></td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Mostrar gráfico si hay datos
    if (reportes.length > 1) {
        mostrarGraficoParticipacion(reportes);
    }
}

/**
 * Mostrar gráfico de participación
 */
function mostrarGraficoParticipacion(reportes) {
    const graficoContainer = document.getElementById('participacionGrafico');
    graficoContainer.classList.remove('d-none');
    
    const canvas = document.getElementById('participacionChart');
    const ctx = canvas.getContext('2d');
    
    // Preparar datos
    const labels = reportes.map(r => {
        const hora = new Date(r.hora_reporte);
        return hora.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' });
    });
    
    // Datos de flujo por hora (reportes independientes)
    const datosFlujoHorario = reportes.map(r => r.personas_votadas);
    
    // Datos históricos (suma progresiva para referencia)
    let totalHistorico = 0;
    const datosHistoricos = reportes.map(r => {
        totalHistorico += r.personas_votadas;
        return totalHistorico;
    });
    
    // Destruir gráfico anterior si existe
    if (window.participacionChart) {
        window.participacionChart.destroy();
    }
    
    // Crear gráfico de barras para flujo horario + línea para histórico
    window.participacionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    type: 'bar',
                    label: 'Flujo por Hora (Independiente)',
                    data: datosFlujoHorario,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgb(255, 99, 132)',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    type: 'line',
                    label: 'Total Histórico (Referencia)',
                    data: datosHistoricos,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.1,
                    fill: false,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Flujo de Votación por Hora (Reportes Independientes)'
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            if (context.dataset.type === 'bar') {
                                return label + ': ' + context.parsed.y + ' personas votaron en esta hora';
                            } else {
                                return label + ': ' + context.parsed.y + ' personas en total hasta esta hora';
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Hora del Reporte'
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Flujo por Hora'
                    },
                    beginAtZero: true,
                    ticks: {
                        stepSize: 10
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Total Histórico'
                    },
                    beginAtZero: true,
                    grid: {
                        drawOnChartArea: false,
                    },
                    ticks: {
                        stepSize: 50
                    }
                }
            }
        }
    });
}

/**
 * Actualizar indicador de ventana de tiempo
 */
function actualizarIndicadorVentana() {
    const ventanaActualElement = document.getElementById('ventanaActual');
    const ventanaDetalleElement = document.getElementById('ventanaDetalle');
    const ventanaTiempoInfo = document.getElementById('ventanaTiempoInfo');
    
    if (!ventanaActualElement || !ventanaDetalleElement || !ventanaTiempoInfo) return;
    
    const ventana = obtenerVentanaTiempo();
    const horaReporteStr = formatearHora12(ventana.horaReporte);
    
    if (ventana.enVentana) {
        ventanaActualElement.textContent = `${horaReporteStr} - ${horaReporteStr.replace(':00', ':30')} (ABIERTA)`;
        ventanaDetalleElement.textContent = `Puede reportar ahora. Tiempo restante: ${ventana.minutosRestantes} minutos`;
        ventanaTiempoInfo.classList.remove('alert-danger');
        ventanaTiempoInfo.classList.add('alert-success');
    } else {
        const proximaHora = formatearHora12(ventana.proximaVentana);
        ventanaActualElement.textContent = `Ventana cerrada`;
        ventanaDetalleElement.textContent = `Próxima ventana: ${proximaHora} - ${proximaHora.replace(':00', ':30')}`;
        ventanaTiempoInfo.classList.remove('alert-success');
        ventanaTiempoInfo.classList.add('alert-danger');
    }
}

// Cargar reportes al iniciar y al cambiar a la pestaña de participación
document.addEventListener('DOMContentLoaded', function() {
    // Cargar reportes al iniciar (después de 2 segundos para dar tiempo a que cargue la mesa)
    setTimeout(() => {
        cargarReportesParticipacion();
    }, 2000);
    
    // También cargar al cambiar a la pestaña
    const participacionTab = document.getElementById('participacion-tab');
    if (participacionTab) {
        participacionTab.addEventListener('shown.bs.tab', function() {
            cargarReportesParticipacion();
        });
    }
    
    // Actualizar indicador de ventana cada minuto
    actualizarIndicadorVentana();
    setInterval(actualizarIndicadorVentana, 60000); // Cada 60 segundos
});
