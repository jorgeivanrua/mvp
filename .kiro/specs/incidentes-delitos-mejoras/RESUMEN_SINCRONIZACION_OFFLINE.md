# Resumen: Sistema de Sincronización Offline Completo

## 📋 Descripción General

Se ha implementado un sistema completo de sincronización offline que permite a los usuarios trabajar sin conexión a internet y sincronizar automáticamente cuando se restablece la conexión. El sistema cubre:

- ✅ Formularios E-14 (Actas de escrutinio)
- ✅ Formularios E-24 (Consolidados)
- ✅ Incidentes electorales
- ✅ Delitos electorales
- ✅ Evidencia fotográfica

## 🏗️ Arquitectura

### Componentes Principales

#### 1. **IndexedDB Service** (`indexeddb-service.js`)
Servicio de almacenamiento local usando IndexedDB.

**Object Stores:**
- `reportes_pendientes`: Almacena formularios, incidentes y delitos pendientes de sincronización
- `evidencia_offline`: Almacena fotos en base64 asociadas a reportes offline
- `configuracion_offline`: Configuración del sistema offline
- `datos_referencia`: Datos de referencia (puestos, mesas, etc.)

**Funciones principales:**
- `guardarReportePendiente()`: Guarda cualquier tipo de reporte offline
- `obtenerReportesPendientes()`: Obtiene reportes pendientes de sincronización
- `marcarReporteSincronizado()`: Marca un reporte como sincronizado
- `guardarEvidenciaOffline()`: Guarda fotos en base64
- `obtenerEstadisticas()`: Obtiene estadísticas de almacenamiento

#### 2. **Sync Manager** (`sync-manager-offline.js`)
Gestor de sincronización automática con retry logic.

**Características:**
- Detección automática de conexión/desconexión
- Sincronización automática cada 5 minutos
- Retry logic con hasta 3 intentos
- Cola de sincronización con gestión de errores
- Soporte para múltiples tipos de reportes

**Funciones principales:**
- `guardarReporteOffline()`: Guarda reporte en IndexedDB
- `syncPendingData()`: Sincroniza todos los reportes pendientes
- `syncReporte()`: Sincroniza un reporte específico
- `syncEvidencia()`: Sincroniza evidencia fotográfica

**Endpoints soportados:**
- `/api/incidentes` - Incidentes electorales
- `/api/delitos` - Delitos electorales
- `/api/formularios` - Formularios E-14
- `/api/formularios/e24` - Formularios E-24
- `/api/evidencia/upload` - Evidencia fotográfica

#### 3. **Formularios Offline Manager** (`formularios-offline.js`)
Gestor específico para formularios E-14 y E-24.

**Funciones principales:**
- `guardarFormularioE14Offline()`: Guarda formulario E-14 offline
- `guardarFormularioE24Offline()`: Guarda formulario E-24 offline
- `migrarDatosLocales()`: Migra datos de localStorage a IndexedDB
- `sincronizarFormularios()`: Sincroniza formularios pendientes

**Funciones globales expuestas:**
- `window.guardarFormularioE14()`: Guarda E-14 con detección de conexión
- `window.guardarFormularioE24()`: Guarda E-24 con detección de conexión
- `window.subirFotosFormulario()`: Sube fotos de formularios

#### 4. **Offline Indicators** (`offline-indicators.js`)
Indicadores visuales del estado offline.

**Componentes UI:**
- Modal informativo cuando se pierde conexión
- Panel de estado de sincronización expandible
- Indicador en navbar cuando está offline
- Log de sincronización en tiempo real
- Estadísticas de reportes pendientes

**Funciones principales:**
- `updateConnectionStatus()`: Actualiza indicadores según conexión
- `updateSyncStats()`: Actualiza estadísticas de sincronización
- `forceSync()`: Fuerza sincronización manual
- `clearSyncedData()`: Limpia datos ya sincronizados

