# Design Document - Sistema de Geolocalización y Verificación de Presencia

## Overview

El Sistema de Geolocalización y Verificación de Presencia es un componente crítico que garantiza la integridad del proceso electoral mediante la verificación física de la ubicación de los testigos electorales. Utiliza tecnología GPS para capturar coordenadas precisas, tracking automático para monitoreo continuo, y mapas interactivos para visualización geográfica en tiempo real.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Geolocation API (HTML5)                     │   │
│  │  - navigator.geolocation.getCurrentPosition()            │   │
│  │  - navigator.geolocation.watchPosition()                 │   │
│  │  - High accuracy GPS capture                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Verificación de Presencia JS                   │   │
│  │  - verificarPresencia()                                  │   │
│  │  - trackingAutomatico()                                  │   │
│  │  - calcularDistancia()                                   │   │
│  │  - mostrarEstadoPresencia()                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Mapa Interactivo                            │   │
│  │  - OpenStreetMap / Leaflet                               │   │
│  │  - Marcadores de puestos y testigos                      │   │
│  │  - Clusters y popups informativos                        │   │
│  │  - Actualización en tiempo real                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTPS/REST API
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (Flask)                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         Verificación de Presencia Routes                 │   │
│  │  - POST /api/verificacion-presencia/verificar            │   │
│  │  - GET /api/verificacion-presencia/estado                │   │
│  │  - GET /api/verificacion-presencia/historial             │   │
│  │  - POST /api/verificacion-presencia/ping-automatico      │   │
│  │  - GET /api/verificacion-presencia/mapa-datos            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Geolocation Service                            │   │
│  │  - calcular_distancia_haversine()                       │   │
│  │  - validar_coordenadas()                                 │   │
│  │  - determinar_estado_presencia()                         │   │
│  │  - generar_alertas_presencia()                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Database Models                             │   │
│  │  - VerificacionPresencia                                 │   │
│  │  - UbicacionTestigo                                      │   │
│  │  - ConfiguracionGeolocalizacion                          │   │
│  │  - AlertaPresencia                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Database (PostgreSQL)                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  Tables                                  │   │
│  │  - verificaciones_presencia                              │   │
│  │  - ubicaciones_testigos                                  │   │
│  │  - puestos_electorales (con coordenadas)                 │   │
│  │  - configuracion_geolocalizacion                         │   │
│  │  - alertas_presencia                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
verificacion-presencia.js
├── Captura de GPS
│   ├── capturarUbicacionGPS()
│   ├── manejarErrorGPS()
│   └── validarPrecisionGPS()
│
├── Verificación Manual
│   ├── verificarPresencia()
│   ├── mostrarResultadoVerificacion()
│   └── actualizarEstadoPresencia()
│
├── Tracking Automático
│   ├── iniciarTrackingAutomatico()
│   ├── pingAutomatico()
│   ├── detenerTracking()
│   └── manejarTrackingOffline()
│
├── Cálculos Geográficos
│   ├── calcularDistancia()
│   ├── determinarEstadoPresencia()
│   └── validarCoordenadasValidas()
│
└── Integración con Dashboard
    ├── actualizarIndicadorPresencia()
    ├── mostrarNotificacionesGPS()
    └── sincronizarDatosOffline()

mapa-geolocalizacion.js
├── Inicialización del Mapa
│   ├── inicializarMapa()
│   ├── configurarCapasBase()
│   └── establecerVistaPorDefecto()
│
├── Marcadores y Clusters
│   ├── crearMarcadorPuesto()
│   ├── crearMarcadorTestigo()
│   ├── actualizarMarcadores()
│   └── configurarClusters()
│
├── Interacciones
│   ├── manejarClickMarcador()
│   ├── mostrarPopupInformativo()
│   └── centrarMapaEnUbicacion()
│
└── Actualización en Tiempo Real
    ├── actualizarMapaAutomatico()
    ├── cargarDatosMapaDesdeAPI()
    └── manejarErroresCargaMapa()
