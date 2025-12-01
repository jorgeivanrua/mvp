# Implementation Plan: Mejoras Admin y Mapas

## Fase 1: Backend - Modelos y Migraciones

- [ ] 1. Crear modelos de base de datos para partidos y candidatos
- [x] 1.1 Crear modelo PartidoPolitico


  - Definir campos: id, nombre, sigla, color, logo_url, activo, fecha_creacion, fecha_actualizacion
  - Definir relación con Candidato
  - Agregar validaciones de modelo
  - _Requirements: 3.1, 3.2, 3.3_


- [ ] 1.2 Crear modelo Candidato
  - Definir campos: id, nombre_completo, partido_id, tipo_eleccion_id, cargo, numero_lista, foto_url, activo
  - Definir relaciones con PartidoPolitico y TipoEleccion
  - Agregar validaciones de modelo

  - _Requirements: 4.1, 4.2, 4.3_

- [ ] 1.3 Crear modelo ConfiguracionSistema
  - Definir campos: id, clave, valor, tipo, descripcion, fecha_actualizacion

  - Agregar métodos helper para get/set valores tipados
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 1.4 Crear migración de base de datos
  - Crear tabla partidos_politicos con índices
  - Crear tabla candidatos con índices y foreign keys


  - Crear tabla configuracion_sistema con índices
  - Agregar datos iniciales de configuración
  - _Requirements: 3.1, 4.1, 8.1_

- [ ] 1.5 Escribir property test para validación de modelos
  - **Property 7: All party fields are editable**


  - **Property 11: All candidate fields are editable**
  - **Validates: Requirements 3.3, 4.3**

## Fase 2: Backend - Servicios de Partidos Políticos

- [x] 2. Implementar servicios para gestión de partidos

- [ ] 2.1 Crear PartidoService con operaciones CRUD
  - Implementar listar_partidos() con filtros
  - Implementar obtener_partido(id)
  - Implementar crear_partido(data) con validaciones
  - Implementar actualizar_partido(id, data)
  - Implementar eliminar_partido(id) con verificación de candidatos


  - _Requirements: 3.1, 3.2, 3.3, 3.4_



- [ ] 2.2 Implementar validación de logo de partido
  - Validar formato de archivo (jpg, jpeg, png, webp)
  - Validar tamaño de archivo (max 5MB)
  - Generar nombre único para archivo
  - Guardar archivo en directorio seguro
  - _Requirements: 3.5_

- [ ] 2.3 Escribir property test para eliminación de partidos
  - **Property 8: Party deletion requires no associated candidates**
  - **Validates: Requirements 3.4**

- [ ] 2.4 Escribir property test para validación de logo
  - **Property 9: Party logo upload validation**
  - **Validates: Requirements 3.5**

## Fase 3: Backend - Rutas de Partidos Políticos

- [ ] 3. Crear endpoints REST para partidos
- [ ] 3.1 Implementar GET /api/partidos
  - Listar todos los partidos con paginación
  - Agregar filtros por activo
  - Incluir contador de candidatos
  - Validar permisos de Super Admin
  - _Requirements: 3.1_

- [ ] 3.2 Implementar POST /api/partidos
  - Recibir datos del partido
  - Validar campos obligatorios
  - Crear partido en base de datos
  - Retornar partido creado
  - _Requirements: 3.2_

- [ ] 3.3 Implementar PUT /api/partidos/<id>
  - Recibir datos actualizados
  - Validar que partido existe
  - Actualizar partido en base de datos
  - Retornar partido actualizado
  - _Requirements: 3.3_

- [ ] 3.4 Implementar DELETE /api/partidos/<id>
  - Validar que partido existe
  - Verificar que no tiene candidatos asociados
  - Eliminar partido de base de datos
  - Retornar confirmación
  - _Requirements: 3.4_

- [ ] 3.5 Implementar POST /api/partidos/<id>/logo
  - Recibir archivo multipart/form-data
  - Validar formato y tamaño
  - Guardar archivo
  - Actualizar logo_url del partido
  - Retornar URL del logo
  - _Requirements: 3.5_

- [ ] 3.6 Escribir property test para listado de partidos
  - **Property 6: All registered parties are listed**
  - **Validates: Requirements 3.1**

