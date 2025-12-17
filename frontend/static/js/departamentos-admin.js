/**
 * Gestión de departamentos habilitados - Panel de Administración
 */

class DepartamentosAdmin {
    constructor() {
        this.departamentosDisponibles = [];
        this.departamentosConfigurados = [];
        this.init();
    }

    async init() {
        console.log('🏛️ Inicializando gestión de departamentos...');
        await this.cargarDatos();
        this.setupEventListeners();
        this.renderizar();
        this.debugInfo();
    }

    async cargarDatos() {
        try {
            // Cargar departamentos disponibles
            const responseDisponibles = await APIClient.get('/super-admin/departamentos/disponibles');
            if (responseDisponibles.success && responseDisponibles.data) {
                this.departamentosDisponibles = responseDisponibles.data;
                console.log('Departamentos disponibles cargados:', this.departamentosDisponibles.length);
            } else {
                console.warn('No se pudieron cargar departamentos disponibles:', responseDisponibles);
                this.departamentosDisponibles = [];
            }

            // Cargar estado actual
            await this.cargarEstado();

        } catch (error) {
            console.error('Error cargando datos de departamentos:', error);
            Utils.showError('Error al cargar datos de departamentos: ' + error.message);
            
            // Inicializar arrays vacíos en caso de error
            this.departamentosDisponibles = [];
            this.departamentosConfigurados = [];
        }
    }

    async cargarEstado() {
        try {
            const response = await APIClient.get('/super-admin/departamentos/estado');
            if (response.success && response.data) {
                this.departamentosConfigurados = response.data;
                console.log('Estado de departamentos cargado:', this.departamentosConfigurados.length);
            } else {
                console.warn('No se pudo cargar estado de departamentos:', response);
                this.departamentosConfigurados = [];
            }
        } catch (error) {
            console.error('Error cargando estado de departamentos:', error);
            this.departamentosConfigurados = [];
        }
    }

    setupEventListeners() {
        // Botón para habilitar departamento
        document.getElementById('btnHabilitarDepartamento')?.addEventListener('click', () => {
            this.mostrarModalHabilitar();
        });

        // Botón para refrescar
        document.getElementById('btnRefrescarDepartamentos')?.addEventListener('click', () => {
            this.refrescar();
        });
    }

    renderizar() {
        this.renderizarTablaDisponibles();
        this.renderizarTablaConfigurados();
        this.renderizarEstadisticas();
    }

