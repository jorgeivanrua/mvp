/**
 * Script de debug para verificar carga de usuarios
 */

console.log('=== DEBUG USUARIOS V2 ===');

// Verificar que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM listo');
    
    // Verificar elementos clave
    const tbody = document.getElementById('usersTableBody');
    console.log('usersTableBody encontrado:', !!tbody);
    
    const usersTab = document.getElementById('users');
    console.log('Tab users encontrado:', !!usersTab);
    
    // Verificar si hay datos globales
    setTimeout(() => {
        console.log('window.allUsers:', window.allUsers);
        console.log('Cantidad de usuarios:', window.allUsers ? window.allUsers.length : 0);
        
        // Verificar si renderUsers está disponible
        console.log('window.renderUsers disponible:', typeof window.renderUsers);
        
        // Si hay usuarios pero no se ven, intentar re-renderizar
        if (window.allUsers && window.allUsers.length > 0 && tbody) {
            console.log('Intentando re-renderizar usuarios...');
            if (typeof window.renderUsers === 'function') {
                window.renderUsers(window.allUsers);
                console.log('Re-renderizado completado');
            }
        }
    }, 2000);
});

// Agregar listener para cuando se cambie a la pestaña de usuarios
document.addEventListener('shown.bs.tab', function(e) {
    if (e.target.id === 'users-tab') {
        console.log('Pestaña de usuarios activada');
        const tbody = document.getElementById('usersTableBody');
        if (tbody) {
            console.log('Contenido actual del tbody:', tbody.innerHTML.substring(0, 200));
        }
    }
});
