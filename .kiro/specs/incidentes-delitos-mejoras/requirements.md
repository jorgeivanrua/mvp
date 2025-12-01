# Requirements Document: Sistema de Incidentes y Delitos Electorales

## Introduction

Este documento especifica las mejoras y clarificaciones necesarias para el sistema de reporte y gestión de incidentes y delitos electorales. El sistema debe permitir a los testigos electorales reportar situaciones irregulares con evidencia fotográfica y texto, asegurando que la información fluya correctamente a través de la cadena de mando y que se mantenga un registro completo de todas las acciones tomadas.

## Glossary

- **Sistema**: Sistema Electoral de Gestión de Incidentes y Delitos
- **Testigo Electoral**: Usuario con rol testigo_electoral asignado a una mesa de votación
- **Coordinador de Puesto**: Usuario con rol coordinador_puesto responsable de un puesto de votación
- **Coordinador Municipal**: Usuario con rol coordinador_municipal responsable de un municipio
- **Coordinador Departamental**: Usuario con rol coordinador_departamental responsable de un departamento
- **Auditor Electoral**: Usuario con rol auditor_electoral con permisos especiales para investigar delitos
- **Incidente Electoral**: Irregularidad o problema operativo en el proceso electoral (ej: retraso, falta de material)
- **Delito Electoral**: Acción ilegal que viola las leyes electorales (ej: compra de votos, fraude)
- **Evidencia Fotográfica**: Imagen capturada como prueba de un incidente o delito
- **Seguimiento**: Registro histórico de todas las acciones tomadas sobre un reporte
- **Notificación**: Alerta enviada a usuarios relevantes sobre nuevos reportes o cambios de estado
- **Estado del Reporte**: Situación actual del incidente o delito (reportado, en_revision, resuelto, etc.)
- **Geolocalización**: Coordenadas GPS del lugar donde ocurrió el incidente o delito

## Requirements

### Requirement 1: Reporte de Incidentes por Testigos

**User Story:** Como testigo electoral, quiero reportar incidentes con evidencia fotográfica y descripción detallada, para que los coordinadores puedan tomar acción inmediata.

#### Acceptance Criteria

1. WHEN un testigo electoral accede a la función de reporte de incidentes THEN el Sistema SHALL mostrar un formulario con campos para tipo de incidente, título, descripción, severidad y opción para adjuntar fotos
2. WHEN un testigo electoral selecciona "adjuntar foto" THEN el Sistema SHALL permitir capturar foto con la cámara del dispositivo o seleccionar desde la galería
3. WHEN un testigo electoral captura una foto THEN el Sistema SHALL incluir automáticamente la geolocalización GPS en los metadatos de la evidencia
4. WHEN un testigo electoral envía un reporte de incidente THEN el Sistema SHALL guardar el incidente con estado "reportado" y asociarlo a la mesa del testigo
5. WHEN un testigo electoral envía un reporte de incidente THEN el Sistema SHALL notificar inmediatamente al coordinador de puesto asignado
6. WHEN un testigo electoral envía un reporte de incidente con severidad "crítica" THEN el Sistema SHALL notificar también al coordinador municipal
7. WHEN un testigo electoral no tiene conexión a internet THEN el Sistema SHALL guardar el reporte localmente y sincronizarlo automáticamente cuando recupere conexión
8. WHEN un testigo electoral intenta enviar un reporte sin descripción THEN el Sistema SHALL mostrar un mensaje de error indicando que la descripción es obligatoria

### Requirement 2: Reporte de Delitos por Testigos

**User Story:** Como testigo electoral, quiero reportar delitos electorales con evidencia y testigos adicionales, para que se inicie una investigación formal.

#### Acceptance Criteria

1. WHEN un testigo electoral accede a la función de reporte de delitos THEN el Sistema SHALL mostrar un formulario con campos para tipo de delito, título, descripción, gravedad, testigos adicionales y opción para adjuntar fotos
2. WHEN un testigo electoral reporta un delito THEN el Sistema SHALL guardar el delito con estado "reportado" y asociarlo a la mesa del testigo
3. WHEN un testigo electoral reporta un delito THEN el Sistema SHALL notificar inmediatamente al coordinador municipal, coordinador departamental y todos los auditores electorales
4. WHEN un testigo electoral reporta un delito THEN el Sistema SHALL crear un registro de seguimiento inicial con la acción "crear" y el usuario reportante
5. WHEN un testigo electoral adjunta evidencia fotográfica a un delito THEN el Sistema SHALL almacenar la URL de la evidencia en el campo evidencia_url
6. WHEN un testigo electoral incluye testigos adicionales THEN el Sistema SHALL guardar los nombres y datos de contacto en el campo testigos_adicionales