## Fase 4: Backend - Servicios de Candidatos

- [ ] 4. Implementar servicios para gestión de candidatos
- [ ] 4.1 Crear CandidatoService con operaciones CRUD
  - Implementar listar_candidatos() con filtros
  - Implementar obtener_candidato(id)
  - Implementar crear_candidato(data) con validaciones
  - Implementar actualizar_candidato(id, data)
  - Implementar eliminar_candidato(id) con verificación de votos
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 4.2 Implementar validación de asociación con partido
  - Verificar que partido_id existe en base de datos
  - Verificar que partido está activo
  - Retornar error descriptivo si no existe
  - _Requirements: 4.5_

- [ ] 4.3 Implementar validación de foto de candidato
  - Validar formato de archivo (jpg, jpeg, png, webp)
  - Validar tamaño de archivo (max 5MB)
  - Generar nombre único para archivo
  - Guardar archivo en directorio seguro
  - _Requirements: 4.2_

- [ ] 4.4 Escribir property test para eliminación de candidatos
  - **Property 12: Candidate deletion requires no registered votes**
  - **Validates: Requirements 4.4**

- [ ] 4.5 Escribir property test para validación de partido
  - **Property 13: Candidate party association validation**
  - **Validates: Requirements 4.5**

## Fase 5: Backend - Rutas de Candidatos

- [ ] 5. Crear endpoints REST para candidatos
- [ ] 5.1 Implementar GET /api/candidatos
  - Listar todos los candidatos con paginación
  - Agregar filtros por partido, tipo_eleccion, activo
  - Incluir datos de partido y tipo_eleccion
  - Validar permisos de Super Admin
  - _Requirements: 4.1_

- [ ] 5.2 Implementar POST /api/candidatos
  - Recibir datos del candidato
  - Validar campos obligatorios
  - Validar que partido existe
  - Crear candidato en base de datos
  - Retornar candidato creado con relaciones
  - _Requirements: 4.2, 4.5_

- [ ] 5.3 Implementar PUT /api/candidatos/<id>
  - Recibir datos actualizados
  - Validar que candidato existe
  - Validar que partido existe si se actualiza
  - Actualizar candidato en base de datos
  - Retornar candidato actualizado
  - _Requirements: 4.3, 4.5_

- [ ] 5.4 Implementar DELETE /api/candidatos/<id>
  - Validar que candidato existe
  - Verificar que no tiene votos registrados
  - Eliminar candidato de base de datos
  - Retornar confirmación
  - _Requirements: 4.4_

- [ ] 5.5 Implementar POST /api/candidatos/<id>/foto
  - Recibir archivo multipart/form-data
  - Validar formato y tamaño
  - Guardar archivo
  - Actualizar foto_url del candidato
  - Retornar URL de la foto
  - _Requirements: 4.2_

- [ ] 5.6 Escribir property test para listado de candidatos
  - **Property 10: All registered candidates are listed**
  - **Validates: Requirements 4.1**

## Fase 6: Backend - Servicios de Configuración

- [ ] 6. Implementar servicios para configuración del sistema
- [ ] 6.1 Crear ConfiguracionService
  - Implementar obtener_configuracion(clave)
  - Implementar actualizar_configuracion(clave, valor)
  - Implementar obtener_todas_configuraciones()
  - Implementar cache con Redis (TTL 5 minutos)
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 6.2 Implementar exportación de configuración
  - Exportar partidos a JSON
  - Exportar candidatos a JSON
  - Exportar tipos de elección a JSON
  - Exportar configuración completa a JSON
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 6.3 Implementar importación de configuración
  - Validar formato JSON
  - Validar estructura de datos
  - Aplicar cambios en transacción
  - Retornar resumen de cambios
  - _Requirements: 10.5_

- [ ] 6.4 Escribir property test para cambios de configuración
  - **Property 30: Configuration changes apply immediately**
  - **Validates: Requirements 8.5**

- [ ] 6.5 Escribir property test para exportación
  - **Property 36: Party export includes all parties**
  - **Property 37: Candidate export includes all candidates**
  - **Property 39: Complete configuration export includes all settings**
  - **Validates: Requirements 10.1, 10.2, 10.4**

