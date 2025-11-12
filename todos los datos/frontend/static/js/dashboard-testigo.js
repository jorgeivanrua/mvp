// Dashboard Testigo Electoral - Sistema Electoral MVP

const API_BASE = '/api';
let currentUser = null;

// Inicializar dashboard
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadUserInfo();
    loadForms();
});

// Verificar autenticación
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!token || !user.id) {
        window.location.href = '/login';
        return;
    }
    
    if (user.rol !== 'testigo_electoral') {
        alert('Acceso no autorizado');
        logout();
        return;
    }
    
    currentUser = user;
}

// Cargar información del usuario
function loadUserInfo() {
    document.getElementById('userName').textContent = currentUser.nombre;
}

// Cargar formularios
async function loadForms() {
    try {
        const response = await fetchAPI('/e14/forms');
        
        if (response.success) {
            const forms = response.data;
            updateStats(forms);
            renderForms(forms);
        } else {
            showError('Error al cargar formularios');
        }
    } catch (error) {
        showError('Error de conexión');
    }
}

// Actualizar estadísticas
function updateStats(forms) {
    const total = forms.length;
    const pending = forms.filter(f => f.estado === 'borrador' || f.estado === 'enviado').length;
    const approved = forms.filter(f => f.estado === 'aprobado').length;
    const rejected = forms.filter(f => f.estado === 'rechazado').length;
    
    document.getElementById('totalForms').textContent = total;
    document.getElementById('pendingForms').textContent = pending;
    document.getElementById('approvedForms').textContent = approved;
    document.getElementById('rejectedForms').textContent = rejected;
}

// Renderizar lista de formularios
function renderForms(forms) {
    const container = document.getElementById('formsList');
    
    if (forms.length === 0) {
        container.innerHTML = '<p class="loading">No hay formularios registrados</p>';
        return;
    }
    
    container.innerHTML = forms.map(form => `
        <div class="form-card" onclick="viewForm(${form.id})">
            <div class="form-card-header">
                <div class="form-card-title">
                    Formulario E-14 #${form.id}
                </div>
                <span class="form-status status-${form.estado}">
                    ${getStatusLabel(form.estado)}
                </span>
            </div>
            <div class="form-card-body">
                <div class="form-field">
                    <strong>Mesa:</strong>
                    ${form.mesa_nombre || 'N/A'}
                </div>
                <div class="form-field">
                    <strong>Total Votos:</strong>
                    ${form.total_votos}
                </div>
                <div class="form-field">
                    <strong>Fecha:</strong>
                    ${formatDate(form.created_at)}
                </div>
                ${form.estado === 'rechazado' ? `
                <div class="form-field" style="grid-column: 1/-1;">
                    <strong>Motivo rechazo:</strong>
                    ${form.observaciones}
                </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Ver detalle de formulario
function viewForm(formId) {
    window.location.href = `/e14/form/${formId}`;
}

// Crear nuevo formulario
function createNewForm() {
    window.location.href = '/e14/new';
}

// Obtener etiqueta de estado
function getStatusLabel(status) {
    const labels = {
        'borrador': 'Borrador',
        'enviado': 'Enviado',
        'aprobado': 'Aprobado',
        'rechazado': 'Rechazado'
    };
    return labels[status] || status;
}

// Formatear fecha
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Cerrar sesión
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
}

// Función auxiliar para hacer peticiones a la API
async function fetchAPI(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    };
    
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    });
    
    if (response.status === 401) {
        logout();
        return;
    }
    
    return await response.json();
}

// Mostrar error
function showError(message) {
    alert(message);
}