### Requirement 3: Gestión de Evidencia Fotográfica

**User Story:** Como usuario del sistema, quiero que las fotos de evidencia se almacenen de forma segura y accesible, para mantener la integridad de las pruebas.

#### Acceptance Criteria

1. WHEN un usuario adjunta una foto como evidencia THEN el Sistema SHALL comprimir la imagen para optimizar el almacenamiento sin perder calidad significativa
2. WHEN un usuario adjunta una foto como evidencia THEN el Sistema SHALL generar un nombre único para el archivo basado en timestamp y hash
3. WHEN un usuario adjunta una foto como evidencia THEN el Sistema SHALL almacenar la foto en un directorio seguro con permisos restringidos
4. WHEN un usuario adjunta una foto como evidencia THEN el Sistema SHALL guardar la URL completa de acceso en el campo evidencia_url del reporte
5. WHEN un coordinador o auditor visualiza un reporte THEN el Sistema SHALL mostrar las fotos de evidencia en tamaño completo con opción de zoom
6. WHEN un usuario intenta adjuntar un archivo que no es imagen THEN el Sistema SHALL rechazar el archivo y mostrar un mensaje de error
7. WHEN un usuario adjunta múltiples fotos THEN el Sistema SHALL almacenar todas las URLs separadas por comas en el campo evidencia_url

### Requirement 4: Flujo de Notificaciones por Jerarquía

**User Story:** Como coordinador, quiero recibir notificaciones automáticas de incidentes y delitos en mi jurisdicción, para poder responder rápidamente.

#### Acceptance Criteria

1. WHEN se crea un incidente con severidad "baja" o "media" THEN el Sistema SHALL notificar solo al coordinador de puesto
2. WHEN se crea un incidente con severidad "alta" THEN el Sistema SHALL notificar al coordinador de puesto y al coordinador municipal
3. WHEN se crea un incidente con severidad "crítica" THEN el Sistema SHALL notificar al coordinador de puesto, coordinador municipal y coordinador departamental
4. WHEN se crea un delito electoral THEN el Sistema SHALL notificar al coordinador municipal, coordinador departamental y todos los auditores electorales
5. WHEN un coordinador cambia el estado de un incidente THEN el Sistema SHALL notificar al testigo que lo reportó
6. WHEN un incidente es escalado THEN el Sistema SHALL notificar al nivel jerárquico superior correspondiente
7. WHEN un usuario recibe una notificación THEN el Sistema SHALL mostrar un badge con el número de notificaciones no leídas
8. WHEN un usuario hace clic en una notificación THEN el Sistema SHALL marcarla como leída y mostrar el detalle del reporte

### Requirement 5: Gestión de Estados de Incidentes

**User Story:** Como coordinador de puesto, quiero actualizar el estado de los incidentes y registrar las acciones tomadas, para mantener un seguimiento completo.

#### Acceptance Criteria

1. WHEN un coordinador de puesto visualiza un incidente THEN el Sistema SHALL mostrar opciones para cambiar el estado a "en_revision", "resuelto" o "escalado"
2. WHEN un coordinador cambia el estado de un incidente a "en_revision" THEN el Sistema SHALL solicitar un comentario obligatorio sobre las acciones en curso
3. WHEN un coordinador cambia el estado de un incidente a "resuelto" THEN el Sistema SHALL solicitar notas de resolución obligatorias y registrar la fecha y usuario que resolvió
4. WHEN un coordinador cambia el estado de un incidente a "escalado" THEN el Sistema SHALL solicitar a qué nivel se escala y notificar al coordinador correspondiente
5. WHEN un coordinador actualiza el estado de un incidente THEN el Sistema SHALL crear un registro de seguimiento con el estado anterior, estado nuevo, usuario y comentario
6. WHEN un testigo electoral intenta cambiar el estado de un incidente THEN el Sistema SHALL denegar la acción y mostrar un mensaje de permisos insuficientes
7. WHEN un incidente está en estado "resuelto" THEN el Sistema SHALL mostrar las notas de resolución, fecha de resolución y usuario que resolvió

### Requirement 6: Gestión de Estados de Delitos

**User Story:** Como auditor electoral, quiero gestionar la investigación de delitos y su denuncia formal, para asegurar el seguimiento legal adecuado.