```

## Components and Interfaces

### 1. Captura de Coordenadas GPS

**Componente:** `capturarUbicacionGPS()`

**Funcionalidad:**
- Utiliza `navigator.geolocation.getCurrentPosition()` con opciones de alta precisión
- Maneja permisos de geolocalización del navegador
- Valida calidad de coordenadas capturadas
- Proporciona feedback visual durante captura

**Opciones de Geolocalización:**
```javascript
{
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 60000
}
```

**Estados de Respuesta:**
- **Éxito:** Coordenadas válidas con precisión aceptable
- **Error de Permisos:** Usuario denegó acceso a ubicación
- **Error de Timeout:** Tiempo de espera agotado
- **Error de Precisión:** Coordenadas con precisión insuficiente

### 2. Verificación Manual de Presencia

**Componente:** `verificarPresencia()`

**Flujo de Verificación:**
1. Capturar coordenadas GPS actuales
2. Obtener coordenadas del puesto asignado
3. Calcular distancia usando fórmula de Haversine
4. Determinar estado de presencia según radio de tolerancia
5. Registrar verificación en base de datos
6. Mostrar resultado al usuario

**Cálculo de Distancia (Haversine):**
```javascript
function calcularDistancia(lat1, lon1, lat2, lon2) {
    const R = 6371000; // Radio de la Tierra en metros
    const φ1 = lat1 * Math.PI/180;
    const φ2 = lat2 * Math.PI/180;
    const Δφ = (lat2-lat1) * Math.PI/180;
    const Δλ = (lon2-lon1) * Math.PI/180;
    
    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ/2) * Math.sin(Δλ/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    
    return R * c; // Distancia en metros
}
```

**Estados de Presencia:**
- **Presente:** Distancia ≤ 500 metros (configurable)
- **Fuera de Rango:** Distancia > 500 metros
- **Desconocido:** Sin ubicación reciente o error en captura

### 3. Tracking Automático

**Componente:** `trackingAutomatico()`

**Configuración:**
- Intervalo: 15 minutos (configurable)
- Método: `setInterval()` con `navigator.geolocation.getCurrentPosition()`
- Persistencia: Almacenamiento local para modo offline
- Sincronización: Envío automático cuando hay conexión

**Flujo de Tracking:**
1. Verificar si dashboard está activo
2. Capturar coordenadas GPS
3. Calcular estado de presencia
4. Almacenar localmente si offline
5. Enviar a servidor si online
6. Actualizar indicadores visuales
7. Programar próximo ping

**Manejo de Errores:**
- Continuar tracking aunque falle captura individual
- Registrar errores para diagnóstico
- Reintentar captura después de error temporal
- Notificar al usuario solo en errores persistentes

### 4. Mapa Interactivo

**Componente:** `mapa-geolocalizacion.js`

**Tecnología:** OpenStreetMap con Leaflet.js

**Capas del Mapa:**
- **Capa Base:** Mapa de calles de OpenStreetMap
- **Marcadores de Puestos:** Íconos azules con información del puesto
- **Marcadores de Testigos:** Íconos de colores según estado de presencia
- **Clusters:** Agrupación automática de marcadores cercanos

**Tipos de Marcadores:**
```javascript
const iconos = {
    puesto: L.icon({
        iconUrl: '/static/images/marcador-puesto.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34]
    }),
    testigoPresente: L.icon({
        iconUrl: '/static/images/marcador-testigo-verde.png',
        iconSize: [25, 41]
    }),
    testigoAusente: L.icon({
        iconUrl: '/static/images/marcador-testigo-rojo.png',
        iconSize: [25, 41]
    }),
    testigoDesconocido: L.icon({
        iconUrl: '/static/images/marcador-testigo-gris.png',
        iconSize: [25, 41]
    })
};
```

**Popups Informativos:**
- **Puesto:** Nombre, código, dirección, testigos asignados
- **Testigo:** Nombre, estado, última ubicación, precisión GPS

### 5. Backend - Verificación de Presencia Routes

**Archivo:** `backend/routes/verificacion_presencia.py`

**Endpoints:**

#### POST /api/verificacion-presencia/verificar
```python
{
    "latitud": -4.5339,
    "longitud": -75.6811,
    "precision": 15.5,
    "timestamp": "2025-12-24T10:30:00Z"
}
```

**Respuesta:**
```python
{
    "success": True,
    "estado_presencia": "presente",
    "distancia_metros": 245.8,
    "puesto_asignado": {
        "nombre": "Puesto Electoral Central",
        "coordenadas": [-4.5341, -75.6815]
    }
}
```

#### GET /api/verificacion-presencia/estado
**Respuesta:**
```python
{
    "success": True,
    "estado_actual": "presente",
    "ultima_verificacion": "2025-12-24T10:30:00Z",
    "distancia_actual": 245.8,
    "tracking_activo": True
}
```

#### POST /api/verificacion-presencia/ping-automatico
```python
{
    "latitud": -4.5339,
    "longitud": -75.6811,
    "precision": 12.3,
    "timestamp": "2025-12-24T10:45:00Z",
    "es_automatico": True
}
```

#### GET /api/verificacion-presencia/mapa-datos
**Respuesta:**
```python
{
    "success": True,
    "puestos": [
        {
            "id": 1,
            "nombre": "Puesto Central",
            "latitud": -4.5341,
            "longitud": -75.6815,
            "testigos_asignados": 3
        }
    ],
    "testigos": [
        {
            "id": 1,
            "nombre": "Juan Pérez",
            "estado_presencia": "presente",
            "latitud": -4.5339,
            "longitud": -75.6811,
            "ultima_actualizacion": "2025-12-24T10:45:00Z",
            "precision": 12.3
        }
    ]
}
```

## Data Models

### 1. VerificacionPresencia

```python
class VerificacionPresencia(db.Model):
    __tablename__ = 'verificaciones_presencia'
    
    id = db.Column(db.Integer, primary_key=True)
    testigo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    puesto_id = db.Column(db.Integer, db.ForeignKey('puestos_electorales.id'), nullable=False)
    
    # Coordenadas capturadas
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    precision_gps = db.Column(db.Float, nullable=True)  # En metros
    
    # Resultado de verificación
    estado_presencia = db.Column(db.String(20), nullable=False)  # presente, ausente, desconocido
    distancia_metros = db.Column(db.Float, nullable=True)
    
    # Metadatos
    es_automatico = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.String(500), nullable=True)
    
    # Relaciones
    testigo = db.relationship('User', foreign_keys=[testigo_id])
    puesto = db.relationship('PuestoElectoral', foreign_keys=[puesto_id])
