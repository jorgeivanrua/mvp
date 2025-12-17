/**
 * Utilidad para limpiar cache del navegador y datos obsoletos
 */

class CacheCleaner {
    constructor() {
        this.version = '2024.12.14.001'; // Versión actual del sistema
        this.storageKey = 'app_version';
    }

    /**
     * Verificar si necesita limpiar cache por cambio de versión
     */
    checkAndCleanIfNeeded() {
        const storedVersion = localStorage.getItem(this.storageKey);
        
        if (storedVersion !== this.version) {
            console.log('🧹 Detectado cambio de versión, limpiando cache...');
            console.log(`   Versión anterior: ${storedVersion || 'ninguna'}`);
            console.log(`   Versión actual: ${this.version}`);
            
            this.cleanAll();
            localStorage.setItem(this.storageKey, this.version);
            
            console.log('✅ Cache limpiado exitosamente');
            return true;
        }
        
        return false;
    }

    /**
     * Limpiar todos los datos de cache
     */
    cleanAll() {
        // Limpiar localStorage (excepto tokens de autenticación)
        this.cleanLocalStorage();
        
        // Limpiar sessionStorage
        this.cleanSessionStorage();
        
        // Limpiar cache del navegador si está disponible
        this.cleanBrowserCache();
    }

    /**
     * Limpiar localStorage manteniendo datos críticos
     */
    cleanLocalStorage() {
        const keysToKeep = [
            'access_token',
            'refresh_token',
            'user_id',
            this.storageKey
        ];
        
        const keysToRemove = [];
        
        // Identificar claves a eliminar
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && !keysToKeep.includes(key)) {
                keysToRemove.push(key);
            }
        }
        
        // Eliminar claves identificadas
        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
            console.log(`   Eliminado de localStorage: ${key}`);
        });
    }

    /**
     * Limpiar sessionStorage
     */
    cleanSessionStorage() {
        const keysToRemove = [];
        
        for (let i = 0; i < sessionStorage.length; i++) {
            const key = sessionStorage.key(i);
            if (key) {
                keysToRemove.push(key);
            }
        }
        
        keysToRemove.forEach(key => {
            sessionStorage.removeItem(key);
            console.log(`   Eliminado de sessionStorage: ${key}`);
        });
    }

    /**
     * Limpiar cache del navegador
     */
    async cleanBrowserCache() {
        try {
            if ('caches' in window) {
                const cacheNames = await caches.keys();
                await Promise.all(
                    cacheNames.map(cacheName => {
                        console.log(`   Eliminando cache: ${cacheName}`);
                        return caches.delete(cacheName);
                    })
                );
            }
        } catch (error) {
            console.warn('No se pudo limpiar cache del navegador:', error);
        }
    }

    /**
     * Limpiar datos específicos de ubicación obsoletos
     */
    cleanLocationData() {
        const locationKeys = [
            'userLocation',
            'currentLocation',
            'mesaSeleccionada',
            'mesaVerificada',
            'presenciaVerificada',
            'mesaVerificadaId',
            'mesaVerificadaData',
            'ubicacionCache',
            'departamentoCache',
            'municipioCache',
            'puestoCache'
        ];
        
        locationKeys.forEach(key => {
            localStorage.removeItem(key);
            sessionStorage.removeItem(key);
        });
        
        console.log('🗺️ Datos de ubicación limpiados');
    }

    /**
     * Forzar recarga completa de la página
     */
    forceReload() {
        console.log('🔄 Forzando recarga completa...');
        
        // Limpiar cache antes de recargar
        this.cleanAll();
        
        // Recargar sin cache
        if (window.location.reload) {
            window.location.reload(true); // true = bypass cache
        } else {
            window.location.href = window.location.href;
        }
    }

    /**
     * Mostrar información de debug sobre el cache
     */
    debugInfo() {
        console.log('🔍 Información de Cache:');
        console.log(`   Versión actual: ${this.version}`);
        console.log(`   Versión almacenada: ${localStorage.getItem(this.storageKey)}`);
        console.log(`   localStorage items: ${localStorage.length}`);
        console.log(`   sessionStorage items: ${sessionStorage.length}`);
        
        // Mostrar claves de localStorage
        console.log('   localStorage keys:');
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            console.log(`     - ${key}`);
        }
    }
}

// Crear instancia global
window.cacheCleaner = new CacheCleaner();

// Auto-limpiar al cargar si es necesario
document.addEventListener('DOMContentLoaded', function() {
    window.cacheCleaner.checkAndCleanIfNeeded();
});

// Función global para limpiar manualmente
window.limpiarCacheCompleto = function() {
    if (confirm('¿Está seguro de que desea limpiar todo el cache?\n\nEsto eliminará datos temporales y puede requerir volver a iniciar sesión.')) {
        window.cacheCleaner.forceReload();
    }
};

// Función específica para limpiar datos de ubicación
window.limpiarDatosUbicacion = function() {
    window.cacheCleaner.cleanLocationData();
    
    // Recargar perfil de usuario
    if (window.loadUserProfile && typeof window.loadUserProfile === 'function') {
        window.loadUserProfile();
    }
    
    console.log('✅ Datos de ubicación limpiados y perfil recargado');
};