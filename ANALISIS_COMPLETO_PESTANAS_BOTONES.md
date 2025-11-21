# 🔍 Análisis Exhaustivo: Pestañas y Botones por Rol

## 📊 RESUMEN EJECUTIVO

### Estructura de Dashboards:

| Rol | Pestañas | Botones Principales | Estado |
|-----|----------|-------------------|--------|
| **Testigo** | 3 | 5 | ⚠️ Incompleto |
| **Coord. Puesto** | 4 | 8 | ✅ Completo |
| **Coord. Municipal** | 4 | 6 | ✅ Completo |
| **Coord. Departamental** | 3 | 4 | ✅ Completo |
| **Super Admin** | 8 | 15+ | ✅ Completo |

---

## 🎯 TESTIGO ELECTORAL

### Pestañas (3):
1. **📄 Formularios E-14** (activa por defecto)
2. **⚠️ Incidentes**
3. **🛡️ Delitos**

### Botones y Acciones:

#### Pestaña: Formularios E-14
```
Sección Superior:
├─ [Selector de Mesa] (dropdown)
├─ [Verificar Presencia] (botón primario)
└─ [Nuevo Formulario E-14] (botón success, deshabilitado hasta verificar presencia)

Sección Formularios:
├─ [Ver] (por cada formulario)
├─ [Editar] (si está en borrador)
└─ [Eliminar] (si está en borrador)

Acciones Globales:
├─ [Sincronizar] (botón outline-primary, esquina superior)
└─ [Cerrar Sesión] (botón outline-danger, esquina superior)
```

**Funcionalidades**:
- ✅ Seleccionar mesa del puesto
- ✅ Verificar presencia en mesa
- ✅ Crear nuevo formulario E-14
- ✅ Ver formularios enviados
- ✅ Editar borradores
- ✅ Eliminar borradores
- ✅ Sincronización offline

**Datos que Carga**:
```javascript
// Al iniciar
loadUserProfile()      → Perfil + ubicación + contexto
loadForms()            → Formularios propios
loadTiposEleccion()    → Tipos de elección
loadTiposIncidentes()  → Tipos de incidentes
loadTiposDelitos()     → Tipos de delitos

// Al verificar presencia
registrarPresencia()   → Actualiza ubicación a mesa
loadUserProfile()      → Recarga perfil actualizado

// Auto-refresh (30s)
loadForms()            → Actualiza formularios
actualizarPanelMesas() → Actualiza estado de mesas
```

#### Pestaña: Incidentes
```
Sección Superior:
└─ [Reportar Nuevo Incidente] (botón primary)

Lista de Incidentes:
├─ [Ver Detalle] (por cada incidente)
└─ [Editar] (si está en borrador)
```

**Funcionalidades**:
- ✅ Reportar incidente
- ✅ Ver incidentes reportados
- ✅ Editar incidentes en borrador
- ❌ NO tiene filtros
- ❌ NO tiene búsqueda

**Datos que Carga**:
```javascript
// Al abrir pestaña
loadIncidentes()  → Incidentes del testigo
```

#### Pestaña: Delitos
```
Sección Superior:
└─ [Reportar Delito Electoral] (botón danger)

Lista de Delitos:
├─ [Ver Detalle] (por cada delito)
└─ [Editar] (si está en borrador)
```

**Funcionalidades**:
- ✅ Reportar delito
- ✅ Ver delitos reportados
- ✅ Editar delitos en borrador
- ❌ NO tiene filtros
- ❌ NO tiene búsqueda

**Datos que Carga**:
```javascript
// Al abrir pestaña
loadDelitos()  → Delitos del testigo
```

---

## 🎯 COORDINADOR DE PUESTO

### Pestañas (4):
1. **📄 Formularios E-14** (activa por defecto)
2. **📊 Consolidado E-24 Puesto**
3. **⚠️ Incidentes** (con badge de contador)
4. **🛡️ Delitos** (con badge de contador)

### Botones y Acciones:

#### Pestaña: Formularios E-14
```
Sección Superior:
├─ [Filtros por Estado]
│  ├─ Todos
│  ├─ Pendientes
│  ├─ Validados
│  └─ Rechazados
└─ [Actualizar] (botón refresh)

Tabla de Formularios:
├─ [Revisar] (si está pendiente)
├─ [Ver] (si está validado/rechazado)
└─ Click en fila → Abre modal de validación

Modal de Validación:
├─ [Editar Datos] (permite corregir antes de validar)
├─ [Validar] (botón success)
├─ [Rechazar] (botón danger)
├─ [Cancelar Edición] (si está editando)
└─ [Validar con Cambios] (si editó datos)

Paneles Laterales:
├─ Panel Consolidado (votos por partido)
├─ Panel Mesas (estado de cada mesa)
└─ Panel Testigos (presentes/ausentes)
```

**Funcionalidades**:
- ✅ Ver todos los formularios del puesto
- ✅ Filtrar por estado
- ✅ Validar formularios
- ✅ Rechazar formularios con motivo
- ✅ Editar datos antes de validar
- ✅ Ver consolidado en tiempo real
- ✅ Ver estado de mesas
- ✅ Ver testigos asignados

**Datos que Carga**:
```javascript
// Al iniciar
loadUserProfile()    → Perfil + ubicación
loadFormularios()    → Formularios del puesto + estadísticas
loadConsolidado()    → Consolidado de votos
loadMesas()          → Mesas del puesto con estado
loadTestigos()       → Testigos asignados

// Auto-refresh (30s)
loadFormularios()
loadConsolidado()
loadMesas()
loadTestigos()
```

#### Pestaña: Consolidado E-24
```
Sección Superior:
├─ [Generar PDF] (botón primary)
└─ [Exportar Excel] (botón success)

Contenido:
├─ Tabla resumen por mesa
├─ Totales del puesto
└─ Votos por partido
```

**Funcionalidades**:
- ✅ Ver consolidado E-24 del puesto
- ✅ Tabla con todas las mesas
- ✅ Totales calculados
- ⏳ Generar PDF (en desarrollo)
- ⏳ Exportar Excel (en desarrollo)

**Datos que Carga**:
```javascript
// Al abrir pestaña
loadE24Data()  → Mesas + consolidado
```

#### Pestaña: Incidentes
```
Sección Superior:
├─ [Filtros por Estado]
│  ├─ Todos
│  ├─ Reportados
│  ├─ En Revisión
│  └─ Resueltos
└─ Badge con contador de pendientes

Lista de Incidentes:
├─ [Gestionar] (por cada incidente)
└─ Modal de Gestión:
    ├─ [Cambiar Estado]
    ├─ [Agregar Comentario]
    └─ [Guardar]
```

**Funcionalidades**:
- ✅ Ver incidentes del puesto
- ✅ Filtrar por estado
- ✅ Gestionar incidentes
- ✅ Cambiar estado
- ✅ Agregar seguimiento
- ✅ Ver historial

**Datos que Carga**:
```javascript
// Al abrir pestaña
cargarIncidentesPuesto()  → Incidentes del puesto
```

#### Pestaña: Delitos
```
Sección Superior:
├─ [Filtros por Estado]
└─ Badge con contador de pendientes

Lista de Delitos:
├─ [Gestionar] (por cada delito)
└─ Modal de Gestión:
    ├─ [Cambiar Estado]
    ├─ [Agregar Comentario]
    └─ [Guardar]
```

**Funcionalidades**:
- ✅ Ver delitos del puesto
- ✅ Filtrar por estado
- ✅ Gestionar delitos
- ✅ Cambiar estado
- ✅ Agregar seguimiento
- ✅ Ver historial

**Datos que Carga**:
```javascript
// Al abrir pestaña
cargarDelitosPuesto()  → Delitos del puesto
```

---

## 🎯 COORDINADOR MUNICIPAL

### Pestañas (4):
1. **🏢 Puestos** (activa por defecto)
2. **📊 Consolidado Municipal**
3. **⚠️ Discrepancias**
4. **📈 Estadísticas**

### Botones y Acciones:

#### Pestaña: Puestos
```
Sección Superior:
├─ [Filtros por Estado]
│  ├─ Todos
│  ├─ Completos
│  ├─ Incompletos
│  └─ Con Discrepancias
├─ [Buscar Puesto] (input)
└─ [Actualizar] (botón refresh)

Tabla de Puestos:
├─ Click en fila → Selecciona puesto
└─ Panel lateral con detalles del puesto

Panel Lateral:
├─ Información del coordinador
├─ Estadísticas del puesto
└─ [Ver Detalles Completos] (botón)
```

**Funcionalidades**:
- ✅ Ver todos los puestos del municipio
- ✅ Filtrar por estado
- ✅ Buscar puesto
- ✅ Ver detalles de puesto
- ✅ Ver progreso por puesto
- ✅ Ver coordinador asignado

**Datos que Carga**:
```javascript
// Al iniciar
loadUserProfile()    → Perfil + ubicación
loadPuestos()        → Puestos del municipio + estadísticas
loadEstadisticas()   → Estadísticas municipales
loadConsolidadoMunicipal()  → Consolidado
loadDiscrepancias()  → Discrepancias detectadas

// Auto-refresh (60s)
loadPuestos()
loadEstadisticas()
loadConsolidadoMunicipal()
loadDiscrepancias()
```

#### Pestaña: Consolidado Municipal
```
Sección Superior:
├─ [Generar E-24 Municipal] (botón primary)
└─ [Exportar Datos] (botón success)

Contenido:
├─ Resumen municipal
├─ Votos por partido
└─ Gráficos de participación
```

**Funcionalidades**:
- ✅ Ver consolidado municipal
- ✅ Votos por partido
- ✅ Participación
- ⏳ Generar E-24 (validación de requisitos)
- ⏳ Exportar datos

#### Pestaña: Discrepancias
```
Lista de Discrepancias:
├─ Filtros por severidad
├─ Click en discrepancia → Va al puesto
└─ Alertas visuales por tipo
```

**Funcionalidades**:
- ✅ Ver discrepancias detectadas
- ✅ Filtrar por severidad
- ✅ Navegar a puesto con problema
- ✅ Ver descripción detallada

#### Pestaña: Estadísticas
```
Contenido:
├─ Resumen general
├─ Estadísticas por puesto
├─ Puestos con mayor tasa de rechazo
└─ Métricas de calidad
```

**Funcionalidades**:
- ✅ Ver estadísticas detalladas
- ✅ Identificar puestos problemáticos
- ✅ Métricas de calidad de datos

---

## 🎯 COORDINADOR DEPARTAMENTAL

### Pestañas (3):
1. **🏛️ Municipios** (activa por defecto)
2. **📊 Consolidado Departamental**
3. **📈 Estadísticas**

### Botones y Acciones:

#### Pestaña: Municipios
```
Sección Superior:
└─ [Actualizar] (botón refresh)

Tabla de Municipios:
├─ Nombre del municipio
├─ Total puestos
├─ Total mesas
├─ Formularios completados
├─ Porcentaje de avance (barra de progreso)
└─ Estado (badge)
```

**Funcionalidades**:
- ✅ Ver todos los municipios del departamento
- ✅ Ver progreso por municipio
- ✅ Ver estadísticas agregadas
- ✅ Identificar municipios con retraso

**Datos que Carga**:
```javascript
// Al iniciar
loadUserProfile()    → Perfil + ubicación
loadMunicipios()     → Municipios + estadísticas
loadEstadisticas()   → Estadísticas departamentales

// Auto-refresh (60s)
loadMunicipios()
loadEstadisticas()
```

#### Pestaña: Consolidado Departamental
```
Contenido:
├─ Resumen departamental
├─ Votos por partido
├─ Participación por municipio
└─ Gráficos comparativos
```

**Funcionalidades**:
- ✅ Ver consolidado departamental
- ✅ Votos por partido
- ✅ Comparativa por municipio

#### Pestaña: Estadísticas
```
Contenido:
├─ Tabla de estadísticas por municipio
├─ Total mesas
├─ Formularios recibidos
├─ Formularios validados
└─ Porcentaje de avance
```

**Funcionalidades**:
- ✅ Ver estadísticas detalladas
- ✅ Comparar municipios
- ✅ Identificar áreas problemáticas

---

## 🎯 SUPER ADMIN