- [ ] 6.6 Escribir property test para importación
  - **Property 40: Configuration import validates format**
  - **Validates: Requirements 10.5**

## Fase 7: Backend - Rutas de Configuración

- [ ] 7. Crear endpoints REST para configuración
- [ ] 7.1 Implementar GET /api/configuracion
  - Listar todas las configuraciones
  - Validar permisos de Super Admin
  - Retornar configuraciones agrupadas por categoría
  - _Requirements: 8.1_

- [ ] 7.2 Implementar PUT /api/configuracion/<clave>
  - Recibir nuevo valor
  - Validar tipo de dato
  - Actualizar configuración
  - Invalidar cache
  - Retornar confirmación
  - _Requirements: 8.2, 8.3, 8.4, 8.5_

- [ ] 7.3 Implementar POST /api/configuracion/exportar
  - Recibir tipo de exportación (partidos, candidatos, tipos, completa)
  - Generar archivo JSON
  - Retornar archivo para descarga
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 7.4 Implementar POST /api/configuracion/importar
  - Recibir archivo JSON
  - Validar formato y estructura
  - Aplicar cambios
  - Retornar resumen de cambios aplicados
  - _Requirements: 10.5_

- [ ] 7.5 Escribir property test para propagación de cambios
  - **Property 27: System name changes propagate to all pages**
  - **Property 28: System logo changes propagate to navbar**
  - **Property 29: Timezone configuration applies to all dates**
  - **Validates: Requirements 8.2, 8.3, 8.4**

## Fase 8: Backend - Mejoras en Mapas

- [ ] 8. Mejorar endpoint de puestos geolocalizados
- [ ] 8.1 Actualizar endpoint GET /api/puestos-geolocalizados
  - Remover filtros por rol (mostrar todos los puestos)
  - Incluir contadores de incidentes por severidad
  - Incluir contadores de delitos por gravedad
  - Incluir contadores de formularios pendientes
  - Agregar campo de indicador visual
  - _Requirements: 1.1, 1.2, 1.4, 6.1, 6.2, 6.3, 6.4_

- [ ] 8.2 Implementar lógica de indicadores visuales
  - Indicador rojo pulsante si hay incidentes críticos
  - Indicador naranja si hay delitos reportados
  - Indicador amarillo si hay formularios pendientes
  - Indicador verde si está completamente reportado
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 8.3 Implementar filtros de mapa
  - Filtro por incidentes (solo puestos con incidentes)
  - Filtro por delitos (solo puestos con delitos)
  - Filtro por pendientes (solo puestos con formularios pendientes)
  - Lógica AND para múltiples filtros
  - _Requirements: 7.1, 7.2, 7.3, 7.5_

- [ ] 8.4 Implementar búsqueda de puestos
  - Búsqueda por código de puesto
  - Búsqueda por nombre de municipio
  - Búsqueda por código de mesa
  - Retornar coordenadas para centrar mapa
  - _Requirements: 9.1, 9.2, 9.3_

- [ ] 8.5 Manejar puestos sin coordenadas GPS
  - Registrar en logs puestos sin GPS
  - No incluir en respuesta de mapa
  - No retornar error al usuario
  - _Requirements: 1.5_

- [ ] 8.6 Escribir property test para visualización de puestos
  - **Property 1: All geolocalized voting locations are displayed**
  - **Property 2: Valid coordinates generate markers**
  - **Validates: Requirements 1.1, 1.2**

- [ ] 8.7 Escribir property test para indicadores visuales
  - **Property 18: Critical incidents show red pulsing indicator**
  - **Property 19: Reported crimes show orange indicator**
  - **Property 20: Pending forms show yellow indicator**
  - **Property 21: Fully reported locations show green indicator**
  - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**

- [ ] 8.8 Escribir property test para filtros
  - **Property 23: Incidents filter shows only locations with incidents**
  - **Property 24: Crimes filter shows only locations with crimes**
  - **Property 25: Pending filter shows only locations with pending forms**
  - **Property 26: Multiple filters use AND logic**
  - **Validates: Requirements 7.1, 7.2, 7.3, 7.5**

