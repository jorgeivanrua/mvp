# Requirements Document - Sistema de Incidentes y Delitos Electorales

## Introduction

El Sistema de Incidentes y Delitos Electorales permite a los usuarios del sistema electoral (testigos, coordinadores, auditores) reportar, dar seguimiento y resolver incidentes y delitos que ocurran durante el proceso electoral. El sistema distingue entre incidentes (irregularidades operacionales) y delitos (violaciones legales), cada uno con sus propios tipos, niveles de gravedad/severidad, y flujos de resolución. Incluye funcionalidades de adjuntar evidencias (fotos, videos), geolocalización de reportes, seguimiento detallado con historial de cambios, notificaciones automáticas a supervisores, escalamiento según gravedad, y estadísticas de reportes.

## Glossary

- **Sistema**: Sistema Electoral de Recolección de Datos
- **Incidente Electoral**: Irregularidad operacional o problema que afecta el proceso electoral pero no constituye un delito
- **Delito Electoral**: Violación legal del proceso electoral que puede ser denunciada ante autoridades competentes
- **Reporte**: Registro de un incidente o delito en el sistema
- **Severidad**: Nivel de gravedad de un incidente (baja, media, alta, crítica)
- **Gravedad**: Nivel de gravedad de un delito (leve, media, grave, muy grave)
- **Estado**: Situación actual del reporte en su ciclo de vida
- **Seguimiento**: Historial de acciones y cambios realizados sobre un reporte
- **Escalamiento**: Proceso de elevar un reporte a un nivel superior de supervisión
- **Evidencia**: Material de soporte (fotos, videos, documentos) adjunto a un reporte
- **Denuncia Formal**: Presentación oficial de un delito ante autoridades competentes
- **Notificación**: Alerta automática enviada a supervisores sobre reportes

## Requirements

### Requirement 1: Reporte de Incidentes Electorales

**User Story:** As a user (testigo, coordinador), I want to report electoral incidents, so that operational problems can be documented and resolved.

#### Acceptance Criteria

1. WHEN a user creates an incident report THEN the System SHALL capture: tipo_incidente, titulo, descripcion, severidad, mesa_id, evidencia_url, ubicacion_gps, fecha_incidente
2. WHEN an incident is created THEN the System SHALL automatically determine puesto_id, municipio_id, and departamento_id based on mesa_id
3. WHEN an incident is created THEN the System SHALL set estado to 'reportado' by default
4. WHEN an incident is created THEN the System SHALL record reportado_por_id with the user's ID
5. WHEN an incident is created THEN the System SHALL record fecha_reporte with the current timestamp

### Requirement 2: Tipos de Incidentes

**User Story:** As a user, I want to select from predefined incident types, so that incidents are categorized consistently.

#### Acceptance Criteria

1. WHEN selecting incident type THEN the System SHALL provide: retraso_apertura, falta_material, problemas_tecnicos, irregularidades_proceso, ausencia_funcionarios, problemas_acceso, disturbios, otros
2. WHEN displaying incident type THEN the System SHALL show the human-readable label (e.g., "Retraso en apertura de mesa")
3. WHEN an incident type is 'otros' THEN the System SHALL require a detailed description
4. WHEN creating an incident THEN the System SHALL validate that tipo_incidente is one of the predefined types
5. WHEN filtering incidents THEN the System SHALL allow filtering by tipo_incidente

### Requirement 3: Niveles de Severidad de Incidentes

**User Story:** As a user, I want to assign a severity level to incidents, so that urgent issues are prioritized.

#### Acceptance Criteria

1. WHEN creating an incident THEN the System SHALL allow selection of severidad: baja, media, alta, critica
2. WHEN severidad is not specified THEN the System SHALL default to 'media'
3. WHEN severidad is 'critica' THEN the System SHALL automatically notify coordinador_municipal in addition to coordinador_puesto
4. WHEN displaying severidad THEN the System SHALL use color coding (green=baja, yellow=media, orange=alta, red=critica)
5. WHEN filtering incidents THEN the System SHALL allow filtering by severidad

