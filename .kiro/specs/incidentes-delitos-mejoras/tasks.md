# Implementation Plan: Sistema de Incidentes y Delitos Electorales

## Fase 1: Gestión de Evidencia Fotográfica

- [x] 1. Implementar backend de upload de fotos


- [x] 1.1 Crear modelo EvidenciaFotografica en base de datos



  - Crear migración para nueva tabla evidencias_fotograficas
  - Agregar relaciones con incidentes y delitos





  - _Requirements: 3.1, 3.2, 3.3_

- [x] 1.2 Implementar UploadService para gestión de archivos

  - Validación de tipo y tamaño de archivo
  - Generación de nombres únicos con timestamp y hash
  - Compresión de imágenes con Pillow

  - Extracción de metadatos GPS de EXIF
  - Almacenamiento en directorio seguro
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 1.3 Escribir property test para nombres únicos de archivo


  - **Property 5: Unicidad de nombres de archivo**
  - **Validates: Requirements 3.2**





- [ ] 1.4 Escribir property test para compresión de imágenes
  - **Property 6: Compresión de imágenes**
  - **Validates: Requirements 3.1**


- [ ] 1.5 Crear endpoint POST /api/evidencia/upload
  - Recibir archivo multipart/form-data
  - Validar permisos del usuario
  - Procesar y guardar evidencia
  - Retornar URL de acceso

  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 1.6 Crear endpoint GET /api/evidencia/<filename>
  - Validar permisos de acceso
  - Generar URL firmada temporal


  - Servir archivo con headers apropiados
  - _Requirements: 3.5_

- [ ] 1.7 Modificar modelos IncidenteElectoral y DelitoElectoral
  - Agregar campos latitud_reporte, longitud_reporte, precision_gps
  - Agregar relación con EvidenciaFotografica


  - Crear migración de base de datos
  - _Requirements: 1.3, 2.1_

- [x] 1.8 Implementar frontend de captura de fotos


  - Componente para capturar foto con cámara

  - Componente para seleccionar foto de galería
  - Función de compresión de imagen en cliente
  - Extracción de coordenadas GPS del navegador
  - Preview de fotos antes de subir
  - _Requirements: 1.2, 1.3, 3.1_

- [ ] 1.9 Implementar UploadManager en frontend
  - Función uploadFoto() con retry logic
  - Función compressImage() con canvas
  - Función extractGPS() del navegador
  - Progress bar durante upload
  - _Requirements: 1.2, 3.1, 3.3_

- [ ] 1.10 Integrar upload en formularios de reporte
  - Agregar campo de fotos a formulario de incidentes





  - Agregar campo de fotos a formulario de delitos


  - Mostrar previews de fotos seleccionadas

  - Permitir eliminar fotos antes de enviar
  - _Requirements: 1.1, 2.1_

- [ ] 1.11 Escribir unit tests para UploadService
  - Test validación de tipo de archivo
  - Test validación de tamaño


  - Test generación de nombre único
  - Test compresión de imagen
  - Test extracción de metadatos
  - _Requirements: 3.1, 3.2, 3.6_




## Fase 2: Sistema de Notificaciones


- [ ] 2. Implementar notificaciones en tiempo real
- [ ] 2.1 Instalar y configurar Flask-SocketIO
  - Agregar flask-socketio a requirements.txt
  - Configurar SocketIO en app.py
  - Configurar Redis como message queue





  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 2.2 Implementar WebSocketService
  - Handler para conexión de usuarios
  - Handler para desconexión


  - Función para emitir notificaciones a usuario específico
  - Función para emitir actualizaciones globales
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 2.3 Modificar NotificacionService para enviar en tiempo real

  - Integrar WebSocketService en notificar_incidente()
  - Integrar WebSocketService en notificar_delito()
  - Integrar WebSocketService en notificar_cambio_estado()
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 2.4 Escribir property test para notificaciones por severidad
  - **Property 2: Notificación a coordinador de puesto**
  - **Property 3: Notificación por severidad crítica**
  - **Validates: Requirements 1.5, 1.6, 4.1, 4.3**






- [ ] 2.5 Escribir property test para notificaciones de delitos
  - **Property 4: Notificación de delitos**
  - **Validates: Requirements 2.3, 4.4**

- [ ] 2.6 Crear modelo ConfiguracionNotificaciones
  - Crear tabla configuracion_notificaciones
  - Agregar campos de preferencias
  - Crear migración de base de datos
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 2.7 Implementar NotificacionesManager en frontend
  - Conectar a WebSocket con autenticación
  - Handler para nueva_notificacion
  - Actualizar badge de notificaciones no leídas
  - Mostrar toast notifications
  - _Requirements: 4.7, 4.8_

