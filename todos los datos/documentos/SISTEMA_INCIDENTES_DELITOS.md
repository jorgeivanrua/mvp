# Sistema de Incidentes y Delitos Electorales

## ✅ Implementación Completada

Se ha implementado un sistema completo de gestión de incidentes y delitos electorales con persistencia en base de datos.

## 📋 Componentes Implementados

### 1. Base de Datos
**Archivo**: `backend/migrations/create_incidentes_delitos_tables.py`

Tablas creadas:
- `incidentes_electorales`: Registro de incidentes durante el proceso electoral
- `delitos_electorales`: Registro de delitos electorales
- `seguimiento_reportes`: Historial de acciones sobre incidentes/delitos
- `notificaciones_reportes`: Sistema de notificaciones para usuarios

Índices optimizados para:
- Búsquedas por usuario reportador
- Filtros por ubicación (mesa, puesto, municipio, departamento)
- Filtros por estado y severidad/gravedad
- Ordenamiento por fecha

### 2. Modelos de Datos
**Archivo**: `backend/models/incidentes_delitos.py`

#### IncidenteElectoral
- Tipos: retraso_apertura, falta_material, problemas_tecnicos, irregularidades_proceso, ausencia_funcionarios, problemas_acceso, disturbios, otros
- Severidades: baja, media, alta, critica
- Estados: reportado, en_revision, resuelto, escalado
- Relaciones con usuarios y ubicaciones

#### DelitoElectoral
- Tipos: compra_votos, coaccion_votante, fraude_electoral, suplantacion_identidad, alteracion_resultados, violencia_electoral, propaganda_ilegal, financiacion_ilegal, otros_delitos
- Gravedades: leve, media, grave, muy_grave
- Estados: reportado, en_investigacion, investigado, denunciado, archivado
- Soporte para denuncia formal con número y autoridad competente

#### SeguimientoReporte
- Registro de todas las acciones realizadas sobre un reporte
- Incluye usuario, acción, comentario y cambios de estado

#### NotificacionReporte
- Sistema de notificaciones para usuarios
- Marca de leído/no leído
- Tipos de notificación personalizables

### 3. Servicio de Negocio
**Archivo**: `backend/services/incidentes_delitos_service.py`

Funcionalidades implementadas:

#### Creación de Reportes
- `crear_incidente()`: Crea un incidente con ubicaciones automáticas
- `crear_delito()`: Crea un delito con notificaciones a coordinadores y auditores

#### Consulta de Reportes
- `obtener_incidentes()`: Lista incidentes según permisos del usuario
- `obtener_delitos()`: Lista delitos según permisos del usuario
- Filtros por: estado, severidad/gravedad, tipo, rango de fechas

#### Gestión de Estados
- `actualizar_estado_incidente()`: Cambia estado de incidente
- `actualizar_estado_delito()`: Cambia estado de delito
- `denunciar_formalmente()`: Marca delito como denunciado formalmente

#### Estadísticas
- `obtener_estadisticas()`: Resumen de incidentes y delitos por estado y severidad/gravedad

#### Seguimiento y Notificaciones
- `obtener_seguimiento()`: Historial de acciones sobre un reporte
- `obtener_notificaciones()`: Notificaciones del usuario
- `marcar_notificacion_leida()`: Marca notificación como leída

### 4. API REST
**Archivo**: `backend/routes/incidentes_delitos.py`

Endpoints implementados:

#### Incidentes
- `POST /api/incidentes` - Crear incidente
- `GET /api/incidentes` - Listar incidentes (con filtros)
- `GET /api/incidentes/<id>` - Detalle de incidente
- `PUT /api/incidentes/<id>/estado` - Actualizar estado
- `GET /api/incidentes/tipos` - Tipos de incidentes disponibles

#### Delitos
- `POST /api/delitos` - Crear delito
- `GET /api/delitos` - Listar delitos (con filtros)
- `GET /api/delitos/<id>` - Detalle de delito
- `PUT /api/delitos/<id>/estado` - Actualizar estado
- `POST /api/delitos/<id>/denunciar` - Denunciar formalmente
- `GET /api/delitos/tipos` - Tipos de delitos disponibles

