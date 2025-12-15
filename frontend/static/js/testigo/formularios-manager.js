/**
 * Gestor de Formularios E-14 para Testigos
 * Maneja la visualización, edición y gestión de formularios
 */

class FormulariosManager {
    constructor() {
        this.formularios = [];
        this.formularioActual = null;
    }

    /**
     * Cargar formularios del testigo
     */
    async cargarFormularios(params = {}) {
        try {
            console.log('[FormulariosManager] Cargando formularios...');
            
            const response = await APIClient.getFormulariosE14(params);
            
            if (response.success) {
                this.formularios = response.data.formularios || response.data || [];
                console.log('[FormulariosManager] Formularios cargados:', this.formularios.length);
                
                this.renderizarTabla();
                this.renderizarCardsMobile();
                
                return this.formularios;
            } else {
                throw new Error(response.error || 'Error al cargar formularios');
            }
        } catch (error) {
            console.error('[FormulariosManager] Error:', error);
            this.mostrarErrorEnTabla(error.message);
            throw error;
        }
    }

    /**
     * Renderizar tabla de formularios (desktop)
     */
    renderizarTabla() {
        const tbody = document.querySelector('#formsTable tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (this.formularios.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-4">
                        <p class="text-muted">No hay formularios registrados</p>
                    </td>
                </tr>
            `;
            return;
        }

        this.formularios.forEach(formulario => {
            const row = this.crearFilaFormulario(formulario);
            tbody.appendChild(row);
        });
    }

    /**
     * Crear fila de formulario para tabla
     */
    crearFilaFormulario(formulario) {
        const row = document.createElement('tr');
        const estadoLabel = this.obtenerEtiquetaEstado(formulario.estado);
        const puedeEditar = this.puedeEditarFormulario(formulario);

        // Hacer fila clickeable si puede editar
        if (puedeEditar) {
            row.style.cursor = 'pointer';
            row.onclick = () => this.editarFormulario(formulario);
            row.onmouseover = () => row.style.backgroundColor = '#f8f9fa';
            row.onmouseout = () => row.style.backgroundColor = '';
        }

        row.innerHTML = `
            <td>Mesa ${formulario.mesa_codigo || 'N/A'}</td>
            <td><span class="badge bg-secondary">${formulario.tipo_eleccion_nombre || 'N/A'}</span></td>
            <td><span class="badge bg-${this.obtenerColorEstado(formulario.estado)}">${estadoLabel}</span></td>
            <td>${Utils.formatNumber(formulario.total_votos)}</td>
            <td>${Utils.formatDate(formulario.created_at)}</td>
            <td>${this.generarBotonesAccion(formulario)}</td>
        `;

        return row;
    }

    /**
     * Renderizar cards para móvil
     */
    renderizarCardsMobile() {
        const container = document.getElementById('formsCardsMobile');
        if (!container) return;

        container.innerHTML = '';

        if (this.formularios.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <i class="bi bi-file-earmark-text" style="font-size: 3rem;"></i>
                    <p class="mt-2">No hay formularios registrados</p>
                </div>
            `;
            return;
        }

        this.formularios.forEach(formulario => {
            const card = this.crearCardFormulario(formulario);
            container.appendChild(card);
        });
    }

    /**
     * Crear card de formulario para móvil
     */
    crearCardFormulario(formulario) {
        const card = document.createElement('div');
        card.className = 'card mb-3';
        
        const estadoLabel = this.obtenerEtiquetaEstado(formulario.estado);

        card.innerHTML = `
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h6 class="card-title mb-0">Mesa ${formulario.mesa_codigo || 'N/A'}</h6>
                    <span class="badge bg-${this.obtenerColorEstado(formulario.estado)}">${estadoLabel}</span>
                </div>
                <div class="row g-2 mb-3">
                    <div class="col-6">
                        <small class="text-muted">Tipo Elección</small>
                        <div class="fw-bold">${formulario.tipo_eleccion_nombre || 'N/A'}</div>
                    </div>
                    <div class="col-6">
                        <small class="text-muted">Total Votos</small>
                        <div class="fw-bold">${Utils.formatNumber(formulario.total_votos)}</div>
                    </div>
                    <div class="col-12">
                        <small class="text-muted">Fecha</small>
                        <div>${Utils.formatDate(formulario.created_at)}</div>
                    </div>
                </div>
                <div class="d-flex gap-2 flex-wrap">
                    ${this.generarBotonesAccionMobile(formulario)}
                </div>
            </div>
        `;

        return card;
    }

    /**
     * Generar botones de acción para tabla
     */
    generarBotonesAccion(formulario) {
        const acciones = this.obtenerAccionesDisponibles(formulario);
        
        return `
            <div class="btn-group btn-group-sm" role="group">
                ${acciones.map(accion => `
                    <button class="btn btn-outline-${accion.color}" 
                            onclick="event.stopPropagation(); ${accion.funcion}(${formulario.id})" 
                            title="${accion.titulo}">
                        <i class="bi bi-${accion.icono}"></i> ${accion.texto}
                    </button>
                `).join('')}
            </div>
        `;
    }

