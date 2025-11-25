# Design Document - Sistema de Incidentes y Delitos Electorales

## Overview

El Sistema de Incidentes y Delitos Electorales es un módulo crítico del sistema electoral que permite reportar, dar seguimiento y resolver irregularidades operacionales (incidentes) y violaciones legales (delitos) durante el proceso electoral. El sistema está implementado con una arquitectura de servicios que separa la lógica de negocio de las rutas API, utilizando 4 modelos de datos principales (IncidenteElectoral, DelitoElectoral, SeguimientoReporte, NotificacionReporte) y un servicio centralizado (IncidentesDelitosService) que maneja toda la lógica de creación, actualización, notificaciones y estadísticas.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Dashboards)                     │
│  - Formulario de reporte de incidentes                      │
│  - Formulario de reporte de delitos                         │
│  - Lista de reportes con filtros                            │
│  - Detalle de reporte con seguimiento                       │
│  - Notificaciones en tiempo real                            │
│  - Estadísticas y gráficos                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API REST Layer                            │
│  - POST /api/incidentes (crear incidente)                   │
│  - GET /api/incidentes (listar incidentes)                  │
│  - PUT /api/incidentes/:id (actualizar incidente)           │
│  - POST /api/delitos (crear delito)                         │
│  - GET /api/delitos (listar delitos)                        │
│  - PUT /api/delitos/:id (actualizar delito)                 │
│  - POST /api/delitos/:id/denunciar (denuncia formal)        │
│  - GET /api/reportes/estadisticas (estadísticas)            │
│  - GET /api/reportes/notificaciones (notificaciones)        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                             │
│  IncidentesDelitosService                                   │
│  - crear_incidente()                                        │
│  - crear_delito()                                           │
│  - obtener_incidentes()                                     │
│  - obtener_delitos()                                        │
│  - actualizar_estado_incidente()                            │
│  - actualizar_estado_delito()                               │
│  - denunciar_formalmente()                                  │
│  - obtener_estadisticas()                                   │
│  - _registrar_seguimiento()                                 │
│  - _crear_notificaciones_incidente()                        │
│  - _crear_notificaciones_delito()                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  - IncidenteElectoral (incidentes)                          │
│  - DelitoElectoral (delitos)                                │
│  - SeguimientoReporte (historial)                           │
│  - NotificacionReporte (notificaciones)                     │
│  - PostgreSQL Database                                      │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **Service Layer**: IncidentesDelitosService (business logic)
- **File Upload**: For evidence attachments
- **Frontend**: HTML, JavaScript, Bootstrap
- **Notifications**: Database-driven notifications

## Components and Interfaces

### 1. Data Models

#### IncidenteElectoral Model

```python
class IncidenteElectoral(db.Model):
    __tablename__ = 'incidentes_electorales'
    
    # Identificación
    id: Integer (Primary Key)
    reportado_por_id: Integer (Foreign Key: users.id)
    
    # Ubicación
    mesa_id: Integer (Foreign Key: locations.id, Nullable)
    puesto_id: Integer (Foreign Key: locations.id, Nullable)
    municipio_id: Integer (Foreign Key: locations.id, Nullable)
    departamento_id: Integer (Foreign Key: locations.id, Nullable)
    
    # Información del incidente
    tipo_incidente: String(50) (Not Null)
    titulo: String(200) (Not Null)
    descripcion: Text (Not Null)
    severidad: String(20) (Default: 'media')  # baja, media, alta, critica
    estado: String(20) (Default: 'reportado')  # reportado, en_revision, resuelto, escalado
    
    # Evidencia y ubicación
    evidencia_url: String(500) (Nullable)
    ubicacion_gps: String(100) (Nullable)
    
    # Fechas
    fecha_incidente: DateTime (Nullable)
    fecha_reporte: DateTime (Default: utcnow)
    
    # Resolución
    resuelto_por_id: Integer (Foreign Key: users.id, Nullable)
    fecha_resolucion: DateTime (Nullable)
    notas_resolucion: Text (Nullable)
    escalado_a: String(50) (Nullable)
    
    created_at: DateTime (Default: utcnow)
    updated_at: DateTime (Default: utcnow, OnUpdate: utcnow)
    
    # Tipos de incidentes
    TIPOS_INCIDENTE = {
        'retraso_apertura', 'falta_material', 'problemas_tecnicos',
        'irregularidades_proceso', 'ausencia_funcionarios',
        'problemas_acceso', 'disturbios', 'otros'
    }
    
    # Niveles de severidad
    SEVERIDADES = {'baja', 'media', 'alta', 'critica'}
    
    # Estados
    ESTADOS = {'reportado', 'en_revision', 'resuelto', 'escalado'}
```

#### DelitoElectoral Model

