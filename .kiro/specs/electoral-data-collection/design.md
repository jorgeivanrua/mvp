# Documento de Diseño Técnico - Sistema Electoral E-14/E-24

## Introducción

Este documento describe el diseño técnico del Sistema Electoral E-14/E-24, una aplicación web para la recolección, validación y consolidación de datos electorales. El sistema utiliza autenticación basada en ubicación jerárquica, permitiendo a testigos electorales capturar formularios E-14 desde cualquier mesa dentro de su puesto asignado, y a coordinadores validar y supervisar el proceso electoral en tiempo real.

## Arquitectura General

### Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Dashboard  │  │   Forms E14  │  │    Admin     │      │
│  │   por Rol    │  │   Capture    │  │    Panel     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/JSON + JWT
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask API)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    API Routes                         │   │
│  │  /auth  /e14  /coordination  /admin  /locations     │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Services Layer                       │   │
│  │  AuthService  E14Service  ValidationService          │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Models (ORM)                        │   │
│  │  User  Location  FormE14  FormE14History            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                DATABASE (SQLite/PostgreSQL)                  │
│  users  locations  forms_e14  forms_e14_history             │
│  political_parties  notifications  audit_logs                │
└─────────────────────────────────────────────────────────────┘
```

### Principios de Diseño

1. **Separación de Responsabilidades**: Backend maneja lógica de negocio, frontend maneja presentación
2. **API RESTful**: Comunicación mediante endpoints HTTP con JSON
3. **Autenticación Basada en Ubicación**: Login sin email, usando jerarquía geográfica
4. **Validación en Múltiples Capas**: Frontend (UX), Backend (seguridad), Base de Datos (integridad)
5. **Responsive Design**: Interfaz adaptable a móvil, tablet y desktop
6. **Offline-First**: Capacidad de trabajar sin conexión y sincronizar después

## Modelo de Datos

### Diagrama de Entidad-Relación

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│    User      │         │   Location   │         │   FormE14    │
├──────────────┤         ├──────────────┤         ├──────────────┤
│ id (PK)      │────┐    │ id (PK)      │    ┌────│ id (PK)      │
│ nombre       │    │    │ depto_codigo │    │    │ mesa_id (FK) │
│ password_hash│    └───▶│ muni_codigo  │◀───┘    │ testigo_id   │
│ rol          │         │ zona_codigo  │         │ total_votos  │
│ ubicacion_id │         │ puesto_codigo│         │ estado       │
│ activo       │         │ mesa_codigo  │         │ foto_url     │
│ intentos_fal │         │ tipo         │         │ created_at   │
│ bloqueado    │         │ nombre       │         └──────────────┘
└──────────────┘         │ votantes     │                │
                         └──────────────┘                │
                                                          ▼
                                                  ┌──────────────┐
                                                  │ FormE14      │
                                                  │ History      │
                                                  ├──────────────┤
                                                  │ id (PK)      │
                                                  │ form_id (FK) │
                                                  │ usuario_id   │
                                                  │ accion       │
                                                  │ estado_ant   │
                                                  │ estado_nuevo │
                                                  │ justificacion│
                                                  │ timestamp    │
                                                  └──────────────┘
```



### Esquemas de Tablas

#### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL CHECK(rol IN ('super_admin', 'admin_departamental', 
        'admin_municipal', 'coordinador_departamental', 'coordinador_municipal', 
        'coordinador_puesto', 'testigo_electoral', 'auditor_electoral')),
    ubicacion_id INTEGER,
    activo BOOLEAN DEFAULT TRUE,
    ultimo_acceso DATETIME,
    intentos_fallidos INTEGER DEFAULT 0,
    bloqueado_hasta DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ubicacion_id) REFERENCES locations(id)
);

CREATE INDEX idx_users_rol ON users(rol);
CREATE INDEX idx_users_ubicacion ON users(ubicacion_id);
CREATE INDEX idx_users_activo ON users(activo);
```

#### locations
```sql
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    departamento_codigo VARCHAR(10) NOT NULL,
    municipio_codigo VARCHAR(10),
    zona_codigo VARCHAR(10),
    puesto_codigo VARCHAR(10),
    mesa_codigo VARCHAR(10),
    nombre_completo VARCHAR(200) NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK(tipo IN ('departamento', 'municipio', 'zona', 'puesto', 'mesa')),
    total_votantes_registrados INTEGER DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    latitud FLOAT,
    longitud FLOAT,
    parent_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES locations(id)
);

