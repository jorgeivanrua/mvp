# Implementation Plan - Dashboard Testigo Electoral

## Overview

Este plan documenta la implementación del Dashboard del Testigo Electoral, que ya está completamente funcional. Las 37 tareas están completadas y el sistema está en producción con todas las funcionalidades implementadas, incluyendo geolocalización GPS, tracking de ubicación, y mapas interactivos.

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
  - Función `seleccionarMesaDesdePanel()` para seleccionar desde panel lateral
  - Implementar panel lateral con lista de mesas
  - Mostrar estado de cada mesa:
    - Badge verde con cantidad de E-14 si tiene formularios
    - Badge gris "Sin E-14" si no tiene formularios
  - Función `actualizarPanelMesas()` para actualizar vista
  - Mostrar mesa seleccionada con clase "active"
  - Mostrar votantes registrados por mesa
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
  - Función `sincronizarBorradoresLocales()` para sincronizar con servidor
  - Botón "Guardar Borrador" en modal
  - Mostrar borradores con badge amarillo "💾 Guardado Localmente" en lista
  - Función `editarBorradorLocal()` para editar borradores
  - Función `eliminarBorradorLocalPorId()` para eliminar desde lista
  - Clave única por mesa y tipo de elección: `${mesa_id}_${tipo_eleccion_id}`
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 7. Implementar envío de formularios
  - Función `saveForm(accion)` con parámetro 'enviar' o 'borrador'
  - Validar campos requeridos antes de enviar (solo si accion='enviar')
  - Endpoint POST `/api/formularios` en backend
  - Cambiar estado a 'pendiente' al enviar
  - Mostrar confirmación de envío exitoso
  - Fallback a guardado local si falla conexión
  - Deshabilitar botones durante envío para prevenir doble envío
  - Limpiar formulario y cerrar modal después de enviar
  - Eliminar borrador local si el envío es exitoso
  - Actualizar vistas (formularios y panel de mesas) después de enviar
  - Delay de 500ms antes de cerrar modal para mostrar mensaje
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 8. Implementar visualización de formularios
  - Función `loadForms()` para cargar formularios del testigo
  - Función `updateFormsTable()` para renderizar tabla
  - Función `getMesaCodigoById()` para obtener código de mesa
  - Mostrar mesa, estado, total votos, fecha para cada formulario
  - Badges de colores según estado:
    - Pendiente (azul): 📤 Enviado - Pendiente Revisión
    - Validado (verde): ✅ Validado
    - Rechazado (rojo): ❌ Rechazado
    - Borrador (gris): 📝 Borrador
    - Local (amarillo): 💾 Guardado Localmente
  - Función `getStatusColor()` para colores de badges
  - Función `getEstadoLabel()` para labels de estados
  - Combinar formularios del servidor y borradores locales
  - Filas clickeables para editar borradores
  - Botones de editar/eliminar para borradores locales
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 9. Implementar carga de partidos y candidatos
  - Función `loadTiposEleccion()` para cargar tipos de elección
  - Función `cargarPartidosYCandidatos()` para cargar según tipo
  - Endpoint GET `/api/configuracion/partidos` en backend
  - Endpoint GET `/api/configuracion/candidatos` en backend con filtro por tipo_eleccion_id
  - Función `renderVotacionForm()` para renderizar formulario dinámico
  - Soporte para elecciones uninominales (un candidato por partido, sin votos de partido)
  - Soporte para elecciones por listas (múltiples candidatos + votos de partido)
  - Agrupar candidatos por partido
  - Cards con color del partido en border-left
  - Inputs numéricos con actualización en tiempo real
  - Mostrar total por partido en elecciones por listas
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
  - Combinar datos del servidor y locales usando SyncManager
  - Mostrar tipo, título, severidad/gravedad, descripción, fecha, mesa
  - Indicar estado de sincronización:
    - ✓ Reportado (verde) - Sincronizado con servidor
    - 💾 Local (amarillo) - Pendiente de sincronización
  - Colores distintivos según severidad/gravedad:
    - Baja/Leve (azul info)
    - Media (amarillo warning)
    - Alta/Grave (rojo danger)
    - Crítica/Muy Grave (gris oscuro)
  - Funciones `getSeveridadColor()` y `getGravedadColor()`
  - Funciones `getTipoIncidenteLabel()` y `getTipoDelitoLabel()`
  - Cards con border-left coloreado según severidad/gravedad
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 13. Implementar SyncManager universal
  - Crear módulo `frontend/static/js/sync-manager.js`
  - Clase `SyncManager` con métodos de sincronización
  - Función `init()` para inicializar sincronización automática
  - Función `syncAll()` para sincronizar todos los datos
  - Función `syncIncidents()` para sincronizar incidentes
  - Función `syncCrimes()` para sincronizar delitos
  - Funciones `saveIncidentLocally()` y `saveCrimeLocally()` para guardado local
  - Funciones `getLocalIncidents()` y `getLocalCrimes()` para lectura
  - Sincronización automática al cargar (2 segundos)
  - Sincronización periódica cada 5 minutos
  - Instancia global `window.syncManager`
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
  - Crear endpoints en `backend/routes/formularios_e14.py`:
    - GET `/api/formularios/mis-formularios` - Listar formularios del testigo
    - POST `/api/formularios` - Crear formulario E-14
    - PUT `/api/formularios/<id>` - Actualizar formulario
    - GET `/api/formularios/<id>` - Obtener formulario específico
  - Crear endpoints en `backend/routes/incidentes_delitos.py`:
    - POST `/api/incidentes-delitos/incidentes` - Reportar incidente
    - GET `/api/incidentes-delitos/incidentes` - Listar incidentes
    - POST `/api/incidentes-delitos/delitos` - Reportar delito
    - GET `/api/incidentes-delitos/delitos` - Listar delitos
    - GET `/api/incidentes-delitos/tipos-incidentes` - Tipos de incidentes
    - GET `/api/incidentes-delitos/tipos-delitos` - Tipos de delitos
  - Crear endpoint en `backend/routes/auth.py`:
    - POST `/api/auth/verificar-presencia` - Verificar presencia del testigo
  - Decoradores `@jwt_required()` y `@role_required(['testigo_electoral'])`
  - Validar acceso solo a mesas asignadas del testigo
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