### Requirement 4: Reporte de Delitos Electorales

**User Story:** As a user, I want to report electoral crimes, so that legal violations can be investigated and prosecuted.

#### Acceptance Criteria

1. WHEN a user creates a crime report THEN the System SHALL capture: tipo_delito, titulo, descripcion, gravedad, mesa_id, evidencia_url, testigos_adicionales, ubicacion_gps, fecha_delito
2. WHEN a crime is created THEN the System SHALL automatically determine puesto_id, municipio_id, and departamento_id based on mesa_id
3. WHEN a crime is created THEN the System SHALL set estado to 'reportado' by default
4. WHEN a crime is created THEN the System SHALL record reportado_por_id with the user's ID
5. WHEN a crime is created THEN the System SHALL record fecha_reporte with the current timestamp

### Requirement 5: Tipos de Delitos

**User Story:** As a user, I want to select from predefined crime types, so that crimes are categorized according to electoral law.

#### Acceptance Criteria

1. WHEN selecting crime type THEN the System SHALL provide: compra_votos, coaccion_votante, fraude_electoral, suplantacion_identidad, alteracion_resultados, violencia_electoral, propaganda_ilegal, financiacion_ilegal, otros_delitos
2. WHEN displaying crime type THEN the System SHALL show the human-readable label (e.g., "Compra de votos")
3. WHEN a crime type is 'otros_delitos' THEN the System SHALL require a detailed description
4. WHEN creating a crime THEN the System SHALL validate that tipo_delito is one of the predefined types
5. WHEN filtering crimes THEN the System SHALL allow filtering by tipo_delito

### Requirement 6: Niveles de Gravedad de Delitos

**User Story:** As a user, I want to assign a gravity level to crimes, so that serious crimes receive appropriate attention.

#### Acceptance Criteria

1. WHEN creating a crime THEN the System SHALL allow selection of gravedad: leve, media, grave, muy_grave
2. WHEN gravedad is not specified THEN the System SHALL default to 'media'
3. WHEN a crime is created THEN the System SHALL automatically notify coordinador_municipal, coordinador_departamental, and auditor_electoral
4. WHEN displaying gravedad THEN the System SHALL use color coding (blue=leve, yellow=media, orange=grave, red=muy_grave)
5. WHEN filtering crimes THEN the System SHALL allow filtering by gravedad

### Requirement 7: Adjuntar Evidencias

**User Story:** As a user, I want to attach evidence to reports, so that incidents and crimes can be properly documented.

#### Acceptance Criteria

1. WHEN creating a report THEN the System SHALL allow uploading photos, videos, or documents as evidence
2. WHEN evidence is uploaded THEN the System SHALL store the file and save the URL in evidencia_url field
3. WHEN displaying a report THEN the System SHALL show attached evidence with preview capability
4. WHEN evidence file size exceeds limit THEN the System SHALL reject the upload with an error message
5. WHEN evidence file type is not allowed THEN the System SHALL reject the upload with an error message

### Requirement 8: Geolocalización de Reportes

**User Story:** As a user, I want to capture GPS coordinates when reporting, so that the exact location of incidents/crimes is recorded.

#### Acceptance Criteria

1. WHEN creating a report THEN the System SHALL capture GPS coordinates if available
2. WHEN GPS coordinates are captured THEN the System SHALL store them in ubicacion_gps field as "latitude,longitude"
3. WHEN displaying a report THEN the System SHALL show the location on a map if GPS coordinates are available
4. WHEN GPS is unavailable THEN the System SHALL allow creating the report without coordinates
5. WHEN filtering reports THEN the System SHALL allow viewing all reports on a map

### Requirement 9: Estados de Incidentes

**User Story:** As a coordinator, I want to track the status of incidents, so that I can monitor their resolution progress.

