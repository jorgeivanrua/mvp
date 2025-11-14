/**
 * Gestor de Sincronización Universal
 * Maneja la sincronización de datos locales con el servidor para todos los roles
 */

class SyncManager {
    constructor() {
        this.syncInterval = null;
        this.indicatorUpdateInterval = null;
        this.isSyncing = false;
    }

    /**
     * Inicializar el gestor de sincronización
     */
    init() {
        console.log('SyncManager: Inicializando...');
        
        // Sincronización inicial después de 2 segundos
        setTimeout(() => {
            this.syncAll(true);
        }, 2000);
        
        // Sincronización periódica cada 5 minutos
        this.syncInterval = setInterval(() => {
            this.syncAll(true);
        }, 5 * 60 * 1000);
        
        // Actualizar indicador cada 30 segundos
        this.indicatorUpdateInterval = setInterval(() => {
            this.updateIndicator();
        }, 30000);
        
        // Actualizar indicador inicial
        this.updateIndicator();
        
        console.log('SyncManager: Inicializado correctamente');
    }

    /**
     * Detener el gestor de sincronización
     */
    stop() {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
            this.syncInterval = null;
        }
        
        if (this.indicatorUpdateInterval) {
            clearInterval(this.indicatorUpdateInterval);
            this.indicatorUpdateInterval = null;
        }
        
