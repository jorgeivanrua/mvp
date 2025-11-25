# Implementation Plan - Sistema de Monitoreo en Tiempo Real

## Estado de Implementación

**Estado General:** 🟡 PARCIALMENTE COMPLETADO (50%)
**Fecha de Inicio:** 2025-11-22
**Fecha Actual:** 2025-11-25
**Implementado por:** Equipo de Desarrollo

---

## Tareas Completadas

- [x] 1. Configurar rol de monitoreo
- [x] 1.1 Agregar rol 'monitoreo' al modelo User
  - Agregar 'monitoreo' a la lista de roles válidos en CHECK constraint
  - Documentar que monitoreo no requiere ubicacion_id
  - _Archivo: backend/models/user.py_
  - _Requirements: 1.1, 1.2_

- [x] 1.2 Configurar autenticación para rol monitoreo
  - Permitir login sin ubicacion_id para rol monitoreo
  - Configurar permisos especiales para monitoreo
  - _Archivo: backend/services/auth_service.py_
  - _Requirements: 1.2_

- [x] 2. Crear API REST endpoints
- [x] 2.1 Crear Blueprint monitoreo_bp
  - Configurar prefix /monitoreo
  - Importar dependencias necesarias
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: Todos_

- [x] 2.2 Implementar GET /dashboard
  - Requerir autenticación JWT
  - Requerir rol monitoreo con @role_required('monitoreo')
  - Renderizar template monitoreo/dashboard.html
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 2.1_

- [x] 2.3 Implementar GET /api/usuarios-activos
  - Requerir autenticación JWT
  - Requerir rol monitoreo
  - Obtener todos los usuarios activos con geolocalización (sin filtros de jurisdicción)
  - Incluir: id, nombre, rol, latitud, longitud, precision, ultima_actualizacion, ubicacion, presencia_verificada
  - Retornar lista completa con total
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 1.3, 1.4, 1.5, 3.1, 3.2, 3.3_

- [x] 2.4 Implementar GET /api/estadisticas
  - Requerir autenticación JWT
  - Requerir rol monitoreo
  - Calcular estadísticas de testigos (total, con_geolocalizacion, con_presencia_verificada, porcentaje_geo)
  - Calcular estadísticas de coordinadores (total, con_geolocalizacion, porcentaje_geo)
  - Calcular estadísticas de formularios (total, validados, pendientes)
  - Retornar diccionario con todas las estadísticas
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 3. Crear componentes de frontend básicos
- [x] 3.1 Crear template base del dashboard
  - Crear archivo monitoreo/dashboard.html
  - Estructura HTML con secciones para: mapa, estadísticas, actividad, alertas
  - Incluir Leaflet.js para mapas
  - Incluir Chart.js para gráficos
  - _Archivo: frontend/templates/monitoreo/dashboard.html_
  - _Requirements: 2.1, 2.2_

- [x] 3.2 Implementar mapa global de usuarios
  - Inicializar mapa Leaflet centrado en Colombia
  - Función cargarUsuariosActivos() para obtener datos
  - Función agregarMarcadorUsuario() para cada usuario
  - Marcadores con colores según rol
  - Popups con información del usuario
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 3.3 Implementar panel de estadísticas
  - Función cargarEstadisticas() para obtener datos
  - Renderizar estadísticas de testigos
  - Renderizar estadísticas de coordinadores
  - Renderizar estadísticas de formularios
  - Mostrar porcentajes y progress bars
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 4. Registrar blueprint en aplicación
- [x] 4.1 Registrar monitoreo_bp en app.py
  - Importar blueprint
  - Registrar con app.register_blueprint()
  - _Archivo: backend/app.py_
  - _Requirements: Todos_

- [x] 5. Crear ruta de frontend
- [x] 5.1 Crear ruta /monitoreo/dashboard en frontend_bp
  - Renderizar template monitoreo/dashboard.html
  - _Archivo: backend/routes/frontend.py_
  - _Requirements: 2.1_

---

## Tareas Pendientes

- [ ] 6. Implementar endpoints adicionales
- [ ] 6.1 Implementar GET /api/actividad-reciente
  - Requerir autenticación JWT
  - Requerir rol monitoreo
  - Obtener últimos 50 eventos del sistema
  - Incluir: formularios creados, incidentes reportados, delitos reportados, presencias verificadas
  - Ordenar por timestamp descendente
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 6.2 Implementar GET /api/alertas
  - Requerir autenticación JWT
  - Requerir rol monitoreo
  - Obtener alertas críticas: incidentes críticos, delitos, testigos sin presencia 2+ horas
  - Incluir estado de alerta (nueva, vista, resuelta)
  - Ordenar por timestamp descendente
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 6.3 Implementar GET /api/incidentes
  - Requerir autenticación JWT
  - Requerir rol monitoreo
  - Obtener todos los incidentes sin filtros de jurisdicción
  - Aplicar filtros opcionales (tipo, estado, severidad, fecha, ubicación)
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 7.1, 7.3, 7.4, 7.5_