CREATE INDEX idx_locations_tipo ON locations(tipo);
CREATE INDEX idx_locations_depto ON locations(departamento_codigo);
CREATE INDEX idx_locations_muni ON locations(municipio_codigo);
CREATE INDEX idx_locations_parent ON locations(parent_id);
CREATE UNIQUE INDEX idx_locations_codes ON locations(
    departamento_codigo, municipio_codigo, zona_codigo, puesto_codigo, mesa_codigo
);
```

#### forms_e14
```sql
CREATE TABLE forms_e14 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa_id INTEGER NOT NULL,
    testigo_id INTEGER NOT NULL,
    total_votantes INTEGER NOT NULL,
    total_votos INTEGER NOT NULL,
    votos_partidos JSON NOT NULL,  -- {"partido_1": 50, "partido_2": 30, ...}
    votos_candidatos JSON,  -- {"candidato_1": 25, ...}
    votos_nulos INTEGER DEFAULT 0,
    votos_no_marcados INTEGER DEFAULT 0,
    foto_url VARCHAR(500),
    estado VARCHAR(50) NOT NULL DEFAULT 'borrador' CHECK(estado IN 
        ('borrador', 'enviado', 'en_revision', 'aprobado', 'rechazado')),
    observaciones TEXT,
    aprobado_por INTEGER,
    aprobado_en DATETIME,
    rechazado_por INTEGER,
    rechazado_en DATETIME,
    justificacion_rechazo TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mesa_id) REFERENCES locations(id),
    FOREIGN KEY (testigo_id) REFERENCES users(id),
    FOREIGN KEY (aprobado_por) REFERENCES users(id),
    FOREIGN KEY (rechazado_por) REFERENCES users(id)
);

CREATE INDEX idx_forms_e14_mesa ON forms_e14(mesa_id);
CREATE INDEX idx_forms_e14_testigo ON forms_e14(testigo_id);
CREATE INDEX idx_forms_e14_estado ON forms_e14(estado);
CREATE INDEX idx_forms_e14_created ON forms_e14(created_at);
CREATE UNIQUE INDEX idx_forms_e14_mesa_aprobado ON forms_e14(mesa_id) 
    WHERE estado = 'aprobado';
```

#### forms_e14_history
```sql
CREATE TABLE forms_e14_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    accion VARCHAR(50) NOT NULL CHECK(accion IN 
        ('creado', 'modificado', 'enviado', 'aprobado', 'rechazado', 'reabierto')),
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50),
    cambios JSON,  -- {"campo": {"anterior": "valor1", "nuevo": "valor2"}}
    justificacion TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (form_id) REFERENCES forms_e14(id),
    FOREIGN KEY (usuario_id) REFERENCES users(id)
);

CREATE INDEX idx_history_form ON forms_e14_history(form_id);
CREATE INDEX idx_history_usuario ON forms_e14_history(usuario_id);
CREATE INDEX idx_history_timestamp ON forms_e14_history(timestamp);
```

#### political_parties
```sql
CREATE TABLE political_parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    color VARCHAR(7),  -- Código hexadecimal #RRGGBB
    logo_url VARCHAR(500),
    orden INTEGER DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_parties_activo ON political_parties(activo);
CREATE INDEX idx_parties_orden ON political_parties(orden);
```

#### notifications
```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK(tipo IN 
        ('form_aprobado', 'form_rechazado', 'alerta_discrepancia', 'mensaje_sistema')),
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    form_id INTEGER,
    leida BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES users(id),
    FOREIGN KEY (form_id) REFERENCES forms_e14(id)
);

CREATE INDEX idx_notifications_usuario ON notifications(usuario_id);
CREATE INDEX idx_notifications_leida ON notifications(leida);
CREATE INDEX idx_notifications_created ON notifications(created_at);
```

#### audit_logs
```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    accion VARCHAR(100) NOT NULL,
    entidad VARCHAR(50) NOT NULL,  -- 'user', 'form_e14', 'location', etc.
    entidad_id INTEGER,
    detalles JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES users(id)
);

