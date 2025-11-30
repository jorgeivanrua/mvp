/**
 * Script de debugging para Testigo Dashboard
 */

console.log('[Testigo Debug] Script cargado');

// Verificar dependencias
if (typeof APIClient === 'undefined') {
    console.error('[Testigo Debug] ❌ APIClient no está definido');
} else {
    console.log('[Testigo Debug] ✓ APIClient disponible');
}

const token = localStorage.getItem('access_token');
if (!token) {
    console.error('[Testigo Debug] ❌ No hay token de acceso');
} else {
    console.log('[Testigo Debug] ✓ Token encontrado');
}

// Función de prueba completa
window.testTestigoDashboard = async function() {
    console.log('[Testigo Debug] === INICIANDO PRUEBA COMPLETA ===');
    
    try {
        // 1. Verificar perfil
        console.log('[Testigo Debug] 1. Verificando perfil...');
        const profileResponse = await APIClient.getProfile();
        console.log('[Testigo Debug] Perfil:', profileResponse);
        
        if (!profileResponse.success) {
            console.error('[Testigo Debug] ❌ Error en perfil:', profileResponse.error);
            return;
        }
        
        const user = profileResponse.data.user;
        console.log('[Testigo Debug] Usuario:', user.nombre, '- Rol:', user.rol);
        
        if (user.rol !== 'testigo_electoral') {
            console.error('[Testigo Debug] ❌ Usuario no es testigo_electoral');
            return;
        }
        
        // 2. Verificar tipos de elección
        console.log('[Testigo Debug] 2. Cargando tipos de elección...');
        const tiposResponse = await APIClient.getTiposEleccion();
        console.log('[Testigo Debug] Tipos de elección:', tiposResponse);
        
        if (tiposResponse && tiposResponse.success && tiposResponse.data) {
            console.log('[Testigo Debug] ✓ Tipos de elección:', tiposResponse.data.length);
            tiposResponse.data.forEach(tipo => {
                console.log(`[Testigo Debug]   - ${tipo.nombre} (ID: ${tipo.id})`);
            });
        } else {
            console.warn('[Testigo Debug] ⚠️ No se pudieron cargar tipos de elección');
        }
        
        // 3. Verificar partidos
        console.log('[Testigo Debug] 3. Cargando partidos...');
        const partidosResponse = await APIClient.getPartidos();
        console.log('[Testigo Debug] Partidos:', partidosResponse);
        
        if (partidosResponse && partidosResponse.success && partidosResponse.data) {
            console.log('[Testigo Debug] ✓ Partidos:', partidosResponse.data.length);
            partidosResponse.data.slice(0, 5).forEach(partido => {
                console.log(`[Testigo Debug]   - ${partido.nombre_corto}`);
            });
        } else {
            console.warn('[Testigo Debug] ⚠️ No se pudieron cargar partidos');
        }
        
        // 4. Verificar mesas
        console.log('[Testigo Debug] 4. Verificando mesas...');
        const mesaSelector = document.getElementById('mesa');
        if (mesaSelector) {
            console.log('[Testigo Debug] ✓ Selector de mesa encontrado');
            console.log('[Testigo Debug]   Opciones:', mesaSelector.options.length);
        } else {
            console.warn('[Testigo Debug] ⚠️ Selector de mesa no encontrado');
        }
        
        // 5. Verificar estado de presencia
        console.log('[Testigo Debug] 5. Verificando presencia...');
        console.log('[Testigo Debug]   presenciaVerificada:', window.presenciaVerificada);
        console.log('[Testigo Debug]   mesaSeleccionadaDashboard:', window.mesaSeleccionadaDashboard);
        
        // 6. Verificar botones
        console.log('[Testigo Debug] 6. Verificando botones...');
        const btnNuevoFormulario = document.getElementById('btnNuevoFormulario');
        const btnNuevoFormularioMobile = document.getElementById('btnNuevoFormularioMobile');
        
        if (btnNuevoFormulario) {
            console.log('[Testigo Debug] ✓ Botón desktop encontrado');
            console.log('[Testigo Debug]   Disabled:', btnNuevoFormulario.disabled);
            console.log('[Testigo Debug]   Classes:', btnNuevoFormulario.className);
        } else {
            console.warn('[Testigo Debug] ⚠️ Botón desktop no encontrado');
        }
        
        if (btnNuevoFormularioMobile) {
            console.log('[Testigo Debug] ✓ Botón móvil encontrado');
            console.log('[Testigo Debug]   Disabled:', btnNuevoFormularioMobile.disabled);
        } else {
            console.warn('[Testigo Debug] ⚠️ Botón móvil no encontrado');
        }
        
        // 7. Verificar formularios
        console.log('[Testigo Debug] 7. Cargando formularios...');
        try {
            const formsResponse = await APIClient.getFormulariosE14();
            console.log('[Testigo Debug] Formularios:', formsResponse);
            
            if (formsResponse && formsResponse.success) {
                console.log('[Testigo Debug] ✓ Formularios cargados:', formsResponse.data?.length || 0);
            }
        } catch (error) {
            console.warn('[Testigo Debug] ⚠️ Error cargando formularios:', error.message);
        }
        
        // 8. Verificar funciones de incidentes/delitos
        console.log('[Testigo Debug] 8. Verificando funciones de incidentes/delitos...');
        console.log('[Testigo Debug]   reportarIncidente:', typeof window.reportarIncidente);
        console.log('[Testigo Debug]   reportarDelito:', typeof window.reportarDelito);
        console.log('[Testigo Debug]   initIncidentesDelitos:', typeof window.initIncidentesDelitos);
        
        console.log('[Testigo Debug] === PRUEBA COMPLETADA ===');
        
    } catch (error) {
        console.error('[Testigo Debug] ❌ Error en prueba:', error);
        console.error('[Testigo Debug] Stack:', error.stack);
    }
};

// Ejecutar automáticamente
setTimeout(() => {
    console.log('[Testigo Debug] Ejecutando prueba automática...');
    window.testTestigoDashboard();
}, 2000);

console.log('[Testigo Debug] Para ejecutar manualmente: testTestigoDashboard()');
