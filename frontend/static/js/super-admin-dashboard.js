/**
 * Dashboard Super Admin
 * Gestión completa del sistema electoral
 */

let currentUser = null;
let allUsers = [];
let allPartidos = [];
let allCandidatos = [];
let allTiposEleccion = [];
let charts = {};

/**
 * Inicializar dashboard
 */
async function initSuperAdminDashboard() {
    try {
        console.log('Inicializando Super Admin Dashboard...');
        
        // Cargar perfil del usuario
        await loadUserProfile();
        
        // Cargar estadísticas principales
        await loadMainStats();
        
        // Cargar actividad reciente
        await loadRecentActivity();
        
        // Inicializar gráficos
        initCharts();
        
        // Cargar datos iniciales
        await loadUsers();
        await loadPartidos();
        await loadTiposEleccion();
        await loadCandidatos();
        await loadCampanas();
        
        // Auto-refresh cada 30 segundos
        setInterval(() => {
            loadMainStats();
            loadRecentActivity();
            updateSystemHealth();
        }, 30000);
        
        console.log('Super Admin Dashboard inicializado correctamente');
        
    } catch (error) {
        console.error('Error inicializando dashboard:', error);
        Utils.showError('Error al cargar el dashboard');
    }
}

/**
 * Cargar perfil del usuario
 */
async function loadUserProfile() {
    try {
        const response = await APIClient.getProfile();
        
        if (response.success) {
            currentUser = response.data.user;
            
            document.getElementById('userInfo').innerHTML = `
                <strong>${currentUser.nombre}</strong> • Super Administrador
                <br><small>Acceso completo al sistema</small>
            `;
        }
    } catch (error) {
        console.error('Error cargando perfil:', error);
    }
}

/**
 * Cargar estadísticas principales
 */
async function loadMainStats() {
    try {
        const response = await APIClient.get('/super-admin/stats');
        
        if (response.success) {
            const stats = response.data;
            
            // Actualizar UI
            document.getElementById('totalUsuarios').textContent = Utils.formatNumber(stats.totalUsuarios);
            document.getElementById('usuariosChange').textContent = stats.usuariosChange >= 0 ? `+${stats.usuariosChange}` : stats.usuariosChange;
            document.getElementById('totalPuestos').textContent = Utils.formatNumber(stats.totalPuestos);
            document.getElementById('totalMesas').textContent = Utils.formatNumber(stats.totalMesas);
            document.getElementById('totalFormularios').textContent = Utils.formatNumber(stats.totalFormularios);
            document.getElementById('formulariosPendientes').textContent = Utils.formatNumber(stats.formulariosPendientes);
            document.getElementById('totalValidados').textContent = Utils.formatNumber(stats.totalValidados);
            document.getElementById('porcentajeValidados').textContent = stats.porcentajeValidados.toFixed(1);
            
            // Actualizar barra de progreso
            const progressBar = document.querySelector('.progress-bar');
            if (progressBar) {
                progressBar.style.width = `${stats.porcentajeValidados}%`;
                progressBar.setAttribute('aria-valuenow', stats.porcentajeValidados);
            }
        }
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
        Utils.showError('Error al cargar estadísticas del sistema');
    }
}

/**
 * Cargar actividad reciente
 */
async function loadRecentActivity() {
    try {
        // TODO: Implementar endpoint real de actividad
        const container = document.getElementById('recentActivity');
        
        const activities = [
            {
                user: 'Juan Pérez',
                action: 'Creó formulario E-14',
                time: '5 min ago',
                icon: 'file-earmark-text',
                color: 'primary'
            },
            {
                user: 'María García',
                action: 'Validó formulario',
                time: '10 min ago',
                icon: 'check-circle',
                color: 'success'
            },
            {
                user: 'Carlos López',
                action: 'Reportó incidente',
                time: '15 min ago',
                icon: 'exclamation-triangle',
                color: 'warning'
            }
        ];
        
        container.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="d-flex align-items-center">
                    <div class="me-3">
                        <i class="bi bi-${activity.icon} text-${activity.color}" style="font-size: 1.5rem;"></i>
                    </div>
                    <div class="flex-grow-1">
                        <strong>${activity.user}</strong>
                        <br><small class="text-muted">${activity.action}</small>
                    </div>
                    <div>
                        <small class="text-muted">${activity.time}</small>
                    </div>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error cargando actividad:', error);
    }
}

/**
 * Actualizar estado de salud del sistema
 */
async function updateSystemHealth() {
    try {
        const response = await APIClient.get('/super-admin/system-health');
        
        if (response.success) {
            const health = response.data;
            const indicator = document.getElementById('systemHealthIndicator');
            const text = document.getElementById('systemHealthText');
            
            // Actualizar indicador visual
            indicator.className = 'health-indicator';
            if (health.status === 'healthy') {
                indicator.classList.add('health-good');
                text.textContent = 'Sistema operando normalmente';
            } else if (health.status === 'warning') {
                indicator.classList.add('health-warning');
                text.textContent = 'Sistema con advertencias';
            } else {
                indicator.classList.add('health-critical');
                text.textContent = 'Sistema con problemas críticos';
            }
            
            // Actualizar métricas detalladas si existen
            const cpuElement = document.getElementById('cpuUsage');
            const memoryElement = document.getElementById('memoryUsage');
            const dbElement = document.getElementById('dbStatus');
            
            if (cpuElement) cpuElement.textContent = `${health.cpu_percent.toFixed(1)}%`;
            if (memoryElement) memoryElement.textContent = `${health.memory_percent.toFixed(1)}%`;
            if (dbElement) {
                dbElement.textContent = health.database === 'healthy' ? 'Conectada' : 'Desconectada';
                dbElement.className = health.database === 'healthy' ? 'text-success' : 'text-danger';
            }
        }
    } catch (error) {
        console.error('Error actualizando salud del sistema:', error);
        const indicator = document.getElementById('systemHealthIndicator');
        const text = document.getElementById('systemHealthText');
        if (indicator && text) {
            indicator.className = 'health-indicator health-critical';
            text.textContent = 'Error al verificar estado del sistema';
        }
    }
}

/**
 * Inicializar gráficos
 */
