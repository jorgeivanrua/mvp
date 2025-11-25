# Requirements Document - Sistema de Geolocalización y Verificación de Presencia

## Introduction

El Sistema de Geolocalización y Verificación de Presencia permite a los usuarios del sistema electoral (testigos, coordinadores, auditores) verificar su presencia física en las ubicaciones asignadas mediante captura de coordenadas GPS. El sistema proporciona tracking en tiempo real de la ubicación de los usuarios, mapas interactivos de puestos y usuarios geolocalizados, historial de verificaciones, y notificaciones automáticas a coordinadores. Incluye funcionalidad de ping automático para mantener la presencia activa y determinar el estado de actividad de cada usuario.

## Glossary

- **Sistema**: Sistema Electoral de Recolección de Datos
- **Usuario**: Cualquier persona con acceso al sistema (testigo, coordinador, auditor, etc.)
- **Testigo Electoral**: Usuario asignado a una mesa de votación específica
- **Coordinador**: Usuario supervisor (coordinador de puesto, municipal, departamental)
- **Verificación de Presencia**: Acción de confirmar que un usuario está físicamente en su ubicación asignada
- **Geolocalización**: Proceso de captura de coordenadas GPS (latitud, longitud)
- **Tracking**: Seguimiento continuo de la ubicación de usuarios
- **Ping**: Señal automática enviada periódicamente para mantener presencia activa
- **Estado de Usuario**: Clasificación del usuario según su actividad (activo, inactivo, ausente)
- **Precisión GPS**: Margen de error en metros de las coordenadas capturadas
- **Último Acceso**: Timestamp de la última interacción del usuario con el sistema

## Requirements

### Requirement 1: Verificación Manual de Presencia

**User Story:** As a user (testigo, coordinador, auditor), I want to manually verify my presence at my assigned location, so that my supervisor knows I am physically present and active.

#### Acceptance Criteria

1. WHEN a user clicks the "Verificar Presencia" button THEN the System SHALL capture the current GPS coordinates (latitude, longitude)
2. WHEN GPS coordinates are captured THEN the System SHALL update the user's presencia_verificada field to True
3. WHEN presence is verified THEN the System SHALL record the timestamp in presencia_verificada_at
4. WHEN presence is verified THEN the System SHALL update the ultimo_acceso timestamp
5. WHEN presence verification succeeds THEN the System SHALL return a success message with the user's role and location information

### Requirement 2: Captura de Coordenadas GPS

**User Story:** As a user, I want the system to capture my GPS coordinates when I verify presence, so that my exact location is recorded.

#### Acceptance Criteria

1. WHEN capturing GPS coordinates THEN the System SHALL request browser geolocation permission
2. WHEN coordinates are obtained THEN the System SHALL store latitude in ultima_latitud field
3. WHEN coordinates are obtained THEN the System SHALL store longitude in ultima_longitud field
4. WHEN coordinates are obtained THEN the System SHALL record the timestamp in ultima_geolocalizacion_at
5. WHEN GPS precision is available THEN the System SHALL store it in precision_geolocalizacion field

### Requirement 3: Tracking de Última Ubicación

**User Story:** As a coordinator, I want to see the last known location of users under my supervision, so that I can verify they are at their assigned locations.

#### Acceptance Criteria

1. WHEN a coordinator views their team THEN the System SHALL display the last known coordinates for each user
2. WHEN displaying location data THEN the System SHALL show the timestamp of the last geolocation update
3. WHEN a user has never shared location THEN the System SHALL display "Sin geolocalización"
4. WHEN location data is older than 60 minutes THEN the System SHALL mark it as "Desactualizada"
5. WHEN displaying coordinates THEN the System SHALL format them with 6 decimal places for precision

### Requirement 4: Estado de Actividad de Usuarios

**User Story:** As a coordinator, I want to see the activity status of users under my supervision, so that I can identify who is active, inactive, or absent.

#### Acceptance Criteria

