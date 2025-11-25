# Implementation Plan - Sistema de Incidentes y Delitos Electorales

## Estado de Implementación

**Estado General:** ✅ COMPLETADO (100%)
**Fecha de Inicio:** 2025-11-19
**Fecha de Finalización:** 2025-11-24
**Implementado por:** Equipo de Desarrollo

---

## Tareas Completadas

- [x] 1. Crear modelos de datos
- [x] 1.1 Crear modelo IncidenteElectoral
  - Implementar campos de identificación y ubicación
  - Implementar campos de información del incidente
  - Implementar campos de evidencia y fechas
  - Implementar campos de resolución
  - Definir TIPOS_INCIDENTE, SEVERIDADES, ESTADOS
  - Implementar método to_dict()
  - _Archivo: backend/models/incidentes_delitos.py_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 3.1, 9.1, 9.2, 9.3, 9.4_

- [x] 1.2 Crear modelo DelitoElectoral
  - Implementar campos de identificación y ubicación
  - Implementar campos de información del delito
  - Implementar campos de evidencia, testigos y fechas
  - Implementar campos de investigación
  - Implementar campos de denuncia formal
  - Definir TIPOS_DELITO, GRAVEDADES, ESTADOS
  - Implementar método to_dict()
  - _Archivo: backend/models/incidentes_delitos.py_
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 6.1, 10.1, 10.2, 10.3, 10.4, 10.5, 14.1, 14.2, 14.3, 14.4, 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 1.3 Crear modelo SeguimientoReporte
  - Implementar campos: tipo_reporte, reporte_id, usuario_id, accion, comentario, estado_anterior, estado_nuevo, created_at
  - Implementar método to_dict()
  - _Archivo: backend/models/incidentes_delitos.py_
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 1.4 Crear modelo NotificacionReporte
  - Implementar campos: usuario_id, tipo_reporte, reporte_id, tipo_notificacion, titulo, mensaje, leida, fecha_lectura, created_at
  - Implementar método marcar_como_leida()
  - Implementar método to_dict()
  - _Archivo: backend/models/incidentes_delitos.py_
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 2. Crear servicio de lógica de negocio
- [x] 2.1 Crear clase IncidentesDelitosService
  - Crear archivo de servicio
  - Importar modelos y dependencias
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: Todos_

- [x] 2.2 Implementar crear_incidente()
  - Obtener información del usuario
  - Determinar ubicaciones (puesto, municipio, departamento) basadas en mesa_id
  - Crear instancia de IncidenteElectoral
  - Registrar seguimiento
  - Crear notificaciones
  - Commit a base de datos
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 11.1, 12.1, 12.2_

- [x] 2.3 Implementar crear_delito()
  - Obtener información del usuario
  - Determinar ubicaciones basadas en mesa_id
  - Crear instancia de DelitoElectoral
  - Registrar seguimiento
  - Crear notificaciones (más urgentes que incidentes)
  - Commit a base de datos
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 11.1, 12.3_

- [x] 2.4 Implementar obtener_incidentes()
  - Construir query base
  - Aplicar filtros de permisos según rol (testigo, coordinador_puesto, coordinador_municipal, coordinador_departamental, super_admin, auditor)
  - Aplicar filtros adicionales (estado, severidad, tipo_incidente, fecha_desde, fecha_hasta)
  - Ordenar por fecha_reporte descendente
  - Retornar lista de incidentes serializados
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5, 19.1, 19.2, 19.3, 19.4, 19.5_

- [x] 2.5 Implementar obtener_delitos()
  - Construir query base
  - Aplicar filtros de permisos según rol
  - Aplicar filtros adicionales (estado, gravedad, tipo_delito, fecha_desde, fecha_hasta)
  - Ordenar por fecha_reporte descendente
  - Retornar lista de delitos serializados
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5, 19.1, 19.2, 19.3, 19.4, 19.5_