- [ ] 8.9 Escribir property test para búsqueda
  - **Property 31: Voting location code search centers map**
  - **Property 32: Municipality search returns all locations**
  - **Property 33: Table code search returns containing location**
  - **Validates: Requirements 9.1, 9.2, 9.3**

## Fase 9: Frontend - Componentes de Partidos

- [ ] 9. Crear interfaz de gestión de partidos políticos
- [ ] 9.1 Crear partidos-manager.js
  - Implementar función cargarPartidos() con paginación
  - Implementar función mostrarFormularioPartido(partido)
  - Implementar función guardarPartido(data)
  - Implementar función eliminarPartido(id)
  - Agregar búsqueda y filtros
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 9.2 Crear modal de partido
  - Formulario con campos: nombre, sigla, color, logo
  - Validación de campos obligatorios
  - Preview de color seleccionado
  - Upload de logo con preview
  - Botones guardar y cancelar
  - _Requirements: 3.2, 3.5_

- [ ] 9.3 Implementar upload de logo
  - Input file con validación de tipo
  - Preview de imagen antes de subir
  - Progress bar durante upload
  - Manejo de errores de upload
  - _Requirements: 3.5_

- [ ] 9.4 Crear tabla de partidos
  - Columnas: logo, nombre, sigla, color, candidatos, acciones
  - Botones editar y eliminar por fila
  - Confirmación antes de eliminar
  - Indicador de partido activo/inactivo
  - _Requirements: 3.1, 3.3, 3.4_

## Fase 10: Frontend - Componentes de Candidatos

- [ ] 10. Crear interfaz de gestión de candidatos
- [ ] 10.1 Crear candidatos-manager.js
  - Implementar función cargarCandidatos() con paginación
  - Implementar función mostrarFormularioCandidato(candidato)
  - Implementar función guardarCandidato(data)
  - Implementar función eliminarCandidato(id)
  - Agregar búsqueda y filtros por partido y tipo
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 10.2 Crear modal de candidato
  - Formulario con campos: nombre, partido, tipo_eleccion, cargo, numero_lista, foto
  - Selector de partido con búsqueda
  - Selector de tipo de elección
  - Validación de campos obligatorios
  - Upload de foto con preview
  - _Requirements: 4.2, 4.5_

- [ ] 10.3 Implementar upload de foto
  - Input file con validación de tipo
  - Preview de imagen antes de subir
  - Progress bar durante upload
  - Manejo de errores de upload
  - _Requirements: 4.2_

- [ ] 10.4 Crear tabla de candidatos
  - Columnas: foto, nombre, partido, tipo_eleccion, cargo, acciones
  - Filtros por partido y tipo de elección
  - Botones editar y eliminar por fila
  - Confirmación antes de eliminar
  - _Requirements: 4.1, 4.3, 4.4_

## Fase 11: Frontend - Sistema de Tabs de Configuración

- [ ] 11. Reorganizar dashboard de Super Admin con tabs
- [ ] 11.1 Crear configuracion-tabs.js
  - Implementar sistema de tabs para configuración
  - Sub-tabs: Partidos, Candidatos, Tipos de Elección, Sistema
  - Navegación entre tabs sin recargar página
  - Persistir tab activo en localStorage
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 11.2 Actualizar template super_admin.html
  - Agregar estructura de tabs de configuración
  - Integrar partidos-manager en tab de Partidos
  - Integrar candidatos-manager en tab de Candidatos
  - Agregar placeholders para otros tabs
  - _Requirements: 2.1, 2.2, 2.3_

- [ ] 11.3 Crear estilos para tabs
  - Estilos para tabs activos e inactivos
  - Transiciones suaves entre tabs
  - Responsive design para móviles
  - _Requirements: 2.1_

## Fase 12: Frontend - Mejoras en Mapas

- [ ] 12. Mejorar visualización de mapas
- [ ] 12.1 Actualizar mapa-visualizacion.js
  - Cargar todos los puestos sin filtros de rol
  - Implementar indicadores visuales según estado
  - Agregar animación pulsante para críticos
  - Mejorar popups con información detallada
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 6.1, 6.2, 6.3, 6.4_

