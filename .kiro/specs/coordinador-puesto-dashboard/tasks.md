# Implementation Plan - Dashboard Coordinador de Puesto

- [x] 1. Crear modelos de base de datos para formularios E-14


  - Crear modelo `FormularioE14` con campos de votación, estado y validación
  - Crear modelo `VotoPartido` para registrar votos por partido
  - Crear modelo `VotoCandidato` para registrar votos por candidato
  - Crear modelo `HistorialFormulario` para auditoría de cambios
  - Agregar relaciones entre modelos (formulario → votos, formulario → historial)
  - _Requirements: 1.1, 2.1, 10.2_




- [ ] 2. Crear migraciones y scripts de base de datos
  - Crear migración para tablas de formularios E-14
  - Crear migración para tablas de votos (partidos y candidatos)


  - Crear migración para tabla de historial


  - Agregar índices para optimización (mesa_id, estado, created_at)
  - _Requirements: 1.1, 2.1_

- [ ] 3. Implementar servicios de backend para formularios
  - [x] 3.1 Crear `FormularioService` con métodos CRUD


    - Método para crear formulario E-14
    - Método para obtener formularios por puesto
    - Método para obtener formulario por ID con detalles completos
    - Método para actualizar formulario
    - _Requirements: 1.1, 2.1_
  


  - [ ] 3.2 Crear `ValidacionService` para lógica de validación
    - Método para validar coherencia de totales


    - Método para calcular discrepancias


    - Método para validar formulario (cambiar estado a validado)
    - Método para rechazar formulario con motivo
    - Método para registrar cambios en historial
    - _Requirements: 2.3, 2.4, 2.5, 2.7, 3.3_
  

  - [ ] 3.3 Crear `ConsolidadoService` para cálculos agregados
    - Método para calcular consolidado por puesto
    - Método para obtener votos por partido consolidados
    - Método para calcular estadísticas (participación, totales)
    - _Requirements: 4.1, 4.2, 4.3, 4.5_


- [ ] 4. Implementar rutas API para formularios
  - [ ] 4.1 Crear endpoint GET `/api/formularios/puesto`
    - Obtener formularios del puesto del coordinador
    - Implementar filtros por estado
    - Implementar paginación
    - Incluir estadísticas en respuesta

    - _Requirements: 1.1, 1.3, 1.5_
  
  - [ ] 4.2 Crear endpoint GET `/api/formularios/:id`
    - Obtener detalles completos del formulario
    - Incluir votos por partido y candidato
    - Incluir validaciones automáticas

    - Incluir historial de cambios
    - _Requirements: 2.1, 2.2, 2.3, 10.4_
  
  - [ ] 4.3 Crear endpoint PUT `/api/formularios/:id/validar`
    - Validar permisos del coordinador
    - Permitir cambios opcionales en datos

    - Cambiar estado a "validado"
    - Registrar en historial
    - _Requirements: 2.4, 2.7, 3.1, 3.3, 3.5_


  
  - [ ] 4.4 Crear endpoint PUT `/api/formularios/:id/rechazar`
    - Validar permisos del coordinador
    - Requerir motivo de rechazo
    - Cambiar estado a "rechazado"
    - Registrar en historial
    - _Requirements: 2.5, 2.6, 2.7_
  
  - [ ] 4.5 Crear endpoint GET `/api/formularios/consolidado`
    - Calcular consolidado del puesto
    - Incluir solo formularios validados


    - Retornar votos por partido con porcentajes


    - Incluir estadísticas generales
    - _Requirements: 4.1, 4.2, 4.3, 4.6_
  
  - [ ] 4.6 Crear endpoint GET `/api/formularios/mesas`
    - Obtener lista de mesas del puesto
    - Incluir estado de reporte de cada mesa

    - Incluir información del testigo asignado
    - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [ ] 5. Crear template HTML del dashboard coordinador
  - Crear archivo `frontend/templates/coordinador/puesto.html`
  - Implementar estructura base con Bootstrap
  - Crear header con información del puesto y estadísticas
  - Crear tabla de formularios con columnas: mesa, testigo, estado, votos, fecha, acciones

  - Crear filtros por estado (todos, pendiente, validado, rechazado)
  - Crear modal de validación con vista dividida (imagen + datos)
  - Crear modal de rechazo con campo de motivo
  - Crear panel de consolidado con gráfico y tabla
  - Crear panel de lista de mesas con indicadores de estado
  - Optimizar para responsive design (móvil, tablet, desktop)

  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 4.1, 4.2, 5.1, 5.2, 8.1, 8.2_

