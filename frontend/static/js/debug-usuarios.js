/**
 * Script de depuración para verificar el estado de la tabla de usuarios
 */

console.log('=== DEBUG USUARIOS ===');

// Verificar que el elemento existe
const tbody = document.getElementById('usersTableBody');
console.log('1. Elemento usersTableBody:', tbody);

if (tbody) {
    console.log('2. Contenido HTML del tbody:', tbody.innerHTML.substring(0, 200));
    console.log('3. Número de filas:', tbody.querySelectorAll('tr').length);
    console.log('4. Visible:', tbody.offsetParent !== null);
    console.log('5. Display:', window.getComputedStyle(tbody).display);
    
    // Verificar el contenedor padre
    const table = tbody.closest('table');
    console.log('6. Tabla padre:', table);
    if (table) {
        console.log('7. Tabla visible:', table.offsetParent !== null);
        console.log('8. Tabla display:', window.getComputedStyle(table).display);
    }
    
    // Verificar el tab
    const usersTab = document.getElementById('users');
    console.log('9. Tab de usuarios:', usersTab);
    if (usersTab) {
        console.log('10. Tab activo:', usersTab.classList.contains('active'));
        console.log('11. Tab show:', usersTab.classList.contains('show'));
        console.log('12. Tab display:', window.getComputedStyle(usersTab).display);
    }
}

// Verificar datos globales
console.log('13. allUsers:', window.allUsers ? window.allUsers.length : 'undefined');

// Función para forzar re-render
window.debugForceRenderUsers = function() {
    console.log('=== FORZANDO RE-RENDER ===');
    if (typeof renderUsers === 'function' && window.allUsers) {
        renderUsers(window.allUsers);
        console.log('Re-render completado');
    } else {
        console.error('No se puede hacer re-render:', {
            renderUsers: typeof renderUsers,
            allUsers: window.allUsers ? 'existe' : 'no existe'
        });
    }
};

console.log('=== FIN DEBUG ===');
console.log('Para forzar re-render, ejecuta: debugForceRenderUsers()');