    renderizarTablaDisponibles() {
        const tbody = document.getElementById('tablaDisponiblesTBody');
        if (!tbody) return;

        tbody.innerHTML = '';

        this.departamentosDisponibles.forEach(depto => {
            const configurado = this.departamentosConfigurados.find(
                c => c.departamento_codigo === depto.departamento_codigo
            );

            const nombreDepartamento = depto.departamento_nombre || 'Departamento desconocido';
            const codigoDepartamento = depto.departamento_codigo || 'N/A';
            const totalMunicipios = depto.total_municipios || 0;
            const totalRegistros = depto.total_registros || 0;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${codigoDepartamento}</td>
                <td>${nombreDepartamento}</td>
                <td>${totalMunicipios}</td>
                <td>${totalRegistros.toLocaleString()}</td>
                <td>
                    ${configurado ? 
                        `<span class="badge bg-${configurado.habilitado ? 'success' : 'secondary'}">
                            ${configurado.habilitado ? 'Habilitado' : 'Deshabilitado'}
                            ${configurado.es_principal ? ' (Principal)' : ''}
                        </span>` : 
                        '<span class="badge bg-light text-dark">No configurado</span>'
                    }
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        ${!configurado || !configurado.habilitado ? 
                            `<button class="btn btn-success btn-sm" onclick="departamentosAdmin.habilitar('${codigoDepartamento}', false)" title="Habilitar">
                                <i class="bi bi-check-circle"></i>
                            </button>` : ''
                        }
                        ${configurado && configurado.habilitado && !configurado.es_principal ? 
                            `<button class="btn btn-primary btn-sm" onclick="departamentosAdmin.marcarPrincipal('${codigoDepartamento}')" title="Marcar como principal">
                                <i class="bi bi-star"></i>
                            </button>` : ''
                        }
                        ${configurado && configurado.habilitado ? 
                            `<button class="btn btn-warning btn-sm" onclick="departamentosAdmin.deshabilitar('${codigoDepartamento}')" title="Deshabilitar">
                                <i class="bi bi-x-circle"></i>
                            </button>` : ''
                        }
                        <button class="btn btn-info btn-sm" onclick="departamentosAdmin.cargarDatos('${codigoDepartamento}')" title="Cargar/Recargar datos">
                            <i class="bi bi-arrow-repeat"></i>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    renderizarTablaConfigurados() {
        const tbody = document.getElementById('tablaConfiguradosTBody');
        if (!tbody) return;

        tbody.innerHTML = '';

        this.departamentosConfigurados
            .filter(config => config.habilitado)
            .forEach(config => {
                const row = document.createElement('tr');
                row.className = config.es_principal ? 'table-primary' : '';
                
                const nombreDepartamento = config.departamento_nombre || 'Departamento desconocido';
                const codigoDepartamento = config.departamento_codigo || 'N/A';
                const totalMunicipios = config.total_municipios || 0;
                const totalPuestos = config.total_puestos || 0;
                const totalMesas = config.total_mesas || 0;
                const totalUsuarios = config.total_usuarios_creados || 0;
                
                row.innerHTML = `
                    <td>
                        ${nombreDepartamento}
                        ${config.es_principal ? '<i class="bi bi-star-fill text-warning ms-1" title="Principal"></i>' : ''}
                    </td>
                    <td>${totalMunicipios}</td>
                    <td>${totalPuestos}</td>
                    <td>${totalMesas}</td>
                    <td>${totalUsuarios}</td>
                    <td>
                        <small class="text-muted">
                            ${config.ultima_carga_at ? 
                                new Date(config.ultima_carga_at).toLocaleString() : 
                                'Nunca'
                            }
                        </small>
                    </td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            ${!config.es_principal ? 
                                `<button class="btn btn-primary btn-sm" onclick="departamentosAdmin.marcarPrincipal('${codigoDepartamento}')" title="Marcar como principal">
                                    <i class="bi bi-star"></i>
                                </button>` : ''
                            }
                            <button class="btn btn-info btn-sm" onclick="departamentosAdmin.cargarDatos('${codigoDepartamento}')" title="Recargar datos">
                                <i class="bi bi-arrow-repeat"></i>
                            </button>
                            <button class="btn btn-warning btn-sm" onclick="departamentosAdmin.deshabilitar('${codigoDepartamento}')" title="Deshabilitar">
                                <i class="bi bi-x-circle"></i>
                            </button>
                        </div>
                    </td>
                `;
                tbody.appendChild(row);
            });

        if (this.departamentosConfigurados.filter(c => c.habilitado).length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted py-4">
                        No hay departamentos habilitados
                    </td>
                </tr>
            `;
        }
    }

    renderizarEstadisticas() {
        const habilitados = this.departamentosConfigurados.filter(c => c.habilitado);
        const principal = habilitados.find(c => c.es_principal);

        // Estadísticas generales
        const statDepartamentosHabilitados = document.getElementById('statDepartamentosHabilitados');
        const statDepartamentoPrincipal = document.getElementById('statDepartamentoPrincipal');
        
        if (statDepartamentosHabilitados) {
            statDepartamentosHabilitados.textContent = habilitados.length;
        }
        
        if (statDepartamentoPrincipal) {
            statDepartamentoPrincipal.textContent = 
                principal && principal.departamento_nombre ? principal.departamento_nombre : 'Ninguno';
        }

        // Totales con validación de valores
        const totalMunicipios = habilitados.reduce((sum, d) => sum + (d.total_municipios || 0), 0);
        const totalPuestos = habilitados.reduce((sum, d) => sum + (d.total_puestos || 0), 0);
        const totalMesas = habilitados.reduce((sum, d) => sum + (d.total_mesas || 0), 0);
        const totalUsuarios = habilitados.reduce((sum, d) => sum + (d.total_usuarios_creados || 0), 0);

        const statTotalMunicipios = document.getElementById('statTotalMunicipios');
        const statTotalPuestos = document.getElementById('statTotalPuestos');
        const statTotalMesas = document.getElementById('statTotalMesas');
        const statTotalUsuarios = document.getElementById('statTotalUsuarios');
        
        if (statTotalMunicipios) statTotalMunicipios.textContent = totalMunicipios;
        if (statTotalPuestos) statTotalPuestos.textContent = totalPuestos;
        if (statTotalMesas) statTotalMesas.textContent = totalMesas;
        if (statTotalUsuarios) statTotalUsuarios.textContent = totalUsuarios;
    }

    async habilitar(departamentoCodigo, esPrincipal = false) {
        try {
            const depto = this.departamentosDisponibles.find(d => d.departamento_codigo === departamentoCodigo);
            
            if (!depto) {
                Utils.showError('Departamento no encontrado');
                return;
            }
            
            const mensaje = esPrincipal ? 
                `¿Habilitar ${depto.departamento_nombre} como departamento PRINCIPAL?\n\nEsto cargará automáticamente:\n• ${depto.total_municipios} municipios\n• ~${Math.round(depto.total_registros / 2)} puestos\n• ${depto.total_registros} mesas\n• Usuarios para todos los niveles` :
                `¿Habilitar el departamento ${depto.departamento_nombre}?\n\nEsto cargará automáticamente:\n• ${depto.total_municipios} municipios\n• ~${Math.round(depto.total_registros / 2)} puestos\n• ${depto.total_registros} mesas\n• Usuarios para todos los niveles`;

            if (!confirm(mensaje)) return;

            Utils.showInfo(`Habilitando ${depto.departamento_nombre}...`);

            const response = await APIClient.post('/super-admin/departamentos/habilitar', {
                departamento_codigo: departamentoCodigo,
                es_principal: esPrincipal,
                auto_cargar: true
            });

            if (response.success) {
                Utils.showSuccess(`Departamento ${depto.departamento_nombre} habilitado exitosamente`);
                await this.refrescar();
            } else {
                Utils.showError(response.error || 'Error al habilitar departamento');
            }

        } catch (error) {
            console.error('Error habilitando departamento:', error);
            Utils.showError('Error al habilitar departamento: ' + error.message);
        }
    }

    async deshabilitar(departamentoCodigo) {
        try {
            const config = this.departamentosConfigurados.find(c => c.departamento_codigo === departamentoCodigo);
            
            if (!config) {
                Utils.showError('Configuración de departamento no encontrada');
                return;
            }
            
            if (config.es_principal) {
                Utils.showError('No se puede deshabilitar el departamento principal. Marque otro como principal primero.');
                return;
            }

            const nombreDepartamento = config.departamento_nombre || 'Departamento desconocido';

            if (!confirm(`¿Deshabilitar el departamento ${nombreDepartamento}?\n\nEsto desactivará:\n• Todas las ubicaciones del departamento\n• Todos los usuarios del departamento\n\nLos datos no se eliminarán, solo se desactivarán.`)) {
                return;
            }

            Utils.showInfo(`Deshabilitando ${nombreDepartamento}...`);

            const response = await APIClient.post('/super-admin/departamentos/deshabilitar', {
                departamento_codigo: departamentoCodigo,
                desactivar_usuarios: true
            });

            if (response.success) {
                Utils.showSuccess(`Departamento ${nombreDepartamento} deshabilitado exitosamente`);
                await this.refrescar();
            } else {
                Utils.showError(response.error || 'Error al deshabilitar departamento');
            }

        } catch (error) {
            console.error('Error deshabilitando departamento:', error);
            Utils.showError('Error al deshabilitar departamento: ' + error.message);
        }
    }

    async marcarPrincipal(departamentoCodigo) {
        try {
            const depto = this.departamentosDisponibles.find(d => d.departamento_codigo === departamentoCodigo);
            
            if (!depto) {
                Utils.showError('Departamento no encontrado');
                return;
            }
            
            const nombreDepartamento = depto.departamento_nombre || 'Departamento desconocido';
            
            if (!confirm(`¿Marcar ${nombreDepartamento} como departamento PRINCIPAL?\n\nEsto quitará la marca principal del departamento actual.`)) {
                return;
            }

            Utils.showInfo(`Marcando ${nombreDepartamento} como principal...`);

            const response = await APIClient.post('/super-admin/departamentos/principal', {
                departamento_codigo: departamentoCodigo
            });

            if (response.success) {
                Utils.showSuccess(`${nombreDepartamento} es ahora el departamento principal`);
                await this.refrescar();
            } else {
                Utils.showError(response.error || 'Error al marcar como principal');
            }

        } catch (error) {
            console.error('Error marcando como principal:', error);
            Utils.showError('Error al marcar como principal: ' + error.message);
        }
    }

    async cargarDatos(departamentoCodigo) {
        try {
            const depto = this.departamentosDisponibles.find(d => d.departamento_codigo === departamentoCodigo);
            
            if (!depto) {
                Utils.showError('Departamento no encontrado');
                return;
            }
            
            if (!confirm(`¿Cargar/recargar datos del departamento ${depto.departamento_nombre}?\n\nEsto procesará todos los registros del archivo DIVIPOLA y creará/actualizará ubicaciones y usuarios.`)) {
                return;
            }

            Utils.showInfo(`Cargando datos de ${depto.departamento_nombre}...`);

            const response = await APIClient.post('/super-admin/departamentos/cargar-datos', {
                departamento_codigo: departamentoCodigo
            });

            if (response.success) {
                const datos = response.data;
                Utils.showSuccess(`Datos cargados exitosamente:\n• ${datos.ubicaciones.municipios} municipios\n• ${datos.ubicaciones.puestos} puestos\n• ${datos.ubicaciones.mesas_creadas} mesas\n• ${Object.values(datos.usuarios).reduce((a, b) => a + b, 0)} usuarios`);
                await this.refrescar();
            } else {
                Utils.showError(response.error || 'Error al cargar datos');
            }

        } catch (error) {
            console.error('Error cargando datos:', error);
            Utils.showError('Error al cargar datos: ' + error.message);
        }
    }

    async refrescar() {
        Utils.showInfo('Actualizando datos...');
        await this.cargarDatos();
        this.renderizar();
        Utils.showSuccess('Datos actualizados');
    }

    mostrarModalHabilitar() {
        // Implementar modal si es necesario
        console.log('Modal habilitar departamento');
    }

    debugInfo() {
        console.log('=== DEBUG DEPARTAMENTOS ADMIN ===');
        console.log('Departamentos disponibles:', this.departamentosDisponibles);
        console.log('Departamentos configurados:', this.departamentosConfigurados);
        console.log('Elementos DOM encontrados:');
        console.log('- tablaDisponiblesTBody:', !!document.getElementById('tablaDisponiblesTBody'));
        console.log('- tablaConfiguradosTBody:', !!document.getElementById('tablaConfiguradosTBody'));
        console.log('- statDepartamentosHabilitados:', !!document.getElementById('statDepartamentosHabilitados'));
        console.log('- statDepartamentoPrincipal:', !!document.getElementById('statDepartamentoPrincipal'));
        console.log('================================');
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar cuando se detecte el contenedor o cuando se abra la tab
    const initDepartamentosAdmin = () => {
        if (document.getElementById('departamentosAdminContainer') && !window.departamentosAdmin) {
            console.log('🏛️ Inicializando DepartamentosAdmin...');
            window.departamentosAdmin = new DepartamentosAdmin();
        }
    };

    // Intentar inicializar inmediatamente
    initDepartamentosAdmin();

    // También intentar cuando se abra la tab de departamentos
    const departamentosTab = document.getElementById('departamentos-tab');
    if (departamentosTab) {
        departamentosTab.addEventListener('shown.bs.tab', function() {
            setTimeout(initDepartamentosAdmin, 100);
        });
    }
});