CREATE INDEX idx_audit_usuario ON audit_logs(usuario_id);
CREATE INDEX idx_audit_entidad ON audit_logs(entidad, entidad_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
```

## Componentes y Interfaces

### Backend - Flask API

#### Estructura de Directorios

```
backend/
├── app.py                      # Aplicación principal Flask
├── config.py                   # Configuración
├── models/                     # Modelos de datos
│   ├── __init__.py
│   ├── user.py
│   ├── location.py
│   ├── form_e14.py
│   ├── political_party.py
│   └── notification.py
├── routes/                     # Endpoints API
│   ├── __init__.py
│   ├── auth.py                # Autenticación
│   ├── e14.py                 # Formularios E-14
│   ├── locations.py           # Ubicaciones
│   ├── coordination.py        # Coordinación
│   ├── admin.py               # Administración
│   └── notifications.py       # Notificaciones
├── services/                   # Lógica de negocio
│   ├── __init__.py
│   ├── auth_service.py
│   ├── e14_service.py
│   ├── validation_service.py
│   ├── notification_service.py
│   └── report_service.py
├── utils/                      # Utilidades
│   ├── __init__.py
│   ├── validators.py
│   ├── sanitizers.py
│   ├── decorators.py
│   └── helpers.py
└── tests/                      # Tests
    ├── test_auth.py
    ├── test_e14.py
    └── test_validation.py
```

#### Servicios Principales

**AuthService** - Gestión de autenticación
```python
class AuthService:
    @staticmethod
    def authenticate_location_based(rol, ubicacion_data, password):
        """
        Autentica usuario basado en rol, ubicación jerárquica y contraseña
        
        Args:
            rol: Rol del usuario
            ubicacion_data: Dict con departamento, municipio, zona, puesto según rol
            password: Contraseña
            
        Returns:
            tuple: (user, access_token, refresh_token) o (None, None, None)
        """
        # Construir identificador de ubicación
        location = Location.find_by_hierarchy(ubicacion_data)
        if not location:
            return None, None, None
            
        # Buscar usuario por rol y ubicación
        user = User.query.filter_by(
            rol=rol,
            ubicacion_id=location.id,
            activo=True
        ).first()
        
        if not user:
            return None, None, None
            
        # Verificar si está bloqueado
        if user.bloqueado_hasta and user.bloqueado_hasta > datetime.now():
            raise AccountBlockedException("Cuenta bloqueada temporalmente")
            
        # Verificar contraseña
        if not user.check_password(password):
            user.intentos_fallidos += 1
            if user.intentos_fallidos >= 5:
                user.bloqueado_hasta = datetime.now() + timedelta(minutes=30)
            db.session.commit()
            return None, None, None
            
        # Reset intentos fallidos
        user.intentos_fallidos = 0
        user.ultimo_acceso = datetime.now()
        db.session.commit()
        
        # Generar tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return user, access_token, refresh_token
```

**E14Service** - Gestión de formularios E-14
```python
class E14Service:
    @staticmethod
    def create_form(testigo_id, mesa_id, form_data):
        """
        Crea un nuevo formulario E-14
        
        Args:
            testigo_id: ID del testigo
            mesa_id: ID de la mesa
            form_data: Datos del formulario
            
        Returns:
            FormE14: Formulario creado
        """
        # Validar que el testigo tenga acceso a la mesa
        testigo = User.query.get(testigo_id)
        mesa = Location.query.get(mesa_id)
        
        if not E14Service.can_access_mesa(testigo, mesa):
            raise PermissionDeniedException("No tiene acceso a esta mesa")
            
        # Validar datos
        errors = ValidationService.validate_e14_data(form_data, mesa)
        if errors:
            raise ValidationException(errors)
            
        # Crear formulario
        form = FormE14(
            mesa_id=mesa_id,
            testigo_id=testigo_id,
            total_votantes=form_data['total_votantes'],
            total_votos=form_data['total_votos'],
            votos_partidos=form_data['votos_partidos'],
            votos_nulos=form_data['votos_nulos'],
            votos_no_marcados=form_data['votos_no_marcados'],
            foto_url=form_data.get('foto_url'),
            estado='borrador'
        )
        
        db.session.add(form)
        db.session.commit()
        
        # Registrar en historial
        E14Service.add_history(form.id, testigo_id, 'creado', None, 'borrador')
        
        return form
    
    @staticmethod
    def can_access_mesa(user, mesa):
        """Verifica si un usuario puede acceder a una mesa"""
        if user.rol == 'super_admin':
            return True
            
        if user.rol == 'testigo_electoral':
            # Testigo puede acceder a cualquier mesa de su puesto
            return mesa.get_puesto().id == user.ubicacion.get_puesto().id
            
        if user.rol == 'coordinador_puesto':
            return mesa.get_puesto().id == user.ubicacion_id
            
        if user.rol == 'coordinador_municipal':
            return mesa.get_municipio().id == user.ubicacion_id
            
        if user.rol == 'coordinador_departamental':
            return mesa.get_departamento().id == user.ubicacion_id
            
        return False
```

**ValidationService** - Validaciones de negocio
```python
class ValidationService:
    @staticmethod
    def validate_e14_data(form_data, mesa):
        """
        Valida datos de formulario E-14
        
        Returns:
            list: Lista de errores (vacía si es válido)
        """
        errors = []
        
        total_votos = form_data['total_votos']
        total_votantes = form_data['total_votantes']
        votos_partidos = form_data['votos_partidos']
        votos_nulos = form_data['votos_nulos']
        votos_no_marcados = form_data['votos_no_marcados']
        
        # Validar que total votos no exceda votantes registrados
        if total_votos > mesa.total_votantes_registrados:
            errors.append(
                f"Total de votos ({total_votos}) excede votantes registrados "
                f"({mesa.total_votantes_registrados})"
            )
            
        # Validar que total votantes no exceda votantes registrados
        if total_votantes > mesa.total_votantes_registrados:
            errors.append(
                f"Total de votantes ({total_votantes}) excede votantes registrados "
                f"({mesa.total_votantes_registrados})"
            )
            
        # Validar suma de votos
        suma_votos_partidos = sum(votos_partidos.values())
        suma_total = suma_votos_partidos + votos_nulos + votos_no_marcados
        
        if suma_total != total_votos:
            errors.append(
                f"La suma de votos ({suma_total}) no coincide con el total "
                f"de votos ({total_votos})"
            )
            
        # Validar que no haya valores negativos
        if any(v < 0 for v in votos_partidos.values()):
            errors.append("Los votos por partido no pueden ser negativos")
            
        if votos_nulos < 0 or votos_no_marcados < 0:
            errors.append("Los votos nulos y no marcados no pueden ser negativos")
            
        return errors
```



### API Endpoints

#### Autenticación

```
POST /api/auth/login
Body: {
    "rol": "testigo_electoral",
    "departamento": "Caquetá",
    "municipio_id": 123,
    "zona_id": 456,
    "puesto_id": 789,
    "password": "contraseña123"
}
Response: {
    "success": true,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {
            "id": 1,
            "nombre": "Juan Pérez",
            "rol": "testigo_electoral",
            "ubicacion": {...}
        }
    }
}