#### Acceptance Criteria

1. WHEN an incident is created THEN the System SHALL set estado to 'reportado'
2. WHEN a coordinator reviews an incident THEN the System SHALL allow changing estado to 'en_revision'
3. WHEN an incident is resolved THEN the System SHALL allow changing estado to 'resuelto'
4. WHEN an incident requires escalation THEN the System SHALL allow changing estado to 'escalado'
5. WHEN estado changes THEN the System SHALL record the change in seguimiento history

### Requirement 10: Estados de Delitos

**User Story:** As a coordinator or auditor, I want to track the status of crimes, so that I can monitor investigation and prosecution progress.

#### Acceptance Criteria

1. WHEN a crime is created THEN the System SHALL set estado to 'reportado'
2. WHEN an auditor begins investigation THEN the System SHALL allow changing estado to 'en_investigacion'
3. WHEN investigation is complete THEN the System SHALL allow changing estado to 'investigado'
4. WHEN a crime is formally reported to authorities THEN the System SHALL allow changing estado to 'denunciado'
5. WHEN a crime is closed without action THEN the System SHALL allow changing estado to 'archivado'

### Requirement 11: Seguimiento de Reportes

**User Story:** As a coordinator, I want to see the complete history of a report, so that I can understand all actions taken.

#### Acceptance Criteria

1. WHEN any action is performed on a report THEN the System SHALL create a seguimiento record
2. WHEN creating seguimiento THEN the System SHALL record: tipo_reporte, reporte_id, usuario_id, accion, comentario, estado_anterior, estado_nuevo, created_at
3. WHEN viewing a report THEN the System SHALL display all seguimiento records in chronological order
4. WHEN displaying seguimiento THEN the System SHALL show: user name, action, comment, state change, timestamp
5. WHEN a report has no seguimiento THEN the System SHALL show "Sin seguimiento registrado"

### Requirement 12: Notificaciones de Reportes

**User Story:** As a coordinator, I want to receive notifications about new reports, so that I can respond quickly to incidents and crimes.

#### Acceptance Criteria

1. WHEN an incident is created THEN the System SHALL notify the coordinador_puesto of the affected puesto
2. WHEN an incident with severidad 'critica' is created THEN the System SHALL also notify the coordinador_municipal
3. WHEN a crime is created THEN the System SHALL notify coordinador_municipal, coordinador_departamental, and all auditor_electoral users
4. WHEN a notification is created THEN the System SHALL record: usuario_id, tipo_reporte, reporte_id, tipo_notificacion, titulo, mensaje, leida, created_at
5. WHEN displaying notifications THEN the System SHALL show unread notifications prominently

### Requirement 13: Resolución de Incidentes

**User Story:** As a coordinator, I want to resolve incidents, so that they are marked as complete with resolution notes.

#### Acceptance Criteria

1. WHEN resolving an incident THEN the System SHALL require changing estado to 'resuelto'
2. WHEN an incident is resolved THEN the System SHALL record resuelto_por_id with the coordinator's ID
3. WHEN an incident is resolved THEN the System SHALL record fecha_resolucion with the current timestamp
4. WHEN resolving an incident THEN the System SHALL allow adding notas_resolucion
5. WHEN an incident is resolved THEN the System SHALL create a seguimiento record with the resolution notes

### Requirement 14: Investigación de Delitos

**User Story:** As an auditor, I want to investigate crimes, so that I can determine if formal prosecution is warranted.

#### Acceptance Criteria

1. WHEN an auditor begins investigating a crime THEN the System SHALL record investigado_por_id with the auditor's ID
2. WHEN investigation begins THEN the System SHALL record fecha_investigacion with the current timestamp
3. WHEN investigation is complete THEN the System SHALL allow adding resultado_investigacion
4. WHEN investigation concludes THEN the System SHALL change estado to 'investigado'
5. WHEN investigation is recorded THEN the System SHALL create a seguimiento record with investigation results

