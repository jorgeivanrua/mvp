# Design Document - Dashboard Coordinador Municipal

## Overview

El Dashboard del Coordinador Municipal es una aplicación web que permite supervisar todos los puestos de votación de un municipio, consolidar resultados electorales, identificar discrepancias, y generar el formulario E-24 Municipal oficial. El sistema se construye sobre la arquitectura existente del sistema electoral, reutilizando servicios, modelos y componentes ya implementados para el Dashboard del Coordinador de Puesto.

### Objetivos del Diseño

1. Proporcionar una vista consolidada de todos los puestos del municipio
2. Permitir drill-down desde municipio → puesto → formularios individuales
3. Detectar automáticamente discrepancias y anomalías
4. Generar reportes oficiales (E-24 Municipal)
5. Facilitar comunicación con coordinadores de puesto
6. Mantener consistencia con dashboards existentes

### Principios de Diseño

- **Reutilización**: Aprovechar servicios y componentes existentes
- **Escalabilidad**: Diseño que soporte municipios con muchos puestos
- **Tiempo Real**: Actualización automática de datos sin recargar página
- **Usabilidad**: Interfaz intuitiva similar al dashboard de puesto
- **Seguridad**: Control de acceso estricto por ubicación

## Architecture

### System Context


```
┌─────────────────────────────────────────────────────────────┐
│                  Coordinador Municipal                       │
│                    (Navegador Web)                           │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/JWT
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Frontend - Dashboard Municipal                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Vista General│  │ Vista Puesto │  │ Comparación  │     │
│  │  Municipio   │  │  Individual  │  │   Puestos    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                Backend - Flask API                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Routes (coordinador_municipal.py)          │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────┴─────────────────────────────────┐  │
│  │              Services Layer                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │ Consolidado  │  │  Discrepancia│  │   E-24     │ │  │
│  │  │   Service    │  │   Service    │  │  Service   │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────┴─────────────────────────────────┐  │
│  │              Models Layer                             │  │
│  │  FormularioE14 | Location | User | Partido           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                         │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- HTML5 + CSS3 (Bootstrap 5)
- JavaScript (Vanilla ES6+)
- Chart.js para gráficos
- Bootstrap Icons

**Backend:**
- Python 3.9+
- Flask 2.x
- SQLAlchemy (ORM)
- Flask-JWT-Extended (autenticación)

**Database:**
- PostgreSQL 13+



## Components and Interfaces

### Backend Components

#### 1. Routes - coordinador_municipal.py

Nuevo blueprint para endpoints específicos del coordinador municipal:

```python
# GET /api/coordinador-municipal/puestos
# Obtener lista de puestos del municipio con estadísticas
# Response: {
#   success: bool,
#   data: {
#     puestos: [
#       {
#         id: int,
#         codigo: str,
#         nombre: str,
#         total_mesas: int,
#         mesas_reportadas: int,
#         mesas_validadas: int,
#         porcentaje_avance: float,
#         coordinador: {id, nombre, telefono, ultimo_acceso},
#         estado: str,  # completo, incompleto, con_discrepancias
#         tiene_discrepancias: bool,
#         ultima_actualizacion: datetime
#       }
#     ],
#     estadisticas: {
#       total_puestos: int,
#       puestos_completos: int,
#       puestos_incompletos: int,
#       puestos_con_discrepancias: int,
#       cobertura_porcentaje: float
#     }
#   }
# }

# GET /api/coordinador-municipal/consolidado
# Obtener consolidado municipal
# Query params: tipo_eleccion_id (opcional)
# Response: {
#   success: bool,
#   data: {
#     municipio: {id, codigo, nombre, total_puestos, total_mesas},
#     resumen: {
#       total_votantes_registrados: int,
#       total_votos: int,
#       votos_validos: int,
#       votos_nulos: int,
#       votos_blanco: int,
#       participacion_porcentaje: float
#     },
#     votos_por_partido: [...],
#     votos_por_candidato: [...]
#   }
# }

# GET /api/coordinador-municipal/puesto/<puesto_id>
# Obtener detalles completos de un puesto
# Response: {
#   success: bool,
#   data: {
#     puesto: {...},
#     coordinador: {...},
#     mesas: [...],
#     formularios: [...],
#     consolidado: {...},
#     estadisticas: {...}
#   }
# }

# GET /api/coordinador-municipal/discrepancias
# Obtener puestos con discrepancias
# Response: {
#   success: bool,
#   data: [
#     {
#       puesto_id: int,
#       puesto_nombre: str,
#       tipo_discrepancia: str,
#       severidad: str,  # baja, media, alta, critica
#       descripcion: str,
#       valor_esperado: any,
#       valor_actual: any
#     }
#   ]
# }

# POST /api/coordinador-municipal/e24-municipal
# Generar formulario E-24 Municipal
# Body: {tipo_eleccion_id: int}
# Response: {
#   success: bool,
#   data: {
#     e24_id: int,
#     pdf_url: str,
#     fecha_generacion: datetime
#   }
# }