POST /api/auth/logout
Headers: Authorization: Bearer <token>
Response: {
    "success": true,
    "message": "Sesión cerrada exitosamente"
}

POST /api/auth/change-password
Headers: Authorization: Bearer <token>
Body: {
    "current_password": "antigua",
    "new_password": "nueva123"
}
Response: {
    "success": true,
    "message": "Contraseña actualizada"
}

GET /api/auth/profile
Headers: Authorization: Bearer <token>
Response: {
    "success": true,
    "data": {
        "user": {...},
        "accessible_locations": [...]
    }
}
```

#### Ubicaciones

```
GET /api/locations/departamentos
Response: {
    "success": true,
    "data": [
        {"id": 1, "nombre": "Caquetá", "codigo": "18"},
        ...
    ]
}

GET /api/locations/municipios?departamento_id=1
Response: {
    "success": true,
    "data": [
        {"id": 10, "nombre": "Florencia", "codigo": "001"},
        ...
    ]
}

GET /api/locations/zonas?municipio_id=10
Response: {
    "success": true,
    "data": [
        {"id": 100, "nombre": "Zona 1", "codigo": "01"},
        ...
    ]
}

GET /api/locations/puestos?zona_id=100
Response: {
    "success": true,
    "data": [
        {"id": 1000, "nombre": "Escuela Central", "codigo": "001"},
        ...
    ]
}

GET /api/locations/mesas?puesto_id=1000
Response: {
    "success": true,
    "data": [
        {
            "id": 10000,
            "numero": "001",
            "total_votantes_registrados": 350
        },
        ...
    ]
}
```

#### Formularios E-14

```
POST /api/e14/forms
Headers: Authorization: Bearer <token>
Body: {
    "mesa_id": 10000,
    "total_votantes": 300,
    "total_votos": 280,
    "votos_partidos": {
        "partido_1": 120,
        "partido_2": 100,
        "partido_3": 50
    },
    "votos_nulos": 5,
    "votos_no_marcados": 5,
    "observaciones": "Sin novedad"
}
Response: {
    "success": true,
    "data": {
        "form": {...},
        "message": "Formulario creado exitosamente"
    }
}

GET /api/e14/forms?estado=enviado&page=1&per_page=20
Headers: Authorization: Bearer <token>
Response: {
    "success": true,
    "data": [...],
    "page": 1,
    "per_page": 20,
    "total": 45
}

GET /api/e14/forms/:id
Headers: Authorization: Bearer <token>
Response: {
    "success": true,
    "data": {
        "form": {...},
        "history": [...]
    }
}

POST /api/e14/forms/:id/submit
Headers: Authorization: Bearer <token>
Response: {
    "success": true,
    "data": {
        "form": {...},
        "message": "Formulario enviado para revisión"
    }
}

POST /api/e14/forms/:id/approve
Headers: Authorization: Bearer <coord_token>
Body: {
    "observaciones": "Datos correctos, aprobado"
}
Response: {
    "success": true,
    "data": {
        "form": {...},
        "message": "Formulario aprobado"
    }
}

POST /api/e14/forms/:id/reject
Headers: Authorization: Bearer <coord_token>
Body: {
    "justificacion": "Suma de votos no coincide con total"
}
Response: {
    "success": true,
    "data": {
        "form": {...},
        "message": "Formulario rechazado"
    }
}

