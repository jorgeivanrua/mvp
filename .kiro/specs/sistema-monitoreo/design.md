# Design Document - Sistema de Monitoreo en Tiempo Real

## Overview

El Sistema de Monitoreo en Tiempo Real es un módulo de supervisión global del sistema electoral que permite a usuarios con rol 'monitoreo' visualizar y analizar toda la actividad del sistema sin restricciones de jurisdicción. El sistema está implementado con un dashboard centralizado que integra mapas de geolocalización, estadísticas en tiempo real, feeds de actividad reciente, y alertas automáticas. A diferencia de los coordinadores que tienen visibilidad limitada a su jurisdicción, el rol de monitoreo tiene acceso completo a todos los datos para supervisión y análisis.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Monitoring Dashboard (Frontend)                 │
│  - Mapa global de usuarios geolocalizados                   │
│  - Panel de estadísticas globales                           │
│  - Feed de actividad reciente                               │
│  - Panel de alertas                                         │
│  - Herramientas de filtrado y búsqueda                      │
│  - Auto-refresh cada 30 segundos                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API REST Layer                            │
│  Blueprint: monitoreo_bp                                    │
│  Prefix: /monitoreo                                         │
│  - GET /dashboard (render dashboard)                        │
│  - GET /api/usuarios-activos (todos los usuarios con GPS)  │
│  - GET /api/estadisticas (estadísticas globales)           │
│  - GET /api/actividad-reciente (últimos eventos)           │
│  - GET /api/alertas (alertas críticas)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  - User (todos los usuarios)                                │
│  - FormularioE14 (todos los formularios)                    │
│  - IncidenteElectoral (todos los incidentes)                │
│  - DelitoElectoral (todos los delitos)                      │
│  - Location (todas las ubicaciones)                         │
│  - PostgreSQL Database                                      │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **Authorization**: @role_required('monitoreo') decorator
- **Maps**: Leaflet.js for global user visualization
- **Charts**: Chart.js for statistics
- **Real-time**: Polling every 30 seconds
- **Frontend**: HTML, JavaScript, Bootstrap

## Components and Interfaces

### 1. API Endpoints

#### GET /monitoreo/dashboard
- **Description**: Render monitoring dashboard
- **Authentication**: JWT Required
- **Authorization**: monitoreo role only
- **Response**: HTML template

#### GET /monitoreo/api/usuarios-activos
- **Description**: Get all active users with geolocation
- **Authentication**: JWT Required
- **Authorization**: monitoreo role only
- **Response**: 
  ```json
  {
    "success": true,
    "data": [
      {
        "id": 123,
        "nombre": "Juan Pérez",
        "rol": "testigo_electoral",
        "latitud": 4.6097,
        "longitud": -74.0817,
        "precision": 10.5,
        "ultima_actualizacion": "2025-11-25T10:30:00",
        "ubicacion": { /* location object */ },
        "presencia_verificada": true
      }
    ],
    "total": 150
  }
  ```

#### GET /monitoreo/api/estadisticas
- **Description**: Get global system statistics
- **Authentication**: JWT Required
- **Authorization**: monitoreo role only
- **Response**: 
  ```json
  {
    "success": true,
    "data": {
      "testigos": {
        "total": 500,
        "con_geolocalizacion": 450,
        "con_presencia_verificada": 480,
        "porcentaje_geo": 90.0
      },
      "coordinadores": {
        "total": 100,
        "con_geolocalizacion": 85,
        "porcentaje_geo": 85.0
      },
      "formularios": {
        "total": 450,
        "validados": 380,
        "pendientes": 70
      }
    }
  }
  ```

### 2. Frontend Components

#### Global Map Component
- **Purpose**: Display all geolocated users on a map
- **Features**:
  - Markers for all users with GPS
  - Color-coded by role
  - Popup with user details
  - Filter by role
  - Auto-refresh every 30 seconds

#### Statistics Panel
- **Purpose**: Display global statistics
- **Features**:
  - Testigos statistics (total, with GPS, with presence)
  - Coordinadores statistics (total, with GPS)
  - Formularios statistics (total, validated, pending)
  - Progress bars and percentages
  - Auto-refresh every 30 seconds

#### Recent Activity Feed
- **Purpose**: Show latest system events
- **Features**:
  - Last 50 events
  - Event types: formularios, incidentes, delitos, presencias
  - Timestamp and user info
  - Click to view details
  - Auto-refresh every 30 seconds

#### Alerts Panel
- **Purpose**: Display critical alerts
- **Features**:
  - Critical incidents
  - Crimes reported
  - Testigos without presence for 2+ hours
  - Alert status (new, viewed, resolved)
  - Click to view details

