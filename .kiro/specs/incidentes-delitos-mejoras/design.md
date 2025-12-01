# Design Document: Sistema de Incidentes y Delitos Electorales

## Overview

Este documento describe el diseño técnico para las mejoras del sistema de reporte y gestión de incidentes y delitos electorales. El sistema permitirá a los testigos reportar situaciones con evidencia fotográfica, gestionar el flujo de información a través de la jerarquía organizacional, y mantener un registro completo de auditoría.

### Objetivos del Diseño

1. **Gestión de Evidencia Fotográfica**: Sistema robusto para capturar, almacenar y visualizar fotos
2. **Notificaciones en Tiempo Real**: Alertas inmediatas según jerarquía y severidad
3. **Gestión de Estados**: Flujo de trabajo claro con seguimiento completo
4. **Sincronización Offline**: Operación sin conexión con sincronización automática
5. **Permisos Granulares**: Control de acceso por rol y jurisdicción
6. **Auditoría Completa**: Registro de todas las acciones realizadas

### Principios de Diseño

- **Seguridad First**: Evidencia protegida, permisos estrictos
- **Offline First**: Funcionar sin conexión, sincronizar cuando sea posible
- **Mobile First**: Optimizado para dispositivos móviles
- **Auditable**: Registro completo de todas las acciones
- **Escalable**: Soportar miles de reportes simultáneos

## Architecture

### Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (PWA)                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Reportes   │  │Notificaciones│  │  Seguimiento │     │
│  │   Component  │  │   Component  │  │   Component  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Upload    │  │     Sync     │  │     Mapa     │     │
│  │   Manager    │  │   Manager    │  │   Component  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           IndexedDB (Offline Storage)               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS / WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND (Flask)                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Incidentes  │  │    Delitos   │  │Notificaciones│     │
│  │    Routes    │  │    Routes    │  │    Routes    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Upload    │  │     Sync     │  │  WebSocket   │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              PostgreSQL Database                    │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           File Storage (Local/S3/Azure)             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```


### Flujo de Datos

#### Flujo de Reporte de Incidente/Delito

```
1. Testigo captura foto → 2. Compresión local → 3. Guardar en IndexedDB
                                                          ↓
4. Detectar conexión → 5. Upload foto → 6. Crear reporte → 7. Notificar
                                                          ↓
8. Coordinador recibe notificación → 9. Revisa evidencia → 10. Actualiza estado
                                                          ↓
11. Registrar seguimiento → 12. Notificar testigo → 13. Actualizar mapa
```

#### Flujo de Notificaciones

```
Evento (crear/actualizar reporte)
    ↓
Determinar destinatarios según:
    - Severidad/Gravedad
    - Jerarquía organizacional
    - Jurisdicción
    ↓
Crear registros de notificación en DB
    ↓
Enviar notificación en tiempo real (WebSocket)
    ↓
