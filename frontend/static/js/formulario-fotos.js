/**
 * Manejo de múltiples fotos para formularios E-14
 */

class FormularioFotos {
    constructor(formularioId, esCoordinador = false) {
        this.formularioId = formularioId;
        this.esCoordinador = esCoordinador;
        this.fotos = [];
        this.fotoActual = 0;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.cargarFotos();
    }
    
    setupEventListeners() {
        // Subir foto
        const inputFoto = document.getElementById('input-foto');
        const btnSubirFoto = document.getElementById('btn-subir-foto');
        
        if (inputFoto && btnSubirFoto) {
            btnSubirFoto.addEventListener('click', () => inputFoto.click());
            inputFoto.addEventListener('change', (e) => this.subirFoto(e.target.files[0]));
        }
        
        // Navegación de fotos
        const btnAnterior = document.getElementById('btn-foto-anterior');
        const btnSiguiente = document.getElementById('btn-foto-siguiente');
        
        if (btnAnterior) btnAnterior.addEventListener('click', () => this.navegarFoto(-1));
        if (btnSiguiente) btnSiguiente.addEventListener('click', () => this.navegarFoto(1));
        
        // Validación (solo coordinadores)
        if (this.esCoordinador) {
            const btnValidar = document.getElementById('btn-validar-foto');
            const btnRechazar = document.getElementById('btn-rechazar-foto');
            const btnValidarTodas = document.getElementById('btn-validar-todas');
            
            if (btnValidar) btnValidar.addEventListener('click', () => this.validarFoto(true));
            if (btnRechazar) btnRechazar.addEventListener('click', () => this.validarFoto(false));
            if (btnValidarTodas) btnValidarTodas.addEventListener('click', () => this.validarTodasFotos());
        }
        
        // Eliminar foto
        const btnEliminar = document.getElementById('btn-eliminar-foto');
        if (btnEliminar) btnEliminar.addEventListener('click', () => this.eliminarFoto());
        
        // Establecer como principal
        const btnPrincipal = document.getElementById('btn-foto-principal');
        if (btnPrincipal) btnPrincipal.addEventListener('click', () => this.establecerPrincipal());
    }
    
    async cargarFotos() {
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/formulario-fotos/formulario/${this.formularioId}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.fotos = data.fotos;
                this.actualizarVisualizacion();
            } else {
                this.mostrarError('Error al cargar fotos: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al cargar fotos');
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
        
        // Validar tamaño (10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.mostrarError('Archivo muy grande. Máximo 10MB');
            return;
        }
        