- [ ] 6.4 Implementar GET /api/delitos
  - Requerir autenticación JWT
  - Requerir rol monitoreo
  - Obtener todos los delitos sin filtros de jurisdicción
  - Aplicar filtros opcionales (tipo, estado, gravedad, fecha, ubicación)
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 7.2, 7.3, 7.4, 7.5_

- [ ] 6.5 Implementar POST /api/exportar
  - Requerir autenticación JWT
  - Requerir rol monitoreo
  - Aceptar parámetros: tipo_datos (usuarios, formularios, incidentes, delitos, estadísticas), formato (excel, csv, pdf)
  - Generar archivo según formato
  - Retornar archivo para descarga
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 7. Completar componentes de frontend
- [ ] 7.1 Implementar auto-refresh
  - Función iniciarAutoRefresh() que ejecuta cada 30 segundos
  - Refrescar: mapa, estadísticas, actividad, alertas
  - Detener auto-refresh al salir del dashboard
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 2.4, 2.5_

- [ ] 7.2 Implementar filtros por rol en mapa
  - Checkboxes para cada rol (testigos, coordinadores)
  - Función filtrarPorRol() que muestra/oculta marcadores
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 3.4_

- [ ] 7.3 Implementar feed de actividad reciente
  - Función cargarActividadReciente() para obtener datos
  - Renderizar lista de eventos con: tipo, descripción, usuario, ubicación, timestamp
  - Click en evento navega a detalle
  - Auto-refresh cada 30 segundos
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 7.4 Implementar panel de alertas
  - Función cargarAlertas() para obtener datos
  - Renderizar alertas con: tipo, descripción, timestamp, estado
  - Badge con contador de alertas nuevas
  - Click en alerta marca como vista y navega a detalle
  - Auto-refresh cada 30 segundos
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 7.5 Implementar filtros avanzados
  - Panel de filtros con opciones para: rol, estado, departamento, municipio, fecha
  - Función aplicarFiltros() que actualiza todos los componentes
  - Botón "Limpiar Filtros"
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 7.6 Implementar búsqueda global
  - Campo de búsqueda en header del dashboard
  - Función buscarGlobal() que busca en: usuarios, formularios, incidentes, delitos
  - Mostrar resultados con tipo de dato y campos relevantes
  - Click en resultado navega a detalle
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 7.7 Implementar mapa de calor
  - Función cargarMapaCalor() para calcular densidad de actividad
  - Usar Leaflet.heat plugin
  - Considerar: número de usuarios, formularios, reportes
  - Gradiente de colores (azul=bajo, amarillo=medio, rojo=alto)
  - Hover muestra contador de actividad
  - Click filtra datos por área
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ] 7.8 Implementar comparación entre departamentos
  - Función cargarComparacionDepartamentos() para obtener datos
  - Tabla o gráfico con métricas por departamento
  - Métricas: total mesas, formularios completados, porcentaje avance, incidentes, delitos
  - Ordenar por porcentaje de avance
  - Click en departamento filtra todos los datos
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ] 7.9 Implementar exportación de datos
  - Botón "Exportar" con dropdown de opciones
  - Modal para seleccionar: tipo de datos, formato
  - Función exportarDatos() que llama a POST /api/exportar
  - Descargar archivo generado
  - _Archivo: frontend/templates/monitoreo/dashboard.html (script section)_
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 8. Implementar seguridad y logging
- [ ] 8.1 Implementar logging de accesos
  - Registrar cada acceso al dashboard de monitoreo
  - Incluir: usuario, timestamp, IP, acción
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 15.2_

- [ ] 8.2 Implementar validación de permisos
  - Verificar que solo super_admin puede crear usuarios monitoreo
  - Verificar que usuarios desactivados no pueden acceder
  - _Archivo: backend/routes/super_admin.py, backend/routes/monitoreo.py_
  - _Requirements: 15.3, 15.4_

- [ ] 8.3 Implementar enmascaramiento de datos sensibles
  - Enmascarar números de teléfono parcialmente
  - Enmascarar información personal sensible
  - _Archivo: backend/routes/monitoreo.py_
  - _Requirements: 15.5_

- [ ] 9. Crear migraciones de base de datos
- [ ] 9.1 Crear migración para agregar rol monitoreo
  - Actualizar CHECK constraint en users table
  - _Requirements: 1.1_

