/**
 * Super Admin Dashboard - Enhanced Version
 * Versión optimizada con mejoras de rendimiento
 * 
 * Optimizaciones implementadas:
 * 1. Paginación en tablas grandes
 * 2. Caché de datos frecuentes
 * 3. Lazy loading de imágenes
 * 4. Búsqueda avanzada con filtros
 * 5. Ordenamiento en tablas
 * 
 * Este archivo extiende el dashboard original con optimizaciones
 */

// Managers de optimización
let usersPagination = null;
let usersSearch = null;

// Verificar que las optimizaciones estén cargadas
if (!window.cacheManager) {
    console.error('❌ CacheManager no está cargado');
}
if (!window.lazyLoadManager) {
    console.error('❌ LazyLoadManager no está cargado');
}

console.log('✅ Dashboard Enhanced cargado');

/**
 * Inicializar dashboard con optimizaciones
 */
async function initSuperAdminDashboard() {
    try {
        console.log('🚀 Inicializando Super Admin Dashboard (Enhanced)...');
        
        // Cargar perfil del usuario
        await loadUserProfile();
        
        // Cargar estadísticas principales (con caché)
        await loadMainStatsWithCache();
        
        // Cargar actividad reciente
        await loadRecentActivity();
        
        // Inicializar gráficos
        initCharts();
        
        // Cargar datos iniciales con caché
        await loadUsersWithOptimizations();
        await loadPartidosWithCache();
        await loadTiposEleccionWithCache();
        await loadCandidatosWithCache();
        
        // Auto-refresh cada 30 segundos (solo stats)
        setInterval(() => {
            loadMainStatsWithCache();
            loadRecentActivity();
            updateSystemHealth();
        }, 30000);
        
        console.log('✅ Super Admin Dashboard inicializado correctamente');
        
    } catch (error) {
        console.error('❌ Error inicializando dashboard:', error);
        Utils.showError('Error al cargar el dashboard');
    }
}

/**
 * Cargar estadísticas con caché
 */
async function loadMainStatsWithCache() {
    try {
        // Intentar obtener del caché
        const cached = window.cacheManager.get('main_stats');
        if (cached) {
            updateStatsUI(cached);
            return;
        }

        // Si no hay caché, cargar del servidor
        const response = await APIClient.get('/super-admin/stats');
        
        if (response.success) {
            const stats = response.data;
            
            // Guardar en caché (5 minutos)
            window.cacheManager.set('main_stats', stats, 5 * 60 * 1000);
            
            updateStatsUI(stats);
        }
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
        Utils.showError('Error al cargar estadísticas del sistema');
    }
}

/**
 * Actualizar UI de estadísticas
 */
function updateStatsUI(stats) {
    const elements = {
        totalUsuarios: document.getElementById('totalUsuarios'),
        usuariosChange: document.getElementById('usuariosChange'),
        totalPuestos: document.getElementById('totalPuestos'),
        totalMesas: document.getElementById('totalMesas'),
        totalFormularios: document.getElementById('totalFormularios'),
        formulariosPendientes: document.getElementById('formulariosPendientes'),
        totalValidados: document.getElementById('totalValidados'),
        porcentajeValidados: document.getElementById('porcentajeValidados')
    };

    if (elements.totalUsuarios) elements.totalUsuarios.textContent = Utils.formatNumber(stats.totalUsuarios);
    if (elements.usuariosChange) elements.usuariosChange.textContent = stats.usuariosChange >= 0 ? `+${stats.usuariosChange}` : stats.usuariosChange;
    if (elements.totalPuestos) elements.totalPuestos.textContent = Utils.formatNumber(stats.totalPuestos);
    if (elements.totalMesas) elements.totalMesas.textContent = Utils.formatNumber(stats.totalMesas);
    if (elements.totalFormularios) elements.totalFormularios.textContent = Utils.formatNumber(stats.totalFormularios);
    if (elements.formulariosPendientes) elements.formulariosPendientes.textContent = Utils.formatNumber(stats.formulariosPendientes);
    if (elements.totalValidados) elements.totalValidados.textContent = Utils.formatNumber(stats.totalValidados);
    if (elements.porcentajeValidados) elements.porcentajeValidados.textContent = stats.porcentajeValidados.toFixed(1);
    
    // Actualizar barra de progreso
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = `${stats.porcentajeValidados}%`;
        progressBar.setAttribute('aria-valuenow', stats.porcentajeValidados);
    }
}

/**
 * Cargar usuarios con optimizaciones (paginación + búsqueda + ordenamiento)
 */
