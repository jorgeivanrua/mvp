# Design Document - Sistema de Geolocalización y Verificación de Presencia

## Overview

El Sistema de Geolocalización y Verificación de Presencia es un módulo crítico del sistema electoral que permite el tracking en tiempo real de usuarios (testigos, coordinadores, auditores) mediante captura de coordenadas GPS. El sistema está implementado con una arquitectura RESTful que integra la API de Geolocalización del navegador con el backend Flask/PostgreSQL. Proporciona funcionalidades de verificación manual de presencia, ping automático cada 5 minutos, visualización de estado del equipo con clasificación por actividad (activo/inactivo/ausente), y mapas interactivos con marcadores de usuarios geolocalizados.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                        │
│  - Geolocation API (navigator.geolocation)                  │
│  - Botón "Verificar Presencia"                              │
│  - Ping automático cada 5 minutos                           │
│  - Mapa interactivo (Leaflet/Google Maps)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API REST Layer                            │
│  Blueprint: verificacion_bp                                 │
│  Prefix: /api/verificacion                                  │
│  - POST /presencia (verificar presencia)                    │
│  - POST /ping (ping automático)                             │
│  - GET /estado-equipo (estado del equipo)                   │
│  - GET /usuarios-geolocalizados (mapa)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic                            │
│  - calcular_minutos_inactivo()                              │
│  - determinar_estado_usuario()                              │
│  - Filtrado por rol y jurisdicción                          │
│  - Validación de coordenadas                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  - User Model (campos de geolocalización)                   │
│  - Location Model (ubicaciones asignadas)                   │
│  - PostgreSQL Database                                      │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
Usuario hace clic en "Verificar Presencia"
    │
    ▼
Frontend solicita permiso de geolocalización
    │
    ▼
Browser Geolocation API captura coordenadas
    │
    ▼
Frontend envía POST /api/verificacion/presencia
    │
    ▼
Backend actualiza User.ultima_latitud, ultima_longitud
Backend actualiza User.presencia_verificada = True
Backend actualiza User.presencia_verificada_at = now()
Backend actualiza User.ultimo_acceso = now()
    │
    ▼
Backend retorna success con datos de ubicación
    │
    ▼
Frontend muestra mensaje de éxito
Frontend inicia ping automático cada 5 minutos
```

### Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **Geolocation**: Browser Geolocation API
- **Maps**: Leaflet.js or Google Maps API
- **Frontend**: HTML, JavaScript, Bootstrap
- **Real-time Updates**: Polling (every 5 minutes)

## Components and Interfaces

### 1. Data Models

#### User Model (Extended)

```python
class User(db.Model):
    """Modelo de usuario con campos de geolocalización"""
    __tablename__ = 'users'
    
    # Campos existentes
    id: Integer (Primary Key)
    nombre: String(100) (Not Null)
    password_hash: String(255) (Not Null)
    rol: String(50) (Not Null)
    ubicacion_id: Integer (Foreign Key: locations.id)
    activo: Boolean (Default: True)
    ultimo_acceso: DateTime (Nullable)
    
    # Verificación de presencia
    presencia_verificada: Boolean (Default: False)
    presencia_verificada_at: DateTime (Nullable)
    
    # Geolocalización
    ultima_latitud: Float (Nullable)
    ultima_longitud: Float (Nullable)
    ultima_geolocalizacion_at: DateTime (Nullable)
    precision_geolocalizacion: Float (Nullable)
    
    created_at: DateTime (Default: utcnow)
    updated_at: DateTime (Default: utcnow, OnUpdate: utcnow)
    
    # Relationships
    ubicacion: Location
    
    # Methods
    verificar_presencia() -> None
    to_dict(include_sensitive=False) -> dict
