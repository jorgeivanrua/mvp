# Design Document - Sistema de Personalización de Fondos

## Overview

El Sistema de Personalización de Fondos es un módulo del sistema electoral que permite al Super Admin personalizar la apariencia visual de la página de login. El sistema está implementado con una arquitectura de tres capas: modelos de datos (SQLAlchemy), API REST (Flask), y componentes de interfaz (HTML/JavaScript). Soporta tres tipos de fondos (gradientes, imágenes, colores sólidos) y proporciona fondos predefinidos para selección rápida.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Login Page (Public)                      │
│  - Carga fondo activo automáticamente                       │
│  - Endpoint público: GET /api/config-sistema/fondos/activo  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Super Admin Dashboard (Protected)               │
│  - Gestión de fondos                                        │
│  - Preview en tiempo real                                   │
│  - Subida de imágenes                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API REST Layer                            │
│  Blueprint: config_sistema_bp                               │
│  Prefix: /api/config-sistema                                │
│  - GET /fondos (público)                                    │
│  - GET /fondos/activo (público)                             │
│  - POST /fondos (protegido)                                 │
│  - PUT /fondos/:id/activar (protegido)                      │
│  - DELETE /fondos/:id (protegido)                           │
│  - POST /fondos/upload (protegido)                          │
│  - GET /fondos/predefinidos (protegido)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  - ConfiguracionSistema (modelo genérico)                   │
│  - FondoLogin (modelo específico)                           │
│  - PostgreSQL Database                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    File Storage                              │
│  - frontend/static/uploads/fondos/                          │
│  - Almacenamiento de imágenes subidas                       │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **File Upload**: Werkzeug secure_filename
- **Frontend**: HTML, JavaScript, Bootstrap
- **File Storage**: Local filesystem

## Components and Interfaces

### 1. Data Models

#### ConfiguracionSistema Model

```python
class ConfiguracionSistema(db.Model):
    """Configuración general del sistema"""
    __tablename__ = 'configuracion_sistema'
    
    id: Integer (Primary Key)
    clave: String(100) (Unique, Not Null)
    valor: Text (Nullable)
    tipo: String(50) (Not Null)  # text, image, color, json
    descripcion: String(255) (Nullable)
    created_at: DateTime (Default: utcnow)
    updated_at: DateTime (Default: utcnow, OnUpdate: utcnow)
    updated_by: Integer (Foreign Key: users.id)
    
    # Relationships
    actualizado_por: User
    
    # Methods
    to_dict() -> dict
    get_valor(clave, default=None) -> str (static)
    set_valor(clave, valor, tipo, descripcion, user_id) -> ConfiguracionSistema (static)
```

#### FondoLogin Model

```python
class FondoLogin(db.Model):
    """Fondos disponibles para la página de login"""
    __tablename__ = 'fondos_login'
    
    id: Integer (Primary Key)
    nombre: String(100) (Not Null)
    tipo: String(20) (Not Null)  # gradient, image, solid
    
    # Para gradientes
    color1: String(7) (Nullable)  # #FCD116
    color2: String(7) (Nullable)  # #003893
    color3: String(7) (Nullable)  # #CE1126
    direccion: String(20) (Default: '180deg')
    
    # Para imágenes
    imagen_url: String(500) (Nullable)
    imagen_posicion: String(50) (Default: 'center')
    imagen_tamano: String(50) (Default: 'cover')
    
    # Para colores sólidos
    color_solido: String(7) (Nullable)
    
    # Overlay opcional
    overlay_color: String(7) (Nullable)
    overlay_opacity: Float (Default: 0.1)
    
    activo: Boolean (Default: False)
    predeterminado: Boolean (Default: False)
    created_at: DateTime (Default: utcnow)
    created_by: Integer (Foreign Key: users.id)
    
    # Relationships
    creado_por: User
    
    # Methods
    to_dict() -> dict
    get_css() -> dict
    get_activo() -> FondoLogin (static)
```

### 2. API Endpoints

#### GET /api/config-sistema/fondos
- **Description**: Obtener todos los fondos disponibles
- **Authentication**: Public (no requiere autenticación)
- **Authorization**: N/A
- **Request**: None
- **Response**: 
  ```json
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "nombre": "Bandera de Colombia",
        "tipo": "gradient",
        "color1": "#FCD116",
        "color2": "#003893",
        "color3": "#CE1126",
        "direccion": "180deg",
        "activo": true,
        "created_at": "2025-11-25T10:00:00"
      }
    ]
  }
  ```