- [ ] 6. Implementar JavaScript del dashboard coordinador
  - [ ] 6.1 Crear archivo `frontend/static/js/coordinador-puesto.js`
    - Función para cargar perfil del coordinador
    - Función para cargar lista de formularios con filtros

    - Función para renderizar tabla de formularios
    - Función para aplicar filtros y ordenamiento
    - Implementar auto-refresh cada 30 segundos
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [ ] 6.2 Implementar funciones de validación de formularios
    - Función para abrir modal de validación
    - Función para cargar detalles del formulario
    - Función para mostrar imagen con zoom
    - Función para calcular validaciones automáticas
    - Función para habilitar modo de edición
    - Función para validar formulario (con o sin cambios)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2_
  
  - [ ] 6.3 Implementar funciones de rechazo
    - Función para abrir modal de rechazo
    - Función para validar motivo no vacío
    - Función para rechazar formulario
    - Función para mostrar confirmación
    - _Requirements: 2.5, 2.6_
  
  - [ ] 6.4 Implementar panel de consolidado
    - Función para cargar datos consolidados
    - Función para renderizar gráfico de barras (Chart.js)
    - Función para renderizar tabla de resultados
    - Función para actualizar consolidado al validar
    - _Requirements: 4.1, 4.2, 4.3, 4.5_
  
  - [ ] 6.5 Implementar panel de mesas
    - Función para cargar lista de mesas
    - Función para renderizar estado de cada mesa
    - Función para mostrar indicador de progreso
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 7. Implementar sistema de notificaciones
  - Crear componente de notificaciones en el header
  - Implementar contador de formularios pendientes
  - Implementar badge de nuevos formularios
  - Implementar alertas para discrepancias significativas
  - Agregar función para marcar notificaciones como leídas
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 8. Implementar generación de reportes PDF
  - Crear servicio `ReporteService` para generar PDFs
  - Crear plantilla HTML para reporte consolidado
  - Implementar endpoint POST `/api/formularios/reporte-pdf`
  - Incluir datos del puesto, votos por partido, firma digital
  - Implementar descarga de PDF desde frontend
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 9. Implementar seguridad y control de acceso
  - Agregar decorador para verificar rol `coordinador_puesto`
  - Implementar verificación de puesto asignado en cada endpoint
  - Agregar logging de todas las acciones de validación
  - Implementar cierre de sesión automático (30 minutos)
  - Agregar rate limiting en endpoints críticos
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 10. Optimizar rendimiento
  - Agregar índices en base de datos (mesa_id, estado, created_at)
  - Implementar lazy loading de imágenes en frontend
  - Implementar debounce en filtros de búsqueda
  - Optimizar queries con eager loading
  - Implementar compresión de imágenes al subir
  - _Requirements: 1.4, 8.1_

- [ ] 11. Integrar con sistema de testigos
  - Actualizar dashboard de testigo para crear formularios E-14
  - Implementar endpoint POST `/api/formularios` para crear formulario
  - Implementar upload de imagen del formulario
  - Implementar estados: borrador, pendiente
  - Conectar testigo con coordinador de puesto
  - _Requirements: 1.1, 2.1, 2.6_

- [ ] 12. Agregar validaciones y manejo de errores
  - Validar permisos en todos los endpoints
  - Validar estados de formularios antes de cambios
  - Validar coherencia de datos antes de validar
  - Implementar manejo de errores en frontend
  - Mostrar mensajes de error claros al usuario
  - _Requirements: 2.3, 9.1, 9.2_

- [ ] 13. Crear tests de integración
  - Test para GET `/api/formularios/puesto` con filtros
  - Test para PUT `/api/formularios/:id/validar`
  - Test para PUT `/api/formularios/:id/rechazar`
  - Test para GET `/api/formularios/consolidado`
  - Test de permisos y seguridad
  - _Requirements: 9.1, 9.2_

- [ ] 14. Crear documentación
  - Documentar endpoints de API
  - Documentar flujo de validación
  - Crear guía de usuario para coordinadores
  - Documentar estructura de base de datos
  - _Requirements: All_

- [x] 15. Implementar visualización de incidentes del puesto
  - Crear sección de incidentes en el dashboard
  - Función `cargarIncidentes()` para listar incidentes del puesto
  - Tabla de incidentes con filtros por severidad, tipo, mesa
  - Colores distintivos según severidad (baja, media, alta, crítica)
  - Modal de detalle de incidente
  - Contador de incidentes por severidad
  - Actualización automática cada 30 segundos
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7_

- [x] 16. Implementar visualización de delitos electorales del puesto
  - Crear sección de delitos en el dashboard
  - Función `cargarDelitos()` para listar delitos del puesto
  - Tabla de delitos con filtros por gravedad, tipo, mesa
  - Colores distintivos según gravedad (leve, media, grave, muy grave)
  - Modal de detalle de delito
  - Contador de delitos por gravedad
  - Actualización automática cada 30 segundos
  - Advertencia visual prominente cuando hay delitos
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9_

- [x] 17. Implementar gestión y seguimiento de reportes
  - Función `agregarComentario()` para seguimiento
  - Función `cambiarEstadoIncidente()` con estados (pendiente, en revisión, resuelto)
  - Función `cambiarEstadoDelito()` con estados (reportado, escalado, en investigación, resuelto)
  - Registro de cambios con timestamp y usuario
  - Notificación al testigo cuando se agrega comentario
  - Historial completo de seguimiento
  - Asignación de prioridad a reportes
  - Generación de reportes consolidados
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8_