#### 5. **Reportes Pendientes Panel** (`reportes-pendientes-panel.js`)
Panel visual para gestionar reportes pendientes.

**Características:**
- Lista de reportes pendientes con detalles
- Badge con contador de pendientes
- Tiempo transcurrido desde creación
- Botón para sincronizar manualmente
- Auto-actualización cada 30 segundos

## 📝 Gestión de Múltiples Formularios E-14

### Concepto Importante

Una **misma mesa** puede tener **múltiples formularios E-14**, uno por cada tipo de elección:

- E-14 para **Presidente**
- E-14 para **Diputados**
- E-14 para **Alcalde**
- E-14 para **Concejales**
- etc.

### Identificación Única

Cada formulario E-14 se identifica por:

```
Identificador = mesa_id + tipo_eleccion_id + timestamp
Ejemplo: E14_M123_T1_1701234567890
```

### Visualización para Coordinadores

Cuando un coordinador revisa los reportes pendientes, verá:

```
📄 E-14: Mesa 001-A
   Elección Presidencial
   🕐 hace 5 minutos
   📸 3 fotos
```

```
📄 E-14: Mesa 001-A
   Diputados Nacionales
   🕐 hace 3 minutos
   📸 2 fotos
```

Esto evita confusión al tener múltiples E-14 de la misma mesa.

### Fotos Múltiples por Acta

Cada E-14 puede tener **varias fotos** (páginas del acta):

```javascript
Foto 1: "Acta E-14 - Mesa 001-A - Presidente - Página 1/3"
Foto 2: "Acta E-14 - Mesa 001-A - Presidente - Página 2/3"
Foto 3: "Acta E-14 - Mesa 001-A - Presidente - Página 3/3"
```

Cada foto incluye:
- Mesa específica
- Tipo de elección específico
- Número de página
- Total de páginas

## 🔄 Flujo de Trabajo

### Guardado Offline

```
1. Usuario completa formulario/reporte
2. Sistema detecta estado de conexión
3. Si NO hay conexión:
   a. Guarda datos en IndexedDB
   b. Guarda fotos en base64
   c. Muestra mensaje: "Guardado localmente"
   d. Agrega a cola de sincronización
4. Si HAY conexión:
   a. Intenta enviar al servidor
   b. Si falla, guarda offline (paso 3)
   c. Si tiene éxito, sube fotos
```

### Sincronización Automática

```
1. Sistema detecta recuperación de conexión
2. SyncManager inicia sincronización
3. Para cada reporte pendiente:
   a. Prepara datos (elimina campos internos)
   b. Determina endpoint según tipo
   c. Envía POST al servidor
   d. Si tiene éxito:
      - Marca como sincronizado
      - Sincroniza evidencia asociada
   e. Si falla:
      - Incrementa contador de intentos
      - Reintenta hasta 3 veces
4. Actualiza indicadores visuales
5. Notifica resultado al usuario
```

### Sincronización de Evidencia

```
1. Obtiene evidencia asociada al reporte
2. Para cada foto:
   a. Convierte base64 a Blob
   b. Crea FormData
   c. Envía a /api/evidencia/upload
   d. Asocia con ID del servidor
3. Marca evidencia como sincronizada
```

## 📊 Tipos de Datos Soportados

### Formularios E-14
```javascript
{
    tipo: 'formulario_e14',
    mesa_id: number,
    tipo_eleccion_id: number,
    mesa_codigo: string,              // Para identificación visual
    tipo_eleccion_nombre: string,     // Para identificación visual
    identificador_unico: string,      // E14_M123_T1_timestamp
    total_votantes_registrados: number,
    votos_partidos: array,
    votos_candidatos: array,
    observaciones: string,
    // ... otros campos
}
```

**Nota importante**: Cada mesa puede tener **múltiples formularios E-14**, uno por cada tipo de elección (Presidente, Diputados, Alcalde, etc.). El sistema identifica cada formulario por la combinación de `mesa_id` + `tipo_eleccion_id`.