Mostrar badge y lista en UI
```

## Components and Interfaces

### Frontend Components

#### 1. ReporteFormComponent
**Responsabilidad**: Formulario para crear incidentes/delitos

**Props**:
- `tipo`: 'incidente' | 'delito'
- `mesaId`: number
- `onSubmit`: (data) => void

**State**:
- `formData`: objeto con campos del formulario
- `fotos`: array de archivos
- `uploading`: boolean
- `errors`: objeto con errores de validación

**Métodos**:
- `handleFotoCapture()`: Capturar foto con cámara
- `handleFotoSelect()`: Seleccionar foto de galería
- `compressImage(file)`: Comprimir imagen antes de guardar
- `validateForm()`: Validar campos requeridos
- `submitReporte()`: Enviar reporte (online/offline)

#### 2. NotificacionesComponent
**Responsabilidad**: Panel de notificaciones

**Props**:
- `userId`: number

**State**:
- `notificaciones`: array de notificaciones
- `noLeidas`: number
- `loading`: boolean

**Métodos**:
- `loadNotificaciones()`: Cargar notificaciones del usuario
- `marcarLeida(id)`: Marcar notificación como leída
- `navegarAReporte(id)`: Navegar al detalle del reporte

#### 3. SeguimientoComponent
**Responsabilidad**: Línea de tiempo de seguimiento

**Props**:
- `tipoReporte`: 'incidente' | 'delito'
- `reporteId`: number

**State**:
- `seguimientos`: array de registros
- `loading`: boolean

**Métodos**:
- `loadSeguimiento()`: Cargar historial
- `formatFecha(date)`: Formatear fecha/hora
- `getIconoAccion(accion)`: Obtener icono según acción


#### 4. UploadManager
**Responsabilidad**: Gestionar upload de fotos

**Métodos**:
- `uploadFoto(file, metadata)`: Subir foto al servidor
- `compressImage(file, maxWidth, maxHeight, quality)`: Comprimir imagen
- `extractGPS(file)`: Extraer coordenadas GPS de EXIF
- `generateUniqueFilename(file)`: Generar nombre único
- `retryUpload(file, attempts)`: Reintentar upload si falla

#### 5. SyncManager
**Responsabilidad**: Sincronización offline

**Métodos**:
- `saveReporteLocally(reporte)`: Guardar en IndexedDB
- `getPendingReportes()`: Obtener reportes pendientes
- `syncReporte(reporte)`: Sincronizar un reporte
- `syncAll()`: Sincronizar todos los pendientes
- `onOnline()`: Handler cuando recupera conexión
- `onOffline()`: Handler cuando pierde conexión

### Backend Services

#### 1. UploadService
**Responsabilidad**: Gestionar archivos de evidencia

```python
class UploadService:
    @staticmethod
    def upload_evidencia(file, tipo_reporte, reporte_id, user_id):
        """
        Subir archivo de evidencia
        
        Returns:
            dict: {'url': str, 'filename': str, 'size': int}
        """
        # 1. Validar tipo de archivo (jpg, png, heic)
        # 2. Validar tamaño (max 10MB)
        # 3. Generar nombre único: {timestamp}_{hash}_{original}
        # 4. Comprimir si es necesario
        # 5. Extraer metadatos GPS
        # 6. Guardar en storage
        # 7. Retornar URL
        
    @staticmethod
    def get_evidencia_url(filename):
        """Obtener URL firmada para acceder a evidencia"""
        
    @staticmethod
    def delete_evidencia(filename):
        """Eliminar archivo de evidencia"""
```

#### 2. NotificacionService
**Responsabilidad**: Gestionar notificaciones

```python
class NotificacionService:
    @staticmethod
    def notificar_incidente(incidente):
        """
        Crear notificaciones para un incidente
        
        Lógica:
        - Severidad baja/media: coordinador puesto
        - Severidad alta: coordinador puesto + municipal
        - Severidad crítica: coordinador puesto + municipal + departamental
        """
        
    @staticmethod
    def notificar_delito(delito):
        """
        Crear notificaciones para un delito
        
        Lógica:
        - Siempre: coordinador municipal + departamental + auditores
        """
        
    @staticmethod
    def notificar_cambio_estado(reporte, estado_anterior, estado_nuevo):
        """Notificar al reportante sobre cambio de estado"""
        
    @staticmethod
    def enviar_notificacion_realtime(user_id, notificacion):
        """Enviar notificación por WebSocket"""
```


#### 3. WebSocketService
**Responsabilidad**: Comunicación en tiempo real

```python
from flask_socketio import SocketIO, emit, join_room

class WebSocketService:
    socketio = SocketIO()
    
    @staticmethod
    def init_app(app):
        """Inicializar SocketIO con la app"""
        WebSocketService.socketio.init_app(app, cors_allowed_origins="*")
        
    @staticmethod
    def on_connect(user_id):
        """Usuario se conecta, unirlo a su sala"""
        join_room(f'user_{user_id}')
        
    @staticmethod
    def emit_notificacion(user_id, notificacion):
        """Emitir notificación a un usuario específico"""
        WebSocketService.socketio.emit(
            'nueva_notificacion',
            notificacion,
            room=f'user_{user_id}'
        )
        
    @staticmethod
    def emit_actualizacion_mapa():
        """Emitir actualización global del mapa"""
        WebSocketService.socketio.emit('actualizar_mapa', broadcast=True)