#### Acceptance Criteria

1. WHEN un auditor electoral visualiza un delito THEN el Sistema SHALL mostrar opciones para cambiar el estado a "en_investigacion", "investigado", "denunciado" o "archivado"
2. WHEN un auditor cambia el estado de un delito a "en_investigacion" THEN el Sistema SHALL registrar al auditor como investigador y la fecha de inicio de investigación
3. WHEN un auditor cambia el estado de un delito a "investigado" THEN el Sistema SHALL solicitar el resultado de la investigación en un campo de texto obligatorio
4. WHEN un auditor marca un delito como "denunciado" THEN el Sistema SHALL solicitar número de denuncia y autoridad competente de forma obligatoria
5. WHEN un auditor denuncia formalmente un delito THEN el Sistema SHALL marcar el campo denunciado_formalmente como true y registrar la fecha de denuncia
6. WHEN un coordinador municipal intenta denunciar formalmente un delito THEN el Sistema SHALL denegar la acción indicando que solo auditores pueden hacerlo
7. WHEN un delito está en estado "denunciado" THEN el Sistema SHALL mostrar el número de denuncia, autoridad competente y fecha de denuncia

### Requirement 7: Visualización de Seguimiento Completo

**User Story:** Como usuario autorizado, quiero ver el historial completo de acciones sobre un reporte, para entender qué se ha hecho al respecto.

#### Acceptance Criteria

1. WHEN un usuario visualiza el detalle de un incidente o delito THEN el Sistema SHALL mostrar una línea de tiempo con todos los registros de seguimiento
2. WHEN el Sistema muestra un registro de seguimiento THEN el Sistema SHALL incluir fecha/hora, usuario que realizó la acción, acción realizada, estado anterior, estado nuevo y comentario
3. WHEN un usuario visualiza el seguimiento THEN el Sistema SHALL ordenar los registros del más reciente al más antiguo
4. WHEN se crea un nuevo reporte THEN el Sistema SHALL crear automáticamente el primer registro de seguimiento con acción "crear"
5. WHEN se cambia el estado de un reporte THEN el Sistema SHALL crear automáticamente un registro de seguimiento con acción "cambiar_estado"
6. WHEN un usuario agrega un comentario sin cambiar estado THEN el Sistema SHALL crear un registro de seguimiento con acción "comentar"

### Requirement 8: Permisos y Visibilidad por Rol

**User Story:** Como administrador del sistema, quiero que cada rol vea solo los reportes de su jurisdicción, para mantener la seguridad y privacidad de la información.

#### Acceptance Criteria

1. WHEN un testigo electoral consulta incidentes THEN el Sistema SHALL mostrar solo los incidentes que él mismo reportó
2. WHEN un testigo electoral consulta delitos THEN el Sistema SHALL mostrar solo los delitos que él mismo reportó
3. WHEN un coordinador de puesto consulta incidentes THEN el Sistema SHALL mostrar solo incidentes de su puesto asignado
4. WHEN un coordinador municipal consulta incidentes THEN el Sistema SHALL mostrar solo incidentes de su municipio asignado
5. WHEN un coordinador departamental consulta incidentes THEN el Sistema SHALL mostrar solo incidentes de su departamento asignado
6. WHEN un auditor electoral consulta reportes THEN el Sistema SHALL mostrar todos los incidentes y delitos del sistema
7. WHEN un super_admin consulta reportes THEN el Sistema SHALL mostrar todos los incidentes y delitos del sistema
8. WHEN un usuario intenta acceder a un reporte fuera de su jurisdicción THEN el Sistema SHALL denegar el acceso y retornar error 403

### Requirement 9: Indicadores Visuales en Mapas

**User Story:** Como usuario de monitoreo, quiero ver indicadores visuales en el mapa cuando hay incidentes o delitos activos, para identificar rápidamente áreas problemáticas.

#### Acceptance Criteria