        try {
            this.mostrarCargando(true);
            
            const formData = new FormData();
            formData.append('foto', file);
            formData.append('descripcion', document.getElementById('descripcion-foto')?.value || '');
            
            const response = await fetch(`/api/formulario-fotos/subir/${this.formularioId}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarExito('Foto subida exitosamente');
                await this.cargarFotos(); // Recargar fotos
                
                // Limpiar input
                const inputFoto = document.getElementById('input-foto');
                if (inputFoto) inputFoto.value = '';
                
                const descripcionInput = document.getElementById('descripcion-foto');
                if (descripcionInput) descripcionInput.value = '';
                
            } else {
                this.mostrarError('Error al subir foto: ' + (data.errors?.file?.[0] || data.error));
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al subir foto');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
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
        const contenedorFotos = document.getElementById('contenedor-fotos');
        const infoFotos = document.getElementById('info-fotos');
        const imagenActual = document.getElementById('imagen-actual');
        
        if (!contenedorFotos) return;
        
        if (this.fotos.length === 0) {
            contenedorFotos.innerHTML = `
                <div class="text-center p-4">
                    <i class="fas fa-camera fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No hay fotos subidas</p>
                    ${!this.esCoordinador ? '<p class="small">Haga clic en "Subir Foto" para agregar imágenes</p>' : ''}
                </div>
            `;
            
            if (infoFotos) infoFotos.textContent = 'Sin fotos';
            return;
        }
        
        const foto = this.fotos[this.fotoActual];
        
        // Actualizar imagen
        if (imagenActual) {
            imagenActual.src = foto.url;
            imagenActual.alt = foto.descripcion || `Foto ${this.fotoActual + 1}`;
        }
        
        // Actualizar información
        if (infoFotos) {
            infoFotos.innerHTML = `
                Foto ${this.fotoActual + 1} de ${this.fotos.length}
                ${foto.es_principal ? '<span class="badge badge-primary ml-2">Principal</span>' : ''}
                ${foto.validada ? '<span class="badge badge-success ml-2">Validada</span>' : 
                  '<span class="badge badge-warning ml-2">Pendiente</span>'}
            `;
        }
        
        // Actualizar descripción
        const descripcionActual = document.getElementById('descripcion-actual');
        if (descripcionActual) {
            descripcionActual.textContent = foto.descripcion || 'Sin descripción';
        }
        
        // Actualizar comentario de validación
        const comentarioValidacion = document.getElementById('comentario-validacion');
        if (comentarioValidacion) {
            if (foto.comentario_validacion) {
                comentarioValidacion.innerHTML = `
                    <strong>Comentario:</strong> ${foto.comentario_validacion}
                    <br><small class="text-muted">Por: ${foto.validada_por_nombre || 'Sistema'}</small>
                `;
                comentarioValidacion.style.display = 'block';
            } else {
                comentarioValidacion.style.display = 'none';
            }
        }
        
        // Actualizar botones
        this.actualizarBotones();
        
        // Actualizar miniaturas
        this.actualizarMiniaturas();
    }
    
    actualizarBotones() {
        const btnAnterior = document.getElementById('btn-foto-anterior');
        const btnSiguiente = document.getElementById('btn-foto-siguiente');
        const btnEliminar = document.getElementById('btn-eliminar-foto');
        const btnPrincipal = document.getElementById('btn-foto-principal');
        const btnValidar = document.getElementById('btn-validar-foto');
        const btnRechazar = document.getElementById('btn-rechazar-foto');
        
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
        const contenedorMiniaturas = document.getElementById('miniaturas-fotos');
        if (!contenedorMiniaturas) return;
        
        contenedorMiniaturas.innerHTML = '';
        
        this.fotos.forEach((foto, index) => {
            const miniatura = document.createElement('div');
            miniatura.className = `miniatura ${index === this.fotoActual ? 'activa' : ''}`;
            miniatura.innerHTML = `
                <img src="${foto.url}" alt="Foto ${index + 1}" class="img-thumbnail" style="width: 60px; height: 60px; object-fit: cover; cursor: pointer;">
                ${foto.es_principal ? '<i class="fas fa-star text-warning position-absolute" style="top: 2px; right: 2px;"></i>' : ''}
                ${foto.validada ? '<i class="fas fa-check-circle text-success position-absolute" style="bottom: 2px; right: 2px;"></i>' : 
                  '<i class="fas fa-clock text-warning position-absolute" style="bottom: 2px; right: 2px;"></i>'}
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
    
    async validarFoto(validada) {
        if (this.fotos.length === 0) return;
        
        const foto = this.fotos[this.fotoActual];
        const comentario = prompt(validada ? 'Comentario de validación (opcional):' : 'Motivo de rechazo:');
        
        if (comentario === null) return; // Usuario canceló
        
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/formulario-fotos/validar/${foto.id}`, {
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
                this.mostrarError('Error al validar foto: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al validar foto');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
    }
    
    async validarTodasFotos() {
        if (this.fotos.length === 0) return;
        
        const validada = confirm('¿Validar todas las fotos del formulario?');
        if (!validada) return;
        
        const comentario = prompt('Comentario para todas las fotos (opcional):') || '';
        
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/formulario-fotos/validacion-masiva/${this.formularioId}`, {
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
        
        if (!confirm('¿Está seguro de eliminar esta foto? Esta acción no se puede deshacer.')) {
            return;
        }
        
        try {
            this.mostrarCargando(true);
            
            const response = await fetch(`/api/formulario-fotos/eliminar/${foto.id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarExito('Foto eliminada exitosamente');
                
                // Ajustar índice actual
                if (this.fotoActual >= this.fotos.length - 1) {
                    this.fotoActual = Math.max(0, this.fotos.length - 2);
                }
                
                await this.cargarFotos(); // Recargar fotos
            } else {
                this.mostrarError('Error al eliminar foto: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al eliminar foto');
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
            
            const response = await fetch(`/api/formulario-fotos/principal/${foto.id}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarExito('Foto establecida como principal');
                await this.cargarFotos(); // Recargar fotos
            } else {
                this.mostrarError('Error al establecer foto principal: ' + data.error);
            }
            
        } catch (error) {
            this.mostrarError('Error de conexión al establecer foto principal');
            console.error('Error:', error);
        } finally {
            this.mostrarCargando(false);
        }
    }
    
    mostrarCargando(mostrar) {
        const spinner = document.getElementById('spinner-fotos');
        if (spinner) {
            spinner.style.display = mostrar ? 'block' : 'none';
        }
    }
    
    mostrarError(mensaje) {
        const alertContainer = document.getElementById('alert-container-fotos');
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
        const alertContainer = document.getElementById('alert-container-fotos');
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

// Función global para inicializar el manejo de fotos
window.inicializarFormularioFotos = function(formularioId, esCoordinador = false) {
    return new FormularioFotos(formularioId, esCoordinador);
};