POST /api/e14/forms/:id/upload-photo
Headers: Authorization: Bearer <token>
Content-Type: multipart/form-data
Body: FormData with file
Response: {
    "success": true,
    "data": {
        "foto_url": "/uploads/e14/2024/11/uuid-filename.jpg"
    }
}
```

#### Dashboards

```
GET /api/coordination/dashboard
Headers: Authorization: Bearer <coord_token>
Response: {
    "success": true,
    "data": {
        "pendientes": 15,
        "aprobados_hoy": 45,
        "rechazados_hoy": 3,
        "forms_pendientes": [...],
        "estadisticas": {
            "total_mesas": 50,
            "mesas_reportadas": 48,
            "porcentaje_avance": 96
        }
    }
}

GET /api/admin/stats
Headers: Authorization: Bearer <admin_token>
Response: {
    "success": true,
    "data": {
        "total_usuarios": 150,
        "usuarios_por_rol": {...},
        "total_formularios": 500,
        "formularios_por_estado": {...},
        "actividad_reciente": [...],
        "mesas_con_formulario": 480,
        "total_mesas": 500,
        "porcentaje_cobertura": 96
    }
}
```

### Frontend - Arquitectura

#### Estructura de Archivos

```
frontend/
├── templates/                  # Plantillas HTML
│   ├── base.html              # Template base
│   ├── auth/
│   │   └── login.html         # Login con ubicación
│   ├── testigo/
│   │   └── dashboard.html     # Dashboard testigo
│   ├── coordinador/
│   │   ├── puesto_dashboard.html
│   │   ├── municipal_dashboard.html
│   │   └── departamental_dashboard.html
│   ├── auditor/
│   │   └── dashboard.html
│   └── admin/
│       └── dashboard.html
├── static/
│   ├── js/
│   │   ├── api-client.js      # Cliente API
│   │   ├── utils.js           # Utilidades
│   │   ├── form-handler.js    # Manejo de formularios
│   │   ├── location-map.js    # Mapas interactivos
│   │   ├── testigo.js         # Lógica testigo
│   │   ├── coordinador.js     # Lógica coordinador
│   │   └── admin.js           # Lógica admin
│   ├── css/
│   │   ├── main.css           # Estilos principales
│   │   ├── dashboard.css      # Estilos dashboards
│   │   ├── forms.css          # Estilos formularios
│   │   └── responsive.css     # Responsive
│   └── img/
│       └── logos/
└── uploads/                    # Archivos subidos
    └── e14/
```

#### Componentes JavaScript

**APIClient** - Cliente para comunicación con API
```javascript
class APIClient {
    static baseURL = '/api';
    
    static getAuthHeaders() {
        const token = localStorage.getItem('access_token');
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
    
    static async get(endpoint, params = {}) {
        const url = new URL(`${window.location.origin}${this.baseURL}${endpoint}`);
        Object.keys(params).forEach(key => 
            url.searchParams.append(key, params[key])
        );
        
        const response = await fetch(url, {
            method: 'GET',
            headers: this.getAuthHeaders()
        });
        
        return this.handleResponse(response);
    }
    
    static async post(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        return this.handleResponse(response);
    }
    
    static async put(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'PUT',
            headers: this.getAuthHeaders(),
            body: JSON.stringify(data)
        });
        
