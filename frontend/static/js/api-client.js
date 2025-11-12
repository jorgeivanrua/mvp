/**
 * Cliente API para comunicación con el backend
 */
class APIClient {
    static baseURL = '/api';
    
    static getAuthHeaders() {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        return headers;
    }
    
    static async handleResponse(response) {
        let data;
        
        try {
            data = await response.json();
        } catch (error) {
            throw new Error('Error parsing response JSON');
        }
        
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');
            
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
            
            throw new Error('Sesión expirada');
        }
        
        if (!data.success) {
            throw new Error(data.error || 'Error en la petición');
        }
        
        return data;
    }
    
    static async get(endpoint, params = {}) {
        const url = new URL(`${window.location.origin}${this.baseURL}${endpoint}`);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined) {
                url.searchParams.append(key, params[key]);
            }
        });
        
        const response = await fetch(url, {
            method: 'GET',
            headers: this.getAuthHeaders()
        });
        
        return this.handleResponse(response);
    }
    
    static async post(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        return this.handleResponse(response);
    }
    
    // Métodos específicos de autenticación
    static async login(credentials) {
        return this.post('/auth/login', credentials);
    }
    
    static async logout() {
        return this.post('/auth/logout', {});
    }
    
    static async getProfile() {
        return this.get('/auth/profile');
    }
    
    static async changePassword(passwords) {
        return this.post('/auth/change-password', passwords);
    }
    
    // Métodos de ubicaciones
    static async getDepartamentos() {
        return this.get('/locations/departamentos');
    }
    
    static async getMunicipios(departamentoId) {
        return this.get('/locations/municipios', { departamento_codigo: departamentoId });
    }
    
    static async getZonas(municipioId) {
        return this.get('/locations/zonas', { municipio_codigo: municipioId });
    }
    
    static async getPuestos(zonaId) {
        return this.get('/locations/puestos', { zona_codigo: zonaId });
    }
    
    static async getMesas(puestoId) {
        return this.get('/locations/mesas', { puesto_codigo: puestoId });
    }
    
    // Métodos de configuración electoral
    static async getTiposEleccion() {
        return this.get('/configuracion/tipos-eleccion');
    }
    
    static async getPartidos() {
        return this.get('/configuracion/partidos');
    }
    
    static async getCandidatos(params = {}) {
        return this.get('/configuracion/candidatos', params);
    }
    
    static async getCoaliciones() {
        return this.get('/configuracion/coaliciones');
    }
    
    static async createTipoEleccion(data) {
        return this.post('/configuracion/tipos-eleccion', data);
    }
    
    static async createPartido(data) {
        return this.post('/configuracion/partidos', data);
    }
    
    static async createCandidato(data) {
        return this.post('/configuracion/candidatos', data);
    }
    
    static async createCoalicion(data) {
        return this.post('/configuracion/coaliciones', data);
    }
}

window.APIClient = APIClient;

    // ==========================================
    // FORMULARIOS E-14
    // ==========================================
    
    static async getFormulariosE14(params = {}) {
        return this.get('/formularios-e14', params);
    }
    
    static async getFormularioE14(id) {
        return this.get(`/formularios-e14/${id}`);
    }
    
    static async createFormularioE14(data) {
        return this.post('/formularios-e14', data);
    }
    
    static async updateFormularioE14(id, data) {
        return this.put(`/formularios-e14/${id}`, data);
    }
    
    static async validarFormularioE14(id, estado, observaciones = '') {
        return this.post(`/formularios-e14/${id}/validar`, { estado, observaciones });
    }
    
    static async deleteFormularioE14(id) {
        return this.delete(`/formularios-e14/${id}`);
    }