- [x] 2.6 Implementar actualizar_estado_incidente()
  - Obtener incidente por ID
  - Actualizar estado
  - Si estado es 'resuelto', actualizar resuelto_por_id, fecha_resolucion, notas_resolucion
  - Registrar seguimiento con cambio de estado
  - Commit a base de datos
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 9.2, 9.3, 9.4, 9.5, 13.1, 13.2, 13.3, 13.4, 13.5_

- [x] 2.7 Implementar actualizar_estado_delito()
  - Obtener delito por ID
  - Actualizar estado
  - Si estado es 'en_investigacion', actualizar investigado_por_id, fecha_investigacion
  - Si estado es 'investigado', actualizar resultado_investigacion
  - Registrar seguimiento con cambio de estado
  - Commit a base de datos
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 10.2, 10.3, 10.4, 10.5, 14.1, 14.2, 14.3, 14.4, 14.5_

- [x] 2.8 Implementar denunciar_formalmente()
  - Obtener delito por ID
  - Actualizar denunciado_formalmente a True
  - Actualizar numero_denuncia, autoridad_competente, fecha_denuncia
  - Cambiar estado a 'denunciado'
  - Registrar seguimiento
  - Commit a base de datos
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 2.9 Implementar obtener_estadisticas()
  - Construir queries con filtros de permisos según rol
  - Calcular total de incidentes y delitos
  - Calcular breakdown por estado (incidentes y delitos)
  - Calcular breakdown por severidad (incidentes)
  - Calcular breakdown por gravedad (delitos)
  - Calcular delitos denunciados formalmente
  - Retornar diccionario con estadísticas
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [x] 2.10 Implementar _registrar_seguimiento()
  - Crear instancia de SeguimientoReporte
  - Registrar tipo_reporte, reporte_id, usuario_id, accion, comentario, estado_anterior, estado_nuevo
  - Agregar a sesión (no commit, se hace en método principal)
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 11.1, 11.2_

- [x] 2.11 Implementar _crear_notificaciones_incidente()
  - Notificar a coordinador_puesto del puesto afectado
  - Si severidad es 'critica', notificar también a coordinador_municipal
  - Crear instancias de NotificacionReporte
  - Agregar a sesión
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 12.1, 12.2_

- [x] 2.12 Implementar _crear_notificaciones_delito()
  - Notificar a coordinador_municipal del municipio afectado
  - Notificar a coordinador_departamental del departamento afectado
  - Notificar a todos los auditor_electoral
  - Crear instancias de NotificacionReporte
  - Agregar a sesión
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 12.3_

- [x] 2.13 Implementar obtener_seguimiento()
  - Obtener seguimientos por tipo_reporte y reporte_id
  - Ordenar por created_at descendente
  - Retornar lista serializada
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 11.3, 11.4_

- [x] 2.14 Implementar obtener_notificaciones()
  - Obtener notificaciones por usuario_id
  - Filtrar por leida si solo_no_leidas=True
  - Ordenar por created_at descendente
  - Retornar lista serializada
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 12.5_

- [x] 2.15 Implementar marcar_notificacion_leida()
  - Obtener notificación por ID
  - Llamar método marcar_como_leida()
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 12.5_

- [x] 3. Crear API REST endpoints
- [x] 3.1 Crear rutas para incidentes
  - POST /api/incidentes - Crear incidente
  - GET /api/incidentes - Listar incidentes con filtros
  - GET /api/incidentes/:id - Obtener detalle de incidente
  - PUT /api/incidentes/:id - Actualizar estado de incidente
  - GET /api/incidentes/:id/seguimiento - Obtener seguimiento de incidente
  - _Archivo: backend/routes/incidentes.py_
  - _Requirements: 1.1, 9.2, 9.3, 9.4, 11.3, 13.1, 17.1, 17.2, 17.3, 17.4, 17.5_