### Requirement 15: Denuncia Formal de Delitos

**User Story:** As an auditor or coordinator, I want to formally report crimes to authorities, so that legal action can be taken.

#### Acceptance Criteria

1. WHEN formally reporting a crime THEN the System SHALL record denunciado_formalmente as True
2. WHEN formally reporting THEN the System SHALL require numero_denuncia (complaint number)
3. WHEN formally reporting THEN the System SHALL require autoridad_competente (competent authority)
4. WHEN formally reporting THEN the System SHALL record fecha_denuncia with the current timestamp
5. WHEN formally reporting THEN the System SHALL change estado to 'denunciado'

### Requirement 16: Escalamiento de Reportes

**User Story:** As a coordinator, I want to escalate reports to higher levels, so that complex issues receive appropriate attention.

#### Acceptance Criteria

1. WHEN escalating an incident THEN the System SHALL allow setting escalado_a to: coordinador_municipal, coordinador_departamental, or auditor
2. WHEN escalating THEN the System SHALL change estado to 'escalado'
3. WHEN escalating THEN the System SHALL create notifications for the escalation target
4. WHEN escalating THEN the System SHALL create a seguimiento record with escalation reason
5. WHEN displaying escalated reports THEN the System SHALL show the escalation target

### Requirement 17: Filtrado y Búsqueda de Reportes

**User Story:** As a coordinator, I want to filter and search reports, so that I can find specific incidents or crimes quickly.

#### Acceptance Criteria

1. WHEN viewing reports THEN the System SHALL allow filtering by estado
2. WHEN viewing reports THEN the System SHALL allow filtering by severidad/gravedad
3. WHEN viewing reports THEN the System SHALL allow filtering by tipo_incidente/tipo_delito
4. WHEN viewing reports THEN the System SHALL allow filtering by fecha_desde and fecha_hasta
5. WHEN no filters are applied THEN the System SHALL show all reports ordered by fecha_reporte descending

### Requirement 18: Estadísticas de Reportes

**User Story:** As a coordinator, I want to see statistics about reports, so that I can identify patterns and trends.

#### Acceptance Criteria

1. WHEN viewing statistics THEN the System SHALL show total number of incidents and crimes
2. WHEN viewing statistics THEN the System SHALL show breakdown by estado for both incidents and crimes
3. WHEN viewing statistics THEN the System SHALL show breakdown by severidad for incidents
4. WHEN viewing statistics THEN the System SHALL show breakdown by gravedad for crimes
5. WHEN viewing statistics THEN the System SHALL show number of crimes formally reported (denunciados)

### Requirement 19: Permisos de Visualización

**User Story:** As a system administrator, I want reports filtered by user role and jurisdiction, so that users only see reports they are authorized to view.

#### Acceptance Criteria

1. WHEN a testigo_electoral views reports THEN the System SHALL show only reports created by that testigo
2. WHEN a coordinador_puesto views reports THEN the System SHALL show only reports from their puesto
3. WHEN a coordinador_municipal views reports THEN the System SHALL show only reports from their municipio
4. WHEN a coordinador_departamental views reports THEN the System SHALL show only reports from their departamento
5. WHEN a super_admin or auditor_electoral views reports THEN the System SHALL show all reports

### Requirement 20: Exportación de Reportes

**User Story:** As a coordinator or auditor, I want to export reports, so that I can analyze them externally or share with authorities.

#### Acceptance Criteria

1. WHEN exporting reports THEN the System SHALL allow selection of format: PDF, Excel, or CSV
2. WHEN exporting to PDF THEN the System SHALL include all report details, evidence links, and seguimiento history
3. WHEN exporting to Excel THEN the System SHALL create a spreadsheet with one row per report
4. WHEN exporting to CSV THEN the System SHALL create a comma-separated file with all report fields
5. WHEN exporting THEN the System SHALL apply current filters to determine which reports to export