## Data Models

### No New Models Required

The monitoring system uses existing models:
- **User**: For user data and geolocation
- **FormularioE14**: For form statistics
- **IncidenteElectoral**: For incident data
- **DelitoElectoral**: For crime data
- **Location**: For geographic data

### Role Configuration

```python
# In User model
ROLES = [
    'super_admin',
    'admin_departamental',
    'admin_municipal',
    'coordinador_departamental',
    'coordinador_municipal',
    'coordinador_puesto',
    'testigo_electoral',
    'auditor_electoral',
    'monitoreo'  # Special role with global visibility
]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Global Visibility
*For any* monitoreo user querying data, no jurisdiction filters should be applied
**Validates: Requirements 1.3, 1.4, 1.5**

### Property 2: Role Authorization
*For any* non-monitoreo user attempting to access monitoring endpoints, the system should return 403 Forbidden
**Validates: Requirements 15.1**

### Property 3: Statistics Accuracy
*For any* statistics query, the sum of (validados + pendientes + rechazados) should equal total formularios
**Validates: Requirements 6.1, 6.2, 6.3, 6.5**

### Property 4: Geolocation Filtering
*For any* usuarios-activos query, all returned users should have non-null ultima_latitud and ultima_longitud
**Validates: Requirements 3.1**

### Property 5: Auto-Refresh Consistency
*For any* dashboard session, data should be refreshed every 30 seconds while the dashboard is active
**Validates: Requirements 2.4**

## Error Handling

### Error Categories

1. **Authorization Errors** (403 Forbidden)
   - Non-monitoreo user attempting to access monitoring dashboard
   - Deactivated monitoreo user attempting access

2. **Not Found Errors** (404 Not Found)
   - Monitoring dashboard route not found
   - API endpoint not found

3. **Server Errors** (500 Internal Server Error)
   - Database connection failures
   - Query timeout
   - Unexpected exceptions

## Testing Strategy

### Unit Testing

1. **Authorization Tests**
   - Test monitoreo user can access dashboard
   - Test non-monitoreo user receives 403
   - Test deactivated monitoreo user receives 403

2. **Data Tests**
   - Test usuarios-activos returns all users with GPS
   - Test estadisticas calculates correct totals
   - Test no jurisdiction filters are applied

3. **Statistics Tests**
   - Test testigos statistics calculation
   - Test coordinadores statistics calculation
   - Test formularios statistics calculation

### Property-Based Testing

Property-based tests will use **Hypothesis** library for Python:

1. **Property Test: Global Visibility**
   - Generate random users across different jurisdictions
   - Query as monitoreo user
   - Verify all users are returned

2. **Property Test: Statistics Accuracy**
   - Generate random formularios with different estados
   - Calculate statistics
   - Verify totals match

3. **Property Test: Geolocation Filtering**
   - Generate random users with and without GPS
   - Query usuarios-activos
   - Verify only users with GPS are returned

### Integration Testing

1. Monitoreo user logs in → Accesses dashboard → Sees all data
2. Non-monitoreo user attempts access → Receives 403
3. Dashboard loads → Auto-refreshes every 30 seconds → Data updates
4. Filter by role → Only users with that role shown
5. Export data → File downloaded with all data

## Security Considerations

- All endpoints require JWT authentication
- Only monitoreo role can access monitoring endpoints
- Access logging for audit purposes
- Sensitive data masking (partial phone numbers, etc.)
- Super admin required to create monitoreo users
- Immediate access revocation on user deactivation

## Performance Considerations

- Indexes on User.ultima_latitud, User.ultima_longitud for fast geolocation queries
- Caching of statistics (updated every 30 seconds)
- Pagination for large datasets
- Efficient queries without jurisdiction filters
- Auto-refresh interval optimized (30 seconds)

## Deployment Considerations

- Monitoring dashboard accessible at /monitoreo/dashboard
- API endpoints under /monitoreo/api/*
- Requires monitoreo role to be added to database
- Super admin can create monitoreo users
- Dashboard optimized for large screens (desktop/tablet)

## Future Enhancements

1. **Real-time Updates**: WebSockets instead of polling
2. **Advanced Analytics**: Machine learning for pattern detection
3. **Custom Dashboards**: User-configurable dashboard layouts
4. **Mobile App**: Dedicated monitoring mobile application
5. **Alert Rules**: Configurable alert thresholds
6. **Historical Analysis**: Time-series data visualization
7. **Predictive Analytics**: Forecast based on historical data
8. **Integration**: Export to external BI tools
9. **Multi-language**: Support for multiple languages
10. **Voice Alerts**: Audio notifications for critical events