```python
class DelitoElectoral(db.Model):
    __tablename__ = 'delitos_electorales'
    
    # Identificación
    id: Integer (Primary Key)
    reportado_por_id: Integer (Foreign Key: users.id)
    
    # Ubicación
    mesa_id: Integer (Foreign Key: locations.id, Nullable)
    puesto_id: Integer (Foreign Key: locations.id, Nullable)
    municipio_id: Integer (Foreign Key: locations.id, Nullable)
    departamento_id: Integer (Foreign Key: locations.id, Nullable)
    
    # Información del delito
    tipo_delito: String(50) (Not Null)
    titulo: String(200) (Not Null)
    descripcion: Text (Not Null)
    gravedad: String(20) (Default: 'media')  # leve, media, grave, muy_grave
    estado: String(30) (Default: 'reportado')  # reportado, en_investigacion, investigado, denunciado, archivado
    
    # Evidencia y testigos
    evidencia_url: String(500) (Nullable)
    testigos_adicionales: Text (Nullable)
    ubicacion_gps: String(100) (Nullable)
    
    # Fechas
    fecha_delito: DateTime (Nullable)
    fecha_reporte: DateTime (Default: utcnow)
    
    # Investigación
    investigado_por_id: Integer (Foreign Key: users.id, Nullable)
    fecha_investigacion: DateTime (Nullable)
    resultado_investigacion: Text (Nullable)
    
    # Denuncia formal
    denunciado_formalmente: Boolean (Default: False)
    numero_denuncia: String(100) (Nullable)
    autoridad_competente: String(200) (Nullable)
    fecha_denuncia: DateTime (Nullable)
    seguimiento: Text (Nullable)
    
    created_at: DateTime (Default: utcnow)
    updated_at: DateTime (Default: utcnow, OnUpdate: utcnow)
    
    # Tipos de delitos
    TIPOS_DELITO = {
        'compra_votos', 'coaccion_votante', 'fraude_electoral',
        'suplantacion_identidad', 'alteracion_resultados',
        'violencia_electoral', 'propaganda_ilegal',
        'financiacion_ilegal', 'otros_delitos'
    }
    
    # Niveles de gravedad
    GRAVEDADES = {'leve', 'media', 'grave', 'muy_grave'}
    
    # Estados
    ESTADOS = {'reportado', 'en_investigacion', 'investigado', 'denunciado', 'archivado'}
```

#### SeguimientoReporte Model

```python
class SeguimientoReporte(db.Model):
    __tablename__ = 'seguimiento_reportes'
    
    id: Integer (Primary Key)
    tipo_reporte: String(20) (Not Null)  # 'incidente' o 'delito'
    reporte_id: Integer (Not Null)
    usuario_id: Integer (Foreign Key: users.id)
    accion: String(50) (Not Null)
    comentario: Text (Nullable)
    estado_anterior: String(30) (Nullable)
    estado_nuevo: String(30) (Nullable)
    created_at: DateTime (Default: utcnow)
```

#### NotificacionReporte Model

```python
class NotificacionReporte(db.Model):
    __tablename__ = 'notificaciones_reportes'
    
    id: Integer (Primary Key)
    usuario_id: Integer (Foreign Key: users.id)
    tipo_reporte: String(20) (Not Null)  # 'incidente' o 'delito'
    reporte_id: Integer (Not Null)
    tipo_notificacion: String(50) (Not Null)
    titulo: String(200) (Not Null)
    mensaje: Text (Not Null)
    leida: Boolean (Default: False)
    fecha_lectura: DateTime (Nullable)
    created_at: DateTime (Default: utcnow)
```

### 2. Service Layer

#### IncidentesDelitosService

**Métodos principales:**

- `crear_incidente(data, usuario_id)` - Crea un nuevo incidente
- `crear_delito(data, usuario_id)` - Crea un nuevo delito
- `obtener_incidentes(filtros, usuario_id, rol_usuario)` - Lista incidentes con filtros y permisos
- `obtener_delitos(filtros, usuario_id, rol_usuario)` - Lista delitos con filtros y permisos
- `actualizar_estado_incidente(incidente_id, nuevo_estado, usuario_id, comentario)` - Actualiza estado de incidente
- `actualizar_estado_delito(delito_id, nuevo_estado, usuario_id, comentario)` - Actualiza estado de delito
- `denunciar_formalmente(delito_id, usuario_id, numero_denuncia, autoridad_competente)` - Registra denuncia formal
- `obtener_estadisticas(usuario_id, rol_usuario)` - Calcula estadísticas de reportes
- `obtener_seguimiento(tipo_reporte, reporte_id)` - Obtiene historial de seguimiento
- `obtener_notificaciones(usuario_id, solo_no_leidas)` - Obtiene notificaciones del usuario
- `marcar_notificacion_leida(notificacion_id)` - Marca notificación como leída

