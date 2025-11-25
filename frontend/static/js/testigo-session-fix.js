/**
 * Fix para problema de sesión al tomar fotos
 * Guarda y restaura el estado del formulario automáticamente
 */

// Guardar estado del formulario antes de abrir cámara
function guardarEstadoFormulario() {
    try {
        const formData = {
            mesa_id: document.getElementById('mesa_id')?.value || '',
            tipo_eleccion_id: document.getElementById('tipo_eleccion_id')?.value || '',
            votantes_registrados: document.getElementById('votantes_registrados')?.value || '',
            total_votos: document.getElementById('total_votos')?.value || '',
            votos_validos: document.getElementById('votos_validos')?.value || '',
            votos_nulos: document.getElementById('votos_nulos')?.value || '',
            votos_blanco: document.getElementById('votos_blanco')?.value || '',
            tarjetas_no_marcadas: document.getElementById('tarjetas_no_marcadas')?.value || '',
            observaciones: document.getElementById('observaciones')?.value || '',
            votosData: typeof votosData !== 'undefined' ? votosData : {},
            timestamp: Date.now()
        };
        
        localStorage.setItem('formulario_e14_temp', JSON.stringify(formData));
        console.log('✅ Estado del formulario guardado');
        return true;
    } catch (error) {
        console.error('❌ Error al guardar formulario:', error);
        return false;
    }
}

// Restaurar estado del formulario
function restaurarEstadoFormulario() {
    const savedData = localStorage.getItem('formulario_e14_temp');
    if (!savedData) {
        console.log('No hay datos guardados para restaurar');
        return false;
    }
    
    try {
        const formData = JSON.parse(savedData);
        
        // Verificar que no sea muy antiguo (más de 2 horas)
        const maxAge = 2 * 60 * 60 * 1000; // 2 horas en milisegundos
        if (Date.now() - formData.timestamp > maxAge) {
            console.log('Datos guardados muy antiguos, descartando');
            localStorage.removeItem('formulario_e14_temp');
            return false;
        }
        
        // Restaurar campos si existen
        const campos = [
            'mesa_id', 'tipo_eleccion_id', 'votantes_registrados',
            'total_votos', 'votos_validos', 'votos_nulos',
            'votos_blanco', 'tarjetas_no_marcadas', 'observaciones'
        ];
        
        let camposRestaurados = 0;
        campos.forEach(campo => {
            const elemento = document.getElementById(campo);
            if (elemento && formData[campo]) {
                elemento.value = formData[campo];
                camposRestaurados++;
            }
        });
        
        // Restaurar votosData si existe
        if (formData.votosData && typeof votosData !== 'undefined') {
            votosData = formData.votosData;
        }
        
        console.log(`✅ Estado del formulario restaurado (${camposRestaurados} campos)`);
        
        // Mostrar notificación al usuario
        if (camposRestaurados > 0) {
            mostrarNotificacion('Formulario restaurado automáticamente', 'success');
        }
        
        // Limpiar después de restaurar
        localStorage.removeItem('formulario_e14_temp');
        return true;
    } catch (error) {
        console.error('❌ Error al restaurar formulario:', error);
        localStorage.removeItem('formulario_e14_temp');
        return false;
    }
}

// Función para abrir cámara con guardado previo
function abrirCamara() {
    console.log('📸 Abriendo cámara...');
    
    // Guardar estado antes de abrir cámara
    guardarEstadoFormulario();
    
    // Abrir input de archivo
    const input = document.getElementById('imagen');
    if (input) {
        input.click();
    } else {
        console.error('❌ Input de imagen no encontrado');
    }
}

// Mostrar notificación al usuario
function mostrarNotificacion(mensaje, tipo = 'info') {
    // Verificar si existe la función showToast
    if (typeof showToast === 'function') {
        showToast(mensaje, tipo);
        return;
    }
    
    // Fallback: crear notificación simple
    const notification = document.createElement('div');
    notification.className = `alert alert-${tipo} position-fixed top-0 start-50 translate-middle-x mt-3`;
    notification.style.zIndex = '9999';
    notification.textContent = mensaje;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Detectar cuando la página vuelve a estar visible
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        console.log('👁️ Página visible nuevamente');
        
        // Verificar si hay sesión activa
        const token = localStorage.getItem('token');
        if (!token) {
            console.warn('⚠️ Sesión perdida, redirigiendo a login');
            window.location.href = '/login';
            return;
        }
        
        // Restaurar estado del formulario si existe
        setTimeout(() => {
            restaurarEstadoFormulario();
        }, 500);
        
        // Recargar datos si la función existe
        if (typeof loadFormularios === 'function') {
            setTimeout(() => {
                loadFormularios();
            }, 1000);
        }
    }
});

// Guardar estado antes de que la página se oculte
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.log('👁️ Página oculta, guardando estado');
        
        // Solo guardar si hay un formulario abierto
        const modal = document.getElementById('formModal');
        if (modal && modal.classList.contains('show')) {
            guardarEstadoFormulario();
        }
    }
});

// Guardar estado periódicamente (cada 30 segundos) si hay formulario abierto
setInterval(() => {
    const modal = document.getElementById('formModal');
    if (modal && modal.classList.contains('show')) {
        // Verificar si hay datos en el formulario
        const totalVotos = document.getElementById('total_votos')?.value;
        if (totalVotos && totalVotos !== '0') {
            guardarEstadoFormulario();
            console.log('💾 Auto-guardado periódico');
        }
    }
}, 30000); // Cada 30 segundos

// Renovar sesión automáticamente cada 30 minutos
setInterval(async () => {
    try {
        const token = localStorage.getItem('token');
        if (token && typeof APIClient !== 'undefined') {
            // Hacer una petición simple para mantener la sesión activa
            await APIClient.getProfile();
            console.log('🔄 Sesión renovada automáticamente');
        }
    } catch (error) {
        console.error('❌ Error al renovar sesión:', error);
    }
}, 30 * 60 * 1000); // Cada 30 minutos

// Interceptar el setupImagePreview para agregar guardado
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Session Fix cargado');
    
    // Esperar a que el DOM esté completamente cargado
    setTimeout(() => {
        const input = document.getElementById('imagen');
        if (input) {
            // Agregar listener adicional para guardar antes de cambiar
            input.addEventListener('click', function() {
                console.log('📸 Input de imagen clickeado, guardando estado...');
                guardarEstadoFormulario();
            });
            
            // Agregar listener para cuando se selecciona archivo
            input.addEventListener('change', function() {
                console.log('📸 Archivo seleccionado');
                // Restaurar estado después de seleccionar imagen
                setTimeout(() => {
                    const savedData = localStorage.getItem('formulario_e14_temp');
                    if (savedData) {
                        console.log('Hay datos guardados, restaurando...');
                        restaurarEstadoFormulario();
                    }
                }, 100);
            });
        }
    }, 1000);
});

// Prevenir pérdida de datos al cerrar/recargar página
window.addEventListener('beforeunload', function(e) {
    const modal = document.getElementById('formModal');
    if (modal && modal.classList.contains('show')) {
        const totalVotos = document.getElementById('total_votos')?.value;
        if (totalVotos && totalVotos !== '0') {
            // Guardar estado
            guardarEstadoFormulario();
            
            // Mostrar advertencia
            e.preventDefault();
            e.returnValue = '¿Está seguro de salir? Hay un formulario sin guardar.';
            return e.returnValue;
        }
    }
});

console.log('✅ Testigo Session Fix v1.0 cargado correctamente');