async function loadUsersWithOptimizations() {
    try {
        console.log('🔄 Cargando usuarios con optimizaciones...');
        
        // Intentar obtener del caché
        const cached = window.cacheManager.get('users_list');
        if (cached) {
            allUsers = cached;
            initializeUsersOptimizations();
            return;
        }

        const response = await APIClient.get('/super-admin/users');
        
        if (response.success) {
            allUsers = response.data;
            
            // Guardar en caché (3 minutos)
            window.cacheManager.set('users_list', allUsers, 3 * 60 * 1000);
            
            console.log(`✅ ${allUsers.length} usuarios cargados`);
            
            // Inicializar optimizaciones
            initializeUsersOptimizations();
        }
    } catch (error) {
        console.error('❌ Error cargando usuarios:', error);
        Utils.showError('Error al cargar usuarios: ' + error.message);
    }
}

/**
 * Inicializar optimizaciones para tabla de usuarios
 */
function initializeUsersOptimizations() {
    // 1. Inicializar búsqueda avanzada
    usersSearch = new AdvancedSearchManager(allUsers, {
        searchFields: ['nombre', 'rol', 'ubicacion_nombre']
    });

    // 2. Inicializar paginación
    usersPagination = new PaginationManager('usersTableBody', {
        itemsPerPage: 25,
        paginationContainerId: 'usersPagination',
        renderCallback: renderUsersPage
    });

    // 3. Inicializar ordenamiento
    initTableSorting('usersTable', {
        sortableClass: 'sortable'
    });

    // 4. Establecer datos
    usersPagination.setData(allUsers);

    // 5. Crear UI de búsqueda
    createUsersSearchUI();
}

/**
 * Renderizar página de usuarios
 */
