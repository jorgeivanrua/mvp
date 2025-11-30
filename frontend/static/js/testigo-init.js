/**
 * Inicialización del Dashboard de Testigo
 * Coordina la inicialización de todos los módulos
 */

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('[Testigo Init] Inicializando dashboard de testigo...');
    
    // Inicializar módulos en orden
    initializeTestigoDashboard();
});

/**
 * Inicializar todos los módulos del dashboard
 */
async function initializeTestigoDashboard() {
    try {
        // 1. Inicializar incidentes y delitos
        if (typeof initIncidentesDelitos === 'function') {
            console.log('[Testigo Init] Inicializando módulo de incidentes y delitos...');
            await initIncidentesDelitos();
        } else {
            console.warn('[Testigo Init] Módulo de incidentes y delitos no disponible');
        }
        
        // 2. Cargar datos iniciales si hay funciones disponibles
        if (typeof cargarMesas === 'function') {
            console.log('[Testigo Init] Cargando mesas...');
            await cargarMesas();
        }
        
        if (typeof cargarTiposEleccion === 'function') {
            console.log('[Testigo Init] Cargando tipos de elección...');
            await cargarTiposEleccion();
        }
        
        // 3. Actualizar estadísticas
        if (typeof actualizarEstadisticas === 'function') {
            console.log('[Testigo Init] Actualizando estadísticas...');
            actualizarEstadisticas();
        }
        
        console.log('[Testigo Init] ✓ Dashboard inicializado correctamente');
        
    } catch (error) {
        console.error('[Testigo Init] Error inicializando dashboard:', error);
        if (typeof Utils !== 'undefined' && typeof Utils.showError === 'function') {
            Utils.showError('Error inicializando el dashboard. Por favor, recargue la página.');
        }
    }
}

// Exponer función globalmente
window.initializeTestigoDashboard = initializeTestigoDashboard;
