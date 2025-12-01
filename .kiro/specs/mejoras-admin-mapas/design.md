# Design Document: Mejoras Admin y Mapas

## Overview

Este diseño implementa mejoras significativas para el dashboard de Super Admin y la visualización de mapas en el sistema electoral. El enfoque principal es reorganizar la configuración del sistema en pestañas específicas y asegurar que todos los usuarios puedan visualizar correctamente los puestos de votación en los mapas.

El sistema actual tiene dos problemas principales:
1. La configuración del Super Admin está desorganizada, mezclando diferentes tipos de gestión
2. Los mapas no muestran todos los puestos de votación para todos los roles

Esta solución proporciona:
- Una interfaz de configuración organizada por categorías (Partidos, Candidatos, Tipos de Elección, Sistema)
- Visualización completa de puestos en mapas para todos los roles
- Gestión completa de partidos políticos y candidatos
- Indicadores visuales mejorados en mapas
- Capacidades de búsqueda y filtrado en mapas

## Architecture

### Backend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Flask Application                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Partidos   │  │  Candidatos  │  │  Tipos de    │     │
│  │   Routes     │  │   Routes     │  │  Elección    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│  ┌──────▼──────────────────▼──────────────────▼───────┐    │
│  │              Service Layer                          │    │
│  │  - PartidoService                                   │    │
│  │  - CandidatoService                                 │    │
│  │  - TipoEleccionService                              │    │
│  │  - ConfiguracionService                             │    │
│  └──────┬──────────────────────────────────────────────┘    │
│         │                                                    │
│  ┌──────▼──────────────────────────────────────────────┐    │
│  │              Data Access Layer                       │    │
│  │  - PartidoPolitico Model                            │    │
│  │  - Candidato Model                                  │    │
│  │  - TipoEleccion Model                               │    │
│  │  - ConfiguracionSistema Model                       │    │
│  └──────┬──────────────────────────────────────────────┘    │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
    ┌─────▼─────┐
    │ PostgreSQL │
    └───────────┘
```

### Frontend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Super Admin Dashboard                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Navigation Tabs                            │   │
│  │  [Usuarios] [Puestos] [Configuración] [Mapas]       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Configuración Sub-Tabs                       │   │
│  │  [Partidos] [Candidatos] [Tipos] [Sistema]          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Content Area                               │   │
│  │  - Partidos Manager (CRUD)                           │   │
│  │  - Candidatos Manager (CRUD)                         │   │
│  │  - Tipos Elección Manager (CRUD)                     │   │
│  │  - Sistema Config (Settings)                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Map Visualization                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Search Bar + Filters                                │   │
│  │  [Buscar puesto...] [Incidentes] [Delitos] [...]    │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Leaflet Map                                │   │
│  │                                                       │   │
│  │    📍 Puesto Normal                                  │   │
│  │    🔴 Puesto con Incidente Crítico                   │   │
│  │    🟠 Puesto con Delito                              │   │
│  │    🟡 Puesto con Pendientes                          │   │
│  │    🟢 Puesto Completo                                │   │
│  │                                                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Backend Models

#### PartidoPolitico Model
```python
class PartidoPolitico(db.Model):
    __tablename__ = 'partidos_politicos'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False, unique=True)
    sigla = Column(String(20), nullable=False, unique=True)
    color = Column(String(7), nullable=False)  # Hex color
    logo_url = Column(String(500))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    candidatos = relationship('Candidato', back_populates='partido')
```

#### Candidato Model
```python
class Candidato(db.Model):
    __tablename__ = 'candidatos'
    
    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(200), nullable=False)
    partido_id = Column(Integer, ForeignKey('partidos_politicos.id'))
    tipo_eleccion_id = Column(Integer, ForeignKey('tipos_eleccion.id'))
    cargo = Column(String(100), nullable=False)
    numero_lista = Column(Integer)
    foto_url = Column(String(500))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    partido = relationship('PartidoPolitico', back_populates='candidatos')
    tipo_eleccion = relationship('TipoEleccion')
