/**
 * Manejo de múltiples fotos para incidentes y delitos electorales
 */

class IncidentesDelitosFotos {
    constructor(tipoReporte, reporteId, esCoordinador = false) {
        this.tipoReporte = tipoReporte; // 'incidente' o 'delito'
        this.reporteId = reporteId;
        this.esCoordinador = esCoordinador;
        this.fotos = [];
        this.fotoActual = 0;
        this.categorias = {};
        this.tiposEvidencia = {};
        this.relevancias = {};
        
        this.init();
    }
    
    init() {
        this.cargarCategorias();
        this.setupEventListeners();
        this.cargarFotos();
    }
    
    async cargarCategorias() {
        try {
            const response = await fetch('/api/evidencias-fotos/categorias', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.categorias = data.categorias;
                this.tiposEvidencia = data.tipos_evidencia;
                this.relevancias = data.relevancias;
                this.actualizarSelectores();
            }
        } catch (error) {
            console.error('Error al cargar categorías:', error);
        }
    }
    
    actualizarSelectores() {
        // Actualizar selector de categoría
        const selectCategoria = document.getElementById('categoria-evidencia');
        if (selectCategoria) {
            selectCategoria.innerHTML = '';
            Object.entries(this.categorias).forEach(([key, value]) => {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = value;
                selectCategoria.appendChild(option);
            });
        }
        
        // Actualizar selector de tipo de evidencia
        const selectTipo = document.getElementById('tipo-evidencia');
        if (selectTipo) {
            selectTipo.innerHTML = '';
            Object.entries(this.tiposEvidencia).forEach(([key, value]) => {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = value;
                selectTipo.appendChild(option);
            });
        }
        
        // Actualizar selector de relevancia
        const selectRelevancia = document.getElementById('relevancia-evidencia');
        if (selectRelevancia) {
            selectRelevancia.innerHTML = '';
            Object.entries(this.relevancias).forEach(([key, value]) => {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = value;
                selectRelevancia.appendChild(option);
            });
        }
    }
    
    setupEventListeners() {
        // Subir foto
        const inputFoto = document.getElementById('input-foto-evidencia');
        const btnSubirFoto = document.getElementById('btn-subir-evidencia');
        
        if (inputFoto && btnSubirFoto) {
            btnSubirFoto.addEventListener('click', () => inputFoto.click());
            inputFoto.addEventListener('change', (e) => this.subirFoto(e.target.files[0]));
        }
        
        // Navegación de fotos
        const btnAnterior = document.getElementById('btn-evidencia-anterior');
        const btnSiguiente = document.getElementById('btn-evidencia-siguiente');
        
        if (btnAnterior) btnAnterior.addEventListener('click', () => this.navegarFoto(-1));
        if (btnSiguiente) btnSiguiente.addEventListener('click', () => this.navegarFoto(1));
        
        // Validación (solo coordinadores)
        if (this.esCoordinador) {
            const btnValidar = document.getElementById('btn-validar-evidencia');
            const btnRechazar = document.getElementById('btn-rechazar-evidencia');
            const btnValidarTodas = document.getElementById('btn-validar-todas-evidencias');
            
            if (btnValidar) btnValidar.addEventListener('click', () => this.validarFoto(true));
            if (btnRechazar) btnRechazar.addEventListener('click', () => this.validarFoto(false));
            if (btnValidarTodas) btnValidarTodas.addEventListener('click', () => this.validarTodasFotos());
        }
        
        // Eliminar foto
        const btnEliminar = document.getElementById('btn-eliminar-evidencia');
        if (btnEliminar) btnEliminar.addEventListener('click', () => this.eliminarFoto());
        
        // Establecer como principal
        const btnPrincipal = document.getElementById('btn-evidencia-principal');
        if (btnPrincipal) btnPrincipal.addEventListener('click', () => this.establecerPrincipal());
        
        // Editar metadatos
        const btnEditarMetadatos = document.getElementById('btn-editar-metadatos');
        if (btnEditarMetadatos) btnEditarMetadatos.addEventListener('click', () => this.mostrarModalMetadatos());
    }
    
    async cargarFotos() {
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/evidencias-fotos/${this.tipoReporte}/${this.reporteId}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.fotos = data.fotos;
                this.estadisticas = data.estadisticas;
                this.actualizarVisualizacion();
                this.actualizarEstadisticas();
            } else {
                this.mostrarError('Error al cargar evidencias: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al cargar evidencias');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
    }
    