        return this.handleResponse(response);
    }
    
    static async delete(endpoint) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'DELETE',
            headers: this.getAuthHeaders()
        });
        
        return this.handleResponse(response);
    }
    
    static async uploadFile(endpoint, formData) {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
                // No incluir Content-Type para multipart/form-data
            },
            body: formData
        });
        
        return this.handleResponse(response);
    }
    
    static async handleResponse(response) {
        if (response.status === 401) {
            // Token expirado, redirigir a login
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return;
        }
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Error en la petición');
        }
        
        return data;
    }
}
```

**Utils** - Utilidades generales
```javascript
class Utils {
    static showAlert(message, type = 'info', duration = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
        alertDiv.style.zIndex = '9999';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, duration);
    }
    
    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-CO', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    static formatNumber(number) {
        return new Intl.NumberFormat('es-CO').format(number);
    }
    
    static formatPercentage(value, total) {
        if (total === 0) return '0%';
        return ((value / total) * 100).toFixed(1) + '%';
    }
    
    static sanitizeInput(input) {
        const div = document.createElement('div');
        div.textContent = input;
        return div.innerHTML;
    }
    
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}
```

**FormHandler** - Manejo de formularios
```javascript
class FormHandler {
    static setupImagePreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);
        
        if (!input || !preview) return;
        
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tamaño (5MB máximo)
                if (file.size > 5 * 1024 * 1024) {
                    Utils.showAlert('El archivo no puede exceder 5MB', 'danger');
                    input.value = '';
                    return;
                }
                
                // Validar tipo
                if (!file.type.match('image.*')) {
                    Utils.showAlert('Solo se permiten archivos de imagen', 'danger');
                    input.value = '';
                    return;
                }
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.innerHTML = `
                        <img src="${e.target.result}" class="img-fluid rounded">
                    `;
                };
                reader.readAsDataURL(file);
            }
        });
    }
    
    static validateVoteTotals(formData) {
        const errors = [];
        
        const totalVotantes = parseInt(formData.total_votantes) || 0;
        const totalVotos = parseInt(formData.total_votos) || 0;
        const votosNulos = parseInt(formData.votos_nulos) || 0;
        const votosNoMarcados = parseInt(formData.votos_no_marcados) || 0;
        
        // Validar que total votos no exceda votantes
        if (totalVotos > totalVotantes) {
            errors.push('El total de votos no puede exceder el total de votantes');
        }
        
        // Calcular suma de votos por partidos
        let votosPartidos = 0;
        if (formData.votos_partidos) {
            votosPartidos = Object.values(formData.votos_partidos)
                .reduce((sum, v) => sum + (parseInt(v) || 0), 0);
        }
        
        // Validar suma total
        const sumaTotal = votosPartidos + votosNulos + votosNoMarcados;
        
        if (sumaTotal !== totalVotos) {
            errors.push(
                `La suma de votos (${sumaTotal}) no coincide con el total (${totalVotos})`
            );
        }
        
        return errors;
    }
    
    static showValidationErrors(errors, containerId = 'validation-errors') {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        if (errors.length === 0) {
            container.innerHTML = '';
            container.style.display = 'none';
            return;
        }
        
        container.style.display = 'block';
        container.innerHTML = errors.map(error => 
            `<div class="alert alert-danger alert-sm">${error}</div>`
        ).join('');
    }
    
    static setupRealTimeValidation(formId) {
        const form = document.getElementById(formId);
        if (!form) return;
        
        const inputs = form.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('input', Utils.debounce(() => {
                const formData = new FormData(form);
                const data = Object.fromEntries(formData);
                const errors = FormHandler.validateVoteTotals(data);
                FormHandler.showValidationErrors(errors);
            }, 500));
        });
    }
}
```

## Manejo de Errores

### Códigos de Estado HTTP

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Datos inválidos o faltantes |
| 401 | Unauthorized | No autenticado o token inválido |
| 403 | Forbidden | Sin permisos para el recurso |
| 404 | Not Found | Recurso no encontrado |
| 409 | Conflict | Conflicto (ej: formulario duplicado) |
| 422 | Unprocessable Entity | Validación de negocio fallida |
| 500 | Internal Server Error | Error del servidor |

### Formato de Respuestas de Error

```json
{
    "success": false,
    "error": "Mensaje de error general",
    "errors": {
        "campo1": ["Error específico del campo"],
        "campo2": ["Otro error"]
    },
    "code": "ERROR_CODE"
}
```

### Manejo de Errores en Frontend

```javascript
try {
    const response = await APIClient.post('/e14/forms', formData);
    Utils.showAlert('Formulario creado exitosamente', 'success');
} catch (error) {
    if (error.message.includes('suma de votos')) {
        Utils.showAlert(error.message, 'warning');
    } else {
        Utils.showAlert('Error al crear formulario: ' + error.message, 'danger');
    }
}
```

## Seguridad

### Autenticación JWT

```python
# Configuración
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
JWT_TOKEN_LOCATION = ['headers']
JWT_HEADER_NAME = 'Authorization'
JWT_HEADER_TYPE = 'Bearer'
```

### Control de Acceso

```python
# Decoradores
@token_required
def protected_route():
    """Requiere token JWT válido"""
    pass

@role_required('coordinador_puesto')
def coordinator_route():
    """Requiere rol específico"""
    pass

@location_access_required
def location_route(location_id):
    """Requiere acceso a ubicación específica"""
    pass
```

### Validación y Sanitización

```python
# Sanitización de entrada
from utils.sanitizers import DataSanitizer

data = DataSanitizer.sanitize_user_input(request.json)

# Validación
from utils.validators import ElectoralValidators

errors = ElectoralValidators.validate_e14_data(data)
if errors:
    return jsonify({'success': False, 'errors': errors}), 422
```

### Protección contra Ataques

1. **SQL Injection**: Uso de ORM (SQLAlchemy) con parámetros preparados
2. **XSS**: Sanitización de entrada, escape de salida
3. **CSRF**: Tokens CSRF en formularios
4. **Brute Force**: Bloqueo después de 5 intentos fallidos
5. **Rate Limiting**: Límite de peticiones por IP



## Testing Strategy

### Niveles de Testing

#### 1. Tests Unitarios
```python
# tests/test_validation_service.py
def test_validate_e14_suma_correcta():
    form_data = {
        'total_votos': 100,
        'votos_partidos': {'p1': 50, 'p2': 40},
        'votos_nulos': 5,
        'votos_no_marcados': 5
    }
    mesa = Mock(total_votantes_registrados=150)
    
    errors = ValidationService.validate_e14_data(form_data, mesa)
    assert len(errors) == 0