```

#### ConfiguracionSistema Model
```python
class ConfiguracionSistema(db.Model):
    __tablename__ = 'configuracion_sistema'
    
    id = Column(Integer, primary_key=True)
    clave = Column(String(100), nullable=False, unique=True)
    valor = Column(Text)
    tipo = Column(String(50))  # string, integer, boolean, json
    descripcion = Column(Text)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow)
```

### Backend Routes

#### Partidos Routes (`/api/partidos`)
- `GET /api/partidos` - Listar todos los partidos
- `GET /api/partidos/<id>` - Obtener partido específico
- `POST /api/partidos` - Crear nuevo partido
- `PUT /api/partidos/<id>` - Actualizar partido
- `DELETE /api/partidos/<id>` - Eliminar partido
- `POST /api/partidos/<id>/logo` - Subir logo de partido

#### Candidatos Routes (`/api/candidatos`)
- `GET /api/candidatos` - Listar todos los candidatos
- `GET /api/candidatos/<id>` - Obtener candidato específico
- `POST /api/candidatos` - Crear nuevo candidato
- `PUT /api/candidatos/<id>` - Actualizar candidato
- `DELETE /api/candidatos/<id>` - Eliminar candidato
- `POST /api/candidatos/<id>/foto` - Subir foto de candidato

#### Configuración Routes (`/api/configuracion`)
- `GET /api/configuracion` - Obtener toda la configuración
- `GET /api/configuracion/<clave>` - Obtener configuración específica
- `PUT /api/configuracion/<clave>` - Actualizar configuración
- `POST /api/configuracion/exportar` - Exportar configuración completa
- `POST /api/configuracion/importar` - Importar configuración

### Frontend Components

#### PartidosManager.js
Gestiona la interfaz CRUD para partidos políticos:
- Lista de partidos con búsqueda y filtros
- Modal para crear/editar partido
- Upload de logo con preview
- Validación de formularios
- Confirmación de eliminación

#### CandidatosManager.js
Gestiona la interfaz CRUD para candidatos:
- Lista de candidatos con búsqueda y filtros
- Modal para crear/editar candidato
- Selector de partido político
- Selector de tipo de elección
- Upload de foto con preview
- Validación de formularios

#### MapaVisualizacion.js
Mejora la visualización de mapas:
- Carga de todos los puestos geolocalizados
- Indicadores visuales según estado
- Popups con información detallada
- Búsqueda de puestos
- Filtros múltiples
- Actualización en tiempo real

#### ConfiguracionTabs.js
Organiza la configuración en pestañas:
- Sistema de tabs para diferentes categorías
- Navegación entre sub-pestañas
- Carga dinámica de contenido
- Persistencia de tab activo

## Data Models

### Database Schema

```sql
-- Partidos Políticos
CREATE TABLE partidos_politicos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL UNIQUE,
    sigla VARCHAR(20) NOT NULL UNIQUE,
    color VARCHAR(7) NOT NULL,
    logo_url VARCHAR(500),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP
);

-- Candidatos
CREATE TABLE candidatos (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(200) NOT NULL,
    partido_id INTEGER REFERENCES partidos_politicos(id),
    tipo_eleccion_id INTEGER REFERENCES tipos_eleccion(id),
    cargo VARCHAR(100) NOT NULL,
    numero_lista INTEGER,
    foto_url VARCHAR(500),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP
);

-- Configuración del Sistema
CREATE TABLE configuracion_sistema (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT,
    tipo VARCHAR(50),
    descripcion TEXT,
    fecha_actualizacion TIMESTAMP
);

