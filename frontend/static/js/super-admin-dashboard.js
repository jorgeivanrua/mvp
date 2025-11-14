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
        // TODO: Implementar endpoint real de estadísticas
        // Por ahora usamos datos de ejemplo
        
        const stats = {
            totalUsuarios: 0,
            usuariosChange: 0,
            totalPuestos: 0,
            totalMesas: 0,
            totalFormularios: 0,
            formulariosPendientes: 0,
            totalValidados: 0,
            porcentajeValidados: 0
        };
        
        // Actualizar UI
        document.getElementById('totalUsuarios').textContent = Utils.formatNumber(stats.totalUsuarios);
        document.getElementById('usuariosChange').textContent = stats.usuariosChange;
        document.getElementById('totalPuestos').textContent = Utils.formatNumber(stats.totalPuestos);
        document.getElementById('totalMesas').textContent = Utils.formatNumber(stats.totalMesas);
        document.getElementById('totalFormularios').textContent = Utils.formatNumber(stats.totalFormularios);
        document.getElementById('formulariosPendientes').textContent = Utils.formatNumber(stats.formulariosPendientes);
        document.getElementById('totalValidados').textContent = Utils.formatNumber(stats.totalValidados);
        document.getElementById('porcentajeValidados').textContent = stats.porcentajeValidados.toFixed(1);
        
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
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
function updateSystemHealth() {
    // TODO: Implementar verificación real de salud
    const indicator = document.getElementById('systemHealthIndicator');
    const text = document.getElementById('systemHealthText');
    
    // Por ahora siempre mostramos "bueno"
    indicator.className = 'health-indicator health-good';
    text.textContent = 'Sistema operando normalmente';
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
        // TODO: Implementar endpoint real
        const tbody = document.getElementById('usersTableBody');
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><p class="text-muted">No hay usuarios para mostrar</p></td></tr>';
        
    } catch (error) {
        console.error('Error cargando usuarios:', error);
    }
}

/**
 * Filtrar usuarios
 */
function filterUsers() {
    const role = document.getElementById('filterRole').value;
    const status = document.getElementById('filterStatus').value;
    const search = document.getElementById('searchUser').value.toLowerCase();
    
    // TODO: Implementar filtrado real
    console.log('Filtrando usuarios:', { role, status, search });
}

/**
 * Mostrar modal de crear usuario
 */
function showCreateUserModal() {
    Utils.showInfo('Funcionalidad de crear usuario en desarrollo');
    // TODO: Implementar modal
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
        <div class="d-flex align-items-center justify-content-between mb-2 p-2 border rounded">
            <div class="d-flex align-items-center">
                <div style="width: 30px; height: 30px; background-color: ${partido.color}; border-radius: 4px; margin-right: 10px;"></div>
                <div>
                    <strong>${partido.nombre}</strong>
                    <br><small class="text-muted">${partido.nombre_corto}</small>
                </div>
            </div>
            <div>
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
    
    container.innerHTML = allTiposEleccion.map(tipo => `
        <div class="d-flex align-items-center justify-content-between mb-2 p-2 border rounded">
            <div>
                <strong>${tipo.nombre}</strong>
                <br><small class="text-muted">${tipo.es_uninominal ? 'Uninominal' : 'Por listas'}</small>
            </div>
            <div>
                <button class="btn btn-sm btn-outline-primary" onclick="editTipoEleccion(${tipo.id})">
                    <i class="bi bi-pencil"></i>
                </button>
            </div>
        </div>
    `).join('');
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
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4"><p class="text-muted">No hay candidatos registrados</p></td></tr>';
        return;
    }
    
    tbody.innerHTML = allCandidatos.map(candidato => `
        <tr>
            <td>${candidato.nombre_completo}</td>
            <td>${candidato.partido_nombre || 'Independiente'}</td>
            <td>${candidato.tipo_eleccion_nombre || 'N/A'}</td>
            <td>${candidato.numero_lista || '-'}</td>
            <td><span class="badge bg-${candidato.activo ? 'success' : 'secondary'}">${candidato.activo ? 'Activo' : 'Inactivo'}</span></td>
            <td>
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
