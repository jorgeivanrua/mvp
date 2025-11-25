# Requirements Document - Sistema de Monitoreo en Tiempo Real

## Introduction

El Sistema de Monitoreo en Tiempo Real permite a usuarios con rol de monitoreo supervisar la actividad global del sistema electoral sin restricciones de jurisdicción. El sistema proporciona un dashboard centralizado con vista de todos los usuarios geolocalizados, todos los formularios E-14, todos los incidentes y delitos reportados, y estadísticas globales en tiempo real. A diferencia de los coordinadores que solo ven su jurisdicción, el rol de monitoreo tiene visibilidad completa del sistema para supervisión y análisis.

## Glossary

- **Sistema**: Sistema Electoral de Recolección de Datos
- **Monitoreo**: Rol especial con visibilidad global del sistema sin restricciones de jurisdicción
- **Dashboard de Monitoreo**: Interfaz centralizada para supervisión en tiempo real
- **Visibilidad Global**: Capacidad de ver todos los datos del sistema sin filtros de jurisdicción
- **Tiempo Real**: Datos actualizados automáticamente sin necesidad de recargar la página
- **Geolocalización Global**: Vista de todos los usuarios con GPS activo en un mapa
- **Estadísticas Globales**: Métricas agregadas de todo el sistema electoral
- **Alertas**: Notificaciones automáticas sobre eventos críticos
- **Exportación**: Capacidad de descargar datos en formatos externos

## Requirements

### Requirement 1: Rol de Monitoreo

**User Story:** As a system administrator, I want a dedicated monitoring role, so that authorized personnel can supervise the entire electoral system without jurisdiction restrictions.

#### Acceptance Criteria

1. WHEN creating a user with rol 'monitoreo' THEN the System SHALL not require ubicacion_id (no jurisdiction restriction)
2. WHEN a monitoreo user logs in THEN the System SHALL grant access to the monitoring dashboard
3. WHEN a monitoreo user accesses data THEN the System SHALL not apply jurisdiction filters
4. WHEN a monitoreo user views reports THEN the System SHALL show all reports from all locations
5. WHEN a monitoreo user views users THEN the System SHALL show all users regardless of location

### Requirement 2: Dashboard de Monitoreo en Tiempo Real

**User Story:** As a monitoring user, I want a real-time dashboard, so that I can see the current state of the electoral system at a glance.

#### Acceptance Criteria

1. WHEN accessing the monitoring dashboard THEN the System SHALL display a centralized interface with multiple panels
2. WHEN the dashboard loads THEN the System SHALL show: map of geolocated users, statistics panel, recent activity feed, alerts panel
3. WHEN data changes THEN the System SHALL update the dashboard automatically without page reload
4. WHEN the dashboard is active THEN the System SHALL refresh data every 30 seconds
5. WHEN the user leaves the dashboard THEN the System SHALL stop automatic refreshing

### Requirement 3: Vista de Todos los Usuarios Geolocalizados

**User Story:** As a monitoring user, I want to see all geolocated users on a map, so that I can visualize the geographic distribution of electoral personnel.

#### Acceptance Criteria

1. WHEN viewing the map THEN the System SHALL display all users with valid GPS coordinates
2. WHEN displaying users THEN the System SHALL show: testigos, coordinadores_puesto, coordinadores_municipal, coordinadores_departamental
3. WHEN clicking a user marker THEN the System SHALL show: nombre, rol, ubicación asignada, última actualización GPS, presencia verificada (if testigo)
4. WHEN filtering by role THEN the System SHALL show only users with the selected role
5. WHEN a user's GPS updates THEN the System SHALL update their marker position on the map

### Requirement 4: Estadísticas Globales de Testigos

**User Story:** As a monitoring user, I want to see global statistics about testigos, so that I can assess their coverage and activity.

#### Acceptance Criteria

1. WHEN viewing statistics THEN the System SHALL show total number of active testigos
2. WHEN viewing statistics THEN the System SHALL show number of testigos with geolocation active
3. WHEN viewing statistics THEN the System SHALL show number of testigos with verified presence
4. WHEN viewing statistics THEN the System SHALL calculate percentage of testigos with geolocation
5. WHEN viewing statistics THEN the System SHALL calculate percentage of testigos with verified presence

### Requirement 5: Estadísticas Globales de Coordinadores

**User Story:** As a monitoring user, I want to see global statistics about coordinadores, so that I can assess their coverage and activity.

#### Acceptance Criteria

1. WHEN viewing statistics THEN the System SHALL show total number of active coordinadores (all levels)
2. WHEN viewing statistics THEN the System SHALL show number of coordinadores with geolocation active
3. WHEN viewing statistics THEN the System SHALL calculate percentage of coordinadores with geolocation
4. WHEN viewing statistics THEN the System SHALL break down coordinadores by level (departamental, municipal, puesto)
5. WHEN viewing statistics THEN the System SHALL show activity status of coordinadores

### Requirement 6: Estadísticas Globales de Formularios

**User Story:** As a monitoring user, I want to see global statistics about formularios E-14, so that I can track data collection progress.

#### Acceptance Criteria

1. WHEN viewing statistics THEN the System SHALL show total number of formularios E-14
2. WHEN viewing statistics THEN the System SHALL show number of formularios validados
3. WHEN viewing statistics THEN the System SHALL show number of formularios pendientes
4. WHEN viewing statistics THEN the System SHALL calculate percentage of formularios validados
5. WHEN viewing statistics THEN the System SHALL show formularios by estado (pendiente, validado, rechazado)

### Requirement 7: Vista de Todos los Incidentes y Delitos

**User Story:** As a monitoring user, I want to see all incidents and crimes, so that I can identify patterns and critical issues.

#### Acceptance Criteria