```

### 2. UbicacionTestigo

```python
class UbicacionTestigo(db.Model):
    __tablename__ = 'ubicaciones_testigos'
    
    id = db.Column(db.Integer, primary_key=True)
    testigo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Última ubicación conocida
    ultima_latitud = db.Column(db.Float, nullable=True)
    ultima_longitud = db.Column(db.Float, nullable=True)
    ultima_precision = db.Column(db.Float, nullable=True)
    ultima_actualizacion = db.Column(db.DateTime, nullable=True)
    
    # Estado actual
    estado_presencia_actual = db.Column(db.String(20), default='desconocido')
    tracking_activo = db.Column(db.Boolean, default=False)
    
    # Estadísticas del día
    total_verificaciones_hoy = db.Column(db.Integer, default=0)
    tiempo_presente_hoy = db.Column(db.Integer, default=0)  # En minutos
    tiempo_ausente_hoy = db.Column(db.Integer, default=0)   # En minutos
    
    # Relación
    testigo = db.relationship('User', foreign_keys=[testigo_id])
```

### 3. ConfiguracionGeolocalizacion

```python
class ConfiguracionGeolocalizacion(db.Model):
    __tablename__ = 'configuracion_geolocalizacion'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Parámetros de verificación
    radio_tolerancia_metros = db.Column(db.Integer, default=500)
    precision_gps_minima = db.Column(db.Float, default=100.0)
    
    # Parámetros de tracking
    intervalo_tracking_minutos = db.Column(db.Integer, default=15)
    tiempo_alerta_ausencia_minutos = db.Column(db.Integer, default=30)
    
    # Parámetros de retención
    dias_retencion_historial = db.Column(db.Integer, default=30)
    max_ubicaciones_offline = db.Column(db.Integer, default=100)
    
    # Metadatos
    actualizado_por = db.Column(db.Integer, db.ForeignKey('users.id'))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
```

### 4. AlertaPresencia

```python
class AlertaPresencia(db.Model):
    __tablename__ = 'alertas_presencia'
    
    id = db.Column(db.Integer, primary_key=True)
    testigo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coordinador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Tipo y descripción
    tipo_alerta = db.Column(db.String(50), nullable=False)  # ausencia_prolongada, fuera_rango, sin_ubicacion
    descripcion = db.Column(db.Text, nullable=False)
    
    # Estado
    estado = db.Column(db.String(20), default='activa')  # activa, revisada, resuelta
    prioridad = db.Column(db.String(10), default='media')  # baja, media, alta, critica
    
    # Timestamps
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_resolucion = db.Column(db.DateTime, nullable=True)
    resuelto_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relaciones
    testigo = db.relationship('User', foreign_keys=[testigo_id])
    coordinador = db.relationship('User', foreign_keys=[coordinador_id])
    resolvio = db.relationship('User', foreign_keys=[resuelto_por])
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Cálculo de Distancia Consistente
*For any* dos pares de coordenadas válidas, el cálculo de distancia usando la fórmula de Haversine debe ser simétrico y producir el mismo resultado independientemente del orden de los puntos
**Validates: Requirements 2.3, 14.4**