- [ ] 2.8 Crear componente NotificacionesPanel
  - Lista de notificaciones con scroll infinito
  - Marcar como leída al hacer clic
  - Navegar al reporte correspondiente
  - Filtrar por leídas/no leídas
  - _Requirements: 4.7, 4.8_

- [ ] 2.9 Agregar badge de notificaciones en navbar
  - Mostrar contador de no leídas
  - Dropdown con últimas notificaciones
  - Link a panel completo de notificaciones
  - _Requirements: 4.7_

- [ ] 2.10 Escribir unit tests para NotificacionService
  - Test notificaciones según severidad
  - Test notificaciones según gravedad
  - Test no duplicar notificaciones
  - Test notificación al reportante
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 2.11 Escribir integration test para flujo de notificaciones
  - Crear incidente → verificar notificaciones creadas
  - Cambiar estado → verificar notificación al reportante
  - Verificar WebSocket emite correctamente
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

## Fase 3: Gestión de Estados y Seguimiento

- [x] 3. Implementar UI para gestión de estados






- [ ] 3.1 Crear componente EstadoIncidenteModal
  - Modal para cambiar estado de incidente
  - Dropdown con estados disponibles según permisos
  - Campo de comentario obligatorio


  - Validación de permisos en frontend
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 3.2 Crear componente EstadoDelitoModal
  - Modal para cambiar estado de delito

  - Dropdown con estados disponibles según permisos
  - Campo de comentario obligatorio
  - Campos adicionales para denuncia formal

  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 3.3 Escribir property test para permisos de cambio de estado
  - **Property 14: Permisos para cambiar estado de incidentes**
  - **Validates: Requirements 5.6**



- [ ] 3.4 Escribir property test para campos obligatorios en resolución
  - **Property 16: Campos obligatorios en resolución**
  - **Validates: Requirements 5.3, 5.7**


- [ ] 3.5 Crear componente SeguimientoTimeline
  - Línea de tiempo vertical con registros
  - Mostrar usuario, fecha, acción y comentario

  - Iconos según tipo de acción
  - Formato de fecha relativo (hace X minutos)
  - _Requirements: 7.1, 7.2, 7.3_


- [ ] 3.6 Integrar seguimiento en vista de detalle de reporte
  - Agregar sección de seguimiento en página de detalle
  - Cargar seguimiento al abrir detalle
  - Actualizar en tiempo real cuando hay cambios
  - _Requirements: 7.1, 7.2, 7.3_

- [x] 3.7 Escribir property test para registro de seguimiento


  - **Property 11: Registro de seguimiento en creación**

  - **Property 12: Registro de seguimiento en cambio de estado**
  - **Validates: Requirements 2.4, 5.5, 6.3, 7.4, 7.5**

- [ ] 3.8 Escribir unit tests para gestión de estados
  - Test transiciones de estado válidas

  - Test validación de permisos
  - Test campos obligatorios
  - Test registro de seguimiento
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_



## Fase 4: Sincronización Offline

- [ ] 4. Implementar sincronización offline robusta
- [ ] 4.1 Configurar IndexedDB schema
  - Crear store reportes_pendientes

  - Crear store fotos_pendientes
  - Crear índices apropiados
  - _Requirements: 10.1, 10.2_




- [ ] 4.2 Implementar SyncManager
  - Función saveReporteLocally()
  - Función getPendingReportes()
  - Función syncReporte() con retry logic

  - Función syncAll()
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_


- [ ] 4.3 Agregar event listeners para online/offline
  - Handler onOnline() para iniciar sync
  - Handler onOffline() para detener sync
  - Auto-sync cada minuto cuando está online
  - _Requirements: 10.3_


- [ ] 4.4 Modificar formularios para guardar offline
  - Detectar si hay conexión antes de enviar
  - Guardar en IndexedDB si no hay conexión
  - Mostrar mensaje al usuario
  - _Requirements: 1.7, 10.1, 10.2_

- [ ] 4.5 Agregar indicador de reportes pendientes
  - Badge con número de reportes pendientes
  - Lista de reportes pendientes de sincronización
  - Distinguir visualmente reportes sincronizados vs pendientes
  - _Requirements: 10.6, 10.7_

- [ ] 4.6 Escribir property test para sincronización offline
  - **Property 18: Sincronización offline**
  - **Validates: Requirements 1.7, 10.3**

- [ ] 4.7 Escribir unit tests para SyncManager
  - Test guardar reporte localmente
  - Test sincronizar cuando hay conexión
  - Test manejar conflictos
  - Test reintentar en caso de error
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 4.8 Escribir integration test para flujo offline
  - Crear reporte sin conexión
  - Verificar guardado en IndexedDB
  - Simular recuperación de conexión
  - Verificar sincronización automática
  - _Requirements: 10.1, 10.2, 10.3_

