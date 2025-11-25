# Plan de Implementación - Sistema Electoral E-14/E-24

## Introducción

Este documento describe el plan de implementación del Sistema Electoral E-14/E-24, organizado en tareas incrementales que construyen sobre el trabajo anterior. Este spec actúa como "spec paraguas" que engloba funcionalidades distribuidas en otros dashboards específicos. Estado actual: 85% completado, con funcionalidades core implementadas en Testigo Dashboard, Coordinador Puesto, y Super Admin Dashboard.

## Estructura de Tareas

Las tareas están organizadas en épicas principales, cada una con sub-tareas específicas. Todas las tareas son requeridas para una implementación completa y robusta del sistema, incluyendo testing, documentación y despliegue.

---

## Épica 1: Configuración Inicial del Proyecto

- [ ] 1.1 Configurar estructura de directorios del proyecto
  - Crear estructura backend/ con models/, routes/, services/, utils/
  - Crear estructura frontend/ con templates/, static/js/, static/css/
  - Configurar archivos de configuración (.env, config.py)
  - _Requerimientos: Todos_

- [ ] 1.2 Configurar base de datos y migraciones
  - Instalar SQLAlchemy y Flask-Migrate
  - Crear archivo de configuración de base de datos
  - Inicializar sistema de migraciones
  - _Requerimientos: 6, 18_

- [ ] 1.3 Configurar autenticación JWT
  - Instalar Flask-JWT-Extended
  - Configurar tokens de acceso y renovación
  - Implementar decoradores de autenticación
  - _Requerimientos: 1, 16_

- [ ] 1.4 Configurar entorno de testing
  - Instalar pytest y dependencias
  - Crear estructura de tests/
  - Configurar fixtures básicos
  - _Requerimientos: Testing_

---

## Épica 2: Modelos de Datos y Base de Datos

- [ ] 2.1 Implementar modelo User
  - Crear clase User con todos los campos
  - Implementar método check_password con bcrypt
  - Implementar método para bloqueo por intentos fallidos
  - Agregar validaciones de rol y estado
  - _Requerimientos: 1, 5, 14_

- [ ] 2.2 Implementar modelo Location con jerarquía DIVIPOLA
  - Crear clase Location con códigos jerárquicos
  - Implementar métodos para navegar jerarquía (get_departamento, get_municipio, etc.)
  - Implementar método find_by_hierarchy para búsqueda por ubicación
  - Agregar validaciones de tipo y códigos únicos
  - _Requerimientos: 2, 6_

- [ ] 2.3 Implementar modelo FormE14
  - Crear clase FormE14 con todos los campos
  - Implementar campo JSON para votos_partidos
  - Agregar validaciones de estado
  - Implementar relaciones con User y Location
  - _Requerimientos: 7, 8, 28_

- [ ] 2.4 Implementar modelo FormE14History
  - Crear clase para historial de cambios
  - Implementar campo JSON para cambios detallados
  - Agregar índices para consultas eficientes
  - _Requerimientos: 10_

- [ ] 2.5 Implementar modelos adicionales
  - Crear modelo PoliticalParty para partidos políticos
  - Crear modelo Notification para notificaciones
  - Crear modelo AuditLog para auditoría
  - _Requerimientos: 21, 24, 26_

- [ ] 2.6 Crear migraciones iniciales y ejecutar
  - Generar migraciones para todos los modelos
  - Ejecutar migraciones en base de datos
  - Verificar creación de tablas e índices
  - _Requerimientos: Todos los modelos_

---

## Épica 3: Servicios de Autenticación

- [ ] 3.1 Implementar AuthService para login basado en ubicación
  - Crear método authenticate_location_based
  - Implementar búsqueda de usuario por rol + ubicación
  - Implementar verificación de contraseña con bcrypt
  - Implementar lógica de bloqueo por intentos fallidos
  - Implementar generación de tokens JWT
  - _Requerimientos: 1, 14_