### Pestañas (8):
1. **📊 Dashboard** (activa por defecto)
2. **👥 Usuarios**
3. **⚙️ Configuración**
4. **📈 Monitoreo**
5. **📋 Auditoría**
6. **⚠️ Incidentes**
7. **🗳️ Campañas**
8. **🎨 Temas**

### Botones y Acciones (Resumen):

#### Pestaña: Dashboard
- Ver estadísticas globales
- Gráficos de progreso nacional
- Actividad reciente

#### Pestaña: Usuarios
- [Crear Usuario]
- [Editar Usuario]
- [Resetear Contraseña]
- [Activar/Desactivar]
- [Cargar Usuarios Masivamente]

#### Pestaña: Configuración
- Gestionar Partidos
- Gestionar Tipos de Elección
- Gestionar Candidatos
- [Habilitar/Deshabilitar]
- [Editar]
- [Eliminar]

#### Pestaña: Monitoreo
- Ver progreso por departamento
- Gráficos en tiempo real
- Tabla de monitoreo
- Estado del sistema

#### Pestaña: Auditoría
- Ver logs del sistema
- Filtrar por usuario/acción
- Exportar logs

#### Pestaña: Incidentes
- Ver todos los incidentes
- Ver todos los delitos
- Información completa de contexto
- Filtrar por estado

#### Pestaña: Campañas
- [Crear Campaña]
- [Activar Campaña]
- [Resetear Campaña]
- [Eliminar Campaña]

#### Pestaña: Temas
- Configurar tema visual
- Colores personalizados

---

## 📊 TABLA COMPARATIVA: FUNCIONALIDADES POR ROL

| Funcionalidad | Testigo | Coord. Puesto | Coord. Municipal | Coord. Departamental | Super Admin |
|---------------|---------|---------------|------------------|---------------------|-------------|
| **Crear Formularios** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Validar Formularios** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Ver Consolidado** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Gestionar Incidentes** | ✅ Crear | ✅ Gestionar | ✅ Ver | ✅ Ver | ✅ Ver Todos |
| **Gestionar Delitos** | ✅ Crear | ✅ Gestionar | ✅ Ver | ✅ Ver | ✅ Ver Todos |
| **Ver Estadísticas** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Exportar Datos** | ❌ | ⏳ | ⏳ | ⏳ | ✅ |
| **Generar Reportes** | ❌ | ⏳ | ⏳ | ⏳ | ✅ |
| **Gestionar Usuarios** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Configurar Sistema** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Auto-refresh** | ✅ 30s | ✅ 30s | ✅ 60s | ✅ 60s | ✅ 30s |
| **Sincronización Offline** | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## ⚠️ INCONSISTENCIAS IDENTIFICADAS

### 1. Testigo vs Coordinadores - Gestión de Incidentes/Delitos

**Testigo**:
- ✅ Puede crear incidentes/delitos
- ❌ NO puede ver estado de seguimiento
- ❌ NO puede ver si fueron resueltos
- ❌ NO tiene filtros
- ❌ NO tiene búsqueda

**Coordinadores**:
- ✅ Pueden gestionar incidentes/delitos
- ✅ Pueden cambiar estado
- ✅ Pueden agregar seguimiento
- ✅ Tienen filtros por estado
- ✅ Ven historial completo

**Problema**: Testigo no sabe si su reporte fue atendido

**Solución Recomendada**:
```javascript
// Agregar en testigo:
- Badge de estado en cada incidente/delito
- Sección de "Seguimiento" (solo lectura)
- Notificación cuando cambia estado
- Filtro por estado
```

---

### 2. Testigo - Falta Panel de Estadísticas

**Testigo**:
- ❌ NO ve cuántos formularios ha creado
- ❌ NO ve cuántos fueron validados
- ❌ NO ve cuántos fueron rechazados
- ❌ NO ve su porcentaje de completado

**Coordinadores**:
- ✅ Ven estadísticas completas
- ✅ Ven progreso en tiempo real
- ✅ Ven métricas de calidad

**Problema**: Testigo no tiene feedback de su desempeño

