/**
 * Modal de Visualización de Formularios E-14
 * Maneja la visualización detallada de formularios enviados
 */

class ModalVisualizacion {
    constructor() {
        this.formularioActual = null;
        this.modal = null;
    }

    /**
     * Inicializar modal
     */
    init() {
        const modalElement = document.getElementById('verFormularioModal');
        if (modalElement) {
            this.modal = new bootstrap.Modal(modalElement);
        }
    }

    /**
     * Mostrar formulario en modal
     */
    mostrar(formulario) {
        if (!formulario) {
            console.error('[ModalVisualizacion] No se proporcionó formulario');
            return;
        }

        this.formularioActual = formulario;
        
        // Llenar datos del modal
        this.llenarInformacionBasica();
        this.llenarDatosVotacion();
        this.mostrarVotosPorPartido();
        this.mostrarImagenFormulario();
        this.mostrarEstadoDetallado();

        // Mostrar modal
        if (this.modal) {
            this.modal.show();
        }
    }

    /**
     * Llenar información básica
     */
    llenarInformacionBasica() {
        const formulario = this.formularioActual;
        
        // Mesa
        this.setElementText('verMesa', `Mesa ${formulario.mesa_codigo || 'N/A'}`);
        
        // Estado con badge
        const estadoElement = document.getElementById('verEstado');
        if (estadoElement) {
            const estadoLabel = this.getEstadoLabel(formulario.estado);
            const estadoColor = this.getEstadoColor(formulario.estado);
            estadoElement.innerHTML = `<span class="badge bg-${estadoColor}">${estadoLabel}</span>`;
        }

        // Observaciones
        this.setElementText('verObservaciones', formulario.observaciones || 'Sin observaciones');
    }

    /**
     * Llenar datos de votación
     */
    llenarDatosVotacion() {
        const formulario = this.formularioActual;
        
        const campos = {
            'verVotantesRegistrados': formulario.total_votantes_registrados || 0,
            'verTotalVotos': formulario.total_votos || 0,
            'verVotosValidos': formulario.votos_validos || 0,
            'verVotosNulos': formulario.votos_nulos || 0,
            'verVotosBlanco': formulario.votos_blanco || 0,
            'verTarjetasNoMarcadas': formulario.tarjetas_no_marcadas || 0
        };

        Object.entries(campos).forEach(([id, valor]) => {
            this.setElementText(id, Utils.formatNumber(valor));
        });
    }

