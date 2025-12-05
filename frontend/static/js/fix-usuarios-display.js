/**
 * Fix temporal para forzar la visualización de usuarios
 */

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('[Fix Display] Aplicando correcciones de visualización...');
    
    // Agregar event listener al botón de usuarios
    const usersTabButton = document.querySelector('[data-bs-target="#users"]');
    if (usersTabButton) {
        usersTabButton.addEventListener('shown.bs.tab', function() {
            console.log('[Fix Display] Pestaña de usuarios mostrada');
            
            // Forzar re-render
            if (typeof window.renderUsers === 'function' && window.allUsers) {
                console.log('[Fix Display] Forzando re-render de usuarios...');
                window.renderUsers(window.allUsers);
            }
            
            // Verificar visibilidad
            const usersTab = document.getElementById('users');
            const tbody = document.getElementById('usersTableBody');
            const chartCard = document.querySelector('#users .chart-card');
            
            console.log('[Fix Display] Estado de elementos:');
            console.log('  - usersTab display:', window.getComputedStyle(usersTab).display);
            console.log('  - tbody visible:', tbody.offsetParent !== null);
            console.log('  - chartCard height:', chartCard ? chartCard.offsetHeight : 'N/A');
            
            // Forzar estilos si es necesario
            if (chartCard && chartCard.offsetHeight === 0) {
                console.log('[Fix Display] Forzando altura mínima...');
                chartCard.style.minHeight = '500px';
            }
        });
        
        console.log('[Fix Display] Event listener agregado al botón de usuarios');
    } else {
        console.error('[Fix Display] No se encontró el botón de usuarios');
    }
});

// También agregar un fix global para cuando se cambie de tab
document.addEventListener('shown.bs.tab', function(e) {
    if (e.target.getAttribute('data-bs-target') === '#users') {
        console.log('[Fix Display] Tab de usuarios activado via evento global');
        
        setTimeout(() => {
            if (typeof window.renderUsers === 'function' && window.allUsers && window.allUsers.length > 0) {
                console.log('[Fix Display] Re-renderizando usuarios después de cambio de tab');
                window.renderUsers(window.allUsers);
            }
        }, 100);
    }
});