```

### 2. API Endpoints

#### POST /api/verificacion/presencia
- **Description**: Verificar presencia del usuario en su ubicación asignada
- **Authentication**: JWT Required
- **Authorization**: All authenticated users
- **Request**: 
  ```json
  {
    "latitud": 4.6097,
    "longitud": -74.0817,
    "precision": 10.5
  }
  ```
- **Response**: 
  ```json
  {
    "success": true,
    "message": "Presencia verificada exitosamente para testigo_electoral",
    "data": {
      "presencia_verificada": true,
      "presencia_verificada_at": "2025-11-25T10:30:00",
      "rol": "testigo_electoral",
      "ubicacion": {
        "id": 123,
        "nombre": "Mesa 001 - Puesto 01 - Bogotá",
        "tipo": "mesa"
      }
    }
  }
  ```

#### POST /api/verificacion/ping
- **Description**: Ping automático para mantener presencia activa
- **Authentication**: JWT Required
- **Authorization**: All authenticated users
- **Request**: None (empty body)
- **Response**: 
  ```json
  {
    "success": true,
    "data": {
      "ultimo_acceso": "2025-11-25T10:35:00",
      "presencia_verificada": true
    }
  }
  ```

#### GET /api/verificacion/estado-equipo
- **Description**: Obtener estado de presencia del equipo bajo supervisión
- **Authentication**: JWT Required
- **Authorization**: coordinador_puesto, coordinador_municipal, coordinador_departamental, super_admin
- **Request**: None
- **Response**: 
  ```json
  {
    "success": true,
    "data": {
      "equipo": [
        {
          "id": 45,
          "nombre": "Juan Pérez",
          "rol": "Testigo Electoral",
          "ubicacion": "Mesa 001",
          "presencia_verificada": true,
          "presencia_verificada_at": "2025-11-25T10:00:00",
          "ultimo_acceso": "2025-11-25T10:30:00",
          "minutos_inactivo": 5,
          "estado": "activo"
        }
      ],
      "estadisticas": {
        "total": 10,
        "presentes": 8,
        "inactivos": 1,
        "ausentes": 1,
        "porcentaje_presencia": 80.0
      }
    }
  }
  ```

#### GET /api/verificacion/usuarios-geolocalizados
- **Description**: Obtener usuarios con geolocalización activa para mostrar en mapa
- **Authentication**: JWT Required
- **Authorization**: coordinador_puesto, coordinador_municipal, coordinador_departamental, super_admin, auditor_electoral
- **Request**: None
- **Response**: 
  ```json
  {
    "success": true,
    "data": [
      {
        "id": 45,
        "nombre": "Juan Pérez",
        "rol": "testigo_electoral",
        "latitud": 4.6097,
        "longitud": -74.0817,
        "ultima_geolocalizacion_at": "2025-11-25T10:30:00",
        "ultimo_acceso": "2025-11-25T10:30:00",
        "minutos_inactivo": 5,
        "estado": "activo",
        "ubicacion_nombre": "Mesa 001 - Puesto 01 - Bogotá",
        "ubicacion_tipo": "mesa"
      }
    ]
  }
  ```

### 3. Business Logic Functions

#### calcular_minutos_inactivo(ultimo_acceso)
```python
def calcular_minutos_inactivo(ultimo_acceso):
    """
    Calcular minutos desde el último acceso
    
    Args:
        ultimo_acceso: DateTime del último acceso
        
    Returns:
        int: Minutos de inactividad, None si nunca accedió
    """
    if not ultimo_acceso:
        return None
    
    delta = datetime.now() - ultimo_acceso
    return int(delta.total_seconds() / 60)
```

#### determinar_estado_usuario(usuario)
```python
def determinar_estado_usuario(usuario):
    """
    Determinar estado del usuario basado en último acceso
    
    Estados:
    - activo: menos de 15 minutos
    - inactivo: entre 15 y 60 minutos
    - ausente: más de 60 minutos o nunca conectado
    
    Args:
        usuario: User object
        
    Returns:
        str: 'activo', 'inactivo', o 'ausente'
    """
    if not usuario.ultimo_acceso:
        return 'ausente'
    
    minutos = calcular_minutos_inactivo(usuario.ultimo_acceso)
    
    if minutos < 15:
        return 'activo'
    elif minutos < 60:
        return 'inactivo'
    else:
        return 'ausente'
```

### 4. Frontend Components

#### Botón de Verificación de Presencia
```javascript
async function verificarPresencia() {
    try {
        // Solicitar geolocalización
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject, {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            });
        });
        
        // Enviar al backend
        const response = await fetch('/api/verificacion/presencia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                latitud: position.coords.latitude,
                longitud: position.coords.longitude,
                precision: position.coords.accuracy
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            mostrarMensajeExito('Presencia verificada exitosamente');
            iniciarPingAutomatico();
        }
    } catch (error) {
        manejarErrorGPS(error);
    }
}
```

#### Ping Automático
```javascript
let pingInterval = null;