# GET /api/coordinador-municipal/comparacion
# Comparar múltiples puestos
# Query params: puesto_ids (comma-separated)
# Response: {
#   success: bool,
#   data: {
#     puestos: [...],
#     comparacion: {
#       participacion: [...],
#       votos_por_partido: [...],
#       desviacion_estandar: float
#     }
#   }
# }

# GET /api/coordinador-municipal/estadisticas
# Obtener estadísticas detalladas del municipio
# Response: {
#   success: bool,
#   data: {
#     resumen_general: {...},
#     formularios_por_estado: {...},
#     tiempo_promedio_validacion: float,
#     tasa_rechazo_por_puesto: [...],
#     progreso_temporal: [...]
#   }
# }

# POST /api/coordinador-municipal/notificar
# Enviar notificación a coordinadores de puesto
# Body: {
#   puesto_ids: [int],
#   mensaje: str,
#   prioridad: str
# }

# GET /api/coordinador-municipal/exportar
# Exportar datos consolidados
# Query params: formato (csv, xlsx)
# Response: archivo descargable
```



#### 2. Services - municipal_service.py

Nuevo servicio para lógica de negocio del coordinador municipal:

```python
class MunicipalService:
    """Servicio para operaciones del coordinador municipal"""
    
    @staticmethod
    def obtener_puestos_municipio(municipio_id, filtros=None):
        """
        Obtener lista de puestos con estadísticas
        
        Args:
            municipio_id: ID del municipio
            filtros: dict con filtros opcionales (estado, zona, etc.)
            
        Returns:
            dict con puestos y estadísticas
        """
        pass
    
    @staticmethod
    def calcular_estadisticas_puesto(puesto_id):
        """
        Calcular estadísticas detalladas de un puesto
        Reutiliza ConsolidadoService.obtener_estadisticas_puesto()
        """
        pass
    
    @staticmethod
    def obtener_puesto_detallado(puesto_id, coordinador_id):
        """
        Obtener información completa de un puesto
        Incluye: datos básicos, coordinador, mesas, formularios, consolidado
        """
        pass
    
    @staticmethod
    def comparar_puestos(puesto_ids):
        """
        Comparar estadísticas entre múltiples puestos
        Calcula desviación estándar y outliers
        """
        pass
```

#### 3. Services - discrepancia_service.py

Nuevo servicio para detección de discrepancias:

```python
class DiscrepanciaService:
    """Servicio para detección de anomalías y discrepancias"""
    
    @staticmethod
    def detectar_discrepancias_puesto(puesto_id):
        """
        Detectar discrepancias en un puesto
        
        Tipos de discrepancias:
        - Participación anormal (>95% o <30%)
        - Suma de votos no coincide
        - Coordinador inactivo (>2 horas sin acceso)
        - Alta tasa de rechazo (>15%)
        
        Returns:
            list de discrepancias con severidad
        """
        pass
    
    @staticmethod
    def detectar_discrepancias_municipio(municipio_id):
        """
        Detectar discrepancias a nivel municipal
        Agrega discrepancias de todos los puestos
        """
        pass
    
    @staticmethod
    def calcular_severidad(tipo_discrepancia, valores):
        """
        Calcular nivel de severidad de una discrepancia
        Returns: 'baja', 'media', 'alta', 'critica'
        """
        pass
```

#### 4. Services - e24_service.py

Nuevo servicio para generación de formularios E-24:

```python
class E24Service:
    """Servicio para generación de formularios E-24"""
    
    @staticmethod
    def generar_e24_municipal(municipio_id, tipo_eleccion_id, coordinador_id):
        """
        Generar formulario E-24 Municipal
        
        Validaciones:
        - Al menos 80% de puestos con datos completos
        - Todos los datos consolidados son coherentes
        
        Proceso:
        1. Validar requisitos mínimos
        2. Calcular consolidado municipal
        3. Generar PDF con formato oficial
        4. Registrar en base de datos
        5. Retornar URL del PDF
        """
        pass
    
    @staticmethod
    def validar_requisitos_e24(municipio_id):
        """
        Validar que se cumplen requisitos para generar E-24
        Returns: (bool, list_errores)
        """
        pass
    
    @staticmethod
    def generar_pdf_e24(datos_consolidado, municipio, coordinador):
        """
        Generar PDF del formulario E-24 Municipal
        Usa librería ReportLab o WeasyPrint
        """
        pass