**Solución Recomendada**:
```html
<!-- Agregar panel de estadísticas en dashboard del testigo -->
<div class="row mb-3">
    <div class="col-md-3">
        <div class="card">
            <div class="card-body">
                <h6>Formularios Creados</h6>
                <h3 id="totalFormularios">0</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body">
                <h6>Validados</h6>
                <h3 id="formulariosValidados" class="text-success">0</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body">
                <h6>Pendientes</h6>
                <h3 id="formulariosPendientes" class="text-warning">0</h3>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card">
            <div class="card-body">
                <h6>Rechazados</h6>
                <h3 id="formulariosRechazados" class="text-danger">0</h3>
            </div>
        </div>
    </div>
</div>
```

---

### 3. Testigo - Falta Información de Mesas

**Testigo**:
- ❌ NO ve lista de mesas del puesto
- ❌ NO ve cuáles mesas ya tienen formulario
- ❌ NO ve estado de cada mesa
- ❌ Solo ve selector dropdown

**Coordinadores**:
- ✅ Ven panel con todas las mesas
- ✅ Ven estado de cada mesa
- ✅ Ven qué testigo está asignado
- ✅ Ven si hay formulario

**Problema**: Testigo no tiene visibilidad del puesto

**Solución Recomendada**:
```html
<!-- Agregar panel de mesas en dashboard del testigo -->
<div class="card">
    <div class="card-header">
        <h6>Mesas del Puesto</h6>
    </div>
    <div class="card-body">
        <div id="panelMesas">
            <!-- Lista de mesas con estado -->
        </div>
    </div>
</div>
```

---

### 4. Exportación de Datos

**Testigo**:
- ❌ NO puede exportar sus formularios
- ❌ NO puede descargar respaldo

**Coordinadores**:
- ⏳ Exportación en desarrollo
- ⏳ Botones presentes pero no funcionales

**Super Admin**:
- ✅ Puede exportar todo

**Problema**: Nadie excepto Super Admin puede exportar

**Solución**: Implementar exportación para todos los roles

---

## ✅ RECOMENDACIONES DE MEJORA

### Para Testigo:

1. **Agregar Panel de Estadísticas** (Alta Prioridad)
   - Total formularios creados
   - Validados, pendientes, rechazados
   - Porcentaje de completado
   - Gráfico de progreso

2. **Mejorar Gestión de Incidentes/Delitos** (Alta Prioridad)
   - Mostrar estado actual
   - Mostrar seguimiento (solo lectura)
   - Agregar filtros por estado
   - Notificar cuando cambia estado

3. **Agregar Panel de Mesas** (Media Prioridad)
   - Lista de mesas del puesto
   - Estado de cada mesa
   - Indicador de formulario creado
   - Resaltar mesa actual

4. **Implementar Exportación** (Media Prioridad)
   - Exportar mis formularios a PDF
   - Descargar respaldo de datos
   - Exportar incidentes/delitos

5. **Agregar Pestaña de Ayuda** (Baja Prioridad)
   - Guía de uso
   - Preguntas frecuentes
   - Contacto de soporte

### Para Coordinadores:

1. **Completar Exportación** (Alta Prioridad)
   - Implementar exportación a CSV/Excel
   - Implementar generación de PDF
   - Agregar templates de reportes

2. **Mejorar Búsqueda y Filtros** (Media Prioridad)
   - Búsqueda avanzada
   - Filtros combinados
   - Guardar filtros favoritos

3. **Agregar Notificaciones** (Media Prioridad)
   - Notificar nuevos formularios
   - Notificar incidentes críticos
   - Notificar discrepancias

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### Testigo - Mejoras Pendientes:
- [ ] Panel de estadísticas en dashboard
- [ ] Estado de seguimiento en incidentes/delitos
- [ ] Filtros en incidentes/delitos
- [ ] Panel de mesas del puesto
- [ ] Exportación de formularios
- [ ] Pestaña de ayuda

### Coordinadores - Mejoras Pendientes:
- [ ] Exportación funcional
- [ ] Generación de PDF
- [ ] Búsqueda avanzada
- [ ] Notificaciones push

### General - Mejoras Pendientes:
- [ ] Estandarizar manejo de errores
- [ ] Unificar estilos de UI
- [ ] Agregar tooltips explicativos
- [ ] Mejorar responsive en móviles

---

*Análisis completado: $(date)*
*Estado: Listo para implementar mejoras*