    /**
     * Mostrar votos por partido
     */
    mostrarVotosPorPartido() {
        const container = document.getElementById('verVotosPorPartido');
        if (!container) return;

        const votosPartidos = this.formularioActual.votos_partidos || [];

        if (votosPartidos.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay votos registrados</p>';
            return;
        }

        const totalVotos = votosPartidos.reduce((sum, vp) => sum + (vp.votos || 0), 0);
        
        const html = votosPartidos.map(vp => {
            const porcentaje = totalVotos > 0 ? ((vp.votos || 0) / totalVotos * 100).toFixed(1) : 0;
            
            return `
                <div class="d-flex justify-content-between align-items-center mb-2 p-2 border rounded">
                    <div>
                        <span class="badge me-2" style="background-color: ${vp.partido_color || '#6c757d'};">
                            ${vp.partido_sigla || 'N/A'}
                        </span>
                        <strong>${vp.partido_nombre || 'Desconocido'}</strong>
                    </div>
                    <div class="text-end">
                        <span class="fw-bold">${Utils.formatNumber(vp.votos || 0)}</span>
                        <small class="text-muted d-block">${porcentaje}%</small>
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    /**
     * Mostrar imagen del formulario
     */
    mostrarImagenFormulario() {
        const container = document.getElementById('verImagenFormulario');
        if (!container) return;

        const formulario = this.formularioActual;

        if (formulario.imagen_url) {
            container.innerHTML = `
                <div class="text-center">
                    <img src="${formulario.imagen_url}" 
                         class="img-fluid border rounded shadow-sm" 
                         style="max-height: 400px; cursor: pointer;" 
                         onclick="window.open('${formulario.imagen_url}', '_blank')"
                         alt="Formulario E-14"
                         loading="lazy">
                    <p class="text-muted mt-2 mb-0">
                        <small><i class="bi bi-zoom-in"></i> Click para ver en tamaño completo</small>
                    </p>
                </div>
            `;
        } else {
            container.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <i class="bi bi-image" style="font-size: 3rem;"></i>
                    <p class="mt-2">No hay imagen disponible</p>
                </div>
            `;
        }
    }

    /**
     * Mostrar estado detallado
     */
    mostrarEstadoDetallado() {
        const container = document.getElementById('verEstadoDetalle');
        if (!container) return;

        const formulario = this.formularioActual;
        let html = '';

        switch (formulario.estado) {
            case 'pendiente':
                html = this.crearAlertaPendiente(formulario);
                break;
            case 'validado':
                html = this.crearAlertaValidado(formulario);
                break;
            case 'rechazado':
                html = this.crearAlertaRechazado(formulario);
                break;
            default:
                html = this.crearAlertaGeneral(formulario);
        }

        container.innerHTML = html;
    }

    /**
     * Crear alerta para formulario pendiente
     */
    crearAlertaPendiente(formulario) {
        return `
            <div class="alert alert-info">
                <div class="d-flex align-items-center">
                    <i class="bi bi-clock-history fs-4 me-3"></i>
                    <div>
                        <h6 class="alert-heading mb-1">Formulario Enviado</h6>
                        <p class="mb-1">Su formulario ha sido enviado y está pendiente de revisión por el coordinador de puesto.</p>
                        <small class="text-muted">
                            <i class="bi bi-calendar"></i> Enviado el: ${Utils.formatDate(formulario.created_at)}
                        </small>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Crear alerta para formulario validado
     */
    crearAlertaValidado(formulario) {
        return `
            <div class="alert alert-success">
                <div class="d-flex align-items-center">
                    <i class="bi bi-check-circle-fill fs-4 me-3"></i>
                    <div>
                        <h6 class="alert-heading mb-1">Formulario Validado</h6>
                        <p class="mb-1">Su formulario ha sido validado por el coordinador de puesto.</p>
                        <small class="text-muted">
                            <i class="bi bi-calendar-check"></i> Validado el: ${Utils.formatDate(formulario.validado_at)}
                        </small>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Crear alerta para formulario rechazado
     */
    crearAlertaRechazado(formulario) {
        return `
            <div class="alert alert-danger">
                <div class="d-flex align-items-start">
                    <i class="bi bi-x-circle-fill fs-4 me-3 mt-1"></i>
                    <div class="flex-grow-1">
                        <h6 class="alert-heading mb-2">Formulario Rechazado</h6>
                        <div class="mb-2">
                            <strong>Motivo:</strong> ${formulario.motivo_rechazo || 'No especificado'}
                        </div>
                        <small class="text-muted d-block mb-3">
                            <i class="bi bi-calendar-x"></i> Rechazado el: ${Utils.formatDate(formulario.validado_at)}
                        </small>
                        <button class="btn btn-warning btn-sm" 
                                onclick="window.modalVisualizacion.editarFormularioRechazado()">
                            <i class="bi bi-pencil"></i> Corregir y Reenviar
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Crear alerta general
     */
    crearAlertaGeneral(formulario) {
        return `
            <div class="alert alert-secondary">
                <div class="d-flex align-items-center">
                    <i class="bi bi-info-circle fs-4 me-3"></i>
                    <div>
                        <h6 class="alert-heading mb-1">Estado: ${this.getEstadoLabel(formulario.estado)}</h6>
                        <small class="text-muted">
                            <i class="bi bi-calendar"></i> Creado el: ${Utils.formatDate(formulario.created_at)}
                        </small>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Editar formulario rechazado
     */
    editarFormularioRechazado() {
        if (!this.formularioActual) return;

        // Cerrar modal
        if (this.modal) {
            this.modal.hide();
        }

        // Abrir formulario para edición
        if (window.formulariosManager) {
            window.formulariosManager.editarFormulario(this.formularioActual.id);
        }
    }

    /**
     * Cerrar modal
     */
    cerrar() {
        if (this.modal) {
            this.modal.hide();
        }
        this.formularioActual = null;
    }

    /**
     * Establecer texto de elemento
     */
    setElementText(id, texto) {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.textContent = texto;
        }
    }

    /**
     * Obtener etiqueta de estado
     */
    getEstadoLabel(estado) {
        const etiquetas = {
            'pendiente': '📤 Enviado - Pendiente Revisión',
            'validado': '✅ Validado',
            'rechazado': '❌ Rechazado',
            'borrador': '📝 Borrador',
            'local': '💾 Guardado Localmente'
        };
        return etiquetas[estado] || estado;
    }

    /**
     * Obtener color de estado
     */
    getEstadoColor(estado) {
        const colores = {
            'pendiente': 'info',
            'validado': 'success',
            'rechazado': 'danger',
            'borrador': 'secondary',
            'local': 'warning'
        };
        return colores[estado] || 'secondary';
    }
}

// Exportar para uso global
window.ModalVisualizacion = ModalVisualizacion;