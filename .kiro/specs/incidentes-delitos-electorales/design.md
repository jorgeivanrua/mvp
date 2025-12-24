# Design Document - Sistema de Incidentes y Delitos Electorales

## Overview

El Sistema de Incidentes y Delitos Electorales es un componente crítico que garantiza la transparencia y trazabilidad del proceso electoral mediante el reporte, gestión y seguimiento de irregularidades y violaciones. Utiliza un enfoque de escalamiento automático basado en severidad, notificaciones en tiempo real, y un sistema completo de auditoría para mantener la integridad del proceso electoral.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Incidentes y Delitos UI                     │   │
│  │  - Formularios de reporte                                │   │
│  │  - Dashboard de seguimiento                              │   │
│  │  - Gestión de evidencias fotográficas                    │   │
│  │  - Notificaciones en tiempo real                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Incidentes-Delitos JS Module                   │   │
│  │  - reportarIncidente()                                   │   │
│  │  - reportarDelito()                                      │   │
│  │  - subirEvidencia()                                      │   │
│  │  - actualizarEstado()                                    │   │
│  │  - cargarNotificaciones()                                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Sync Manager (Universal)                    │   │
│  │  - Sincronización offline de reportes                   │   │
│  │  - Upload de evidencias en background                    │   │
│  │  - Notificaciones push                                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTPS/REST API
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (Flask)                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         Incidentes y Delitos Routes                      │   │
│  │  - POST /api/incidentes                                  │   │
│  │  - GET /api/incidentes                                   │   │
│  │  - PUT /api/incidentes/{id}/estado                       │   │
│  │  - POST /api/delitos                                     │   │
│  │  - GET /api/delitos                                      │   │
│  │  - PUT /api/delitos/{id}/estado                          │   │
│  │  - POST /api/delitos/{id}/denunciar                      │   │
│  │  - POST /api/evidencia/upload                            │   │
│  │  - GET /api/evidencia/{filename}                         │   │
│  │  - GET /api/notificaciones                               │   │
│  │  - GET /api/reportes/estadisticas                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Incidentes Delitos Service                     │   │
│  │  - crear_incidente()                                     │   │
│  │  - crear_delito()                                        │   │
│  │  - actualizar_estado()                                   │   │
│  │  - generar_notificaciones()                              │   │
│  │  - calcular_escalamiento()                               │   │
│  │  - obtener_estadisticas()                                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Database Models                             │   │
│  │  - IncidenteElectoral                                    │   │
│  │  - DelitoElectoral                                       │   │
│  │  - EvidenciaFotografica                                  │   │
│  │  - NotificacionReporte                                   │   │
│  │  - SeguimientoReporte                                    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Database (PostgreSQL)                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  Tables                                  │   │
│  │  - incidentes_electorales                                │   │
│  │  - delitos_electorales                                   │   │
│  │  - evidencias_fotograficas                               │   │
│  │  - notificaciones_reportes                               │   │
│  │  - seguimiento_reportes                                  │   │
│  │  - users (relación con reportantes)                      │   │
│  │  - locations (relación con ubicaciones)                  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
incidentes-delitos.js
├── Inicialización
│   ├── initIncidentesDelitos()
│   ├── cargarTiposIncidentesDelitos()
│   └── poblarSelectores()
│
├── Reporte de Incidentes
│   ├── mostrarFormularioIncidente()
│   ├── reportarIncidente()
│   ├── validarDatosIncidente()
│   └── confirmarEnvioIncidente()
│
├── Reporte de Delitos
│   ├── mostrarFormularioDelito()
│   ├── reportarDelito()
│   ├── validarDatosDelito()
│   └── confirmarEnvioDelito()
│
├── Gestión de Evidencias
│   ├── subirEvidencia()
│   ├── previsualizarImagen()
│   ├── validarArchivo()
│   └── eliminarEvidencia()
│
├── Dashboard de Seguimiento
│   ├── cargarReportes()
│   ├── filtrarReportes()
│   ├── actualizarEstado()
│   └── verDetalleReporte()
│
├── Notificaciones
│   ├── cargarNotificaciones()
│   ├── marcarComoLeida()
│   ├── mostrarNotificacionPush()
│   └── actualizarContadorNotificaciones()
│
└── Sincronización Offline
    ├── guardarReporteOffline()
    ├── sincronizarReportesOffline()
    ├── subirEvidenciasOffline()
    └── manejarConflictosSincronizacion()