def test_validate_e14_suma_incorrecta():
    form_data = {
        'total_votos': 100,
        'votos_partidos': {'p1': 50, 'p2': 40},
        'votos_nulos': 5,
        'votos_no_marcados': 10  # Suma = 105, no 100
    }
    mesa = Mock(total_votantes_registrados=150)
    
    errors = ValidationService.validate_e14_data(form_data, mesa)
    assert len(errors) > 0
    assert 'no coincide' in errors[0]
```

#### 2. Tests de Integración
```python
# tests/test_e14_workflow.py
def test_flujo_completo_e14(client, testigo_token, coordinador_token):
    # 1. Testigo crea formulario
    response = client.post('/api/e14/forms',
        headers={'Authorization': f'Bearer {testigo_token}'},
        json={...}
    )
    assert response.status_code == 201
    form_id = response.json['data']['form']['id']
    
    # 2. Testigo envía formulario
    response = client.post(f'/api/e14/forms/{form_id}/submit',
        headers={'Authorization': f'Bearer {testigo_token}'}
    )
    assert response.status_code == 200
    
    # 3. Coordinador aprueba
    response = client.post(f'/api/e14/forms/{form_id}/approve',
        headers={'Authorization': f'Bearer {coordinador_token}'},
        json={'observaciones': 'Aprobado'}
    )
    assert response.status_code == 200
    assert response.json['data']['form']['estado'] == 'aprobado'
```

#### 3. Tests End-to-End
```javascript
// tests/e2e/testigo_workflow.spec.js
describe('Flujo Testigo Electoral', () => {
    it('debe permitir crear y enviar formulario E-14', async () => {
        // Login
        await page.goto('/login');
        await page.select('#rol', 'testigo_electoral');
        await page.select('#departamento', 'Caquetá');
        // ... seleccionar ubicación
        await page.type('#password', 'test123');
        await page.click('button[type="submit"]');
        
        // Esperar dashboard
        await page.waitForSelector('#testigo-dashboard');
        
        // Crear formulario
        await page.click('#btn-nuevo-formulario');
        await page.waitForSelector('#formModal');
        
        // Llenar datos
        await page.type('#total_votantes', '300');
        await page.type('#total_votos', '280');
        // ... más campos
        
        // Enviar
        await page.click('#btn-guardar-formulario');
        
        // Verificar éxito
        const alert = await page.waitForSelector('.alert-success');
        expect(await alert.textContent()).toContain('exitosamente');
    });
});
```

### Cobertura de Tests

| Componente | Cobertura Objetivo |
|------------|-------------------|
| Servicios Backend | 90% |
| Validaciones | 100% |
| API Endpoints | 85% |
| Frontend JS | 70% |
| E2E Críticos | 100% |

## Despliegue

### Entornos

#### Desarrollo
```bash
# .env.development
FLASK_ENV=development
DEBUG=True
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=dev-jwt-secret
DATABASE_URL=sqlite:///electoral_dev.db
UPLOAD_FOLDER=uploads/dev
```

#### Staging
```bash
# .env.staging
FLASK_ENV=staging
DEBUG=False
SECRET_KEY=${STAGING_SECRET_KEY}
JWT_SECRET_KEY=${STAGING_JWT_SECRET}
DATABASE_URL=postgresql://user:pass@staging-db:5432/electoral
UPLOAD_FOLDER=/var/www/uploads
```

#### Producción
```bash
# .env.production
FLASK_ENV=production
DEBUG=False
SECRET_KEY=${PROD_SECRET_KEY}
JWT_SECRET_KEY=${PROD_JWT_SECRET}
DATABASE_URL=postgresql://user:pass@prod-db:5432/electoral
UPLOAD_FOLDER=/var/www/uploads
SENTRY_DSN=${SENTRY_DSN}
```

### Infraestructura

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
│                    (Nginx/HAProxy)                       │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
│  App Server 1  │  │  App Server 2  │  │  App Server 3  │
│  (Gunicorn)    │  │  (Gunicorn)    │  │  (Gunicorn)    │
└────────────────┘  └────────────────┘  └────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                ┌───────────▼───────────┐
                │   PostgreSQL DB       │
                │   (Primary/Replica)   │
                └───────────────────────┘
                            │
                ┌───────────▼───────────┐
                │   Redis Cache         │
                │   (Session/Queue)     │
                └───────────────────────┘
```

### Comandos de Despliegue