- [x] 30. Implementar métodos en API Client
  - Agregar métodos en `frontend/static/js/api-client.js`:
    - `getFormulariosE14()` - Obtener formularios del testigo
    - `getFormularioE14(id)` - Obtener formulario específico
    - `createFormularioE14(data)` - Crear formulario
    - `updateFormularioE14(id, data)` - Actualizar formulario
    - `getTiposEleccion()` - Obtener tipos de elección
    - `getPartidos()` - Obtener partidos políticos
    - `getCandidatos(params)` - Obtener candidatos con filtros
    - `getTiposIncidentes()` - Obtener tipos de incidentes
    - `getTiposDelitos()` - Obtener tipos de delitos
    - `reportarIncidente(data)` - Reportar incidente (alias de crearIncidente)
    - `reportarDelito(data)` - Reportar delito (alias de crearDelito)
    - `getIncidentes(params)` - Obtener incidentes
    - `getDelitos(params)` - Obtener delitos
  - Todos los métodos retornan promesas con formato `{success, data, error}`
  - Manejo de errores centralizado en `handleResponse()`
  - _Requirements: Todos_

- [x] 31. Documentar código
  - Comentarios JSDoc en funciones principales
  - Comentarios explicativos en lógica compleja
  - Comentarios de secciones con separadores visuales
  - _Requirements: Mantenibilidad_