        console.log('SyncManager: Detenido');
    }

    /**
     * Sincronizar todos los datos locales
     */
    async syncAll(silent = false) {
        if (this.isSyncing) {
            console.log('SyncManager: Ya hay una sincronización en curso');
            return;
        }

        this.isSyncing = true;

        try {
            if (!silent) {
                console.log('SyncManager: Iniciando sincronización completa...');
            }

            let totalSyncedIncidents = 0;
            let totalSyncedCrimes = 0;
            let totalErrors = 0;

            // Sincronizar incidentes
            const incidentsResult = await this.syncIncidents(silent);
            totalSyncedIncidents = incidentsResult.synced;
            totalErrors += incidentsResult.errors;

            // Sincronizar delitos
            const crimesResult = await this.syncCrimes(silent);
            totalSyncedCrimes = crimesResult.synced;
            totalErrors += crimesResult.errors;

            const totalSynced = totalSyncedIncidents + totalSyncedCrimes;

            // Mostrar resumen si no es silencioso
            if (!silent && (totalSynced > 0 || totalErrors > 0)) {
                let message = '';

                if (totalSynced > 0) {
                    message += `✓ ${totalSynced} registro(s) sincronizado(s)`;
                    if (totalSyncedIncidents > 0) message += ` (${totalSyncedIncidents} incidente(s))`;
                    if (totalSyncedCrimes > 0) message += ` (${totalSyncedCrimes} delito(s))`;
                }

                if (totalErrors > 0) {
                    if (message) message += '\n';
                    message += `⚠️ ${totalErrors} registro(s) con error`;
                }

                if (totalSynced > 0 && totalErrors === 0) {
                    Utils.showSuccess(message);
                } else if (totalErrors > 0) {
                    Utils.showWarning(message);
                }
            }

            // Actualizar indicador
            this.updateIndicator();

            if (!silent) {
                console.log(`SyncManager: Sincronización completa - ${totalSynced} sincronizados, ${totalErrors} errores`);
            }

            return { totalSynced, totalErrors };

        } catch (error) {
            console.error('SyncManager: Error en sincronización completa:', error);
            if (!silent) {
                Utils.showError('Error al sincronizar datos');
            }
            return { totalSynced: 0, totalErrors: 0 };
        } finally {
            this.isSyncing = false;
        }
    }

    /**
     * Sincronizar incidentes locales
     */
    async syncIncidents(silent = false) {
        try {
            const incidents = this.getLocalIncidents();
            const keys = Object.keys(incidents);

            if (keys.length === 0) {
                return { synced: 0, errors: 0 };
            }

            let synced = 0;
            let errors = 0;

            for (const key of keys) {
                const incident = incidents[key];

                // Solo sincronizar los que no están sincronizados
                if (incident.sincronizado) {
                    continue;
                }

                try {
                    const dataToSend = {
                        mesa_id: incident.mesa_id,
                        tipo_incidente: incident.tipo_incidente,
                        titulo: incident.titulo,
                        severidad: incident.severidad,
                        descripcion: incident.descripcion
                    };

                    const response = await APIClient.reportarIncidente(dataToSend);

                    if (response.success) {
                        // Marcar como sincronizado
                        incident.sincronizado = true;
                        incident.id_servidor = response.data.id;
                        incidents[key] = incident;
                        this.saveLocalIncidents(incidents);

                        synced++;
                        console.log('SyncManager: Incidente sincronizado:', key);
                    } else {
                        errors++;
                        console.error('SyncManager: Error sincronizando incidente:', key, response.error);
                    }
                } catch (error) {
                    errors++;
                    console.error('SyncManager: Error sincronizando incidente:', key, error);
                }
            }

            return { synced, errors };

        } catch (error) {
            console.error('SyncManager: Error en sincronización de incidentes:', error);
            return { synced: 0, errors: 0 };
        }
    }

    /**
     * Sincronizar delitos locales
     */
    async syncCrimes(silent = false) {
        try {
            const crimes = this.getLocalCrimes();
            const keys = Object.keys(crimes);

            if (keys.length === 0) {
                return { synced: 0, errors: 0 };
            }

            let synced = 0;
            let errors = 0;

            for (const key of keys) {
                const crime = crimes[key];

                // Solo sincronizar los que no están sincronizados
                if (crime.sincronizado) {
                    continue;
                }

                try {
                    const dataToSend = {
                        mesa_id: crime.mesa_id,
                        tipo_delito: crime.tipo_delito,
                        titulo: crime.titulo,
                        gravedad: crime.gravedad,
                        descripcion: crime.descripcion,
                        testigos_adicionales: crime.testigos_adicionales || null
                    };

                    const response = await APIClient.reportarDelito(dataToSend);

                    if (response.success) {
                        // Marcar como sincronizado
                        crime.sincronizado = true;
                        crime.id_servidor = response.data.id;
                        crimes[key] = crime;
                        this.saveLocalCrimes(crimes);

                        synced++;
                        console.log('SyncManager: Delito sincronizado:', key);
                    } else {
                        errors++;
                        console.error('SyncManager: Error sincronizando delito:', key, response.error);
                    }
                } catch (error) {
                    errors++;
                    console.error('SyncManager: Error sincronizando delito:', key, error);
                }
            }

            return { synced, errors };

        } catch (error) {
            console.error('SyncManager: Error en sincronización de delitos:', error);
            return { synced: 0, errors: 0 };
        }
    }

    /**
     * Obtener incidentes locales
     */
    getLocalIncidents() {
        try {
            const data = localStorage.getItem('incidentes_locales');
            return data ? JSON.parse(data) : {};
        } catch (error) {
            console.error('SyncManager: Error obteniendo incidentes locales:', error);
            return {};
        }
    }

    /**
     * Guardar incidentes locales
     */
    saveLocalIncidents(incidents) {
        try {
            localStorage.setItem('incidentes_locales', JSON.stringify(incidents));
        } catch (error) {
            console.error('SyncManager: Error guardando incidentes locales:', error);
        }
    }

    /**
     * Obtener delitos locales
     */
    getLocalCrimes() {
        try {
            const data = localStorage.getItem('delitos_locales');
            return data ? JSON.parse(data) : {};
        } catch (error) {
            console.error('SyncManager: Error obteniendo delitos locales:', error);
            return {};
        }
    }

    /**
     * Guardar delitos locales
     */
    saveLocalCrimes(crimes) {
        try {
            localStorage.setItem('delitos_locales', JSON.stringify(crimes));
        } catch (error) {
            console.error('SyncManager: Error guardando delitos locales:', error);
        }
    }

    /**
     * Guardar incidente localmente
     */
    saveIncidentLocally(data) {
        try {
            const incidents = this.getLocalIncidents();
            const id = `incidente_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            
            data.id = id;
            data.sincronizado = false;
            data.fecha_hora = data.fecha_hora || new Date().toISOString();
            
            incidents[id] = data;
            this.saveLocalIncidents(incidents);
            
            console.log('SyncManager: Incidente guardado localmente:', id);
            this.updateIndicator();
            
            return id;
        } catch (error) {
            console.error('SyncManager: Error guardando incidente local:', error);
            throw error;
        }
    }

    /**
     * Guardar delito localmente
     */
    saveCrimeLocally(data) {
        try {
            const crimes = this.getLocalCrimes();
            const id = `delito_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            
            data.id = id;
            data.sincronizado = false;
            data.fecha_hora = data.fecha_hora || new Date().toISOString();
            
            crimes[id] = data;
            this.saveLocalCrimes(crimes);
            
            console.log('SyncManager: Delito guardado localmente:', id);
            this.updateIndicator();
            
            return id;
        } catch (error) {
            console.error('SyncManager: Error guardando delito local:', error);
            throw error;
        }
    }

    /**
     * Actualizar indicador de sincronización
     */
    updateIndicator() {
        const incidents = this.getLocalIncidents();
        const crimes = this.getLocalCrimes();

        // Contar pendientes
        const pendingIncidents = Object.values(incidents).filter(i => !i.sincronizado).length;
        const pendingCrimes = Object.values(crimes).filter(c => !c.sincronizado).length;

        const totalPending = pendingIncidents + pendingCrimes;

        // Buscar o crear indicador
        let indicator = document.getElementById('syncIndicator');

        if (totalPending > 0) {
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.id = 'syncIndicator';
                indicator.className = 'alert alert-warning d-flex justify-content-between align-items-center';
                indicator.style.position = 'fixed';
                indicator.style.bottom = '20px';
                indicator.style.right = '20px';
                indicator.style.zIndex = '1050';
                indicator.style.minWidth = '300px';
                indicator.style.maxWidth = '400px';
                indicator.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
                document.body.appendChild(indicator);
            }

            let details = [];
            if (pendingIncidents > 0) details.push(`${pendingIncidents} incidente(s)`);
            if (pendingCrimes > 0) details.push(`${pendingCrimes} delito(s)`);

            indicator.innerHTML = `
                <div>
                    <i class="bi bi-cloud-upload"></i>
                    <strong>${totalPending}</strong> registro(s) pendiente(s)
                    <br>
                    <small class="text-muted">${details.join(', ')}</small>
                </div>
                <button class="btn btn-sm btn-warning" onclick="window.syncManager.syncAll()">
                    <i class="bi bi-arrow-repeat"></i> Sincronizar
                </button>
            `;
        } else {
            // Eliminar indicador si no hay pendientes
            if (indicator) {
                indicator.remove();
            }
        }
    }

    /**
     * Limpiar datos sincronizados antiguos (más de 7 días)
     */
    cleanOldSyncedData() {
        try {
            const sevenDaysAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);

            // Limpiar incidentes
            const incidents = this.getLocalIncidents();
            let cleanedIncidents = 0;
            Object.keys(incidents).forEach(key => {
                const incident = incidents[key];
                if (incident.sincronizado && incident.fecha_hora) {
                    const incidentDate = new Date(incident.fecha_hora).getTime();
                    if (incidentDate < sevenDaysAgo) {
                        delete incidents[key];
                        cleanedIncidents++;
                    }
                }
            });
            if (cleanedIncidents > 0) {
                this.saveLocalIncidents(incidents);
                console.log(`SyncManager: Limpiados ${cleanedIncidents} incidentes antiguos`);
            }

            // Limpiar delitos
            const crimes = this.getLocalCrimes();
            let cleanedCrimes = 0;
            Object.keys(crimes).forEach(key => {
                const crime = crimes[key];
                if (crime.sincronizado && crime.fecha_hora) {
                    const crimeDate = new Date(crime.fecha_hora).getTime();
                    if (crimeDate < sevenDaysAgo) {
                        delete crimes[key];
                        cleanedCrimes++;
                    }
                }
            });
            if (cleanedCrimes > 0) {
                this.saveLocalCrimes(crimes);
                console.log(`SyncManager: Limpiados ${cleanedCrimes} delitos antiguos`);
            }

        } catch (error) {
            console.error('SyncManager: Error limpiando datos antiguos:', error);
        }
    }
}

// Crear instancia global
window.syncManager = new SyncManager();

// Limpiar datos antiguos al cargar
window.addEventListener('load', () => {
    window.syncManager.cleanOldSyncedData();
});