```



### Frontend Components

#### 1. coordinador-municipal.html

Template principal del dashboard:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Coordinador Municipal</title>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-icons.css">
    <link rel="stylesheet" href="/static/css/dashboard.css">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-dark bg-primary">
        <div class="container-fluid">
            <span class="navbar-brand">Dashboard Coordinador Municipal</span>
            <div>
                <span id="municipioInfo" class="text-white me-3"></span>
                <button class="btn btn-outline-light btn-sm" onclick="logout()">
                    <i class="bi bi-box-arrow-right"></i> Salir
                </button>
            </div>
        </div>
    </nav>

    <div class="container-fluid py-4">
        <div class="row">
            <!-- Panel izquierdo: Estadísticas y Consolidado -->
            <div class="col-md-3">
                <!-- Estadísticas Generales -->
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0">Estadísticas Generales</h6>
                    </div>
                    <div class="card-body">
                        <div id="estadisticasGenerales"></div>
                    </div>
                </div>

                <!-- Consolidado Municipal -->
                <div class="card mb-3">
                    <div class="card-header">
                        <h6 class="mb-0">Consolidado Municipal</h6>
                    </div>
                    <div class="card-body">
                        <div id="consolidadoMunicipal"></div>
                    </div>
                </div>

                <!-- Acciones Rápidas -->
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0">Acciones</h6>
                    </div>
                    <div class="card-body">
                        <button class="btn btn-primary btn-sm w-100 mb-2" 
                                onclick="generarE24Municipal()">
                            <i class="bi bi-file-earmark-pdf"></i> Generar E-24
                        </button>
                        <button class="btn btn-outline-primary btn-sm w-100 mb-2" 
                                onclick="exportarDatos()">
                            <i class="bi bi-download"></i> Exportar Datos
                        </button>
                        <button class="btn btn-outline-secondary btn-sm w-100" 
                                onclick="abrirComparacion()">
                            <i class="bi bi-bar-chart"></i> Comparar Puestos
                        </button>
                    </div>
                </div>
            </div>

            <!-- Panel central: Lista de Puestos -->
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Puestos de Votación</h5>
                        <div>
                            <button class="btn btn-sm btn-outline-primary" 
                                    onclick="loadPuestos()">
                                <i class="bi bi-arrow-clockwise"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <!-- Filtros -->
                        <div class="mb-3">
                            <div class="btn-group btn-group-sm" id="filterButtons">
                                <button class="btn btn-outline-secondary active" 
                                        onclick="filtrarPuestos('')">
                                    Todos
                                </button>
                                <button class="btn btn-outline-success" 
                                        onclick="filtrarPuestos('completo')">
                                    Completos
                                </button>
                                <button class="btn btn-outline-warning" 
                                        onclick="filtrarPuestos('incompleto')">
                                    Incompletos
                                </button>
                                <button class="btn btn-outline-danger" 
                                        onclick="filtrarPuestos('con_discrepancias')">
                                    Con Discrepancias
                                </button>
                            </div>
                            <input type="text" class="form-control form-control-sm mt-2" 
                                   id="searchPuesto" placeholder="Buscar puesto..."
                                   onkeyup="buscarPuesto()">
                        </div>

                        <!-- Tabla de Puestos -->
                        <div class="table-responsive" style="max-height: 600px; overflow-y: auto;">
                            <table class="table table-hover" id="puestosTable">
                                <thead class="table-light sticky-top">
                                    <tr>
                                        <th>Puesto</th>
                                        <th>Coordinador</th>
                                        <th>Avance</th>
                                        <th>Estado</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Panel derecho: Detalle de Puesto Seleccionado -->
            <div class="col-md-3">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0">Detalle de Puesto</h6>
                    </div>
                    <div class="card-body">
                        <div id="detallePuesto">
                            <p class="text-muted text-center">
                                Seleccione un puesto para ver detalles
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Discrepancias -->
                <div class="card mt-3">
                    <div class="card-header">
                        <h6 class="mb-0">Alertas y Discrepancias</h6>
                    </div>
                    <div class="card-body">
                        <div id="discrepanciasPanel"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Modales -->
    <!-- Modal: Detalle Completo de Puesto -->
    <!-- Modal: Comparación de Puestos -->
    <!-- Modal: Generación E-24 -->
    <!-- Modal: Exportar Datos -->

    <script src="/static/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/chart.min.js"></script>
    <script src="/static/js/utils.js"></script>
    <script src="/static/js/api-client.js"></script>
    <script src="/static/js/coordinador-municipal.js"></script>
</body>
</html>
```



#### 2. coordinador-municipal.js

Script principal del dashboard:

```javascript
// Estado global
let currentUser = null;
let userLocation = null;
let puestos = [];
let puestoSeleccionado = null;
let filtroEstado = '';
let autoRefreshInterval = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    loadUserProfile();
    loadPuestos();
    loadConsolidadoMunicipal();
    loadDiscrepancias();
    
    // Auto-refresh cada 60 segundos
    autoRefreshInterval = setInterval(() => {
        loadPuestos();
        loadConsolidadoMunicipal();
        loadDiscrepancias();
    }, 60000);
});

// Funciones principales
async function loadPuestos() {
    // Cargar lista de puestos con estadísticas
    // GET /api/coordinador-municipal/puestos
}

async function loadConsolidadoMunicipal() {
    // Cargar consolidado municipal
    // GET /api/coordinador-municipal/consolidado
    // Renderizar gráfico de barras con Chart.js
}

async function loadDiscrepancias() {
    // Cargar discrepancias detectadas
    // GET /api/coordinador-municipal/discrepancias
}

async function seleccionarPuesto(puestoId) {
    // Cargar detalles completos del puesto
    // GET /api/coordinador-municipal/puesto/{puestoId}
    // Mostrar en panel derecho
}

async function generarE24Municipal() {
    // Validar requisitos
    // Mostrar modal de confirmación
    // POST /api/coordinador-municipal/e24-municipal
    // Descargar PDF generado
}

async function abrirComparacion() {
    // Mostrar modal para seleccionar puestos
    // GET /api/coordinador-municipal/comparacion
    // Renderizar gráficos comparativos
}

async function exportarDatos(formato) {
    // GET /api/coordinador-municipal/exportar?formato={csv|xlsx}
    // Descargar archivo
}

function filtrarPuestos(estado) {
    // Filtrar lista de puestos por estado
    filtroEstado = estado;
    renderPuestosTable(puestos);
}

function buscarPuesto() {
    // Buscar puesto por código o nombre
    const query = document.getElementById('searchPuesto').value;
    // Filtrar y renderizar
}

function renderPuestosTable(puestos) {
    // Renderizar tabla de puestos
    // Aplicar filtros activos
    // Resaltar puestos con discrepancias
}

function renderDetallePuesto(puesto) {
    // Renderizar detalles del puesto seleccionado
    // Mostrar: coordinador, mesas, formularios, consolidado
}

function renderDiscrepancias(discrepancias) {
    // Renderizar lista de discrepancias
    // Agrupar por severidad
    // Permitir navegar al puesto con discrepancia
}
```