    /**
     * Generar botones de acción para móvil
     */
    generarBotonesAccionMobile(formulario) {
        const acciones = this.obtenerAccionesDisponibles(formulario);
        
        return acciones.map(accion => `
            <button class="btn btn-sm btn-outline-${accion.color}" 
                    onclick="${accion.funcion}(${formulario.id})" 
                    title="${accion.titulo}">
                <i class="bi bi-${accion.icono}"></i> ${accion.texto}
            </button>
        `).join('');
    }

    /**
     * Obtener acciones disponibles según el estado del formulario
     */
    obtenerAccionesDisponibles(formulario) {
        const acciones = [];
        const esLocal = formulario.es_local || formulario.estado === 'local';

        switch (formulario.estado) {
            case 'borrador':
            case 'local':
                acciones.push({
                    texto: 'Editar',
                    icono: 'pencil',
                    color: 'warning',
                    titulo: 'Editar formulario',
                    funcion: esLocal ? 'window.formulariosManager.editarBorradorLocal' : 'window.formulariosManager.editarFormulario'
                });
                
                if (esLocal) {
                    acciones.push({
                        texto: 'Eliminar',
                        icono: 'trash',
                        color: 'danger',
                        titulo: 'Eliminar borrador',
                        funcion: 'window.formulariosManager.eliminarBorradorLocal'
                    });
                }
                break;

            case 'rechazado':
                acciones.push({
                    texto: 'Corregir',
                    icono: 'arrow-repeat',
                    color: 'warning',
                    titulo: 'Corregir y reenviar',
                    funcion: 'window.formulariosManager.editarFormulario'
                });
                acciones.push({
                    texto: 'Ver',
                    icono: 'eye',
                    color: 'primary',
                    titulo: 'Ver detalles y motivo',
                    funcion: 'window.formulariosManager.verFormulario'
                });
                break;

            case 'pendiente':
            case 'validado':
                acciones.push({
                    texto: 'Ver',
                    icono: 'eye',
                    color: 'primary',
                    titulo: 'Ver detalles',
                    funcion: 'window.formulariosManager.verFormulario'
                });
                break;
        }

        return acciones;
    }

    /**
     * Ver formulario en modal
     */
    async verFormulario(formularioId) {
        try {
            console.log('[FormulariosManager] Cargando formulario para visualización:', formularioId);
            
            const response = await APIClient.getMiFormularioE14(formularioId);
            
            if (response.success) {
                this.formularioActual = response.data;
                this.mostrarModalVisualizacion();
            } else {
                Utils.showError('Error al cargar formulario: ' + (response.error || 'Error desconocido'));
            }
        } catch (error) {
            console.error('[FormulariosManager] Error al cargar formulario:', error);
            Utils.showError('Error al cargar formulario: ' + error.message);
        }
    }

    /**
     * Editar formulario
     */
    async editarFormulario(formularioId) {
        try {
            const response = await APIClient.getMiFormularioE14(formularioId);
            
            if (response.success) {
                this.formularioActual = response.data;
                // Abrir modal de edición
                if (window.showCreateForm) {
                    window.showCreateForm(this.formularioActual);
                }
            } else {
                Utils.showError('Error al cargar formulario para edición');
            }
        } catch (error) {
            console.error('[FormulariosManager] Error al editar formulario:', error);
            Utils.showError('Error al cargar formulario: ' + error.message);
        }
    }