**Métodos privados:**

- `_registrar_seguimiento()` - Registra acción en historial
- `_crear_notificaciones_incidente()` - Crea notificaciones para incidente
- `_crear_notificaciones_delito()` - Crea notificaciones para delito

## Data Models

### Database Schema

```sql
-- Tabla de incidentes electorales
CREATE TABLE incidentes_electorales (
    id SERIAL PRIMARY KEY,
    reportado_por_id INTEGER REFERENCES users(id) NOT NULL,
    mesa_id INTEGER REFERENCES locations(id),
    puesto_id INTEGER REFERENCES locations(id),
    municipio_id INTEGER REFERENCES locations(id),
    departamento_id INTEGER REFERENCES locations(id),
    tipo_incidente VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    severidad VARCHAR(20) DEFAULT 'media',
    estado VARCHAR(20) DEFAULT 'reportado',
    evidencia_url VARCHAR(500),
    ubicacion_gps VARCHAR(100),
    fecha_incidente TIMESTAMP,
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resuelto_por_id INTEGER REFERENCES users(id),
    fecha_resolucion TIMESTAMP,
    notas_resolucion TEXT,
    escalado_a VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de delitos electorales
CREATE TABLE delitos_electorales (
    id SERIAL PRIMARY KEY,
    reportado_por_id INTEGER REFERENCES users(id) NOT NULL,
    mesa_id INTEGER REFERENCES locations(id),
    puesto_id INTEGER REFERENCES locations(id),
    municipio_id INTEGER REFERENCES locations(id),
    departamento_id INTEGER REFERENCES locations(id),
    tipo_delito VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    gravedad VARCHAR(20) DEFAULT 'media',
    estado VARCHAR(30) DEFAULT 'reportado',
    evidencia_url VARCHAR(500),
    testigos_adicionales TEXT,
    ubicacion_gps VARCHAR(100),
    fecha_delito TIMESTAMP,
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    investigado_por_id INTEGER REFERENCES users(id),
    fecha_investigacion TIMESTAMP,
    resultado_investigacion TEXT,
    denunciado_formalmente BOOLEAN DEFAULT FALSE,
    numero_denuncia VARCHAR(100),
    autoridad_competente VARCHAR(200),
    fecha_denuncia TIMESTAMP,
    seguimiento TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de seguimiento de reportes
CREATE TABLE seguimiento_reportes (
    id SERIAL PRIMARY KEY,
    tipo_reporte VARCHAR(20) NOT NULL,
    reporte_id INTEGER NOT NULL,
    usuario_id INTEGER REFERENCES users(id) NOT NULL,
    accion VARCHAR(50) NOT NULL,
    comentario TEXT,
    estado_anterior VARCHAR(30),
    estado_nuevo VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de notificaciones de reportes
CREATE TABLE notificaciones_reportes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES users(id) NOT NULL,
    tipo_reporte VARCHAR(20) NOT NULL,
    reporte_id INTEGER NOT NULL,
    tipo_notificacion VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    leida BOOLEAN DEFAULT FALSE,
    fecha_lectura TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_incidentes_estado ON incidentes_electorales(estado);
CREATE INDEX idx_incidentes_severidad ON incidentes_electorales(severidad);
CREATE INDEX idx_incidentes_puesto ON incidentes_electorales(puesto_id);
CREATE INDEX idx_incidentes_municipio ON incidentes_electorales(municipio_id);
CREATE INDEX idx_delitos_estado ON delitos_electorales(estado);
CREATE INDEX idx_delitos_gravedad ON delitos_electorales(gravedad);
CREATE INDEX idx_delitos_puesto ON delitos_electorales(puesto_id);
CREATE INDEX idx_delitos_municipio ON delitos_electorales(municipio_id);
CREATE INDEX idx_seguimiento_reporte ON seguimiento_reportes(tipo_reporte, reporte_id);
CREATE INDEX idx_notificaciones_usuario ON notificaciones_reportes(usuario_id, leida);
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Report Creation Timestamps
*For any* created report (incident or crime), the fecha_reporte should be set to the current timestamp
**Validates: Requirements 1.5, 4.5**

### Property 2: Automatic Location Hierarchy
*For any* report with mesa_id, the system should automatically populate puesto_id, municipio_id, and departamento_id based on the mesa's location hierarchy
**Validates: Requirements 1.2, 4.2**

### Property 3: Default Estado Values
*For any* newly created incident, estado should be 'reportado'; for any newly created crime, estado should be 'reportado'
**Validates: Requirements 1.3, 4.3**

### Property 4: Seguimiento Creation on Actions
*For any* action performed on a report (create, update estado, resolve), a seguimiento record should be created
**Validates: Requirements 11.1**

### Property 5: Critical Incident Notifications
*For any* incident with severidad 'critica', notifications should be sent to both coordinador_puesto and coordinador_municipal
**Validates: Requirements 3.3, 12.2**

### Property 6: Crime Notifications to Multiple Roles
*For any* created crime, notifications should be sent to coordinador_municipal, coordinador_departamental, and all auditor_electoral users
**Validates: Requirements 12.3**

### Property 7: Resolution Timestamp Consistency
*For any* incident marked as 'resuelto', the fecha_resolucion should be set and resuelto_por_id should be populated
**Validates: Requirements 13.2, 13.3**

### Property 8: Investigation Timestamp Consistency
*For any* crime with estado 'en_investigacion', the fecha_investigacion should be set and investigado_por_id should be populated
**Validates: Requirements 14.2**

### Property 9: Formal Complaint Fields
*For any* crime with denunciado_formalmente=True, the fields numero_denuncia, autoridad_competente, and fecha_denuncia should all be non-null
**Validates: Requirements 15.1, 15.2, 15.3, 15.4**

### Property 10: Permission-Based Filtering
*For any* testigo_electoral viewing reports, only reports where reportado_por_id equals the testigo's ID should be returned
**Validates: Requirements 19.1**

## Error Handling

### Error Categories

1. **Validation Errors** (400 Bad Request)
   - Invalid tipo_incidente or tipo_delito
   - Missing required fields
   - Invalid estado transition
   - Invalid severidad or gravedad

2. **Authorization Errors** (403 Forbidden)
   - User attempting to view reports outside their jurisdiction
   - Non-coordinator attempting to resolve incidents
   - Non-auditor attempting to investigate crimes

3. **Not Found Errors** (404 Not Found)
   - Report ID does not exist
   - User ID does not exist
   - Location ID does not exist

4. **Business Logic Errors** (400 Bad Request)
   - Attempting to resolve already resolved incident
   - Attempting to formally report crime without investigation
   - Invalid estado transition

5. **Server Errors** (500 Internal Server Error)
   - Database connection failures
   - File upload failures
   - Unexpected exceptions

## Testing Strategy

### Unit Testing

1. **Model Tests**
   - Test IncidenteElectoral.to_dict() serialization
   - Test DelitoElectoral.to_dict() serialization
   - Test SeguimientoReporte.to_dict() serialization
   - Test NotificacionReporte.marcar_como_leida()

2. **Service Tests**
   - Test crear_incidente() creates incident with correct fields
   - Test crear_delito() creates crime with correct fields
   - Test obtener_incidentes() filters by role correctly
   - Test obtener_delitos() filters by role correctly
   - Test actualizar_estado_incidente() updates estado and creates seguimiento
   - Test denunciar_formalmente() sets all required fields
   - Test obtener_estadisticas() calculates counts correctly
   - Test _crear_notificaciones_incidente() creates correct notifications
   - Test _crear_notificaciones_delito() notifies all required roles

3. **Permission Tests**
   - Test testigo only sees their own reports
   - Test coordinador_puesto only sees reports from their puesto
   - Test coordinador_municipal only sees reports from their municipio
   - Test super_admin sees all reports

### Property-Based Testing

Property-based tests will use **Hypothesis** library for Python:

1. **Property Test: Report Creation Timestamps**
   - Generate random reports
   - Verify fecha_reporte is set

2. **Property Test: Automatic Location Hierarchy**
   - Generate random mesas
   - Create reports with mesa_id
   - Verify puesto_id, municipio_id, departamento_id are populated

3. **Property Test: Seguimiento Creation**
   - Perform random actions on reports
   - Verify seguimiento records are created

4. **Property Test: Statistics Calculation**
   - Generate random reports
   - Calculate statistics
   - Verify counts match actual data

### Integration Testing

1. Create incident → Verify notifications sent → Resolve incident → Verify seguimiento
2. Create crime → Investigate → Formally report → Verify all fields set
3. Create critical incident → Verify both coordinador_puesto and coordinador_municipal notified
4. Filter reports by role → Verify only authorized reports returned

## Security Considerations

- All endpoints require JWT authentication
- Reports filtered by user role and jurisdiction
- Only coordinators can resolve incidents
- Only auditores can investigate crimes
- Evidence files validated for type and size
- SQL injection prevention via SQLAlchemy ORM

## Performance Considerations

- Indexes on estado, severidad/gravedad, puesto_id, municipio_id
- Efficient filtering in database queries
- Pagination for large result sets
- Caching of statistics (updated on report creation)

## Future Enhancements

1. Real-time notifications via WebSockets
2. Mobile app for field reporting
3. Photo/video evidence upload
4. Automatic escalation based on severity/gravity
5. Integration with external authorities
6. Advanced analytics and pattern detection
7. Geofencing alerts
8. Multi-language support
9. Voice-to-text for descriptions
10. Blockchain for evidence integrity

