# Implementation Plan - Dashboard Coordinador Departamental

## Overview

Este plan implementa el Dashboard del Coordinador Departamental reutilizando al máximo el código del Dashboard Municipal. La estrategia es copiar y adaptar componentes existentes, cambiando la jerarquía de municipio→puestos a departamento→municipios.

## Tasks

- [x] 1. Crear modelo ReporteDepartamental y migración



  - Crear modelo `ReporteDepartamental` basado en `FormularioE24Municipal`
  - Crear modelo `VotoPartidoReporteDepartamental` para votos por partido
  - Crear migración de base de datos con tablas e índices
  - Ejecutar migración y verificar tablas
  - _Requirements: 7.1, 7.5_

- [ ] 2. Implementar DepartamentalService
  - Copiar `municipal_service.py` como base para `departamental_service.py`
  - Adaptar `obtener_municipios_departamento()` (similar a obtener_puestos_municipio)
  - Implementar `calcular_consolidado_departamental()` sumando consolidados municipales
  - Adaptar `comparar_municipios()` (similar a comparar_puestos)
  - Implementar `obtener_municipio_detallado()` para drill-down
  - _Requirements: 1.1, 2.1, 3.1, 5.1, 9.1_

- [ ] 3. Adaptar DiscrepanciaService para nivel departamental
  - Agregar método `detectar_discrepancias_departamento()` en DiscrepanciaService existente
  - Reutilizar lógica de detección pero aplicada a municipios en lugar de puestos
  - Detectar municipios con participación anormal, coordinadores inactivos, alta tasa rechazo
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 4. Implementar ReporteDepartamentalService
  - Crear `reporte_departamental_service.py` basado en `e24_service.py`
  - Implementar `validar_requisitos_reporte()` (mínimo 90% municipios completos)
  - Implementar `generar_reporte_departamental()` para crear reporte oficial
  - Implementar `generar_pdf_reporte()` para PDF del reporte
  - Registrar generación en base de datos con hash SHA-256
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 5. Crear endpoints API para coordinador departamental
  - Copiar `coordinador_municipal.py` como base para `coordinador_departamental.py`
  - Adaptar endpoint GET `/api/coordinador-departamental/municipios` (lista de municipios)
  - Adaptar endpoint GET `/api/coordinador-departamental/consolidado` (consolidado departamental)
  - Adaptar endpoint GET `/api/coordinador-departamental/municipio/<id>` (detalles de municipio)
  - Adaptar endpoint GET `/api/coordinador-departamental/discrepancias` (anomalías departamentales)
  - Validar que coordinador solo acceda a su departamento asignado
  - _Requirements: 1.1, 2.1, 3.1, 6.1, 14.1, 14.2_

- [ ] 6. Implementar endpoints de acciones avanzadas
  - Adaptar endpoint POST `/api/coordinador-departamental/reporte-departamental` (generar reporte)
  - Adaptar endpoint GET `/api/coordinador-departamental/comparacion` (comparar municipios)
  - Adaptar endpoint GET `/api/coordinador-departamental/estadisticas` (métricas departamentales)
  - Adaptar endpoint POST `/api/coordinador-departamental/notificar` (notificar coordinadores municipales)
  - Adaptar endpoint GET `/api/coordinador-departamental/exportar` (exportar datos CSV/XLSX)
  - _Requirements: 7.1, 8.4, 9.1, 11.1, 11.2_

- [ ] 7. Registrar blueprint y configurar rutas
  - Registrar coordinador_departamental_bp en `backend/routes/__init__.py`
  - Registrar blueprint en `backend/app.py`
  - Verificar que las rutas estén accesibles con autenticación
  - _Requirements: 14.1_

- [ ] 8. Crear template HTML del dashboard
  - Copiar `municipal.html` como base para `departamental.html`
  - Reemplazar "Puestos" → "Municipios" en toda la interfaz
  - Reemplazar "Coordinador de Puesto" → "Coordinador Municipal"
  - Reemplazar "E-24 Municipal" → "Reporte Departamental"
  - Mantener estructura de 3 columnas (estadísticas, lista, detalles)
  - _Requirements: 1.1, 2.1, 3.1, 13.1_