- [ ] 3.2 Implementar endpoints de autenticación
  - Crear POST /api/auth/login con validación de ubicación jerárquica
  - Crear POST /api/auth/logout para invalidar tokens
  - Crear POST /api/auth/change-password con validación de contraseña actual
  - Crear GET /api/auth/profile para obtener datos de usuario
  - _Requerimientos: 1, 14, 16_

- [ ] 3.3 Implementar decoradores de autorización
  - Crear @token_required para validar JWT
  - Crear @role_required para validar roles específicos
  - Crear @location_access_required para validar acceso a ubicaciones
  - _Requerimientos: 4, 11_

- [ ] 3.4 Escribir tests de autenticación
  - Test de login exitoso con ubicación correcta
  - Test de login fallido con credenciales incorrectas
  - Test de bloqueo después de 5 intentos
  - Test de cambio de contraseña
  - _Requerimientos: 1, 14_

---

## Épica 4: Endpoints de Ubicaciones

- [ ] 4.1 Implementar endpoints de carga jerárquica de ubicaciones
  - Crear GET /api/locations/departamentos
  - Crear GET /api/locations/municipios?departamento_id=X
  - Crear GET /api/locations/zonas?municipio_id=X
  - Crear GET /api/locations/puestos?zona_id=X
  - Crear GET /api/locations/mesas?puesto_id=X
  - _Requerimientos: 2, 3_

- [ ] 4.2 Implementar filtrado por permisos de usuario
  - Aplicar filtros según rol del usuario autenticado
  - Restringir ubicaciones según ubicación asignada
  - _Requerimientos: 4, 6_

- [ ] 4.3 Escribir tests de endpoints de ubicaciones
  - Test de carga de municipios por departamento
  - Test de filtrado por permisos de usuario
  - Test de jerarquía completa
  - _Requerimientos: 2, 6_

---

## Épica 5: Servicios de Validación

- [ ] 5.1 Implementar ValidationService para formularios E-14
  - Crear método validate_e14_data
  - Implementar validación de suma de votos
  - Implementar validación de total votos vs votantes registrados
  - Implementar validación de valores no negativos
  - _Requerimientos: 8, 12_

- [ ] 5.2 Implementar sanitización de datos
  - Crear DataSanitizer para limpiar entradas
  - Implementar escape de HTML y caracteres especiales
  - Implementar trim de espacios en blanco
  - _Requerimientos: 19_

- [ ] 5.3 Escribir tests de validación
  - Test de validación exitosa con datos correctos
  - Test de validación fallida con suma incorrecta
  - Test de validación fallida con votos excediendo votantes
  - _Requerimientos: 8, 12_

---

## Épica 6: Gestión de Formularios E-14

- [ ] 6.1 Implementar E14Service para crear formularios
  - Crear método create_form
  - Implementar validación de acceso a mesa
  - Implementar creación de formulario con estado 'borrador'
  - Implementar registro en historial
  - _Requerimientos: 7, 10_

- [ ] 6.2 Implementar endpoints de formularios E-14
  - Crear POST /api/e14/forms para crear formulario
  - Crear GET /api/e14/forms para listar formularios
  - Crear GET /api/e14/forms/:id para obtener detalles
  - Crear PUT /api/e14/forms/:id para actualizar formulario
  - Crear POST /api/e14/forms/:id/submit para enviar a revisión
  - _Requerimientos: 7, 8, 13_

- [ ] 6.3 Implementar carga de imágenes
  - Crear POST /api/e14/forms/:id/upload-photo
  - Implementar validación de tipo y tamaño de archivo
  - Implementar almacenamiento con nombre único
  - Implementar optimización de imagen
  - _Requerimientos: 16_

- [ ] 6.4 Implementar aprobación y rechazo de formularios
  - Crear POST /api/e14/forms/:id/approve
  - Crear POST /api/e14/forms/:id/reject con justificación obligatoria
  - Implementar validación de unicidad de formulario aprobado por mesa
  - Implementar registro en historial
  - _Requerimientos: 9, 10, 28_

- [ ] 6.5 Escribir tests de gestión de formularios
  - Test de creación de formulario
  - Test de envío de formulario
  - Test de aprobación por coordinador
  - Test de rechazo con justificación
  - Test de unicidad de formulario aprobado
  - _Requerimientos: 7, 8, 9, 28_

