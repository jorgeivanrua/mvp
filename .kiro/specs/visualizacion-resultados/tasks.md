# Implementation Plan: Visualización de Resultados Electorales

## Fase 1: Backend - Servicio de Agregación

- [ ] 1. Implementar servicio de agregación de votos
- [ ] 1.1 Crear AgregacionService
  - Implementar agregar_votos_puesto(puesto_id, tipo_eleccion_id)
  - Implementar agregar_votos_municipio(municipio_codigo, tipo_eleccion_id)
  - Implementar agregar_votos_departamento(departamento_codigo, tipo_eleccion_id)
  - Implementar agregar_votos_nacional(tipo_eleccion_id)
  - Agregar caché con Redis (TTL 5 minutos)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ]* 1.2 Escribir property test para agregación precisa
  - **Property 41: Vote aggregation is accurate**
  - **Validates: Requirements 1.5**

- [ ]* 1.3 Escribir property test para consistencia jerárquica
  - **Property 42: Hierarchical aggregation is consistent**
  - **Validates: Requirements 1.1, 1.2, 1.3, 1.4**

## Fase 2: Backend - Servicio de Estadísticas

- [ ] 2. Implementar servicio de estadísticas
- [ ] 2.1 Crear EstadisticasService
  - Implementar calcular_estadisticas_generales(resultados)
  - Implementar calcular_porcentajes_partido(votos_partidos)
  - Implementar calcular_porcentajes_candidato(votos_candidatos)
  - Implementar calcular_progreso_reporte(nivel, ubicacion)
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ]* 2.2 Escribir property test para cálculo de porcentajes
  - **Property 43: Percentage calculations are correct**
  - **Validates: Requirements 3.2, 4.4**

## Fase 3: Backend - Servicio de Resultados

- [ ] 3. Implementar servicio principal de resultados
- [ ] 3.1 Crear ResultadosService
  - Implementar obtener_resultados_por_nivel(user, tipo_eleccion_id, filtros)
  - Implementar obtener_resultados_por_partido(user, tipo_eleccion_id)
  - Implementar obtener_resultados_por_candidato(user, tipo_eleccion_id)
  - Implementar obtener_desglose_geografico(user, tipo_eleccion_id)
  - Agregar validación de permisos por nivel de usuario
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 3.1, 4.1, 5.1, 5.2, 5.3_

- [ ] 3.2 Implementar filtrado por jurisdicción
  - Filtrar por puesto para Coordinador de Puesto
  - Filtrar por municipio para Coordinador Municipal
  - Filtrar por departamento para Coordinador Departamental
  - Sin filtros para Super Admin
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

## Fase 4: Backend - Rutas de Resultados

- [ ] 4. Crear endpoints REST para resultados
- [ ] 4.1 Implementar GET /api/resultados/general
  - Obtener resultados generales según nivel de usuario
  - Incluir estadísticas agregadas
  - Validar permisos de usuario
  - Aplicar filtros opcionales
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 4.2 Implementar GET /api/resultados/partidos
  - Obtener votos agregados por partido
  - Calcular porcentajes
  - Ordenar por cantidad de votos
  - Incluir información de partido (color, logo)
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 4.3 Implementar GET /api/resultados/candidatos
  - Obtener votos agregados por candidato
  - Incluir información de partido asociado
  - Incluir foto de candidato
  - Calcular porcentajes
  - Ordenar por cantidad de votos
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 4.4 Implementar GET /api/resultados/desglose
  - Obtener desglose geográfico según nivel
  - Incluir coordenadas GPS para mapa
  - Incluir progreso de reporte por ubicación
  - Incluir resultados por partido por ubicación
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 4.5 Implementar GET /api/resultados/estadisticas
  - Obtener estadísticas agregadas
  - Incluir total de votos válidos, nulos, blancos
  - Incluir porcentaje de participación
  - Incluir progreso de reporte
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ]* 4.6 Escribir property test para filtro de tipo de elección
  - **Property 44: Election type filter shows only matching results**
  - **Validates: Requirements 2.2**

## Fase 5: Backend - Servicio de Exportación

- [ ] 5. Implementar servicio de exportación
- [ ] 5.1 Crear ExportacionService
  - Implementar exportar_excel(resultados, filtros)
  - Implementar exportar_pdf(resultados, filtros)
  - Implementar exportar_csv(resultados, filtros)
  - Agregar timestamp y filtros en nombre de archivo
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 5.2 Implementar POST /api/resultados/exportar
  - Recibir formato de exportación (excel, pdf, csv)
  - Recibir filtros aplicados
  - Generar archivo
  - Retornar archivo para descarga
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

## Fase 6: Backend - Optimización de Base de Datos