```

## Data Models

### Modificaciones a Modelos Existentes

#### IncidenteElectoral (modificaciones)

```python
class IncidenteElectoral(db.Model):
    # ... campos existentes ...
    
    # NUEVO: Soporte para múltiples fotos
    evidencias = db.relationship('EvidenciaFotografica', backref='incidente', lazy=True)
    
    # NUEVO: Metadatos de geolocalización
    latitud_reporte = db.Column(db.Float, nullable=True)
    longitud_reporte = db.Column(db.Float, nullable=True)
    precision_gps = db.Column(db.Float, nullable=True)  # en metros
    
    # NUEVO: Sincronización offline
    sincronizado = db.Column(db.Boolean, default=True)
    fecha_sincronizacion = db.Column(db.DateTime, nullable=True)
    dispositivo_id = db.Column(db.String(100), nullable=True)
```

#### DelitoElectoral (modificaciones)

```python
class DelitoElectoral(db.Model):
    # ... campos existentes ...
    
    # NUEVO: Soporte para múltiples fotos
    evidencias = db.relationship('EvidenciaFotografica', backref='delito', lazy=True)
    
    # NUEVO: Metadatos de geolocalización
    latitud_reporte = db.Column(db.Float, nullable=True)
    longitud_reporte = db.Column(db.Float, nullable=True)
    precision_gps = db.Column(db.Float, nullable=True)
    
    # NUEVO: Sincronización offline
    sincronizado = db.Column(db.Boolean, default=True)
    fecha_sincronizacion = db.Column(db.DateTime, nullable=True)
    dispositivo_id = db.Column(db.String(100), nullable=True)
```

### Nuevos Modelos

#### EvidenciaFotografica

```python
class EvidenciaFotografica(db.Model):
    """Modelo para evidencia fotográfica"""
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
    
    # Metadatos de la foto
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    latitud = db.Column(db.Float, nullable=True)
    longitud = db.Column(db.Float, nullable=True)
    fecha_captura = db.Column(db.DateTime, nullable=True)
    dispositivo = db.Column(db.String(200), nullable=True)
    
    # Auditoría
    subido_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    subido_por = db.relationship('User', backref='evidencias_subidas')
```


#### ConfiguracionNotificaciones

```python
class ConfiguracionNotificaciones(db.Model):
    """Configuración de notificaciones por usuario"""
    __tablename__ = 'configuracion_notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Preferencias de notificación
    notificar_incidentes_baja = db.Column(db.Boolean, default=True)
    notificar_incidentes_media = db.Column(db.Boolean, default=True)
    notificar_incidentes_alta = db.Column(db.Boolean, default=True)
    notificar_incidentes_critica = db.Column(db.Boolean, default=True)
    notificar_delitos = db.Column(db.Boolean, default=True)
    notificar_cambios_estado = db.Column(db.Boolean, default=True)
    
    # Canales de notificación
    notificar_web = db.Column(db.Boolean, default=True)
    notificar_email = db.Column(db.Boolean, default=False)
    notificar_sms = db.Column(db.Boolean, default=False)
    
    # Relaciones
    usuario = db.relationship('User', backref='config_notificaciones')
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Estado inicial de reportes
*For any* incidente o delito creado por un testigo, el estado inicial debe ser "reportado" y debe estar asociado a la mesa del testigo.
**Validates: Requirements 1.4, 2.2**

### Property 2: Notificación a coordinador de puesto
*For any* incidente creado, debe existir al menos una notificación para el coordinador de puesto correspondiente.
**Validates: Requirements 1.5**

### Property 3: Notificación por severidad crítica
*For any* incidente con severidad "crítica", deben existir notificaciones para coordinador de puesto, coordinador municipal y coordinador departamental.
**Validates: Requirements 1.6, 4.3**

### Property 4: Notificación de delitos
*For any* delito creado, deben existir notificaciones para coordinador municipal, coordinador departamental y todos los auditores electorales.
**Validates: Requirements 2.3, 4.4**

### Property 5: Unicidad de nombres de archivo
*For any* par de fotos subidas, los nombres de archivo generados deben ser únicos.
**Validates: Requirements 3.2**