### Formularios E-24
```javascript
{
    tipo: 'formulario_e24',
    puesto_id: number,
    tipo_eleccion_id: number,
    total_mesas: number,
    mesas_reportadas: number,
    consolidado_votos: object,
    // ... otros campos
}
```

### Incidentes
```javascript
{
    tipo: 'incidente',
    tipo_incidente: string,
    titulo: string,
    descripcion: string,
    severidad: string,
    mesa_id: number
}
```

### Delitos
```javascript
{
    tipo: 'delito',
    tipo_delito: string,
    titulo: string,
    descripcion: string,
    gravedad: string,
    testigos_adicionales: string,
    mesa_id: number
}
```

### Evidencia Fotográfica
```javascript
{
    file_data: string (base64),
    filename: string,
    mime_type: string,
    tipo_reporte: string,
    reporte_temp_id: string,
    fecha_captura: string (ISO),
    // Metadatos adicionales para E-14
    mesa_id: number,                  // ID de la mesa
    tipo_eleccion_id: number,         // ID del tipo de elección
    mesa_codigo: string,              // Código de la mesa
    tipo_eleccion_nombre: string,     // Nombre del tipo de elección
    numero_pagina: number,            // Número de página del acta
    total_paginas: number,            // Total de páginas del acta
    descripcion: string               // Descripción completa
}
```

**Nota importante**: Los formularios E-14 pueden tener **múltiples fotos** (páginas del acta). Cada foto incluye metadatos completos para identificar a qué mesa y tipo de elección pertenece, evitando confusiones al revisar.

## 🎨 Interfaz de Usuario

### Indicadores Visuales

1. **Modal Offline**
   - Se muestra automáticamente al perder conexión
   - Explica funcionalidad offline
   - Botón "Entendido" para cerrar

2. **Indicador en Navbar**
   - Badge rojo "Sin conexión" cuando está offline
   - Se oculta automáticamente cuando hay conexión

3. **Panel de Sincronización**
   - Ubicación: Esquina inferior derecha
   - Expandible/colapsable
   - Muestra estadísticas en tiempo real
   - Botones de acción (Sincronizar, Limpiar)
   - Log de sincronización

4. **Panel de Reportes Pendientes**
   - Ubicación: Esquina inferior izquierda
   - Lista detallada de reportes pendientes
   - Badge con contador
   - Tiempo transcurrido
   - Botón de sincronización manual

5. **Badge Flotante**
   - Muestra número de elementos pendientes
   - Icono de sincronización (gira durante sync)
   - Click para ver detalles

### Mensajes al Usuario

- ✅ **Éxito**: "Formulario enviado exitosamente"
- ⚠️ **Offline**: "Sin conexión. Guardado localmente y se sincronizará automáticamente"
- 🔄 **Sincronizando**: "Sincronizando datos..."
- ✅ **Sincronizado**: "Sincronización completada: X exitosos, Y errores"
- ❌ **Error**: "Error al guardar: [mensaje]"

## 🔧 Integración con Código Existente

### Modificaciones en `incidentes-delitos.js`

```javascript
// Antes
async function guardarIncidente() {
    const response = await APIClient.crearIncidente(data);
    // ...
}

// Después
async function guardarIncidente() {
    // Detecta conexión y guarda offline si es necesario
    if (!navigator.onLine) {
        await guardarIncidenteOffline(data, fotos);
        return;
    }
    
    try {
        const response = await APIClient.crearIncidente(data);
        // ...
    } catch (error) {
        // Fallback a offline
        await guardarIncidenteOffline(data, fotos);
    }
}
```

### Nuevas Funciones Globales