1. WHEN un puesto tiene incidentes activos (no resueltos) THEN el Sistema SHALL mostrar un icono de alerta amarillo sobre el pin del puesto en el mapa
2. WHEN un puesto tiene incidentes críticos activos THEN el Sistema SHALL mostrar un icono de alerta rojo parpadeante sobre el pin del puesto en el mapa
3. WHEN un puesto tiene delitos activos (no archivados) THEN el Sistema SHALL mostrar un icono de alerta rojo sobre el pin del puesto en el mapa
4. WHEN un usuario hace clic en un puesto con alertas THEN el Sistema SHALL mostrar en el popup el número de incidentes activos, incidentes críticos, delitos activos y delitos graves
5. WHEN un puesto tiene múltiples tipos de alertas THEN el Sistema SHALL mostrar el indicador de mayor prioridad (delitos > incidentes críticos > incidentes normales)
6. WHEN se resuelve el último incidente activo de un puesto THEN el Sistema SHALL remover el indicador de alerta del mapa
7. WHEN se archiva el último delito activo de un puesto THEN el Sistema SHALL remover el indicador de alerta del mapa

### Requirement 10: Sincronización Offline

**User Story:** Como testigo electoral en zona con conectividad intermitente, quiero que mis reportes se guarden localmente y se sincronicen automáticamente, para no perder información crítica.

#### Acceptance Criteria

1. WHEN un testigo intenta reportar un incidente sin conexión THEN el Sistema SHALL guardar el reporte en almacenamiento local del dispositivo
2. WHEN un testigo intenta reportar un delito sin conexión THEN el Sistema SHALL guardar el reporte en almacenamiento local del dispositivo
3. WHEN el dispositivo recupera conexión a internet THEN el Sistema SHALL sincronizar automáticamente todos los reportes pendientes
4. WHEN el Sistema sincroniza un reporte guardado localmente THEN el Sistema SHALL mostrar una notificación de éxito al usuario
5. WHEN el Sistema intenta sincronizar y falla THEN el Sistema SHALL mantener el reporte en cola local y reintentar en el próximo ciclo de sincronización
6. WHEN un usuario tiene reportes pendientes de sincronización THEN el Sistema SHALL mostrar un indicador visual con el número de reportes pendientes
7. WHEN un usuario visualiza sus reportes THEN el Sistema SHALL distinguir visualmente entre reportes sincronizados y pendientes de sincronización

### Requirement 11: Estadísticas y Reportes

**User Story:** Como coordinador, quiero ver estadísticas de incidentes y delitos en mi jurisdicción, para identificar patrones y tomar decisiones informadas.

#### Acceptance Criteria

1. WHEN un coordinador accede a estadísticas THEN el Sistema SHALL mostrar el total de incidentes por estado (reportado, en_revision, resuelto, escalado)
2. WHEN un coordinador accede a estadísticas THEN el Sistema SHALL mostrar el total de incidentes por severidad (baja, media, alta, crítica)
3. WHEN un coordinador accede a estadísticas THEN el Sistema SHALL mostrar el total de delitos por estado (reportado, en_investigacion, investigado, denunciado, archivado)
4. WHEN un coordinador accede a estadísticas THEN el Sistema SHALL mostrar el total de delitos por gravedad (leve, media, grave, muy_grave)
5. WHEN un coordinador accede a estadísticas THEN el Sistema SHALL mostrar el número de delitos denunciados formalmente
6. WHEN un coordinador accede a estadísticas THEN el Sistema SHALL filtrar los datos según su jurisdicción (puesto, municipio o departamento)
7. WHEN un auditor o super_admin accede a estadísticas THEN el Sistema SHALL mostrar datos de todo el sistema sin filtros de jurisdicción

### Requirement 12: Exportación de Evidencia

**User Story:** Como auditor electoral, quiero exportar reportes con toda su evidencia para presentar ante autoridades, para facilitar procesos legales.

#### Acceptance Criteria

1. WHEN un auditor selecciona exportar un delito THEN el Sistema SHALL generar un archivo PDF con toda la información del delito incluyendo evidencia fotográfica
2. WHEN el Sistema genera un PDF de exportación THEN el Sistema SHALL incluir título, descripción, tipo de delito, gravedad, fecha, ubicación, testigos y todas las fotos de evidencia
3. WHEN el Sistema genera un PDF de exportación THEN el Sistema SHALL incluir el historial completo de seguimiento con todas las acciones realizadas
4. WHEN el Sistema genera un PDF de exportación THEN el Sistema SHALL incluir información de denuncia formal si existe (número, autoridad, fecha)
5. WHEN un auditor exporta múltiples delitos THEN el Sistema SHALL generar un archivo ZIP con un PDF por cada delito
6. WHEN un coordinador intenta exportar un delito THEN el Sistema SHALL permitir la exportación solo si el delito está en su jurisdicción
7. WHEN se exporta un reporte THEN el Sistema SHALL registrar la exportación en el seguimiento con usuario y fecha