- [x] 3.2 Crear rutas para delitos
  - POST /api/delitos - Crear delito
  - GET /api/delitos - Listar delitos con filtros
  - GET /api/delitos/:id - Obtener detalle de delito
  - PUT /api/delitos/:id - Actualizar estado de delito
  - POST /api/delitos/:id/denunciar - Registrar denuncia formal
  - GET /api/delitos/:id/seguimiento - Obtener seguimiento de delito
  - _Archivo: backend/routes/delitos.py_
  - _Requirements: 4.1, 10.2, 10.3, 10.4, 11.3, 14.1, 15.1, 17.1, 17.2, 17.3, 17.4, 17.5_

- [x] 3.3 Crear rutas para estadísticas y notificaciones
  - GET /api/reportes/estadisticas - Obtener estadísticas
  - GET /api/reportes/notificaciones - Obtener notificaciones del usuario
  - PUT /api/reportes/notificaciones/:id/leer - Marcar notificación como leída
  - _Archivo: backend/routes/reportes.py_
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5, 12.5_

- [x] 4. Implementar componentes de frontend
- [x] 4.1 Crear formulario de reporte de incidentes
  - Selector de tipo de incidente
  - Campo de título
  - Campo de descripción (textarea)
  - Selector de severidad
  - Selector de mesa (si aplica)
  - Campo de evidencia (file upload)
  - Botón de captura de GPS
  - Botón "Reportar Incidente"
  - _Archivo: frontend/templates/testigo_dashboard.html (y otros dashboards)_
  - _Requirements: 1.1, 2.1, 3.1, 7.1, 8.1_

- [x] 4.2 Crear formulario de reporte de delitos
  - Selector de tipo de delito
  - Campo de título
  - Campo de descripción (textarea)
  - Selector de gravedad
  - Selector de mesa (si aplica)
  - Campo de evidencia (file upload)
  - Campo de testigos adicionales (textarea)
  - Botón de captura de GPS
  - Botón "Reportar Delito"
  - _Archivo: frontend/templates/testigo_dashboard.html (y otros dashboards)_
  - _Requirements: 4.1, 5.1, 6.1, 7.1, 8.1_

- [x] 4.3 Crear lista de reportes con filtros
  - Tabla con columnas: Tipo, Título, Estado, Severidad/Gravedad, Fecha, Acciones
  - Filtros: Estado, Severidad/Gravedad, Tipo, Rango de fechas
  - Paginación
  - Botón "Ver Detalle" por cada reporte
  - Indicadores de color según estado y severidad/gravedad
  - _Archivo: frontend/templates/coordinador_puesto_dashboard.html (y otros coordinadores)_
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

- [x] 4.4 Crear vista de detalle de reporte
  - Información completa del reporte
  - Evidencia adjunta (con preview)
  - Mapa con ubicación GPS (si disponible)
  - Historial de seguimiento
  - Botones de acción según rol (Resolver, Investigar, Denunciar, Escalar)
  - _Archivo: frontend/templates/detalle_reporte.html_
  - _Requirements: 7.3, 8.3, 11.3, 11.4, 13.1, 14.1, 15.1, 16.1_

- [x] 4.5 Crear panel de notificaciones
  - Lista de notificaciones no leídas
  - Badge con contador de notificaciones
  - Notificaciones en tiempo real (polling cada 30 segundos)
  - Botón "Marcar como leída"
  - Link a detalle del reporte
  - _Archivo: frontend/templates/base.html (header)_
  - _Requirements: 12.5_

- [x] 4.6 Crear dashboard de estadísticas
  - Gráfico de incidentes por estado
  - Gráfico de incidentes por severidad
  - Gráfico de delitos por estado
  - Gráfico de delitos por gravedad
  - Contador de delitos denunciados
  - Totales generales
  - _Archivo: frontend/templates/estadisticas_reportes.html_
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [x] 5. Implementar lógica JavaScript
- [x] 5.1 Implementar función crearIncidente()
  - Recopilar datos del formulario
  - Capturar GPS si está disponible
  - Enviar POST a /api/incidentes
  - Mostrar mensaje de éxito/error
  - Limpiar formulario
  - Recargar lista de reportes
  - _Archivo: frontend/templates/testigo_dashboard.html (script section)_
  - _Requirements: 1.1, 8.1_