```

## Components and Interfaces

### 1. Formulario de Reporte de Incidentes

**Componente:** `mostrarFormularioIncidente()`

**Campos del Formulario:**
- **Tipo de Incidente:** Select con 15 tipos predefinidos
- **Título:** Input text (máximo 200 caracteres)
- **Descripción:** Textarea (mínimo 20 caracteres, máximo 2000)
- **Mesa Afectada:** Select con mesas asignadas al testigo
- **Fecha y Hora:** DateTime picker (default: ahora)
- **Severidad:** Select (Baja, Media, Alta) - default: Media
- **Evidencias:** Upload de hasta 3 fotografías
- **Ubicación GPS:** Captura automática si disponible

**Validaciones:**
- Tipo de incidente obligatorio
- Título obligatorio (mínimo 10 caracteres)
- Descripción obligatoria (mínimo 20 caracteres)
- Validación de archivos de imagen (JPG, PNG, WEBP, máximo 5MB)
- Detección de reportes duplicados (mismo tipo, ubicación, tiempo < 30 min)

**Flujo de Envío:**
1. Validar datos del formulario
2. Mostrar confirmación con resumen
3. Guardar localmente si offline
4. Enviar a servidor si online
5. Mostrar resultado y limpiar formulario

### 2. Formulario de Reporte de Delitos

**Componente:** `mostrarFormularioDelito()`

**Campos del Formulario:**
- **Tipo de Delito:** Select con 10 tipos predefinidos
- **Título:** Input text (máximo 200 caracteres)
- **Descripción:** Textarea (mínimo 50 caracteres, máximo 3000)
- **Mesa Afectada:** Select con mesas asignadas
- **Fecha y Hora:** DateTime picker (default: ahora)
- **Gravedad:** Select automático según tipo de delito
- **Testigos Adicionales:** Textarea opcional
- **Evidencias:** Upload de hasta 5 fotografías
- **Ubicación GPS:** Captura automática

**Validaciones Especiales:**
- Descripción mínimo 50 caracteres (más detallada que incidentes)
- Confirmación adicional antes de envío
- Validación de gravedad según tipo de delito
- Alertas sobre consecuencias legales

**Escalamiento Automático:**
- Delitos "Críticos" → Notificar a coordinador puesto, municipal y departamental
- Delitos "Altos" → Notificar a coordinador puesto y municipal
- Generación automática de alertas de seguimiento

### 3. Sistema de Evidencias Fotográficas

**Componente:** `subirEvidencia()`

**Funcionalidades:**
- **Captura desde Cámara:** Usar `navigator.mediaDevices.getUserMedia()`
- **Selección de Archivos:** Input file con múltiple selección
- **Preview de Imágenes:** Mostrar thumbnails antes de envío
- **Compresión Automática:** Reducir tamaño si > 2MB manteniendo calidad
- **Upload Progresivo:** Barra de progreso para cada imagen
- **Validación de Metadatos:** Extraer EXIF (fecha, ubicación, dispositivo)

**Formatos Soportados:**
```javascript
const formatosPermitidos = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
const tamañoMaximo = 5 * 1024 * 1024; // 5MB
const dimensionesMaximas = { width: 4000, height: 4000 };
```

**Almacenamiento:**
- Directorio: `frontend/static/uploads/evidencias/`
- Nomenclatura: `{UUID}_{timestamp}.{extension}`
- Thumbnails: `thumbnails/{UUID}_thumb.jpg` (150x150px)

### 4. Dashboard de Seguimiento para Coordinadores

**Componente:** `cargarReportes()`

**Vista de Tabla:**
- **Columnas:** Número, Tipo, Título, Severidad/Gravedad, Estado, Fecha, Testigo, Acciones
- **Filtros:** Estado, Tipo, Severidad, Fecha, Mesa, Testigo
- **Ordenamiento:** Por fecha (desc), severidad, estado
- **Paginación:** 20 reportes por página
- **Búsqueda:** Por número de reporte, título, descripción

**Estados de Reportes:**
```javascript
const estadosIncidentes = {
    'reportado': { label: 'Reportado', color: 'warning', icon: 'exclamation-triangle' },
    'en_revision': { label: 'En Revisión', color: 'info', icon: 'eye' },
    'resuelto': { label: 'Resuelto', color: 'success', icon: 'check-circle' },
    'escalado': { label: 'Escalado', color: 'danger', icon: 'arrow-up' }
};

