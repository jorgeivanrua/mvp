# Implementation Plan - Dashboard Testigo Electoral

## Overview

Este plan documenta la implementación del Dashboard del Testigo Electoral, que ya está completamente funcional. Las tareas marcadas como completadas representan el estado actual del sistema.

## Tasks

- [x] 1. Crear estructura base del dashboard
  - Crear template HTML `frontend/templates/testigo/dashboard.html`
  - Implementar header con información del usuario
  - Agregar botones de sincronización y cerrar sesión
  - Crear tabs de navegación (Formularios, Incidentes, Delitos)
  - Implementar diseño responsive móvil-first
  - _Requirements: 1.1, 12.1, 12.2, 18.1_

- [x] 2. Implementar gestión de mesas asignadas
  - Crear función `loadMesas()` para cargar mesas del testigo
  - Implementar selector de mesa con dropdown
  - Crear función `cambiarMesa()` para cambiar mesa activa
  - Implementar panel lateral con lista de mesas
  - Mostrar estado de cada mesa (con/sin formularios)
  - Función `actualizarPanelMesas()` para actualizar vista
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 15.1, 15.2_

- [x] 3. Implementar verificación de presencia
  - Crear botón "Verificar Presencia" en UI
  - Implementar función `verificarPresencia()` 
  - Crear endpoint `/api/auth/verificar-presencia` en backend
  - Registrar timestamp de verificación en BD
  - Mostrar confirmación visual de presencia verificada
  - Función `verificarEstadoPresencia()` para cargar estado
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 4. Crear formulario E-14
  - Implementar modal de creación con Bootstrap
  - Sección de información básica (mesa, tipo elección)
  - Sección de foto del formulario con preview
  - Sección de datos de votación (nulos, blancos, no marcadas)
  - Sección de votos por partido y candidato
  - Sección de resumen automático
  - Campo de observaciones opcional
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

- [x] 5. Implementar cálculos automáticos
  - Función `calcularTotales()` para cálculos en tiempo real
  - Calcular votos válidos (suma de votos por partido/candidato)
  - Calcular total votos (válidos + nulos + blancos)
  - Calcular total tarjetas (votos + no marcadas)
  - Identificar partido con más votos
  - Actualizar resumen automáticamente
  - Cargar votantes registrados de la mesa
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 20.1, 20.2, 20.3, 20.4, 20.5_

- [x] 6. Implementar guardado de borradores
  - Función `guardarBorradorLocal()` para guardar en localStorage
  - Función `obtenerBorradoresLocales()` para leer borradores
  - Función `eliminarBorradorLocal()` para eliminar borradores
  - Botón "Guardar Borrador" en modal
  - Mostrar borradores con badge gris en lista
  - Función `editarBorradorLocal()` para editar borradores
  - Función `eliminarBorradorLocalPorId()` para eliminar desde lista
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 7. Implementar envío de formularios
  - Función `saveForm(accion)` con parámetro 'enviar' o 'borrador'
  - Validar campos requeridos antes de enviar
  - Endpoint POST `/api/formularios` en backend
  - Cambiar estado a 'pendiente' al enviar
  - Mostrar confirmación de envío exitoso
  - Fallback a guardado local si falla conexión
  - Limpiar formulario y cerrar modal después de enviar
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 8. Implementar visualización de formularios
  - Función `loadForms()` para cargar formularios del testigo
  - Función `updateFormsTable()` para renderizar tabla
  - Mostrar mesa, estado, total votos, fecha para cada formulario
  - Badges de colores según estado (pendiente/validado/rechazado/borrador/local)
  - Función `getStatusColor()` para colores de badges
  - Función `getEstadoLabel()` para labels de estados
  - Combinar formularios del servidor y locales
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 9. Implementar carga de partidos y candidatos
  - Función `loadTiposEleccion()` para cargar tipos de elección
  - Función `cargarPartidosYCandidatos()` para cargar según tipo
  - Endpoint GET `/api/configuracion/partidos` en backend
  - Endpoint GET `/api/configuracion/candidatos` en backend
  - Función `renderVotacionForm()` para renderizar formulario dinámico
  - Soporte para elecciones uninominales y por listas
  - Agrupar candidatos por partido
  - _Requirements: 3.2, 3.3, 3.4_

