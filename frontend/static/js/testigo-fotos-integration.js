/**
 * Integración de sistemas de fotos múltiples en el dashboard del testigo
 */

class TestigoFotosIntegration {
    constructor() {
        this.formularioFotosInstance = null;
        this.incidenteFotosInstance = null;
        this.delitoFotosInstance = null;
    }

    /**
     * Inicializar el sistema de fotos múltiples para formularios E-14
     */
    async inicializarFormularioFotos(formularioId) {
        const container = document.getElementById('formulario-fotos-container');
        if (!container || !formularioId) return;

        try {
            // Cargar el componente HTML
            const response = await fetch('/api/components/formulario-fotos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    formulario_id: formularioId,
                    es_coordinador: false,
                    es_solo_lectura: false
                })
            });

            if (response.ok) {
                const html = await response.text();
                container.innerHTML = html;

                // Inicializar la funcionalidad JavaScript
                if (window.inicializarFormularioFotos) {
                    this.formularioFotosInstance = window.inicializarFormularioFotos(formularioId, false);
                }
            } else {
                throw new Error('Error al cargar componente de fotos');
            }
        } catch (error) {
            console.error('Error al inicializar fotos de formulario:', error);
            container.innerHTML = `
                <div class="alert alert-warning">
                    <i class="bi bi-exclamation-triangle"></i>
                    Error al cargar el sistema de fotos múltiples. 
                    <button class="btn btn-sm btn-outline-primary ms-2" onclick="window.testigoFotos.inicializarFormularioFotos(${formularioId})">
                        Reintentar
                    </button>
                </div>
            `;
        }
    }

    /**
     * Inicializar el sistema de evidencias fotográficas para incidentes
     */
    async inicializarIncidenteFotos(incidenteId) {
        const container = document.getElementById('incidente-fotos-container');
        if (!container || !incidenteId) return;

        try {
            // Cargar el componente HTML
            const response = await fetch('/api/components/incidentes-delitos-fotos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    tipo_reporte: 'incidente',
                    reporte_id: incidenteId,
                    es_coordinador: false,
                    es_solo_lectura: false
                })
            });

            if (response.ok) {
                const html = await response.text();
                container.innerHTML = html;

                // Inicializar la funcionalidad JavaScript
                if (window.inicializarIncidentesDelitosFotos) {
                    this.incidenteFotosInstance = window.inicializarIncidentesDelitosFotos('incidente', incidenteId, false);
                }
            } else {
                throw new Error('Error al cargar componente de evidencias');
            }
        } catch (error) {
            console.error('Error al inicializar evidencias de incidente:', error);
            container.innerHTML = `
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    El sistema de evidencias fotográficas se habilitará después de guardar el incidente.
                </div>
            `;
        }
    }

    /**
     * Inicializar el sistema de evidencias fotográficas para delitos
     */
    async inicializarDelitoFotos(delitoId) {
        const container = document.getElementById('delito-fotos-container');
        if (!container || !delitoId) return;

        try {
            // Cargar el componente HTML
            const response = await fetch('/api/components/incidentes-delitos-fotos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    tipo_reporte: 'delito',
                    reporte_id: delitoId,
                    es_coordinador: false,
                    es_solo_lectura: false
                })
            });

            if (response.ok) {
                const html = await response.text();
                container.innerHTML = html;

                // Inicializar la funcionalidad JavaScript
                if (window.inicializarIncidentesDelitosFotos) {
                    this.delitoFotosInstance = window.inicializarIncidentesDelitosFotos('delito', delitoId, false);
                }
            } else {
                throw new Error('Error al cargar componente de evidencias');
            }
        } catch (error) {
            console.error('Error al inicializar evidencias de delito:', error);
            container.innerHTML = `
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    El sistema de evidencias fotográficas se habilitará después de guardar el delito electoral.
                </div>
            `;
        }
    }

    /**
     * Limpiar instancias cuando se cierre un modal
     */
    limpiarInstancias() {
        this.formularioFotosInstance = null;
        this.incidenteFotosInstance = null;
        this.delitoFotosInstance = null;
    }

    /**
     * Mostrar sistema de fotos básico para formularios nuevos
     */
    mostrarFotosBasicasFormulario() {
        const container = document.getElementById('formulario-fotos-container');
        if (!container) return;

        container.innerHTML = `
            <div class="card border-primary">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0">
                        <i class="bi bi-camera"></i> Foto del Formulario E-14
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-12 mb-3">
                            <input type="file" class="form-control d-none" id="imagen" name="imagen" accept="image/*">
                            <button type="button" class="btn btn-primary w-100 mb-2" onclick="abrirCamara()">
                                <i class="bi bi-camera-fill"></i> Tomar Foto del Formulario
                            </button>
                            <button type="button" class="btn btn-outline-secondary w-100" onclick="document.getElementById('imagen').click()">
                                <i class="bi bi-image"></i> Seleccionar desde Galería
                            </button>
                            <small class="text-muted d-block mt-1">Tome una foto clara del formulario completo</small>
                        </div>
                        <div class="col-12">
                            <div class="image-preview" id="imagePreview">
                                <p class="text-muted">Toque el botón para tomar una foto</p>
                            </div>
                        </div>
                    </div>
                    <div class="alert alert-info mt-3">
                        <i class="bi bi-info-circle"></i>
                        <small>Después de guardar el formulario, podrá agregar múltiples fotos y gestionar evidencias adicionales.</small>
                    </div>
                </div>
            </div>
        `;
    }
}

// Instancia global
window.testigoFotos = new TestigoFotosIntegration();

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar sistema básico para formularios nuevos
    window.testigoFotos.mostrarFotosBasicasFormulario();
});