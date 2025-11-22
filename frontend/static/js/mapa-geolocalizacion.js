/**
 * Sistema de Geolocalización y Mapas
 * Visualización en tiempo real de usuarios y puestos de votación
 */

class MapaGeolocalizacion {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.map = null;
        this.markers = {};
        this.options = {
            center: options.center || [4.5709, -74.2973], // Bogotá por defecto
            zoom: options.zoom || 6,
            autoUpdate: options.autoUpdate !== false,
            updateInterval: options.updateInterval || 30000, // 30 segundos
            showPuestos: options.showPuestos !== false,
            showUsuarios: options.showUsuarios !== false
        };
        this.updateInterval = null;
    }

    /**
     * Inicializar mapa
     */
    async init() {
        try {
            const container = document.getElementById(this.containerId);
            if (!container) {
                console.error('Contenedor del mapa no encontrado:', this.containerId);
                return false;
            }

            // Crear mapa con Leaflet
            this.map = L.map(this.containerId).setView(this.options.center, this.options.zoom);

            // Agregar capa de OpenStreetMap
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }).addTo(this.map);

            // Cargar datos iniciales
            await this.cargarDatos();

            // Iniciar actualización automática
            if (this.options.autoUpdate) {
                this.iniciarActualizacionAutomatica();
            }

            console.log('Mapa inicializado correctamente');
            return true;

        } catch (error) {
            console.error('Error inicializando mapa:', error);
            return false;
        }
    }

    /**
     * Cargar datos de puestos y usuarios
     */
    async cargarDatos() {
        try {
            // Cargar puestos de votación
            if (this.options.showPuestos) {
                await this.cargarPuestos();
            }

            // Cargar usuarios geolocalizados
            if (this.options.showUsuarios) {
                await this.cargarUsuarios();
            }

        } catch (error) {
            console.error('Error cargando datos:', error);
        }
    }

    /**
     * Cargar puestos de votación
     */
    async cargarPuestos() {
        try {
            const response = await fetch('/api/locations/puestos-geolocalizados', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success && data.data) {
                data.data.forEach(puesto => {
                    if (puesto.latitud && puesto.longitud) {
                        this.agregarMarkerPuesto(puesto);
                    }
                });
            }

        } catch (error) {
            console.error('Error cargando puestos:', error);
        }
    }

    /**
     * Cargar usuarios geolocalizados
     */
    async cargarUsuarios() {
        try {
            const response = await fetch('/api/verificacion/usuarios-geolocalizados', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const data = await response.json();

            if (data.success && data.data) {
                data.data.forEach(usuario => {
                    if (usuario.latitud && usuario.longitud) {
                        this.agregarMarkerUsuario(usuario);
                    }
                });
            }

        } catch (error) {
            console.error('Error cargando usuarios:', error);
        }
    }

    /**
     * Agregar marker de puesto de votación
     */
    agregarMarkerPuesto(puesto) {
        const markerId = `puesto_${puesto.id}`;

        // Eliminar marker anterior si existe
        if (this.markers[markerId]) {
            this.map.removeLayer(this.markers[markerId]);
        }

        // Icono personalizado para puestos
        const iconoPuesto = L.divIcon({
            className: 'custom-marker-puesto',
            html: '<div class="marker-pin marker-puesto"><i class="bi bi-building"></i></div>',
            iconSize: [30, 42],
            iconAnchor: [15, 42],
            popupAnchor: [0, -42]
        });

        // Crear marker
        const marker = L.marker([puesto.latitud, puesto.longitud], {
            icon: iconoPuesto,
            title: puesto.nombre_completo
        });

        // Popup con información
        const popupContent = `
            <div class="marker-popup">
                <h6><i class="bi bi-building"></i> ${puesto.puesto_nombre || 'Puesto'}</h6>
                <p class="mb-1"><strong>Código:</strong> ${puesto.puesto_codigo}</p>
                <p class="mb-1"><strong>Municipio:</strong> ${puesto.municipio_nombre}</p>
                <p class="mb-1"><strong>Departamento:</strong> ${puesto.departamento_nombre}</p>
                ${puesto.direccion ? `<p class="mb-1"><strong>Dirección:</strong> ${puesto.direccion}</p>` : ''}
                ${puesto.total_mesas ? `<p class="mb-0"><strong>Mesas:</strong> ${puesto.total_mesas}</p>` : ''}
            </div>
        `;

        marker.bindPopup(popupContent);
        marker.addTo(this.map);

        this.markers[markerId] = marker;
    }

    /**
     * Agregar marker de usuario
     */
    agregarMarkerUsuario(usuario) {
        const markerId = `usuario_${usuario.id}`;

        // Eliminar marker anterior si existe
        if (this.markers[markerId]) {
            this.map.removeLayer(this.markers[markerId]);
        }

        // Determinar color según estado
        const colorEstado = this.getColorEstado(usuario.estado);
        const iconoRol = this.getIconoRol(usuario.rol);

        // Icono personalizado para usuarios
        const iconoUsuario = L.divIcon({
            className: 'custom-marker-usuario',
            html: `<div class="marker-pin marker-usuario marker-${usuario.estado}"><i class="bi ${iconoRol}"></i></div>`,
            iconSize: [30, 42],
            iconAnchor: [15, 42],
            popupAnchor: [0, -42]
        });

        // Crear marker
        const marker = L.marker([usuario.latitud, usuario.longitud], {
            icon: iconoUsuario,
            title: usuario.nombre
        });

        // Popup con información
        const estadoBadge = this.getEstadoBadge(usuario.estado);
        const tiempoInactivo = usuario.minutos_inactivo !== null 
            ? `${usuario.minutos_inactivo} min` 
            : 'Nunca';

        const popupContent = `
            <div class="marker-popup">
                <h6><i class="bi ${iconoRol}"></i> ${usuario.nombre}</h6>
                <p class="mb-1"><strong>Rol:</strong> ${this.formatearRol(usuario.rol)}</p>
                <p class="mb-1"><strong>Estado:</strong> ${estadoBadge}</p>
                <p class="mb-1"><strong>Inactivo:</strong> ${tiempoInactivo}</p>
                ${usuario.ubicacion_nombre ? `<p class="mb-1"><strong>Ubicación:</strong> ${usuario.ubicacion_nombre}</p>` : ''}
                <p class="mb-0"><strong>Última actualización:</strong><br>${new Date(usuario.ultima_geolocalizacion_at).toLocaleString()}</p>
            </div>
        `;

        marker.bindPopup(popupContent);
        marker.addTo(this.map);

        this.markers[markerId] = marker;
    }

    /**
     * Obtener color según estado
     */
    getColorEstado(estado) {
        const colores = {
            'activo': '#28a745',
            'inactivo': '#ffc107',
            'ausente': '#dc3545'
        };
        return colores[estado] || '#6c757d';
    }

    /**
     * Obtener icono según rol
     */
    getIconoRol(rol) {
        const iconos = {
            'testigo_electoral': 'bi-person-check',
            'coordinador_puesto': 'bi-person-badge',
            'coordinador_municipal': 'bi-person-workspace',
            'coordinador_departamental': 'bi-person-gear',
            'auditor_electoral': 'bi-shield-check',
            'super_admin': 'bi-star'
        };
        return iconos[rol] || 'bi-person';
    }

    /**
     * Formatear nombre del rol
     */
    formatearRol(rol) {
        const roles = {
            'testigo_electoral': 'Testigo Electoral',
            'coordinador_puesto': 'Coordinador de Puesto',
            'coordinador_municipal': 'Coordinador Municipal',
            'coordinador_departamental': 'Coordinador Departamental',
            'auditor_electoral': 'Auditor Electoral',
            'super_admin': 'Super Admin'
        };
        return roles[rol] || rol;
    }

    /**
     * Obtener badge de estado
     */
    getEstadoBadge(estado) {
        const badges = {
            'activo': '<span class="badge bg-success">Activo</span>',
            'inactivo': '<span class="badge bg-warning">Inactivo</span>',
            'ausente': '<span class="badge bg-danger">Ausente</span>'
        };
        return badges[estado] || '<span class="badge bg-secondary">Desconocido</span>';
    }

    /**
     * Centrar mapa en una ubicación
     */
    centrarEn(latitud, longitud, zoom = 15) {
        if (this.map) {
            this.map.setView([latitud, longitud], zoom);
        }
    }

    /**
     * Ajustar vista para mostrar todos los markers
     */
    ajustarVista() {
        if (this.map && Object.keys(this.markers).length > 0) {
            const group = L.featureGroup(Object.values(this.markers));
            this.map.fitBounds(group.getBounds().pad(0.1));
        }
    }

    /**
     * Iniciar actualización automática
     */
    iniciarActualizacionAutomatica() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        this.updateInterval = setInterval(() => {
            this.actualizar();
        }, this.options.updateInterval);

        console.log(`Actualización automática del mapa iniciada (cada ${this.options.updateInterval / 1000}s)`);
    }

    /**
     * Detener actualización automática
     */
    detenerActualizacionAutomatica() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
            console.log('Actualización automática del mapa detenida');
        }
    }

    /**
     * Actualizar datos del mapa
     */
    async actualizar() {
        try {
            await this.cargarDatos();
            console.log('Mapa actualizado:', new Date().toLocaleTimeString());
        } catch (error) {
            console.error('Error actualizando mapa:', error);
        }
    }

    /**
     * Limpiar todos los markers
     */
    limpiarMarkers() {
        Object.values(this.markers).forEach(marker => {
            this.map.removeLayer(marker);
        });
        this.markers = {};
    }

    /**
     * Destruir mapa
     */
    destroy() {
        this.detenerActualizacionAutomatica();
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
        this.markers = {};
        console.log('Mapa destruido');
    }
}

