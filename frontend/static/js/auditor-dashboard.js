/**
 * Dashboard Auditor Electoral
 * Sistema de auditoría y verificación de integridad del proceso electoral
 */

const AuditorDashboard = {
    // Variables globales
    currentUser: null,
    departamento: null,
    formularios: [],
    discrepancias: [],
    incidentes: [],
    delitos: [],
    logs: [],
    filtroEstado: '',
    autoRefreshInterval: null,
    charts: {},
    mapa: null,

    /**
     * Inicializar dashboard
     */
    async init() {
        console.log('[Auditor] Inicializando dashboard de auditor...');
        
        try {
            await this.loadUserProfile();
            await this.loadSystemLogs();
            await this.loadUserActivity();
            await this.loadFormularios();
            await this.loadIncidentes();
            await this.loadDelitos();
            await this.loadAnomalias();
            await this.loadStats();
            
            this.setupEventListeners();
            this.startAutoRefresh();
            
            console.log('[Auditor] Dashboard inicializado correctamente');
        } catch (error) {
            console.error('[Auditor] Error inicializando dashboard:', error);
            Utils.showError('Error al inicializar el dashboard de auditoría');
        }
    },

    /**
     * Cargar perfil del auditor
     */
    async loadUserProfile() {
        try {
            const response = await APIClient.get('/auth/profile');
            
            if (response.success) {
                this.currentUser = response.data.user;
                this.departamento = response.data.ubicacion;
                
                // Actualizar información en el header
                const userNameElement = document.getElementById('auditor-name');
                if (userNameElement) {
                    userNameElement.textContent = this.currentUser.nombre;
                }
                
                const deptElement = document.getElementById('auditor-departamento');
                if (deptElement && this.departamento) {
                    deptElement.textContent = this.departamento.departamento_nombre || 'Nacional';
                }
                
                console.log('[Auditor] Perfil cargado:', this.currentUser);
            } else {
                throw new Error(response.error || 'Error al cargar perfil');
            }
        } catch (error) {
            console.error('[Auditor] Error loading profile:', error);
            Utils.showError('Error al cargar perfil del auditor');
        }
    },

    /**
     * Cargar logs del sistema
     */
    async loadSystemLogs() {
        try {
            const response = await APIClient.get('/auditor/logs', {
                limit: 100,
                order: 'desc'
            });
            
            if (response.success) {
                this.logs = response.data || [];
                this.renderSystemLogs();
            } else {
                throw new Error(response.error || 'Error al cargar logs');
            }
        } catch (error) {
            console.error('[Auditor] Error loading logs:', error);
            this.renderSystemLogsError();
        }
    },

    /**
     * Renderizar logs del sistema
     */
    renderSystemLogs() {
        const container = document.getElementById('system-logs-container');
        if (!container) return;
        
        if (this.logs.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-journal-text text-muted" style="font-size: 2rem;"></i>
                    <p class="text-muted mt-2">No hay logs disponibles</p>
                </div>
            `;
            return;
        }
        
        const logsHtml = this.logs.slice(0, 20).map(log => {
            const fecha = new Date(log.timestamp).toLocaleString('es-CO');
            const severityClass = this.getSeverityClass(log.nivel_severidad);
            
            return `
                <div class="log-entry border-bottom py-2">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <span class="badge bg-${severityClass} me-2">${log.nivel_severidad}</span>
                            <strong>${log.accion}</strong>
                            <p class="mb-1 text-muted small">${log.detalles || 'Sin detalles'}</p>
                            <small class="text-muted">
                                Usuario: ${log.usuario_nombre || 'Sistema'} | 
                                IP: ${log.ip_address || 'N/A'}
                            </small>
                        </div>
                        <small class="text-muted">${fecha}</small>
                    </div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = logsHtml;
    },

    /**
     * Renderizar error en logs
     */
    renderSystemLogsError() {
        const container = document.getElementById('system-logs-container');
        if (!container) return;
        
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-exclamation-triangle text-danger" style="font-size: 2rem;"></i>
                <p class="text-danger mt-2">Error al cargar logs del sistema</p>
                <button class="btn btn-sm btn-outline-primary" onclick="AuditorDashboard.loadSystemLogs()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    },

    /**
     * Cargar actividad de usuarios
     */
    async loadUserActivity() {
        try {
            const response = await APIClient.get('/auditor/user-activity');
            
            if (response.success) {
                this.renderUserActivity(response.data);
            } else {
                throw new Error(response.error || 'Error al cargar actividad');
            }
        } catch (error) {
            console.error('[Auditor] Error loading user activity:', error);
            this.renderUserActivityError();
        }
    },

    /**
     * Renderizar actividad de usuarios
     */
    renderUserActivity(activity) {
        const container = document.getElementById('user-activity-container');
        if (!container) return;
        
        if (!activity || activity.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-people text-muted" style="font-size: 2rem;"></i>
                    <p class="text-muted mt-2">No hay actividad reciente</p>
                </div>
            `;
            return;
        }
        
        const activityHtml = activity.slice(0, 15).map(act => {
            const fecha = new Date(act.timestamp).toLocaleString('es-CO');
            const roleClass = this.getRoleClass(act.rol);
            
            return `
                <div class="activity-entry border-bottom py-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <span class="badge bg-${roleClass} me-2">${act.rol}</span>
                            <strong>${act.usuario_nombre}</strong>
                            <p class="mb-0 text-muted small">${act.accion}</p>
                        </div>
                        <small class="text-muted">${fecha}</small>
                    </div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = activityHtml;
    },

    /**
     * Renderizar error en actividad de usuarios
     */
    renderUserActivityError() {
        const container = document.getElementById('user-activity-container');
        if (!container) return;
        
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-exclamation-triangle text-danger" style="font-size: 2rem;"></i>
                <p class="text-danger mt-2">Error al cargar actividad de usuarios</p>
                <button class="btn btn-sm btn-outline-primary" onclick="AuditorDashboard.loadUserActivity()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    },

    /**
     * Cargar formularios para verificación
     */
    async loadFormularios() {
        try {
            let params = { limit: 100 };
            if (this.filtroEstado) {
                params.estado = this.filtroEstado;
            }
            
            const response = await APIClient.get('/auditor/formularios', params);
            
            if (response.success) {
                this.formularios = response.data || [];
                this.renderFormulariosTable();
            } else {
                throw new Error(response.error || 'Error al cargar formularios');
            }
        } catch (error) {
            console.error('[Auditor] Error loading formularios:', error);
            this.renderFormulariosError();
        }
    },

    /**
     * Renderizar tabla de formularios
     */
    renderFormulariosTable() {
        const tbody = document.querySelector('#tabla-formularios tbody');
        if (!tbody) return;
        
        if (this.formularios.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="9" class="text-center py-4">
                        <i class="bi bi-inbox text-muted" style="font-size: 2rem;"></i>
                        <p class="text-muted mt-2">No hay formularios ${this.filtroEstado ? 'en estado ' + this.filtroEstado : ''}</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = this.formularios.map(form => {
            const estadoBadge = this.getEstadoBadge(form.estado);
            const fecha = this.formatDate(form.updated_at || form.created_at);
            const integridad = this.calculateIntegrity(form);
            
            return `
                <tr onclick="AuditorDashboard.verDetalleFormulario(${form.id})" style="cursor: pointer;">
                    <td><strong>#${form.id}</strong></td>
                    <td>${form.mesa_codigo || 'N/A'}</td>
                    <td>${form.puesto_nombre || 'N/A'}</td>
                    <td>${form.municipio_nombre || 'N/A'}</td>
                    <td>${form.testigo_nombre || 'N/A'}</td>
                    <td class="text-center">${form.total_votos || 0}</td>
                    <td class="text-center">${estadoBadge}</td>
                    <td class="text-center">
                        <span class="badge bg-${integridad.class}">${integridad.score}%</span>
                    </td>
                    <td class="text-center">
                        <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); AuditorDashboard.verDetalleFormulario(${form.id})">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-info" onclick="event.stopPropagation(); AuditorDashboard.verificarFormulario(${form.id})">
                            <i class="bi bi-shield-check"></i>
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    },

    /**
     * Renderizar error en formularios
     */
    renderFormulariosError() {
        const tbody = document.querySelector('#tabla-formularios tbody');
        if (!tbody) return;
        
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4">
                    <i class="bi bi-exclamation-triangle text-danger" style="font-size: 2rem;"></i>
                    <p class="text-danger mt-2">Error al cargar formularios</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="AuditorDashboard.loadFormularios()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </td>
            </tr>
        `;
    },

    /**
     * Cargar incidentes
     */
    async loadIncidentes() {
        try {
            const response = await APIClient.get('/auditor/incidentes', { limit: 50 });
            
            if (response.success) {
                this.incidentes = response.data || [];
                this.renderIncidentes();
            } else {
                throw new Error(response.error || 'Error al cargar incidentes');
            }
        } catch (error) {
            console.error('[Auditor] Error loading incidentes:', error);
            this.renderIncidentesError();
        }
    },

    /**
     * Renderizar incidentes
     */
    renderIncidentes() {
        const tbody = document.querySelector('#tabla-incidentes tbody');
        if (!tbody) return;
        
        if (this.incidentes.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-4">
                        <i class="bi bi-shield-check text-success" style="font-size: 2rem;"></i>
                        <p class="text-muted mt-2">No hay incidentes reportados</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = this.incidentes.map(inc => {
            const severidadBadge = this.getSeveridadBadge(inc.severidad);
            const estadoBadge = this.getEstadoIncidenteBadge(inc.estado);
            const fecha = this.formatDate(inc.fecha_reporte);
            
            return `
                <tr onclick="AuditorDashboard.verDetalleIncidente(${inc.id})" style="cursor: pointer;">
                    <td>${inc.tipo_incidente_label || inc.tipo_incidente}</td>
                    <td>${inc.titulo || 'Sin título'}</td>
                    <td>${inc.puesto_nombre || 'N/A'}</td>
                    <td class="text-center">${severidadBadge}</td>
                    <td>${inc.reportado_por || 'N/A'}</td>
                    <td><small>${fecha}</small></td>
                    <td class="text-center">${estadoBadge}</td>
                </tr>
            `;
        }).join('');
    },

    /**
     * Renderizar error en incidentes
     */
    renderIncidentesError() {
        const tbody = document.querySelector('#tabla-incidentes tbody');
        if (!tbody) return;
        
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4">
                    <i class="bi bi-exclamation-triangle text-danger" style="font-size: 2rem;"></i>
                    <p class="text-danger mt-2">Error al cargar incidentes</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="AuditorDashboard.loadIncidentes()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </td>
            </tr>
        `;
    },

    /**
     * Cargar delitos electorales
     */
    async loadDelitos() {
        try {
            const response = await APIClient.get('/auditor/delitos', { limit: 50 });
            
            if (response.success) {
                this.delitos = response.data || [];
                this.renderDelitos();
            } else {
                throw new Error(response.error || 'Error al cargar delitos');
            }
        } catch (error) {
            console.error('[Auditor] Error loading delitos:', error);
            this.renderDelitosError();
        }
    },

    /**
     * Renderizar delitos
     */
    renderDelitos() {
        const tbody = document.querySelector('#tabla-delitos tbody');
        if (!tbody) return;
        
        if (this.delitos.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-4">
                        <i class="bi bi-shield-check text-success" style="font-size: 2rem;"></i>
                        <p class="text-muted mt-2">No hay delitos electorales reportados</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = this.delitos.map(delito => {
            const gravedadBadge = this.getGravedadBadge(delito.gravedad);
            const estadoBadge = this.getEstadoDelitoBadge(delito.estado);
            const fecha = this.formatDate(delito.fecha_reporte);
            
            return `
                <tr onclick="AuditorDashboard.verDetalleDelito(${delito.id})" style="cursor: pointer;">
                    <td>${delito.tipo_delito_label || delito.tipo_delito}</td>
                    <td>${delito.titulo || 'Sin título'}</td>
                    <td>${delito.puesto_nombre || 'N/A'}</td>
                    <td class="text-center">${gravedadBadge}</td>
                    <td>${delito.reportado_por || 'N/A'}</td>
                    <td><small>${fecha}</small></td>
                    <td class="text-center">${estadoBadge}</td>
                </tr>
            `;
        }).join('');
    },

    /**
     * Renderizar error en delitos
     */
    renderDelitosError() {
        const tbody = document.querySelector('#tabla-delitos tbody');
        if (!tbody) return;
        
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4">
                    <i class="bi bi-exclamation-triangle text-danger" style="font-size: 2rem;"></i>
                    <p class="text-danger mt-2">Error al cargar delitos electorales</p>
                    <button class="btn btn-sm btn-outline-primary" onclick="AuditorDashboard.loadDelitos()">
                        <i class="bi bi-arrow-clockwise"></i> Reintentar
                    </button>
                </td>
            </tr>
        `;
    },

    /**
     * Cargar anomalías detectadas
     */
    async loadAnomalias() {
        try {
            const response = await APIClient.get('/auditor/detect-anomalies');
            
            if (response.success) {
                this.discrepancias = response.data || [];
                this.renderAnomalias();
            } else {
                throw new Error(response.error || 'Error al detectar anomalías');
            }
        } catch (error) {
            console.error('[Auditor] Error loading anomalias:', error);
            this.renderAnomaliasError();
        }
    },

    /**
     * Renderizar anomalías
     */
    renderAnomalias() {
        const container = document.getElementById('anomalias-container');
        if (!container) return;
        
        if (this.discrepancias.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-check-circle text-success" style="font-size: 2rem;"></i>
                    <p class="text-success mt-2">No se detectaron anomalías</p>
                    <small class="text-muted">Sistema funcionando correctamente</small>
                </div>
            `;
            return;
        }
        
        // Agrupar por severidad
        const criticas = this.discrepancias.filter(d => d.severidad === 'critica');
        const altas = this.discrepancias.filter(d => d.severidad === 'alta');
        const medias = this.discrepancias.filter(d => d.severidad === 'media');
        const bajas = this.discrepancias.filter(d => d.severidad === 'baja');
        
        let html = '';
        
        // Anomalías críticas
        if (criticas.length > 0) {
            html += `
                <div class="alert alert-danger">
                    <h6 class="alert-heading">
                        <i class="bi bi-exclamation-octagon"></i> Anomalías Críticas (${criticas.length})
                    </h6>
                    ${criticas.slice(0, 5).map(a => this.renderAnomaliaItem(a)).join('')}
                    ${criticas.length > 5 ? `<small class="text-muted">Y ${criticas.length - 5} más...</small>` : ''}
                </div>
            `;
        }
        
        // Anomalías altas
        if (altas.length > 0) {
            html += `
                <div class="alert alert-warning">
                    <h6 class="alert-heading">
                        <i class="bi bi-exclamation-triangle"></i> Anomalías Altas (${altas.length})
                    </h6>
                    ${altas.slice(0, 3).map(a => this.renderAnomaliaItem(a)).join('')}
                    ${altas.length > 3 ? `<small class="text-muted">Y ${altas.length - 3} más...</small>` : ''}
                </div>
            `;
        }
        
        // Anomalías medias (solo mostrar si no hay críticas o altas)
        if (medias.length > 0 && criticas.length === 0 && altas.length === 0) {
            html += `
                <div class="alert alert-info">
                    <h6 class="alert-heading">
                        <i class="bi bi-info-circle"></i> Anomalías Medias (${medias.length})
                    </h6>
                    ${medias.slice(0, 3).map(a => this.renderAnomaliaItem(a)).join('')}
                </div>
            `;
        }
        
        container.innerHTML = html;
    },

    /**
     * Renderizar item de anomalía
     */
    renderAnomaliaItem(anomalia) {
        return `
            <div class="mb-2 p-2 border-start border-3 border-${this.getSeverityClass(anomalia.severidad)} bg-light">
                <strong>${anomalia.tipo}</strong>: ${anomalia.descripcion}
                <br><small class="text-muted">
                    ${anomalia.ubicacion || 'Ubicación no especificada'} | 
                    Detectado: ${this.formatDate(anomalia.fecha_deteccion)}
                </small>
            </div>
        `;
    },

    /**
     * Renderizar error en anomalías
     */
    renderAnomaliasError() {
        const container = document.getElementById('anomalias-container');
        if (!container) return;
        
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-exclamation-triangle text-danger" style="font-size: 2rem;"></i>
                <p class="text-danger mt-2">Error al detectar anomalías</p>
                <button class="btn btn-sm btn-outline-primary" onclick="AuditorDashboard.loadAnomalias()">
                    <i class="bi bi-arrow-clockwise"></i> Reintentar
                </button>
            </div>
        `;
    },

    /**
     * Cargar estadísticas generales
     */
    async loadStats() {
        try {
            const response = await APIClient.get('/auditor/stats');
            
            if (response.success) {
                this.updateStatsCards(response.data);
            } else {
                throw new Error(response.error || 'Error al cargar estadísticas');
            }
        } catch (error) {
            console.error('[Auditor] Error loading stats:', error);
            this.updateStatsCardsError();
        }
    },

    /**
     * Actualizar tarjetas de estadísticas
     */
    updateStatsCards(stats) {
        // Total de formularios auditados
        const formulariosElement = document.getElementById('stat-formularios-auditados');
        if (formulariosElement) {
            formulariosElement.textContent = stats.formularios_auditados || 0;
        }
        
        const formulariosInfoElement = document.getElementById('stat-formularios-info');
        if (formulariosInfoElement) {
            formulariosInfoElement.textContent = `${stats.total_formularios || 0} formularios totales`;
        }
        
        // Anomalías detectadas
        const anomaliasElement = document.getElementById('stat-anomalias');
        if (anomaliasElement) {
            anomaliasElement.textContent = stats.anomalias_detectadas || 0;
        }
        
        const anomaliasInfoElement = document.getElementById('stat-anomalias-info');
        if (anomaliasInfoElement) {
            const criticas = stats.anomalias_criticas || 0;
            anomaliasInfoElement.textContent = criticas > 0 ? `${criticas} críticas` : 'Bajo control';
        }
        
        // Incidentes reportados
        const incidentesElement = document.getElementById('stat-incidentes');
        if (incidentesElement) {
            incidentesElement.textContent = stats.incidentes_reportados || 0;
        }
        
        const incidentesInfoElement = document.getElementById('stat-incidentes-info');
        if (incidentesInfoElement) {
            const pendientes = stats.incidentes_pendientes || 0;
            incidentesInfoElement.textContent = `${pendientes} pendientes`;
        }
        
        // Progreso de auditoría
        const progresoElement = document.getElementById('stat-progreso');
        if (progresoElement) {
            const porcentaje = stats.porcentaje_auditado || 0;
            progresoElement.textContent = `${porcentaje.toFixed(1)}%`;
        }
        
        const progresoInfoElement = document.getElementById('stat-progreso-info');
        if (progresoInfoElement) {
            progresoInfoElement.textContent = 'Auditoría completada';
        }
    },

    /**
     * Actualizar tarjetas con error
     */
    updateStatsCardsError() {
        const elements = [
            'stat-formularios-auditados',
            'stat-anomalias', 
            'stat-incidentes',
            'stat-progreso'
        ];
        
        elements.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = 'Error';
            }
        });
    },

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Filtros de formularios
        const filtroEstado = document.getElementById('filtro-estado-formularios');
        if (filtroEstado) {
            filtroEstado.addEventListener('change', (e) => {
                this.filtroEstado = e.target.value;
                this.loadFormularios();
            });
        }
        
        // Búsqueda de formularios
        const searchInput = document.getElementById('buscar-formulario');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.buscarFormularios(e.target.value);
            });
        }
        
        // Tabs
        const tabs = document.querySelectorAll('[data-bs-toggle="tab"]');
        tabs.forEach(tab => {
            tab.addEventListener('shown.bs.tab', (e) => {
                const targetId = e.target.getAttribute('data-bs-target');
                this.onTabShown(targetId);
            });
        });
        
        // Botones de acción
        const btnExportar = document.getElementById('btn-exportar-auditoria');
        if (btnExportar) {
            btnExportar.addEventListener('click', () => this.exportarReporte());
        }
        
        const btnVerificar = document.getElementById('btn-verificar-integridad');
        if (btnVerificar) {
            btnVerificar.addEventListener('click', () => this.verificarIntegridad());
        }
        
        const btnDetectar = document.getElementById('btn-detectar-anomalias');
        if (btnDetectar) {
            btnDetectar.addEventListener('click', () => this.detectarAnomalias());
        }
    },

    /**
     * Manejar cambio de tab
     */
    onTabShown(targetId) {
        switch (targetId) {
            case '#tab-logs':
                this.loadSystemLogs();
                break;
            case '#tab-actividad':
                this.loadUserActivity();
                break;
            case '#tab-formularios':
                this.loadFormularios();
                break;
            case '#tab-incidentes':
                this.loadIncidentes();
                break;
            case '#tab-delitos':
                this.loadDelitos();
                break;
            case '#tab-anomalias':
                this.loadAnomalias();
                break;
            case '#tab-reportes':
                this.loadReportes();
                break;
        }
    },

    /**
     * Iniciar auto-refresh
     */
    startAutoRefresh() {
        this.autoRefreshInterval = setInterval(() => {
            console.log('[Auditor] Auto-refresh ejecutándose...');
            this.loadStats();
            this.loadAnomalias();
            
            // Solo refrescar la tab activa
            const activeTab = document.querySelector('.tab-pane.active');
            if (activeTab) {
                const tabId = '#' + activeTab.id;
                this.onTabShown(tabId);
            }
        }, 30000); // 30 segundos
    },

    /**
     * Detener auto-refresh
     */
    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
    },

    /**
     * Ver detalle de formulario
     */
    async verDetalleFormulario(formularioId) {
        try {
            const response = await APIClient.get(`/formularios/${formularioId}`);
            
            if (response.success) {
                this.mostrarModalDetalleFormulario(response.data);
            } else {
                throw new Error(response.error || 'Error al cargar formulario');
            }
        } catch (error) {
            console.error('[Auditor] Error loading formulario:', error);
            Utils.showError('Error al cargar detalle del formulario');
        }
    },

    /**
     * Mostrar modal con detalle del formulario
     */
    mostrarModalDetalleFormulario(formulario) {
        // TODO: Implementar modal completo
        const integridad = this.calculateIntegrity(formulario);
        
        Utils.showInfo(`
            Formulario #${formulario.id}
            Estado: ${formulario.estado}
            Mesa: ${formulario.mesa_codigo}
            Total Votos: ${formulario.total_votos}
            Integridad: ${integridad.score}%
        `);
    },

    /**
     * Ver detalle de incidente
     */
    async verDetalleIncidente(incidenteId) {
        try {
            const response = await APIClient.get(`/incidentes-delitos/incidentes/${incidenteId}`);
            
            if (response.success) {
                this.mostrarModalDetalleIncidente(response.data);
            } else {
                throw new Error(response.error || 'Error al cargar incidente');
            }
        } catch (error) {
            console.error('[Auditor] Error loading incidente:', error);
            Utils.showError('Error al cargar detalle del incidente');
        }
    },

    /**
     * Mostrar modal con detalle del incidente
     */
    mostrarModalDetalleIncidente(incidente) {
        // TODO: Implementar modal completo
        Utils.showInfo(`
            Incidente #${incidente.id}
            Tipo: ${incidente.tipo_incidente}
            Severidad: ${incidente.severidad}
            Estado: ${incidente.estado}
            Descripción: ${incidente.descripcion}
        `);
    },

    /**
     * Ver detalle de delito
     */
    async verDetalleDelito(delitoId) {
        try {
            const response = await APIClient.get(`/incidentes-delitos/delitos/${delitoId}`);
            
            if (response.success) {
                this.mostrarModalDetalleDelito(response.data);
            } else {
                throw new Error(response.error || 'Error al cargar delito');
            }
        } catch (error) {
            console.error('[Auditor] Error loading delito:', error);
            Utils.showError('Error al cargar detalle del delito');
        }
    },

    /**
     * Mostrar modal con detalle del delito
     */
    mostrarModalDetalleDelito(delito) {
        // TODO: Implementar modal completo
        Utils.showInfo(`
            Delito Electoral #${delito.id}
            Tipo: ${delito.tipo_delito}
            Gravedad: ${delito.gravedad}
            Estado: ${delito.estado}
            Descripción: ${delito.descripcion}
        `);
    },

    /**
     * Verificar formulario específico
     */
    async verificarFormulario(formularioId) {
        try {
            Utils.showInfo('Verificando integridad del formulario...');
            
            const response = await APIClient.post('/auditor/verify-formularios', {
                formulario_ids: [formularioId]
            });
            
            if (response.success) {
                const resultado = response.data.resultados[0];
                if (resultado.valido) {
                    Utils.showSuccess('Formulario verificado correctamente');
                } else {
                    Utils.showWarning(`Formulario con inconsistencias: ${resultado.errores.join(', ')}`);
                }
            } else {
                throw new Error(response.error || 'Error en verificación');
            }
        } catch (error) {
            console.error('[Auditor] Error verificando formulario:', error);
            Utils.showError('Error al verificar formulario');
        }
    },

    /**
     * Verificar integridad general
     */
    async verificarIntegridad() {
        try {
            Utils.showInfo('Verificando integridad del sistema...');
            
            const response = await APIClient.post('/auditor/check-integrity');
            
            if (response.success) {
                const resultado = response.data;
                Utils.showSuccess(`
                    Verificación completada:
                    - Formularios verificados: ${resultado.formularios_verificados}
                    - Errores encontrados: ${resultado.errores_encontrados}
                    - Integridad general: ${resultado.porcentaje_integridad}%
                `);
            } else {
                throw new Error(response.error || 'Error en verificación');
            }
        } catch (error) {
            console.error('[Auditor] Error verificando integridad:', error);
            Utils.showError('Error al verificar integridad del sistema');
        }
    },

    /**
     * Detectar anomalías
     */
    async detectarAnomalias() {
        try {
            Utils.showInfo('Detectando anomalías...');
            
            const response = await APIClient.post('/auditor/detect-anomalies');
            
            if (response.success) {
                this.discrepancias = response.data || [];
                this.renderAnomalias();
                
                const total = this.discrepancias.length;
                const criticas = this.discrepancias.filter(d => d.severidad === 'critica').length;
                
                if (total === 0) {
                    Utils.showSuccess('No se detectaron anomalías');
                } else {
                    Utils.showWarning(`Se detectaron ${total} anomalía(s), ${criticas} crítica(s)`);
                }
            } else {
                throw new Error(response.error || 'Error en detección');
            }
        } catch (error) {
            console.error('[Auditor] Error detectando anomalías:', error);
            Utils.showError('Error al detectar anomalías');
        }
    },

    /**
     * Cargar reportes disponibles
     */
    async loadReportes() {
        const container = document.getElementById('reportes-container');
        if (!container) return;
        
        container.innerHTML = `
            <div class="row">
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="bi bi-file-earmark-text"></i> Reporte de Auditoría
                            </h5>
                            <p class="card-text">Reporte completo de la auditoría electoral</p>
                            <button class="btn btn-primary" onclick="AuditorDashboard.generarReporte('auditoria')">
                                <i class="bi bi-download"></i> Generar
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="bi bi-shield-check"></i> Reporte de Cumplimiento
                            </h5>
                            <p class="card-text">Análisis de cumplimiento normativo</p>
                            <button class="btn btn-success" onclick="AuditorDashboard.generarReporte('cumplimiento')">
                                <i class="bi bi-download"></i> Generar
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="bi bi-speedometer2"></i> Reporte de Performance
                            </h5>
                            <p class="card-text">Métricas de rendimiento del sistema</p>
                            <button class="btn btn-info" onclick="AuditorDashboard.generarReporte('performance')">
                                <i class="bi bi-download"></i> Generar
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">
                                <i class="bi bi-lock"></i> Reporte de Seguridad
                            </h5>
                            <p class="card-text">Análisis de seguridad y accesos</p>
                            <button class="btn btn-warning" onclick="AuditorDashboard.generarReporte('seguridad')">
                                <i class="bi bi-download"></i> Generar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    },

    /**
     * Generar reporte específico
     */
    async generarReporte(tipo) {
        try {
            Utils.showInfo(`Generando reporte de ${tipo}...`);
            
            const response = await APIClient.post(`/auditor/generate-${tipo}-report`);
            
            if (response.success) {
                // Descargar archivo
                const blob = new Blob([response.data], { type: 'application/pdf' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `reporte_${tipo}_${new Date().getTime()}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                
                Utils.showSuccess(`Reporte de ${tipo} generado exitosamente`);
            } else {
                throw new Error(response.error || 'Error al generar reporte');
            }
        } catch (error) {
            console.error(`[Auditor] Error generando reporte ${tipo}:`, error);
            Utils.showError(`Error al generar reporte de ${tipo}`);
        }
    },

    /**
     * Exportar reporte general
     */
    async exportarReporte() {
        try {
            Utils.showInfo('Exportando datos de auditoría...');
            
            const response = await APIClient.get('/auditor/export', {
                formato: 'csv'
            });
            
            if (response.success) {
                // Descargar CSV
                const csvContent = response.data;
                const blob = new Blob([csvContent], { type: 'text/csv' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `auditoria_${new Date().getTime()}.csv`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                
                Utils.showSuccess('Datos exportados exitosamente');
            } else {
                throw new Error(response.error || 'Error al exportar');
            }
        } catch (error) {
            console.error('[Auditor] Error exportando:', error);
            Utils.showError('Error al exportar datos de auditoría');
        }
    },

    /**
     * Buscar formularios
     */
    buscarFormularios(query) {
        if (!query) {
            this.renderFormulariosTable();
            return;
        }
        
        const filtered = this.formularios.filter(f => {
            const searchText = `${f.id} ${f.mesa_codigo} ${f.puesto_nombre} ${f.testigo_nombre}`.toLowerCase();
            return searchText.includes(query.toLowerCase());
        });
        
        // Renderizar resultados filtrados
        const tbody = document.querySelector('#tabla-formularios tbody');
        if (!tbody) return;
        
        if (filtered.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="9" class="text-center py-4">
                        <i class="bi bi-search text-muted" style="font-size: 2rem;"></i>
                        <p class="text-muted mt-2">No se encontraron formularios con "${query}"</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = filtered.map(form => {
            const estadoBadge = this.getEstadoBadge(form.estado);
            const integridad = this.calculateIntegrity(form);
            
            return `
                <tr onclick="AuditorDashboard.verDetalleFormulario(${form.id})" style="cursor: pointer;">
                    <td><strong>#${form.id}</strong></td>
                    <td>${form.mesa_codigo || 'N/A'}</td>
                    <td>${form.puesto_nombre || 'N/A'}</td>
                    <td>${form.municipio_nombre || 'N/A'}</td>
                    <td>${form.testigo_nombre || 'N/A'}</td>
                    <td class="text-center">${form.total_votos || 0}</td>
                    <td class="text-center">${estadoBadge}</td>
                    <td class="text-center">
                        <span class="badge bg-${integridad.class}">${integridad.score}%</span>
                    </td>
                    <td class="text-center">
                        <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); AuditorDashboard.verDetalleFormulario(${form.id})">
                            <i class="bi bi-eye"></i>
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    },

    // ============================================================================
    // FUNCIONES AUXILIARES
    // ============================================================================

    /**
     * Calcular integridad de formulario
     */
    calculateIntegrity(formulario) {
        let score = 100;
        let issues = [];
        
        // Verificar campos obligatorios
        if (!formulario.total_votos || formulario.total_votos === 0) {
            score -= 20;
            issues.push('Sin votos registrados');
        }
        
        // Verificar coherencia de totales
        const calculado = (formulario.votos_validos || 0) + (formulario.votos_nulos || 0) + (formulario.votos_blanco || 0);
        if (Math.abs(calculado - (formulario.total_votos || 0)) > 0) {
            score -= 15;
            issues.push('Inconsistencia en totales');
        }
        
        // Verificar estado
        if (formulario.estado === 'rechazado') {
            score -= 30;
            issues.push('Formulario rechazado');
        }
        
        // Verificar fecha
        if (!formulario.created_at) {
            score -= 10;
            issues.push('Sin fecha de creación');
        }
        
        score = Math.max(0, score);
        
        return {
            score: score,
            class: score >= 90 ? 'success' : score >= 70 ? 'warning' : 'danger',
            issues: issues
        };
    },

    /**
     * Obtener badge de estado
     */
    getEstadoBadge(estado) {
        const badges = {
            'borrador': '<span class="badge bg-secondary">Borrador</span>',
            'pendiente': '<span class="badge bg-warning text-dark">Pendiente</span>',
            'validado': '<span class="badge bg-success">Validado</span>',
            'rechazado': '<span class="badge bg-danger">Rechazado</span>',
            'en_revision': '<span class="badge bg-info">En Revisión</span>'
        };
        return badges[estado] || `<span class="badge bg-secondary">${estado}</span>`;
    },

    /**
     * Obtener badge de severidad
     */
    getSeveridadBadge(severidad) {
        const badges = {
            'baja': '<span class="badge bg-info">Baja</span>',
            'media': '<span class="badge bg-warning">Media</span>',
            'alta': '<span class="badge bg-danger">Alta</span>',
            'critica': '<span class="badge bg-dark">Crítica</span>'
        };
        return badges[severidad] || `<span class="badge bg-secondary">${severidad}</span>`;
    },

    /**
     * Obtener badge de gravedad
     */
    getGravedadBadge(gravedad) {
        const badges = {
            'leve': '<span class="badge bg-info">Leve</span>',
            'grave': '<span class="badge bg-warning">Grave</span>',
            'muy_grave': '<span class="badge bg-danger">Muy Grave</span>'
        };
        return badges[gravedad] || `<span class="badge bg-secondary">${gravedad}</span>`;
    },

    /**
     * Obtener badge de estado de incidente
     */
    getEstadoIncidenteBadge(estado) {
        const badges = {
            'reportado': '<span class="badge bg-warning">Reportado</span>',
            'en_revision': '<span class="badge bg-info">En Revisión</span>',
            'resuelto': '<span class="badge bg-success">Resuelto</span>',
            'escalado': '<span class="badge bg-danger">Escalado</span>'
        };
        return badges[estado] || `<span class="badge bg-secondary">${estado}</span>`;
    },

    /**
     * Obtener badge de estado de delito
     */
    getEstadoDelitoBadge(estado) {
        const badges = {
            'reportado': '<span class="badge bg-warning">Reportado</span>',
            'en_investigacion': '<span class="badge bg-info">En Investigación</span>',
            'investigado': '<span class="badge bg-success">Investigado</span>',
            'archivado': '<span class="badge bg-secondary">Archivado</span>'
        };
        return badges[estado] || `<span class="badge bg-secondary">${estado}</span>`;
    },

    /**
     * Obtener clase CSS para severidad
     */
    getSeverityClass(severidad) {
        const classes = {
            'baja': 'info',
            'media': 'warning', 
            'alta': 'danger',
            'critica': 'dark'
        };
        return classes[severidad] || 'secondary';
    },

    /**
     * Obtener clase CSS para rol
     */
    getRoleClass(rol) {
        const classes = {
            'testigo_electoral': 'primary',
            'coordinador_puesto': 'info',
            'coordinador_municipal': 'success',
            'coordinador_departamental': 'warning',
            'auditor': 'danger',
            'super_admin': 'dark'
        };
        return classes[rol] || 'secondary';
    },

    /**
     * Formatear fecha
     */
    formatDate(dateString) {
        if (!dateString) return 'N/A';
        
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-CO', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (error) {
            return 'Fecha inválida';
        }
    },

    /**
     * Función de logout
     */
    async logout() {
        try {
            this.stopAutoRefresh();
            await APIClient.logout();
        } catch (error) {
            console.error('[Auditor] Error al cerrar sesión:', error);
        } finally {
            localStorage.clear();
            window.location.href = '/auth/login';
        }
    }
};

// Limpiar interval al salir
window.addEventListener('beforeunload', function() {
    AuditorDashboard.stopAutoRefresh();
});

// Exponer globalmente
window.AuditorDashboard = AuditorDashboard;

// Auto-inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('[Auditor] DOM cargado, inicializando dashboard...');
    AuditorDashboard.init();
});

// ============================================================================
// FUNCIONES ADICIONALES PARA EL TEMPLATE HTML
// ============================================================================

/**
 * Mostrar tab de auditoría específico
 */
function showAuditTab(tabName) {
    // Ocultar todos los contenidos
    const contents = document.querySelectorAll('.audit-content');
    contents.forEach(content => {
        content.classList.remove('active');
    });
    
    // Remover clase active de todos los tabs
    const tabs = document.querySelectorAll('.audit-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Mostrar contenido seleccionado
    const selectedContent = document.getElementById(`audit-${tabName}`);
    if (selectedContent) {
        selectedContent.classList.add('active');
    }
    
    // Activar tab seleccionado
    const selectedTab = event.target;
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Cargar datos específicos del tab
    AuditorDashboard.onTabShown(`#tab-${tabName}`);
}

/**
 * Cargar logs del sistema
 */
async function cargarLogs() {
    await AuditorDashboard.loadSystemLogs();
}

/**
 * Filtrar logs según criterios seleccionados
 */
function filtrarLogs() {
    const fecha = document.getElementById('filtro-fecha-logs')?.value;
    const usuario = document.getElementById('filtro-usuario-logs')?.value;
    const accion = document.getElementById('filtro-accion-logs')?.value;
    const severidad = document.getElementById('filtro-severidad-logs')?.value;
    
    // TODO: Implementar filtrado de logs
    console.log('Filtros aplicados:', { fecha, usuario, accion, severidad });
    AuditorDashboard.loadSystemLogs();
}

/**
 * Ejecutar verificación de formularios
 */
async function ejecutarVerificacionFormularios() {
    try {
        Utils.showInfo('Ejecutando verificación de formularios...');
        
        const response = await APIClient.post('/auditor/verify-formularios');
        
        if (response.success) {
            const resultado = response.data;
            
            // Actualizar contadores
            document.getElementById('formularios-total').textContent = resultado.total_formularios || 0;
            document.getElementById('formularios-validos').textContent = resultado.formularios_validos || 0;
            document.getElementById('formularios-inconsistentes').textContent = resultado.formularios_inconsistentes || 0;
            document.getElementById('formularios-duplicados').textContent = resultado.formularios_duplicados || 0;
            
            // Mostrar resultado detallado
            const container = document.getElementById('resultado-verificacion-formularios');
            if (container && resultado.detalles) {
                container.innerHTML = `
                    <div class="alert alert-info">
                        <h6>Resultado de la Verificación</h6>
                        <ul class="mb-0">
                            ${resultado.detalles.map(detalle => `<li>${detalle}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            Utils.showSuccess('Verificación de formularios completada');
        } else {
            throw new Error(response.error || 'Error en verificación');
        }
    } catch (error) {
        console.error('[Auditor] Error en verificación de formularios:', error);
        Utils.showError('Error al verificar formularios');
    }
}

/**
 * Ejecutar verificación de integridad
 */
async function ejecutarVerificacionIntegridad() {
    await AuditorDashboard.verificarIntegridad();
}

/**
 * Filtrar anomalías
 */
function filtrarAnomalias() {
    const tipo = document.getElementById('filtro-tipo-anomalia')?.value;
    const severidad = document.getElementById('filtro-severidad-anomalia')?.value;
    
    // TODO: Implementar filtrado de anomalías
    console.log('Filtros de anomalías:', { tipo, severidad });
    AuditorDashboard.loadAnomalias();
}

/**
 * Ejecutar detección de anomalías
 */
async function ejecutarDeteccionAnomalias() {
    await AuditorDashboard.detectarAnomalias();
}

/**
 * Generar reporte de auditoría general
 */
async function generarReporteAuditoria() {
    await AuditorDashboard.generarReporte('auditoria');
}

/**
 * Generar reporte de cumplimiento
 */
async function generarReporteCumplimiento() {
    await AuditorDashboard.generarReporte('cumplimiento');
}

/**
 * Generar reporte de performance
 */
async function generarReportePerformance() {
    await AuditorDashboard.generarReporte('performance');
}

/**
 * Generar reporte de seguridad
 */
async function generarReporteSeguridad() {
    await AuditorDashboard.generarReporte('seguridad');
}

/**
 * Exportar datos de auditoría
 */
async function exportarDatosAuditoria() {
    await AuditorDashboard.exportarReporte();
}

/**
 * Mostrar alertas críticas
 */
async function mostrarAlertas() {
    try {
        const response = await APIClient.get('/auditor/alertas-criticas');
        
        if (response.success) {
            const alertas = response.data || [];
            
            const container = document.getElementById('contenido-alertas');
            if (container) {
                if (alertas.length === 0) {
                    container.innerHTML = `
                        <div class="text-center py-4">
                            <i class="bi bi-check-circle text-success" style="font-size: 3rem;"></i>
                            <h5 class="text-success mt-3">No hay alertas críticas</h5>
                            <p class="text-muted">El sistema está funcionando correctamente</p>
                        </div>
                    `;
                } else {
                    container.innerHTML = alertas.map(alerta => `
                        <div class="alert alert-danger">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <h6 class="alert-heading">${alerta.titulo}</h6>
                                    <p class="mb-1">${alerta.descripcion}</p>
                                    <small class="text-muted">
                                        Detectado: ${AuditorDashboard.formatDate(alerta.fecha_deteccion)}
                                    </small>
                                </div>
                                <span class="badge bg-danger">${alerta.severidad}</span>
                            </div>
                        </div>
                    `).join('');
                }
            }
            
            // Mostrar modal
            const modal = new bootstrap.Modal(document.getElementById('modalAlertas'));
            modal.show();
        }
    } catch (error) {
        console.error('[Auditor] Error cargando alertas:', error);
        Utils.showError('Error al cargar alertas críticas');
    }
}

/**
 * Marcar alertas como atendidas
 */
async function marcarAlertasAtendidas() {
    try {
        const response = await APIClient.post('/auditor/marcar-alertas-atendidas');
        
        if (response.success) {
            Utils.showSuccess('Alertas marcadas como atendidas');
            
            // Ocultar contador de alertas
            const counter = document.getElementById('alert-counter');
            if (counter) {
                counter.classList.add('hidden');
            }
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalAlertas'));
            if (modal) {
                modal.hide();
            }
        } else {
            throw new Error(response.error || 'Error al marcar alertas');
        }
    } catch (error) {
        console.error('[Auditor] Error marcando alertas:', error);
        Utils.showError('Error al marcar alertas como atendidas');
    }
}

/**
 * Función de logout global
 */
async function logout() {
    await AuditorDashboard.logout();
}

// ============================================================================
// FUNCIONES DE INICIALIZACIÓN ADICIONALES
// ============================================================================

/**
 * Actualizar contador de alertas críticas
 */
async function actualizarContadorAlertas() {
    try {
        const response = await APIClient.get('/auditor/count-alertas-criticas');
        
        if (response.success) {
            const count = response.data.count || 0;
            const counter = document.getElementById('alert-counter');
            const countElement = document.getElementById('alert-count');
            
            if (counter && countElement) {
                if (count > 0) {
                    countElement.textContent = count;
                    counter.classList.remove('hidden');
                } else {
                    counter.classList.add('hidden');
                }
            }
        }
    } catch (error) {
        console.error('[Auditor] Error actualizando contador de alertas:', error);
    }
}

/**
 * Inicializar gráficos con Chart.js
 */
function inicializarGraficos() {
    // Gráfico de actividad de usuarios
    const ctxActividad = document.getElementById('chart-actividad-usuarios');
    if (ctxActividad) {
        new Chart(ctxActividad, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                datasets: [{
                    label: 'Usuarios Activos',
                    data: [12, 19, 3, 5, 2, 3],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
    
    // Gráfico de usuarios por rol
    const ctxRoles = document.getElementById('chart-usuarios-por-rol');
    if (ctxRoles) {
        new Chart(ctxRoles, {
            type: 'doughnut',
            data: {
                labels: ['Testigos', 'Coordinadores', 'Auditores', 'Admins'],
                datasets: [{
                    data: [300, 50, 10, 5],
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
    
    // Gráfico de incidentes en el tiempo
    const ctxIncidentes = document.getElementById('chart-incidentes-tiempo');
    if (ctxIncidentes) {
        new Chart(ctxIncidentes, {
            type: 'bar',
            data: {
                labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                datasets: [{
                    label: 'Incidentes Reportados',
                    data: [12, 19, 3, 5, 2, 3, 7],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Gráfico de incidentes por severidad
    const ctxSeveridad = document.getElementById('chart-incidentes-severidad');
    if (ctxSeveridad) {
        new Chart(ctxSeveridad, {
            type: 'pie',
            data: {
                labels: ['Baja', 'Media', 'Alta', 'Crítica'],
                datasets: [{
                    data: [30, 20, 15, 5],
                    backgroundColor: [
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)',
                        'rgb(255, 99, 132)',
                        'rgb(128, 0, 128)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

// Extender la inicialización del dashboard
const originalInit = AuditorDashboard.init;
AuditorDashboard.init = async function() {
    await originalInit.call(this);
    
    // Inicializar funcionalidades adicionales
    actualizarContadorAlertas();
    inicializarGraficos();
    
    // Auto-actualizar contador de alertas cada 2 minutos
    setInterval(actualizarContadorAlertas, 120000);
};

console.log('[Auditor] Funciones adicionales cargadas correctamente');