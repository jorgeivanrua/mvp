/**
 * Script de limpieza de IndexedDB
 * Ejecutar en la consola del navegador para limpiar reportes problemáticos
 */

async function limpiarReportesProblematicos() {
    console.log('🧹 Iniciando limpieza de reportes problemáticos...');
    
    try {
        // Verificar que IndexedDB esté disponible
        if (!window.indexedDBService || !window.indexedDBService.db) {
            console.error('❌ IndexedDB no está inicializado');
            return;
        }
        
        // Obtener todos los reportes pendientes
        const reportes = await window.indexedDBService.obtenerReportesPendientes();
        console.log(`📊 Total de reportes pendientes: ${reportes.length}`);
        
        if (reportes.length === 0) {
            console.log('✅ No hay reportes pendientes para limpiar');
            return;
        }
        
        let eliminados = 0;
        
        // Eliminar reportes con demasiados intentos o muy antiguos
        for (const reporte of reportes) {
            const demasiadosIntentos = reporte.intentos_sync >= 3;
            const fechaCreacion = new Date(reporte.fecha_creacion_offline);
            const diasDesdeCreacion = (Date.now() - fechaCreacion.getTime()) / (1000 * 60 * 60 * 24);
            const muyAntiguo = diasDesdeCreacion > 7; // Más de 7 días
            
            if (demasiadosIntentos || muyAntiguo) {
                console.log(`🗑️ Eliminando reporte ${reporte.id}:`, {
                    tipo: reporte.tipo,
                    intentos: reporte.intentos_sync,
                    dias: Math.round(diasDesdeCreacion),
                    motivo: demasiadosIntentos ? 'Demasiados intentos' : 'Muy antiguo'
                });
                
                await window.indexedDBService.eliminarReporte(reporte.id);
                eliminados++;
            }
        }
        
        console.log(`✅ Limpieza completada: ${eliminados} reportes eliminados`);
        console.log(`📊 Reportes restantes: ${reportes.length - eliminados}`);
        
        return {
            total: reportes.length,
            eliminados: eliminados,
            restantes: reportes.length - eliminados
        };
        
    } catch (error) {
        console.error('❌ Error durante la limpieza:', error);
        throw error;
    }
}

async function limpiarTodoIndexedDB() {
    console.log('⚠️ ADVERTENCIA: Esto eliminará TODOS los datos de IndexedDB');
    
    if (!confirm('¿Está seguro de que desea eliminar TODOS los datos offline? Esta acción no se puede deshacer.')) {
        console.log('❌ Operación cancelada');
        return;
    }
    
    try {
        const dbName = 'ElectoralSystemDB';
        
        // Cerrar conexión actual
        if (window.indexedDBService && window.indexedDBService.db) {
            window.indexedDBService.db.close();
        }
        
        // Eliminar base de datos
        const request = indexedDB.deleteDatabase(dbName);
        
        request.onsuccess = () => {
            console.log('✅ Base de datos eliminada exitosamente');
            console.log('🔄 Recargue la página para reinicializar IndexedDB');
        };
        
        request.onerror = (event) => {
            console.error('❌ Error eliminando base de datos:', event);
        };
        
        request.onblocked = () => {
            console.warn('⚠️ La eliminación está bloqueada. Cierre todas las pestañas de la aplicación e intente nuevamente.');
        };
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
}

async function verEstadoIndexedDB() {
    console.log('📊 Estado de IndexedDB:');
    console.log('='.repeat(50));
    
    try {
        if (!window.indexedDBService || !window.indexedDBService.db) {
            console.log('❌ IndexedDB no está inicializado');
            return;
        }
        
        // Reportes pendientes
        const reportes = await window.indexedDBService.obtenerReportesPendientes();
        console.log(`\n📋 Reportes pendientes: ${reportes.length}`);
        
        if (reportes.length > 0) {
            const porTipo = {};
            const porIntentos = {};
            
            reportes.forEach(r => {
                // Contar por tipo
                porTipo[r.tipo] = (porTipo[r.tipo] || 0) + 1;
                
                // Contar por intentos
                const intentos = r.intentos_sync || 0;
                porIntentos[intentos] = (porIntentos[intentos] || 0) + 1;
            });
            
            console.log('\n📊 Por tipo:');
            Object.entries(porTipo).forEach(([tipo, count]) => {
                console.log(`  - ${tipo}: ${count}`);
            });
            
            console.log('\n🔄 Por intentos de sincronización:');
            Object.entries(porIntentos).forEach(([intentos, count]) => {
                console.log(`  - ${intentos} intentos: ${count} reportes`);
            });
            
            // Reportes problemáticos
            const problematicos = reportes.filter(r => r.intentos_sync >= 3);
            if (problematicos.length > 0) {
                console.log(`\n⚠️ Reportes problemáticos (3+ intentos): ${problematicos.length}`);
                problematicos.forEach(r => {
                    console.log(`  - ID ${r.id}: ${r.tipo}, ${r.intentos_sync} intentos`);
                });
            }
        }
        
        console.log('\n' + '='.repeat(50));
        console.log('💡 Comandos disponibles:');
        console.log('  - limpiarReportesProblematicos() - Eliminar reportes con errores');
        console.log('  - limpiarTodoIndexedDB() - Eliminar toda la base de datos');
        console.log('  - verEstadoIndexedDB() - Ver este resumen');
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
}

// Exponer funciones globalmente
window.limpiarReportesProblematicos = limpiarReportesProblematicos;
window.limpiarTodoIndexedDB = limpiarTodoIndexedDB;
window.verEstadoIndexedDB = verEstadoIndexedDB;

console.log('🧹 Script de limpieza de IndexedDB cargado');
console.log('💡 Ejecuta verEstadoIndexedDB() para ver el estado actual');