```bash
# Desarrollo
python run.py

# Producción con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 --access-logfile - --error-logfile - run:app

# Con Docker
docker-compose up -d

# Migraciones de BD
flask db upgrade

# Cargar datos iniciales
python scripts/load_divipola.py
python scripts/create_admin_user.py
```

## Monitoreo y Logs

### Logging

```python
# config/logging.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug:
        # File handler
        file_handler = RotatingFileHandler(
            'logs/electoral.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Sistema Electoral startup')
```

### Métricas

```python
# Métricas a monitorear
- Usuarios activos concurrentes
- Formularios creados por hora
- Tiempo promedio de aprobación
- Tasa de rechazo de formularios
- Errores por endpoint
- Tiempo de respuesta de API
- Uso de CPU/Memoria
- Espacio en disco
```

### Alertas

```python
# Configurar alertas para:
- Errores 500 > 10 en 5 minutos
- Tiempo de respuesta > 2 segundos
- Uso de disco > 80%
- Base de datos no disponible
- Formularios sin aprobar > 100
- Intentos de login fallidos > 50 en 10 minutos
```

## Optimización de Rendimiento

### Base de Datos

```sql
-- Índices críticos
CREATE INDEX idx_forms_e14_estado_created ON forms_e14(estado, created_at);
CREATE INDEX idx_forms_e14_mesa_estado ON forms_e14(mesa_id, estado);
CREATE INDEX idx_users_rol_ubicacion ON users(rol, ubicacion_id);

-- Consultas optimizadas
-- Usar EXPLAIN ANALYZE para verificar planes de ejecución
EXPLAIN ANALYZE
SELECT * FROM forms_e14 
WHERE estado = 'enviado' 
AND mesa_id IN (SELECT id FROM locations WHERE puesto_id = 123)
ORDER BY created_at DESC
LIMIT 20;
```

### Caché

```python
# Redis para caché
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@cache.cached(timeout=300, key_prefix='dashboard_stats')
def get_dashboard_stats(user_id):
    # Cálculos costosos
    return stats
```

### Frontend

```javascript
// Lazy loading de imágenes
<img src="placeholder.jpg" data-src="real-image.jpg" class="lazy">

// Paginación infinita
const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        loadMoreForms();
    }
});

// Debounce en búsquedas
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', Utils.debounce(performSearch, 500));
```

## Consideraciones de Escalabilidad

### Horizontal Scaling

- Múltiples instancias de la aplicación detrás de load balancer
- Sesiones en Redis (no en memoria del servidor)
- Archivos en almacenamiento compartido (S3, NFS)
- Base de datos con réplicas de lectura

### Vertical Scaling

- Aumentar recursos de servidor según carga
- Optimizar consultas SQL
- Implementar caché agresivo
- Comprimir respuestas HTTP

### Límites del Sistema

| Métrica | Límite Actual | Límite Objetivo |
|---------|---------------|-----------------|
| Usuarios concurrentes | 100 | 1,000 |
| Formularios/hora | 500 | 5,000 |
| Tiempo respuesta API | 2s | 500ms |
| Tamaño BD | 10GB | 100GB |
| Archivos subidos | 1,000 | 50,000 |

## Mantenimiento

### Backups

```bash
# Backup diario de base de datos
0 2 * * * pg_dump electoral > /backups/electoral_$(date +\%Y\%m\%d).sql

# Backup de archivos subidos
0 3 * * * rsync -av /var/www/uploads/ /backups/uploads/

# Retención: 30 días
find /backups -name "*.sql" -mtime +30 -delete
```

### Actualizaciones

```bash
# 1. Backup
./scripts/backup.sh

# 2. Detener aplicación
systemctl stop electoral

# 3. Actualizar código
git pull origin main

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Migrar BD
flask db upgrade

# 6. Reiniciar aplicación
systemctl start electoral

# 7. Verificar
curl http://localhost:8000/api/health
```

### Limpieza

```python
# Limpiar logs antiguos
find logs/ -name "*.log" -mtime +90 -delete

# Limpiar sesiones expiradas
flask clean-sessions

# Limpiar archivos temporales
flask clean-temp-files

# Optimizar base de datos
VACUUM ANALYZE;
```

## Conclusión

Este diseño técnico proporciona una arquitectura robusta y escalable para el Sistema Electoral E-14/E-24. Los componentes están claramente separados, las interfaces bien definidas, y se han considerado aspectos críticos como seguridad, rendimiento y mantenibilidad.

### Próximos Pasos

1. Revisar y aprobar este diseño
2. Crear el plan de implementación detallado (tasks.md)
3. Comenzar desarrollo por fases priorizadas
4. Implementar tests desde el inicio
5. Desplegar en ambiente de staging para pruebas
6. Capacitar usuarios antes del día electoral