1. WHEN a user's ultimo_acceso is less than 15 minutes ago THEN the System SHALL classify them as "activo"
2. WHEN a user's ultimo_acceso is between 15 and 60 minutes ago THEN the System SHALL classify them as "inactivo"
3. WHEN a user's ultimo_acceso is more than 60 minutes ago THEN the System SHALL classify them as "ausente"
4. WHEN a user has never accessed the system THEN the System SHALL classify them as "ausente"
5. WHEN displaying user status THEN the System SHALL show minutes since last access

### Requirement 5: Ping Automático de Presencia

**User Story:** As a user, I want the system to automatically send presence pings while I'm active, so that I don't have to manually verify presence repeatedly.

#### Acceptance Criteria

1. WHEN a user is logged in and active THEN the System SHALL send automatic ping requests every 5 minutes
2. WHEN a ping is sent THEN the System SHALL update the user's ultimo_acceso timestamp
3. WHEN a user has not verified presence THEN the System SHALL mark presencia_verificada as True on first ping
4. WHEN a ping fails THEN the System SHALL retry up to 3 times before marking the user as inactive
5. WHEN the user closes the browser THEN the System SHALL stop sending pings

### Requirement 6: Vista de Estado del Equipo

**User Story:** As a coordinator, I want to view the presence status of my entire team, so that I can monitor who is active and who needs attention.

#### Acceptance Criteria

1. WHEN a coordinador_puesto views team status THEN the System SHALL display all testigos assigned to their puesto
2. WHEN a coordinador_municipal views team status THEN the System SHALL display all coordinadores_puesto in their municipio
3. WHEN a coordinador_departamental views team status THEN the System SHALL display all coordinadores_municipal in their departamento
4. WHEN a super_admin views team status THEN the System SHALL display all coordinadores_departamental
5. WHEN displaying team status THEN the System SHALL show: name, role, location, presence status, last access, minutes inactive, and activity state

### Requirement 7: Estadísticas de Presencia

**User Story:** As a coordinator, I want to see presence statistics for my team, so that I can quickly assess overall team status.

#### Acceptance Criteria

1. WHEN viewing team status THEN the System SHALL calculate total number of team members
2. WHEN calculating statistics THEN the System SHALL count users in "activo" state
3. WHEN calculating statistics THEN the System SHALL count users in "inactivo" state
4. WHEN calculating statistics THEN the System SHALL count users in "ausente" state
5. WHEN displaying statistics THEN the System SHALL show percentage of present users (activo / total * 100)

### Requirement 8: Mapa de Usuarios Geolocalizados

**User Story:** As a coordinator, I want to see a map with all geolocalized users under my supervision, so that I can visualize their physical distribution.

#### Acceptance Criteria

1. WHEN a coordinator accesses the map THEN the System SHALL display all users with valid GPS coordinates
2. WHEN displaying users on map THEN the System SHALL filter based on the coordinator's role and jurisdiction
3. WHEN a coordinador_puesto views the map THEN the System SHALL show only testigos from their puesto
4. WHEN a coordinador_municipal views the map THEN the System SHALL show coordinadores_puesto and testigos from their municipio
5. WHEN a coordinador_departamental views the map THEN the System SHALL show all coordinadores and testigos from their departamento

### Requirement 9: Información de Marcadores en Mapa

**User Story:** As a coordinator, I want to see detailed information about each user on the map, so that I can identify them and check their status.

#### Acceptance Criteria

1. WHEN displaying a user on the map THEN the System SHALL show their name, role, and assigned location
2. WHEN displaying a user marker THEN the System SHALL use different colors based on activity state (green=activo, yellow=inactivo, red=ausente)
3. WHEN clicking a user marker THEN the System SHALL display a popup with: name, role, location, last access, minutes inactive, and coordinates
4. WHEN a user's location is outdated THEN the System SHALL display a warning indicator
5. WHEN displaying coordinates THEN the System SHALL show latitude and longitude with 6 decimal places