    async subirFoto(file) {
        if (!file) return;
        
        // Validar tipo de archivo
        const tiposPermitidos = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        if (!tiposPermitidos.includes(file.type)) {
            this.mostrarError('Tipo de archivo no permitido. Use JPG, PNG o WebP');
            return;
        }
        
        // Validar tamaño (15MB para evidencias)
        if (file.size > 15 * 1024 * 1024) {
            this.mostrarError('Archivo muy grande. Máximo 15MB');
            return;
        }
        
        try {
            this.mostrarCargando(true);
            
            const formData = new FormData();
            formData.append('foto', file);
            formData.append('descripcion', document.getElementById('descripcion-evidencia')?.value || '');
            formData.append('categoria', document.getElementById('categoria-evidencia')?.value || 'general');
            formData.append('tipo_evidencia', document.getElementById('tipo-evidencia')?.value || 'directa');
            formData.append('relevancia', document.getElementById('relevancia-evidencia')?.value || 'media');
            
            const response = await fetch(`/api/evidencias-fotos/subir/${this.tipoReporte}/${this.reporteId}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarExito('Evidencia subida exitosamente');
                await this.cargarFotos(); // Recargar fotos
                
                // Limpiar formulario
                this.limpiarFormulario();
                
            } else {
                this.mostrarError('Error al subir evidencia: ' + (data.errors?.file?.[0] || data.error));
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al subir evidencia');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
    }
    
    limpiarFormulario() {
        const inputFoto = document.getElementById('input-foto-evidencia');
        if (inputFoto) inputFoto.value = '';
        
        const descripcion = document.getElementById('descripcion-evidencia');
        if (descripcion) descripcion.value = '';
        
        const categoria = document.getElementById('categoria-evidencia');
        if (categoria) categoria.value = 'general';
        
        const tipo = document.getElementById('tipo-evidencia');
        if (tipo) tipo.value = 'directa';
        
        const relevancia = document.getElementById('relevancia-evidencia');
        if (relevancia) relevancia.value = 'media';
    }
    
    navegarFoto(direccion) {
        if (this.fotos.length === 0) return;
        
        this.fotoActual += direccion;
        
        if (this.fotoActual < 0) {
            this.fotoActual = this.fotos.length - 1;
        } else if (this.fotoActual >= this.fotos.length) {
            this.fotoActual = 0;
        }
        
        this.actualizarVisualizacion();
    }
    
    actualizarVisualizacion() {
        const contenedorFotos = document.getElementById('contenedor-evidencias');
        const infoFotos = document.getElementById('info-evidencias');
        const imagenActual = document.getElementById('imagen-evidencia-actual');
        
        if (!contenedorFotos) return;
        
        if (this.fotos.length === 0) {
            contenedorFotos.innerHTML = `
                <div class="text-center p-4">
                    <i class="fas fa-camera fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No hay evidencias fotográficas</p>
                    ${!this.esCoordinador ? '<p class="small">Haga clic en "Subir Evidencia" para agregar fotos</p>' : ''}
                </div>
            `;
            
            if (infoFotos) infoFotos.textContent = 'Sin evidencias';
            return;
        }
        
        const foto = this.fotos[this.fotoActual];
        
        // Actualizar imagen
        if (imagenActual) {
            imagenActual.src = foto.url;
            imagenActual.alt = foto.descripcion || `Evidencia ${this.fotoActual + 1}`;
        }
        
        // Actualizar información
        if (infoFotos) {
            infoFotos.innerHTML = `
                Evidencia ${this.fotoActual + 1} de ${this.fotos.length}
                ${foto.es_principal ? '<span class="badge badge-primary ml-2">Principal</span>' : ''}
                ${foto.validada ? '<span class="badge badge-success ml-2">Validada</span>' : 
                  '<span class="badge badge-warning ml-2">Pendiente</span>'}
                <span class="badge badge-info ml-2">${foto.categoria_label}</span>
                <span class="badge badge-${this.getBadgeColorRelevancia(foto.relevancia)} ml-2">${foto.relevancia_label}</span>
            `;
        }
        
        // Actualizar detalles
        this.actualizarDetallesFoto(foto);
        
        // Actualizar botones
        this.actualizarBotones();
        
        // Actualizar miniaturas
        this.actualizarMiniaturas();
    }
    
    getBadgeColorRelevancia(relevancia) {
        const colores = {
            'baja': 'secondary',
            'media': 'info',
            'alta': 'warning',
            'critica': 'danger'
        };
        return colores[relevancia] || 'secondary';
    }
    
    actualizarDetallesFoto(foto) {
        // Actualizar descripción
        const descripcionActual = document.getElementById('descripcion-evidencia-actual');
        if (descripcionActual) {
            descripcionActual.textContent = foto.descripcion || 'Sin descripción';
        }
        
        // Actualizar tipo de evidencia
        const tipoEvidencia = document.getElementById('tipo-evidencia-actual');
        if (tipoEvidencia) {
            tipoEvidencia.textContent = foto.tipo_evidencia_label || 'No especificado';
        }
        
        // Actualizar comentario de validación
        const comentarioValidacion = document.getElementById('comentario-validacion-evidencia');
        if (comentarioValidacion) {
            if (foto.comentario_validacion) {
                comentarioValidacion.innerHTML = `
                    <strong>Comentario de validación:</strong> ${foto.comentario_validacion}
                    <br><small class="text-muted">Por: ${foto.validada_por_nombre || 'Sistema'}</small>
                `;
                comentarioValidacion.style.display = 'block';
            } else {
                comentarioValidacion.style.display = 'none';
            }
        }
        
        // Actualizar metadatos adicionales
        const metadatosAdicionales = document.getElementById('metadatos-adicionales');
        if (metadatosAdicionales) {
            let metadatos = [];
            
            if (foto.fecha_captura) {
                metadatos.push(`<strong>Capturada:</strong> ${new Date(foto.fecha_captura).toLocaleString()}`);
            }
            
            if (foto.dispositivo) {
                metadatos.push(`<strong>Dispositivo:</strong> ${foto.dispositivo}`);
            }
            
            if (foto.tamaño_bytes) {
                const tamaño = (foto.tamaño_bytes / (1024 * 1024)).toFixed(2);
                metadatos.push(`<strong>Tamaño:</strong> ${tamaño} MB`);
            }
            
            if (foto.ancho && foto.alto) {
                metadatos.push(`<strong>Resolución:</strong> ${foto.ancho}x${foto.alto}`);
            }
            
            metadatosAdicionales.innerHTML = metadatos.join('<br>');
        }
    }
    
    actualizarBotones() {
        const btnAnterior = document.getElementById('btn-evidencia-anterior');
        const btnSiguiente = document.getElementById('btn-evidencia-siguiente');
        const btnEliminar = document.getElementById('btn-eliminar-evidencia');
        const btnPrincipal = document.getElementById('btn-evidencia-principal');
        const btnValidar = document.getElementById('btn-validar-evidencia');
        const btnRechazar = document.getElementById('btn-rechazar-evidencia');
        
        const hayFotos = this.fotos.length > 0;
        const foto = hayFotos ? this.fotos[this.fotoActual] : null;
        
        // Navegación
        if (btnAnterior) btnAnterior.disabled = !hayFotos;
        if (btnSiguiente) btnSiguiente.disabled = !hayFotos;
        
        // Eliminar
        if (btnEliminar) btnEliminar.disabled = !hayFotos;
        
        // Principal
        if (btnPrincipal) {
            btnPrincipal.disabled = !hayFotos || (foto && foto.es_principal);
            btnPrincipal.textContent = foto && foto.es_principal ? 'Es Principal' : 'Marcar Principal';
        }
        
        // Validación (solo coordinadores)
        if (this.esCoordinador && foto) {
            if (btnValidar) {
                btnValidar.disabled = foto.validada;
                btnValidar.textContent = foto.validada ? 'Validada' : 'Validar';
            }
            if (btnRechazar) {
                btnRechazar.disabled = foto.validada === false;
                btnRechazar.textContent = foto.validada === false ? 'Rechazada' : 'Rechazar';
            }
        }
    }
    
    actualizarMiniaturas() {
        const contenedorMiniaturas = document.getElementById('miniaturas-evidencias');
        if (!contenedorMiniaturas) return;
        
        contenedorMiniaturas.innerHTML = '';
        
        this.fotos.forEach((foto, index) => {
            const miniatura = document.createElement('div');
            miniatura.className = `miniatura-evidencia ${index === this.fotoActual ? 'activa' : ''}`;
            miniatura.innerHTML = `
                <img src="${foto.url}" alt="Evidencia ${index + 1}" class="img-thumbnail" style="width: 60px; height: 60px; object-fit: cover; cursor: pointer;">
                ${foto.es_principal ? '<i class="fas fa-star text-warning position-absolute" style="top: 2px; right: 2px;"></i>' : ''}
                ${foto.validada ? '<i class="fas fa-check-circle text-success position-absolute" style="bottom: 2px; right: 2px;"></i>' : 
                  '<i class="fas fa-clock text-warning position-absolute" style="bottom: 2px; right: 2px;"></i>'}
                <div class="badge badge-${this.getBadgeColorRelevancia(foto.relevancia)} position-absolute" style="top: 2px; left: 2px; font-size: 0.6em;">
                    ${foto.relevancia.charAt(0).toUpperCase()}
                </div>
            `;
            miniatura.style.position = 'relative';
            miniatura.style.display = 'inline-block';
            miniatura.style.margin = '2px';
            
            miniatura.addEventListener('click', () => {
                this.fotoActual = index;
                this.actualizarVisualizacion();
            });
            
            contenedorMiniaturas.appendChild(miniatura);
        });
    }
    
    actualizarEstadisticas() {
        if (!this.estadisticas) return;
        
        const statsContainer = document.getElementById('estadisticas-evidencias');
        if (statsContainer) {
            statsContainer.innerHTML = `
                <div class="row">
                    <div class="col-3">
                        <div class="text-center">
                            <h5 class="mb-0">${this.estadisticas.total_fotos}</h5>
                            <small class="text-muted">Total</small>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="text-center">
                            <h5 class="mb-0 text-success">${this.estadisticas.fotos_validadas}</h5>
                            <small class="text-muted">Validadas</small>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="text-center">
                            <h5 class="mb-0 text-warning">${this.estadisticas.fotos_pendientes}</h5>
                            <small class="text-muted">Pendientes</small>
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="text-center">
                            <h5 class="mb-0 text-info">${this.estadisticas.porcentaje_validadas.toFixed(1)}%</h5>
                            <small class="text-muted">Validadas</small>
                        </div>
                    </div>
                </div>
            `;
        }
    }
    
    async validarFoto(validada) {
        if (this.fotos.length === 0) return;
        
        const foto = this.fotos[this.fotoActual];
        const comentario = prompt(validada ? 'Comentario de validación (opcional):' : 'Motivo de rechazo:');
        
        if (comentario === null) return; // Usuario canceló
        
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/evidencias-fotos/validar/${foto.id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    validada: validada,
                    comentario: comentario
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarExito(data.message);
                await this.cargarFotos(); // Recargar fotos
            } else {
                this.mostrarError('Error al validar evidencia: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al validar evidencia');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
    }
    
    async validarTodasFotos() {
        if (this.fotos.length === 0) return;
        
        const validada = confirm('¿Validar todas las evidencias del reporte?');
        if (!validada) return;
        
        const comentario = prompt('Comentario para todas las evidencias (opcional):') || '';
        
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/evidencias-fotos/validacion-masiva/${this.tipoReporte}/${this.reporteId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({
                    validada: true,
                    comentario: comentario
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarExito(data.message);
                await this.cargarFotos(); // Recargar fotos
            } else {
                this.mostrarError('Error en validación masiva: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión en validación masiva');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
    }
    
    async eliminarFoto() {
        if (this.fotos.length === 0) return;
        
        const foto = this.fotos[this.fotoActual];
        
        if (!confirm('¿Está seguro de eliminar esta evidencia? Esta acción no se puede deshacer.')) {
            return;
        }
        
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/evidencias-fotos/eliminar/${foto.id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarExito('Evidencia eliminada exitosamente');
                
                // Ajustar índice actual
                if (this.fotoActual >= this.fotos.length - 1) {
                    this.fotoActual = Math.max(0, this.fotos.length - 2);
                }
                
                await this.cargarFotos(); // Recargar fotos
            } else {
                this.mostrarError('Error al eliminar evidencia: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al eliminar evidencia');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
    }
    
    async establecerPrincipal() {
        if (this.fotos.length === 0) return;
        
        const foto = this.fotos[this.fotoActual];
        
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/evidencias-fotos/principal/${foto.id}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarExito('Evidencia establecida como principal');
                await this.cargarFotos(); // Recargar fotos
            } else {
                this.mostrarError('Error al establecer evidencia principal: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al establecer evidencia principal');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
    }
    
    mostrarCargando(mostrar) {
        const spinner = document.getElementById('spinner-evidencias');
        if (spinner) {
            spinner.style.display = mostrar ? 'block' : 'none';
        }
    }
    
    mostrarError(mensaje) {
        const alertContainer = document.getElementById('alert-container-evidencias');
        if (alertContainer) {
            alertContainer.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="fas fa-exclamation-triangle"></i> ${mensaje}
                    <button type="button" class="close" data-dismiss="alert">
                        <span>&times;</span>
                    </button>
                </div>
            `;
        } else {
            alert('Error: ' + mensaje);
        }
    }
    
    mostrarExito(mensaje) {
        const alertContainer = document.getElementById('alert-container-evidencias');
        if (alertContainer) {
            alertContainer.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <i class="fas fa-check-circle"></i> ${mensaje}
                    <button type="button" class="close" data-dismiss="alert">
                        <span>&times;</span>
                    </button>
                </div>
            `;
        } else {
            alert('Éxito: ' + mensaje);
        }
    }
}

// Función global para inicializar el manejo de evidencias fotográficas
window.inicializarIncidentesDelitosFotos = function(tipoReporte, reporteId, esCoordinador = false) {
    return new IncidentesDelitosFotos(tipoReporte, reporteId, esCoordinador);
};