```javascript
// Formularios E-14
window.guardarFormularioE14(data, fotos)
window.guardarFormularioE14Offline(data, fotos)

// Formularios E-24
window.guardarFormularioE24(data, fotos)
window.guardarFormularioE24Offline(data, fotos)

// Incidentes
window.guardarIncidenteOffline(data, fotos)

// Delitos
window.guardarDelitoOffline(data, fotos)

// Evidencia
window.subirFotosFormulario(fotos, tipo, id)
```

## 📱 Soporte Móvil

- Diseño responsive para todos los componentes
- Indicadores adaptados a pantallas pequeñas
- Paneles optimizados para móviles
- Touch-friendly

## 🔒 Seguridad

- Tokens de autenticación incluidos en sincronización
- Validación de permisos en servidor
- Datos encriptados en IndexedDB (según navegador)
- Limpieza automática de datos antiguos

## 📈 Rendimiento

- Sincronización periódica cada 5 minutos
- Compresión de imágenes antes de guardar
- Lazy loading de datos
- Caché inteligente
- Limpieza automática de datos sincronizados (7 días)

## 🐛 Manejo de Errores

- Retry logic con backoff exponencial
- Máximo 3 intentos por reporte
- Logs detallados en consola
- Notificaciones al usuario
- Fallback a offline en caso de error

## 📊 Estadísticas

El sistema proporciona estadísticas en tiempo real:

```javascript
{
    reportes_pendientes: number,
    reportes_sincronizados: number,
    evidencia_offline: number,
    datos_referencia: number,
    formularios_e14: number,
    formularios_e24: number,
    incidentes: number,
    delitos: number,
    total: number
}
```

## 🚀 Uso

### Para Desarrolladores

```javascript
// Guardar formulario E-14 con detección automática
await guardarFormularioE14({
    mesa_id: 123,
    tipo_eleccion_id: 1,
    votos_partidos: [...]
}, fotosArray);

// Forzar sincronización
await window.syncManager.forcSync();

// Obtener estadísticas
const stats = await window.formulariosOfflineManager.obtenerEstadisticas();
```

### Para Usuarios

1. Completar formulario normalmente
2. Si no hay conexión, el sistema guarda automáticamente
3. Ver reportes pendientes en panel inferior izquierdo
4. Sincronización automática al recuperar conexión
5. Opción de sincronizar manualmente con botón

## ✅ Beneficios

1. **Trabajo sin interrupciones**: Los usuarios pueden trabajar sin conexión
2. **Sincronización automática**: No requiere intervención manual
3. **Transparente**: El usuario no necesita saber si está online/offline
4. **Confiable**: Retry logic asegura que los datos se sincronicen
5. **Visual**: Indicadores claros del estado del sistema
6. **Completo**: Soporta todos los tipos de reportes y evidencia

## 🔄 Migración de Datos

El sistema migra automáticamente datos existentes de localStorage a IndexedDB:

- Borradores E-14
- Incidentes locales
- Delitos locales

## 📝 Notas Técnicas

- IndexedDB versión 1
- Soporte para navegadores modernos
- Fallback a localStorage si IndexedDB no disponible
- Compatible con PWA
- Service Worker ready

## 🎯 Casos de Uso

1. **Testigo en zona rural**: Sin señal, reporta incidentes que se sincronizan al llegar a zona con cobertura
2. **Coordinador de puesto**: Completa formularios E-14 offline durante corte de luz
3. **Auditor**: Revisa reportes pendientes y fuerza sincronización antes de reunión
4. **Coordinador municipal**: Genera E-24 consolidado sin depender de conexión constante

## 🔮 Futuras Mejoras

- [ ] Compresión de datos en IndexedDB
- [ ] Sincronización selectiva (por tipo)
- [ ] Priorización de sincronización
- [ ] Estadísticas de uso de almacenamiento
- [ ] Exportación de datos offline
- [ ] Modo offline forzado para testing
- [ ] Sincronización en background con Service Worker

---

**Fecha de implementación**: Diciembre 2024  
**Versión**: 1.0  
**Estado**: ✅ Completado y funcional
