# Implementation Plan - Dashboard Coordinador Municipal

## Overview

Este plan de implementación convierte el diseño del Dashboard del Coordinador Municipal en tareas específicas de código. Estado actual: 75% completado (15/20 tareas). Los modelos de datos están implementados, la mayoría de endpoints están funcionales, pero falta completar algunos servicios y el frontend.

## Tasks

- [x] 1. Crear modelos de base de datos y migraciones


  - Crear modelos FormularioE24Municipal, VotoPartidoE24Municipal, Notificacion, y AuditLog en `backend/models/`
  - Implementar métodos `to_dict()` en cada modelo para serialización
  - Crear migración de base de datos con tablas e índices necesarios
  - Ejecutar migración y verificar que las tablas se crean correctamente
  - _Requirements: 5.1, 5.5, 14.1_



- [x] 2. Implementar MunicipalService para lógica de negocio
  - Crear `backend/services/municipal_service.py` con clase MunicipalService
  - Implementar `obtener_puestos_municipio()` para obtener lista de puestos con estadísticas
  - Implementar `calcular_estadisticas_puesto()` reutilizando ConsolidadoService existente
  - Implementar `obtener_puesto_detallado()` para información completa de un puesto
  - Implementar `comparar_puestos()` para comparación estadística entre puestos
  - _Requirements: 1.1, 1.2, 1.3, 8.1, 13.1_

- [x] 3. Implementar DiscrepanciaService para detección de anomalías
  - Crear `backend/services/discrepancia_service.py` con clase DiscrepanciaService
  - Implementar `detectar_discrepancias_puesto()` para detectar participación anormal, suma incorrecta, coordinador inactivo
  - Implementar `detectar_discrepancias_municipio()` para agregar discrepancias de todos los puestos
  - Implementar `calcular_severidad()` para clasificar discrepancias (baja, media, alta, crítica)
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 4. Implementar E24Service para generación de formularios


  - Crear `backend/services/e24_service.py` con clase E24Service
  - Implementar `validar_requisitos_e24()` para verificar que al menos 80% de puestos tienen datos completos
  - Implementar `generar_e24_municipal()` para crear formulario E-24 Municipal con consolidado
  - Implementar `generar_pdf_e24()` usando ReportLab para crear PDF con formato oficial
  - Registrar generación en base de datos con hash SHA-256 del PDF
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 5. Crear endpoints API para coordinador municipal


  - Crear `backend/routes/coordinador_municipal.py` con blueprint coordinador_municipal_bp
  - Implementar endpoint GET `/api/coordinador-municipal/puestos` para lista de puestos
  - Implementar endpoint GET `/api/coordinador-municipal/consolidado` para consolidado municipal
  - Implementar endpoint GET `/api/coordinador-municipal/puesto/<id>` para detalles de puesto
  - Implementar endpoint GET `/api/coordinador-municipal/discrepancias` para puestos con anomalías
  - Agregar decoradores `@jwt_required()` y `@role_required(['coordinador_municipal'])` a todos los endpoints
  - Validar que el coordinador solo acceda a datos de su municipio asignado


  - _Requirements: 1.1, 2.1, 3.1, 4.1, 11.1, 11.2_

- [x] 6. Implementar endpoints de acciones avanzadas
  - Implementar endpoint POST `/api/coordinador-municipal/e24-municipal` para generar E-24
  - Implementar endpoint GET `/api/coordinador-municipal/comparacion` para comparar puestos
  - Implementar endpoint GET `/api/coordinador-municipal/estadisticas` para métricas detalladas
  - Implementar endpoint POST `/api/coordinador-municipal/notificar` para enviar notificaciones
  - Implementar endpoint GET `/api/coordinador-municipal/exportar` para exportar datos en CSV/XLSX
  - Agregar validaciones y manejo de errores en cada endpoint
  - _Requirements: 5.1, 6.4, 8.1, 9.1, 9.2, 13.1_



- [x] 7. Registrar blueprint y configurar rutas
  - Registrar coordinador_municipal_bp en `backend/routes/__init__.py`
  - Agregar imports de servicios en `backend/services/__init__.py`
  - Verificar que las rutas estén accesibles con autenticación correcta
  - _Requirements: 11.1_