## Data Models

### Existing Models (Reused)

El dashboard reutiliza los modelos existentes:

- **FormularioE14**: Formularios de mesa electoral
- **Location**: Jerarquía geográfica (departamento → municipio → puesto → mesa)
- **User**: Usuarios del sistema (coordinadores, testigos)
- **Partido**: Partidos políticos
- **Candidato**: Candidatos por tipo de elección
- **VotoPartido**: Votos por partido en formularios
- **VotoCandidato**: Votos por candidato en formularios

### New Models

#### FormularioE24Municipal

Nuevo modelo para registrar generaciones del E-24 Municipal:

```python
class FormularioE24Municipal(db.Model):
    """Formulario E-24 consolidado municipal"""
    __tablename__ = 'formularios_e24_municipal'
    
    id = db.Column(db.Integer, primary_key=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    coordinador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'), nullable=False)
    
    # Datos consolidados
    total_puestos = db.Column(db.Integer, nullable=False)
    puestos_incluidos = db.Column(db.Integer, nullable=False)
    total_mesas = db.Column(db.Integer, nullable=False)
    total_votantes_registrados = db.Column(db.Integer, nullable=False)
    total_votos = db.Column(db.Integer, nullable=False)
    votos_validos = db.Column(db.Integer, nullable=False)
    votos_nulos = db.Column(db.Integer, nullable=False)
    votos_blanco = db.Column(db.Integer, nullable=False)
    
    # Archivo PDF
    pdf_url = db.Column(db.String(500), nullable=False)
    pdf_hash = db.Column(db.String(64))  # SHA-256
    
    # Metadatos
    version = db.Column(db.Integer, default=1)  # Para regeneraciones
    observaciones = db.Column(db.Text)
    
    # Auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    municipio = db.relationship('Location', foreign_keys=[municipio_id])
    coordinador = db.relationship('User', foreign_keys=[coordinador_id])
    tipo_eleccion = db.relationship('TipoEleccion')
    votos_partidos = db.relationship('VotoPartidoE24Municipal', cascade='all, delete-orphan')
```

#### VotoPartidoE24Municipal

```python
class VotoPartidoE24Municipal(db.Model):
    """Votos por partido en E-24 Municipal"""
    __tablename__ = 'votos_partidos_e24_municipal'
    
    id = db.Column(db.Integer, primary_key=True)
    e24_municipal_id = db.Column(db.Integer, db.ForeignKey('formularios_e24_municipal.id'), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    
    # Relaciones
    e24_municipal = db.relationship('FormularioE24Municipal', back_populates='votos_partidos')
    partido = db.relationship('Partido')
```

#### Notificacion

```python
class Notificacion(db.Model):
    """Notificaciones enviadas a coordinadores"""
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    remitente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.String(20), default='normal')  # baja, normal, alta, urgente
    leida = db.Column(db.Boolean, default=False)
    leida_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    remitente = db.relationship('User', foreign_keys=[remitente_id])
    destinatario = db.relationship('User', foreign_keys=[destinatario_id])
```



## Error Handling

### Error Types

1. **Errores de Autenticación**
   - Token JWT inválido o expirado
   - Usuario sin permisos de coordinador municipal
   - Usuario sin municipio asignado

2. **Errores de Validación**
   - Requisitos mínimos no cumplidos para E-24 (< 80% puestos)
   - Datos inconsistentes en consolidado
   - Parámetros de request inválidos

3. **Errores de Datos**
   - Puesto no encontrado
   - Municipio sin puestos asignados
   - No hay formularios validados

4. **Errores del Sistema**
   - Error de base de datos
   - Error al generar PDF
   - Error al exportar datos

### Error Response Format

```json
{
  "success": false,
  "error": "Mensaje de error legible",
  "error_code": "ERROR_CODE",
  "details": {
    "field": "campo específico con error",
    "value": "valor que causó el error"
  }
}
```

### Frontend Error Handling

