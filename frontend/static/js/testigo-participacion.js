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
    
    // Calcular porcentaje al cambiar personas votadas (incremental)
    document.getElementById('personasVotadas').addEventListener('input', async function() {
        const personasVotadasHora = parseInt(this.value) || 0;
        const votantesRegistrados = mesa.total_votantes_registrados || 0;
        
        if (votantesRegistrados > 0 && personasVotadasHora >= 0) {
            // Obtener total acumulado actual
            let totalAcumuladoActual = 0;
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`/api/reporte-participacion/mesa/${mesa.id}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    const data = await response.json();
                    if (data.success && data.data.reportes) {
                        totalAcumuladoActual = data.data.reportes.reduce((sum, r) => sum + r.personas_votadas, 0);
                    }
                }
            } catch (error) {
                console.warn('Error obteniendo reportes previos:', error);
            }
            
            // Calcular nuevo total acumulado
            const nuevoTotalAcumulado = totalAcumuladoActual + personasVotadasHora;
            const porcentaje = (nuevoTotalAcumulado / votantesRegistrados * 100).toFixed(2);
            
            document.getElementById('infoVotantesRegistrados').textContent = votantesRegistrados;
            document.getElementById('infoPorcentaje').textContent = porcentaje + '%';
            
            // Mostrar información adicional
            const infoElement = document.getElementById('participacionInfo');
            infoElement.innerHTML = `
                <small>
                    <strong>Votantes Registrados:</strong> ${votantesRegistrados}<br>
                    <strong>Total Acumulado Previo:</strong> ${totalAcumuladoActual}<br>
                    <strong>Votarán en Esta Hora:</strong> ${personasVotadasHora}<br>
                    <strong>Nuevo Total Acumulado:</strong> ${nuevoTotalAcumulado}<br>
                    <strong>Porcentaje de Participación:</strong> ${porcentaje}%
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
    
    // Calcular totales acumulados para mostrar correctamente
    let totalAcumulado = 0;
    const reportesConAcumulado = reportes.map(reporte => {
        totalAcumulado += reporte.personas_votadas;
        return {
            ...reporte,
            total_acumulado: totalAcumulado
        };
    });
    
    // Mostrar tabla de reportes
    let html = `
        <div class="alert alert-info mb-3">
            <i class="bi bi-info-circle"></i>
            <strong>Datos Incrementales:</strong> Cada reporte muestra las personas que votaron en esa hora específica.
            El total acumulado se calcula sumando todos los incrementos.
        </div>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Hora</th>
                        <th>Votaron en la Hora</th>
                        <th>Total Acumulado</th>
                        <th>Participación</th>
                        <th>Observaciones</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    reportesConAcumulado.forEach(reporte => {
        const hora = new Date(reporte.hora_reporte);
        const horaFormateada = hora.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' });
        
        html += `
            <tr>
                <td><strong>${horaFormateada}</strong></td>
                <td>
                    <span class="badge bg-primary">${reporte.personas_votadas}</span>
                    <small class="text-muted d-block">incremental</small>
                </td>
                <td>
                    <strong>${reporte.total_acumulado}</strong>
                    <small class="text-muted d-block">total hasta ahora</small>
                </td>
                <td>
                    <span class="badge bg-info">${reporte.porcentaje_participacion}%</span>
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
    
    // Datos incrementales (por hora)
    const datosIncrementales = reportes.map(r => r.personas_votadas);
    
    // Datos acumulados
    let totalAcumulado = 0;
    const datosAcumulados = reportes.map(r => {
        totalAcumulado += r.personas_votadas;
        return totalAcumulado;
    });
    
    // Destruir gráfico anterior si existe
    if (window.participacionChart) {
        window.participacionChart.destroy();
    }
    
    // Crear nuevo gráfico con dos líneas
    window.participacionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Votaron por Hora (Incremental)',
                    data: datosIncrementales,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.1,
                    fill: false,
                    yAxisID: 'y'
                },
                {
                    label: 'Total Acumulado',
                    data: datosAcumulados,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1,
                    fill: true,
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
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            return label + ': ' + context.parsed.y + ' personas';
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
                        text: 'Personas por Hora'
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
                        text: 'Total Acumulado'
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