- [ ] 9. Crear JavaScript del dashboard
  - Copiar `coordinador-municipal.js` como base para `coordinador-departamental.js`
  - Adaptar URLs de API de `/coordinador-municipal/` a `/coordinador-departamental/`
  - Adaptar terminología en variables y funciones (puestos → municipios)
  - Mantener funcionalidad de auto-refresh cada 60 segundos
  - _Requirements: 1.1, 1.5, 2.1, 2.5, 12.1, 12.5_

- [ ] 10. Implementar funcionalidades de interacción
  - Adaptar `seleccionarMunicipio()` para cargar detalles de municipio
  - Adaptar `filtrarMunicipios()` para filtrar por estado
  - Adaptar `buscarMunicipio()` para búsqueda por código o nombre
  - Implementar navegación con breadcrumb (Departamento > Municipio > Puesto)
  - _Requirements: 3.1, 3.3, 3.4, 3.5_

- [ ] 11. Implementar generación de Reporte Departamental
  - Adaptar `generarReporteDepartamental()` en frontend
  - Validar requisitos mínimos (90% municipios completos)
  - Mostrar modal de confirmación con validaciones
  - Descargar PDF automáticamente al completar
  - Registrar generación en historial
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

- [ ] 12. Implementar comparación de municipios
  - Adaptar `abrirComparacion()` para seleccionar municipios
  - Permitir seleccionar 2-5 municipios para comparación
  - Renderizar gráficos comparativos con Chart.js
  - Mostrar tabla comparativa con estadísticas
  - Calcular y mostrar desviación estándar
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 13. Implementar exportación de datos
  - Adaptar `exportarDatos()` para consolidado departamental
  - Soportar formatos CSV y XLSX
  - Incluir metadatos (fecha, coordinador, timestamp)
  - Registrar exportación en audit log
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 14. Implementar sistema de notificaciones
  - Adaptar `enviarNotificacion()` para coordinadores municipales
  - Permitir seleccionar destinatarios específicos o todos
  - Soportar niveles de prioridad
  - Mostrar confirmación de envío
  - _Requirements: 8.4, 15.1_

- [ ] 15. Implementar visualización de estadísticas
  - Renderizar panel de estadísticas departamentales
  - Mostrar gráfico de consolidado departamental
  - Implementar métricas en tiempo real (actualización cada 30 segundos)
  - Mostrar gráfico de progreso temporal
  - _Requirements: 2.1, 2.3, 9.1, 9.5, 12.1, 12.5_

- [ ] 16. Implementar ranking de municipios
  - Crear función `renderRankingMunicipios()` para mostrar rankings
  - Permitir ordenar por: avance, participación, tiempo validación, tasa rechazo
  - Resaltar municipios de mejor y peor desempeño
  - Actualizar ranking automáticamente
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 17. Implementar mapa geográfico (placeholder)
  - Crear contenedor para mapa del departamento
  - Mostrar mensaje "Funcionalidad de mapa en desarrollo"
  - Preparar estructura para futura integración con librería de mapas
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 18. Implementar responsive design
  - Adaptar layout de 3 columnas para móviles
  - Optimizar tabla de municipios para pantallas pequeñas
  - Ajustar gráficos para visualización móvil
  - Verificar funcionalidades en dispositivos móviles
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ] 19. Implementar seguridad y auditoría
  - Reutilizar sistema de audit logs del dashboard municipal
  - Registrar todas las acciones del coordinador departamental
  - Validar permisos en cada endpoint (solo su departamento)
  - Implementar cierre de sesión automático (30 minutos)
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ] 20. Crear ruta de navegación en app principal
  - Actualizar ruta `/coordinador/departamental` en `backend/routes/frontend.py`
  - Verificar que solo usuarios con rol `coordinador_departamental` puedan acceder
  - Agregar enlace en menú de navegación
  - _Requirements: 14.1_