#### GET /api/config-sistema/fondos/activo
- **Description**: Obtener el fondo activo actual
- **Authentication**: Public (no requiere autenticación)
- **Authorization**: N/A
- **Request**: None
- **Response**: 
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "nombre": "Bandera de Colombia",
      "tipo": "gradient",
      "color1": "#FCD116",
      "color2": "#003893",
      "color3": "#CE1126",
      "direccion": "180deg"
    }
  }
  ```

#### POST /api/config-sistema/fondos
- **Description**: Crear un nuevo fondo
- **Authentication**: JWT Required
- **Authorization**: super_admin only
- **Request**: 
  ```json
  {
    "nombre": "Mi Gradiente",
    "tipo": "gradient",
    "color1": "#FF0000",
    "color2": "#00FF00",
    "direccion": "135deg",
    "overlay_color": "#FFFFFF",
    "overlay_opacity": 0.1
  }
  ```
- **Response**: 
  ```json
  {
    "success": true,
    "message": "Fondo creado exitosamente",
    "data": { /* fondo object */ }
  }
  ```

#### PUT /api/config-sistema/fondos/:id/activar
- **Description**: Activar un fondo (desactiva los demás)
- **Authentication**: JWT Required
- **Authorization**: super_admin only
- **Request**: None
- **Response**: 
  ```json
  {
    "success": true,
    "message": "Fondo activado exitosamente",
    "data": { /* fondo object */ }
  }
  ```

#### DELETE /api/config-sistema/fondos/:id
- **Description**: Eliminar un fondo
- **Authentication**: JWT Required
- **Authorization**: super_admin only
- **Request**: None
- **Response**: 
  ```json
  {
    "success": true,
    "message": "Fondo eliminado exitosamente"
  }
  ```

#### POST /api/config-sistema/fondos/upload
- **Description**: Subir imagen de fondo
- **Authentication**: JWT Required
- **Authorization**: super_admin only
- **Request**: multipart/form-data
  - file: Image file (png, jpg, jpeg, gif, webp)
  - nombre: String (optional)
  - imagen_posicion: String (optional, default: 'center')
  - imagen_tamano: String (optional, default: 'cover')
  - overlay_color: String (optional)
  - overlay_opacity: Float (optional, default: 0.1)
- **Response**: 
  ```json
  {
    "success": true,
    "message": "Imagen subida exitosamente",
    "data": { /* fondo object */ }
  }
  ```

#### GET /api/config-sistema/fondos/predefinidos
- **Description**: Obtener fondos predefinidos
- **Authentication**: JWT Required
- **Authorization**: super_admin only
- **Request**: None
- **Response**: 
  ```json
  {
    "success": true,
    "data": [
      {
        "nombre": "Bandera de Colombia",
        "tipo": "gradient",
        "color1": "#FCD116",
        "color2": "#003893",
        "color3": "#CE1126",
        "direccion": "180deg",
        "preview": "linear-gradient(...)"
      }
    ]
  }
  ```

### 3. Frontend Components

#### Background Management Modal
- **Location**: Super Admin Dashboard
- **Components**:
  - Grid de fondos existentes
  - Botón "Crear Nuevo Fondo"
  - Modal de creación/edición
  - Panel de preview en tiempo real
  - Selector de tipo de fondo (tabs)
  - Formulario de configuración
  - Botones de acción (Guardar, Cancelar, Eliminar)

#### Background Preview Panel
- **Purpose**: Mostrar vista previa en tiempo real
- **Features**:
  - Actualización instantánea al cambiar configuración
  - Muestra overlay si está configurado
  - Dimensiones similares a la página de login real

#### Background Grid
- **Purpose**: Mostrar todos los fondos disponibles
- **Features**:
  - Vista en cuadrícula con previews
  - Indicador de fondo activo
  - Botones de acción (Activar, Editar, Eliminar)
  - Información de cada fondo (nombre, tipo, fecha)

### 4. File Upload Handler

```python
UPLOAD_FOLDER = 'frontend/static/uploads/fondos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(file):
    # Validar tipo de archivo
    # Generar nombre único con UUID
    # Crear directorio si no existe
    # Guardar archivo
    # Retornar URL relativa
```

## Data Models

### Database Schema

```sql
-- Tabla de configuración general del sistema
CREATE TABLE configuracion_sistema (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(100) UNIQUE NOT NULL,
    valor TEXT,
    tipo VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER REFERENCES users(id)
);