## Fase 5: Permisos y Seguridad

- [ ] 5. Implementar control de acceso granular
- [ ] 5.1 Refactorizar obtener_incidentes() con filtros por rol
  - Testigo: solo sus reportes
  - Coordinador puesto: reportes de su puesto
  - Coordinador municipal: reportes de su municipio
  - Coordinador departamental: reportes de su departamento
  - Auditor/Super admin: todos los reportes
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 5.2 Refactorizar obtener_delitos() con filtros por rol
  - Aplicar misma lógica que incidentes
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 5.3 Agregar validación de permisos en endpoints de actualización
  - Validar que usuario puede cambiar estado
  - Validar que usuario puede denunciar formalmente
  - Validar que usuario puede acceder al reporte
  - _Requirements: 5.6, 6.6, 8.8_

- [ ] 5.4 Escribir property tests para permisos por rol
  - **Property 9: Permisos de visualización por rol**
  - **Property 10: Permisos de visualización por jurisdicción**
  - **Property 15: Permisos para denuncia formal**
  - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 6.6**

- [ ] 5.4 Implementar URLs firmadas para evidencia
  - Generar tokens temporales con expiración
  - Validar token antes de servir archivo
  - Registrar accesos a evidencia sensible
  - _Requirements: 3.5_

- [ ] 5.5 Agregar rate limiting a endpoints críticos
  - Limitar uploads a 10 por minuto
  - Limitar creación de reportes a 5 por hora
  - Limitar requests generales a 100 por minuto
  - _Requirements: Security_


- [ ] 5.6 Escribir unit tests para validación de permisos
  - Test acceso denegado fuera de jurisdicción
  - Test cambio de estado sin permisos
  - Test denuncia formal sin permisos
  - _Requirements: 5.6, 6.6, 8.8_



- [ ] 5.7 Escribir integration test para seguridad
  - Intentar acceder a reporte fuera de jurisdicción
  - Intentar cambiar estado sin permisos
  - Verificar denegación de acceso
  - _Requirements: 8.8_

## Fase 6: Visualización en Mapas

- [ ] 6. Mejorar indicadores visuales en mapas
- [ ] 6.1 Actualizar endpoint puestos-geolocalizados
  - Ya implementado: devuelve contadores de incidentes/delitos
  - Verificar que funciona correctamente
  - _Requirements: 9.1, 9.2, 9.3_

- [ ] 6.2 Mejorar popups de puestos en mapa
  - Mostrar sección de alertas si hay incidentes/delitos
  - Mostrar número de incidentes activos y críticos
  - Mostrar número de delitos activos y graves
  - Agregar badges con colores según severidad
  - _Requirements: 9.4_

- [ ] 6.3 Implementar animación para alertas críticas
  - Pulsar icono de alerta para incidentes críticos
  - Pulsar icono de alerta para delitos graves
  - _Requirements: 9.2, 9.3_

- [ ] 6.4 Escribir property tests para indicadores en mapa
  - **Property 19: Indicadores visuales en mapa**
  - **Property 20: Remoción de indicadores**
  - **Validates: Requirements 9.1, 9.2, 9.3, 9.6, 9.7**

- [ ] 6.5 Agregar filtros de mapa por tipo de alerta
  - Filtro para mostrar solo puestos con incidentes
  - Filtro para mostrar solo puestos con delitos
  - Filtro para mostrar solo alertas críticas
  - _Requirements: 9.1, 9.2, 9.3_

- [ ] 6.6 Actualizar mapa en tiempo real cuando hay cambios
  - Escuchar evento actualizar_mapa por WebSocket
  - Recargar datos de puestos
  - Actualizar indicadores visuales
  - _Requirements: 9.6, 9.7_


## Fase 7: Estadísticas y Reportes

- [ ] 7. Implementar dashboard de estadísticas
- [ ] 7.1 Crear página de estadísticas
  - Layout con cards para métricas principales
  - Gráficos con Chart.js
  - Filtros por fecha y jurisdicción
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7_

- [ ] 7.2 Implementar gráfico de incidentes por estado
  - Gráfico de barras con estados
  - Colores según estado
  - Tooltip con detalles
  - _Requirements: 11.1_

- [ ] 7.3 Implementar gráfico de incidentes por severidad
  - Gráfico de dona con severidades
  - Colores según severidad
  - Leyenda con porcentajes
  - _Requirements: 11.2_

- [ ] 7.4 Implementar gráfico de delitos por estado
  - Similar a incidentes por estado
  - _Requirements: 11.3_

- [ ] 7.5 Implementar gráfico de delitos por gravedad
  - Similar a incidentes por severidad
  - _Requirements: 11.4_

- [ ] 7.6 Agregar métrica de delitos denunciados
  - Card con número y porcentaje
  - Comparación con período anterior
  - _Requirements: 11.5_