- [ ] 12.2 Implementar filtros de mapa
  - Checkbox "Solo con incidentes"
  - Checkbox "Solo con delitos"
  - Checkbox "Pendientes de reporte"
  - Aplicar filtros sin recargar página
  - Actualizar contador de puestos visibles
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 12.3 Implementar búsqueda de puestos
  - Input de búsqueda con autocompletado
  - Búsqueda por código, municipio o mesa
  - Centrar mapa en resultado
  - Resaltar marcador encontrado
  - Mostrar mensaje si no se encuentra
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 12.4 Mejorar popups de puestos
  - Mostrar sección de alertas si hay incidentes/delitos
  - Mostrar badges con colores según severidad
  - Agregar links a detalles de incidentes/delitos
  - Mostrar progreso de formularios
  - _Requirements: 1.3, 6.5_

- [ ] 12.5 Implementar clustering de marcadores
  - Agrupar marcadores cercanos
  - Mostrar número de puestos en cluster
  - Expandir cluster al hacer zoom
  - _Requirements: 1.1, 1.2_

## Fase 13: Frontend - Configuración del Sistema

- [ ] 13. Crear interfaz de configuración general
- [ ] 13.1 Crear sistema-config.js
  - Implementar función cargarConfiguracion()
  - Implementar función guardarConfiguracion(clave, valor)
  - Implementar función exportarConfiguracion(tipo)
  - Implementar función importarConfiguracion(archivo)
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 13.2 Crear formulario de configuración
  - Campo para nombre del sistema
  - Upload de logo del sistema
  - Selector de zona horaria
  - Otros parámetros configurables
  - Botón guardar con confirmación
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 13.3 Implementar exportación/importación
  - Botones para exportar partidos, candidatos, tipos
  - Botón para exportar configuración completa
  - Input file para importar configuración
  - Validación de archivo antes de importar
  - Mostrar resumen de cambios a aplicar
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

## Fase 14: Testing y Validación

- [ ] 14. Checkpoint - Asegurar calidad del código
- [ ] 14.1 Ejecutar todos los property-based tests
  - Verificar que todas las propiedades se cumplen
  - Corregir bugs encontrados por property testing
  - Aumentar iteraciones a 100 si es necesario

- [ ] 14.2 Ejecutar pruebas de integración
  - Crear partido → Crear candidato → Verificar asociación
  - Upload logo → Verificar URL → Acceder archivo
  - Aplicar filtros → Verificar resultados correctos
  - Exportar → Importar → Verificar integridad

- [ ] 14.3 Pruebas de UI/UX
  - Verificar navegación entre tabs
  - Verificar validación de formularios
  - Verificar uploads de archivos
  - Verificar mapas cargan correctamente
  - Verificar filtros funcionan sin recargar

- [ ] 14.4 Pruebas de permisos
  - Verificar solo Super Admin accede a configuración
  - Verificar todos los roles ven mapas completos
  - Verificar validación de permisos en backend

- [ ] 14.5 Optimización de rendimiento
  - Verificar queries de base de datos
  - Implementar índices faltantes
  - Verificar caching funciona correctamente
  - Optimizar carga de mapas con muchos puestos

## Fase 15: Documentación y Deployment

- [ ] 15. Preparar para producción
- [ ] 15.1 Actualizar documentación técnica
  - Documentar nuevos endpoints de API
  - Documentar nuevos modelos de datos
  - Actualizar diagramas de arquitectura
  - Documentar configuración de variables de entorno

- [ ] 15.2 Crear guía de usuario
  - Cómo gestionar partidos políticos
  - Cómo gestionar candidatos
  - Cómo usar filtros y búsqueda en mapas
  - Cómo exportar/importar configuración

- [ ] 15.3 Ejecutar migraciones de base de datos
  - Crear backup de base de datos
  - Ejecutar migraciones en staging
  - Verificar integridad de datos
  - Ejecutar migraciones en producción

- [ ] 15.4 Configurar variables de entorno
  - UPLOAD_FOLDER para logos y fotos
  - MAX_UPLOAD_SIZE para límite de archivos
  - ALLOWED_EXTENSIONS para tipos permitidos
  - Configurar Redis para caching

- [ ] 15.5 Desplegar a producción
  - Desplegar backend con nuevos endpoints
  - Desplegar frontend con nuevas interfaces
  - Verificar que todo funciona correctamente
  - Monitorear logs y métricas