```javascript
try {
    const response = await APIClient.get('/api/coordinador-municipal/puestos');
    if (!response.success) {
        throw new Error(response.error);
    }
    // Procesar datos
} catch (error) {
    console.error('Error:', error);
    
    // Mostrar mensaje al usuario
    if (error.message.includes('autenticación')) {
        Utils.showError('Sesión expirada. Por favor inicie sesión nuevamente.');
        setTimeout(() => window.location.href = '/login', 2000);
    } else if (error.message.includes('permisos')) {
        Utils.showError('No tiene permisos para acceder a esta funcionalidad.');
    } else {
        Utils.showError('Error al cargar datos: ' + error.message);
    }
    
    // Mostrar UI de error con opción de reintentar
    renderErrorState('No se pudieron cargar los puestos', () => loadPuestos());
}
```

### Backend Error Handling

```python
from backend.utils.exceptions import (
    NotFoundException,
    ValidationException,
    UnauthorizedException
)

@coordinador_municipal_bp.route('/puestos', methods=['GET'])
@jwt_required()
@role_required(['coordinador_municipal'])
def obtener_puestos():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            raise ValidationException('Usuario sin ubicación asignada')
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'municipio':
            raise ValidationException('Usuario no asignado a un municipio válido')
        
        # Obtener puestos
        resultado = MunicipalService.obtener_puestos_municipio(ubicacion.id)
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
        
    except ValidationException as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f'Error en obtener_puestos: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
```



## Testing Strategy

### Unit Tests

**Backend Services:**

```python
# tests/test_municipal_service.py
class TestMunicipalService:
    def test_obtener_puestos_municipio(self):
        """Verificar que se obtienen todos los puestos del municipio"""
        pass
    
    def test_obtener_puestos_con_filtros(self):
        """Verificar filtrado por estado"""
        pass
    
    def test_calcular_estadisticas_puesto(self):
        """Verificar cálculo de estadísticas"""
        pass
    
    def test_comparar_puestos(self):
        """Verificar comparación entre puestos"""
        pass

# tests/test_discrepancia_service.py
class TestDiscrepanciaService:
    def test_detectar_participacion_anormal_alta(self):
        """Detectar participación > 95%"""
        pass
    
    def test_detectar_participacion_anormal_baja(self):
        """Detectar participación < 30%"""
        pass
    
    def test_detectar_suma_votos_incorrecta(self):
        """Detectar cuando suma de votos no coincide"""
        pass
    
    def test_calcular_severidad(self):
        """Verificar cálculo de severidad"""
        pass

# tests/test_e24_service.py
class TestE24Service:
    def test_validar_requisitos_e24_cumplidos(self):
        """Validar cuando se cumplen requisitos (>80% puestos)"""
        pass
    
    def test_validar_requisitos_e24_no_cumplidos(self):
        """Validar cuando no se cumplen requisitos"""
        pass
    
    def test_generar_e24_municipal(self):
        """Verificar generación completa del E-24"""
        pass
    
    def test_generar_pdf_e24(self):
        """Verificar generación del PDF"""
        pass
```

**Backend Routes:**

```python
# tests/test_coordinador_municipal_routes.py
class TestCoordinadorMunicipalRoutes:
    def test_obtener_puestos_sin_autenticacion(self):
        """Verificar que requiere autenticación"""
        pass
    
    def test_obtener_puestos_rol_incorrecto(self):
        """Verificar que requiere rol coordinador_municipal"""
        pass
    
    def test_obtener_puestos_exitoso(self):
        """Verificar respuesta exitosa"""
        pass
    
    def test_generar_e24_sin_requisitos(self):
        """Verificar que falla si no se cumplen requisitos"""
        pass
    
    def test_generar_e24_exitoso(self):
        """Verificar generación exitosa del E-24"""
        pass
```

### Integration Tests

```python
# tests/integration/test_dashboard_municipal_flow.py
class TestDashboardMunicipalFlow:
    def test_flujo_completo_coordinador_municipal(self):
        """
        Flujo completo:
        1. Login como coordinador municipal
        2. Obtener lista de puestos
        3. Seleccionar un puesto
        4. Ver detalles del puesto
        5. Obtener consolidado municipal
        6. Detectar discrepancias
        7. Generar E-24 Municipal
        """
        pass
    
    def test_comparacion_puestos(self):
        """
        Flujo de comparación:
        1. Seleccionar múltiples puestos
        2. Obtener datos comparativos
        3. Verificar cálculos estadísticos
        """
        pass
```

### Frontend Tests

```javascript
// tests/frontend/test_coordinador_municipal.js
describe('Dashboard Coordinador Municipal', () => {
    describe('loadPuestos', () => {
        it('debe cargar lista de puestos correctamente', async () => {
            // Mock API response
            // Verificar renderizado
        });
        
        it('debe manejar error de carga', async () => {
            // Mock error response
            // Verificar mensaje de error
        });
    });
    
    describe('filtrarPuestos', () => {
        it('debe filtrar por estado completo', () => {
            // Verificar filtrado
        });
        
        it('debe filtrar por discrepancias', () => {
            // Verificar filtrado
        });
    });
    
    describe('generarE24Municipal', () => {
        it('debe validar requisitos antes de generar', async () => {
            // Verificar validación
        });
        
        it('debe descargar PDF al generar exitosamente', async () => {
            // Verificar descarga
        });
    });
});
```