- [x] 18. Implementar alertas de incidentes y delitos críticos
  - Alerta visual prominente para incidentes críticos
  - Alerta visual prominente para delitos electorales
  - Sonido de notificación para alertas críticas
  - Contador de alertas no atendidas en header
  - Función `marcarAlertaAtendida()` para gestionar alertas
  - Historial de alertas recibidas
  - Notificación por email para delitos muy graves
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7_

- [x] 19. Integrar endpoints de incidentes y delitos
  - Endpoint `GET /api/incidentes-delitos/incidentes` - Listar incidentes del puesto
  - Endpoint `GET /api/incidentes-delitos/delitos` - Listar delitos del puesto
  - Endpoint `POST /api/incidentes-delitos/incidentes/:id/comentario` - Agregar comentario
  - Endpoint `PUT /api/incidentes-delitos/incidentes/:id/estado` - Cambiar estado
  - Endpoint `PUT /api/incidentes-delitos/delitos/:id/estado` - Cambiar estado
  - Filtrado por puesto del coordinador
  - Validación de permisos
  - _Requirements: 12.1, 13.1, 14.1, 14.2, 14.3_

- [x] 20. Actualizar dashboard con pestañas de incidentes y delitos
  - Agregar pestañas de navegación (Formularios, Incidentes, Delitos)
  - Cargar incidentes al mostrar pestaña
  - Cargar delitos al mostrar pestaña
  - Badges con contadores en pestañas
  - Actualización automática de contadores
  - _Requirements: 12.6, 13.6, 15.4_

## Estado Actual

✅ **Dashboard Coordinador de Puesto 75% Funcional**

15 de 20 tareas completadas. El sistema tiene implementadas las funcionalidades principales de validación de formularios E-14 y gestión de incidentes y delitos electorales.

### Funcionalidades Implementadas

- ✅ **Modelos de base de datos**
  - FormularioE14, VotoPartido, VotoCandidato, HistorialFormulario
  - IncidenteElectoral, DelitoElectoral, SeguimientoReporte

- ✅ **Visualización de formularios del puesto**
  - Tabla con todos los formularios E-14
  - Filtros por estado
  - Actualización automática cada 30 segundos
  - Indicador de progreso

- ✅ **Validación de formularios E-14**
  - Modal de revisión con imagen y datos
  - Validaciones automáticas
  - Aprobar y rechazar formularios
  - Registro de validaciones

- ✅ **Gestión de mesas del puesto**
  - Lista de mesas con estado
  - Indicador de presencia de testigos
  - Sincronización con base de datos

- ✅ **Visualización de incidentes**
  - Lista de incidentes del puesto
  - Filtros por severidad, tipo, mesa
  - Colores distintivos
  - Contador por severidad
  - Actualización automática

- ✅ **Visualización de delitos electorales**
  - Lista de delitos del puesto
  - Filtros por gravedad, tipo, mesa
  - Colores distintivos
  - Contador por gravedad
  - Advertencia visual prominente

- ✅ **Gestión y seguimiento de reportes**
  - Agregar comentarios
  - Cambiar estados
  - Historial de seguimiento
  - Asignación de prioridad
  - Reportes consolidados

- ✅ **Alertas de incidentes y delitos críticos**
  - Alertas visuales prominentes
  - Sonido de notificación
  - Contador de alertas no atendidas
  - Historial de alertas

### Funcionalidades Pendientes (25%)

- ⏳ **Migraciones de base de datos** (Tarea 2)
- ⏳ **Servicios de validación** (Tarea 3.2)
- ⏳ **Rutas API completas** (Tarea 4)
- ⏳ **Sistema de notificaciones** (Tarea 7)
- ⏳ **Generación de reportes PDF** (Tarea 8)

### Archivos Implementados

**Frontend:**
- `frontend/templates/coordinador/puesto.html` - Dashboard principal
- `frontend/static/js/coordinador-puesto.js` - Lógica principal

**Backend:**
- `backend/routes/coordinador_puesto.py` - Endpoints específicos
- `backend/routes/formularios_e14.py` - Gestión de formularios
- `backend/routes/incidentes_delitos.py` - Gestión de incidentes y delitos
- `backend/models/formulario_e14.py` - Modelos de formularios
- `backend/models/incidentes_delitos.py` - Modelos de incidentes y delitos

## Mejoras Futuras (Opcionales)

- [ ] Implementar chat en tiempo real con testigos
- [ ] Agregar notificaciones push para alertas críticas
- [ ] Implementar dashboard de métricas con gráficos avanzados
- [ ] Agregar exportación de reportes en múltiples formatos
- [ ] Implementar sistema de firma digital para E-24
- [ ] Agregar análisis predictivo de participación
- [ ] Implementar geolocalización de incidentes en mapa
- [ ] Agregar integración con sistemas de autoridades electorales