1. WHEN viewing incidents THEN the System SHALL show all incidents from all locations
2. WHEN viewing crimes THEN the System SHALL show all crimes from all locations
3. WHEN displaying reports THEN the System SHALL show: tipo, título, severidad/gravedad, estado, ubicación, fecha
4. WHEN filtering reports THEN the System SHALL allow filtering by: tipo, estado, severidad/gravedad, fecha, ubicación
5. WHEN clicking a report THEN the System SHALL show full details including seguimiento history

### Requirement 8: Alertas y Notificaciones

**User Story:** As a monitoring user, I want to receive alerts about critical events, so that I can respond quickly to important issues.

#### Acceptance Criteria

1. WHEN a critical incident is reported THEN the System SHALL create an alert for monitoring users
2. WHEN a crime is reported THEN the System SHALL create an alert for monitoring users
3. WHEN a testigo has not verified presence for 2 hours THEN the System SHALL create an alert
4. WHEN displaying alerts THEN the System SHALL show: tipo de alerta, descripción, timestamp, estado (nueva, vista, resuelta)
5. WHEN an alert is clicked THEN the System SHALL mark it as vista and navigate to the relevant detail

### Requirement 9: Exportación de Datos

**User Story:** As a monitoring user, I want to export data, so that I can perform external analysis or generate reports.

#### Acceptance Criteria

1. WHEN exporting data THEN the System SHALL allow selection of data type: usuarios, formularios, incidentes, delitos, estadísticas
2. WHEN exporting THEN the System SHALL allow selection of format: Excel, CSV, PDF
3. WHEN exporting to Excel THEN the System SHALL create a spreadsheet with all selected data
4. WHEN exporting to CSV THEN the System SHALL create a comma-separated file
5. WHEN exporting to PDF THEN the System SHALL create a formatted report with charts and tables

### Requirement 10: Filtros Avanzados

**User Story:** As a monitoring user, I want advanced filtering options, so that I can focus on specific subsets of data.

#### Acceptance Criteria

1. WHEN filtering users THEN the System SHALL allow filtering by: rol, estado de presencia, con/sin geolocalización, departamento, municipio
2. WHEN filtering formularios THEN the System SHALL allow filtering by: estado, departamento, municipio, puesto, fecha
3. WHEN filtering reports THEN the System SHALL allow filtering by: tipo, estado, severidad/gravedad, departamento, municipio, fecha
4. WHEN multiple filters are applied THEN the System SHALL combine them with AND logic
5. WHEN filters are cleared THEN the System SHALL show all data again

### Requirement 11: Búsqueda Global

**User Story:** As a monitoring user, I want to search across all data, so that I can quickly find specific information.

#### Acceptance Criteria

1. WHEN searching THEN the System SHALL search across: usuarios (nombre), formularios (mesa), incidentes (título, descripción), delitos (título, descripción)
2. WHEN search results are displayed THEN the System SHALL show the data type and relevant fields
3. WHEN clicking a search result THEN the System SHALL navigate to the detail view
4. WHEN search query is empty THEN the System SHALL show recent activity
5. WHEN no results are found THEN the System SHALL display "No se encontraron resultados"

### Requirement 12: Panel de Actividad Reciente

**User Story:** As a monitoring user, I want to see recent activity, so that I can stay informed of the latest events.

#### Acceptance Criteria

1. WHEN viewing recent activity THEN the System SHALL show the last 50 events
2. WHEN displaying events THEN the System SHALL include: formularios creados, incidentes reportados, delitos reportados, presencias verificadas
3. WHEN displaying events THEN the System SHALL show: tipo de evento, descripción, usuario, ubicación, timestamp
4. WHEN new events occur THEN the System SHALL add them to the top of the feed
5. WHEN clicking an event THEN the System SHALL navigate to the relevant detail view

### Requirement 13: Mapa de Calor de Actividad

**User Story:** As a monitoring user, I want to see a heatmap of activity, so that I can identify areas with high or low activity.

#### Acceptance Criteria

1. WHEN viewing the heatmap THEN the System SHALL show activity density by geographic area
2. WHEN calculating density THEN the System SHALL consider: number of users, number of formularios, number of reports
3. WHEN displaying the heatmap THEN the System SHALL use color gradient (blue=low, yellow=medium, red=high)
4. WHEN hovering over an area THEN the System SHALL show activity count for that area
5. WHEN clicking an area THEN the System SHALL filter data to show only that area

### Requirement 14: Comparación entre Departamentos

**User Story:** As a monitoring user, I want to compare departments, so that I can identify which departments are performing well or need attention.

#### Acceptance Criteria

1. WHEN viewing department comparison THEN the System SHALL show metrics for each department
2. WHEN displaying metrics THEN the System SHALL include: total mesas, formularios completados, porcentaje de avance, incidentes, delitos
3. WHEN displaying comparison THEN the System SHALL sort departments by porcentaje de avance
4. WHEN clicking a department THEN the System SHALL filter all data to show only that department
5. WHEN exporting comparison THEN the System SHALL include all department metrics

### Requirement 15: Permisos y Seguridad

**User Story:** As a system administrator, I want monitoring access to be secure, so that only authorized personnel can view global data.

#### Acceptance Criteria

1. WHEN a non-monitoreo user attempts to access monitoring dashboard THEN the System SHALL return 403 Forbidden
2. WHEN a monitoreo user accesses data THEN the System SHALL log the access for audit purposes
3. WHEN creating a monitoreo user THEN the System SHALL require super_admin authorization
4. WHEN a monitoreo user is deactivated THEN the System SHALL immediately revoke access to the monitoring dashboard
5. WHEN displaying sensitive data THEN the System SHALL mask personal information (e.g., partial phone numbers)

