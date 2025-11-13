# Implementation Plan - Dashboard Coordinador Municipal

## Overview

Este plan de implementación convierte el diseño del Dashboard del Coordinador Municipal en tareas específicas de código. Cada tarea construye sobre las anteriores de manera incremental, asegurando que el código se integre correctamente en cada paso.

## Tasks

- [x] 1. Crear modelos de base de datos y migraciones


  - Crear modelos FormularioE24Municipal, VotoPartidoE24Municipal, Notificacion, y AuditLog en `backend/models/`
  - Implementar métodos `to_dict()` en cada modelo para serialización
  - Crear migración de base de datos con tablas e índices necesarios
  - Ejecutar migración y verificar que las tablas se crean correctamente
  - _Requirements: 5.1, 5.5, 14.1_



- [ ] 2. Implementar MunicipalService para lógica de negocio
  - Crear `backend/services/municipal_service.py` con clase MunicipalService
  - Implementar `obtener_puestos_municipio()` para obtener lista de puestos con estadísticas
  - Implementar `calcular_estadisticas_puesto()` reutilizando ConsolidadoService existente
  - Implementar `obtener_puesto_detallado()` para información completa de un puesto


  - Implementar `comparar_puestos()` para comparación estadística entre puestos
  - _Requirements: 1.1, 1.2, 1.3, 8.1, 13.1_

- [ ] 3. Implementar DiscrepanciaService para detección de anomalías
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

- [ ] 6. Implementar endpoints de acciones avanzadas
  - Implementar endpoint POST `/api/coordinador-municipal/e24-municipal` para generar E-24


  - Implementar endpoint GET `/api/coordinador-municipal/comparacion` para comparar puestos
  - Implementar endpoint GET `/api/coordinador-municipal/estadisticas` para métricas detalladas
  - Implementar endpoint POST `/api/coordinador-municipal/notificar` para enviar notificaciones
  - Implementar endpoint GET `/api/coordinador-municipal/exportar` para exportar datos en CSV/XLSX
  - Agregar validaciones y manejo de errores en cada endpoint
  - _Requirements: 5.1, 6.4, 8.1, 9.1, 9.2, 13.1_



- [ ] 7. Registrar blueprint y configurar rutas
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

- [ ] 20. Crear ruta de navegación en app principal
  - Agregar ruta `/coordinador/municipal` en `backend/app.py`
  - Implementar redirección automática según rol del usuario al hacer login
  - Verificar que solo usuarios con rol `coordinador_municipal` puedan acceder
  - Agregar enlace al dashboard municipal en menú de navegación
  - _Requirements: 11.1_