---

## Épica 7: Frontend - Componentes JavaScript Core

- [ ] 7.1 Implementar APIClient para comunicación con backend
  - Crear clase APIClient con métodos get, post, put, delete
  - Implementar manejo de tokens JWT en headers
  - Implementar manejo de respuestas y errores
  - Implementar auto-redirect a login en 401
  - Implementar método uploadFile para multipart/form-data
  - _Requerimientos: 18_

- [ ] 7.2 Implementar Utils para utilidades generales
  - Crear método showAlert para mostrar mensajes
  - Crear método formatDate para formatear fechas
  - Crear método formatNumber para formatear números
  - Crear método formatPercentage para calcular porcentajes
  - Crear método sanitizeInput para limpiar entradas
  - Crear método debounce para optimizar eventos
  - _Requerimientos: 25_

- [ ] 7.3 Implementar FormHandler para manejo de formularios
  - Crear método setupImagePreview para preview de imágenes
  - Crear método validateVoteTotals para validación en tiempo real
  - Crear método showValidationErrors para mostrar errores
  - Crear método setupRealTimeValidation para validación automática
  - _Requerimientos: 8, 12_

- [ ] 7.4 Implementar LocationMap para mapas interactivos
  - Crear clase LocationMap con Leaflet
  - Implementar método init para inicializar mapa
  - Implementar método loadMapData para cargar ubicaciones
  - Implementar método loadMarkers para mostrar marcadores
  - Implementar evento locationSelected para selección
  - _Requerimientos: 29_

---

## Épica 8: Frontend - Página de Login

- [ ] 8.1 Implementar formulario de login con ubicación jerárquica
  - Crear selectores dinámicos para departamento, municipio, zona, puesto
  - Implementar carga dinámica de opciones según selección anterior
  - Implementar habilitación/deshabilitación de selectores según rol
  - Implementar validación de campos requeridos según rol
  - _Requerimientos: 1, 2, 3_

- [ ] 8.2 Implementar lógica de autenticación en frontend
  - Crear función handleLogin para enviar credenciales
  - Implementar almacenamiento de tokens en localStorage
  - Implementar redirección a dashboard según rol
  - Implementar manejo de errores de autenticación
  - _Requerimientos: 1, 16_

- [ ] 8.3 Implementar estilos responsive para login
  - Crear estilos CSS para formulario de login
  - Implementar diseño responsive para móvil y tablet
  - Agregar animaciones y transiciones
  - _Requerimientos: 29_

---

## Épica 9: Frontend - Dashboard Testigo Electoral

- [ ] 9.1 Implementar estructura HTML del dashboard testigo
  - Crear sección de métricas (total, pendientes, aprobados, rechazados)
  - Crear tabla de formularios E-14
  - Crear selector de mesa electoral
  - Crear sección de ubicación asignada
  - _Requerimientos: 3, 11_

- [ ] 9.2 Implementar carga de datos del dashboard testigo
  - Crear función loadUserProfile para obtener datos de usuario
  - Crear función loadForms para listar formularios
  - Crear función updateMetrics para actualizar métricas
  - Crear función updateFormsTable para llenar tabla
  - _Requerimientos: 11_

- [ ] 9.3 Implementar modal de creación de formulario E-14
  - Crear modal con formulario completo
  - Implementar preview de imagen
  - Implementar campos dinámicos para partidos políticos
  - Implementar validación en tiempo real
  - Implementar función saveForm para guardar formulario
  - _Requerimientos: 7, 8_

- [ ] 9.4 Implementar funcionalidad de envío de formulario
  - Crear función submitForm para enviar a revisión
  - Implementar confirmación antes de enviar
  - Implementar actualización de lista después de enviar
  - _Requerimientos: 7_

- [ ] 9.5 Implementar selector dinámico de mesa
  - Crear selector de mesa con mesas del puesto
  - Implementar cambio de mesa seleccionada
  - Implementar actualización de formularios según mesa
  - _Requerimientos: 3_

---