-- Tabla de fondos de login
CREATE TABLE fondos_login (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('gradient', 'image', 'solid')),
    
    -- Campos para gradientes
    color1 VARCHAR(7),
    color2 VARCHAR(7),
    color3 VARCHAR(7),
    direccion VARCHAR(20) DEFAULT '180deg',
    
    -- Campos para imágenes
    imagen_url VARCHAR(500),
    imagen_posicion VARCHAR(50) DEFAULT 'center',
    imagen_tamano VARCHAR(50) DEFAULT 'cover',
    
    -- Campos para colores sólidos
    color_solido VARCHAR(7),
    
    -- Overlay opcional
    overlay_color VARCHAR(7),
    overlay_opacity FLOAT DEFAULT 0.1,
    
    activo BOOLEAN DEFAULT FALSE,
    predeterminado BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id)
);

-- Índices
CREATE INDEX idx_fondos_login_activo ON fondos_login(activo);
CREATE INDEX idx_fondos_login_tipo ON fondos_login(tipo);
```

### Data Relationships

```
User (1) ──────── (N) FondoLogin
     │                  (created_by)
     │
     └──────────── (N) ConfiguracionSistema
                       (updated_by)
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Single Active Background
*For any* point in time, at most one background should be marked as active in the database
**Validates: Requirements 7.1, 7.2**

### Property 2: Background Type Consistency
*For any* background of type 'gradient', the color1 field should be non-null; for type 'image', the imagen_url field should be non-null; for type 'solid', the color_solido field should be non-null
**Validates: Requirements 2.1, 3.1, 4.1**

### Property 3: File Upload Security
*For any* uploaded file, the file extension should be in the allowed list (png, jpg, jpeg, gif, webp)
**Validates: Requirements 3.1, 10.3**

### Property 4: Active Background Deletion Prevention
*For any* background marked as active, attempting to delete it should fail with an error
**Validates: Requirements 8.1, 8.2**

### Property 5: Default Background Fallback
*For any* login page load when no active background exists, the system should apply the default Bandera de Colombia gradient
**Validates: Requirements 7.3, 11.2**

### Property 6: Unique Filename Generation
*For any* two uploaded images, their generated filenames should be different (UUID-based)
**Validates: Requirements 12.2, 12.3**

### Property 7: Overlay Opacity Range
*For any* background with an overlay, the overlay_opacity value should be between 0.0 and 1.0 inclusive
**Validates: Requirements 9.2**

### Property 8: Authorization Enforcement
*For any* protected endpoint (POST, PUT, DELETE), requests without super_admin role should receive a 403 Forbidden response
**Validates: Requirements 10.1**

### Property 9: CSS Generation Correctness
*For any* gradient background with three colors, the generated CSS should distribute colors as: color1 (0-50%), color2 (50-75%), color3 (75-100%)
**Validates: Requirements 2.3**

### Property 10: Image File Cleanup
*For any* deleted image background, the associated image file should be removed from the filesystem
**Validates: Requirements 3.5, 8.3**

## Error Handling

### Error Categories

1. **Validation Errors** (400 Bad Request)
   - Invalid background type
   - Missing required fields
   - Invalid file format
   - Invalid color format

2. **Authorization Errors** (403 Forbidden)
   - Non-super-admin attempting protected operations
   - Insufficient permissions

3. **Not Found Errors** (404 Not Found)
   - Background ID does not exist
   - Image file not found

4. **Business Logic Errors** (400 Bad Request)
   - Attempting to delete active background
   - Duplicate background name

5. **Server Errors** (500 Internal Server Error)
   - Database connection failures
   - File system errors
   - Unexpected exceptions

### Error Response Format