### Manual Testing Checklist

- [ ] Login como coordinador municipal
- [ ] Visualizar lista de puestos con estadísticas correctas
- [ ] Filtrar puestos por estado (completo, incompleto, con discrepancias)
- [ ] Buscar puesto por código o nombre
- [ ] Seleccionar puesto y ver detalles
- [ ] Visualizar consolidado municipal con gráfico
- [ ] Detectar y visualizar discrepancias
- [ ] Comparar múltiples puestos
- [ ] Generar E-24 Municipal (validar requisitos)
- [ ] Exportar datos en CSV y XLSX
- [ ] Enviar notificación a coordinador de puesto
- [ ] Verificar auto-refresh cada 60 segundos
- [ ] Verificar responsive design en móvil
- [ ] Verificar control de acceso (solo datos del municipio asignado)



## Security Considerations

### Authentication & Authorization

1. **JWT Token Validation**
   - Todos los endpoints requieren token JWT válido
   - Token debe contener user_id y rol
   - Expiración de token: 30 minutos de inactividad

2. **Role-Based Access Control (RBAC)**
   - Solo usuarios con rol `coordinador_municipal` pueden acceder
   - Decorador `@role_required(['coordinador_municipal'])` en todas las rutas

3. **Location-Based Access Control**
   - Coordinador solo puede ver datos de su municipio asignado
   - Validación en cada endpoint: `user.ubicacion_id == municipio_id`
   - No se permite acceso a datos de otros municipios

### Data Protection

1. **Input Validation**
   - Validar todos los parámetros de request
   - Sanitizar inputs para prevenir SQL injection
   - Validar tipos de datos y rangos

2. **Output Sanitization**
   - Escapar HTML en datos mostrados
   - No exponer información sensible en responses
   - Ocultar stack traces en producción

3. **File Security**
   - PDFs generados almacenados en directorio seguro
   - URLs de PDFs con tokens de acceso temporal
   - Validar hash SHA-256 de archivos

### Audit Logging

```python
class AuditLog(db.Model):
    """Log de auditoría de acciones"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accion = db.Column(db.String(100), nullable=False)
    recurso = db.Column(db.String(100))  # ej: 'puesto', 'e24_municipal'
    recurso_id = db.Column(db.Integer)
    detalles = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User')
```

**Acciones auditadas:**
- Visualización de puestos
- Acceso a detalles de puesto
- Generación de E-24 Municipal
- Exportación de datos
- Envío de notificaciones
- Comparación de puestos

### Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@coordinador_municipal_bp.route('/puestos', methods=['GET'])
@limiter.limit("100 per hour")
@jwt_required()
def obtener_puestos():
    pass

@coordinador_municipal_bp.route('/e24-municipal', methods=['POST'])
@limiter.limit("10 per hour")  # Límite más restrictivo
@jwt_required()
def generar_e24_municipal():
    pass
```

### HTTPS & CORS

```python
# Configuración CORS
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://sistema-electoral.gob.bo"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Forzar HTTPS en producción
@app.before_request
def before_request():
    if not request.is_secure and app.config['ENV'] == 'production':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```



## Performance Optimization

### Database Optimization

1. **Indexes**
```sql
-- Índices para mejorar queries frecuentes
CREATE INDEX idx_formularios_mesa_estado ON formularios_e14(mesa_id, estado);
CREATE INDEX idx_locations_municipio_tipo ON locations(municipio_codigo, tipo);
CREATE INDEX idx_locations_puesto ON locations(puesto_codigo);
CREATE INDEX idx_users_ubicacion_rol ON users(ubicacion_id, rol);
```

2. **Query Optimization**
```python
# Usar eager loading para evitar N+1 queries
puestos = Location.query.filter_by(
    municipio_codigo=municipio.municipio_codigo,
    tipo='puesto'
).options(
    joinedload(Location.coordinador),
    joinedload(Location.mesas)
).all()

# Usar agregaciones en base de datos en lugar de Python
stats = db.session.query(
    FormularioE14.estado,
    func.count(FormularioE14.id).label('total')
).filter(
    FormularioE14.mesa_id.in_(mesa_ids)
).group_by(
    FormularioE14.estado
).all()
```

3. **Caching**
```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@coordinador_municipal_bp.route('/consolidado', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, key_prefix='consolidado_municipal')
def obtener_consolidado():
    # Cache por 60 segundos
    pass
```

### Frontend Optimization

1. **Lazy Loading**
```javascript
// Cargar detalles de puesto solo cuando se selecciona
async function seleccionarPuesto(puestoId) {
    if (!puestoCache[puestoId]) {
        puestoCache[puestoId] = await APIClient.get(`/api/coordinador-municipal/puesto/${puestoId}`);
    }
    renderDetallePuesto(puestoCache[puestoId]);
}
```

2. **Debouncing**
```javascript
// Debounce para búsqueda
let searchTimeout;
function buscarPuesto() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        const query = document.getElementById('searchPuesto').value;
        filtrarYRenderizar(query);
    }, 300);
}
```

3. **Virtual Scrolling**
```javascript
// Para municipios con muchos puestos (>100)
// Renderizar solo elementos visibles en viewport
function renderPuestosVirtual(puestos) {
    const container = document.getElementById('puestosContainer');
    const itemHeight = 60; // altura de cada fila
    const visibleItems = Math.ceil(container.clientHeight / itemHeight);
    
    // Renderizar solo items visibles + buffer
    // Implementar con IntersectionObserver
}
```

### API Response Optimization

1. **Pagination**
```python
@coordinador_municipal_bp.route('/puestos', methods=['GET'])
def obtener_puestos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    pagination = Location.query.filter_by(
        municipio_codigo=municipio.municipio_codigo,
        tipo='puesto'
    ).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'data': {
            'puestos': [p.to_dict() for p in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }
    })