- [x] 10. Implementar reporte de incidentes
  - Crear modal de reporte de incidentes
  - Función `reportarIncidente()` para abrir modal
  - Función `guardarIncidente()` para guardar incidente
  - Endpoint POST `/api/incidentes-delitos/incidentes` en backend
  - Función `loadTiposIncidentes()` para cargar tipos
  - Campos: tipo, título, severidad, descripción
  - Guardar localmente si falla conexión
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [x] 11. Implementar reporte de delitos
  - Crear modal de reporte de delitos con advertencia
  - Función `reportarDelito()` para abrir modal
  - Función `guardarDelito()` para guardar delito
  - Endpoint POST `/api/incidentes-delitos/delitos` en backend
  - Función `loadTiposDelitos()` para cargar tipos
  - Campos: tipo, título, gravedad, descripción, testigos adicionales
  - Confirmación antes de reportar
  - Guardar localmente si falla conexión
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8_

- [x] 12. Implementar visualización de incidentes y delitos
  - Función `cargarIncidentes()` para cargar y renderizar incidentes
  - Función `cargarDelitos()` para cargar y renderizar delitos
  - Combinar datos del servidor y locales
  - Mostrar tipo, título, severidad/gravedad, descripción, fecha
  - Indicar estado de sincronización (sincronizado/pendiente)
  - Colores distintivos según severidad/gravedad
  - Funciones `getSeveridadColor()` y `getGravedadColor()`
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 13. Implementar SyncManager universal
  - Crear módulo `frontend/static/js/sync-manager.js`
  - Clase `SyncManager` con métodos de sincronización
  - Función `init()` para inicializar sincronización automática
  - Función `syncAll()` para sincronizar todos los datos
  - Función `syncIncidents()` para sincronizar incidentes
  - Función `syncCrimes()` para sincronizar delitos
  - Sincronización automática al cargar (2 segundos)
  - Sincronización periódica cada 5 minutos
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

- [x] 14. Implementar indicador de sincronización
  - Función `updateIndicator()` para actualizar indicador
  - Indicador flotante en esquina inferior derecha
  - Mostrar cantidad total de registros pendientes
  - Desglosar por tipo (formularios, incidentes, delitos)
  - Botón de sincronización manual en indicador
  - Ocultar indicador cuando no hay pendientes
  - Actualización automática cada 30 segundos
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

- [x] 15. Implementar validaciones de formularios
  - Validar selección de mesa
  - Validar selección de tipo de elección
  - Validar campos numéricos
  - Validar valores no negativos
  - Función `form.checkValidity()` de HTML5
  - Mostrar mensajes de error con `form.reportValidity()`
  - Prevenir envío con errores
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6_

- [x] 16. Implementar gestión de múltiples mesas
  - Permitir cambiar entre mesas asignadas
  - Filtrar formularios por mesa seleccionada
  - Mostrar claramente mesa seleccionada
  - Permitir crear formularios para cualquier mesa asignada
  - Prevenir múltiples formularios para misma mesa/tipo
  - Deshabilitar mesas que ya tienen formulario
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

- [x] 17. Implementar interfaz móvil-first
  - CSS responsive con media queries
  - Inputs optimizados para móvil (type="number")
  - Botón de cámara para tomar fotos (capture="environment")
  - Botones grandes y táctiles
  - Modales adaptados para móvil
  - Función `setupImagePreview()` para preview de fotos
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_

- [x] 18. Implementar manejo de errores
  - Try-catch en todas las funciones async
  - Mensajes de error con `Utils.showError()`
  - Mensajes de advertencia con `Utils.showWarning()`
  - Mensajes de éxito con `Utils.showSuccess()`
  - Fallback a guardado local en errores de conexión
  - Logging de errores en console
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5, 17.6_

- [x] 19. Implementar seguridad y cierre de sesión
  - Función `logout()` para cerrar sesión
  - Limpiar tokens de localStorage
  - Redirigir a página de login
  - Mantener datos locales después de logout
  - Botón de cerrar sesión visible en header
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [x] 20. Implementar instrucciones y ayuda
  - Panel de instrucciones en sidebar
  - Lista de pasos para crear formulario
  - Tooltips en campos con `title` attribute
  - Iconos intuitivos de Bootstrap Icons
  - Mensajes de confirmación para acciones importantes
  - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_