const estadosDelitos = {
    'reportado': { label: 'Reportado', color: 'warning', icon: 'exclamation-triangle' },
    'en_investigacion': { label: 'En Investigación', color: 'info', icon: 'search' },
    'investigado': { label: 'Investigado', color: 'primary', icon: 'clipboard-check' },
    'denunciado': { label: 'Denunciado', color: 'success', icon: 'gavel' },
    'archivado': { label: 'Archivado', color: 'secondary', icon: 'archive' }
};
```

**Acciones por Reporte:**
- **Ver Detalles:** Modal con información completa
- **Cambiar Estado:** Select con comentario obligatorio
- **Ver Evidencias:** Galería de imágenes
- **Agregar Comentario:** Sistema de seguimiento
- **Exportar:** PDF individual o CSV masivo

### 5. Sistema de Notificaciones

**Componente:** `cargarNotificaciones()`

**Tipos de Notificaciones:**
```javascript
const tiposNotificacion = {
    'nuevo_incidente': {
        titulo: 'Nuevo Incidente Reportado',
        icono: 'exclamation-triangle',
        color: 'warning'
    },
    'nuevo_delito': {
        titulo: 'Nuevo Delito Reportado',
        icono: 'shield-exclamation',
        color: 'danger'
    },
    'cambio_estado': {
        titulo: 'Estado de Reporte Actualizado',
        icono: 'sync',
        color: 'info'
    },
    'comentario_agregado': {
        titulo: 'Nuevo Comentario',
        icono: 'comment',
        color: 'primary'
    }
};
```

**Canales de Notificación:**
- **Dashboard:** Badge numérico en header
- **Push Notifications:** Para delitos críticos
- **Email:** Para coordinadores (configurable)
- **Sonido:** Alerta audible para delitos

**Gestión de Notificaciones:**
- Auto-refresh cada 30 segundos
- Marcar como leída al hacer clic
- Agrupar notificaciones similares
- Retención por 30 días

## Data Models

### 1. IncidenteElectoral

```python
class IncidenteElectoral(db.Model):
    __tablename__ = 'incidentes_electorales'
    
    # Identificación
    id = db.Column(db.Integer, primary_key=True)
    reportado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Ubicación jerárquica
    mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    puesto_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    
    # Información del incidente
    tipo_incidente = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    severidad = db.Column(db.String(20), default='media')  # baja, media, alta, critica
    estado = db.Column(db.String(20), default='reportado')  # reportado, en_revision, resuelto, escalado
    
    # Evidencias y ubicación
    evidencia_url = db.Column(db.String(500), nullable=True)  # Deprecated - usar EvidenciaFotografica
    ubicacion_gps = db.Column(db.String(100), nullable=True)
    latitud_reporte = db.Column(db.Float, nullable=True)
    longitud_reporte = db.Column(db.Float, nullable=True)
    precision_gps = db.Column(db.Float, nullable=True)
    
    # Fechas
    fecha_incidente = db.Column(db.DateTime, nullable=True)
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Resolución
    resuelto_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    fecha_resolucion = db.Column(db.DateTime, nullable=True)
    notas_resolucion = db.Column(db.Text, nullable=True)
    escalado_a = db.Column(db.String(50), nullable=True)
    
    # Sincronización offline
    sincronizado = db.Column(db.Boolean, default=True)
    fecha_sincronizacion = db.Column(db.DateTime, nullable=True)
    dispositivo_id = db.Column(db.String(100), nullable=True)
    
    # Auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Tipos de Incidentes:**
```python
TIPOS_INCIDENTE = {
    'retraso_apertura': 'Retraso en apertura de mesa',
    'falta_material': 'Falta de material electoral',
    'problemas_tecnicos': 'Problemas técnicos',
    'irregularidades_proceso': 'Irregularidades en el proceso',
    'ausencia_funcionarios': 'Ausencia de funcionarios',
    'problemas_acceso': 'Problemas de acceso al puesto',
    'disturbios': 'Disturbios o alteración del orden',
    'otros': 'Otros incidentes'
}
```

