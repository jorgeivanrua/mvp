/**
 * Script para forzar actualización de datos de ubicación en el dashboard del testigo
 */

/**
 * Forzar recarga completa del perfil de usuario y ubicación
 */
async function forzarActualizacionUbicacion() {
    try {
        console.log('🔄 Forzando actualización de ubicación...');
        
        // Limpiar datos de ubicación del cache
        if (window.cacheCleaner) {
            window.cacheCleaner.cleanLocationData();
        }
        
        // Limpiar variables globales
        window.currentUser = null;
        window.userLocation = null;
        window.mesaSeleccionadaDashboard = null;
        window.presenciaVerificada = false;
        
        // Mostrar indicador de carga
        const mesaInfo = document.getElementById('mesaInfo');
        if (mesaInfo) {
            mesaInfo.textContent = 'Actualizando ubicación...';
        }
        
        // Recargar perfil desde el servidor
        const response = await APIClient.getProfile();
        
        if (response.success) {
            console.log('✅ Perfil actualizado:', response.data);
            
            // Actualizar variables globales
            window.currentUser = response.data.user;
            window.userLocation = response.data.ubicacion;
            
            // Mostrar información actualizada
            if (window.userLocation) {
                console.log('📍 Nueva ubicación:', window.userLocation);
                
                if (mesaInfo) {
                    mesaInfo.textContent = `${window.userLocation.departamento_nombre} - ${window.userLocation.municipio_nombre}`;
                }
                
                // Recargar mesas si es necesario
                if (window.loadMesas && typeof window.loadMesas === 'function') {
                    await window.loadMesas();
                }
                
                // Actualizar panel de mesas
                if (window.actualizarPanelMesas && typeof window.actualizarPanelMesas === 'function') {
                    await window.actualizarPanelMesas();
                }
            }
            
            // Mostrar mensaje de éxito
            if (window.Utils && window.Utils.showSuccess) {
                window.Utils.showSuccess('Ubicación actualizada correctamente');
            } else {
                alert('Ubicación actualizada correctamente');
            }
            
        } else {
            throw new Error(response.error || 'Error al obtener perfil');
        }
        
    } catch (error) {
        console.error('❌ Error al actualizar ubicación:', error);
        
        if (window.Utils && window.Utils.showError) {
            window.Utils.showError('Error al actualizar ubicación: ' + error.message);
        } else {
            alert('Error al actualizar ubicación: ' + error.message);
        }
    }
}

/**
 * Verificar y mostrar información de debug sobre la ubicación actual
 */
function debugUbicacionActual() {
    console.log('🔍 DEBUG - Información de Ubicación:');
    console.log('  currentUser:', window.currentUser);
    console.log('  userLocation:', window.userLocation);
    console.log('  mesaSeleccionadaDashboard:', window.mesaSeleccionadaDashboard);
    console.log('  presenciaVerificada:', window.presenciaVerificada);
    
    // Verificar localStorage
    console.log('  localStorage presenciaVerificada:', localStorage.getItem('presenciaVerificada'));
    console.log('  localStorage mesaVerificadaData:', localStorage.getItem('mesaVerificadaData'));
    
    // Verificar elementos del DOM
    const mesaInfo = document.getElementById('mesaInfo');
    console.log('  mesaInfo element:', mesaInfo);
    console.log('  mesaInfo text:', mesaInfo?.textContent);
    
    // Verificar selector de mesa
    const mesaSelector = document.getElementById('mesa');
    console.log('  mesa selector:', mesaSelector);
    console.log('  mesa selector value:', mesaSelector?.value);
    console.log('  mesa selector options:', mesaSelector?.options?.length);
}

// Hacer funciones disponibles globalmente
window.forzarActualizacionUbicacion = forzarActualizacionUbicacion;
window.debugUbicacionActual = debugUbicacionActual;

// Agregar función mejorada para limpiar datos de ubicación
window.limpiarDatosUbicacionMejorado = async function() {
    if (confirm('¿Desea limpiar los datos de ubicación y recargar desde el servidor?\n\nEsto puede ayudar a resolver problemas de ubicación incorrecta.')) {
        await forzarActualizacionUbicacion();
    }
};

// Auto-ejecutar verificación al cargar
document.addEventListener('DOMContentLoaded', function() {
    // Esperar un poco para que se carguen otros scripts
    setTimeout(() => {
        // Solo ejecutar si hay problemas evidentes
        if (window.userLocation && window.userLocation.departamento_nombre === 'CAQUETA') {
            console.warn('⚠️ Detectado departamento CAQUETA, puede ser datos obsoletos');
            console.log('💡 Ejecute forzarActualizacionUbicacion() para actualizar');
        }
    }, 2000);
});