```

2. **Field Selection**
```python
# Permitir seleccionar campos específicos
@coordinador_municipal_bp.route('/puestos', methods=['GET'])
def obtener_puestos():
    fields = request.args.get('fields', '').split(',')
    
    # Retornar solo campos solicitados
    if fields:
        puestos_data = [
            {k: v for k, v in p.to_dict().items() if k in fields}
            for p in puestos
        ]
    else:
        puestos_data = [p.to_dict() for p in puestos]
```

3. **Compression**
```python
from flask_compress import Compress

Compress(app)  # Comprime responses automáticamente
```

### Monitoring & Metrics

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Métricas personalizadas
request_duration = metrics.histogram(
    'request_duration_seconds',
    'Request duration in seconds',
    labels={'endpoint': lambda: request.endpoint}
)

@coordinador_municipal_bp.route('/puestos', methods=['GET'])
@request_duration.time()
def obtener_puestos():
    pass
```



## Deployment Considerations

### Environment Configuration

```python
# config.py
class Config:
    # Base config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    
    # File storage
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/var/uploads')
    PDF_FOLDER = os.environ.get('PDF_FOLDER', '/var/pdfs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/1')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = '/var/log/sistema-electoral/app.log'
```

### Database Migrations

```python
# migrations/versions/xxx_add_coordinador_municipal_tables.py
"""Add coordinador municipal tables

Revision ID: xxx
Revises: yyy
Create Date: 2024-xx-xx

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Crear tabla formularios_e24_municipal
    op.create_table(
        'formularios_e24_municipal',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('municipio_id', sa.Integer(), nullable=False),
        sa.Column('coordinador_id', sa.Integer(), nullable=False),
        sa.Column('tipo_eleccion_id', sa.Integer(), nullable=False),
        sa.Column('total_puestos', sa.Integer(), nullable=False),
        sa.Column('puestos_incluidos', sa.Integer(), nullable=False),
        sa.Column('total_mesas', sa.Integer(), nullable=False),
        sa.Column('total_votantes_registrados', sa.Integer(), nullable=False),
        sa.Column('total_votos', sa.Integer(), nullable=False),
        sa.Column('votos_validos', sa.Integer(), nullable=False),
        sa.Column('votos_nulos', sa.Integer(), nullable=False),
        sa.Column('votos_blanco', sa.Integer(), nullable=False),
        sa.Column('pdf_url', sa.String(500), nullable=False),
        sa.Column('pdf_hash', sa.String(64)),
        sa.Column('version', sa.Integer(), default=1),
        sa.Column('observaciones', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['municipio_id'], ['locations.id']),
        sa.ForeignKeyConstraint(['coordinador_id'], ['users.id']),
        sa.ForeignKeyConstraint(['tipo_eleccion_id'], ['tipos_eleccion.id'])
    )
    
    # Crear tabla votos_partidos_e24_municipal
    op.create_table(
        'votos_partidos_e24_municipal',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('e24_municipal_id', sa.Integer(), nullable=False),
        sa.Column('partido_id', sa.Integer(), nullable=False),
        sa.Column('votos', sa.Integer(), nullable=False),
        sa.Column('porcentaje', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['e24_municipal_id'], ['formularios_e24_municipal.id']),
        sa.ForeignKeyConstraint(['partido_id'], ['partidos.id'])
    )
    
    # Crear tabla notificaciones
    op.create_table(
        'notificaciones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('remitente_id', sa.Integer(), nullable=False),
        sa.Column('destinatario_id', sa.Integer(), nullable=False),
        sa.Column('mensaje', sa.Text(), nullable=False),
        sa.Column('prioridad', sa.String(20), default='normal'),
        sa.Column('leida', sa.Boolean(), default=False),
        sa.Column('leida_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['remitente_id'], ['users.id']),
        sa.ForeignKeyConstraint(['destinatario_id'], ['users.id'])
    )
    
    # Crear tabla audit_logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('accion', sa.String(100), nullable=False),
        sa.Column('recurso', sa.String(100)),
        sa.Column('recurso_id', sa.Integer()),
        sa.Column('detalles', sa.JSON()),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('user_agent', sa.String(500)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )
    
    # Crear índices
    op.create_index('idx_e24_municipal_municipio', 'formularios_e24_municipal', ['municipio_id'])
    op.create_index('idx_notificaciones_destinatario', 'notificaciones', ['destinatario_id', 'leida'])
    op.create_index('idx_audit_logs_user', 'audit_logs', ['user_id', 'created_at'])

def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('notificaciones')
    op.drop_table('votos_partidos_e24_municipal')
    op.drop_table('formularios_e24_municipal')
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorios para uploads y PDFs
RUN mkdir -p /var/uploads /var/pdfs /var/log/sistema-electoral

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "backend.app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/electoral
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    volumes:
      - ./uploads:/var/uploads
      - ./pdfs:/var/pdfs
      - ./logs:/var/log/sistema-electoral
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=electoral
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:6-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

### Monitoring & Logging

```python
# backend/utils/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    """Configurar logging para la aplicación"""
    
    if not app.debug:
        # File handler
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/sistema-electoral.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Sistema Electoral startup')
```



## Implementation Notes

### Development Workflow

1. **Phase 1: Backend Foundation**
   - Crear modelos nuevos (FormularioE24Municipal, Notificacion, AuditLog)
   - Ejecutar migraciones de base de datos
   - Implementar servicios (MunicipalService, DiscrepanciaService, E24Service)
   - Crear tests unitarios para servicios

2. **Phase 2: API Endpoints**
   - Implementar routes en coordinador_municipal.py
   - Agregar decoradores de autenticación y autorización
   - Implementar manejo de errores
   - Crear tests de integración para endpoints

3. **Phase 3: Frontend Development**
   - Crear template HTML (coordinador-municipal.html)
   - Implementar JavaScript (coordinador-municipal.js)
   - Integrar con API Client existente
   - Implementar gráficos con Chart.js

4. **Phase 4: Features Avanzadas**
   - Implementar detección de discrepancias
   - Implementar generación de E-24 Municipal (PDF)
   - Implementar comparación de puestos
   - Implementar exportación de datos

5. **Phase 5: Testing & Refinement**
   - Testing manual completo
   - Optimización de performance
   - Ajustes de UI/UX
   - Documentación

### Code Reuse Strategy

**Servicios Existentes a Reutilizar:**
- `ConsolidadoService.calcular_consolidado_puesto()` - Para consolidados de puestos individuales
- `ConsolidadoService.obtener_estadisticas_puesto()` - Para estadísticas de puestos
- `FormularioService.obtener_formulario_por_id()` - Para detalles de formularios
- `ValidacionService` - Para lógica de validación

**Componentes Frontend a Reutilizar:**
- `api-client.js` - Cliente HTTP con autenticación
- `utils.js` - Funciones utilitarias (formateo, fechas, etc.)
- `dashboard.css` - Estilos base del dashboard
- Componentes de Bootstrap existentes

**Modelos Existentes:**
- `FormularioE14` - Formularios de mesa
- `Location` - Jerarquía geográfica
- `User` - Usuarios del sistema
- `Partido`, `Candidato` - Configuración electoral

### Dependencies

**Python Packages:**
```txt
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
Flask-JWT-Extended==4.5.0
Flask-CORS==4.0.0
Flask-Caching==2.0.0
Flask-Limiter==3.3.0
Flask-Compress==1.13
psycopg2-binary==2.9.0
reportlab==4.0.0  # Para generación de PDFs
openpyxl==3.1.0  # Para exportación Excel
redis==4.5.0
gunicorn==20.1.0
prometheus-flask-exporter==0.22.0
```

**JavaScript Libraries:**
```html
<!-- Ya incluidas en el proyecto -->
<script src="/static/js/bootstrap.bundle.min.js"></script>
<script src="/static/js/chart.min.js"></script>