### 2. DelitoElectoral

```python
class DelitoElectoral(db.Model):
    __tablename__ = 'delitos_electorales'
    
    # Identificación (similar a IncidenteElectoral)
    id = db.Column(db.Integer, primary_key=True)
    reportado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Ubicación jerárquica
    mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    puesto_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    
    # Información del delito
    tipo_delito = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    gravedad = db.Column(db.String(20), default='media')  # leve, media, grave, muy_grave
    estado = db.Column(db.String(30), default='reportado')  # reportado, en_investigacion, investigado, denunciado, archivado
    
    # Información adicional para delitos
    testigos_adicionales = db.Column(db.Text, nullable=True)
    
    # Investigación
    investigado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    fecha_investigacion = db.Column(db.DateTime, nullable=True)
    resultado_investigacion = db.Column(db.Text, nullable=True)
    
    # Denuncia formal
    denunciado_formalmente = db.Column(db.Boolean, default=False)
    numero_denuncia = db.Column(db.String(100), nullable=True)
    autoridad_competente = db.Column(db.String(200), nullable=True)
    fecha_denuncia = db.Column(db.DateTime, nullable=True)
    seguimiento = db.Column(db.Text, nullable=True)
```

**Tipos de Delitos:**
```python
TIPOS_DELITO = {
    'compra_votos': 'Compra de votos',
    'coaccion_votante': 'Coacción al votante',
    'fraude_electoral': 'Fraude electoral',
    'suplantacion_identidad': 'Suplantación de identidad',
    'alteracion_resultados': 'Alteración de resultados',
    'violencia_electoral': 'Violencia electoral',
    'propaganda_ilegal': 'Propaganda ilegal',
    'financiacion_ilegal': 'Financiación ilegal de campaña',
    'otros_delitos': 'Otros delitos electorales'
}
```

### 3. EvidenciaFotografica

```python
class EvidenciaFotografica(db.Model):
    __tablename__ = 'evidencias_fotograficas'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación con reporte
    incidente_id = db.Column(db.Integer, db.ForeignKey('incidentes_electorales.id'), nullable=True)
    delito_id = db.Column(db.Integer, db.ForeignKey('delitos_electorales.id'), nullable=True)
    
    # Información del archivo
    filename = db.Column(db.String(255), nullable=False, unique=True)
    filename_original = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    mime_type = db.Column(db.String(50), nullable=False)
    size_bytes = db.Column(db.Integer, nullable=False)
    
    # Metadatos de imagen
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    fecha_captura = db.Column(db.DateTime, nullable=True)
    dispositivo = db.Column(db.String(200), nullable=True)
    
    # Auditoría
    subido_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
```

### 4. NotificacionReporte

```python
class NotificacionReporte(db.Model):
    __tablename__ = 'notificaciones_reportes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo_reporte = db.Column(db.String(20), nullable=False)  # 'incidente' o 'delito'
    reporte_id = db.Column(db.Integer, nullable=False)
    tipo_notificacion = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    leida = db.Column(db.Boolean, default=False)
    fecha_lectura = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 5. SeguimientoReporte

```python
class SeguimientoReporte(db.Model):
    __tablename__ = 'seguimiento_reportes'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_reporte = db.Column(db.String(20), nullable=False)  # 'incidente' o 'delito'
    reporte_id = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accion = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado_anterior = db.Column(db.String(30), nullable=True)
    estado_nuevo = db.Column(db.String(30), nullable=True)
    visible_testigo = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Escalamiento Automático Consistente
*For any* delito reportado, el sistema debe generar notificaciones a los coordinadores apropiados según el nivel de gravedad configurado, sin duplicados ni omisiones
**Validates: Requirements 5.2, 5.3, 5.4, 8.1, 8.2**

### Property 2: Integridad de Estados de Reportes
*For any* cambio de estado de reporte, debe existir un registro de seguimiento correspondiente con usuario responsable, timestamp, y descripción válida
**Validates: Requirements 6.2, 6.4, 10.2, 15.2**