- [x] 32. Implementar verificación de presencia con geolocalización
  - Crear archivo `frontend/static/js/verificacion-presencia.js`
  - Implementar función `verificarPresencia()` con captura de GPS
  - Solicitar permiso de geolocalización al usuario
  - Capturar coordenadas GPS (latitud, longitud)
  - Capturar precisión de geolocalización
  - Enviar datos a endpoint `/api/verificacion/presencia`
  - Mostrar confirmación con coordenadas capturadas
  - Manejar error si usuario no otorga permiso
  - Permitir verificación sin GPS con advertencia
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 2.6, 2.9_

- [x] 33. Implementar tracking de ubicación y ping automático
  - Iniciar ping automático después de verificar presencia
  - Implementar función `iniciarPingAutomatico()` cada 15 minutos
  - Actualizar última ubicación en cada ping
  - Almacenar timestamp de última geolocalización
  - Detener ping al cerrar sesión
  - Guardar pings localmente si no hay conexión
  - Sincronizar pings cuando recupera conexión
  - _Requirements: 21.1, 21.2, 21.3, 21.4, 21.7_

- [x] 34. Agregar campos de geolocalización al modelo User
  - Agregar campo `ultima_latitud` (FLOAT) a modelo User
  - Agregar campo `ultima_longitud` (FLOAT) a modelo User
  - Agregar campo `ultima_geolocalizacion_at` (TIMESTAMP) a modelo User
  - Agregar campo `precision_geolocalizacion` (FLOAT) a modelo User
  - Crear migración SQL para agregar campos
  - Aplicar migración en base de datos
  - _Requirements: 2.4, 2.8, 21.2, 21.3_

- [x] 35. Implementar endpoints de geolocalización
  - Crear endpoint `POST /api/verificacion/presencia` en `backend/routes/verificacion_presencia.py`
  - Crear endpoint `GET /api/locations/puestos-geolocalizados` en `backend/routes/locations_geo.py`
  - Crear endpoint `GET /api/verificacion/usuarios-geolocalizados` en `backend/routes/locations_geo.py`
  - Validar coordenadas GPS en backend
  - Almacenar ubicación en base de datos
  - Notificar a coordinador sobre verificación
  - _Requirements: 2.4, 2.6, 22.1, 22.2, 22.3_

- [x] 36. Implementar mapa de puestos y testigos geolocalizados
  - Crear archivo `frontend/static/js/mapa-geolocalizacion.js`
  - Integrar librería de mapas (Leaflet o Google Maps)
  - Cargar puestos electorales con coordenadas GPS
  - Mostrar marcadores de puestos en el mapa
  - Cargar testigos con última ubicación conocida
  - Mostrar marcadores de testigos en el mapa
  - Usar colores diferentes para puestos y testigos
  - Mostrar información al hacer clic en marcador
  - Implementar filtros por departamento/municipio/puesto
  - Actualizar mapa automáticamente con nuevas ubicaciones
  - Mostrar precisión GPS en tooltip
  - _Requirements: 22.1, 22.2, 22.3, 22.4, 22.5, 22.6, 22.7, 22.8_

- [x] 37. Corregir verificación automática de presencia
  - Eliminar verificación automática en `init()`
  - Verificar presencia SOLO cuando testigo hace clic en botón
  - Iniciar ping automático DESPUÉS de verificar presencia
  - Mejorar manejo de `sessionStorage`
  - Prevenir llamadas automáticas a `/api/verificacion/presencia`
  - _Requirements: 2.7_

## Estado Actual

✅ **Dashboard Testigo Electoral 100% Funcional**

Todas las 37 tareas están completadas y el sistema está en producción. El dashboard incluye:

### Funcionalidades Principales
- ✅ **Gestión completa de formularios E-14**
  - Creación con cálculos automáticos
  - Guardado de borradores locales
  - Envío para revisión
  - Edición de borradores
  - Visualización con estados (pendiente/validado/rechazado/borrador/local)

- ✅ **Reporte de incidentes y delitos**
  - Modales de reporte con validaciones
  - Tipos predefinidos cargados desde servidor
  - Guardado local si falla conexión
  - Visualización con colores por severidad/gravedad