- [ ] 6. Optimizar consultas de agregación
- [ ] 6.1 Crear índices de base de datos
  - Índice compuesto en (tipo_eleccion_id, puesto_id)
  - Índice compuesto en (tipo_eleccion_id, municipio_codigo)
  - Índice compuesto en (tipo_eleccion_id, departamento_codigo)
  - Índice en validado para filtrar formularios validados
  - _Requirements: Performance_

- [ ] 6.2 Crear vistas materializadas
  - Vista para agregación por puesto
  - Vista para agregación por municipio
  - Vista para agregación por departamento
  - Configurar refresh automático cada 5 minutos
  - _Requirements: Performance_

## Fase 7: Frontend - Componente de Visualización

- [ ] 7. Crear componente de visualización de resultados
- [ ] 7.1 Crear ResultadosVisualizacion.js
  - Implementar constructor con opciones
  - Implementar init() para inicialización
  - Implementar cargarResultados(tipoEleccionId)
  - Implementar cargarResultadosPartidos()
  - Implementar cargarResultadosCandidatos()
  - Implementar cargarDesgloseGeografico()
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 7.2 Implementar renderizado de estadísticas
  - Renderizar total de votos válidos
  - Renderizar total de votos nulos y blancos
  - Renderizar porcentaje de participación
  - Renderizar progreso de reporte con barra de progreso
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

## Fase 8: Frontend - Gráficos de Resultados

- [ ] 8. Implementar visualización gráfica
- [ ] 8.1 Implementar gráfico de resultados por partido
  - Usar Chart.js para gráfico de barras
  - Usar colores distintivos por partido
  - Mostrar porcentajes en barras
  - Agregar tooltip con información detallada
  - Hacer responsive
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 8.2 Implementar gráfico de pastel opcional
  - Gráfico de pastel para distribución de votos
  - Usar colores de partidos
  - Mostrar leyenda
  - Agregar interactividad
  - _Requirements: 3.3, 3.4_

- [ ] 8.3 Implementar tabla de resultados por candidato
  - Mostrar foto de candidato
  - Mostrar nombre y partido
  - Mostrar total de votos y porcentaje
  - Ordenar por cantidad de votos
  - Agregar paginación si hay muchos candidatos
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

## Fase 9: Frontend - Desglose Geográfico

- [ ] 9. Implementar desglose geográfico
- [ ] 9.1 Integrar mapa con resultados
  - Reutilizar MapaGeolocalizacion
  - Agregar markers con resultados por ubicación
  - Usar colores según partido ganador
  - Mostrar popup con resultados detallados
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 9.2 Implementar tabla de desglose
  - Mostrar lista de ubicaciones
  - Mostrar progreso de reporte por ubicación
  - Mostrar partido ganador por ubicación
  - Agregar búsqueda de ubicaciones
  - Agregar ordenamiento por columnas
  - _Requirements: 5.1, 5.2, 5.3_

## Fase 10: Frontend - Filtros y Búsqueda

- [ ] 10. Implementar filtros y búsqueda
- [ ] 10.1 Crear selector de tipo de elección
  - Dropdown con tipos de elección disponibles
  - Cargar resultados al cambiar tipo
  - Mantener tipo seleccionado en localStorage
  - _Requirements: 2.1, 2.2, 2.3_

- [ ] 10.2 Implementar filtros de progreso
  - Checkbox "Completados" (100% reportado)
  - Checkbox "En Progreso" (parcialmente reportado)
  - Checkbox "Pendientes" (sin reportes)
  - Aplicar lógica AND para múltiples filtros
  - Botón para limpiar filtros
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 10.3 Implementar búsqueda de ubicaciones
  - Input de búsqueda
  - Búsqueda por código de puesto
  - Búsqueda por nombre de municipio
  - Búsqueda por código de mesa
  - Resaltar resultado en mapa y tabla
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 10.4 Escribir property test para filtros de progreso
  - **Property 45: Progress filters use AND logic**
  - **Validates: Requirements 6.4**

- [ ]* 10.5 Escribir property test para búsqueda
  - **Property 46: Search returns matching locations**
  - **Validates: Requirements 7.1, 7.2, 7.3**

## Fase 11: Frontend - Actualización en Tiempo Real

- [ ] 11. Implementar actualización automática
- [ ] 11.1 Configurar WebSocket para actualizaciones
  - Conectar a canal de resultados
  - Escuchar eventos de nuevos formularios validados
  - Actualizar resultados automáticamente
  - Mantener filtros y vista actual
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [ ] 11.2 Implementar notificaciones de actualización
  - Mostrar toast cuando hay nuevos datos
  - Indicar número de nuevos formularios
  - Agregar botón para actualizar manualmente
  - _Requirements: 11.3_