### Property 3: Validación de Evidencias Fotográficas
*For any* evidencia fotográfica subida, debe tener un formato válido, tamaño dentro de límites, y estar asociada a exactamente un reporte existente
**Validates: Requirements 7.2, 7.3, 7.4, 7.5**

### Property 4: Prevención de Duplicados
*For any* reporte creado, si existe otro reporte del mismo tipo, ubicación y dentro de 30 minutos, debe activarse la detección de duplicados
**Validates: Requirements 14.1, 14.2, 14.3**

### Property 5: Permisos de Acceso Jerárquicos
*For any* usuario accediendo a reportes, solo debe ver reportes de su jurisdicción según su rol (testigo ve sus reportes, coordinadores ven su área)
**Validates: Requirements 19.2, 19.3**

### Property 6: Sincronización Offline Correcta
*For any* reporte creado offline, cuando se restaure la conexión, debe sincronizarse exactamente una vez sin pérdida de datos
**Validates: Requirements 1.7, 13.6, 18.6**

### Property 7: Auditoría Completa de Acciones
*For any* acción realizada en el sistema (crear, modificar, acceder), debe existir un registro de auditoría correspondiente con todos los metadatos requeridos
**Validates: Requirements 15.1, 15.2, 15.3, 15.5, 19.3**

### Property 8: Notificaciones Apropiadas
*For any* evento que requiera notificación (nuevo reporte, cambio de estado), debe generarse exactamente una notificación por usuario destinatario
**Validates: Requirements 8.1, 8.2, 8.7, 10.5**

## Error Handling

### 1. Errores de Validación de Datos

**Tipos de Error:**
- Campos obligatorios faltantes
- Formatos de datos inválidos
- Archivos de evidencia corruptos o muy grandes
- Tipos de incidente/delito no válidos

**Estrategias de Manejo:**
- Validación en frontend antes de envío
- Validación en backend con mensajes específicos
- Mostrar errores campo por campo
- Permitir corrección sin perder datos ingresados

### 2. Errores de Permisos y Acceso

**Escenarios:**
- Usuario sin permisos para ver reporte
- Intento de modificar reporte de otro usuario
- Acceso a evidencias sin autorización
- Cambio de estado sin permisos de coordinador

**Estrategias:**
- Verificación de permisos en cada endpoint
- Mensajes de error claros sobre restricciones
- Logging de intentos de acceso no autorizado
- Redirección a página apropiada según rol

### 3. Errores de Conectividad y Sincronización

**Problemas:**
- Pérdida de conexión durante envío de reporte
- Falla en upload de evidencias
- Conflictos de sincronización offline
- Timeout en requests largos

**Estrategias:**
- Almacenamiento local automático
- Reintento automático con backoff exponencial
- Indicadores de estado de sincronización
- Resolución de conflictos con timestamp

### 4. Errores de Almacenamiento de Archivos

**Tipos:**
- Espacio insuficiente en servidor
- Permisos de escritura en directorio
- Archivos corruptos durante upload
- Formatos de imagen no soportados

**Estrategias:**
- Validación de espacio disponible
- Compresión automática de imágenes grandes
- Verificación de integridad de archivos
- Fallback a formatos alternativos

## Testing Strategy

### Unit Tests
- Validar lógica de escalamiento por severidad/gravedad
- Probar cálculos de permisos jerárquicos
- Verificar validaciones de datos de entrada
- Testear generación de notificaciones

### Property-Based Tests
- Generar reportes aleatorios y verificar escalamiento correcto
- Probar integridad de estados con transiciones aleatorias
- Validar permisos con combinaciones de roles y ubicaciones
- Verificar sincronización offline con datos aleatorios

### Integration Tests
- Probar flujo completo de reporte de incidente
- Verificar upload y acceso a evidencias fotográficas
- Testear notificaciones en tiempo real
- Probar exportación de reportes

### Manual Tests
- Verificar interfaz de usuario en dispositivos móviles
- Probar funcionalidad offline en condiciones reales
- Validar flujo de escalamiento con múltiples coordinadores
- Verificar generación de reportes estadísticos

**Configuración de Property Tests:**
- Mínimo 100 iteraciones por propiedad
- Generadores de datos que respeten restricciones del dominio
- Simulación de condiciones de red variables
- Validación de invariantes del sistema en cada ejecución