### Property 6: Compresión de imágenes
*For any* imagen subida, el tamaño del archivo comprimido debe ser menor o igual al original.
**Validates: Requirements 3.1**

### Property 7: Metadatos GPS en evidencia
*For any* foto capturada con GPS disponible, los metadatos de la evidencia deben incluir latitud y longitud.
**Validates: Requirements 1.3**

### Property 8: Validación de descripción obligatoria
*For any* intento de crear un reporte sin descripción, el sistema debe rechazarlo con un error específico.
**Validates: Requirements 1.8**

### Property 9: Permisos de visualización por rol
*For any* testigo electoral, solo debe poder ver los reportes que él mismo creó.
**Validates: Requirements 8.1, 8.2**

### Property 10: Permisos de visualización por jurisdicción
*For any* coordinador de puesto, solo debe poder ver reportes de su puesto asignado.
**Validates: Requirements 8.3**

### Property 11: Registro de seguimiento en creación
*For any* reporte creado, debe existir un registro de seguimiento inicial con acción "crear".
**Validates: Requirements 2.4, 7.4**

### Property 12: Registro de seguimiento en cambio de estado
*For any* cambio de estado de un reporte, debe crearse un registro de seguimiento con estado anterior y nuevo.
**Validates: Requirements 5.5, 6.3, 7.5**

### Property 13: Notificación al reportante
*For any* cambio de estado de un reporte, debe crearse una notificación para el usuario que lo reportó.
**Validates: Requirements 4.5**

### Property 14: Permisos para cambiar estado de incidentes
*For any* testigo electoral que intente cambiar el estado de un incidente, el sistema debe denegar la acción.
**Validates: Requirements 5.6**

### Property 15: Permisos para denuncia formal
*For any* usuario que no sea auditor o super_admin que intente denunciar formalmente un delito, el sistema debe denegar la acción.
**Validates: Requirements 6.6**

### Property 16: Campos obligatorios en resolución
*For any* incidente marcado como "resuelto", debe tener notas de resolución, fecha de resolución y usuario que resolvió.
**Validates: Requirements 5.3, 5.7**

### Property 17: Campos obligatorios en denuncia
*For any* delito marcado como "denunciado", debe tener número de denuncia, autoridad competente y fecha de denuncia.
**Validates: Requirements 6.4, 6.5, 6.7**

### Property 18: Sincronización offline
*For any* reporte guardado localmente, cuando el dispositivo recupere conexión, el reporte debe sincronizarse automáticamente.
**Validates: Requirements 1.7, 10.3**

### Property 19: Indicadores visuales en mapa
*For any* puesto con incidentes activos, el mapa debe mostrar un indicador de alerta.
**Validates: Requirements 9.1, 9.2, 9.3**

### Property 20: Remoción de indicadores
*For any* puesto donde se resuelve el último incidente activo, el indicador de alerta debe removerse del mapa.
**Validates: Requirements 9.6, 9.7**


## Error Handling

### Estrategias de Manejo de Errores

#### 1. Upload de Fotos

**Errores Posibles**:
- Archivo demasiado grande (> 10MB)
- Tipo de archivo no soportado
- Error de red durante upload
- Espacio de almacenamiento lleno

**Manejo**:
```python
try:
    # Validar tamaño
    if file.size > 10 * 1024 * 1024:
        raise ValueError('Archivo demasiado grande. Máximo 10MB')
    
    # Validar tipo
    if file.mimetype not in ['image/jpeg', 'image/png', 'image/heic']:
        raise ValueError('Tipo de archivo no soportado')
    
    # Intentar upload
    url = storage.upload(file)
    
except ValueError as e:
    return {'success': False, 'error': str(e)}, 400
except StorageError as e:
    # Guardar localmente para reintentar
    save_for_retry(file)
    return {'success': False, 'error': 'Error de almacenamiento'}, 500
except Exception as e:
    log.error(f'Error inesperado en upload: {e}')
    return {'success': False, 'error': 'Error interno'}, 500
```

#### 2. Sincronización Offline

**Errores Posibles**:
- Conflicto de datos (reporte modificado en servidor)
- Token expirado
- Datos corruptos en IndexedDB