- [ ] 11.3 Implementar indicador de conexión
  - Mostrar estado de conexión (conectado/desconectado)
  - Intentar reconexión automática
  - Mostrar mensaje cuando hay error de conexión
  - _Requirements: 11.5_

- [ ]* 11.4 Escribir property test para actualizaciones
  - **Property 47: New forms trigger result updates**
  - **Validates: Requirements 11.1**

- [ ]* 11.5 Escribir property test para preservación de contexto
  - **Property 48: Updates preserve user context**
  - **Validates: Requirements 11.4**

## Fase 12: Frontend - Exportación

- [ ] 12. Implementar funcionalidad de exportación
- [ ] 12.1 Crear botones de exportación
  - Botón "Exportar a Excel"
  - Botón "Exportar a PDF"
  - Botón "Exportar a CSV"
  - Mostrar progress bar durante exportación
  - _Requirements: 10.1, 10.2, 10.3_

- [ ] 12.2 Implementar descarga de archivos
  - Llamar a endpoint de exportación
  - Descargar archivo generado
  - Mostrar mensaje de éxito/error
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

## Fase 13: Frontend - Interfaz Responsiva

- [ ] 13. Optimizar para diferentes dispositivos
- [ ] 13.1 Adaptar layout para móvil
  - Reorganizar paneles en columna única
  - Hacer gráficos responsivos
  - Optimizar tabla para pantalla pequeña
  - Agregar menú hamburguesa para filtros
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 13.2 Optimizar para tablet
  - Layout de dos columnas
  - Gráficos de tamaño medio
  - Tabla con scroll horizontal si necesario
  - _Requirements: 12.2_

- [ ] 13.3 Agregar soporte táctil
  - Gestos de swipe para cambiar entre vistas
  - Tap para seleccionar elementos
  - Pinch to zoom en gráficos
  - _Requirements: 12.5_

## Fase 14: Integración en Dashboards

- [ ] 14. Integrar en dashboards de coordinadores
- [ ] 14.1 Agregar pestaña de resultados en dashboard de Coordinador de Puesto
  - Crear template coordinador/resultados-puesto.html
  - Integrar ResultadosVisualizacion.js
  - Configurar para nivel de puesto
  - _Requirements: 1.1_

- [ ] 14.2 Agregar pestaña de resultados en dashboard de Coordinador Municipal
  - Crear template coordinador/resultados-municipal.html
  - Integrar ResultadosVisualizacion.js
  - Configurar para nivel municipal
  - _Requirements: 1.2_

- [ ] 14.3 Agregar pestaña de resultados en dashboard de Coordinador Departamental
  - Crear template coordinador/resultados-departamental.html
  - Integrar ResultadosVisualizacion.js
  - Configurar para nivel departamental
  - _Requirements: 1.3_

- [ ] 14.4 Agregar pestaña de resultados en dashboard de Super Admin
  - Crear template admin/resultados-nacional.html
  - Integrar ResultadosVisualizacion.js
  - Configurar para nivel nacional
  - _Requirements: 1.4_

## Fase 15: Testing y Validación

- [ ] 15. Checkpoint - Asegurar calidad del código
- [ ] 15.1 Ejecutar todos los property-based tests
  - Verificar Properties 41-48
  - Corregir bugs encontrados
  - Aumentar iteraciones a 100

- [ ] 15.2 Ejecutar pruebas de integración
  - Validar formulario E-14 → Ver resultados actualizados
  - Aplicar filtros → Verificar resultados correctos
  - Cambiar tipo de elección → Verificar resultados correctos
  - Exportar → Verificar contenido de archivo

- [ ] 15.3 Pruebas de rendimiento
  - Probar con 1000+ formularios E-14
  - Verificar tiempo de agregación < 2 segundos
  - Verificar tiempo de renderizado < 1 segundo
  - Optimizar queries lentas

- [ ] 15.4 Pruebas de UI/UX
  - Verificar responsive en móvil, tablet, desktop
  - Verificar gráficos se renderizan correctamente
  - Verificar actualización en tiempo real funciona
  - Verificar exportación genera archivos correctos

## Fase 16: Documentación

- [ ] 16. Documentar funcionalidad
- [ ] 16.1 Crear guía de usuario
  - Cómo ver resultados por nivel
  - Cómo usar filtros y búsqueda
  - Cómo interpretar gráficos
  - Cómo exportar resultados

- [ ] 16.2 Documentar API
  - Documentar endpoints de resultados
  - Documentar formatos de respuesta
  - Documentar parámetros de filtros
  - Agregar ejemplos de uso

- [ ] 16.3 Documentar arquitectura
  - Diagrama de flujo de agregación
  - Diagrama de componentes frontend
  - Estrategia de caching
  - Consideraciones de rendimiento