-- Índices
CREATE INDEX idx_candidatos_partido ON candidatos(partido_id);
CREATE INDEX idx_candidatos_tipo_eleccion ON candidatos(tipo_eleccion_id);
CREATE INDEX idx_candidatos_activo ON candidatos(activo);
CREATE INDEX idx_partidos_activo ON partidos_politicos(activo);
CREATE INDEX idx_configuracion_clave ON configuracion_sistema(clave);
```

### API Response Formats

#### Partido Response
```json
{
  "id": 1,
  "nombre": "Partido Ejemplo",
  "sigla": "PE",
  "color": "#FF5733",
  "logo_url": "/uploads/partidos/logo_pe.png",
  "activo": true,
  "fecha_creacion": "2024-01-15T10:30:00Z",
  "fecha_actualizacion": "2024-01-20T14:45:00Z",
  "total_candidatos": 5
}
```

#### Candidato Response
```json
{
  "id": 1,
  "nombre_completo": "Juan Pérez García",
  "partido": {
    "id": 1,
    "nombre": "Partido Ejemplo",
    "sigla": "PE",
    "color": "#FF5733"
  },
  "tipo_eleccion": {
    "id": 1,
    "nombre": "Presidencial"
  },
  "cargo": "Presidente",
  "numero_lista": 1,
  "foto_url": "/uploads/candidatos/foto_1.jpg",
  "activo": true,
  "fecha_creacion": "2024-01-15T10:30:00Z"
}
```

#### Puesto Geolocalizado Response
```json
{
  "id": 1,
  "codigo": "P001",
  "nombre": "Escuela Central",
  "latitud": -17.3935,
  "longitud": -66.1570,
  "municipio": "Cochabamba",
  "departamento": "Cochabamba",
  "total_mesas": 10,
  "incidentes": {
    "total": 2,
    "criticos": 1,
    "activos": 2
  },
  "delitos": {
    "total": 1,
    "graves": 1,
    "activos": 1
  },
  "formularios": {
    "total_esperados": 10,
    "total_recibidos": 7,
    "pendientes": 3
  }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Map Visualization Properties

Property 1: All geolocalized voting locations are displayed
*For any* user role accessing a map dashboard, all voting locations with valid GPS coordinates should be returned in the map data
**Validates: Requirements 1.1**

Property 2: Valid coordinates generate markers
*For any* voting location with valid GPS coordinates (latitude and longitude within valid ranges), a marker should be included in the map response
**Validates: Requirements 1.2**

Property 3: Marker clicks show details
*For any* voting location marker, clicking it should display complete detailed information including name, code, address, and statistics
**Validates: Requirements 1.3**

Property 4: Visual indicators for incidents and crimes
*For any* voting location with incidents or crimes, the map response should include visual indicator data (color, icon, animation) corresponding to the severity
**Validates: Requirements 1.4**

Property 5: Missing GPS coordinates are logged without user errors
*For any* voting location without GPS coordinates, the system should log this condition but not return error responses to users
**Validates: Requirements 1.5**

### Political Parties Management Properties

Property 6: All registered parties are listed
*For any* set of registered political parties in the database, accessing the parties management endpoint should return all of them
**Validates: Requirements 3.1**

Property 7: All party fields are editable
*For any* existing political party, all its fields (nombre, sigla, color, logo_url, activo) should be modifiable through the update endpoint
**Validates: Requirements 3.3**

Property 8: Party deletion requires no associated candidates
*For any* political party with associated candidates, deletion should be rejected; for any party without candidates, deletion should succeed
**Validates: Requirements 3.4**

Property 9: Party logo upload validation
*For any* uploaded file for party logo, the system should validate format (image types only) and size (within configured limits) before accepting
**Validates: Requirements 3.5**

### Candidates Management Properties

Property 10: All registered candidates are listed
*For any* set of registered candidates in the database, accessing the candidates management endpoint should return all of them
**Validates: Requirements 4.1**

Property 11: All candidate fields are editable
*For any* existing candidate, all its fields (nombre_completo, partido_id, tipo_eleccion_id, cargo, numero_lista, foto_url, activo) should be modifiable through the update endpoint
**Validates: Requirements 4.3**

Property 12: Candidate deletion requires no registered votes
*For any* candidate with registered votes, deletion should be rejected; for any candidate without votes, deletion should succeed
**Validates: Requirements 4.4**

Property 13: Candidate party association validation
*For any* candidate creation or update with a partido_id, the system should validate that the party exists in the database before accepting the operation
**Validates: Requirements 4.5**

### Election Types Management Properties

Property 14: All configured election types are listed
*For any* set of configured election types in the database, accessing the election types management endpoint should return all of them
**Validates: Requirements 5.1**

Property 15: All election type fields are editable
*For any* existing election type, all its fields should be modifiable through the update endpoint
**Validates: Requirements 5.3**

Property 16: Election type deletion requires no associated E-14 forms
*For any* election type with associated E-14 forms, deletion should be rejected; for any type without forms, deletion should succeed
**Validates: Requirements 5.4**

Property 17: Election type status changes propagate
*For any* election type, changing its active status should be reflected in queries for related forms and candidates
**Validates: Requirements 5.5**

### Visual Indicators Properties

Property 18: Critical incidents show red pulsing indicator
*For any* voting location with at least one critical incident, the map data should include a red pulsing indicator
**Validates: Requirements 6.1**

Property 19: Reported crimes show orange indicator
*For any* voting location with at least one reported crime, the map data should include an orange indicator
**Validates: Requirements 6.2**

Property 20: Pending forms show yellow indicator
*For any* voting location with pending forms (total_recibidos < total_esperados), the map data should include a yellow indicator
**Validates: Requirements 6.3**

Property 21: Fully reported locations show green indicator
*For any* voting location with all forms received (total_recibidos >= total_esperados) and no active incidents or crimes, the map data should include a green indicator
**Validates: Requirements 6.4**

Property 22: Indicator clicks show relevant details
*For any* indicator clicked, the system should display details specific to that indicator type (incidents, crimes, or forms)
**Validates: Requirements 6.5**

### Map Filters Properties

Property 23: Incidents filter shows only locations with incidents
*For any* set of voting locations, applying the "Solo con incidentes" filter should return only those with total_incidentes > 0
**Validates: Requirements 7.1**

Property 24: Crimes filter shows only locations with crimes
*For any* set of voting locations, applying the "Solo con delitos" filter should return only those with total_delitos > 0
**Validates: Requirements 7.2**

Property 25: Pending filter shows only locations with pending forms
*For any* set of voting locations, applying the "Pendientes de reporte" filter should return only those with formularios_pendientes > 0
**Validates: Requirements 7.3**

Property 26: Multiple filters use AND logic
*For any* combination of filters applied simultaneously, the system should return only voting locations that satisfy all active filters
**Validates: Requirements 7.5**

### System Configuration Properties

Property 27: System name changes propagate to all pages
*For any* system name configuration change, the new name should appear in the title of all pages on subsequent requests
**Validates: Requirements 8.2**

Property 28: System logo changes propagate to navbar
*For any* system logo configuration change, the new logo should appear in the navbar on subsequent requests
**Validates: Requirements 8.3**

Property 29: Timezone configuration applies to all dates
*For any* timezone configuration setting, all date/time values returned by the API should be formatted using that timezone
**Validates: Requirements 8.4**

Property 30: Configuration changes apply immediately
*For any* configuration change saved, subsequent requests should reflect the new value without requiring system restart
**Validates: Requirements 8.5**

### Map Search Properties

Property 31: Voting location code search centers map
*For any* valid voting location code entered in search, the map should center on that location's coordinates
**Validates: Requirements 9.1**

Property 32: Municipality search returns all locations
*For any* municipality name entered in search, the system should return all voting locations in that municipality
**Validates: Requirements 9.2**

Property 33: Table code search returns containing location
*For any* valid table code entered in search, the system should return the voting location that contains that table
**Validates: Requirements 9.3**

Property 34: Invalid search shows informative message
*For any* search query that returns no results, the system should display an informative message rather than an error
**Validates: Requirements 9.4**

Property 35: Found locations are highlighted
*For any* successful search result, the corresponding marker should be highlighted temporarily on the map
**Validates: Requirements 9.5**

### Export/Import Properties

Property 36: Party export includes all parties
*For any* set of political parties in the database, the export function should generate a JSON file containing all of them with complete data
**Validates: Requirements 10.1**

Property 37: Candidate export includes all candidates
*For any* set of candidates in the database, the export function should generate a JSON file containing all of them with complete data
**Validates: Requirements 10.2**

Property 38: Election type export includes all types
*For any* set of election types in the database, the export function should generate a JSON file containing all of them with complete data
**Validates: Requirements 10.3**

Property 39: Complete configuration export includes all settings
*For any* system configuration state, the complete export function should generate a file containing all configuration keys and values
**Validates: Requirements 10.4**

Property 40: Configuration import validates format
*For any* configuration file imported, the system should validate the JSON format and data types before applying changes
**Validates: Requirements 10.5**

## Error Handling

### Validation Errors

**Party Validation:**
- Duplicate nombre or sigla: Return 409 Conflict with descriptive message
- Invalid color format: Return 400 Bad Request with format requirements
- Missing required fields: Return 400 Bad Request with list of missing fields
- Logo file too large: Return 413 Payload Too Large with size limit
- Invalid logo format: Return 400 Bad Request with accepted formats

**Candidate Validation:**
- Non-existent partido_id: Return 404 Not Found with party not found message
- Non-existent tipo_eleccion_id: Return 404 Not Found with election type not found message
- Missing required fields: Return 400 Bad Request with list of missing fields
- Duplicate numero_lista for same tipo_eleccion: Return 409 Conflict

**Configuration Validation:**
- Invalid configuration key: Return 404 Not Found
- Invalid value type: Return 400 Bad Request with expected type
- Invalid JSON in import: Return 400 Bad Request with parsing error

### Referential Integrity Errors

**Deletion Constraints:**
- Delete party with candidates: Return 409 Conflict with message "Cannot delete party with associated candidates"
- Delete candidate with votes: Return 409 Conflict with message "Cannot delete candidate with registered votes"
- Delete election type with forms: Return 409 Conflict with message "Cannot delete election type with associated E-14 forms"

### Permission Errors

**Authorization:**
- Non-super-admin accessing configuration: Return 403 Forbidden
- Non-super-admin modifying parties: Return 403 Forbidden
- Non-super-admin modifying candidates: Return 403 Forbidden

### Map Errors

**Geolocation Errors:**
- Voting location without GPS: Log warning, exclude from map, don't return error
- Invalid GPS coordinates: Log error, exclude from map, don't return error
- Map service unavailable: Return 503 Service Unavailable with retry message

### File Upload Errors

**Upload Validation:**
- File too large: Return 413 Payload Too Large
- Invalid file type: Return 400 Bad Request
- Upload failed: Return 500 Internal Server Error with retry message
- Storage full: Return 507 Insufficient Storage

## Testing Strategy

### Unit Testing

**Backend Unit Tests:**
- Model validation tests for PartidoPolitico, Candidato, ConfiguracionSistema
- Service layer tests for CRUD operations
- Route handler tests with mocked services
- File upload validation tests
- Permission validation tests
- Filter logic tests
- Search functionality tests

**Frontend Unit Tests:**
- Component rendering tests
- Form validation tests
- API call mocking tests
- Tab navigation tests
- Filter UI tests
- Search UI tests

### Property-Based Testing

We will use **Hypothesis** (Python) for backend property-based testing.

**Configuration:**
- Minimum 100 iterations per property test
- Each property test must reference its design document property with format: `**Feature: mejoras-admin-mapas, Property {number}: {property_text}**`

**Property Test Coverage:**
- All 40 correctness properties must have corresponding property-based tests
- Tests should generate random valid and invalid inputs
- Tests should verify invariants hold across all generated inputs

**Key Property Tests:**
- Property 1: Generate random user roles, verify all geolocalized locations returned
- Property 8: Generate random parties with/without candidates, verify deletion logic
- Property 13: Generate random candidate data with valid/invalid party IDs, verify validation
- Property 26: Generate random filter combinations, verify AND logic
- Property 40: Generate random valid/invalid JSON configs, verify validation

### Integration Testing

**End-to-End Flows:**
- Create party → Create candidate → Verify association
- Upload party logo → Verify URL → Access logo file
- Apply multiple filters → Verify correct locations returned
- Export configuration → Import configuration → Verify data integrity
- Search voting location → Verify map centers → Verify marker highlights

**Database Integration:**
- Test transactions and rollbacks
- Test referential integrity constraints
- Test cascade behaviors
- Test index performance

### Manual Testing Checklist

**UI/UX Testing:**
- Tab navigation works smoothly
- Forms validate correctly
- File uploads show progress
- Maps load and display correctly
- Filters apply without page reload
- Search provides instant feedback
- Indicators are visually distinct

**Cross-Browser Testing:**
- Chrome, Firefox, Safari, Edge
- Mobile responsive design
- Touch interactions on mobile

## Performance Considerations

### Database Optimization

**Indexes:**
- Index on partidos_politicos.activo for filtering
- Index on candidatos.partido_id for joins
- Index on candidatos.tipo_eleccion_id for joins
- Index on configuracion_sistema.clave for lookups
- Composite index on (municipio, departamento) for location searches

**Query Optimization:**
- Use eager loading for party-candidate relationships
- Implement pagination for large lists (50 items per page)
- Cache configuration values in Redis (5 minute TTL)
- Use database views for complex map queries

### Frontend Optimization

**Map Performance:**
- Implement marker clustering for dense areas (>100 markers)
- Lazy load marker details on click
- Debounce search input (300ms)
- Cache map tiles in browser
- Use WebGL rendering for large datasets

**Asset Optimization:**
- Compress uploaded images (max 1MB, 1920px width)
- Generate thumbnails for logos (200x200px)
- Use CDN for static assets
- Implement lazy loading for images
- Minify and bundle JavaScript

### Caching Strategy

**Backend Caching:**
- Configuration values: 5 minutes
- Party list: 10 minutes
- Candidate list: 10 minutes
- Map data: 2 minutes
- Invalidate on updates

**Frontend Caching:**
- API responses: Use ETags
- Map tiles: Browser cache (7 days)
- Static assets: Browser cache (30 days)

## Security Considerations

### Authentication & Authorization

**Role-Based Access Control:**
- Only Super Admin can access configuration endpoints
- Only Super Admin can modify parties and candidates
- All users can view maps (filtered by jurisdiction)
- Implement middleware for role checking

### Input Validation

**Server-Side Validation:**
- Validate all inputs against expected types and formats
- Sanitize HTML in text fields to prevent XSS
- Validate file uploads (type, size, content)
- Use parameterized queries to prevent SQL injection
- Validate GPS coordinates are within valid ranges

### File Upload Security

**Upload Protection:**
- Whitelist allowed file types (image/jpeg, image/png, image/webp)
- Scan uploaded files for malware
- Generate unique filenames to prevent overwrites
- Store files outside web root
- Serve files through controlled endpoint with validation
- Implement rate limiting on uploads (10 per minute per user)

### API Security

**Request Protection:**
- Implement CSRF tokens for state-changing operations
- Use HTTPS for all communications
- Implement rate limiting (100 requests per minute per user)
- Log all configuration changes with user and timestamp
- Validate Content-Type headers

### Data Privacy

**Sensitive Data:**
- Don't log sensitive configuration values
- Implement audit trail for configuration changes
- Encrypt sensitive configuration values at rest
- Implement data retention policies

## Deployment Considerations

### Database Migrations

**Migration Steps:**
1. Create partidos_politicos table
2. Create candidatos table
3. Create configuracion_sistema table
4. Add indexes
5. Seed initial configuration values
6. Migrate existing data if applicable

### Configuration

**Environment Variables:**
```
UPLOAD_FOLDER=/var/app/uploads
MAX_UPLOAD_SIZE=5242880  # 5MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp
MAP_TILE_SERVER=https://tile.openstreetmap.org
REDIS_URL=redis://localhost:6379/0
```

### Monitoring

**Metrics to Track:**
- API response times (p50, p95, p99)
- Database query performance
- File upload success/failure rates
- Map load times
- Cache hit rates
- Error rates by endpoint

**Alerts:**
- API response time > 2 seconds
- Error rate > 5%
- Database connection pool exhausted
- Storage usage > 80%
- Redis connection failures

### Rollback Plan

**Rollback Steps:**
1. Revert application code to previous version
2. Rollback database migrations if necessary
3. Clear Redis cache
4. Verify system functionality
5. Monitor error logs

**Data Backup:**
- Daily database backups
- Backup uploaded files to S3/Azure
- Keep backups for 30 days
- Test restore procedures monthly