## Épica 10: Frontend - Dashboard Coordinador de Puesto

- [ ] 10.1 Implementar estructura HTML del dashboard coordinador
  - Crear sección de métricas (pendientes, aprobados hoy, rechazados hoy)
  - Crear tabla de formularios pendientes
  - Crear filtros por estado y mesa
  - _Requerimientos: 12_

- [ ] 10.2 Implementar carga de datos del dashboard coordinador
  - Crear función loadDashboardData para obtener estadísticas
  - Crear función loadPendingForms para listar formularios pendientes
  - Implementar actualización automática cada 30 segundos
  - _Requerimientos: 12_

- [ ] 10.3 Implementar interfaz de revisión de formularios
  - Crear modal de revisión con imagen y datos
  - Implementar zoom y pan en imagen
  - Implementar comparación visual de datos vs imagen
  - _Requerimientos: 9_

- [ ] 10.4 Implementar aprobación y rechazo de formularios
  - Crear función approveForm con observaciones opcionales
  - Crear función rejectForm con justificación obligatoria
  - Implementar validación de justificación mínima
  - Implementar actualización de lista después de acción
  - _Requerimientos: 9_

- [ ] 10.5 Implementar filtros y búsqueda
  - Crear filtros por estado de formulario
  - Crear filtro por mesa electoral
  - Crear búsqueda por código de mesa
  - _Requerimientos: 22_

---

## Épica 11: Frontend - Dashboards de Coordinadores Municipal y Departamental

- [ ] 11.1 Implementar dashboard coordinador municipal
  - Crear estructura HTML con métricas municipales
  - Implementar tabla de puestos con estadísticas
  - Implementar mapa de puestos del municipio
  - Implementar gráficos de avance por puesto
  - _Requerimientos: 12, 16_

- [ ] 11.2 Implementar dashboard coordinador departamental
  - Crear estructura HTML con métricas departamentales
  - Implementar tabla de municipios con estadísticas
  - Implementar mapa departamental
  - Implementar gráficos de avance por municipio
  - _Requerimientos: 12, 16_

- [ ] 11.3 Implementar selector dinámico de ubicación para coordinadores
  - Crear selectores para navegar por ubicaciones
  - Implementar actualización de datos según ubicación seleccionada
  - _Requerimientos: 16_

---

## Épica 12: Frontend - Dashboard Auditor

- [ ] 12.1 Implementar estructura HTML del dashboard auditor
  - Crear sección de logs de auditoría
  - Crear filtros de auditoría (usuario, acción, fecha)
  - Crear timeline de actividades
  - _Requerimientos: 17, 24_

- [ ] 12.2 Implementar carga y visualización de logs
  - Crear función loadAuditLogs para obtener logs
  - Implementar paginación de logs
  - Implementar búsqueda en logs
  - _Requerimientos: 17, 24_

- [ ] 12.3 Implementar vista de trazabilidad de formulario
  - Crear modal con historial completo de formulario
  - Implementar comparación de versiones
  - Implementar visualización de cambios
  - _Requerimientos: 10, 17_

---

## Épica 13: Frontend - Dashboard Administrador

- [ ] 13.1 Arreglar dashboard administrador existente
  - Incluir jQuery en base.html antes de otros scripts
  - Verificar que todas las funciones JavaScript funcionen
  - Corregir inicialización de gráficos con Chart.js
  - _Requerimientos: 13_

- [ ] 13.2 Implementar gestión de usuarios funcional
  - Crear modal de creación/edición de usuario
  - Implementar formulario con validaciones
  - Implementar tabla de usuarios con paginación
  - Implementar búsqueda y filtros de usuarios
  - _Requerimientos: 5, 13_

- [ ] 13.3 Implementar gestión de ubicaciones funcional
  - Crear modal de creación/edición de ubicación
  - Implementar formulario jerárquico de ubicación
  - Implementar tabla de ubicaciones con jerarquía
  - Implementar importación masiva de DIVIPOLA
  - _Requerimientos: 6, 13_