- [ ] 10. Documentación
- [ ] 10.1 Documentar API endpoints
  - Documentar todos los endpoints de monitoreo
  - Incluir request/response examples
  - _Archivo: Este documento (design.md)_

- [ ] 10.2 Crear guía de usuario para monitoreo
  - Guía paso a paso para usar el dashboard
  - Explicar cada componente y funcionalidad
  - _Archivo: md_funciones/GUIA_MONITOREO.md_

---

## Resumen de Implementación

### Estado Actual: 50% Completado

**Funcionalidades Implementadas (✅):**
- ✅ Rol de monitoreo configurado
- ✅ Autenticación y autorización
- ✅ Endpoint GET /dashboard
- ✅ Endpoint GET /api/usuarios-activos
- ✅ Endpoint GET /api/estadisticas
- ✅ Template base del dashboard
- ✅ Mapa global de usuarios
- ✅ Panel de estadísticas básicas
- ✅ Blueprint registrado

**Funcionalidades Pendientes (⏳):**
- ⏳ Endpoint GET /api/actividad-reciente
- ⏳ Endpoint GET /api/alertas
- ⏳ Endpoint GET /api/incidentes (sin filtros de jurisdicción)
- ⏳ Endpoint GET /api/delitos (sin filtros de jurisdicción)
- ⏳ Endpoint POST /api/exportar
- ⏳ Auto-refresh cada 30 segundos
- ⏳ Filtros por rol en mapa
- ⏳ Feed de actividad reciente
- ⏳ Panel de alertas
- ⏳ Filtros avanzados
- ⏳ Búsqueda global
- ⏳ Mapa de calor de actividad
- ⏳ Comparación entre departamentos
- ⏳ Exportación de datos
- ⏳ Logging de accesos
- ⏳ Enmascaramiento de datos sensibles

### Archivos Creados/Modificados

**Completados:**
1. **backend/models/user.py** - Rol monitoreo agregado
2. **backend/services/auth_service.py** - Autenticación sin ubicacion_id para monitoreo
3. **backend/routes/monitoreo.py** - Blueprint con 3 endpoints
4. **frontend/templates/monitoreo/dashboard.html** - Dashboard básico
5. **backend/app.py** - Blueprint registrado
6. **backend/routes/frontend.py** - Ruta de frontend

**Pendientes:**
7. **backend/routes/monitoreo.py** - 5 endpoints adicionales
8. **frontend/templates/monitoreo/dashboard.html** - 7 componentes adicionales
9. **backend/migrations/** - Migración para rol monitoreo
10. **md_funciones/GUIA_MONITOREO.md** - Guía de usuario

### Endpoints Implementados

**Completados (3/8):**
1. ✅ `GET /monitoreo/dashboard` - Render dashboard
2. ✅ `GET /monitoreo/api/usuarios-activos` - Todos los usuarios con GPS
3. ✅ `GET /monitoreo/api/estadisticas` - Estadísticas globales

**Pendientes (5/8):**
4. ⏳ `GET /monitoreo/api/actividad-reciente` - Últimos eventos
5. ⏳ `GET /monitoreo/api/alertas` - Alertas críticas
6. ⏳ `GET /monitoreo/api/incidentes` - Todos los incidentes
7. ⏳ `GET /monitoreo/api/delitos` - Todos los delitos
8. ⏳ `POST /monitoreo/api/exportar` - Exportar datos

### Componentes de Frontend

**Completados (3/10):**
1. ✅ Template base del dashboard
2. ✅ Mapa global de usuarios
3. ✅ Panel de estadísticas

**Pendientes (7/10):**
4. ⏳ Auto-refresh cada 30 segundos
5. ⏳ Feed de actividad reciente
6. ⏳ Panel de alertas
7. ⏳ Filtros avanzados
8. ⏳ Búsqueda global
9. ⏳ Mapa de calor
10. ⏳ Comparación entre departamentos

---

## Notas de Implementación

- El sistema está 50% funcional con funcionalidades básicas
- El rol de monitoreo está configurado y funciona correctamente
- Los endpoints básicos (usuarios-activos, estadísticas) están implementados
- El dashboard tiene estructura básica con mapa y estadísticas
- Falta implementar: auto-refresh, alertas, actividad reciente, filtros avanzados, búsqueda, exportación
- El sistema no aplica filtros de jurisdicción para rol monitoreo
- La autorización está implementada con @role_required('monitoreo')
- El mapa muestra todos los usuarios con GPS sin restricciones

---

**Fecha de Creación:** 2025-11-25
**Última Actualización:** 2025-11-25
**Estado:** 🟡 PARCIALMENTE COMPLETADO (50%)
**Implementado por:** Equipo de Desarrollo