**Manejo**:
```javascript
async function syncReporte(reporte) {
    try {
        const response = await api.crearReporte(reporte);
        
        if (response.success) {
            // Marcar como sincronizado
            await db.delete('reportes_pendientes', reporte.id);
            return { success: true };
        }
    } catch (error) {
        if (error.status === 401) {
            // Token expirado, renovar y reintentar
            await refreshToken();
            return syncReporte(reporte);
        } else if (error.status === 409) {
            // Conflicto, resolver manualmente
            return { success: false, conflict: true, data: error.data };
        } else {
            // Otro error, reintentar más tarde
            return { success: false, retry: true };
        }
    }
}
```

#### 3. Notificaciones en Tiempo Real

**Errores Posibles**:
- Conexión WebSocket perdida
- Usuario no conectado
- Error al enviar notificación

**Manejo**:
```python
def enviar_notificacion_realtime(user_id, notificacion):
    try:
        # Intentar enviar por WebSocket
        socketio.emit('nueva_notificacion', notificacion, room=f'user_{user_id}')
        
    except Exception as e:
        # Si falla, la notificación ya está en DB
        # El usuario la verá cuando recargue
        log.warning(f'No se pudo enviar notificación en tiempo real a user {user_id}: {e}')
        
        # Opcional: enviar por email si está configurado
        if user.config_notificaciones.notificar_email:
            send_email_notification(user.email, notificacion)
```

## Testing Strategy

### Unit Testing

**Componentes a Testear**:

1. **UploadService**
   - Test: validación de tipo de archivo
   - Test: validación de tamaño
   - Test: generación de nombre único
   - Test: compresión de imagen
   - Test: extracción de metadatos GPS

2. **NotificacionService**
   - Test: notificaciones según severidad
   - Test: notificaciones según gravedad
   - Test: notificaciones a jerarquía correcta
   - Test: no duplicar notificaciones

3. **Permisos**
   - Test: testigo solo ve sus reportes
   - Test: coordinador ve reportes de su jurisdicción
   - Test: auditor ve todos los reportes
   - Test: denegación de acceso fuera de jurisdicción

4. **SyncManager**
   - Test: guardar reporte localmente
   - Test: sincronizar cuando hay conexión
   - Test: manejar conflictos
   - Test: reintentar en caso de error

### Property-Based Testing

Se utilizará **Hypothesis** (Python) y **fast-check** (JavaScript) para property-based testing.

**Configuración**:
- Mínimo 100 iteraciones por propiedad
- Generadores personalizados para datos del dominio
- Shrinking automático para encontrar casos mínimos

**Propiedades a Testear**:

1. **Property 1: Estado inicial de reportes**
   ```python
   @given(testigo=usuarios_testigo(), reporte_data=reportes_validos())
   def test_estado_inicial_reportado(testigo, reporte_data):
       incidente = crear_incidente(reporte_data, testigo.id)
       assert incidente.estado == 'reportado'
       assert incidente.mesa_id == testigo.ubicacion_id
   ```

2. **Property 5: Unicidad de nombres de archivo**
   ```python
   @given(fotos=st.lists(archivos_imagen(), min_size=2, max_size=10))
   def test_nombres_unicos(fotos):
       nombres = [generar_nombre_unico(foto) for foto in fotos]
       assert len(nombres) == len(set(nombres))  # Todos únicos
   ```

3. **Property 9: Permisos de visualización**
   ```python
   @given(testigo=usuarios_testigo(), otros_reportes=st.lists(reportes()))
   def test_testigo_solo_ve_sus_reportes(testigo, otros_reportes):
       reportes_visibles = obtener_incidentes(testigo.id, testigo.rol)
       assert all(r.reportado_por_id == testigo.id for r in reportes_visibles)
   ```

### Integration Testing

**Escenarios a Testear**:

1. **Flujo completo de reporte**
   - Testigo crea incidente con foto
   - Foto se sube correctamente
   - Notificaciones se crean
   - Coordinador recibe notificación
   - Coordinador actualiza estado
   - Testigo recibe notificación de cambio

