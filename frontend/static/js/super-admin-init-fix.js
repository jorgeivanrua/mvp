/**
 * Fix de inicialización para Super Admin Dashboard
 * Este archivo sobrescribe las funciones problemáticas
 */

console.log('[Super Admin Init Fix] Cargando correcciones...');

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('[Super Admin Init Fix] DOM listo, aplicando correcciones...');
    
    // Esperar a que APIClient esté disponible
    setTimeout(function() {
        if (typeof APIClient === 'undefined') {
            console.error('[Super Admin Init Fix] APIClient no está definido');
            return;
        }
        
        console.log('[Super Admin Init Fix] APIClient disponible, iniciando carga de datos...');
        
        // Cargar usuarios inmediatamente
        loadUsersFixed();
        
        // Cargar partidos
        loadPartidosFixed();
        
        // Cargar candidatos
        loadCandidatosFixed();
        
        // Cargar tipos de elección
        loadTiposEleccionFixed();
        
    }, 1000);
});

// Función para cargar usuarios
async function loadUsersFixed() {
    try {
        console.log('[Fix] Cargando usuarios...');
        
        const response = await APIClient.get('/super-admin/users');
        console.log('[Fix] Respuesta usuarios:', response);
        
        if (response && response.success && response.data) {
            const users = response.data;
            console.log(`[Fix] ${users.length} usuarios recibidos`);
            
            const tbody = document.getElementById('usersTableBody');
            if (!tbody) {
                console.error('[Fix] No se encontró usersTableBody');
                return;
            }
            
            if (users.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center">No hay usuarios</td></tr>';
                return;
            }
            
            tbody.innerHTML = users.map(user => `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.nombre}</td>
                    <td><span class="badge bg-primary">${user.rol}</span></td>
                    <td>${user.ubicacion_nombre || 'N/A'}</td>
                    <td>••••••••</td>
                    <td><span class="badge ${user.activo ? 'bg-success' : 'bg-danger'}">${user.activo ? 'Activo' : 'Inactivo'}</span></td>
                    <td>${user.ultimo_acceso || 'Nunca'}</td>
                </tr>
            `).join('');
            
            console.log('[Fix] ✓ Usuarios renderizados');
        } else {
            console.error('[Fix] Respuesta inválida:', response);
        }
    } catch (error) {
        console.error('[Fix] Error cargando usuarios:', error);
    }
}

// Función para cargar partidos
async function loadPartidosFixed() {
    try {
        console.log('[Fix] Cargando partidos...');
        
        const response = await APIClient.get('/super-admin/partidos');
        console.log('[Fix] Respuesta partidos:', response);
        
        if (response && response.success && response.data) {
            const partidos = response.data;
            console.log(`[Fix] ${partidos.length} partidos recibidos`);
            
            const container = document.getElementById('partiesList');
            if (!container) {
                console.error('[Fix] No se encontró partiesList');
                return;
            }
            
            if (partidos.length === 0) {
                container.innerHTML = '<p class="text-muted">No hay partidos</p>';
                return;
            }
            
            container.innerHTML = partidos.map(partido => `
                <div class="d-flex justify-content-between align-items-center mb-2 p-2 border-bottom">
                    <div>
                        <h6 class="mb-1">${partido.nombre}</h6>
                        <small class="text-muted">${partido.nombre_corto || ''}</small>
                    </div>
                    <span class="badge ${partido.activo ? 'bg-success' : 'bg-secondary'}">${partido.activo ? 'Activo' : 'Inactivo'}</span>
                </div>
            `).join('');
            
            console.log('[Fix] ✓ Partidos renderizados');
        } else {
            console.error('[Fix] Respuesta inválida:', response);
        }
    } catch (error) {
        console.error('[Fix] Error cargando partidos:', error);
    }
}

// Función para cargar candidatos
async function loadCandidatosFixed() {
    try {
        console.log('[Fix] Cargando candidatos...');
        
        const response = await APIClient.get('/super-admin/candidatos');
        console.log('[Fix] Respuesta candidatos:', response);
        
        if (response && response.success && response.data) {
            const candidatos = response.data;
            console.log(`[Fix] ${candidatos.length} candidatos recibidos`);
            
            const tbody = document.getElementById('candidatesTableBody');
            if (!tbody) {
                console.error('[Fix] No se encontró candidatesTableBody');
                return;
            }
            
            if (candidatos.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay candidatos</td></tr>';
                return;
            }
            
            tbody.innerHTML = candidatos.map(candidato => `
                <tr>
                    <td>${candidato.nombre_completo}</td>
                    <td>${candidato.partido_nombre || 'N/A'}</td>
                    <td>${candidato.tipo_eleccion_nombre || 'N/A'}</td>
                    <td>${candidato.numero_lista || 'N/A'}</td>
                    <td><span class="badge ${candidato.activo ? 'bg-success' : 'bg-secondary'}">${candidato.activo ? 'Activo' : 'Inactivo'}</span></td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="editCandidate(${candidato.id})">
                            <i class="bi bi-pencil"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
            
            console.log('[Fix] ✓ Candidatos renderizados');
        } else {
            console.error('[Fix] Respuesta inválida:', response);
        }
    } catch (error) {
        console.error('[Fix] Error cargando candidatos:', error);
    }
}

// Función para cargar tipos de elección
async function loadTiposEleccionFixed() {
    try {
        console.log('[Fix] Cargando tipos de elección...');
        
        const response = await APIClient.get('/super-admin/tipos-eleccion');
        console.log('[Fix] Respuesta tipos:', response);
        
        if (response && response.success && response.data) {
            const tipos = response.data;
            console.log(`[Fix] ${tipos.length} tipos recibidos`);
            
            const container = document.getElementById('electionTypesList');
            if (!container) {
                console.error('[Fix] No se encontró electionTypesList');
                return;
            }
            
            if (tipos.length === 0) {
                container.innerHTML = '<p class="text-muted">No hay tipos de elección</p>';
                return;
            }
            
            container.innerHTML = tipos.map(tipo => `
                <div class="d-flex justify-content-between align-items-center mb-2 p-2 border-bottom">
                    <h6 class="mb-0">${tipo.nombre}</h6>
                    <span class="badge ${tipo.activo ? 'bg-success' : 'bg-secondary'}">${tipo.activo ? 'Activo' : 'Inactivo'}</span>
                </div>
            `).join('');
            
            console.log('[Fix] ✓ Tipos de elección renderizados');
        } else {
            console.error('[Fix] Respuesta inválida:', response);
        }
    } catch (error) {
        console.error('[Fix] Error cargando tipos de elección:', error);
    }
}

console.log('[Super Admin Init Fix] ✓ Archivo cargado');
