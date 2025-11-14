# Design Document - Dashboard Testigo Electoral

## Overview

El Dashboard del Testigo Electoral es una aplicación web progresiva (PWA) optimizada para dispositivos móviles que permite a los testigos electorales reportar resultados, incidentes y delitos desde las mesas de votación. El diseño prioriza la usabilidad móvil, el funcionamiento offline, y la sincronización automática de datos.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Testigo Dashboard                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Formularios  │  │  Incidentes  │  │   Delitos    │      │
│  │    E-14      │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Sync Manager (Universal)                    │   │
│  │  - Sincronización automática cada 5 min              │   │
│  │  - Guardado local con localStorage                   │   │
│  │  - Indicador visual de pendientes                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Backend                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Formularios  │  │  Incidentes  │  │   Delitos    │      │
│  │   Routes     │  │   Routes     │  │   Routes     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Database (PostgreSQL)                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
testigo-dashboard-new.js
├── Gestión de Perfil
│   ├── loadUserProfile()
│   └── verificarPresencia()
│
├── Gestión de Mesas
│   ├── loadMesas()
│   ├── cambiarMesa()
│   └── actualizarPanelMesas()
│
├── Gestión de Formularios E-14
│   ├── loadForms()
│   ├── showCreateForm()
│   ├── saveForm(accion)
│   ├── editForm(id)
│   ├── viewForm(id)
│   ├── guardarBorradorLocal()
│   ├── editarBorradorLocal()
│   └── sincronizarBorradoresLocales()
│
├── Gestión de Votación
│   ├── loadTiposEleccion()
│   ├── cargarPartidosYCandidatos()
│   ├── renderVotacionForm()
│   ├── calcularTotales()
│   └── cambiarMesaFormulario()
│
├── Gestión de Incidentes
│   ├── reportarIncidente()
│   ├── guardarIncidente()
│   ├── cargarIncidentes()
│   └── loadTiposIncidentes()
│
├── Gestión de Delitos
│   ├── reportarDelito()
│   ├── guardarDelito()
│   ├── cargarDelitos()
│   └── loadTiposDelitos()
│
└── Sincronización (usa SyncManager global)
    ├── sincronizarTodosDatosLocales()
    └── actualizarIndicadorSincronizacion()