function initCharts() {
    // Destruir gráficos existentes antes de crear nuevos
    if (charts.progress) {
        charts.progress.destroy();
    }
    if (charts.activity) {
        charts.activity.destroy();
    }
    
    // Gráfico de progreso nacional
    const progressCtx = document.getElementById('progressChart');
    if (progressCtx) {
        charts.progress = new Chart(progressCtx, {
            type: 'bar',
            data: {
                labels: ['Departamento 1', 'Departamento 2', 'Departamento 3', 'Departamento 4', 'Departamento 5'],
                datasets: [{
                    label: 'Formularios Validados',
                    data: [65, 59, 80, 81, 56],
                    backgroundColor: 'rgba(42, 82, 152, 0.8)',
                    borderColor: 'rgba(42, 82, 152, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Gráfico de actividad
    const activityCtx = document.getElementById('activityChart');
    if (activityCtx) {
        charts.activity = new Chart(activityCtx, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
                datasets: [{
                    label: 'Formularios Creados',
                    data: [12, 19, 3, 5, 2, 3, 7],
                    borderColor: 'rgba(42, 82, 152, 1)',
                    backgroundColor: 'rgba(42, 82, 152, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// ============================================
// GESTIÓN DE USUARIOS
// ============================================

/**
 * Cargar usuarios
 */
async function loadUsers() {
    try {
        const response = await APIClient.get('/super-admin/users');
        
        if (response.success) {
            allUsers = response.data;
            renderUsers(allUsers);
        }
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        Utils.showError('Error al cargar usuarios');
    }
}

/**
 * Renderizar tabla de usuarios
 */
function renderUsers(users) {
    const tbody = document.getElementById('usersTableBody');
    
    if (!users || users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><p class="text-muted">No hay usuarios para mostrar</p></td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.id}</td>
            <td>${user.nombre}</td>
            <td><span class="badge bg-${getRoleBadgeColor(user.rol)}">${user.rol}</span></td>
            <td>${user.ubicacion_nombre || 'N/A'}</td>
            <td><span class="badge bg-${user.activo ? 'success' : 'secondary'}">${user.activo ? 'Activo' : 'Inactivo'}</span></td>
            <td>${user.ultimo_acceso ? Utils.formatDateTime(user.ultimo_acceso) : 'Nunca'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editUser(${user.id})" title="Editar">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-warning" onclick="resetUserPassword(${user.id})" title="Resetear contraseña">
                    <i class="bi bi-key"></i>
                </button>
                <button class="btn btn-sm btn-${user.activo ? 'danger' : 'success'}" 
                        onclick="toggleUserStatus(${user.id}, ${!user.activo})" 
                        title="${user.activo ? 'Desactivar' : 'Activar'}">
                    <i class="bi bi-${user.activo ? 'x-circle' : 'check-circle'}"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

/**
 * Obtener color de badge según rol
 */
function getRoleBadgeColor(rol) {
    const colors = {
        'super_admin': 'dark',
        'auditor': 'info',
        'coordinador_departamental': 'primary',
        'coordinador_municipal': 'primary',
        'coordinador_puesto': 'success',
        'testigo': 'warning'
    };
    return colors[rol] || 'secondary';
}

/**
 * Filtrar usuarios
 */
function filterUsers() {
    const role = document.getElementById('filterRole')?.value || '';
    const status = document.getElementById('filterStatus')?.value || '';
    const search = document.getElementById('searchUser')?.value.toLowerCase() || '';
    
    let filtered = allUsers;
    
    // Filtrar por rol
    if (role) {
        filtered = filtered.filter(user => user.rol === role);
    }
    
    // Filtrar por estado
    if (status) {
        const isActive = status === 'activo';
        filtered = filtered.filter(user => user.activo === isActive);
    }
    
    // Filtrar por búsqueda
    if (search) {
        filtered = filtered.filter(user => 
            user.nombre.toLowerCase().includes(search) ||
            (user.ubicacion_nombre && user.ubicacion_nombre.toLowerCase().includes(search))
        );
    }
    
    renderUsers(filtered);
}

/**
 * Mostrar modal de crear usuario
 */
function showCreateUserModal() {
    // Crear modal dinámicamente
    const modalHtml = `
        <div class="modal fade" id="createUserModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Crear Nuevo Usuario</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="createUserForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nombre *</label>
                                    <input type="text" class="form-control" id="userName" required>
                                    <small class="text-muted">Nombre de usuario para login</small>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Rol *</label>
                                    <select class="form-select" id="userRole" required>
                                        <option value="">Seleccione...</option>
                                        <option value="super_admin">Super Admin</option>
                                        <option value="admin_departamental">Admin Departamental</option>
                                        <option value="admin_municipal">Admin Municipal</option>
                                        <option value="coordinador_departamental">Coordinador Departamental</option>
                                        <option value="coordinador_municipal">Coordinador Municipal</option>
                                        <option value="coordinador_puesto">Coordinador de Puesto</option>
                                        <option value="testigo_electoral">Testigo Electoral</option>
                                        <option value="auditor_electoral">Auditor Electoral</option>
                                    </select>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Contraseña *</label>
                                    <input type="password" class="form-control" id="userPassword" required>
                                    <small class="text-muted">Mínimo 6 caracteres</small>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Confirmar Contraseña *</label>
                                    <input type="password" class="form-control" id="userPasswordConfirm" required>
                                </div>
                            </div>
                            <div class="alert alert-info">
                                <i class="bi bi-info-circle"></i>
                                <strong>Nota:</strong> La ubicación se asignará según el rol seleccionado.
                                Para roles que requieren ubicación específica, use la gestión de usuarios avanzada.
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarNuevoUsuario()">Crear Usuario</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Agregar modal al DOM si no existe
    if (!document.getElementById('createUserModal')) {
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('createUserModal'));
    modal.show();
}

/**
 * Guardar nuevo usuario
 */
async function guardarNuevoUsuario() {
    const nombre = document.getElementById('userName').value.trim();
    const rol = document.getElementById('userRole').value;
    const password = document.getElementById('userPassword').value;
    const passwordConfirm = document.getElementById('userPasswordConfirm').value;
    
    // Validaciones
    if (!nombre || !rol || !password) {
        Utils.showError('Todos los campos son requeridos');
        return;
    }
    
    if (password.length < 6) {
        Utils.showError('La contraseña debe tener al menos 6 caracteres');
        return;
    }
    
    if (password !== passwordConfirm) {
        Utils.showError('Las contraseñas no coinciden');
        return;
    }
    
    try {
        Utils.showInfo('Creando usuario...');
        
        const response = await APIClient.post('/super-admin/users', {
            nombre: nombre,
            rol: rol,
            password: password,
            activo: true
        });
        
        if (response.success) {
            Utils.showSuccess('Usuario creado exitosamente');
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('createUserModal'));
            modal.hide();
            
            // Recargar lista de usuarios
            await loadUsers();
        } else {
            Utils.showError(response.error || 'Error al crear usuario');
        }
    } catch (error) {
        console.error('Error creando usuario:', error);
        Utils.showError('Error al crear usuario: ' + error.message);
    }
}

/**
 * Editar usuario
 */
async function editUser(userId) {
    try {
        const user = allUsers.find(u => u.id === userId);
        if (!user) {
            Utils.showError('Usuario no encontrado');
            return;
        }
        
        Utils.showInfo(`Editar usuario: ${user.nombre} (en desarrollo)`);
        // TODO: Implementar modal de edición
    } catch (error) {
        console.error('Error editando usuario:', error);
        Utils.showError('Error al editar usuario');
    }
}

/**
 * Resetear contraseña de usuario
 */
async function resetUserPassword(userId) {
    try {
        const user = allUsers.find(u => u.id === userId);
        if (!user) {
            Utils.showError('Usuario no encontrado');
            return;
        }
        
        const newPassword = prompt(`Ingrese nueva contraseña para ${user.nombre}:`);
        if (!newPassword) return;
        
        if (newPassword.length < 6) {
            Utils.showError('La contraseña debe tener al menos 6 caracteres');
            return;
        }
        
        const response = await APIClient.post(`/super-admin/users/${userId}/reset-password`, {
            password: newPassword
        });
        
        if (response.success) {
            Utils.showSuccess('Contraseña reseteada exitosamente');
        } else {
            Utils.showError(response.error || 'Error al resetear contraseña');
        }
    } catch (error) {
        console.error('Error reseteando contraseña:', error);
        Utils.showError('Error al resetear contraseña');
    }
}

/**
 * Cambiar estado de usuario (activar/desactivar)
 */
async function toggleUserStatus(userId, newStatus) {
    try {
        const user = allUsers.find(u => u.id === userId);
        if (!user) {
            Utils.showError('Usuario no encontrado');
            return;
        }
        
        const action = newStatus ? 'activar' : 'desactivar';
        if (!confirm(`¿Está seguro de ${action} al usuario ${user.nombre}?`)) {
            return;
        }
        
        const response = await APIClient.put(`/super-admin/users/${userId}`, {
            activo: newStatus
        });
        
        if (response.success) {
            Utils.showSuccess(`Usuario ${action}do exitosamente`);
            await loadUsers(); // Recargar lista
        } else {
            Utils.showError(response.error || `Error al ${action} usuario`);
        }
    } catch (error) {
        console.error('Error cambiando estado de usuario:', error);
        Utils.showError('Error al cambiar estado del usuario');
    }
}

// ============================================
// CONFIGURACIÓN
// ============================================

/**
 * Cargar partidos
 */
async function loadPartidos() {
    try {
        const response = await APIClient.getPartidos();
        
        if (response.success) {
            allPartidos = response.data;
            renderPartidos();
        }
    } catch (error) {
        console.error('Error cargando partidos:', error);
    }
}

/**
 * Renderizar partidos
 */
function renderPartidos() {
    const container = document.getElementById('partiesList');
    
    if (allPartidos.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay partidos registrados</p>';
        return;
    }
    
    container.innerHTML = allPartidos.map(partido => `
        <div class="d-flex align-items-center justify-content-between mb-2 p-2 border rounded ${!partido.activo ? 'opacity-50' : ''}">
            <div class="d-flex align-items-center flex-grow-1">
                <div style="width: 30px; height: 30px; background-color: ${partido.color}; border-radius: 4px; margin-right: 10px;"></div>
                <div>
                    <strong>${partido.nombre}</strong>
                    <br><small class="text-muted">${partido.nombre_corto || partido.sigla}</small>
                    ${!partido.activo ? '<br><span class="badge bg-secondary">Deshabilitado</span>' : '<br><span class="badge bg-success">Habilitado</span>'}
                </div>
            </div>
            <div class="d-flex gap-1">
                <button class="btn btn-sm btn-${partido.activo ? 'warning' : 'success'}" 
                        onclick="togglePartido(${partido.id}, ${!partido.activo})"
                        title="${partido.activo ? 'Deshabilitar' : 'Habilitar'}">
                    <i class="bi bi-${partido.activo ? 'toggle-on' : 'toggle-off'}"></i>
                </button>
                <button class="btn btn-sm btn-outline-primary" onclick="editPartido(${partido.id})">
                    <i class="bi bi-pencil"></i>
                </button>
            </div>
        </div>
    `).join('');
}

/**
 * Cargar tipos de elección
 */
async function loadTiposEleccion() {
    try {
        const response = await APIClient.getTiposEleccion();
        
        if (response.success) {
            allTiposEleccion = response.data;
            renderTiposEleccion();
        }
    } catch (error) {
        console.error('Error cargando tipos de elección:', error);
    }
}

/**
 * Renderizar tipos de elección
 */
function renderTiposEleccion() {
    const container = document.getElementById('electionTypesList');
    
    if (allTiposEleccion.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay tipos de elección registrados</p>';
        return;
    }
    
    container.innerHTML = allTiposEleccion.map(tipo => {
        let detalles = [];
        if (tipo.es_uninominal) {
            detalles.push('Uninominal');
        } else {
            if (tipo.permite_lista_cerrada) detalles.push('Lista cerrada');
            if (tipo.permite_lista_abierta) detalles.push('Lista abierta');
            if (tipo.permite_coaliciones) detalles.push('Coaliciones');
        }
        
        return `
            <div class="d-flex align-items-center justify-content-between mb-2 p-2 border rounded ${!tipo.activo ? 'opacity-50' : ''}">
                <div class="flex-grow-1">
                    <strong>${tipo.nombre}</strong>
                    <br><small class="text-muted">${detalles.join(' • ')}</small>
                    ${!tipo.activo ? '<br><span class="badge bg-secondary">Deshabilitado</span>' : '<br><span class="badge bg-success">Habilitado</span>'}
                </div>
                <div class="d-flex gap-1">
                    <button class="btn btn-sm btn-${tipo.activo ? 'warning' : 'success'}" 
                            onclick="toggleTipoEleccion(${tipo.id}, ${!tipo.activo})"
                            title="${tipo.activo ? 'Deshabilitar' : 'Habilitar'}">
                        <i class="bi bi-${tipo.activo ? 'toggle-on' : 'toggle-off'}"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-info" onclick="verDetallesTipo(${tipo.id})" title="Ver detalles">
                        <i class="bi bi-info-circle"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-primary" onclick="editTipoEleccion(${tipo.id})">
                        <i class="bi bi-pencil"></i>
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Ver detalles de un tipo de elección
 */
function verDetallesTipo(tipoId) {
    const tipo = allTiposEleccion.find(t => t.id === tipoId);
    if (!tipo) return;
    
    let detallesHtml = `
        <p><strong>Nombre:</strong> ${tipo.nombre}</p>
        <p><strong>Descripción:</strong> ${tipo.descripcion || 'N/A'}</p>
        <p><strong>Tipo:</strong> ${tipo.es_uninominal ? 'Uninominal (candidato único)' : 'Por corporación (listas)'}</p>
    `;
    
    if (!tipo.es_uninominal) {
        detallesHtml += `
            <p><strong>Configuración de listas:</strong></p>
            <ul>
                <li>Lista cerrada: ${tipo.permite_lista_cerrada ? '✅ Sí' : '❌ No'}</li>
                <li>Lista abierta (voto preferente): ${tipo.permite_lista_abierta ? '✅ Sí' : '❌ No'}</li>
                <li>Coaliciones: ${tipo.permite_coaliciones ? '✅ Sí' : '❌ No'}</li>
            </ul>
        `;
    }
    
    detallesHtml += `<p><strong>Estado:</strong> ${tipo.activo ? '<span class="badge bg-success">Habilitado</span>' : '<span class="badge bg-secondary">Deshabilitado</span>'}</p>`;
    
    const modalHtml = `
        <div class="modal fade" id="detallesTipoModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Detalles del Tipo de Elección</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${detallesHtml}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('detallesTipoModal'));
    modal.show();
    
    document.getElementById('detallesTipoModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Cargar candidatos
 */
async function loadCandidatos() {
    try {
        const response = await APIClient.getCandidatos();
        
        if (response.success) {
            allCandidatos = response.data;
            renderCandidatos();
        }
    } catch (error) {
        console.error('Error cargando candidatos:', error);
    }
}

/**
 * Renderizar candidatos
 */
function renderCandidatos() {
    const tbody = document.getElementById('candidatesTableBody');
    
    if (allCandidatos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><p class="text-muted">No hay candidatos registrados</p></td></tr>';
        return;
    }
    
    tbody.innerHTML = allCandidatos.map(candidato => `
        <tr class="${!candidato.activo ? 'opacity-50' : ''}">
            <td>${candidato.nombre_completo || candidato.nombre}</td>
            <td>${candidato.partido_nombre || 'Independiente'}</td>
            <td>${candidato.tipo_eleccion_nombre || 'N/A'}</td>
            <td>${candidato.numero_lista || '-'}</td>
            <td><span class="badge bg-${candidato.activo ? 'success' : 'secondary'}">${candidato.activo ? 'Habilitado' : 'Deshabilitado'}</span></td>
            <td>
                <button class="btn btn-sm btn-${candidato.activo ? 'warning' : 'success'}" 
                        onclick="toggleCandidato(${candidato.id}, ${!candidato.activo})"
                        title="${candidato.activo ? 'Deshabilitar' : 'Habilitar'}">
                    <i class="bi bi-${candidato.activo ? 'toggle-on' : 'toggle-off'}"></i>
                </button>
                <button class="btn btn-sm btn-outline-primary" onclick="editCandidato(${candidato.id})">
                    <i class="bi bi-pencil"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// ============================================
// ACCIONES RÁPIDAS
// ============================================

/**
 * Mostrar modal de configuración
 */
function showConfigModal() {
    alert('🔧 CONFIGURACIÓN DEL SISTEMA\n\n' +
          'Esta funcionalidad permite configurar:\n' +
          '- Parámetros generales del sistema\n' +
          '- Configuración de notificaciones\n' +
          '- Ajustes de seguridad\n\n' +
          '📝 Estado: En desarrollo\n' +
          '🎯 Disponible en: Próxima versión');
}

/**
 * Exportar todos los datos
 */
async function exportAllData() {
    alert('📥 EXPORTAR DATOS\n\n' +
          'Esta funcionalidad permite exportar:\n' +
          '- Todos los usuarios del sistema\n' +
          '- Formularios E-14 enviados\n' +
          '- Ubicaciones y mesas\n\n' +
          '📝 Estado: En desarrollo\n' +
          '🎯 Disponible en: Próxima versión');
}

/**
 * Crear respaldo
 */
async function createBackup() {
    alert('💾 CREAR RESPALDO\n\n' +
          'Esta funcionalidad permite:\n' +
          '- Crear backup completo de la BD\n' +
          '- Descargar respaldo en formato SQL\n\n' +
          '📝 Estado: En desarrollo\n' +
          '⚠️ Render hace respaldos automáticos de PostgreSQL');
}
}

/**
 * Exportar logs de auditoría
 */
function exportAuditLogs() {
    Utils.showInfo('Exportando logs de auditoría...');
    // TODO: Implementar exportación de logs
}

/**
 * Filtrar logs de auditoría
 */
function filterAuditLogs() {
    const user = document.getElementById('auditFilterUser').value;
    const action = document.getElementById('auditFilterAction').value;
    const date = document.getElementById('auditFilterDate').value;
    
    console.log('Filtrando logs:', { user, action, date });
    // TODO: Implementar filtrado real
}

// ============================================
// FUNCIONES DE EDICIÓN
// ============================================

function editPartido(id) {
    Utils.showInfo('Funcionalidad de edición en desarrollo');
}

function editTipoEleccion(id) {
    Utils.showInfo('Funcionalidad de edición en desarrollo');
}

function editCandidato(id) {
    Utils.showInfo('Funcionalidad de edición en desarrollo');
}

function showCreatePartyModal() {
    Utils.showInfo('Funcionalidad en desarrollo');
}

function showCreateElectionTypeModal() {
    Utils.showInfo('Funcionalidad en desarrollo');
}

function showCreateCandidateModal() {
    Utils.showInfo('Funcionalidad en desarrollo');
}

// ============================================
// FUNCIÓN DE LOGOUT
// ============================================

async function logout() {
    try {
        await APIClient.logout();
    } catch (error) {
        console.error('Error during logout:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
        window.location.href = '/auth/login';
    }
}


// ============================================
// CARGA MASIVA DE DATOS
// ============================================

/**
 * Cargar usuarios desde archivo Excel
 */
async function uploadUsers(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        Utils.showInfo('Cargando usuarios...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/super-admin/upload/users', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showUploadResult(result, 'success');
            await loadUsers(); // Recargar lista de usuarios
        } else {
            showUploadResult(result, 'danger');
        }
        
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        Utils.showError('Error al cargar usuarios: ' + error.message);
    } finally {
        input.value = ''; // Limpiar input
    }
}

/**
 * Cargar ubicaciones (DIVIPOLA) desde archivo Excel
 */
async function uploadLocations(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        Utils.showInfo('Cargando ubicaciones...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/super-admin/upload/locations', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showUploadResult(result, 'success');
        } else {
            showUploadResult(result, 'danger');
        }
        
    } catch (error) {
        console.error('Error cargando ubicaciones:', error);
        Utils.showError('Error al cargar ubicaciones: ' + error.message);
    } finally {
        input.value = ''; // Limpiar input
    }
}

/**
 * Cargar partidos desde archivo Excel
 */
async function uploadPartidos(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        Utils.showInfo('Cargando partidos...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/super-admin/upload/partidos', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showUploadResult(result, 'success');
            await loadPartidos(); // Recargar lista de partidos
        } else {
            showUploadResult(result, 'danger');
        }
        
    } catch (error) {
        console.error('Error cargando partidos:', error);
        Utils.showError('Error al cargar partidos: ' + error.message);
    } finally {
        input.value = ''; // Limpiar input
    }
}

/**
 * Cargar candidatos desde archivo Excel
 */
async function uploadCandidatos(input) {
    const file = input.files[0];
    if (!file) return;
    
    try {
        Utils.showInfo('Cargando candidatos...');
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/super-admin/upload/candidatos', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showUploadResult(result, 'success');
            await loadCandidatos(); // Recargar lista de candidatos
        } else {
            showUploadResult(result, 'danger');
        }
        
    } catch (error) {
        console.error('Error cargando candidatos:', error);
        Utils.showError('Error al cargar candidatos: ' + error.message);
    } finally {
        input.value = ''; // Limpiar input
    }
}

/**
 * Mostrar resultado de carga masiva
 */
function showUploadResult(result, type) {
    const resultDiv = document.getElementById('uploadResult');
    const contentDiv = document.getElementById('uploadResultContent');
    
    if (!resultDiv || !contentDiv) return;
    
    let html = '';
    
    if (result.success && result.data) {
        html = `
            <p class="mb-2"><strong>${result.message}</strong></p>
            <ul class="mb-0">
                <li>Total procesados: ${result.data.total_processed}</li>
                <li>Creados exitosamente: ${result.data.total_created}</li>
                <li>Errores: ${result.data.total_errors}</li>
            </ul>
        `;
        
        if (result.data.errors && result.data.errors.length > 0) {
            html += `
                <hr>
                <p class="mb-2"><strong>Errores encontrados:</strong></p>
                <ul class="small mb-0" style="max-height: 200px; overflow-y: auto;">
                    ${result.data.errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
            `;
        }
    } else {
        html = `<p class="mb-0"><strong>Error:</strong> ${result.error || 'Error desconocido'}</p>`;
    }
    
    contentDiv.innerHTML = html;
    resultDiv.querySelector('.alert').className = `alert alert-${type}`;
    resultDiv.style.display = 'block';
    
    // Auto-ocultar después de 10 segundos si es exitoso
    if (type === 'success') {
        setTimeout(() => {
            resultDiv.style.display = 'none';
        }, 10000);
    }
}

/**
 * Descargar plantilla de usuarios (Excel con datos de ejemplo)
 */
async function downloadTemplateUsers() {
    try {
        const response = await fetch('/api/super-admin/download/template/users', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plantilla_usuarios.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            Utils.showSuccess('Plantilla de usuarios descargada con datos de ejemplo');
        } else {
            Utils.showError('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla: ' + error.message);
    }
}

/**
 * Descargar plantilla de ubicaciones (Excel con datos de ejemplo)
 */
async function downloadTemplateLocations() {
    try {
        const response = await fetch('/api/super-admin/download/template/locations', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plantilla_divipola.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            Utils.showSuccess('Plantilla de DIVIPOLA descargada con datos de ejemplo');
        } else {
            Utils.showError('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla: ' + error.message);
    }
}

/**
 * Descargar plantilla de partidos (Excel con datos de ejemplo)
 */
async function downloadTemplatePartidos() {
    try {
        const response = await fetch('/api/super-admin/download/template/partidos', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plantilla_partidos.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            Utils.showSuccess('Plantilla de partidos descargada con datos de ejemplo');
        } else {
            Utils.showError('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla: ' + error.message);
    }
}

/**
 * Descargar plantilla de candidatos (Excel con datos de ejemplo)
 */
async function downloadTemplateCandidatos() {
    try {
        const response = await fetch('/api/super-admin/download/template/candidatos', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plantilla_candidatos.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            Utils.showSuccess('Plantilla de candidatos descargada con datos de ejemplo');
        } else {
            Utils.showError('Error al descargar plantilla');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al descargar plantilla: ' + error.message);
    }
}

/**
 * Función auxiliar para descargar CSV
 */
function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


// ============================================
// GESTIÓN DE HABILITACIÓN
// ============================================

/**
 * Habilitar/Deshabilitar tipo de elección
 */
async function toggleTipoEleccion(tipoId, activo) {
    try {
        const response = await APIClient.put(`/super-admin/tipos-eleccion/${tipoId}`, {
            activo: activo
        });
        
        if (response.success) {
            Utils.showSuccess(`Tipo de elección ${activo ? 'habilitado' : 'deshabilitado'} exitosamente`);
            await loadTiposEleccion();
        } else {
            Utils.showError(response.error || 'Error al actualizar tipo de elección');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar tipo de elección');
    }
}

/**
 * Habilitar/Deshabilitar partido
 */
async function togglePartido(partidoId, activo) {
    try {
        const response = await APIClient.put(`/super-admin/partidos/${partidoId}/toggle`, {
            activo: activo
        });
        
        if (response.success) {
            Utils.showSuccess(`Partido ${activo ? 'habilitado' : 'deshabilitado'} para recolección de datos`);
            await loadPartidos();
        } else {
            Utils.showError(response.error || 'Error al actualizar partido');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar partido');
    }
}

/**
 * Habilitar/Deshabilitar candidato
 */
async function toggleCandidato(candidatoId, activo) {
    try {
        const response = await APIClient.put(`/super-admin/candidatos/${candidatoId}/toggle`, {
            activo: activo
        });
        
        if (response.success) {
            Utils.showSuccess(`Candidato ${activo ? 'habilitado' : 'deshabilitado'} para recolección de datos`);
            await loadCandidatos();
        } else {
            Utils.showError(response.error || 'Error al actualizar candidato');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar candidato');
    }
}

/**
 * Crear nuevo tipo de elección
 */
async function createTipoEleccion() {
    // Mostrar modal personalizado
    const modalHtml = `
        <div class="modal fade" id="createTipoEleccionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Crear Tipo de Elección</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Nombre *</label>
                            <input type="text" class="form-control" id="tipoNombre" placeholder="Ej: Presidente, Senado, Cámara">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Descripción</label>
                            <textarea class="form-control" id="tipoDescripcion" rows="2"></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Elección</label>
                            <select class="form-select" id="tipoCategoria">
                                <option value="uninominal">Uninominal (Presidente, Gobernador, Alcalde)</option>
                                <option value="corporacion">Por Corporación (Senado, Cámara, Asamblea, Concejo)</option>
                            </select>
                        </div>
                        <div id="opcionesLista" style="display:none;">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="listaC errada" checked>
                                <label class="form-check-label" for="listaCerrada">
                                    Permite lista cerrada
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="listaAbierta">
                                <label class="form-check-label" for="listaAbierta">
                                    Permite lista abierta (voto preferente)
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="coaliciones">
                                <label class="form-check-label" for="coaliciones">
                                    Permite coaliciones
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarTipoEleccion()">Crear</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Agregar modal al DOM
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('createTipoEleccionModal'));
    
    // Manejar cambio de categoría
    document.getElementById('tipoCategoria').addEventListener('change', function() {
        const opcionesLista = document.getElementById('opcionesLista');
        opcionesLista.style.display = this.value === 'corporacion' ? 'block' : 'none';
    });
    
    modal.show();
    
    // Limpiar modal al cerrar
    document.getElementById('createTipoEleccionModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar nuevo tipo de elección
 */
async function guardarTipoEleccion() {
    const nombre = document.getElementById('tipoNombre').value.trim();
    const descripcion = document.getElementById('tipoDescripcion').value.trim();
    const categoria = document.getElementById('tipoCategoria').value;
    
    if (!nombre) {
        Utils.showError('El nombre es requerido');
        return;
    }
    
    const esUninominal = categoria === 'uninominal';
    const listaCerrada = !esUninominal && document.getElementById('listaCerrada').checked;
    const listaAbierta = !esUninominal && document.getElementById('listaAbierta').checked;
    const coaliciones = !esUninominal && document.getElementById('coaliciones').checked;
    
    try {
        const response = await APIClient.post('/super-admin/tipos-eleccion', {
            nombre: nombre,
            descripcion: descripcion,
            es_uninominal: esUninominal,
            permite_lista_cerrada: listaCerrada,
            permite_lista_abierta: listaAbierta,
            permite_coaliciones: coaliciones,
            activo: true
        });
        
        if (response.success) {
            Utils.showSuccess('Tipo de elección creado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('createTipoEleccionModal')).hide();
            await loadTiposEleccion();
        } else {
            Utils.showError(response.error || 'Error al crear tipo de elección');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al crear tipo de elección');
    }
}


// ============================================
// GESTIÓN DE CAMPAÑAS
// ============================================

let allCampanas = [];
let allTemas = [];

/**
 * Cargar campañas
 */
async function loadCampanas() {
    try {
        const response = await APIClient.get('/super-admin/campanas');
        
        if (response.success) {
            allCampanas = response.data;
            renderCampanas();
        }
    } catch (error) {
        console.error('Error cargando campañas:', error);
        Utils.showError('Error al cargar campañas');
    }
}

/**
 * Renderizar campañas
 */
function renderCampanas() {
    const container = document.getElementById('campanasContainer');
    
    if (!allCampanas || allCampanas.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No hay campañas registradas</p>';
        return;
    }
    
    container.innerHTML = allCampanas.map(campana => `
        <div class="card mb-3 ${campana.activa ? 'border-success' : ''}">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h6 class="card-title">
                            ${campana.nombre}
                            ${campana.activa ? '<span class="badge bg-success ms-2">ACTIVA</span>' : ''}
                            ${campana.completada ? '<span class="badge bg-secondary ms-2">Completada</span>' : ''}
                        </h6>
                        <p class="card-text text-muted small">${campana.descripcion || 'Sin descripción'}</p>
                        <div class="d-flex gap-2 align-items-center">
                            <span class="badge" style="background-color: ${campana.color_primario}">Color Primario</span>
                            <span class="badge" style="background-color: ${campana.color_secundario}">Color Secundario</span>
                            ${campana.es_candidato_unico ? '<span class="badge bg-info">Candidato Único</span>' : ''}
                            ${campana.es_partido_completo ? '<span class="badge bg-warning">Partido Completo</span>' : ''}
                        </div>
                    </div>
                    <div class="btn-group-vertical">
                        ${!campana.activa ? `
                            <button class="btn btn-sm btn-success" onclick="activarCampana(${campana.id})" title="Activar campaña">
                                <i class="bi bi-check-circle"></i> Activar
                            </button>
                        ` : ''}
                        <button class="btn btn-sm btn-warning" onclick="resetCampana(${campana.id})" title="Resetear datos">
                            <i class="bi bi-arrow-clockwise"></i> Reset
                        </button>
                        ${!campana.activa ? `
                            <button class="btn btn-sm btn-danger" onclick="deleteCampana(${campana.id})" title="Eliminar campaña">
                                <i class="bi bi-trash"></i> Eliminar
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Mostrar modal para crear campaña
 */
function showCreateCampanaModal() {
    const modalHtml = `
        <div class="modal fade" id="createCampanaModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Crear Nueva Campaña</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Nombre *</label>
                                <input type="text" class="form-control" id="campanaNombre" placeholder="Ej: Campaña Presidencial 2026">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Código</label>
                                <input type="text" class="form-control" id="campanaCodigo" placeholder="Se genera automáticamente">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Descripción</label>
                            <textarea class="form-control" id="campanaDescripcion" rows="2"></textarea>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Fecha Inicio</label>
                                <input type="date" class="form-control" id="campanaFechaInicio">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Fecha Fin</label>
                                <input type="date" class="form-control" id="campanaFechaFin">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Color Primario</label>
                                <input type="color" class="form-control" id="campanaColorPrimario" value="#1e3c72">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Color Secundario</label>
                                <input type="color" class="form-control" id="campanaColorSecundario" value="#2a5298">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Campaña</label>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="campanaCandidatoUnico">
                                <label class="form-check-label" for="campanaCandidatoUnico">
                                    Campaña de candidato único
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="campanaPartidoCompleto">
                                <label class="form-check-label" for="campanaPartidoCompleto">
                                    Campaña de partido completo (múltiples elecciones)
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarCampana()">Crear Campaña</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('createCampanaModal'));
    modal.show();
    
    document.getElementById('createCampanaModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar nueva campaña
 */
async function guardarCampana() {
    const nombre = document.getElementById('campanaNombre').value.trim();
    
    if (!nombre) {
        Utils.showError('El nombre es requerido');
        return;
    }
    
    try {
        const response = await APIClient.post('/super-admin/campanas', {
            nombre: nombre,
            codigo: document.getElementById('campanaCodigo').value.trim(),
            descripcion: document.getElementById('campanaDescripcion').value.trim(),
            fecha_inicio: document.getElementById('campanaFechaInicio').value,
            fecha_fin: document.getElementById('campanaFechaFin').value,
            color_primario: document.getElementById('campanaColorPrimario').value,
            color_secundario: document.getElementById('campanaColorSecundario').value,
            es_candidato_unico: document.getElementById('campanaCandidatoUnico').checked,
            es_partido_completo: document.getElementById('campanaPartidoCompleto').checked
        });
        
        if (response.success) {
            Utils.showSuccess('Campaña creada exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('createCampanaModal')).hide();
            await loadCampanas();
        } else {
            Utils.showError(response.error || 'Error al crear campaña');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al crear campaña');
    }
}

/**
 * Activar campaña
 */
async function activarCampana(campanaId) {
    if (!confirm('¿Está seguro de activar esta campaña? Se desactivarán las demás.')) {
        return;
    }
    
    try {
        const response = await APIClient.put(`/super-admin/campanas/${campanaId}/activar`);
        
        if (response.success) {
            Utils.showSuccess('Campaña activada exitosamente');
            await loadCampanas();
        } else {
            Utils.showError(response.error || 'Error al activar campaña');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al activar campaña');
    }
}

/**
 * Resetear campaña
 */
async function resetCampana(campanaId) {
    const confirmText = prompt('Esta acción eliminará TODOS los datos de la campaña (formularios, incidentes, delitos).\\n\\nEscriba "CONFIRMAR_RESET" para continuar:');
    
    if (confirmText !== 'CONFIRMAR_RESET') {
        return;
    }
    
    try {
        const response = await APIClient.post(`/super-admin/campanas/${campanaId}/reset`, {
            confirmacion: 'CONFIRMAR_RESET'
        });
        
        if (response.success) {
            Utils.showSuccess(`Campaña reseteada. ${response.data.formularios_eliminados} formularios, ${response.data.incidentes_eliminados} incidentes y ${response.data.delitos_eliminados} delitos eliminados.`);
            await loadCampanas();
        } else {
            Utils.showError(response.error || 'Error al resetear campaña');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al resetear campaña');
    }
}

/**
 * Eliminar campaña
 */
async function deleteCampana(campanaId) {
    const confirmText = prompt('Esta acción eliminará PERMANENTEMENTE la campaña y todos sus datos.\\n\\nEscriba "CONFIRMAR_ELIMINACION" para continuar:');
    
    if (confirmText !== 'CONFIRMAR_ELIMINACION') {
        return;
    }
    
    try {
        const response = await APIClient.delete(`/super-admin/campanas/${campanaId}`, {
            confirmacion: 'CONFIRMAR_ELIMINACION'
        });
        
        if (response.success) {
            Utils.showSuccess('Campaña eliminada exitosamente');
            await loadCampanas();
        } else {
            Utils.showError(response.error || 'Error al eliminar campaña');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al eliminar campaña');
    }
}


// ============================================
// TESTING Y AUDITORÍA
// ============================================

/**
 * Cargar datos de prueba
 */
async function loadTestData() {
    if (!confirm('¿Está seguro de cargar datos de prueba?\\n\\nEsto creará:\\n- Usuarios de prueba para todos los roles\\n- Ubicaciones de ejemplo\\n- Partidos y candidatos\\n- Una campaña de prueba\\n\\nCredenciales: usuario_test / test123')) {
        return;
    }
    
    try {
        Utils.showInfo('Cargando datos de prueba... Esto puede tardar un momento.');
        
        const response = await APIClient.post('/super-admin/test/load-data', {});
        
        if (response.success) {
            Utils.showSuccess('Datos de prueba cargados exitosamente');
            
            // Mostrar detalles
            const modalHtml = `
                <div class="modal fade" id="testDataModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header bg-success text-white">
                                <h5 class="modal-title">✅ Datos de Prueba Cargados</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <h6>🔑 Credenciales de Acceso:</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Usuario</th>
                                                <th>Contraseña</th>
                                                <th>Rol</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td><code>admin_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Super Admin</td>
                                            </tr>
                                            <tr>
                                                <td><code>auditor_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Auditor</td>
                                            </tr>
                                            <tr>
                                                <td><code>coord_dept_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Coordinador Departamental</td>
                                            </tr>
                                            <tr>
                                                <td><code>coord_mun_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Coordinador Municipal</td>
                                            </tr>
                                            <tr>
                                                <td><code>coord_puesto_test</code></td>
                                                <td><code>test123</code></td>
                                                <td>Coordinador Puesto</td>
                                            </tr>
                                            <tr>
                                                <td><code>testigo_test_1</code></td>
                                                <td><code>test123</code></td>
                                                <td>Testigo</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="alert alert-info mt-3">
                                    <strong>💡 Tip:</strong> Puede cerrar sesión y probar con cualquiera de estos usuarios para verificar las funcionalidades de cada rol.
                                </div>
                                <pre class="bg-light p-3 rounded"><code>${response.output || 'Datos cargados exitosamente'}</code></pre>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                                <button type="button" class="btn btn-primary" onclick="runSystemAudit()">
                                    <i class="bi bi-clipboard-check"></i> Ejecutar Auditoría
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = new bootstrap.Modal(document.getElementById('testDataModal'));
            modal.show();
            
            document.getElementById('testDataModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
            
            // Recargar datos
            await loadMainStats();
            await loadUsers();
        } else {
            Utils.showError(response.error || 'Error al cargar datos de prueba');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al cargar datos de prueba');
    }
}

/**
 * Ejecutar auditoría del sistema
 */
async function runSystemAudit() {
    try {
        Utils.showInfo('Ejecutando auditoría del sistema...');
        
        const response = await APIClient.get('/super-admin/test/audit');
        
        if (response.success) {
            const audit = response.data;
            
            // Crear modal con resultados
            const checksHtml = audit.checks.map(check => {
                const icon = check.status === 'pass' ? '✅' : '❌';
                const badgeClass = check.status === 'pass' ? 'success' : 'danger';
                
                let detailsHtml = '';
                if (check.details) {
                    detailsHtml = '<ul class="small mb-0">';
                    for (const [key, value] of Object.entries(check.details)) {
                        detailsHtml += `<li>${key}: ${value}</li>`;
                    }
                    detailsHtml += '</ul>';
                }
                
                return `
                    <div class="card mb-2">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="mb-1">${icon} ${check.name}</h6>
                                    <p class="mb-1 text-muted small">${check.message}</p>
                                    ${detailsHtml}
                                </div>
                                <span class="badge bg-${badgeClass}">${check.status.toUpperCase()}</span>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            const statusClass = audit.status === 'success' ? 'success' : 'warning';
            const statusIcon = audit.status === 'success' ? '✅' : '⚠️';
            
            const modalHtml = `
                <div class="modal fade" id="auditModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header bg-${statusClass} text-white">
                                <h5 class="modal-title">${statusIcon} Auditoría del Sistema</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="alert alert-${statusClass}">
                                    <strong>${audit.message}</strong>
                                    <br><small>Ejecutado: ${new Date(audit.timestamp).toLocaleString()}</small>
                                </div>
                                <h6 class="mb-3">Resultados de Verificación:</h6>
                                ${checksHtml}
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                                <button type="button" class="btn btn-primary" onclick="runSystemAudit()">
                                    <i class="bi bi-arrow-clockwise"></i> Ejecutar Nuevamente
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remover modal anterior si existe
            const existingModal = document.getElementById('auditModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = new bootstrap.Modal(document.getElementById('auditModal'));
            modal.show();
            
            document.getElementById('auditModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
            
            if (audit.status === 'success') {
                Utils.showSuccess('Auditoría completada: Todos los checks pasaron');
            } else {
                Utils.showWarning('Auditoría completada con advertencias');
            }
        } else {
            Utils.showError(response.error || 'Error al ejecutar auditoría');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al ejecutar auditoría');
    }
}


// ============================================
// FUNCIONES DE EDICIÓN
// ============================================

/**
 * Editar partido
 */
async function editPartido(partidoId) {
    const partido = allPartidos.find(p => p.id === partidoId);
    if (!partido) {
        Utils.showError('Partido no encontrado');
        return;
    }
    
    const modalHtml = `
        <div class="modal fade" id="editPartidoModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Editar Partido</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Nombre Completo *</label>
                            <input type="text" class="form-control" id="editPartidoNombre" value="${partido.nombre}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Nombre Corto / Sigla *</label>
                            <input type="text" class="form-control" id="editPartidoNombreCorto" value="${partido.nombre_corto || partido.sigla || ''}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Color</label>
                            <input type="color" class="form-control" id="editPartidoColor" value="${partido.color || '#6c757d'}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Logo URL (opcional)</label>
                            <input type="text" class="form-control" id="editPartidoLogo" value="${partido.logo_url || ''}">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarEdicionPartido(${partidoId})">Guardar Cambios</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('editPartidoModal'));
    modal.show();
    
    document.getElementById('editPartidoModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar edición de partido
 */
async function guardarEdicionPartido(partidoId) {
    const nombre = document.getElementById('editPartidoNombre').value.trim();
    const nombreCorto = document.getElementById('editPartidoNombreCorto').value.trim();
    const color = document.getElementById('editPartidoColor').value;
    const logoUrl = document.getElementById('editPartidoLogo').value.trim();
    
    if (!nombre || !nombreCorto) {
        Utils.showError('El nombre y nombre corto son requeridos');
        return;
    }
    
    try {
        const response = await APIClient.put(`/super-admin/partidos/${partidoId}`, {
            nombre: nombre,
            nombre_corto: nombreCorto,
            color: color,
            logo_url: logoUrl || null
        });
        
        if (response.success) {
            Utils.showSuccess('Partido actualizado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('editPartidoModal')).hide();
            await loadPartidos();
        } else {
            Utils.showError(response.error || 'Error al actualizar partido');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar partido');
    }
}

/**
 * Editar tipo de elección
 */
async function editTipoEleccion(tipoId) {
    const tipo = allTiposEleccion.find(t => t.id === tipoId);
    if (!tipo) {
        Utils.showError('Tipo de elección no encontrado');
        return;
    }
    
    const modalHtml = `
        <div class="modal fade" id="editTipoEleccionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Editar Tipo de Elección</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Nombre *</label>
                            <input type="text" class="form-control" id="editTipoNombre" value="${tipo.nombre}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Descripción</label>
                            <textarea class="form-control" id="editTipoDescripcion" rows="2">${tipo.descripcion || ''}</textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Elección</label>
                            <select class="form-select" id="editTipoCategoria">
                                <option value="uninominal" ${tipo.es_uninominal ? 'selected' : ''}>Uninominal (Presidente, Gobernador, Alcalde)</option>
                                <option value="corporacion" ${!tipo.es_uninominal ? 'selected' : ''}>Por Corporación (Senado, Cámara, Asamblea, Concejo)</option>
                            </select>
                        </div>
                        <div id="editOpcionesLista" style="display:${tipo.es_uninominal ? 'none' : 'block'};">
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="editListaCerrada" ${tipo.permite_lista_cerrada ? 'checked' : ''}>
                                <label class="form-check-label" for="editListaCerrada">
                                    Permite lista cerrada
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="editListaAbierta" ${tipo.permite_lista_abierta ? 'checked' : ''}>
                                <label class="form-check-label" for="editListaAbierta">
                                    Permite lista abierta (voto preferente)
                                </label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="checkbox" id="editCoaliciones" ${tipo.permite_coaliciones ? 'checked' : ''}>
                                <label class="form-check-label" for="editCoaliciones">
                                    Permite coaliciones
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarEdicionTipoEleccion(${tipoId})">Guardar Cambios</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('editTipoEleccionModal'));
    
    // Manejar cambio de categoría
    document.getElementById('editTipoCategoria').addEventListener('change', function() {
        const opcionesLista = document.getElementById('editOpcionesLista');
        opcionesLista.style.display = this.value === 'corporacion' ? 'block' : 'none';
    });
    
    modal.show();
    
    document.getElementById('editTipoEleccionModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar edición de tipo de elección
 */
async function guardarEdicionTipoEleccion(tipoId) {
    const nombre = document.getElementById('editTipoNombre').value.trim();
    const descripcion = document.getElementById('editTipoDescripcion').value.trim();
    const categoria = document.getElementById('editTipoCategoria').value;
    
    if (!nombre) {
        Utils.showError('El nombre es requerido');
        return;
    }
    
    const esUninominal = categoria === 'uninominal';
    const listaCerrada = !esUninominal && document.getElementById('editListaCerrada').checked;
    const listaAbierta = !esUninominal && document.getElementById('editListaAbierta').checked;
    const coaliciones = !esUninominal && document.getElementById('editCoaliciones').checked;
    
    try {
        const response = await APIClient.put(`/super-admin/tipos-eleccion/${tipoId}`, {
            nombre: nombre,
            descripcion: descripcion,
            es_uninominal: esUninominal,
            permite_lista_cerrada: listaCerrada,
            permite_lista_abierta: listaAbierta,
            permite_coaliciones: coaliciones
        });
        
        if (response.success) {
            Utils.showSuccess('Tipo de elección actualizado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('editTipoEleccionModal')).hide();
            await loadTiposEleccion();
        } else {
            Utils.showError(response.error || 'Error al actualizar tipo de elección');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar tipo de elección');
    }
}

/**
 * Editar candidato
 */
async function editCandidato(candidatoId) {
    const candidato = allCandidatos.find(c => c.id === candidatoId);
    if (!candidato) {
        Utils.showError('Candidato no encontrado');
        return;
    }
    
    const modalHtml = `
        <div class="modal fade" id="editCandidatoModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Editar Candidato</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Nombre Completo *</label>
                            <input type="text" class="form-control" id="editCandidatoNombre" value="${candidato.nombre_completo || candidato.nombre}">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Partido</label>
                            <select class="form-select" id="editCandidatoPartido">
                                <option value="">Independiente</option>
                                ${allPartidos.map(p => `
                                    <option value="${p.id}" ${p.id === candidato.partido_id ? 'selected' : ''}>${p.nombre}</option>
                                `).join('')}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tipo de Elección *</label>
                            <select class="form-select" id="editCandidatoTipoEleccion">
                                ${allTiposEleccion.map(t => `
                                    <option value="${t.id}" ${t.id === candidato.tipo_eleccion_id ? 'selected' : ''}>${t.nombre}</option>
                                `).join('')}
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Número de Lista (opcional)</label>
                            <input type="number" class="form-control" id="editCandidatoNumeroLista" value="${candidato.numero_lista || ''}" min="1">
                            <small class="text-muted">Solo para elecciones por listas</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Foto URL (opcional)</label>
                            <input type="text" class="form-control" id="editCandidatoFoto" value="${candidato.foto_url || ''}">
                        </div>
                        <div class="form-check mb-2">
                            <input class="form-check-input" type="checkbox" id="editCandidatoIndependiente" ${candidato.es_independiente ? 'checked' : ''}>
                            <label class="form-check-label" for="editCandidatoIndependiente">
                                Candidato Independiente
                            </label>
                        </div>
                        <div class="form-check mb-2">
                            <input class="form-check-input" type="checkbox" id="editCandidatoCabezaLista" ${candidato.es_cabeza_lista ? 'checked' : ''}>
                            <label class="form-check-label" for="editCandidatoCabezaLista">
                                Cabeza de Lista
                            </label>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" onclick="guardarEdicionCandidato(${candidatoId})">Guardar Cambios</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('editCandidatoModal'));
    modal.show();
    
    document.getElementById('editCandidatoModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

/**
 * Guardar edición de candidato
 */
async function guardarEdicionCandidato(candidatoId) {
    const nombre = document.getElementById('editCandidatoNombre').value.trim();
    const partidoId = document.getElementById('editCandidatoPartido').value;
    const tipoEleccionId = document.getElementById('editCandidatoTipoEleccion').value;
    const numeroLista = document.getElementById('editCandidatoNumeroLista').value;
    const fotoUrl = document.getElementById('editCandidatoFoto').value.trim();
    const esIndependiente = document.getElementById('editCandidatoIndependiente').checked;
    const esCabezaLista = document.getElementById('editCandidatoCabezaLista').checked;
    
    if (!nombre || !tipoEleccionId) {
        Utils.showError('El nombre y tipo de elección son requeridos');
        return;
    }
    
    try {
        const response = await APIClient.put(`/super-admin/candidatos/${candidatoId}`, {
            nombre_completo: nombre,
            partido_id: partidoId || null,
            tipo_eleccion_id: parseInt(tipoEleccionId),
            numero_lista: numeroLista ? parseInt(numeroLista) : null,
            foto_url: fotoUrl || null,
            es_independiente: esIndependiente,
            es_cabeza_lista: esCabezaLista
        });
        
        if (response.success) {
            Utils.showSuccess('Candidato actualizado exitosamente');
            bootstrap.Modal.getInstance(document.getElementById('editCandidatoModal')).hide();
            await loadCandidatos();
        } else {
            Utils.showError(response.error || 'Error al actualizar candidato');
        }
    } catch (error) {
        console.error('Error:', error);
        Utils.showError('Error al actualizar candidato');
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initSuperAdminDashboard);


/**
 * Arreglar contraseñas - Actualizar todas a texto plano
 */
async function fixPasswords() {
    if (!confirm('¿Actualizar todas las contraseñas a texto plano?\n\nEsto NO borrará datos, solo actualizará las contraseñas.')) {
        return;
    }
    
    try {
        Utils.showInfo('Actualizando contraseñas...');
        
        const response = await APIClient.post('/admin/fix-passwords', {});
        
        if (response.success) {
            let message = '✅ Contraseñas actualizadas exitosamente!\n\n';
            message += 'CONTRASEÑAS:\n';
            for (const [rol, password] of Object.entries(response.passwords)) {
                message += `${rol}: ${password}\n`;
            }
            
            alert(message);
            Utils.showSuccess('Contraseñas actualizadas. Puedes seguir usando el sistema.');
        } else {
            Utils.showError('Error al actualizar contraseñas: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error actualizando contraseñas:', error);
        Utils.showError('Error al actualizar contraseñas: ' + error.message);
    }
}

/**
 * Resetear base de datos
 * ADVERTENCIA: Esto borrará todos los datos y recreará la BD desde cero
 */
async function resetDatabase() {
    // Confirmación múltiple para evitar borrados accidentales
    if (!confirm('⚠️ ADVERTENCIA: Esto borrará TODA la base de datos y la recreará desde cero.\n\n¿Estás seguro de que quieres continuar?')) {
        return;
    }
    
    if (!confirm('⚠️ ÚLTIMA CONFIRMACIÓN: Se perderán TODOS los datos actuales.\n\nLa aplicación se reiniciará automáticamente.\n\n¿Continuar?')) {
        return;
    }
    
    try {
        Utils.showInfo('Reseteando base de datos...');
        
        const response = await APIClient.post('/admin/reset-database', {});
        
        if (response.success) {
            Utils.showSuccess('✅ Base de datos reseteada. La aplicación se reiniciará en 5 segundos...');
            
            // Esperar 5 segundos y recargar la página
            setTimeout(() => {
                // Limpiar tokens
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_data');
                
                // Redirigir al login
                window.location.href = '/auth/login';
            }, 5000);
        } else {
            Utils.showError('Error al resetear base de datos: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error reseteando base de datos:', error);
        Utils.showError('Error al resetear base de datos: ' + error.message);
    }
}


/**
 * Corregir roles de usuarios
 */
async function fixRoles() {
    if (!confirm('¿Corregir roles de usuarios de prueba?\n\nEsto actualizará:\n- admin → super_admin\n- testigo → testigo_electoral\n- coordinador_puesto → coordinador_puesto\n- coordinador_municipal → coordinador_municipal\n- coordinador_departamental → coordinador_departamental\n\nTambién reseteará contraseñas y desbloqueará cuentas.')) {
        return;
    }
    
    try {
        Utils.showInfo('Corrigiendo roles...');
        
        const response = await APIClient.post('/admin/fix-roles', {});
        
        if (response.success) {
            let message = '✅ Roles corregidos exitosamente!\n\n';
            message += `Total de cambios: ${response.message}\n\n`;
            message += 'RESULTADOS:\n';
            
            for (const resultado of response.resultados) {
                message += `\n${resultado.usuario}: ${resultado.status}`;
                if (resultado.cambios.length > 0) {
                    message += '\n  - ' + resultado.cambios.join('\n  - ');
                }
            }
            
            message += '\n\n⚠️ IMPORTANTE:\n';
            for (const nota of response.importante) {
                message += `- ${nota}\n`;
            }
            
            alert(message);
            Utils.showSuccess('Roles corregidos. Todos los usuarios deben cerrar sesión y volver a iniciar sesión.');
            
            // Recargar estadísticas
            await loadMainStats();
        } else {
            Utils.showError('Error al corregir roles: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error corrigiendo roles:', error);
        Utils.showError('Error al corregir roles: ' + error.message);
    }
}

/**
 * Ejecutar diagnóstico del sistema
 */
async function runDiagnostico() {
    try {
        Utils.showInfo('Ejecutando diagnóstico...');
        
        const response = await APIClient.get('/admin/diagnostico');
        
        if (response.success) {
            const data = response.data;
            
            let message = '📊 DIAGNÓSTICO DEL SISTEMA\n\n';
            
            // Estadísticas
            message += '=== ESTADÍSTICAS ===\n';
            message += `Total de usuarios: ${data.estadisticas.total_usuarios}\n`;
            message += `Usuarios activos: ${data.estadisticas.usuarios_activos}\n`;
            message += `Usuarios bloqueados: ${data.estadisticas.usuarios_bloqueados}\n`;
            message += `Usuarios inactivos: ${data.estadisticas.usuarios_inactivos}\n\n`;
            
            // Roles
            message += '=== USUARIOS POR ROL ===\n';
            for (const [rol, count] of Object.entries(data.roles)) {
                message += `${rol}: ${count}\n`;
            }
            message += '\n';
            
            // Usuarios de prueba
            message += '=== USUARIOS DE PRUEBA ===\n';
            for (const user of data.usuarios_prueba) {
                message += `\n${user.nombre}:\n`;
                message += `  Rol: ${user.rol}\n`;
                message += `  Activo: ${user.activo ? 'Sí' : 'No'}\n`;
                message += `  Bloqueado: ${user.bloqueado ? 'Sí' : 'No'}\n`;
                if (user.presencia_verificada !== null) {
                    message += `  Presencia: ${user.presencia_verificada ? 'Verificada' : 'No verificada'}\n`;
                }
            }
            message += '\n';
            
            // Problemas
            if (data.problemas.length > 0) {
                message += '=== ⚠️ PROBLEMAS DETECTADOS ===\n';
                for (const problema of data.problemas) {
                    message += `- ${problema}\n`;
                }
            } else {
                message += '=== ✅ NO HAY PROBLEMAS ===\n';
            }
            
            message += '\n';
            message += `Base de datos: ${data.database_url}\n`;
            
            alert(message);
            Utils.showSuccess('Diagnóstico completado');
        } else {
            Utils.showError('Error al ejecutar diagnóstico: ' + (response.error || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error ejecutando diagnóstico:', error);
        Utils.showError('Error al ejecutar diagnóstico: ' + error.message);
    }
}


/**
 * Cargar datos de prueba
 */
async function loadTestData() {
    if (!confirm('¿Está seguro de cargar datos de prueba?\n\nEsto creará usuarios, formularios y datos de ejemplo en el sistema.')) {
        return;
    }
    
    try {
        Utils.showInfo('Cargando datos de prueba...');
        
        const response = await APIClient.post('/super-admin/test/load-data', {});
        
        if (response.success) {
            Utils.showSuccess('Datos de prueba cargados exitosamente');
            
            // Recargar estadísticas
            await loadMainStats();
            await loadUsers();
        } else {
            Utils.showError(response.error || 'Error al cargar datos de prueba');
        }
    } catch (error) {
        console.error('Error cargando datos de prueba:', error);
        Utils.showError('Error al cargar datos de prueba: ' + error.message);
    }
}

/**
 * Ejecutar auditoría del sistema
 */
async function runSystemAudit() {
    try {
        Utils.showInfo('Ejecutando auditoría del sistema...');
        
        const response = await APIClient.get('/super-admin/test/audit');
        
        if (response.success) {
            const audit = response.data;
            
            let message = '📊 AUDITORÍA DEL SISTEMA\n\n';
            message += '=== ESTADÍSTICAS ===\n';
            message += `Total usuarios: ${audit.total_usuarios || 0}\n`;
            message += `Total ubicaciones: ${audit.total_ubicaciones || 0}\n`;
            message += `Total formularios: ${audit.total_formularios || 0}\n\n`;
            
            message += '=== PROBLEMAS DETECTADOS ===\n';
            if (audit.problemas && audit.problemas.length > 0) {
                audit.problemas.forEach(p => {
                    message += `⚠️ ${p}\n`;
                });
            } else {
                message += '✅ No se detectaron problemas\n';
            }
            
            alert(message);
            Utils.showSuccess('Auditoría completada');
        } else {
            Utils.showError(response.error || 'Error al ejecutar auditoría');
        }
    } catch (error) {
        console.error('Error ejecutando auditoría:', error);
        Utils.showError('Error al ejecutar auditoría: ' + error.message);
    }
}