// Estilos CSS para los markers personalizados
const estilosMarkers = `
<style>
.custom-marker-puesto, .custom-marker-usuario {
    background: transparent;
    border: none;
}

.marker-pin {
    width: 30px;
    height: 42px;
    border-radius: 50% 50% 50% 0;
    position: relative;
    transform: rotate(-45deg);
    display: flex;
    align-items: center;
    justify-content: center;
}

.marker-pin i {
    transform: rotate(45deg);
    font-size: 16px;
    color: white;
}

.marker-puesto {
    background: #007bff;
    border: 3px solid #0056b3;
}

.marker-usuario {
    border: 3px solid rgba(0,0,0,0.2);
}

.marker-usuario.marker-activo {
    background: #28a745;
}

.marker-usuario.marker-inactivo {
    background: #ffc107;
}

.marker-usuario.marker-ausente {
    background: #dc3545;
}

.marker-popup {
    min-width: 200px;
}

.marker-popup h6 {
    margin-bottom: 10px;
    color: #333;
    border-bottom: 2px solid #007bff;
    padding-bottom: 5px;
}

.marker-popup p {
    font-size: 13px;
    color: #666;
}
</style>
`;

// Inyectar estilos
if (!document.getElementById('marker-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'marker-styles';
    styleElement.innerHTML = estilosMarkers;
    document.head.appendChild(styleElement);
}