```

## Components and Interfaces

### 1. Dashboard Principal

**Componentes:**
- Header con nombre de usuario y botones de acción
- Selector de mesa con lista de mesas asignadas
- Botón de verificación de presencia
- Tabs de navegación (Formularios, Incidentes, Delitos)
- Panel lateral con información de mesas

**Interacciones:**
- Cambio de mesa actualiza formularios mostrados
- Verificación de presencia registra timestamp
- Tabs permiten navegar entre funcionalidades

### 2. Formularios E-14

**Componentes:**
- Lista de formularios con estados
- Botón "Nuevo Formulario"
- Modal de creación/edición con secciones:
  - Información básica (mesa, tipo elección)
  - Foto del formulario
  - Datos de votación (nulos, blancos, no marcadas)
  - Votos por partido y candidato
  - Resumen automático
  - Observaciones

**Interacciones:**
- Click en formulario abre para editar (si es borrador)
- Botón "Guardar Borrador" guarda localmente
- Botón "Enviar" valida y envía al servidor
- Cálculos automáticos en tiempo real

### 3. Incidentes y Delitos

**Componentes:**
- Tabs separados para incidentes y delitos
- Lista de reportes con badges de estado
- Botones "Reportar Incidente" y "Reportar Delito"
- Modales de reporte con formularios

**Interacciones:**
- Click en botón abre modal
- Formulario valida campos requeridos
- Guardado intenta servidor, fallback a local
- Lista muestra estado de sincronización

### 4. Sync Manager (Universal)

**Componentes:**
- Indicador flotante en esquina inferior derecha
- Contador de registros pendientes
- Botón de sincronización manual
- Desglose por tipo (formularios, incidentes, delitos)

**Interacciones:**
- Aparece automáticamente cuando hay pendientes
- Click en botón sincroniza manualmente
- Se oculta cuando todo está sincronizado
- Actualización automática cada 30 segundos

## Data Models

### FormularioE14 (Local Storage)

```javascript
{
  local_id: "mesa_tipo_timestamp",
  mesa_id: number,
  tipo_eleccion_id: number,
  total_votantes_registrados: number,
  total_votos: number,
  votos_validos: number,
  votos_nulos: number,
  votos_blanco: number,
  tarjetas_no_marcadas: number,
  total_tarjetas: number,
  observaciones: string,
  votos_partidos: [
    { partido_id: number, votos: number }
  ],
  votos_candidatos: [
    { candidato_id: number, votos: number }
  ],
  estado: "borrador" | "pendiente" | "validado" | "rechazado",
  saved_at: ISO8601,
  sincronizado: boolean
}
```

### Incidente (Local Storage)

```javascript
{
  id: "incidente_timestamp_random",
  mesa_id: number,
  tipo_incidente: string,
  titulo: string,
  severidad: "baja" | "media" | "alta" | "critica",
  descripcion: string,
  fecha_hora: ISO8601,
  sincronizado: boolean,
  id_servidor: number | null
}
```

### Delito (Local Storage)

```javascript
{
  id: "delito_timestamp_random",
  mesa_id: number,
  tipo_delito: string,
  titulo: string,
  gravedad: "leve" | "media" | "grave" | "muy_grave",
  descripcion: string,
  testigos_adicionales: string | null,
  fecha_hora: ISO8601,
  sincronizado: boolean,
  id_servidor: number | null
}
```

## Error Handling

### Estrategia de Manejo de Errores

1. **Sin Conexión:**
   - Guardar datos en localStorage
   - Mostrar mensaje: "⚠️ Guardado localmente. Se sincronizará automáticamente."
   - Agregar a cola de sincronización

2. **Error de Validación:**
   - Mostrar mensajes específicos por campo
   - Prevenir envío hasta corregir
   - Mantener datos ingresados

3. **Error del Servidor:**
   - Mostrar mensaje de error específico
   - Ofrecer guardar como borrador
   - Registrar en console para debugging

4. **Sesión Expirada:**
   - Redirigir a login
   - Mantener datos locales
   - Sincronizar después de re-login

### Mensajes de Error

```javascript
const ERROR_MESSAGES = {
  NO_MESA: 'Debe seleccionar una mesa',
  NO_TIPO_ELECCION: 'Debe seleccionar un tipo de elección',
  VALIDATION_FAILED: 'Por favor complete todos los campos requeridos',
  SERVER_ERROR: 'Error del servidor. Intente nuevamente.',
  NO_CONNECTION: 'Sin conexión. Los datos se guardarán localmente.',
  SESSION_EXPIRED: 'Su sesión ha expirado. Por favor inicie sesión nuevamente.'
};
```

## Testing Strategy

### Unit Tests

1. **Cálculos Automáticos:**
   - Verificar suma de votos válidos
   - Verificar cálculo de total votos
   - Verificar cálculo de total tarjetas
   - Verificar identificación de partido ganador

2. **Validaciones:**
   - Verificar validación de campos requeridos
   - Verificar validación de números
   - Verificar prevención de valores negativos

3. **Sincronización:**
   - Verificar guardado local
   - Verificar sincronización exitosa
   - Verificar manejo de errores de sincronización
   - Verificar actualización de indicador

### Integration Tests

1. **Flujo Completo de Formulario:**
   - Crear formulario
   - Guardar borrador
   - Editar borrador
   - Enviar para revisión
   - Verificar estado actualizado

2. **Flujo de Incidentes:**
   - Reportar incidente
   - Verificar guardado local
   - Verificar sincronización
   - Verificar visualización

3. **Flujo de Sincronización:**
   - Crear datos offline
   - Simular recuperación de conexión
   - Verificar sincronización automática
   - Verificar actualización de UI

### Manual Testing

1. **Pruebas Móviles:**
   - Verificar en diferentes tamaños de pantalla
   - Verificar teclado numérico en campos numéricos
   - Verificar captura de fotos
   - Verificar usabilidad táctil

2. **Pruebas de Conexión:**
   - Crear datos con conexión
   - Crear datos sin conexión
   - Simular pérdida de conexión durante envío
   - Verificar recuperación de conexión

## UI/UX Design

### Principios de Diseño

1. **Móvil-First:**
   - Diseño optimizado para pantallas pequeñas
   - Botones grandes y fáciles de tocar
   - Inputs optimizados para móvil
   - Minimizar scroll

2. **Feedback Visual:**
   - Badges de colores para estados
   - Iconos intuitivos
   - Mensajes de confirmación
   - Indicadores de carga

3. **Prevención de Errores:**
   - Validación en tiempo real
   - Cálculos automáticos
   - Confirmaciones para acciones importantes
   - Mensajes claros de error

4. **Accesibilidad:**
   - Contraste adecuado
   - Tamaños de fuente legibles
   - Labels claros en formularios
   - Navegación por teclado

### Color Scheme

```css
/* Estados de Formularios */
.badge-pendiente { background: #0dcaf0; } /* Azul - Enviado */
.badge-validado { background: #28a745; }  /* Verde - Validado */
.badge-rechazado { background: #dc3545; } /* Rojo - Rechazado */
.badge-borrador { background: #6c757d; }  /* Gris - Borrador */
.badge-local { background: #ffc107; }     /* Amarillo - Local */

/* Severidad de Incidentes */
.severidad-baja { border-left-color: #0dcaf0; }
.severidad-media { border-left-color: #ffc107; }
.severidad-alta { border-left-color: #fd7e14; }
.severidad-critica { border-left-color: #dc3545; }

/* Gravedad de Delitos */
.gravedad-leve { border-left-color: #0dcaf0; }
.gravedad-media { border-left-color: #ffc107; }
.gravedad-grave { border-left-color: #dc3545; }
.gravedad-muy-grave { border-left-color: #6c757d; }
```

### Responsive Breakpoints

```css
/* Mobile First */
@media (max-width: 768px) {
  /* Diseño de 1 columna */
  /* Botones full-width */
  /* Inputs más grandes */
  /* Modales full-screen */
}

@media (min-width: 769px) and (max-width: 1024px) {
  /* Diseño de 2 columnas */
  /* Sidebar colapsable */
}

@media (min-width: 1025px) {
  /* Diseño de 3 columnas */
  /* Sidebar fijo */
  /* Modales centrados */
}
```

## Performance Considerations

### Optimizaciones

1. **Carga Inicial:**
   - Cargar solo datos necesarios
   - Lazy loading de imágenes
   - Minimizar requests iniciales

2. **Sincronización:**
   - Batch de múltiples registros
   - Throttling de sincronización automática
   - Priorizar formularios sobre incidentes

3. **LocalStorage:**
   - Limpiar datos sincronizados antiguos (>7 días)
   - Comprimir datos si es necesario
   - Limitar tamaño de imágenes

4. **Renderizado:**
   - Virtual scrolling para listas largas
   - Debouncing en búsquedas
   - Memoización de cálculos

### Métricas de Performance

- Tiempo de carga inicial: < 3 segundos
- Tiempo de respuesta de UI: < 100ms
- Tiempo de sincronización: < 5 segundos por registro
- Uso de memoria: < 50MB
- Tamaño de localStorage: < 10MB

## Security Considerations

### Autenticación y Autorización

1. **JWT Tokens:**
   - Access token en memoria
   - Refresh token en localStorage
   - Expiración de 30 minutos

2. **Validación de Rol:**
   - Verificar rol `testigo_electoral` en cada request
   - Validar acceso solo a mesas asignadas
   - Prevenir acceso a datos de otros testigos

### Protección de Datos

1. **Datos Locales:**
   - No almacenar información sensible
   - Limpiar datos al cerrar sesión (opcional)
   - Encriptar datos sensibles si es necesario

2. **Transmisión:**
   - HTTPS obligatorio
   - Validación de certificados
   - Sanitización de inputs

### Auditoría

1. **Logging:**
   - Registrar todas las acciones del testigo
   - Timestamp de creación/modificación
   - IP y user agent

2. **Trazabilidad:**
   - Historial de cambios en formularios
   - Registro de sincronizaciones
   - Logs de errores

## Deployment

### Requisitos

- Navegador moderno con soporte para:
  - ES6+
  - LocalStorage
  - Fetch API
  - Camera API (para fotos)
  - Service Workers (para PWA)

### Configuración

```javascript
// Configuración de sincronización
const SYNC_CONFIG = {
  AUTO_SYNC_INTERVAL: 5 * 60 * 1000, // 5 minutos
  INDICATOR_UPDATE_INTERVAL: 30 * 1000, // 30 segundos
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 5000, // 5 segundos
  CLEANUP_DAYS: 7 // Limpiar datos >7 días
};
```

### Monitoreo

- Tasa de éxito de sincronización
- Tiempo promedio de sincronización
- Cantidad de datos pendientes
- Errores de validación
- Uso de localStorage