- ✅ **Sincronización automática universal (SyncManager)**
  - Sincronización al cargar (2 segundos)
  - Sincronización periódica (cada 5 minutos)
  - Indicador flotante con pendientes
  - Sincronización manual con botón
  - Limpieza de datos antiguos (>7 días)

- ✅ **Funcionamiento offline completo**
  - Guardado local en localStorage
  - Sincronización automática al recuperar conexión
  - Indicadores visuales de estado de sincronización

- ✅ **Interfaz móvil-first responsive**
  - Diseño optimizado para móviles
  - Inputs numéricos con teclado optimizado
  - Captura de fotos con cámara
  - Botones grandes y táctiles

- ✅ **Validaciones y cálculos automáticos**
  - Validación de campos requeridos
  - Cálculo automático de totales
  - Identificación de partido ganador
  - Prevención de errores

- ✅ **Gestión de múltiples mesas**
  - Selector de mesa
  - Panel lateral con lista de mesas
  - Filtrado por mesa seleccionada
  - Prevención de duplicados

- ✅ **Seguridad y auditoría**
  - Autenticación con JWT
  - Validación de rol testigo_electoral
  - Cierre de sesión seguro
  - Logs de todas las acciones

- ✅ **Verificación de presencia con geolocalización**
  - Captura de coordenadas GPS (latitud, longitud)
  - Registro de precisión de geolocalización
  - Verificación manual (no automática)
  - Almacenamiento de última ubicación
  - Timestamp de última geolocalización
  - Notificación a coordinador con ubicación

- ✅ **Tracking de ubicación y ping automático**
  - Ping automático cada 15 minutos después de verificar presencia
  - Actualización de última ubicación en cada ping
  - Almacenamiento de timestamp de última geolocalización
  - Sincronización de pings cuando hay conexión

- ✅ **Mapa de puestos y testigos geolocalizados**
  - Mapa interactivo con marcadores de puestos
  - Marcadores de testigos con última ubicación
  - Información al hacer clic en marcadores
  - Actualización automática del mapa
  - Visualización de precisión GPS

### Archivos Implementados
- `frontend/templates/testigo/dashboard.html` - Template HTML
- `frontend/static/js/testigo-dashboard-final-fix.js` - Lógica principal corregida
- `frontend/static/js/testigo-presencia-simple.js` - Verificación de presencia
- `frontend/static/js/verificacion-presencia.js` - Geolocalización completa
- `frontend/static/js/mapa-geolocalizacion.js` - Mapa interactivo
- `frontend/static/js/sync-manager.js` - Sincronización universal
- `frontend/static/js/api-client.js` - Cliente API con métodos
- `backend/routes/testigo.py` - Endpoints específicos del testigo
- `backend/routes/formularios_e14.py` - Endpoints de formularios
- `backend/routes/incidentes_delitos.py` - Endpoints de incidentes/delitos
- `backend/routes/verificacion_presencia.py` - Verificación con GPS
- `backend/routes/locations_geo.py` - Puestos y usuarios geolocalizados
- `backend/models/user.py` - Campos de geolocalización (ultima_latitud, ultima_longitud, ultima_geolocalizacion_at, precision_geolocalizacion)
- `backend/routes/frontend.py` - Ruta `/testigo/dashboard`

## Mejoras Futuras (Opcionales)

- [ ] Implementar PWA con Service Workers
- [ ] Agregar soporte para modo oscuro
- [ ] Implementar notificaciones push en tiempo real
- [ ] Agregar gráficos de resultados en tiempo real
- [ ] Implementar chat con coordinador
- [ ] Implementar firma digital de formularios
- [ ] Agregar exportación de formularios a PDF
- [ ] Agregar validación de ubicación vs mesa asignada (geofencing)
- [ ] Implementar alertas cuando el testigo se aleja del puesto
- [ ] Agregar historial de ubicaciones del testigo

