/**
 * Corrección para botones de nuevo formulario y carga de tipos de elección
 */

// Sobrescribir función para habilitar botones (desktop y móvil)
window.habilitarBotonNuevoFormulario = function() {
    const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
    const btnNuevoFormularioMobile = document.getElementById('btnNuevoFormularioMobile');
    
    console.log('[Fix Buttons] habilitarBotonNuevoFormulario called');
    console.log('[Fix Buttons] presenciaVerificada:', window.presenciaVerificada);
    console.log('[Fix Buttons] mesaSeleccionadaDashboard:', window.mesaSeleccionadaDashboard);
    
    const habilitado = window.presenciaVerificada && window.mesaSeleccionadaDashboard;
    
    // Botón desktop
    if (btnNuevoFormulario) {
        btnNuevoFormulario.disabled = !habilitado;
        if (habilitado) {
            btnNuevoFormulario.classList.remove('disabled', 'btn-secondary');
            btnNuevoFormulario.classList.add('btn-primary');
            btnNuevoFormulario.title = 'Crear nuevo formulario E-14';
            console.log('[Fix Buttons] ✓ Botón desktop habilitado');
        } else {
            btnNuevoFormulario.classList.add('disabled', 'btn-secondary');
            btnNuevoFormulario.classList.remove('btn-primary');
            btnNuevoFormulario.title = 'Debe seleccionar una mesa y verificar presencia primero';
            console.log('[Fix Buttons] ✗ Botón desktop deshabilitado');
        }
    }
    
    // Botón móvil
    if (btnNuevoFormularioMobile) {
        btnNuevoFormularioMobile.disabled = !habilitado;
        if (habilitado) {
            btnNuevoFormularioMobile.classList.remove('disabled');
            btnNuevoFormularioMobile.classList.add('btn-primary-touch');
            btnNuevoFormularioMobile.classList.remove('btn-secondary');
            btnNuevoFormularioMobile.title = 'Crear nuevo formulario E-14';
            console.log('[Fix Buttons] ✓ Botón móvil habilitado');
        } else {
            btnNuevoFormularioMobile.classList.add('disabled');
            btnNuevoFormularioMobile.classList.remove('btn-primary-touch');
            btnNuevoFormularioMobile.classList.add('btn-secondary');
            btnNuevoFormularioMobile.title = 'Debe seleccionar una mesa y verificar presencia primero';
            console.log('[Fix Buttons] ✗ Botón móvil deshabilitado');
        }
    }
};

// Mejorar función de carga de tipos de elección
window.loadTiposEleccion = async function() {
    try {
        console.log('[Fix Buttons] Cargando tipos de elección...');
        const response = await APIClient.getTiposEleccion();
        console.log('[Fix Buttons] Respuesta tipos de elección:', response);
        
        if (response && response.success && response.data) {
            window.tiposEleccion = response.data;
            console.log('[Fix Buttons] Tipos de elección cargados:', window.tiposEleccion.length);
            
            const select = document.getElementById('tipoEleccion');
            if (select) {
                select.innerHTML = '<option value="">Seleccione...</option>';
                
                window.tiposEleccion.forEach(tipo => {
                    const option = document.createElement('option');
                    option.value = tipo.id;
                    option.textContent = tipo.nombre;
                    option.dataset.tipo = JSON.stringify(tipo);
                    select.appendChild(option);
                    console.log(`[Fix Buttons]   - ${tipo.nombre} (ID: ${tipo.id})`);
                });
                
                console.log('[Fix Buttons] ✓ Tipos de elección cargados en selector');
            } else {
                console.error('[Fix Buttons] ✗ No se encontró el selector tipoEleccion');
            }
        } else {
            console.error('[Fix Buttons] ✗ Error en respuesta:', response);
            
            // Si falla, intentar cargar desde configuración
            console.log('[Fix Buttons] Intentando cargar desde endpoint alternativo...');
            const altResponse = await APIClient.get('/configuracion/tipos-eleccion');
            if (altResponse && altResponse.success && altResponse.data) {
                window.tiposEleccion = altResponse.data;
                console.log('[Fix Buttons] ✓ Tipos de elección cargados desde endpoint alternativo');
                
                const select = document.getElementById('tipoEleccion');
                if (select) {
                    select.innerHTML = '<option value="">Seleccione...</option>';
                    window.tiposEleccion.forEach(tipo => {
                        const option = document.createElement('option');
                        option.value = tipo.id;
                        option.textContent = tipo.nombre;
                        option.dataset.tipo = JSON.stringify(tipo);
                        select.appendChild(option);
                    });
                }
            }
        }
    } catch (error) {
        console.error('[Fix Buttons] ✗ Error cargando tipos de elección:', error);
        
        // Mostrar error al usuario
        if (typeof Utils !== 'undefined' && typeof Utils.showError === 'function') {
            Utils.showError('Error al cargar tipos de elección. Por favor, recargue la página.');
        }
    }
};

// Asegurar que se llame cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[Fix Buttons] DOM listo, recargando tipos de elección...');
        setTimeout(() => {
            if (typeof window.loadTiposEleccion === 'function') {
                window.loadTiposEleccion();
            }
        }, 1000);
    });
} else {
    // DOM ya está listo
    console.log('[Fix Buttons] DOM ya listo, recargando tipos de elección...');
    setTimeout(() => {
        if (typeof window.loadTiposEleccion === 'function') {
            window.loadTiposEleccion();
        }
    }, 1000);
}

console.log('[Fix Buttons] ✓ Correcciones de botones cargadas');