- [x] 21. Integrar con backend
  - Crear endpoints en `backend/routes/formularios_e14.py`
  - Crear endpoints en `backend/routes/incidentes_delitos.py`
  - Decoradores `@jwt_required()` y `@role_required(['testigo_electoral'])`
  - Validar acceso solo a mesas asignadas
  - Registrar blueprints en `backend/app.py`
  - Crear ruta frontend `/testigo/dashboard` en `backend/routes/frontend.py`
  - _Requirements: Todos_

- [x] 22. Implementar limpieza de datos antiguos
  - Función `cleanOldSyncedData()` en SyncManager
  - Eliminar datos sincronizados con más de 7 días
  - Ejecutar al cargar la página
  - Mantener localStorage limpio
  - _Requirements: 17.2_

- [x] 23. Optimizar performance
  - Debouncing en búsquedas
  - Lazy loading de imágenes
  - Minimizar re-renders
  - Batch de sincronización
  - Throttling de auto-refresh
  - _Requirements: Performance_

- [x] 24. Agregar funcionalidad de edición
  - Función `editForm()` para editar formularios del servidor
  - Función `viewForm()` para ver formularios (preparada)
  - Permitir editar solo borradores
  - Cargar datos del formulario en modal
  - Deshabilitar cambio de mesa y tipo elección al editar
  - _Requirements: 4.3, 6.4_

- [x] 25. Implementar auto-selección de mesa
  - Si solo hay una mesa, seleccionarla automáticamente
  - Preseleccionar mesa en formulario si está seleccionada
  - Actualizar información de mesa al cambiar
  - _Requirements: 1.4, 15.3_

- [x] 26. Agregar soporte para elecciones uninominales
  - Detectar tipo de elección (uninominal vs listas)
  - Renderizar formulario diferente según tipo
  - Un candidato por partido en uninominales
  - Sin votos de partido en uninominales
  - _Requirements: 3.2, 3.3_

- [x] 27. Implementar funciones helper de localStorage
  - `obtenerBorradoresLocales()`
  - `obtenerIncidentesLocales()`
  - `obtenerDelitosLocales()`
  - `guardarIncidenteLocal()`
  - `guardarDelitoLocal()`
  - Manejo de errores en todas las funciones
  - _Requirements: 4.2, 7.5, 8.6_

- [x] 28. Agregar eventos de tabs
  - Cargar incidentes al mostrar tab de incidentes
  - Cargar delitos al mostrar tab de delitos
  - Event listeners con `shown.bs.tab`
  - _Requirements: 9.1_

- [x] 29. Implementar selección de todo el texto en inputs
  - Event listener global para inputs numéricos
  - Seleccionar texto al hacer focus
  - Facilitar edición rápida
  - _Requirements: 12.2_

- [x] 30. Documentar código
  - Comentarios JSDoc en funciones principales
  - Comentarios explicativos en lógica compleja
  - README con instrucciones de uso
  - _Requirements: Mantenibilidad_

## Estado Actual

✅ **Dashboard Testigo Electoral 100% Funcional**

Todas las tareas están completadas y el sistema está en producción. El dashboard incluye:

- ✅ Gestión completa de formularios E-14
- ✅ Reporte de incidentes y delitos
- ✅ Sincronización automática universal
- ✅ Funcionamiento offline completo
- ✅ Interfaz móvil-first responsive
- ✅ Validaciones y cálculos automáticos
- ✅ Gestión de múltiples mesas
- ✅ Seguridad y auditoría

## Mejoras Futuras (Opcionales)

- [ ] Implementar PWA con Service Workers
- [ ] Agregar soporte para modo oscuro
- [ ] Implementar notificaciones push
- [ ] Agregar gráficos de resultados en tiempo real
- [ ] Implementar chat con coordinador
- [ ] Agregar geolocalización para verificar ubicación
- [ ] Implementar firma digital de formularios
- [ ] Agregar exportación de formularios a PDF