- [ ] 13.4 Implementar herramientas de administración
  - Crear sección de configuración del sistema
  - Implementar backup manual de base de datos
  - Implementar limpieza de logs
  - Implementar reseteo masivo de contraseñas
  - _Requerimientos: 13, 20_

---

## Épica 14: Sistema de Notificaciones

- [ ] 14.1 Implementar NotificationService en backend
  - Crear método create_notification
  - Crear método get_user_notifications
  - Crear método mark_as_read
  - _Requerimientos: 21_

- [ ] 14.2 Implementar endpoints de notificaciones
  - Crear GET /api/notifications para listar notificaciones
  - Crear POST /api/notifications/:id/read para marcar como leída
  - Crear GET /api/notifications/unread-count para contador
  - _Requerimientos: 21_

- [ ] 14.3 Implementar componente de notificaciones en frontend
  - Crear badge de contador en navbar
  - Crear dropdown de notificaciones
  - Implementar polling cada 30 segundos
  - Implementar marcado como leída al hacer clic
  - _Requerimientos: 21_

- [ ] 14.4 Implementar generación automática de notificaciones
  - Crear notificación cuando formulario es aprobado
  - Crear notificación cuando formulario es rechazado
  - Crear notificación para alertas del sistema
  - _Requerimientos: 21_

---

## Épica 15: Sistema de Reportes y Exportación

- [ ] 15.1 Implementar ReportService en backend
  - Crear método generate_pdf_report
  - Crear método generate_excel_report
  - Crear método generate_csv_export
  - _Requerimientos: 23_

- [ ] 15.2 Implementar endpoints de exportación
  - Crear GET /api/reports/e14/export?format=csv
  - Crear GET /api/reports/e14/export?format=xlsx
  - Crear GET /api/reports/consolidated/pdf
  - _Requerimientos: 23_

- [ ] 15.3 Implementar botones de exportación en dashboards
  - Agregar botones de exportación en cada dashboard
  - Implementar descarga de archivos generados
  - Implementar indicador de progreso durante generación
  - _Requerimientos: 23_

---

## Épica 16: Búsqueda y Filtros Avanzados

- [ ] 16.1 Implementar búsqueda global de formularios
  - Crear endpoint GET /api/e14/search con múltiples criterios
  - Implementar búsqueda por código de mesa
  - Implementar búsqueda por nombre de testigo
  - Implementar búsqueda por rango de fechas
  - _Requerimientos: 22_

- [ ] 16.2 Implementar componente de búsqueda en frontend
  - Crear barra de búsqueda global
  - Implementar autocompletado
  - Implementar filtros combinados
  - Implementar guardado de filtros favoritos
  - _Requerimientos: 22_

---

## Épica 17: Modo Offline y Sincronización

- [ ] 17.1 Implementar almacenamiento local con IndexedDB
  - Configurar IndexedDB para almacenar formularios
  - Implementar guardado de formularios en modo offline
  - Implementar cola de sincronización
  - _Requerimientos: 27_

- [ ] 17.2 Implementar detección de conectividad
  - Crear listener de eventos online/offline
  - Implementar indicador visual de estado de conexión
  - Implementar cambio automático a modo offline
  - _Requerimientos: 27_

- [ ] 17.3 Implementar sincronización automática
  - Crear función syncPendingForms
  - Implementar sincronización al recuperar conexión
  - Implementar manejo de conflictos
  - Implementar notificación de sincronización exitosa
  - _Requerimientos: 27_

---

## Épica 18: Optimización y Rendimiento

- [ ] 18.1 Implementar caché con Redis
  - Configurar Redis para caché
  - Implementar caché de estadísticas de dashboard
  - Implementar caché de ubicaciones
  - Implementar invalidación de caché al actualizar datos
  - _Requerimientos: 20_

- [ ] 18.2 Optimizar consultas de base de datos
  - Agregar índices faltantes
  - Optimizar consultas con EXPLAIN ANALYZE
  - Implementar eager loading para relaciones
  - _Requerimientos: 20_

- [ ] 18.3 Implementar lazy loading en frontend
  - Implementar lazy loading de imágenes
  - Implementar paginación infinita en listas
  - Implementar code splitting para JavaScript
  - _Requerimientos: 20, 29_