function renderUsersPage(users) {
    const tbody = document.getElementById('usersTableBody');
    
    if (!tbody) {
        console.error('❌ Elemento usersTableBody no encontrado');
        return;
    }
    
    if (!users || users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><p class="text-muted">No hay usuarios para mostrar</p></td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td data-sort="${user.id}">${user.id}</td>
            <td data-sort="${user.nombre}"><strong>${user.nombre}</strong></td>
            <td data-sort="${user.rol}"><span class="badge bg-${getRoleBadgeColor(user.rol)}">${user.rol}</span></td>
            <td data-sort="${user.ubicacion_nombre || ''}">${user.ubicacion_nombre || '<span class="text-muted">Sin asignar</span>'}</td>
            <td data-sort="${user.activo ? '1' : '0'}"><span class="badge bg-${user.activo ? 'success' : 'secondary'}">${user.activo ? 'Activo' : 'Inactivo'}</span></td>
            <td data-sort="${user.ultimo_acceso || ''}">${user.ultimo_acceso ? Utils.formatDateTime(user.ultimo_acceso) : '<span class="text-muted">Nunca</span>'}</td>
            <td>
                <div class="btn-group btn-group-sm" role="group">
                    <button class="btn btn-outline-primary" onclick="editUser(${user.id})" title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-warning" onclick="resetUserPassword(${user.id})" title="Resetear contraseña">
                        <i class="bi bi-key"></i>
                    </button>
                    <button class="btn btn-outline-${user.activo ? 'danger' : 'success'}" 
                            onclick="toggleUserStatus(${user.id}, ${!user.activo})" 
                            title="${user.activo ? 'Desactivar' : 'Activar'}">
                        <i class="bi bi-${user.activo ? 'x-circle' : 'check-circle'}"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

/**
 * Crear UI de búsqueda para usuarios
 */
function createUsersSearchUI() {
    const container = document.getElementById('usersSearchContainer');
    if (!container) return;

    container.innerHTML = `
        <div class="row mb-3">
            <div class="col-md-4">
                <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                    <input type="text" class="form-control" id="usersSearchInput" 
                           placeholder="Buscar por nombre, rol o ubicación...">
                </div>
            </div>
            <div class="col-md-2">
                <select class="form-select" id="filterRole">
                    <option value="">Todos los roles</option>
                    <option value="super_admin">Super Admin</option>
                    <option value="auditor">Auditor</option>
                    <option value="coordinador_departamental">Coord. Departamental</option>
                    <option value="coordinador_municipal">Coord. Municipal</option>
                    <option value="coordinador_puesto">Coord. Puesto</option>
                    <option value="testigo">Testigo</option>
                </select>
            </div>
            <div class="col-md-2">
                <select class="form-select" id="filterStatus">
                    <option value="">Todos los estados</option>
                    <option value="activo">Activos</option>
                    <option value="inactivo">Inactivos</option>
                </select>
            </div>
            <div class="col-md-2">
                <select class="form-select" id="usersPerPage">
                    <option value="10">10 por página</option>
                    <option value="25" selected>25 por página</option>
                    <option value="50">50 por página</option>
                    <option value="100">100 por página</option>
                </select>
            </div>
            <div class="col-md-2">
                <button class="btn btn-outline-secondary w-100" onclick="clearUsersFilters()">
                    <i class="bi bi-x-circle"></i> Limpiar
                </button>
            </div>
        </div>
        <div id="usersSearchStats" class="text-muted small mb-2"></div>
    `;

    // Event listeners
    document.getElementById('usersSearchInput').addEventListener('input', filterUsersOptimized);
    document.getElementById('filterRole').addEventListener('change', filterUsersOptimized);
    document.getElementById('filterStatus').addEventListener('change', filterUsersOptimized);
    document.getElementById('usersPerPage').addEventListener('change', (e) => {
        usersPagination.setItemsPerPage(parseInt(e.target.value));
    });
}

/**
 * Filtrar usuarios (optimizado)
 */
function filterUsersOptimized() {
    const searchTerm = document.getElementById('usersSearchInput')?.value.toLowerCase() || '';
    const role = document.getElementById('filterRole')?.value || '';
    const status = document.getElementById('filterStatus')?.value || '';

    // Configurar búsqueda
    usersSearch.setSearchTerm(searchTerm);
    usersSearch.clearFilters();

    if (role) {
        usersSearch.addFilter('rol', role);
    }

    if (status) {
        usersSearch.addFilter('activo', status === 'activo');
    }

    // Ejecutar búsqueda
    const results = usersSearch.search();

    // Actualizar paginación con resultados
    usersPagination.setData(results);

    // Actualizar estadísticas
    updateUsersSearchStats(results.length, allUsers.length);
}

/**
 * Actualizar estadísticas de búsqueda
 */
function updateUsersSearchStats(filtered, total) {
    const statsContainer = document.getElementById('usersSearchStats');
    if (statsContainer) {
        const percentage = ((filtered / total) * 100).toFixed(1);
        statsContainer.innerHTML = `
            <i class="bi bi-info-circle"></i> 
            Mostrando ${filtered} de ${total} usuarios (${percentage}%)
        `;
    }
}

/**
 * Limpiar filtros de usuarios
 */
function clearUsersFilters() {
    document.getElementById('usersSearchInput').value = '';
    document.getElementById('filterRole').value = '';
    document.getElementById('filterStatus').value = '';
    filterUsersOptimized();
}

/**
 * Cargar partidos con caché
 */
async function loadPartidosWithCache() {
    try {
        const cached = window.cacheManager.get('partidos_list');
        if (cached) {
            allPartidos = cached;
            renderPartidos();
            return;
        }

        const response = await APIClient.getPartidos();
        
        if (response.success) {
            allPartidos = response.data;
            window.cacheManager.set('partidos_list', allPartidos, 10 * 60 * 1000); // 10 minutos
            renderPartidos();
        }
    } catch (error) {
        console.error('Error cargando partidos:', error);
    }
}

/**
 * Cargar tipos de elección con caché
 */
async function loadTiposEleccionWithCache() {
    try {
        const cached = window.cacheManager.get('tipos_eleccion_list');
        if (cached) {
            allTiposEleccion = cached;
            renderTiposEleccion();
            return;
        }

        const response = await APIClient.getTiposEleccion();
        
        if (response.success) {
            allTiposEleccion = response.data;
            window.cacheManager.set('tipos_eleccion_list', allTiposEleccion, 10 * 60 * 1000);
            renderTiposEleccion();
        }
    } catch (error) {
        console.error('Error cargando tipos de elección:', error);
    }
}

/**
 * Cargar candidatos con caché
 */
async function loadCandidatosWithCache() {
    try {
        const cached = window.cacheManager.get('candidatos_list');
        if (cached) {
            allCandidatos = cached;
            renderCandidatos();
            return;
        }

        const response = await APIClient.getCandidatos();
        
        if (response.success) {
            allCandidatos = response.data;
            window.cacheManager.set('candidatos_list', allCandidatos, 10 * 60 * 1000);
            renderCandidatos();
        }
    } catch (error) {
        console.error('Error cargando candidatos:', error);
    }
}

/**
 * Invalidar caché cuando se crean/actualizan datos
 */
function invalidateCache(type) {
    switch(type) {
        case 'users':
            window.cacheManager.delete('users_list');
            break;
        case 'partidos':
            window.cacheManager.delete('partidos_list');
            break;
        case 'candidatos':
            window.cacheManager.delete('candidatos_list');
            break;
        case 'tipos_eleccion':
            window.cacheManager.delete('tipos_eleccion_list');
            break;
        case 'stats':
            window.cacheManager.delete('main_stats');
            break;
        case 'all':
            window.cacheManager.clear();
            break;
    }
}

// Exportar funciones para uso global
window.initSuperAdminDashboard = initSuperAdminDashboard;
window.filterUsersOptimized = filterUsersOptimized;
window.clearUsersFilters = clearUsersFilters;
window.invalidateCache = invalidateCache;


/**
 * Hook para interceptar loadUsers original y agregar optimizaciones
 */
(function() {
    // Guardar referencia a la función original si existe
    const originalLoadUsers = window.loadUsers;
    
    // Sobrescribir con versión optimizada
    window.loadUsers = async function() {
        try {
            console.log('🔄 Cargando usuarios con optimizaciones...');
            
            // Intentar obtener del caché
            const cached = window.cacheManager ? window.cacheManager.get('users_list') : null;
            if (cached) {
                window.allUsers = cached;
                console.log('✅ Usuarios cargados desde caché');
                initializeUsersOptimizations();
                return;
            }
            
            // Si no hay caché, llamar a la función original o cargar del servidor
            if (originalLoadUsers) {
                await originalLoadUsers();
            } else {
                const response = await APIClient.get('/super-admin/users');
                if (response.success) {
                    window.allUsers = response.data;
                }
            }
            
            // Guardar en caché
            if (window.cacheManager && window.allUsers) {
                window.cacheManager.set('users_list', window.allUsers, 3 * 60 * 1000);
            }
            
            // Inicializar optimizaciones
            initializeUsersOptimizations();
            
        } catch (error) {
            console.error('❌ Error cargando usuarios:', error);
            Utils.showError('Error al cargar usuarios: ' + error.message);
        }
    };
    
    console.log('✅ loadUsers optimizado instalado');
})();

/**
 * Hook para interceptar renderUsers y usar paginación
 */
(function() {
    const originalRenderUsers = window.renderUsers;
    
    window.renderUsers = function(users) {
        // Si hay paginación activa, usar renderUsersPage
        if (usersPagination) {
            usersPagination.setData(users || window.allUsers || []);
        } else if (originalRenderUsers) {
            originalRenderUsers(users);
        }
    };
    
    console.log('✅ renderUsers optimizado instalado');
})();

/**
 * Hook para invalidar caché al crear/editar/eliminar usuarios
 */
(function() {
    // Guardar funciones originales
    const originalGuardarNuevoUsuario = window.guardarNuevoUsuario;
    const originalGuardarEdicionUser = window.guardarEdicionUser;
    const originalToggleUserStatus = window.toggleUserStatus;
    
    // Sobrescribir guardarNuevoUsuario
    if (originalGuardarNuevoUsuario) {
        window.guardarNuevoUsuario = async function() {
            const result = await originalGuardarNuevoUsuario.apply(this, arguments);
            if (window.cacheManager) {
                window.cacheManager.delete('users_list');
            }
            return result;
        };
    }
    
    // Sobrescribir guardarEdicionUser
    if (originalGuardarEdicionUser) {
        window.guardarEdicionUser = async function() {
            const result = await originalGuardarEdicionUser.apply(this, arguments);
            if (window.cacheManager) {
                window.cacheManager.delete('users_list');
            }
            return result;
        };
    }
    
    // Sobrescribir toggleUserStatus
    if (originalToggleUserStatus) {
        window.toggleUserStatus = async function() {
            const result = await originalToggleUserStatus.apply(this, arguments);
            if (window.cacheManager) {
                window.cacheManager.delete('users_list');
            }
            return result;
        };
    }
    
    console.log('✅ Hooks de invalidación de caché instalados');
})();

/**
 * Inicializar optimizaciones cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando optimizaciones del dashboard...');
    
    // Esperar un momento para que el dashboard original se inicialice
    setTimeout(() => {
        // Verificar si hay usuarios cargados
        if (window.allUsers && window.allUsers.length > 0) {
            initializeUsersOptimizations();
        }
    }, 1000);
});

console.log('✅ Super Admin Dashboard Enhanced completamente cargado');
