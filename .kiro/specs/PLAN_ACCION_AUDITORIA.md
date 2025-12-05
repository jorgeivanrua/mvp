# Plan de Acción: Auditoría y Corrección de Dashboards

## Fecha: 5 de Diciembre de 2024

## Resumen Ejecutivo

Se ha realizado una auditoría completa de todos los roles y dashboards del sistema electoral. Se identificaron problemas menores y se creó el dashboard faltante para el rol de Auditor Electoral.

## Hallazgos Principales

### ✅ Completado
1. **Dashboard de Auditor Electoral Creado**
   - Template: `frontend/templates/auditor/dashboard.html`
   - JavaScript: `frontend/static/js/auditor-dashboard.js` (ya existía)
   - Funcionalidades: Formularios, anomalías, incidentes, mapa, reportes

### ⚠️ Pendiente de Verificación

#### 1. Super Admin Dashboard
**Archivo**: `frontend/templates/admin/super-admin-dashboard.html`
**Estado**: Implementado, requiere verificación

**Verificaciones Pendientes**:
- [ ] Verificar carga de datos de usuarios desde BD
- [ ] Verificar carga de partidos desde BD (✅ implementado recientemente)
- [ ] Verificar carga de candidatos desde BD (✅ implementado recientemente)
- [ ] Verificar mapa con filtros y búsqueda (✅ implementado recientemente)
- [ ] Verificar estadísticas en tiempo real
- [ ] Verificar gestión de usuarios funciona
- [ ] Verificar configuración del sistema
- [ ] Verificar personalización (logos, colores)
- [ ] Verificar carga masiva CSV

**Errores Potenciales a Revisar**:
- Errores de JavaScript en consola
- Errores de ortografía en textos
- Endpoints que no existen
- Datos hardcodeados en lugar de BD

#### 2. Coordinador Departamental Dashboard
**Archivo**: `frontend/templates/coordinador/departamental.html`
**Estado**: Implementado, requiere verificación

**Verificaciones Pendientes**:
- [ ] Verificar filtrado por departamento del usuario
- [ ] Verificar que solo ve datos de su departamento
- [ ] Verificar carga de municipios desde BD
- [ ] Verificar mapa filtra correctamente
- [ ] Verificar estadísticas agregadas
- [ ] Verificar formularios E-24 departamentales
- [ ] Verificar incidentes y delitos filtrados

#### 3. Coordinador Municipal Dashboard
**Archivo**: `frontend/templates/coordinador/municipal.html`
**Estado**: Implementado, requiere verificación

**Verificaciones Pendientes**:
- [ ] Verificar filtrado por municipio del usuario
- [ ] Verificar que solo ve datos de su municipio
- [ ] Verificar carga de puestos desde BD
- [ ] Verificar mapa filtra correctamente
- [ ] Verificar estadísticas agregadas
- [ ] Verificar formularios E-24 municipales
- [ ] Verificar incidentes y delitos filtrados

#### 4. Coordinador de Puesto Dashboard
**Archivo**: `frontend/templates/coordinador/puesto.html`
**Estado**: Implementado, requiere verificación

**Verificaciones Pendientes**:
- [ ] Verificar filtrado por puesto del usuario
- [ ] Verificar que solo ve datos de su puesto
- [ ] Verificar carga de mesas desde BD
- [ ] Verificar formularios E-14 del puesto
- [ ] Verificar validación de formularios
- [ ] Verificar formularios E-24 del puesto
- [ ] Verificar incidentes y delitos filtrados

**Nota**: Existe también `puesto-mejorado.html` - verificar cuál se usa

#### 5. Testigo Electoral Dashboard
**Archivo**: `frontend/templates/testigo/dashboard.html`
**Estado**: Implementado, requiere verificación

**Verificaciones Pendientes**:
- [ ] Verificar carga de mesa asignada
- [ ] Verificar formulario E-14 funciona
- [ ] Verificar reporte de incidentes
- [ ] Verificar reporte de delitos
- [ ] Verificar geolocalización
- [ ] Verificar modo offline

#### 6. Monitoreo Dashboard
**Archivo**: `frontend/templates/monitoreo/dashboard_simple.html`
**Estado**: Implementado, requiere verificación

**Verificaciones Pendientes**:
- [ ] Verificar actualización en tiempo real
- [ ] Verificar WebSocket conectado
- [ ] Verificar mapa con todos los puestos
- [ ] Verificar estadísticas en tiempo real
- [ ] Verificar alertas funcionan

## Plan de Acción Detallado

### Fase 1: Verificación de Endpoints Backend (Prioridad Alta)

**Objetivo**: Asegurar que todos los endpoints existen y funcionan

**Tareas**:
1. [ ] Crear endpoint `/api/auditor/stats` para estadísticas de auditor
2. [ ] Crear endpoint `/api/auditor/formularios` para lista de formularios
3. [ ] Crear endpoint `/api/auditor/discrepancias` para anomalías
4. [ ] Crear endpoint `/api/auditor/municipios` para estadísticas por municipio
5. [ ] Crear endpoint `/api/auditor/consolidado` para resultados consolidados
6. [ ] Crear endpoint `/api/auditor/exportar` para exportación de reportes
7. [ ] Verificar todos los endpoints de coordinadores funcionan
8. [ ] Verificar todos los endpoints de monitoreo funcionan

### Fase 2: Actualización de JavaScript (Prioridad Alta)

**Objetivo**: Actualizar JavaScript para que funcione con nuevos templates