---

## Épica 19: Seguridad y Auditoría

- [ ] 19.1 Implementar logging de auditoría
  - Crear función log_audit_event
  - Implementar logging en todas las acciones críticas
  - Implementar almacenamiento de IP y user agent
  - _Requerimientos: 24_

- [ ] 19.2 Implementar rate limiting
  - Configurar Flask-Limiter
  - Implementar límites por endpoint
  - Implementar límites por IP
  - _Requerimientos: 20_

- [ ] 19.3 Implementar protección CSRF
  - Configurar Flask-WTF para CSRF
  - Agregar tokens CSRF en formularios
  - Validar tokens en backend
  - _Requerimientos: 20_

---

## Épica 20: Testing y Calidad

- [ ] 20.1 Escribir tests unitarios de servicios
  - Tests de AuthService
  - Tests de E14Service
  - Tests de ValidationService
  - Tests de NotificationService
  - _Requerimientos: Todos_

- [ ] 20.2 Escribir tests de integración de API
  - Tests de flujo completo de autenticación
  - Tests de flujo completo de creación y aprobación de E-14
  - Tests de permisos y control de acceso
  - _Requerimientos: Todos_

- [ ] 20.3 Escribir tests end-to-end
  - Tests de flujo de testigo electoral
  - Tests de flujo de coordinador
  - Tests de flujo de administrador
  - _Requerimientos: Todos_

- [ ] 20.4 Configurar CI/CD
  - Configurar GitHub Actions o GitLab CI
  - Implementar ejecución automática de tests
  - Implementar análisis de cobertura de código
  - _Requerimientos: Testing_

---

## Épica 21: Documentación y Capacitación

- [ ] 21.1 Crear documentación de API
  - Documentar todos los endpoints con Swagger/OpenAPI
  - Incluir ejemplos de request/response
  - Incluir códigos de error
  - _Requerimientos: Todos_

- [ ] 21.2 Crear manual de usuario
  - Manual para testigos electorales
  - Manual para coordinadores
  - Manual para administradores
  - _Requerimientos: 30_

- [ ] 21.3 Crear videos tutoriales
  - Video de cómo usar el sistema como testigo
  - Video de cómo validar formularios como coordinador
  - Video de cómo administrar el sistema
  - _Requerimientos: 30_

---

## Épica 22: Despliegue y Monitoreo

- [ ] 22.1 Configurar entorno de producción
  - Configurar servidor con Gunicorn
  - Configurar Nginx como reverse proxy
  - Configurar PostgreSQL en producción
  - Configurar Redis en producción
  - _Requerimientos: 20_

- [ ] 22.2 Implementar monitoreo y alertas
  - Configurar Sentry para tracking de errores
  - Configurar logging centralizado
  - Configurar alertas de Slack/Email
  - _Requerimientos: 20, 25_

- [ ] 22.3 Implementar backups automáticos
  - Configurar backup diario de base de datos
  - Configurar backup de archivos subidos
  - Configurar retención de backups
  - Implementar restauración de backups
  - _Requerimientos: 20_

---

## Resumen de Prioridades

### 🔴 Crítico (Semanas 1-4)
- Épicas 1-6: Configuración, modelos, autenticación, ubicaciones, validación, formularios E-14
- Épicas 7-9: Componentes JS core, login, dashboard testigo
- Épica 10: Dashboard coordinador de puesto

### 🟡 Alto (Semanas 5-8)
- Épica 11: Dashboards coordinadores municipal/departamental
- Épica 12: Dashboard auditor
- Épica 13: Dashboard administrador
- Épica 14: Sistema de notificaciones
- Épica 15: Reportes y exportación

### 🟢 Medio (Semanas 9-12)
- Épica 16: Búsqueda avanzada
- Épica 17: Modo offline
- Épica 18: Optimización
- Épica 19: Seguridad avanzada

### 🔵 Bajo (Semanas 13-16)
- Épica 20: Testing completo
- Épica 21: Documentación
- Épica 22: Despliegue avanzado