- [ ] 7.7 Escribir unit tests para estadísticas
  - Test filtrado por jurisdicción
  - Test cálculo de porcentajes
  - Test agregaciones
  - _Requirements: 11.6, 11.7_

## Fase 8: Exportación de Evidencia

- [ ] 8. Implementar exportación de reportes
- [ ] 8.1 Instalar biblioteca para generación de PDFs
  - Agregar reportlab o weasyprint a requirements.txt
  - Configurar templates para PDFs
  - _Requirements: 12.1, 12.2_

- [ ] 8.2 Implementar ExportService
  - Función exportar_incidente_pdf()
  - Función exportar_delito_pdf()
  - Función exportar_multiples_pdf()
  - Incluir fotos de evidencia en PDF
  - _Requirements: 12.1, 12.2, 12.3, 12.4_

- [ ] 8.3 Crear endpoint POST /api/reportes/exportar
  - Recibir lista de IDs de reportes
  - Validar permisos de acceso
  - Generar PDFs
  - Retornar archivo ZIP si son múltiples
  - _Requirements: 12.1, 12.5, 12.6_

- [ ] 8.4 Registrar exportaciones en seguimiento
  - Crear registro cuando se exporta un reporte
  - Incluir usuario y fecha
  - _Requirements: 12.7_

- [ ] 8.5 Agregar botón de exportar en vista de detalle
  - Botón "Exportar PDF" en página de detalle
  - Descargar PDF automáticamente
  - Mostrar mensaje de éxito
  - _Requirements: 12.1_

- [ ] 8.6 Agregar exportación masiva en lista de reportes
  - Checkbox para seleccionar múltiples reportes
  - Botón "Exportar seleccionados"
  - Descargar ZIP con todos los PDFs
  - _Requirements: 12.5_

- [ ] 8.7 Escribir unit tests para exportación
  - Test generación de PDF
  - Test inclusión de evidencia
  - Test validación de permisos
  - Test registro de exportación
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.6, 12.7_

## Fase 9: Testing y Optimización

- [ ] 9. Checkpoint - Asegurar calidad del código
- [ ] 9.1 Ejecutar todos los unit tests
  - Verificar que todos los tests pasan
  - Corregir tests fallidos
  - Asegurar cobertura > 80%

- [ ] 9.2 Ejecutar todos los property-based tests
  - Verificar que todas las propiedades se cumplen
  - Corregir bugs encontrados por property testing
  - Aumentar número de iteraciones si es necesario

- [ ] 9.3 Ejecutar integration tests
  - Verificar flujos completos end-to-end
  - Corregir problemas de integración

- [ ] 9.4 Optimizar queries de base de datos
  - Agregar índices faltantes
  - Optimizar queries N+1
  - Verificar explain plans

- [ ] 9.5 Optimizar carga de imágenes
  - Implementar lazy loading
  - Generar thumbnails
  - Configurar caching apropiado

- [ ] 9.6 Realizar pruebas de carga
  - Simular 100 usuarios concurrentes
  - Verificar tiempos de respuesta
  - Identificar cuellos de botella

- [ ] 9.7 Revisar seguridad
  - Ejecutar análisis de vulnerabilidades
  - Verificar validación de inputs
  - Revisar permisos y autenticación

## Fase 10: Documentación y Deployment

- [ ] 10. Preparar para producción
- [ ] 10.1 Actualizar documentación técnica
  - Documentar nuevos endpoints
  - Documentar nuevos modelos
  - Actualizar diagramas de arquitectura

- [ ] 10.2 Crear guía de usuario
  - Cómo reportar incidentes con fotos
  - Cómo gestionar estados
  - Cómo ver notificaciones
  - Cómo exportar evidencia

- [ ] 10.3 Configurar variables de entorno
  - UPLOAD_FOLDER
  - MAX_UPLOAD_SIZE
  - SOCKETIO_MESSAGE_QUEUE
  - Otras configuraciones

- [ ] 10.4 Configurar almacenamiento de archivos
  - Decidir entre local/S3/Azure
  - Configurar permisos
  - Configurar backups

- [ ] 10.5 Configurar Redis para WebSocket
  - Instalar Redis
  - Configurar como message queue
  - Configurar persistencia

- [ ] 10.6 Ejecutar migraciones de base de datos
  - Crear backup de DB
  - Ejecutar migraciones
  - Verificar integridad de datos

- [ ] 10.7 Realizar pruebas en staging
  - Desplegar en ambiente de staging
  - Ejecutar suite completa de tests
  - Verificar funcionalidad end-to-end

- [ ] 10.8 Desplegar a producción
  - Crear backup completo
  - Desplegar nueva versión
  - Verificar que todo funciona
  - Monitorear logs y métricas

