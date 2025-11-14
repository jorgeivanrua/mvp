# Design Document - Dashboard Super Admin

## Overview

El Dashboard del Super Admin es la interfaz de administración de más alto nivel del sistema electoral. Proporciona acceso completo a todos los datos, configuraciones y funcionalidades del sistema sin restricciones geográficas. Está diseñado para supervisión, gestión y control total del sistema a nivel nacional.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Super Admin Dashboard                           │
│                                                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  Vista   │ │ Usuarios │ │  Config  │ │ Monitoreo│           │
│  │ General  │ │          │ │          │ │          │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                   │
│  ┌──────────┐ ┌──────────┐                                      │
│  │Auditoría │ │Incidentes│                                      │
│  │          │ │          │                                      │
│  └──────────┘ └──────────┘                                      │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │              Sync Manager (Universal)                   │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Backend                                 │
│                                                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  Users   │ │ Partidos │ │Candidatos│ │  Stats   │           │
│  │  CRUD    │ │  Config  │ │  Config  │ │  Global  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│  │  Audit   │ │ Backups  │ │  Health  │                        │
│  │   Logs   │ │          │ │  Check   │                        │
│  └──────────┘ └──────────┘ └──────────┘                        │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │              Database (PostgreSQL)                      │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Vista General (Overview Tab)

**Componentes:**
- Estadísticas principales (4 cards):
  - Usuarios activos
  - Puestos electorales
  - Formularios E-14
  - Formularios validados
- Gráfico de progreso nacional por departamento
- Gráfico de actividad del sistema (últimas 24h)
- Panel de acciones rápidas
- Panel de actividad reciente

**Interacciones:**
- Auto-refresh cada 30 segundos
- Click en estadística navega a tab correspondiente
- Acciones rápidas abren modales o ejecutan acciones

### 2. Gestión de Usuarios (Users Tab)

**Componentes:**
- Tabla de usuarios con paginación
- Filtros por rol y estado
- Búsqueda por nombre
- Botón "Nuevo Usuario"
- Acciones por usuario (editar, resetear password, activar/desactivar)

**Interacciones:**
- Filtros actualizan tabla en tiempo real
- Click en editar abre modal con datos del usuario
- Resetear password genera nueva contraseña
- Activar/desactivar cambia estado inmediatamente

### 3. Configuración (Config Tab)

**Componentes:**
- Panel de partidos políticos
- Panel de tipos de elección
- Tabla de candidatos
- Botones para crear nuevos registros

**Interacciones:**
- Click en editar abre modal con datos
- Cambios se aplican inmediatamente
- Validación de códigos únicos

### 4. Monitoreo (Monitoring Tab)

**Componentes:**
- Métricas en tiempo real:
  - Usuarios conectados
  - Requests por minuto
  - Tiempo de respuesta promedio
- Gráfico de métricas del sistema
- Tabla de sesiones activas
- Indicador de salud del sistema

**Interacciones:**
- Auto-refresh cada 10 segundos
- Click en sesión permite cerrarla
- Indicador de salud cambia color según estado

### 5. Auditoría (Audit Tab)

**Componentes:**
- Tabla de logs de auditoría
- Filtros por usuario, acción, fecha
- Botón de exportación
- Paginación

**Interacciones:**
- Filtros actualizan logs
- Exportación genera CSV/JSON
- Click en log muestra detalles

### 6. Incidentes (Incidents Tab)

**Componentes:**
- Sub-tabs para incidentes y delitos
- Lista de incidentes con filtros
- Lista de delitos con filtros
- Gráfico de estadísticas
- Acciones de gestión

**Interacciones:**
- Filtros por estado, severidad, fecha
- Click en incidente/delito muestra detalles
- Acciones de actualización de estado

## Data Models

### User (Backend)

```python
class User(db.Model):
    id: int
    nombre: str
    password_hash: str
    rol: str  # super_admin, coordinador_*, testigo_electoral, auditor_electoral
    ubicacion_id: int | None
    activo: bool
    ultimo_acceso: datetime | None
    intentos_fallidos: int
    bloqueado_hasta: datetime | None
    presencia_verificada: bool
    presencia_verificada_at: datetime | None
    created_at: datetime
    updated_at: datetime
```

### SystemStats (API Response)

```javascript
{
  totalUsuarios: number,
  usuariosChange: number,
  totalPuestos: number,
  totalMesas: number,
  totalFormularios: number,
  formulariosPendientes: number,
  totalValidados: number,
  porcentajeValidados: number
}
```

### SystemHealth (API Response)

```javascript
{
  status: "healthy" | "warning" | "critical",
  database: "healthy" | "unhealthy",
  cpu_percent: number,
  memory_percent: number,
  memory_available_mb: number,
  timestamp: number
}
```

## API Endpoints

### Super Admin Endpoints