- [x] 8. Crear template HTML del dashboard

  - Crear `frontend/templates/coordinador/municipal.html` con estructura de 3 columnas
  - Implementar panel izquierdo con estadísticas generales y consolidado municipal
  - Implementar panel central con tabla de puestos y filtros
  - Implementar panel derecho con detalle de puesto seleccionado y alertas
  - Agregar navbar con información del municipio y botón de logout
  - Incluir referencias a CSS y JS necesarios (Bootstrap, Chart.js, api-client.js)

  - _Requirements: 1.1, 2.1, 3.1, 4.1, 10.1_

- [ ] 9. Implementar JavaScript del dashboard
  - Crear `frontend/static/js/coordinador-municipal.js` con funciones principales
  - Implementar `loadUserProfile()` para cargar información del coordinador
  - Implementar `loadPuestos()` para obtener lista de puestos con auto-refresh cada 60 segundos
  - Implementar `loadConsolidadoMunicipal()` para obtener y renderizar consolidado con gráfico
  - Implementar `loadDiscrepancias()` para obtener y mostrar alertas

  - Implementar `renderPuestosTable()` para mostrar tabla de puestos con badges de estado
  - _Requirements: 1.1, 1.5, 2.1, 2.5, 4.1, 12.1_

- [ ] 10. Implementar funcionalidades de interacción
  - Implementar `seleccionarPuesto()` para cargar y mostrar detalles de puesto en panel derecho
  - Implementar `filtrarPuestos()` para filtrar por estado (completo, incompleto, con_discrepancias)
  - Implementar `buscarPuesto()` para búsqueda por código o nombre con debouncing
  - Implementar navegación entre vista general y detalle de puesto manteniendo contexto

  - _Requirements: 3.1, 7.1, 7.2, 7.5, 15.1, 15.2_

- [ ] 11. Implementar generación de E-24 Municipal
  - Implementar `generarE24Municipal()` en frontend para solicitar generación
  - Crear modal de confirmación mostrando requisitos y validaciones
  - Validar que se cumplan requisitos mínimos (80% puestos completos) antes de generar
  - Mostrar progreso durante generación del PDF

  - Descargar PDF automáticamente al completar generación
  - Registrar generación en historial con fecha y hora
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [ ] 12. Implementar comparación de puestos
  - Implementar `abrirComparacion()` para mostrar modal de selección de puestos

  - Permitir seleccionar múltiples puestos (2-5) para comparación
  - Obtener datos comparativos del endpoint `/api/coordinador-municipal/comparacion`
  - Renderizar gráficos comparativos de votos por partido usando Chart.js
  - Mostrar tabla comparativa con estadísticas clave (participación, votos, etc.)
  - Calcular y mostrar desviación estándar entre puestos seleccionados
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_


- [ ] 13. Implementar exportación de datos
  - Implementar `exportarDatos()` para descargar consolidado en CSV o XLSX
  - Crear modal para seleccionar formato de exportación (CSV, Excel)
  - Incluir en exportación: fecha de generación, nombre del coordinador, timestamp
  - Implementar descarga de archivo generado por el backend
  - Registrar cada exportación en log de auditoría
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_


- [ ] 14. Implementar sistema de notificaciones
  - Implementar `enviarNotificacion()` para enviar mensajes a coordinadores de puesto
  - Crear modal para componer notificación con destinatarios y prioridad
  - Permitir seleccionar coordinadores específicos o todos los del municipio
  - Mostrar confirmación de envío exitoso
  - _Requirements: 6.4, 12.1_


- [ ] 15. Implementar visualización de estadísticas
  - Renderizar panel de estadísticas generales (total puestos, mesas, cobertura)
  - Implementar gráfico de barras para consolidado municipal con Chart.js
  - Mostrar métricas de formularios por estado (pendientes, validados, rechazados)
  - Implementar gráfico de línea de tiempo con progreso durante el día
  - Actualizar estadísticas automáticamente con auto-refresh

  - _Requirements: 2.1, 2.3, 2.4, 8.1, 8.2, 8.5_