### Property 2: Validación de Coordenadas GPS
*For any* coordenadas GPS capturadas, deben estar dentro de los límites geográficos válidos (latitud: -90 a 90, longitud: -180 a 180) y tener precisión menor a 1000 metros
**Validates: Requirements 14.1, 14.2, 14.3**

### Property 3: Estado de Presencia Determinístico
*For any* verificación de presencia con coordenadas válidas, el estado resultante debe ser determinístico basado en la distancia calculada y el radio de tolerancia configurado
**Validates: Requirements 2.4, 2.5, 8.1**

### Property 4: Tracking Automático Consistente
*For any* testigo con tracking activo, el sistema debe capturar ubicación en intervalos regulares y mantener consistencia en el estado de presencia entre capturas consecutivas
**Validates: Requirements 3.1, 3.2, 3.4**

### Property 5: Integridad de Datos de Ubicación
*For any* ubicación almacenada en la base de datos, debe tener un timestamp válido, coordenadas dentro de rangos válidos, y estar asociada a un testigo existente
**Validates: Requirements 6.2, 9.2, 14.5**

### Property 6: Sincronización Offline Correcta
*For any* ubicaciones almacenadas offline, cuando se restaure la conexión, todas deben sincronizarse en el orden correcto sin pérdida de datos
**Validates: Requirements 10.2, 10.5, 10.7**

### Property 7: Generación de Alertas Apropiada
*For any* testigo que esté fuera de rango por más del tiempo configurado, debe generarse exactamente una alerta activa hasta que se resuelva la situación
**Validates: Requirements 7.1, 7.2, 7.6**

### Property 8: Privacidad de Datos de Ubicación
*For any* acceso a datos de ubicación, debe estar autorizado según el rol del usuario y registrado en el log de auditoría
**Validates: Requirements 9.4, 9.7**

## Error Handling

### 1. Errores de Geolocalización

**Tipos de Error:**
- `PERMISSION_DENIED`: Usuario denegó permisos de ubicación
- `POSITION_UNAVAILABLE`: No se puede determinar ubicación
- `TIMEOUT`: Tiempo de espera agotado
- `ACCURACY_INSUFFICIENT`: Precisión GPS insuficiente

**Estrategias de Manejo:**
- Mostrar mensajes específicos por tipo de error
- Proporcionar instrucciones para habilitar ubicación
- Permitir reintentos manuales
- Degradar graciosamente a modo manual

### 2. Errores de Conectividad

**Escenarios:**
- Sin conexión a internet durante captura
- Falla en envío de datos al servidor
- Timeout en requests de API

**Estrategias:**
- Almacenamiento local automático
- Reintento automático con backoff exponencial
- Indicadores visuales de estado de conexión
- Sincronización diferida cuando se restaure conexión

### 3. Errores de Validación

**Validaciones:**
- Coordenadas fuera de rangos válidos
- Precisión GPS insuficiente
- Cambios de ubicación imposibles (teletransporte)
- Datos corruptos o incompletos

**Estrategias:**
- Validación en frontend y backend
- Rechazo de datos inválidos con mensaje explicativo
- Logging de intentos de datos inválidos
- Solicitud de nueva captura para datos sospechosos

## Testing Strategy

### Unit Tests
- Validar cálculos de distancia con coordenadas conocidas
- Probar validaciones de coordenadas GPS
- Verificar lógica de determinación de estado de presencia
- Testear manejo de errores de geolocalización

### Property-Based Tests
- Generar coordenadas aleatorias válidas y verificar consistencia de cálculos
- Probar simetría de cálculo de distancia
- Verificar que estados de presencia sean determinísticos
- Validar integridad de datos en operaciones de base de datos

### Integration Tests
- Probar flujo completo de verificación de presencia
- Verificar sincronización offline-online
- Testear generación y resolución de alertas
- Probar actualización de mapas en tiempo real

### Manual Tests
- Verificar funcionamiento en diferentes dispositivos móviles
- Probar precisión GPS en ubicaciones reales
- Validar experiencia de usuario en condiciones de red limitada
- Verificar mapas interactivos con datos reales

**Configuración de Property Tests:**
- Mínimo 100 iteraciones por propiedad
- Generadores de coordenadas dentro de límites de Colombia
- Simulación de condiciones de red variables
- Validación de consistencia temporal en tracking automático