```
GET    /api/super-admin/stats                    - Estadísticas globales
GET    /api/super-admin/users                    - Listar todos los usuarios
POST   /api/super-admin/users                    - Crear usuario
PUT    /api/super-admin/users/<id>               - Actualizar usuario
POST   /api/super-admin/users/<id>/reset-password - Resetear contraseña
GET    /api/super-admin/system-health            - Estado de salud del sistema
GET    /api/super-admin/audit-logs               - Logs de auditoría (TODO)
GET    /api/super-admin/active-sessions          - Sesiones activas (TODO)
POST   /api/super-admin/backup                   - Crear respaldo (TODO)
GET    /api/super-admin/backups                  - Listar respaldos (TODO)
POST   /api/super-admin/export                   - Exportar datos (TODO)
```

### Endpoints Compartidos

```
GET    /api/configuracion/partidos               - Listar partidos
POST   /api/configuracion/partidos               - Crear partido (TODO)
PUT    /api/configuracion/partidos/<id>          - Actualizar partido (TODO)

GET    /api/configuracion/candidatos             - Listar candidatos
POST   /api/configuracion/candidatos             - Crear candidato (TODO)
PUT    /api/configuracion/candidatos/<id>        - Actualizar candidato (TODO)

GET    /api/configuracion/tipos-eleccion         - Listar tipos de elección
POST   /api/configuracion/tipos-eleccion         - Crear tipo (TODO)
PUT    /api/configuracion/tipos-eleccion/<id>    - Actualizar tipo (TODO)
```

## Error Handling

### Estrategia de Manejo de Errores

1. **Errores de Autenticación:**
   - Token inválido → Redirigir a login
   - Permisos insuficientes → Mostrar error 403
   - Sesión expirada → Refresh token o redirigir

2. **Errores de Validación:**
   - Datos inválidos → Mostrar mensajes específicos
   - Códigos duplicados → Prevenir creación
   - Campos requeridos → Validar antes de enviar

3. **Errores del Sistema:**
   - Base de datos no disponible → Mostrar alerta crítica
   - CPU/Memoria alta → Mostrar advertencia
   - Servicios externos caídos → Degradar funcionalidad

4. **Errores de Usuario:**
   - Usuario no encontrado → Mensaje claro
   - Acción no permitida → Explicar por qué
   - Datos inconsistentes → Sugerir corrección

## Testing Strategy

### Unit Tests

1. **Gestión de Usuarios:**
   - Crear usuario con datos válidos
   - Validar campos requeridos
   - Prevenir duplicados
   - Resetear contraseña

2. **Configuración:**
   - Crear partido con código único
   - Validar colores hexadecimales
   - Crear candidato con partido válido

3. **Estadísticas:**
   - Calcular totales correctamente
   - Calcular porcentajes
   - Manejar divisiones por cero

### Integration Tests

1. **Flujo de Gestión de Usuario:**
   - Crear usuario → Verificar en BD
   - Actualizar usuario → Verificar cambios
   - Desactivar usuario → Verificar no puede login
   - Resetear password → Verificar nuevo password funciona

2. **Flujo de Monitoreo:**
   - Obtener métricas del sistema
   - Verificar salud de BD
   - Listar sesiones activas
   - Cerrar sesión de usuario

3. **Flujo de Auditoría:**
   - Registrar acción → Verificar en logs
   - Filtrar logs → Verificar resultados
   - Exportar logs → Verificar archivo

## Security Considerations

### Autenticación y Autorización

1. **Rol Super Admin:**
   - Decorador `@role_required(['super_admin'])` en todos los endpoints
   - Validación de JWT en cada request
   - No permitir auto-modificación de rol

2. **Auditoría Obligatoria:**
   - Registrar todas las acciones del super admin
   - Incluir timestamp, IP, user agent
   - No permitir eliminar propios logs

3. **Protección de Datos Sensibles:**
   - No exponer password_hash
   - Sanitizar inputs
   - Validar permisos antes de cada acción

### Rate Limiting

```python
# Límites por endpoint
RATE_LIMITS = {
    '/api/super-admin/users': '100/hour',
    '/api/super-admin/backup': '10/hour',
    '/api/super-admin/export': '20/hour',
    '/api/super-admin/stats': '1000/hour'
}
```

## Performance Considerations

### Optimizaciones

1. **Carga Inicial:**
   - Cargar solo estadísticas principales
   - Lazy loading de tabs
   - Paginación en tablas grandes

2. **Auto-Refresh:**
   - Estadísticas: cada 30 segundos
   - Monitoreo: cada 10 segundos
   - Auditoría: manual
   - Incidentes: cada 60 segundos

3. **Caching:**
   - Cachear configuración (partidos, candidatos) por 5 minutos
   - Cachear estadísticas por 30 segundos
   - Invalidar caché al hacer cambios