#### Estadísticas y Notificaciones
- `GET /api/reportes/estadisticas` - Estadísticas generales
- `GET /api/notificaciones` - Notificaciones del usuario
- `PUT /api/notificaciones/<id>/leer` - Marcar como leída

## 🔐 Control de Permisos por Rol

### Testigo Electoral
- ✅ Puede reportar incidentes y delitos
- ✅ Solo ve sus propios reportes
- ❌ No puede cambiar estados

### Coordinador de Puesto
- ✅ Ve incidentes/delitos de su puesto
- ✅ Puede cambiar estados
- ✅ Recibe notificaciones de nuevos reportes

### Coordinador Municipal
- ✅ Ve incidentes/delitos de su municipio
- ✅ Puede cambiar estados
- ✅ Recibe notificaciones de incidentes críticos

### Coordinador Departamental
- ✅ Ve incidentes/delitos de su departamento
- ✅ Puede cambiar estados
- ✅ Recibe notificaciones de incidentes críticos

### Auditor Electoral
- ✅ Ve todos los incidentes y delitos
- ✅ Puede cambiar estados
- ✅ Puede denunciar formalmente delitos
- ✅ Recibe notificaciones de todos los delitos

### Super Admin
- ✅ Acceso completo a todo el sistema
- ✅ Puede denunciar formalmente delitos

## 📊 Sistema de Notificaciones

### Notificaciones Automáticas

#### Para Incidentes:
- Coordinador de puesto recibe notificación de nuevos incidentes
- Si severidad es alta/crítica: también notifica a coordinadores municipales

#### Para Delitos:
- Notifica a coordinadores de puesto, municipal y departamental
- Notifica a todos los auditores electorales
- Prioridad alta por la naturaleza del reporte

## 🧪 Pruebas

**Archivo**: `backend/scripts/test_incidentes_delitos.py`

Script de prueba que valida:
- ✅ Creación de incidentes
- ✅ Creación de delitos
- ✅ Consulta de reportes
- ✅ Actualización de estados
- ✅ Seguimiento de acciones
- ✅ Sistema de notificaciones
- ✅ Estadísticas

## 🚀 Próximos Pasos

Para completar la implementación del frontend:

1. **Dashboard de Testigos**: Agregar tabs para reportar incidentes/delitos
2. **Dashboard de Coordinadores**: Agregar sección para ver y gestionar reportes
3. **Dashboard de Auditores**: Panel completo con opción de denuncia formal
4. **Formularios de Reporte**: Interfaces para crear incidentes y delitos
5. **Vista de Detalle**: Modal o página para ver detalles completos
6. **Sistema de Notificaciones**: Badge con contador y lista de notificaciones

## 📝 Ejemplo de Uso

```python
# Crear un incidente
data_incidente = {
    'mesa_id': 123,
    'tipo_incidente': 'falta_material',
    'titulo': 'Falta de boletas',
    'descripcion': 'No hay suficientes boletas',
    'severidad': 'alta',
    'ubicacion_gps': '-1.234,-78.123'
}
incidente = IncidentesDelitosService.crear_incidente(data_incidente, usuario_id)

# Crear un delito
data_delito = {
    'mesa_id': 123,
    'tipo_delito': 'compra_votos',
    'titulo': 'Intento de compra de votos',
    'descripcion': 'Se observó ofrecimiento de dinero',
    'gravedad': 'grave',
    'testigos_adicionales': 'Juan Pérez, María González'
}
delito = IncidentesDelitosService.crear_delito(data_delito, usuario_id)

# Actualizar estado
IncidentesDelitosService.actualizar_estado_incidente(
    incidente_id, 'en_revision', coordinador_id, 
    'Revisando el incidente'
)

# Denunciar formalmente
IncidentesDelitosService.denunciar_formalmente(
    delito_id, auditor_id, 
    'DEN-2024-001', 'Fiscalía Electoral'
)
```

## ✅ Estado del Sistema

- ✅ Base de datos creada y migrada
- ✅ Modelos implementados y probados
- ✅ Servicio de negocio completo
- ✅ API REST funcional
- ✅ Control de permisos por rol
- ✅ Sistema de notificaciones
- ✅ Seguimiento de acciones
- ✅ Pruebas exitosas
- ⏳ Frontend pendiente

El backend está 100% funcional y listo para ser consumido por el frontend.