- [x] 5.2 Implementar función crearDelito()
  - Recopilar datos del formulario
  - Capturar GPS si está disponible
  - Enviar POST a /api/delitos
  - Mostrar mensaje de éxito/error
  - Limpiar formulario
  - Recargar lista de reportes
  - _Archivo: frontend/templates/testigo_dashboard.html (script section)_
  - _Requirements: 4.1, 8.1_

- [x] 5.3 Implementar función cargarReportes()
  - Obtener filtros seleccionados
  - Enviar GET a /api/incidentes o /api/delitos con filtros
  - Renderizar tabla con reportes
  - Aplicar colores según estado y severidad/gravedad
  - _Archivo: frontend/templates/coordinador_puesto_dashboard.html (script section)_
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

- [x] 5.4 Implementar función actualizarEstado()
  - Enviar PUT a /api/incidentes/:id o /api/delitos/:id
  - Incluir nuevo estado y comentario
  - Mostrar mensaje de éxito/error
  - Recargar detalle del reporte
  - _Archivo: frontend/templates/detalle_reporte.html (script section)_
  - _Requirements: 9.2, 9.3, 9.4, 10.2, 10.3, 10.4_

- [x] 5.5 Implementar función denunciarFormalmente()
  - Mostrar modal con campos: numero_denuncia, autoridad_competente
  - Enviar POST a /api/delitos/:id/denunciar
  - Mostrar mensaje de éxito/error
  - Recargar detalle del delito
  - _Archivo: frontend/templates/detalle_reporte.html (script section)_
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 5.6 Implementar función cargarNotificaciones()
  - Enviar GET a /api/reportes/notificaciones
  - Actualizar badge con contador
  - Renderizar lista de notificaciones
  - Polling cada 30 segundos
  - _Archivo: frontend/templates/base.html (script section)_
  - _Requirements: 12.5_

- [x] 5.7 Implementar función cargarEstadisticas()
  - Enviar GET a /api/reportes/estadisticas
  - Renderizar gráficos con Chart.js
  - Mostrar totales
  - _Archivo: frontend/templates/estadisticas_reportes.html (script section)_
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [x] 6. Crear migraciones de base de datos
- [x] 6.1 Crear migración para tabla incidentes_electorales
  - Crear tabla con todos los campos
  - Crear foreign keys
  - Crear índices
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 6.2 Crear migración para tabla delitos_electorales
  - Crear tabla con todos los campos
  - Crear foreign keys
  - Crear índices
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 6.3 Crear migración para tabla seguimiento_reportes
  - Crear tabla con todos los campos
  - Crear foreign keys
  - Crear índices
  - _Requirements: 11.1, 11.2_

- [x] 6.4 Crear migración para tabla notificaciones_reportes
  - Crear tabla con todos los campos
  - Crear foreign keys
  - Crear índices
  - _Requirements: 12.1, 12.2, 12.3, 12.4_

- [x] 7. Implementar validaciones y seguridad
- [x] 7.1 Validar tipos de incidentes y delitos
  - Validar que tipo_incidente esté en TIPOS_INCIDENTE
  - Validar que tipo_delito esté en TIPOS_DELITO
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 2.4, 5.4_

- [x] 7.2 Validar permisos de visualización
  - Implementar filtrado por rol en obtener_incidentes()
  - Implementar filtrado por rol en obtener_delitos()
  - _Archivo: backend/services/incidentes_delitos_service.py_
  - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5_

- [x] 7.3 Validar permisos de actualización
  - Solo coordinadores pueden resolver incidentes
  - Solo auditores pueden investigar delitos
  - _Archivo: backend/routes/incidentes.py, backend/routes/delitos.py_
  - _Requirements: 13.1, 14.1_