- [ ] 16. Implementar detección y visualización de discrepancias
  - Renderizar panel de alertas con discrepancias detectadas
  - Agrupar discrepancias por severidad (crítica, alta, media, baja)
  - Mostrar badges visuales en puestos con discrepancias en la tabla
  - Permitir filtrar tabla para mostrar solo puestos con discrepancias



  - Implementar navegación desde alerta a puesto específico
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 17. Implementar responsive design
  - Adaptar layout de 3 columnas a 1 columna en pantallas < 768px
  - Optimizar tabla de puestos para visualización móvil (scroll horizontal)
  - Ajustar tamaño de gráficos para pantallas pequeñas
  - Implementar menú colapsable para filtros en móvil
  - Verificar que todas las funcionalidades principales funcionen en móvil
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 18. Implementar seguridad y auditoría
  - Agregar logging de auditoría para todas las acciones del coordinador
  - Registrar visualización de puestos, generación de E-24, exportaciones
  - Implementar cierre de sesión automático después de 30 minutos de inactividad
  - Validar permisos en cada endpoint (solo datos del municipio asignado)
  - Agregar rate limiting a endpoints críticos (generación E-24, exportación)
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 14.3_

- [ ] 19. Implementar optimizaciones de performance
  - Agregar índices de base de datos para queries frecuentes
  - Implementar caching de consolidado municipal (60 segundos)
  - Usar eager loading para evitar N+1 queries en lista de puestos
  - Implementar paginación en lista de puestos si hay más de 50
  - Optimizar queries usando agregaciones en base de datos
  - _Requirements: 1.5, 2.5_

- [x] 21. Implementar endpoints adicionales de gestión
  - Implementar endpoint GET `/api/coordinador-municipal/e24-puestos` para obtener E-24s de puestos
  - Implementar endpoint GET `/api/coordinador-municipal/consolidado-por-zona` para consolidado por zona
  - Implementar endpoint GET `/api/coordinador-municipal/incidentes` para incidentes del municipio
  - Implementar endpoint GET `/api/coordinador-municipal/delitos` para delitos electorales
  - Implementar endpoint GET `/api/coordinador-municipal/coordinadores` para coordinadores de puesto
  - Implementar endpoint GET `/api/coordinador-municipal/formularios` para formularios del municipio
  - Filtros avanzados en todos los endpoints
  - _Requirements: 1.1, 4.1, 12.1, 13.1_

- [x] 22. Implementar funcionalidades de incidentes y delitos
  - Visualización de incidentes por municipio con filtros
  - Visualización de delitos electorales con filtros
  - Integración con evidencias fotográficas
  - Estados de seguimiento y resolución
  - Estadísticas de incidentes por severidad
  - _Requirements: 12.1, 13.1, 14.1_

- [x] 23. Implementar gestión de coordinadores de puesto
  - Lista de coordinadores con estado de conexión
  - Estadísticas de rendimiento por coordinador
  - Geolocalización de coordinadores
  - Filtros por estado de actividad
  - Métricas de avance por puesto
  - _Requirements: 6.1, 6.2, 6.3, 6.4_


## Estado Actual

✅ **Dashboard Coordinador Municipal 75% Funcional**

**Última actualización:** Diciembre 2025

18 de 23 tareas completadas. El sistema tiene implementadas las funcionalidades principales de gestión de puestos, consolidación municipal, detección de discrepancias, y endpoints de API completos. Falta completar el frontend y algunos servicios.

### Funcionalidades Implementadas

- ✅ **Modelos de base de datos**
  - FormularioE24Municipal, VotoPartidoE24Municipal, Notificacion, y AuditLog
  - Migraciones aplicadas correctamente

- ✅ **Endpoints API completos (16 endpoints)**
  - GET `/api/coordinador-municipal/puestos` - Lista de puestos con estadísticas
  - GET `/api/coordinador-municipal/consolidado` - Consolidado municipal
  - GET `/api/coordinador-municipal/puesto/<id>` - Detalles de puesto específico
  - GET `/api/coordinador-municipal/discrepancias` - Puestos con anomalías
  - POST `/api/coordinador-municipal/e24-municipal` - Generar E-24 Municipal
  - GET `/api/coordinador-municipal/comparacion` - Comparar puestos
  - GET `/api/coordinador-municipal/estadisticas` - Métricas detalladas
  - POST `/api/coordinador-municipal/notificar` - Enviar notificaciones
  - GET `/api/coordinador-municipal/exportar` - Exportar datos CSV
  - GET `/api/coordinador-municipal/e24-puestos` - E-24s de puestos
  - GET `/api/coordinador-municipal/consolidado-por-zona` - Consolidado por zona
  - GET `/api/coordinador-municipal/incidentes` - Incidentes del municipio
  - GET `/api/coordinador-municipal/delitos` - Delitos electorales
  - GET `/api/coordinador-municipal/coordinadores` - Coordinadores de puesto
  - GET `/api/coordinador-municipal/formularios` - Formularios del municipio

