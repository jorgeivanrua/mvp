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
    Utils.showInfo('Funcionalidad de crear usuario en desarrollo');
    // TODO: Implementar modal completo con formulario
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
    Utils.showInfo('Funcionalidad de configuración en desarrollo');
}

/**
 * Exportar todos los datos
 */
async function exportAllData() {
    if (!confirm('¿Está seguro de exportar todos los datos del sistema? Esto puede tardar varios minutos.')) {
        return;
    }
    
    Utils.showInfo('Iniciando exportación de datos...');
    // TODO: Implementar exportación real
}

/**
 * Crear respaldo
 */
async function createBackup() {
    if (!confirm('¿Está seguro de crear un respaldo de la base de datos?')) {
        return;
    }
    
    Utils.showInfo('Creando respaldo...');
    // TODO: Implementar respaldo real
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
        window.location.href = '/login';
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