**Tareas**:
1. [ ] Actualizar `auditor-dashboard.js` para nuevo template
2. [ ] Verificar `super-admin-dashboard.js` funciona correctamente
3. [ ] Verificar `mapa-geolocalizacion.js` con filtros y búsqueda
4. [ ] Verificar `partidos-manager.js` funciona
5. [ ] Verificar `candidatos-manager.js` funciona
6. [ ] Verificar scripts de coordinadores funcionan
7. [ ] Verificar scripts de testigo funcionan
8. [ ] Verificar scripts de monitoreo funcionan

### Fase 3: Corrección de Errores (Prioridad Media)

**Objetivo**: Corregir errores de ortografía y JavaScript

**Tareas**:
1. [ ] Revisar todos los templates para errores de ortografía
2. [ ] Revisar todos los mensajes de error/éxito
3. [ ] Revisar todos los labels y placeholders
4. [ ] Corregir errores de JavaScript en consola
5. [ ] Corregir warnings de JavaScript
6. [ ] Optimizar queries lentas
7. [ ] Agregar manejo de errores faltante

### Fase 4: Pruebas de Integración (Prioridad Media)

**Objetivo**: Probar cada dashboard end-to-end

**Tareas**:
1. [ ] Probar Super Admin dashboard completo
2. [ ] Probar Coordinador Departamental dashboard
3. [ ] Probar Coordinador Municipal dashboard
4. [ ] Probar Coordinador de Puesto dashboard
5. [ ] Probar Testigo Electoral dashboard
6. [ ] Probar Auditor Electoral dashboard
7. [ ] Probar Monitoreo dashboard
8. [ ] Documentar bugs encontrados

### Fase 5: Optimización (Prioridad Baja)

**Objetivo**: Mejorar rendimiento y UX

**Tareas**:
1. [ ] Optimizar carga de datos con paginación
2. [ ] Implementar caching donde sea necesario
3. [ ] Optimizar queries de base de datos
4. [ ] Mejorar responsive design
5. [ ] Agregar loading states
6. [ ] Agregar skeleton loaders
7. [ ] Mejorar mensajes de error

### Fase 6: Documentación (Prioridad Baja)

**Objetivo**: Documentar cada dashboard

**Tareas**:
1. [ ] Documentar funcionalidades de Super Admin
2. [ ] Documentar funcionalidades de Coordinadores
3. [ ] Documentar funcionalidades de Testigo
4. [ ] Documentar funcionalidades de Auditor
5. [ ] Documentar funcionalidades de Monitoreo
6. [ ] Crear guías de usuario
7. [ ] Crear videos tutoriales

## Problemas Específicos Detectados

### 1. Template Duplicado de Coordinador de Puesto
**Archivos**:
- `frontend/templates/coordinador/puesto.html`
- `frontend/templates/coordinador/puesto-mejorado.html`

**Acción**: Verificar cuál se usa y eliminar el obsoleto

### 2. Dashboard Optimizado sin Uso
**Archivo**: `frontend/templates/dashboard/super-admin-dashboard-optimized.html`

**Acción**: Verificar si se usa o eliminar

### 3. Endpoints de Auditor Faltantes
**Endpoints necesarios**:
- `/api/auditor/stats`
- `/api/auditor/formularios`
- `/api/auditor/discrepancias`
- `/api/auditor/municipios`
- `/api/auditor/consolidado`
- `/api/auditor/exportar`

**Acción**: Crear todos los endpoints en `backend/routes/auditor.py`

## Estimación de Esfuerzo

| Fase | Tareas | Estimación |
|------|--------|------------|
| Fase 1: Endpoints Backend | 8 tareas | 1-2 días |
| Fase 2: JavaScript | 8 tareas | 1-2 días |
| Fase 3: Corrección de Errores | 7 tareas | 1 día |
| Fase 4: Pruebas | 8 tareas | 2-3 días |
| Fase 5: Optimización | 7 tareas | 1-2 días |
| Fase 6: Documentación | 7 tareas | 1-2 días |
| **Total** | **45 tareas** | **7-12 días** |

## Prioridades Inmediatas

### ✅ Completado (5 de Diciembre, 2024)
1. ✅ Crear dashboard de Auditor Electoral
2. ✅ Crear endpoints de Auditor
3. ✅ Actualizar JavaScript de Auditor para nuevo template

### Alta Prioridad (Esta Semana)
1. Verificar Super Admin dashboard funciona
2. Verificar Coordinadores dashboards funcionan
3. Verificar Testigo dashboard funciona
4. Verificar Monitoreo dashboard funciona
5. Corregir errores críticos de JavaScript

### Media Prioridad (Próxima Semana)
1. Pruebas de integración completas
2. Corrección de errores de ortografía
3. Optimización de queries
4. Mejoras de UX

### Baja Prioridad (Cuando sea posible)
1. Documentación completa
2. Videos tutoriales
3. Optimizaciones avanzadas

## Métricas de Éxito

- [ ] 0 errores de JavaScript en consola
- [ ] 0 errores de ortografía en UI
- [ ] 100% de endpoints funcionando
- [ ] 100% de dashboards funcionando
- [ ] Tiempo de carga < 2 segundos
- [ ] Todos los datos vienen de BD (no hardcodeados)
- [ ] Todos los filtros funcionan correctamente
- [ ] Todas las búsquedas funcionan correctamente

## Próximos Pasos Inmediatos

1. **Commit y Push** del dashboard de Auditor creado
2. **Crear endpoints** de Auditor en backend
3. **Verificar** Super Admin dashboard
4. **Verificar** Coordinadores dashboards
5. **Documentar** bugs encontrados