2. **Sincronización offline**
   - Crear reporte sin conexión
   - Verificar guardado en IndexedDB
   - Simular recuperación de conexión
   - Verificar sincronización automática
   - Verificar reporte en servidor

3. **Permisos y seguridad**
   - Intentar acceder a reporte fuera de jurisdicción
   - Verificar denegación de acceso
   - Intentar cambiar estado sin permisos
   - Verificar denegación de acción


## Implementation Details

### 1. Upload de Fotos

#### Backend Endpoint

```python
@incidentes_delitos_bp.route('/api/evidencia/upload', methods=['POST'])
@jwt_required()
def upload_evidencia():
    """Upload de evidencia fotográfica"""
    try:
        user_id = get_jwt_identity()
        
        # Validar archivo
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        tipo_reporte = request.form.get('tipo_reporte')  # 'incidente' o 'delito'
        reporte_id = request.form.get('reporte_id')
        
        # Upload
        result = UploadService.upload_evidencia(file, tipo_reporte, reporte_id, user_id)
        
        return jsonify({'success': True, 'data': result}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

#### Frontend Upload

```javascript
async function uploadFoto(file, tipoReporte, reporteId) {
    // Comprimir imagen
    const compressed = await compressImage(file, 1920, 1080, 0.8);
    
    // Crear FormData
    const formData = new FormData();
    formData.append('file', compressed);
    formData.append('tipo_reporte', tipoReporte);
    formData.append('reporte_id', reporteId);
    
    // Upload
    const response = await fetch('/api/evidencia/upload', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${getToken()}`
        },
        body: formData
    });
    
    return await response.json();
}

function compressImage(file, maxWidth, maxHeight, quality) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                let width = img.width;
                let height = img.height;
                
                // Calcular nuevas dimensiones
                if (width > maxWidth) {
                    height = (height * maxWidth) / width;
                    width = maxWidth;
                }
                if (height > maxHeight) {
                    width = (width * maxHeight) / height;
                    height = maxHeight;
                }
                
                canvas.width = width;
                canvas.height = height;
                
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                
                canvas.toBlob((blob) => {
                    resolve(new File([blob], file.name, {
                        type: 'image/jpeg',
                        lastModified: Date.now()
                    }));
                }, 'image/jpeg', quality);
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    });
}
```

### 2. Notificaciones en Tiempo Real

#### Backend WebSocket

```python
from flask_socketio import SocketIO, emit, join_room, leave_room

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    """Usuario se conecta"""
    user_id = get_jwt_identity()
    if user_id:
        join_room(f'user_{user_id}')
        emit('connected', {'message': 'Conectado exitosamente'})

@socketio.on('disconnect')
def handle_disconnect():
    """Usuario se desconecta"""
    user_id = get_jwt_identity()
    if user_id:
        leave_room(f'user_{user_id}')

def enviar_notificacion_realtime(user_id, notificacion):
    """Enviar notificación a un usuario"""
    socketio.emit('nueva_notificacion', notificacion.to_dict(), room=f'user_{user_id}')
```

#### Frontend WebSocket Client

```javascript
class NotificacionesManager {
    constructor() {
        this.socket = null;
        this.notificaciones = [];
        this.callbacks = [];
    }
    
    connect() {
        this.socket = io({
            auth: {
                token: getToken()
            }
        });
        
        this.socket.on('connect', () => {
            console.log('Conectado a notificaciones en tiempo real');
        });
        
        this.socket.on('nueva_notificacion', (notificacion) => {
            this.handleNuevaNotificacion(notificacion);
        });
        
        this.socket.on('disconnect', () => {
            console.log('Desconectado de notificaciones');
        });
    }
    
    handleNuevaNotificacion(notificacion) {
        // Agregar a lista
        this.notificaciones.unshift(notificacion);
        
        // Actualizar badge
        this.actualizarBadge();
        
        // Mostrar toast
        this.mostrarToast(notificacion);
        
        // Notificar a callbacks
        this.callbacks.forEach(cb => cb(notificacion));
    }
    
    actualizarBadge() {
        const noLeidas = this.notificaciones.filter(n => !n.leida).length;
        const badge = document.getElementById('notificaciones-badge');
        if (badge) {
            badge.textContent = noLeidas;
            badge.style.display = noLeidas > 0 ? 'inline' : 'none';
        }
    }
    
    mostrarToast(notificacion) {
        // Usar biblioteca de toasts (ej: Toastify)
        Toastify({
            text: notificacion.titulo,
            duration: 5000,
            gravity: "top",
            position: "right",
            backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
            onClick: () => {
                window.location.href = `/reportes/${notificacion.reporte_id}`;
            }
        }).showToast();
    }
    
    onNuevaNotificacion(callback) {
        this.callbacks.push(callback);
    }
}

// Inicializar
const notificacionesManager = new NotificacionesManager();
notificacionesManager.connect();
```

### 3. Sincronización Offline

#### IndexedDB Schema

```javascript
const DB_NAME = 'electoral-db';
const DB_VERSION = 1;

async function initDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            
            // Store para reportes pendientes
            if (!db.objectStoreNames.contains('reportes_pendientes')) {
                const store = db.createObjectStore('reportes_pendientes', { 
                    keyPath: 'id', 
                    autoIncrement: true 
                });
                store.createIndex('tipo', 'tipo', { unique: false });
                store.createIndex('fecha', 'fecha_creacion', { unique: false });
            }
            
            // Store para fotos pendientes
            if (!db.objectStoreNames.contains('fotos_pendientes')) {
                const store = db.createObjectStore('fotos_pendientes', { 
                    keyPath: 'id', 
                    autoIncrement: true 
                });
                store.createIndex('reporte_id', 'reporte_id', { unique: false });
            }
        };
    });
}
```

#### Sync Manager

```javascript
class SyncManager {
    constructor() {
        this.db = null;
        this.syncing = false;
        this.syncInterval = null;
    }
    
    async init() {
        this.db = await initDB();
        
        // Escuchar eventos de conexión
        window.addEventListener('online', () => this.onOnline());
        window.addEventListener('offline', () => this.onOffline());
        
        // Si ya está online, iniciar sync
        if (navigator.onLine) {
            this.startAutoSync();
        }
    }
    
    async saveReporteLocally(reporte) {
        const tx = this.db.transaction(['reportes_pendientes'], 'readwrite');
        const store = tx.objectStore('reportes_pendientes');
        
        reporte.fecha_creacion = new Date();
        reporte.sincronizado = false;
        
        await store.add(reporte);
        
        // Actualizar UI
        this.updatePendingBadge();
    }
    
    async getPendingReportes() {
        const tx = this.db.transaction(['reportes_pendientes'], 'readonly');
        const store = tx.objectStore('reportes_pendientes');
        
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    async syncAll() {
        if (this.syncing) return;
        
        this.syncing = true;
        const pendientes = await this.getPendingReportes();
        
        for (const reporte of pendientes) {
            try {
                await this.syncReporte(reporte);
            } catch (error) {
                console.error('Error sincronizando reporte:', error);
            }
        }
        
        this.syncing = false;
        this.updatePendingBadge();
    }
    
    async syncReporte(reporte) {
        // Crear reporte en servidor
        const response = await APIClient.crearReporte(reporte);
        
        if (response.success) {
            // Eliminar de IndexedDB
            const tx = this.db.transaction(['reportes_pendientes'], 'readwrite');
            const store = tx.objectStore('reportes_pendientes');
            await store.delete(reporte.id);
            
            // Mostrar notificación
            Utils.showSuccess('✓ Reporte sincronizado');
        }
    }
    
    onOnline() {
        console.log('Conexión recuperada, iniciando sincronización...');
        this.startAutoSync();
        this.syncAll();
    }
    
    onOffline() {
        console.log('Conexión perdida, deteniendo sincronización automática');
        this.stopAutoSync();
    }
    
    startAutoSync() {
        if (this.syncInterval) return;
        
        this.syncInterval = setInterval(() => {
            this.syncAll();
        }, 60000); // Cada minuto
    }
    
    stopAutoSync() {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
            this.syncInterval = null;
        }
    }
    
    async updatePendingBadge() {
        const pendientes = await this.getPendingReportes();
        const badge = document.getElementById('sync-pending-badge');
        if (badge) {
            badge.textContent = pendientes.length;
            badge.style.display = pendientes.length > 0 ? 'inline' : 'none';
        }
    }
}

// Inicializar
const syncManager = new SyncManager();
syncManager.init();
```

## Security Considerations

### 1. Protección de Evidencia Fotográfica

- **Almacenamiento**: Archivos en directorio con permisos restringidos (solo lectura para web server)
- **URLs Firmadas**: Generar URLs temporales con expiración (ej: 1 hora)
- **Validación**: Verificar permisos antes de servir archivos
- **Encriptación**: Considerar encriptar archivos en reposo para datos sensibles

### 2. Control de Acceso

- **JWT**: Tokens con expiración corta (15 minutos) y refresh tokens
- **Permisos por Rol**: Validar en backend, nunca confiar en frontend
- **Jurisdicción**: Filtrar datos según ubicación del usuario
- **Auditoría**: Registrar todos los accesos a reportes sensibles

### 3. Validación de Datos

- **Input Sanitization**: Limpiar todos los inputs del usuario
- **SQL Injection**: Usar ORM (SQLAlchemy) con parámetros preparados
- **XSS**: Escapar HTML en outputs
- **CSRF**: Tokens CSRF en formularios

### 4. Rate Limiting

- **Upload**: Máximo 10 fotos por minuto por usuario
- **Reportes**: Máximo 5 reportes por hora por usuario
- **API**: Límite general de 100 requests por minuto

## Performance Optimization

### 1. Compresión de Imágenes

- **Cliente**: Comprimir antes de subir (reduce tiempo de upload)
- **Servidor**: Generar thumbnails para listados
- **Lazy Loading**: Cargar imágenes solo cuando sean visibles

### 2. Caching

- **Notificaciones**: Cache en memoria con TTL de 5 minutos
- **Estadísticas**: Cache de 15 minutos
- **Evidencia**: Cache de CDN con headers apropiados

### 3. Paginación

- **Reportes**: Máximo 20 por página
- **Notificaciones**: Máximo 50 por carga
- **Seguimiento**: Cargar bajo demanda

### 4. Índices de Base de Datos

```sql
-- Índices para mejorar queries frecuentes
CREATE INDEX idx_incidentes_estado ON incidentes_electorales(estado);
CREATE INDEX idx_incidentes_severidad ON incidentes_electorales(severidad);
CREATE INDEX idx_incidentes_puesto ON incidentes_electorales(puesto_id);
CREATE INDEX idx_incidentes_fecha ON incidentes_electorales(fecha_reporte);

CREATE INDEX idx_delitos_estado ON delitos_electorales(estado);
CREATE INDEX idx_delitos_gravedad ON delitos_electorales(gravedad);
CREATE INDEX idx_delitos_municipio ON delitos_electorales(municipio_id);

CREATE INDEX idx_notificaciones_usuario ON notificaciones_reportes(usuario_id, leida);
CREATE INDEX idx_seguimiento_reporte ON seguimiento_reportes(tipo_reporte, reporte_id);
```

## Deployment Considerations

### 1. Variables de Entorno

```bash
# Storage
UPLOAD_FOLDER=/var/www/electoral/uploads
MAX_UPLOAD_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,heic

# WebSocket
SOCKETIO_MESSAGE_QUEUE=redis://localhost:6379/0
SOCKETIO_CORS_ALLOWED_ORIGINS=*

# Notificaciones
ENABLE_EMAIL_NOTIFICATIONS=true
ENABLE_SMS_NOTIFICATIONS=false
```

### 2. Escalabilidad

- **Load Balancer**: Nginx para distribuir carga
- **WebSocket**: Usar Redis como message queue para múltiples workers
- **Storage**: Considerar S3/Azure Blob para almacenamiento escalable
- **Database**: Read replicas para queries pesadas

### 3. Monitoreo

- **Logs**: Centralizar con ELK stack o similar
- **Métricas**: Prometheus + Grafana
- **Alertas**: Notificar si tasa de error > 5%
- **Health Checks**: Endpoints para verificar estado del sistema

