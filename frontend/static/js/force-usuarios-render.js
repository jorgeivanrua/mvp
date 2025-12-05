/**
 * Script para forzar renderizado de usuarios
 */

console.log('🔧 [Force Render] Script cargado');

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 [Force Render] DOM listo');
    
    // Esperar 3 segundos para que todo se cargue
    setTimeout(() => {
        console.log('🔧 [Force Render] Intentando forzar renderizado...');
        
        // Verificar si hay usuarios cargados
        if (window.allUsers && window.allUsers.length > 0) {
            console.log(`🔧 [Force Render] Encontrados ${window.allUsers.length} usuarios`);
            
            // Buscar el tbody
            const tbody = document.getElementById('usuarios-lista');
            if (tbody) {
                console.log('🔧 [Force Render] Elemento usuarios-lista encontrado');
                console.log('🔧 [Force Render] Contenido actual:', tbody.innerHTML.substring(0, 100));
                
                // Si está vacío o solo tiene el spinner, forzar renderizado
                if (tbody.children.length <= 1 || tbody.innerHTML.includes('spinner-border')) {
                    console.log('🔧 [Force Render] Forzando renderizado manual...');
                    
                    // Renderizar manualmente
                    const html = window.allUsers.map(user => {
                        return `
                            <tr>
                                <td>${user.id}</td>
                                <td><strong>${user.nombre}</strong></td>
                                <td><span class="badge bg-primary">${user.rol}</span></td>
                                <td>${user.ubicacion_nombre || 'Sin asignar'}</td>
                                <td><span class="badge bg-${user.activo ? 'success' : 'secondary'}">${user.activo ? 'Activo' : 'Inactivo'}</span></td>
                                <td><small>${user.ultimo_acceso || 'Nunca'}</small></td>
                                <td class="text-center">
                                    <button class="btn btn-sm btn-outline-primary">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                </td>
                            </tr>
                        `;
                    }).join('');
                    
                    tbody.innerHTML = html;
                    console.log('🔧 [Force Render] ✅ Renderizado forzado completado');
                    
                    // Actualizar contador
                    const counter = document.getElementById('usuarios-count');
                    if (counter) {
                        counter.textContent = window.allUsers.length;
                        console.log('🔧 [Force Render] ✅ Contador actualizado');
                    }
                } else {
                    console.log('🔧 [Force Render] ℹ️ Ya hay contenido en la tabla');
                }
            } else {
                console.error('🔧 [Force Render] ❌ Elemento usuarios-lista NO encontrado');
            }
        } else {
            console.warn('🔧 [Force Render] ⚠️ No hay usuarios cargados en window.allUsers');
        }
    }, 3000);
});

// También intentar cuando se active la pestaña de usuarios
document.addEventListener('shown.bs.tab', function(e) {
    if (e.target.id === 'users-tab') {
        console.log('🔧 [Force Render] Pestaña de usuarios activada');
        
        setTimeout(() => {
            const tbody = document.getElementById('usuarios-lista');
            if (tbody && window.allUsers && window.allUsers.length > 0) {
                if (tbody.children.length <= 1 || tbody.innerHTML.includes('spinner-border')) {
                    console.log('🔧 [Force Render] Forzando renderizado al activar pestaña...');
                    
                    const html = window.allUsers.map(user => {
                        return `
                            <tr>
                                <td>${user.id}</td>
                                <td><strong>${user.nombre}</strong></td>
                                <td><span class="badge bg-primary">${user.rol}</span></td>
                                <td>${user.ubicacion_nombre || 'Sin asignar'}</td>
                                <td><span class="badge bg-${user.activo ? 'success' : 'secondary'}">${user.activo ? 'Activo' : 'Inactivo'}</span></td>
                                <td><small>${user.ultimo_acceso || 'Nunca'}</small></td>
                                <td class="text-center">
                                    <button class="btn btn-sm btn-outline-primary">
                                        <i class="bi bi-pencil"></i>
                                    </button>
                                </td>
                            </tr>
                        `;
                    }).join('');
                    
                    tbody.innerHTML = html;
                    
                    const counter = document.getElementById('usuarios-count');
                    if (counter) counter.textContent = window.allUsers.length;
                    
                    console.log('🔧 [Force Render] ✅ Renderizado forzado en activación de pestaña');
                }
            }
        }, 500);
    }
});