<!-- Nuevas (si es necesario) -->
<script src="/static/js/xlsx.full.min.js"></script>  <!-- Para exportación Excel en cliente -->
```

### Configuration Files

```python
# backend/routes/__init__.py
from backend.routes.coordinador_municipal import coordinador_municipal_bp

def register_blueprints(app):
    # ... blueprints existentes
    app.register_blueprint(coordinador_municipal_bp)
```

```python
# backend/services/__init__.py
from backend.services.municipal_service import MunicipalService
from backend.services.discrepancia_service import DiscrepanciaService
from backend.services.e24_service import E24Service
```

### API Documentation

Usar Swagger/OpenAPI para documentar endpoints:

```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Sistema Electoral - API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
```

### Responsive Design Breakpoints

```css
/* Mobile first approach */

/* Extra small devices (phones, less than 576px) */
@media (max-width: 575.98px) {
    .col-md-3, .col-md-6 {
        width: 100%;
    }
    
    #puestosTable {
        font-size: 0.875rem;
    }
    
    .btn-group {
        flex-direction: column;
    }
}

/* Small devices (tablets, 576px and up) */
@media (min-width: 576px) and (max-width: 767.98px) {
    /* Ajustes para tablets */
}

/* Medium devices (desktops, 768px and up) */
@media (min-width: 768px) {
    /* Layout normal de 3 columnas */
}
```

### Browser Compatibility

**Supported Browsers:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Polyfills Required:**
- None (usando ES6+ features soportadas nativamente)

**Progressive Enhancement:**
- Funcionalidad básica sin JavaScript (formularios)
- Mejoras con JavaScript habilitado (auto-refresh, gráficos)