    /**
     * Mostrar modal de visualización
     */
    mostrarModalVisualizacion() {
        if (!this.formularioActual) return;

        const formulario = this.formularioActual;

        // Llenar información básica
        this.llenarInformacionBasica(formulario);
        
        // Llenar datos de votación
        this.llenarDatosVotacion(formulario);
        
        // Mostrar votos por partido
        this.mostrarVotosPorPartido(formulario.votos_partidos || []);
        
        // Mostrar imagen
        this.mostrarImagenFormulario(formulario);
        
        // Mostrar estado detallado
        this.mostrarEstadoDetallado(formulario);

        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('verFormularioModal'));
        modal.show();
    }

    /**
     * Llenar información básica del modal
     */
    llenarInformacionBasica(formulario) {
        const elementos = {
            'verMesa': `Mesa ${formulario.mesa_codigo || 'N/A'}`,
            'verObservaciones': formulario.observaciones || 'Sin observaciones'
        };

        Object.entries(elementos).forEach(([id, valor]) => {
            const elemento = document.getElementById(id);
            if (elemento) elemento.textContent = valor;
        });

        // Estado con badge
        const estadoElement = document.getElementById('verEstado');
        if (estadoElement) {
            const estadoLabel = this.obtenerEtiquetaEstado(formulario.estado);
            const estadoColor = this.obtenerColorEstado(formulario.estado);
            estadoElement.innerHTML = `<span class="badge bg-${estadoColor}">${estadoLabel}</span>`;
        }
    }

    /**
     * Llenar datos de votación del modal
     */
    llenarDatosVotacion(formulario) {
        const campos = [
            'verVotantesRegistrados', 'verTotalVotos', 'verVotosValidos',
            'verVotosNulos', 'verVotosBlanco', 'verTarjetasNoMarcadas'
        ];

        const valores = [
            formulario.total_votantes_registrados || 0,
            formulario.total_votos || 0,
            formulario.votos_validos || 0,
            formulario.votos_nulos || 0,
            formulario.votos_blanco || 0,
            formulario.tarjetas_no_marcadas || 0
        ];

        campos.forEach((campo, index) => {
            const elemento = document.getElementById(campo);
            if (elemento) {
                elemento.textContent = Utils.formatNumber(valores[index]);
            }
        });
    }

    /**
     * Mostrar votos por partido en el modal
     */
    mostrarVotosPorPartido(votosPartidos) {
        const container = document.getElementById('verVotosPorPartido');
        if (!container) return;

        if (!votosPartidos || votosPartidos.length === 0) {
            container.innerHTML = '<p class="text-muted">No hay votos registrados</p>';
            return;
        }

        const totalVotos = votosPartidos.reduce((sum, vp) => sum + (vp.votos || 0), 0);

        let html = '';
        votosPartidos.forEach(vp => {
            const porcentaje = totalVotos > 0 ? ((vp.votos || 0) / totalVotos * 100).toFixed(1) : 0;
            
            html += `
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
        });

        container.innerHTML = html;
    }

    /**
     * Mostrar imagen del formulario
     */
    mostrarImagenFormulario(formulario) {
        const container = document.getElementById('verImagenFormulario');
        if (!container) return;

        if (formulario.imagen_url) {
            container.innerHTML = `
                <img src="${formulario.imagen_url}" class="img-fluid border rounded" 
                     style="max-height: 400px; cursor: pointer;" 
                     onclick="window.open('${formulario.imagen_url}', '_blank')"
                     alt="Formulario E-14">
                <p class="text-muted mt-2"><small>Click para ver en tamaño completo</small></p>
            `;
        } else {
            container.innerHTML = '<p class="text-muted">No hay imagen disponible</p>';
        }
    }

    /**
     * Mostrar estado detallado del formulario
     */
    mostrarEstadoDetallado(formulario) {
        const container = document.getElementById('verEstadoDetalle');
        if (!container) return;

        let html = '';

        switch (formulario.estado) {
            case 'pendiente':
                html = `
                    <div class="alert alert-info">
                        <i class="bi bi-clock"></i>
                        <strong>Formulario Enviado</strong><br>
                        Su formulario ha sido enviado y está pendiente de revisión por el coordinador de puesto.
                        <br><small>Enviado el: ${Utils.formatDate(formulario.created_at)}</small>
                    </div>
                `;
                break;

            case 'validado':
                html = `
                    <div class="alert alert-success">
                        <i class="bi bi-check-circle"></i>
                        <strong>Formulario Validado</strong><br>
                        Su formulario ha sido validado por el coordinador de puesto.
                        <br><small>Validado el: ${Utils.formatDate(formulario.validado_at)}</small>
                    </div>
                `;
                break;

            case 'rechazado':
                html = `
                    <div class="alert alert-danger">
                        <i class="bi bi-x-circle"></i>
                        <strong>Formulario Rechazado</strong><br>
                        Su formulario ha sido rechazado. Motivo: ${formulario.motivo_rechazo || 'No especificado'}
                        <br><small>Rechazado el: ${Utils.formatDate(formulario.validado_at)}</small>
                        <br><br>
                        <button class="btn btn-warning btn-sm" onclick="window.formulariosManager.editarFormularioRechazado(${formulario.id})">
                            <i class="bi bi-pencil"></i> Corregir y Reenviar
                        </button>
                    </div>
                `;
                break;
        }

        container.innerHTML = html;
    }

    /**
     * Editar formulario rechazado
     */
    async editarFormularioRechazado(formularioId) {
        try {
            // Cerrar modal de visualización
            const verModal = bootstrap.Modal.getInstance(document.getElementById('verFormularioModal'));
            if (verModal) verModal.hide();
            
            // Cargar formulario para edición
            await this.editarFormulario(formularioId);
        } catch (error) {
            console.error('[FormulariosManager] Error al editar formulario rechazado:', error);
            Utils.showError('Error al cargar formulario para edición: ' + error.message);
        }
    }

    /**
     * Mostrar error en tabla
     */
    mostrarErrorEnTabla(mensaje) {
        const tbody = document.querySelector('#formsTable tbody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-4">
                        <p class="text-danger">❌ ${mensaje}</p>
                        <button class="btn btn-sm btn-outline-primary mt-2" onclick="window.formulariosManager.cargarFormularios()">
                            <i class="bi bi-arrow-clockwise"></i> Reintentar
                        </button>
                    </td>
                </tr>
            `;
        }
    }

    /**
     * Verificar si un formulario puede editarse
     */
    puedeEditarFormulario(formulario) {
        return ['borrador', 'local', 'rechazado'].includes(formulario.estado);
    }

    /**
     * Obtener etiqueta de estado
     */
    obtenerEtiquetaEstado(estado) {
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
    obtenerColorEstado(estado) {
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
window.FormulariosManager = FormulariosManager;