```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

### Error Handling Strategy

- All database operations wrapped in try-except blocks
- Automatic rollback on database errors
- Graceful degradation for file system errors
- Detailed error messages for debugging
- User-friendly error messages for frontend

## Testing Strategy

### Unit Testing

Unit tests will verify specific examples and edge cases:

1. **Model Tests**
   - Test FondoLogin.to_dict() serialization
   - Test FondoLogin.get_css() for each background type
   - Test FondoLogin.get_activo() with and without active backgrounds
   - Test ConfiguracionSistema.get_valor() and set_valor()

2. **API Tests**
   - Test GET /fondos returns all backgrounds
   - Test GET /fondos/activo returns active background or default
   - Test POST /fondos creates background with valid data
   - Test POST /fondos rejects invalid data
   - Test PUT /fondos/:id/activar activates background
   - Test DELETE /fondos/:id deletes non-active background
   - Test DELETE /fondos/:id rejects active background deletion
   - Test POST /fondos/upload with valid image
   - Test POST /fondos/upload rejects invalid file types

3. **Authorization Tests**
   - Test super_admin can access all endpoints
   - Test non-super-admin receives 403 on protected endpoints
   - Test unauthenticated users can access public endpoints

4. **File Upload Tests**
   - Test allowed_file() with valid extensions
   - Test allowed_file() with invalid extensions
   - Test unique filename generation
   - Test directory creation

### Property-Based Testing

Property-based tests will use **Hypothesis** library for Python to verify universal properties across many randomly generated inputs:

1. **Property Test: Single Active Background**
   - Generate random list of backgrounds
   - Activate one background
   - Verify only one background has activo=True

2. **Property Test: Background Type Consistency**
   - Generate random backgrounds of each type
   - Verify required fields are non-null for each type

3. **Property Test: File Upload Security**
   - Generate random filenames with various extensions
   - Verify only allowed extensions pass validation

4. **Property Test: Unique Filename Generation**
   - Generate multiple UUID-based filenames
   - Verify all filenames are unique

5. **Property Test: Overlay Opacity Range**
   - Generate random opacity values
   - Verify all values are between 0.0 and 1.0

6. **Property Test: CSS Generation**
   - Generate random gradient backgrounds
   - Verify CSS output matches expected format

### Integration Testing

Integration tests will verify end-to-end workflows:

1. Create gradient background → Activate → Verify on login page
2. Upload image → Activate → Verify image loads on login page
3. Create multiple backgrounds → Activate one → Verify others deactivated
4. Delete non-active background → Verify removed from database and filesystem
5. Attempt to delete active background → Verify rejection

### Test Configuration

- **Framework**: pytest
- **Property Testing**: Hypothesis
- **Coverage Target**: 90%+
- **Test Database**: Separate test database
- **File Storage**: Temporary directory for test uploads

## Security Considerations

### Authentication & Authorization

- All management endpoints require JWT authentication
- Only super_admin role can manage backgrounds
- Public endpoints for login page (GET /fondos, GET /fondos/activo)
- Role validation using @role_required decorator

### File Upload Security

- Whitelist of allowed file extensions
- Filename sanitization using secure_filename
- UUID-based filenames to prevent path traversal
- File size limits (configured in Flask)
- Storage in dedicated directory outside application code

### Input Validation

- Hexadecimal color format validation
- Background type validation (gradient, image, solid)
- Opacity range validation (0.0 - 1.0)
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention via JSON serialization

### Data Integrity

- Database constraints (CHECK, NOT NULL, UNIQUE)
- Foreign key relationships
- Transaction rollback on errors
- Atomic operations for background activation

## Performance Considerations

### Database Optimization

- Index on fondos_login.activo for fast active background lookup
- Index on fondos_login.tipo for filtering by type
- Efficient query: FondoLogin.query.filter_by(activo=True).first()

### Caching Strategy

- Active background can be cached (rarely changes)
- Cache invalidation on background activation
- Static file caching for uploaded images

### File Storage

- Images served as static files (fast)
- No database queries for image serving
- CDN-ready architecture

## Deployment Considerations

### File Storage

- Ensure frontend/static/uploads/fondos directory exists
- Configure proper permissions (read/write for application)
- Consider cloud storage (S3, GCS) for production
- Backup strategy for uploaded images

### Database Migrations

- Create configuracion_sistema table
- Create fondos_login table
- Create indexes
- Seed default Bandera de Colombia background

### Environment Configuration

- UPLOAD_FOLDER path configuration
- MAX_CONTENT_LENGTH for file uploads
- Allowed file extensions configuration

## Future Enhancements

1. **Video Backgrounds**: Support for video backgrounds
2. **Animated Gradients**: CSS animations for gradients
3. **Background Scheduling**: Schedule background changes by date/time
4. **A/B Testing**: Test multiple backgrounds with users
5. **Analytics**: Track which backgrounds perform best
6. **Themes**: Complete theme system beyond just backgrounds
7. **Cloud Storage**: Integration with S3/GCS for scalability
8. **Image Optimization**: Automatic image compression and resizing
9. **Background Library**: Curated library of professional backgrounds
10. **User Preferences**: Allow users to select their preferred background