4. **Queries Optimizadas:**
   - Usar índices en queries frecuentes
   - Limitar resultados con paginación
   - Usar agregaciones en BD

### Métricas de Performance

- Tiempo de carga inicial: < 2 segundos
- Tiempo de respuesta de API: < 500ms
- Actualización de estadísticas: < 1 segundo
- Exportación de datos: < 30 segundos (background)

## UI/UX Design

### Principios de Diseño

1. **Claridad:**
   - Información organizada en tabs
   - Estadísticas destacadas
   - Alertas visibles

2. **Eficiencia:**
   - Acciones rápidas accesibles
   - Filtros intuitivos
   - Búsquedas rápidas

3. **Profesionalismo:**
   - Diseño limpio y moderno
   - Colores corporativos
   - Tipografía legible

4. **Feedback:**
   - Confirmaciones de acciones
   - Indicadores de carga
   - Mensajes de error claros

### Color Scheme

```css
/* Colores Principales */
--primary: #2a5298;      /* Azul institucional */
--secondary: #6c757d;    /* Gris */
--success: #28a745;      /* Verde */
--danger: #dc3545;       /* Rojo */
--warning: #ffc107;      /* Amarillo */
--info: #0dcaf0;         /* Azul claro */

/* Gradientes */
--gradient-header: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);

/* Estados de Salud */
--health-good: #28a745;
--health-warning: #ffc107;
--health-critical: #dc3545;
```

### Responsive Design

```css
/* Desktop (>1024px) */
- Layout de 3 columnas
- Sidebar fijo
- Gráficos grandes

/* Tablet (769px - 1024px) */
- Layout de 2 columnas
- Sidebar colapsable
- Gráficos medianos

/* Mobile (<768px) */
- Layout de 1 columna
- Tabs en lugar de sidebar
- Gráficos compactos
- Priorizar estadísticas críticas
```

## Integration Points

### Con Otros Dashboards

1. **Testigo Dashboard:**
   - Ver todos los formularios de todos los testigos
   - Gestionar usuarios testigos
   - Ver incidentes/delitos reportados

2. **Coordinador Puesto:**
   - Ver actividad de todos los coordinadores de puesto
   - Gestionar usuarios coordinadores
   - Ver formularios validados/rechazados

3. **Coordinador Municipal:**
   - Ver consolidados municipales
   - Gestionar coordinadores municipales
   - Ver reportes E-24

4. **Coordinador Departamental:**
   - Ver consolidados departamentales
   - Gestionar coordinadores departamentales
   - Ver reportes departamentales

### Con Componentes Compartidos

1. **SyncManager:**
   - Sincronización de incidentes/delitos reportados por super admin
   - Indicador de pendientes

2. **API Client:**
   - Todos los métodos disponibles
   - Sin restricciones de acceso

3. **Utils:**
   - Formateo de números y fechas
   - Mensajes de notificación
   - Helpers comunes

## Deployment

### Requisitos del Sistema

- Python 3.9+
- PostgreSQL 12+
- Flask 2.3+
- psutil (para métricas del sistema)

### Variables de Entorno

```bash
# Super Admin
SUPER_ADMIN_EMAIL=admin@sistema.com
SUPER_ADMIN_PASSWORD=SecurePassword123!

# Configuración
SESSION_TIMEOUT=30  # minutos
MAX_LOGIN_ATTEMPTS=5
BACKUP_RETENTION_DAYS=90
LOG_RETENTION_DAYS=90
```

### Configuración de Seguridad

```python
# Configuración de Flask
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

## Monitoring and Logging

### Métricas a Monitorear

1. **Sistema:**
   - CPU usage
   - Memory usage
   - Disk usage
   - Database connections

2. **Aplicación:**
   - Requests per minute
   - Response time
   - Error rate
   - Active users

3. **Negocio:**
   - Formularios creados por hora
   - Tasa de validación
   - Incidentes reportados
   - Usuarios activos por rol

### Logs

```python
# Niveles de log
DEBUG    - Información detallada para debugging
INFO     - Eventos normales del sistema
WARNING  - Situaciones inusuales pero manejables
ERROR    - Errores que afectan funcionalidad
CRITICAL - Errores que requieren atención inmediata
```

## Future Enhancements

### Fase 1 (Corto Plazo)
- Implementar gestión completa de configuración (partidos, candidatos)
- Implementar sistema de respaldos automáticos
- Implementar exportación masiva de datos
- Implementar gestión de sesiones activas

### Fase 2 (Mediano Plazo)
- Implementar dashboard de analytics avanzado
- Implementar sistema de notificaciones push
- Implementar mapa interactivo de Colombia
- Implementar reportes personalizados

### Fase 3 (Largo Plazo)
- Implementar machine learning para detección de anomalías
- Implementar predicciones de participación
- Implementar sistema de alertas inteligentes
- Implementar API pública para terceros