function iniciarPingAutomatico() {
    // Limpiar intervalo anterior si existe
    if (pingInterval) {
        clearInterval(pingInterval);
    }
    
    // Enviar ping cada 5 minutos
    pingInterval = setInterval(async () => {
        try {
            const response = await fetch('/api/verificacion/ping', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            const data = await response.json();
            
            if (!data.success) {
                console.error('Error en ping:', data.error);
            }
        } catch (error) {
            console.error('Error enviando ping:', error);
        }
    }, 5 * 60 * 1000); // 5 minutos
}

// Detener ping al cerrar ventana
window.addEventListener('beforeunload', () => {
    if (pingInterval) {
        clearInterval(pingInterval);
    }
});
```

#### Mapa de Usuarios Geolocalizados
```javascript
let map = null;
let markers = [];

async function cargarMapaUsuarios() {
    // Inicializar mapa
    map = L.map('map').setView([4.6097, -74.0817], 6);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Cargar usuarios
    const response = await fetch('/api/verificacion/usuarios-geolocalizados', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const data = await response.json();
    
    if (data.success) {
        data.data.forEach(usuario => {
            agregarMarcadorUsuario(usuario);
        });
    }
}

function agregarMarcadorUsuario(usuario) {
    // Color según estado
    const color = {
        'activo': 'green',
        'inactivo': 'yellow',
        'ausente': 'red'
    }[usuario.estado];
    
    // Crear marcador
    const marker = L.circleMarker([usuario.latitud, usuario.longitud], {
        radius: 8,
        fillColor: color,
        color: '#000',
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    }).addTo(map);
    
    // Popup con información
    marker.bindPopup(`
        <strong>${usuario.nombre}</strong><br>
        Rol: ${usuario.rol}<br>
        Ubicación: ${usuario.ubicacion_nombre}<br>
        Último acceso: hace ${usuario.minutos_inactivo} minutos<br>
        Estado: ${usuario.estado}<br>
        Coordenadas: ${usuario.latitud.toFixed(6)}, ${usuario.longitud.toFixed(6)}
    `);
    
    markers.push(marker);
}
```

## Data Models

### Database Schema

```sql
-- Extensión de tabla users con campos de geolocalización
ALTER TABLE users ADD COLUMN presencia_verificada BOOLEAN DEFAULT FALSE NOT NULL;
ALTER TABLE users ADD COLUMN presencia_verificada_at TIMESTAMP;
ALTER TABLE users ADD COLUMN ultima_latitud FLOAT;
ALTER TABLE users ADD COLUMN ultima_longitud FLOAT;
ALTER TABLE users ADD COLUMN ultima_geolocalizacion_at TIMESTAMP;
ALTER TABLE users ADD COLUMN precision_geolocalizacion FLOAT;

-- Índices para optimizar queries
CREATE INDEX idx_users_presencia_verificada ON users(presencia_verificada);
CREATE INDEX idx_users_ultimo_acceso ON users(ultimo_acceso);
CREATE INDEX idx_users_geolocalizacion ON users(ultima_latitud, ultima_longitud) 
    WHERE ultima_latitud IS NOT NULL AND ultima_longitud IS NOT NULL;
```

### Data Relationships

```
User (N) ──────── (1) Location
     │                  (ubicacion_id)
     │
     └── presencia_verificada: Boolean
     └── presencia_verificada_at: DateTime
     └── ultima_latitud: Float
     └── ultima_longitud: Float
     └── ultima_geolocalizacion_at: DateTime
     └── precision_geolocalizacion: Float
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Presence Verification Updates Timestamp
*For any* user who verifies presence, the presencia_verificada_at timestamp should be updated to the current time
**Validates: Requirements 1.3**

### Property 2: GPS Coordinates Consistency
*For any* user with GPS coordinates, if ultima_latitud is not null, then ultima_longitud should also not be null, and vice versa
**Validates: Requirements 2.2, 2.3**

### Property 3: Activity State Classification
*For any* user, if ultimo_acceso is less than 15 minutes ago, determinar_estado_usuario() should return 'activo'; if between 15-60 minutes, should return 'inactivo'; if more than 60 minutes or null, should return 'ausente'
**Validates: Requirements 4.1, 4.2, 4.3, 4.4**

### Property 4: Ping Updates Last Access
*For any* user who sends a ping, the ultimo_acceso timestamp should be updated to the current time
**Validates: Requirements 5.2**

### Property 5: Team Filtering by Jurisdiction
*For any* coordinador_puesto, the estado-equipo endpoint should return only testigos from their puesto, not from other puestos
**Validates: Requirements 6.1**

### Property 6: Geolocation Timestamp Consistency
*For any* user with GPS coordinates, if ultima_latitud and ultima_longitud are not null, then ultima_geolocalizacion_at should also not be null
**Validates: Requirements 2.4**

### Property 7: Statistics Calculation Accuracy
*For any* team, the sum of (presentes + inactivos + ausentes) should equal total
**Validates: Requirements 7.1, 7.2, 7.3, 7.4**

### Property 8: Map User Filtering
*For any* coordinador_municipal viewing the map, all returned users should have ubicacion_id within the coordinator's municipio
**Validates: Requirements 8.3, 8.4**

### Property 9: Coordinate Precision Format
*For any* displayed coordinates, they should be formatted with exactly 6 decimal places
**Validates: Requirements 3.5, 9.5**

### Property 10: Presence Verification Idempotence
*For any* user, calling verificar_presencia() multiple times should always result in presencia_verificada = True, with the timestamp updated to the most recent call
**Validates: Requirements 1.2, 1.3**

## Error Handling

### Error Categories

1. **GPS Permission Errors** (Browser-level)
   - Permission denied by user
   - Permission not supported by browser
   - Geolocation API not available

2. **GPS Acquisition Errors** (Browser-level)
   - Timeout (position unavailable within time limit)
   - Position unavailable (GPS hardware issue)
   - Low accuracy (precision > 100 meters)

3. **Authorization Errors** (403 Forbidden)
   - Non-coordinator attempting to view team status
   - User attempting to view users outside their jurisdiction

4. **Not Found Errors** (404 Not Found)
   - User ID does not exist
   - Location ID does not exist

5. **Business Logic Errors** (400 Bad Request)
   - User without assigned location
   - Invalid coordinates (latitude not in [-90, 90], longitude not in [-180, 180])

6. **Server Errors** (500 Internal Server Error)
   - Database connection failures
   - Unexpected exceptions

### Error Response Format

```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

### GPS Error Handling

```javascript
function manejarErrorGPS(error) {
    let mensaje = '';
    
    switch(error.code) {
        case error.PERMISSION_DENIED:
            mensaje = 'Permiso de ubicación denegado. Por favor, habilite la ubicación en su navegador.';
            break;
        case error.POSITION_UNAVAILABLE:
            mensaje = 'GPS no disponible en este dispositivo';
            break;
        case error.TIMEOUT:
            mensaje = 'Tiempo de espera agotado. Intente nuevamente.';
            break;
        default:
            mensaje = 'Error desconocido al obtener ubicación';
    }
    
    mostrarMensajeError(mensaje);
}
```

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and edge cases:

1. **Model Tests**
   - Test User.verificar_presencia() updates fields correctly
   - Test User.to_dict() includes geolocation fields
   - Test coordinate storage with valid values
   - Test coordinate storage with null values

2. **Business Logic Tests**
   - Test calcular_minutos_inactivo() with various timestamps
   - Test calcular_minutos_inactivo() with null ultimo_acceso
   - Test determinar_estado_usuario() returns 'activo' for recent access
   - Test determinar_estado_usuario() returns 'inactivo' for 30 min ago
   - Test determinar_estado_usuario() returns 'ausente' for 90 min ago
   - Test determinar_estado_usuario() returns 'ausente' for null access

3. **API Tests**
   - Test POST /presencia with valid coordinates
   - Test POST /presencia without coordinates
   - Test POST /ping updates ultimo_acceso
   - Test GET /estado-equipo for coordinador_puesto
   - Test GET /estado-equipo for coordinador_municipal
   - Test GET /usuarios-geolocalizados filters by jurisdiction
   - Test authorization on protected endpoints

4. **Filtering Tests**
   - Test coordinador_puesto sees only their testigos
   - Test coordinador_municipal sees only their coordinadores_puesto
   - Test coordinador_departamental sees only their coordinadores_municipal
   - Test super_admin sees all coordinadores_departamental

### Property-Based Testing

Property-based tests will use **Hypothesis** library for Python to verify universal properties across many randomly generated inputs:

1. **Property Test: Presence Verification Updates Timestamp**
   - Generate random users
   - Call verificar_presencia()
   - Verify presencia_verificada_at is updated

2. **Property Test: GPS Coordinates Consistency**
   - Generate random users with coordinates
   - Verify if latitud is not null, longitud is also not null

3. **Property Test: Activity State Classification**
   - Generate random users with various ultimo_acceso values
   - Verify determinar_estado_usuario() returns correct state

4. **Property Test: Statistics Calculation**
   - Generate random teams
   - Calculate statistics
   - Verify presentes + inactivos + ausentes = total

5. **Property Test: Coordinate Precision**
   - Generate random coordinates
   - Format with 6 decimal places
   - Verify format is correct

### Integration Testing

Integration tests will verify end-to-end workflows:

1. User verifies presence → Coordinates saved → Appears on map
2. User sends ping → ultimo_acceso updated → Estado changes to 'activo'
3. Coordinator views team → Sees filtered users → Statistics calculated correctly
4. User inactive for 20 minutes → Estado changes to 'inactivo'
5. User inactive for 70 minutes → Estado changes to 'ausente'

### Test Configuration

- **Framework**: pytest
- **Property Testing**: Hypothesis
- **Coverage Target**: 90%+
- **Test Database**: Separate test database
- **Mock GPS**: Mock browser geolocation for frontend tests

## Security Considerations

### Authentication & Authorization

- All endpoints require JWT authentication
- Team status endpoints require coordinator roles
- Users can only verify their own presence
- Coordinators can only view users in their jurisdiction
- Role validation using @role_required decorator

### Data Privacy

- GPS coordinates stored securely in database
- Users can only see their own coordinates
- Coordinators can only see coordinates of users under supervision
- HTTPS encryption for all GPS data transmission
- Location history retained for audit but marked as archived when user deactivated

### Input Validation

- Latitude validation: -90 to 90
- Longitude validation: -180 to 180
- Precision validation: positive float
- Timestamp validation: not in future
- SQL injection prevention via SQLAlchemy ORM

### GPS Security

- Browser geolocation requires user permission
- High accuracy mode for better precision
- Timeout to prevent indefinite waiting
- Maximum age = 0 to prevent cached locations
- Error handling for denied permissions

## Performance Considerations

### Database Optimization

- Index on users.presencia_verificada for fast filtering
- Index on users.ultimo_acceso for activity state queries
- Composite index on (ultima_latitud, ultima_longitud) for map queries
- Efficient query: User.query.filter(latitud.isnot(None), longitud.isnot(None))

### Caching Strategy

- Team status can be cached for 1 minute (changes infrequently)
- Map data can be cached for 2 minutes
- Cache invalidation on presence verification
- User estado calculated on-demand (not stored)

### Ping Optimization

- Ping every 5 minutes (not too frequent)
- Lightweight endpoint (only updates timestamp)
- No response body needed
- Automatic retry on failure (max 3 attempts)

### Map Performance

- Load only users with coordinates (filter in database)
- Limit to 1000 markers maximum
- Cluster markers when zoomed out
- Lazy load marker popups

## Deployment Considerations

### Database Migrations

- Add geolocation columns to users table
- Create indexes for performance
- Set default values for existing users
- Backfill presencia_verificada = False

### Browser Compatibility

- Geolocation API supported in all modern browsers
- Fallback message for unsupported browsers
- HTTPS required for geolocation (security requirement)
- Test on mobile browsers (iOS Safari, Chrome Android)

### Mobile Considerations

- GPS more accurate on mobile devices
- Battery consumption from frequent GPS requests
- Ping interval optimized for battery life (5 minutes)
- High accuracy mode may drain battery faster

### Environment Configuration

- GPS timeout configuration (default 10 seconds)
- Ping interval configuration (default 5 minutes)
- Activity thresholds configuration (15 min, 60 min)
- Map provider configuration (Leaflet, Google Maps)

## Future Enhancements

1. **Geofencing**: Automatic alerts when users leave assigned area
2. **Route Tracking**: Track user movement throughout the day
3. **Offline Mode**: Queue presence verifications when offline
4. **Push Notifications**: Real-time alerts for coordinators
5. **Heatmaps**: Visualize user density on map
6. **Historical Playback**: Replay user movements over time
7. **Battery Optimization**: Adaptive ping frequency based on battery level
8. **Indoor Positioning**: Support for indoor location (WiFi, Bluetooth)
9. **Location Sharing**: Allow users to share location with specific coordinators
10. **Proximity Alerts**: Notify when users are near each other

