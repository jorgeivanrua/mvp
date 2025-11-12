/**
 * Dashboard del Coordinador de Puesto
 */
class CoordinadorPuestoDashboard {
    constructor() {
        this.userData = null;
        this.init();
    }
    
    async init() {
        if (!this.checkAuth()) {
            window.location.href = '/login';
            return;
        }
        
        await this.loadUserData();
        await this.loadPuestoInfo();
        await this.loadStats();
        await this.loadTestigos();
    }
    
    checkAuth() {
        const token = localStorage.getItem('access_token');
        const userData = localStorage.getItem('user_data');
        
        if (!token || !userData) {
            return false;
        }
        
        try {
            this.userData = JSON.parse(userData);
            return true;
        } catch (e) {
            return false;
        }
    }
    
    async loadUserData() {
        try {
            const response = await APIClient.getProfile();
            this.userData = response.data;
            
            document.getElementById('userInfo').innerHTML = `
                <strong>${this.userData.nombre}</strong> - Coordinador de Puesto<br>
                <small>${this.userData.ubicacion?.nombre_completo || 'Sin ubicación'}</small>
            `;
        } catch (error) {
            console.error('Error loading user data:', error);
        }
    }
    
    async loadPuestoInfo() {
        if (!this.userData || !this.userData.ubicacion) {
            return;
        }
        
        const ubicacion = this.userData.ubicacion;
        
        document.getElementById('puestoInfo').innerHTML = `
            <div class="row">
                <div class="col-md-3">
                    <strong>Departamento:</strong><br>
                    ${ubicacion.departamento_nombre || 'N/A'}
                </div>
                <div class="col-md-3">
                    <strong>Municipio:</strong><br>
                    ${ubicacion.municipio_nombre || 'N/A'}
                </div>
                <div class="col-md-3">
                    <strong>Puesto:</strong><br>
                    ${ubicacion.puesto_nombre || 'N/A'}
                </div>
                <div class="col-md-3">
                    <strong>Dirección:</strong><br>
                    ${ubicacion.direccion || 'N/A'}
                </div>
            </div>
        `;
    }
    
    async loadStats() {
        // Datos simulados por ahora
        document.getElementById('totalTestigos').textContent = '0';
        document.getElementById('totalMesas').textContent = '0';
        document.getElementById('formulariosRegistrados').textContent = '0';
        document.getElementById('totalVotantes').textContent = 
            Utils.formatNumber(this.userData?.ubicacion?.total_votantes_registrados || 0);
    }
    
    async loadTestigos() {
        const container = document.getElementById('testigosContainer');
        
        try {
            // TODO: Implementar endpoint real
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            const testigos = []; // Datos simulados
            
            if (testigos.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-4">
                        <p class="text-muted">No hay testigos asignados aún</p>
                    </div>
                `;
                return;
            }
            
            // Renderizar testigos
            let html = '<div class="table-responsive"><table class="table">';
            html += '<thead><tr><th>Nombre</th><th>Mesa</th><th>Estado</th><th>Último Acceso</th></tr></thead>';
            html += '<tbody>';
            
            testigos.forEach(testigo => {
                html += `
                    <tr>
                        <td>${testigo.nombre}</td>
                        <td>${testigo.mesa}</td>
                        <td><span class="status-badge status-${testigo.activo ? 'activo' : 'inactivo'}">
                            ${testigo.activo ? 'Activo' : 'Inactivo'}
                        </span></td>
                        <td>${Utils.formatDate(testigo.ultimo_acceso)}</td>
                    </tr>
                `;
            });
            
            html += '</tbody></table></div>';
            container.innerHTML = html;
            
        } catch (error) {
            console.error('Error loading testigos:', error);
            container.innerHTML = '<div class="alert alert-danger">Error cargando testigos</div>';
        }
    }
}

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

document.addEventListener('DOMContentLoaded', () => {
    new CoordinadorPuestoDashboard();
});