### Requirement 10: Filtrado de Usuarios por Rol

**User Story:** As a coordinator, I want to filter users on the map by role, so that I can focus on specific types of users.

#### Acceptance Criteria

1. WHEN viewing the map THEN the System SHALL provide role filter options (testigos, coordinadores_puesto, coordinadores_municipal)
2. WHEN a role filter is applied THEN the System SHALL show only users with that role
3. WHEN multiple filters are selected THEN the System SHALL show users matching any of the selected roles
4. WHEN no filter is selected THEN the System SHALL show all users
5. WHEN filters change THEN the System SHALL update the map immediately without page reload

### Requirement 11: Manejo de Errores de GPS

**User Story:** As a user, I want clear error messages when GPS fails, so that I understand what went wrong and how to fix it.

#### Acceptance Criteria

1. WHEN GPS permission is denied THEN the System SHALL display "Permiso de ubicación denegado. Por favor, habilite la ubicación en su navegador."
2. WHEN GPS is unavailable THEN the System SHALL display "GPS no disponible en este dispositivo"
3. WHEN GPS timeout occurs THEN the System SHALL display "Tiempo de espera agotado. Intente nuevamente."
4. WHEN GPS accuracy is too low THEN the System SHALL display a warning "Precisión GPS baja (±X metros)"
5. WHEN GPS error occurs THEN the System SHALL allow the user to retry verification

### Requirement 12: Historial de Verificaciones

**User Story:** As a coordinator, I want to see the history of presence verifications for each user, so that I can track their attendance pattern.

#### Acceptance Criteria

1. WHEN viewing a user's details THEN the System SHALL display their presencia_verificada status
2. WHEN a user has verified presence THEN the System SHALL show the timestamp of verification
3. WHEN viewing team status THEN the System SHALL show how long ago each user verified presence
4. WHEN a user has not verified presence THEN the System SHALL display "No verificada"
5. WHEN displaying verification time THEN the System SHALL format it as relative time (e.g., "hace 15 minutos")

### Requirement 13: Notificaciones de Presencia

**User Story:** As a coordinator, I want to receive notifications when users verify presence, so that I can stay informed of team activity.

#### Acceptance Criteria

1. WHEN a user verifies presence THEN the System SHALL create a notification for their direct supervisor
2. WHEN a testigo verifies presence THEN the System SHALL notify their coordinador_puesto
3. WHEN a coordinador_puesto verifies presence THEN the System SHALL notify their coordinador_municipal
4. WHEN a notification is created THEN the System SHALL include: user name, role, location, and timestamp
5. WHEN displaying notifications THEN the System SHALL show them in chronological order (newest first)

### Requirement 14: Seguridad y Privacidad

**User Story:** As a system administrator, I want GPS data to be secure and private, so that user location information is protected.

#### Acceptance Criteria

1. WHEN storing GPS coordinates THEN the System SHALL encrypt them in the database
2. WHEN a user requests their location data THEN the System SHALL only show their own coordinates
3. WHEN a coordinator requests location data THEN the System SHALL only show users under their jurisdiction
4. WHEN GPS data is transmitted THEN the System SHALL use HTTPS encryption
5. WHEN a user is deactivated THEN the System SHALL retain their location history for audit purposes but mark it as archived

### Requirement 15: Validación de Ubicación

**User Story:** As a coordinator, I want the system to validate that users are at their assigned locations, so that I can detect anomalies.

#### Acceptance Criteria

1. WHEN a user verifies presence THEN the System SHALL compare their GPS coordinates with their assigned location coordinates
2. WHEN coordinates are within 500 meters of assigned location THEN the System SHALL mark verification as "En ubicación correcta"
3. WHEN coordinates are more than 500 meters from assigned location THEN the System SHALL mark verification as "Fuera de ubicación" and create an alert
4. WHEN assigned location has no coordinates THEN the System SHALL skip validation and accept any coordinates
5. WHEN displaying validation status THEN the System SHALL show the distance in meters from assigned location