- [x] 8. Documentación
- [x] 8.1 Documentar modelos de datos
  - Documentar IncidenteElectoral
  - Documentar DelitoElectoral
  - Documentar SeguimientoReporte
  - Documentar NotificacionReporte
  - _Archivo: Este documento (design.md)_

- [x] 8.2 Documentar servicio
  - Documentar IncidentesDelitosService
  - Documentar todos los métodos públicos y privados
  - _Archivo: Este documento (design.md)_

- [x] 8.3 Documentar API endpoints
  - Documentar rutas de incidentes
  - Documentar rutas de delitos
  - Documentar rutas de estadísticas y notificaciones
  - _Archivo: Este documento (design.md)_

---

## Resumen de Implementación

### Archivos Creados/Modificados

1. **backend/models/incidentes_delitos.py** - 4 modelos completos
2. **backend/services/incidentes_delitos_service.py** - Servicio con 15 métodos
3. **backend/routes/incidentes.py** - API REST para incidentes
4. **backend/routes/delitos.py** - API REST para delitos
5. **backend/routes/reportes.py** - API REST para estadísticas y notificaciones
6. **frontend/templates/** - Formularios, listas, detalles, estadísticas
7. **backend/migrations/** - 4 migraciones de base de datos

### Funcionalidades Implementadas

✅ Reporte de incidentes electorales (8 tipos)
✅ Reporte de delitos electorales (9 tipos)
✅ Niveles de severidad (4 niveles) y gravedad (4 niveles)
✅ Adjuntar evidencias (fotos, videos, documentos)
✅ Geolocalización de reportes
✅ Estados de incidentes (4 estados)
✅ Estados de delitos (5 estados)
✅ Seguimiento detallado con historial
✅ Notificaciones automáticas a supervisores
✅ Resolución de incidentes
✅ Investigación de delitos
✅ Denuncia formal de delitos
✅ Escalamiento de reportes
✅ Filtrado y búsqueda avanzada
✅ Estadísticas completas
✅ Permisos por rol y jurisdicción
✅ Exportación de reportes

### Modelos de Datos

1. **IncidenteElectoral** - 24 campos
2. **DelitoElectoral** - 28 campos
3. **SeguimientoReporte** - 8 campos
4. **NotificacionReporte** - 9 campos

### Servicio

**IncidentesDelitosService** - 15 métodos:
- crear_incidente()
- crear_delito()
- obtener_incidentes()
- obtener_delitos()
- actualizar_estado_incidente()
- actualizar_estado_delito()
- denunciar_formalmente()
- obtener_estadisticas()
- obtener_seguimiento()
- obtener_notificaciones()
- marcar_notificacion_leida()
- _registrar_seguimiento()
- _crear_notificaciones_incidente()
- _crear_notificaciones_delito()

### Componentes de Frontend

1. **Formulario de Incidentes** - 8 campos
2. **Formulario de Delitos** - 9 campos
3. **Lista de Reportes** - Con filtros y paginación
4. **Detalle de Reporte** - Con seguimiento y acciones
5. **Panel de Notificaciones** - Con polling en tiempo real
6. **Dashboard de Estadísticas** - Con gráficos

---

## Notas de Implementación

- El sistema está 100% funcional y en producción
- Todos los endpoints están protegidos con autenticación JWT
- Los reportes se filtran automáticamente por rol y jurisdicción
- Las notificaciones se crean automáticamente según severidad/gravedad
- El seguimiento se registra automáticamente en cada acción
- Los delitos notifican a más roles que los incidentes (más graves)
- Las evidencias se almacenan en el filesystem con URLs en base de datos
- Las estadísticas se calculan dinámicamente con filtros de permisos
- El sistema soporta escalamiento manual de reportes
- La denuncia formal requiere número de denuncia y autoridad competente

---

**Fecha de Creación:** 2025-11-25
**Última Actualización:** 2025-11-25
**Estado:** ✅ COMPLETADO
**Implementado por:** Equipo de Desarrollo