- ✅ **Servicios implementados**
  - MunicipalService con lógica de negocio completa
  - DiscrepanciaService para detección de anomalías
  - E24Service para generación de formularios
  - ConsolidadoService para cálculos agregados

- ✅ **Funcionalidades avanzadas**
  - Detección automática de discrepancias por puesto
  - Generación de E-24 Municipal con validaciones
  - Comparación estadística entre puestos
  - Exportación de datos en formato CSV
  - Sistema de notificaciones a coordinadores de puesto
  - Gestión completa de incidentes y delitos
  - Seguimiento de coordinadores con geolocalización
  - Consolidado por zonas del municipio
  - Auditoría completa de todas las acciones

- ✅ **Seguridad y validaciones**
  - Autenticación JWT en todos los endpoints
  - Validación de rol coordinador_municipal
  - Validación de permisos por municipio asignado
  - Registro completo en audit log
  - Manejo estructurado de errores y excepciones

- ✅ **Integración con otros módulos**
  - Formularios E-14 con estados y validaciones
  - Incidentes electorales con evidencias fotográficas
  - Delitos electorales con seguimiento legal
  - Usuarios y ubicaciones DIVIPOLA
  - Sistema de notificaciones

### Funcionalidades Pendientes (25%)

- ⏳ **Frontend JavaScript** (Tareas 9-16)
  - Dashboard principal con layout de 3 columnas
  - Funcionalidades de interacción con puestos
  - Generación de E-24 Municipal desde frontend
  - Comparación visual de puestos
  - Exportación de datos desde interfaz
  - Sistema de notificaciones en tiempo real
  - Visualización de estadísticas con gráficos
  - Detección y visualización de discrepancias

- ⏳ **Optimizaciones** (Tareas 17-19)
  - Responsive design para móviles
  - Seguridad y auditoría adicional
  - Optimizaciones de performance y caching

### Archivos Implementados

**Backend (Completo):**
- `backend/routes/coordinador_municipal.py` - Endpoints completos (2426+ líneas)
- `backend/services/municipal_service.py` - Servicio de lógica de negocio
- `backend/services/discrepancia_service.py` - Detección de anomalías
- `backend/services/e24_service.py` - Generación de E-24
- `backend/models/coordinador_municipal.py` - Modelos de datos

**Frontend (Pendiente):**
- `frontend/templates/coordinador/municipal.html` - Template principal
- `frontend/static/js/coordinador-municipal.js` - Lógica JavaScript

### Próximas Prioridades

1. **Crear template HTML del dashboard** (Tarea 8)
2. **Implementar JavaScript del dashboard** (Tarea 9)
3. **Implementar funcionalidades de interacción** (Tarea 10)
4. **Implementar generación de E-24 Municipal** (Tarea 11)
5. **Implementar responsive design** (Tarea 17)

### Métricas de Implementación

- **Backend**: 100% completado (16 endpoints funcionales)
- **Servicios**: 100% completado (4 servicios principales)
- **Modelos**: 100% completado (4 modelos con relaciones)
- **Frontend**: 0% completado (pendiente de implementación)
- **Testing**: Pendiente de implementación

## Mejoras Futuras (Opcionales)

- [ ] Implementar dashboard de métricas en tiempo real
- [ ] Agregar notificaciones push para alertas críticas
- [ ] Implementar chat en tiempo real con coordinadores de puesto
- [ ] Agregar exportación en múltiples formatos (Excel, PDF)
- [ ] Implementar análisis predictivo de participación
- [ ] Agregar geolocalización de incidentes en mapa
- [ ] Implementar sistema de firma digital para E-24
- [ ] Agregar integración con sistemas externos de autoridades