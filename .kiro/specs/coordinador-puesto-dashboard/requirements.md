# Requirements Document - Dashboard Coordinador de Puesto

## Introduction

El Dashboard del Coordinador de Puesto es una interfaz web que permite a los coordinadores de puesto de votación supervisar, validar y consolidar los formularios E-14 enviados por los testigos electorales de todas las mesas bajo su responsabilidad. Además, permite monitorear y gestionar incidentes y delitos electorales reportados por los testigos. El sistema proporciona herramientas de validación, visualización de datos en tiempo real, gestión de reportes de incidentes y delitos, y generación de reportes consolidados por puesto.

## Glossary

- **Sistema**: El sistema de recolección de datos electorales
- **Coordinador de Puesto**: Usuario con rol `coordinador_puesto` responsable de supervisar todas las mesas de un puesto de votación
- **Testigo Electoral**: Usuario con rol `testigo` que registra datos del formulario E-14 de una mesa específica
- **Formulario E-14**: Documento oficial que registra los resultados de votación de una mesa electoral
- **Puesto de Votación**: Ubicación física donde se agrupan múltiples mesas electorales
- **Mesa Electoral**: Unidad básica de votación con votantes registrados específicos
- **Estado del Formulario**: Clasificación del formulario que puede ser: borrador, pendiente, validado, o rechazado
- **Validación**: Proceso de revisión y aprobación de un formulario E-14 por parte del coordinador
- **Consolidado**: Suma total de votos de todas las mesas de un puesto
- **Dashboard**: Interfaz principal del coordinador de puesto
- **Incidente Electoral**: Problema o irregularidad en el proceso electoral que no constituye un delito
- **Delito Electoral**: Violación grave de la ley electoral que debe ser escalada a autoridades
- **Severidad**: Nivel de importancia de un incidente (baja, media, alta, crítica)
- **Gravedad**: Nivel de seriedad de un delito electoral (leve, media, grave, muy grave)
- **Seguimiento**: Proceso de monitoreo y gestión de incidentes y delitos reportados
- **Escalamiento**: Acción de reportar un delito a autoridades superiores o competentes

## Requirements

### Requirement 1: Visualización de Formularios del Puesto

**User Story:** Como coordinador de puesto, quiero ver todos los formularios E-14 de las mesas de mi puesto, para poder supervisar el progreso de la recolección de datos.

#### Acceptance Criteria

1. WHEN el Coordinador de Puesto accede al Dashboard, THE Sistema SHALL mostrar una tabla con todos los formularios E-14 de las mesas asignadas a su puesto
2. THE Sistema SHALL mostrar para cada formulario: número de mesa, testigo responsable, estado, total de votos, y fecha de envío
3. THE Sistema SHALL permitir filtrar formularios por estado (todos, pendiente, validado, rechazado, borrador)
4. THE Sistema SHALL actualizar la lista de formularios cada 30 segundos sin recargar la página
5. THE Sistema SHALL mostrar un indicador visual del progreso (X de Y mesas reportadas)

### Requirement 2: Validación de Formularios E-14

**User Story:** Como coordinador de puesto, quiero revisar y validar los formularios E-14 enviados por los testigos, para asegurar la calidad y exactitud de los datos.

#### Acceptance Criteria

1. WHEN el Coordinador de Puesto selecciona un formulario pendiente, THE Sistema SHALL mostrar todos los detalles del formulario en un modal de revisión
2. THE Sistema SHALL mostrar la imagen del formulario E-14 físico junto a los datos digitados
3. THE Sistema SHALL calcular y mostrar automáticamente las validaciones: total de votos válidos, suma de votos por partido, y coherencia con votantes registrados
4. THE Sistema SHALL permitir al coordinador aprobar el formulario cambiando su estado a "validado"
5. THE Sistema SHALL permitir al coordinador rechazar el formulario con un motivo obligatorio
6. WHEN el Coordinador de Puesto rechaza un formulario, THE Sistema SHALL notificar al testigo responsable y cambiar el estado a "rechazado"
7. THE Sistema SHALL registrar la fecha, hora y usuario que realizó la validación

### Requirement 3: Edición de Formularios con Errores

**User Story:** Como coordinador de puesto, quiero poder corregir errores menores en los formularios, para evitar rechazos innecesarios y agilizar el proceso.

#### Acceptance Criteria

1. WHEN el Coordinador de Puesto identifica un error menor en un formulario pendiente, THE Sistema SHALL permitir editar los campos numéricos de votación
2. THE Sistema SHALL recalcular automáticamente los totales al modificar cualquier campo
3. THE Sistema SHALL registrar en el historial del formulario los cambios realizados y el usuario que los hizo
4. THE Sistema SHALL mantener la imagen original del formulario E-14 sin modificación
5. WHEN el Coordinador de Puesto guarda las correcciones, THE Sistema SHALL cambiar el estado del formulario a "validado"

### Requirement 4: Visualización de Datos Consolidados

**User Story:** Como coordinador de puesto, quiero ver un resumen consolidado de todos los votos de mi puesto, para tener una visión general de los resultados.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un panel de resumen con el total de votos consolidados del puesto
2. THE Sistema SHALL mostrar votos por partido sumando todas las mesas validadas
3. THE Sistema SHALL mostrar un gráfico de barras con la distribución de votos por partido
4. THE Sistema SHALL mostrar el porcentaje de participación del puesto
5. THE Sistema SHALL actualizar el consolidado automáticamente cuando se valida un nuevo formulario
6. THE Sistema SHALL mostrar solo datos de formularios en estado "validado"

### Requirement 5: Gestión de Mesas del Puesto

**User Story:** Como coordinador de puesto, quiero ver el estado de todas las mesas de mi puesto, para identificar cuáles faltan por reportar.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar una lista de todas las mesas asignadas al puesto del coordinador sincronizadas con la base de datos
2. THE Sistema SHALL indicar para cada mesa: código, testigo asignado, estado del reporte, verificación de presencia del testigo, y última actualización
3. THE Sistema SHALL resaltar visualmente las mesas que no han enviado formularios
4. THE Sistema SHALL mostrar un indicador de progreso general (mesas reportadas vs total de mesas)
5. THE Sistema SHALL permitir al coordinador ver los detalles de contacto del testigo asignado a cada mesa
6. THE Sistema SHALL mostrar un ícono de verificación cuando el testigo ha confirmado su presencia en la mesa
7. THE Sistema SHALL sincronizar la cantidad de mesas mostradas con las mesas reales del puesto en la base de datos

### Requirement 6: Generación de E-24 de Puesto

**User Story:** Como coordinador de puesto, quiero generar el E-24 de Puesto consolidado, para enviar a los coordinadores municipales.

#### Acceptance Criteria

1. THE Sistema SHALL proporcionar un botón para generar el E-24 de Puesto
2. WHEN el Coordinador de Puesto solicita el E-24 de Puesto, THE Sistema SHALL generar un documento PDF con los resultados consolidados
3. THE Sistema SHALL incluir en el E-24 de Puesto: datos del puesto, total de mesas, votos por partido, votos nulos y en blanco, y firma digital del coordinador
4. THE Sistema SHALL permitir descargar el E-24 de Puesto en formato PDF
5. THE Sistema SHALL registrar la fecha y hora de generación de cada E-24 de Puesto

**Nota:** El E-24 de Puesto consolida todos los E-14 validados del puesto. No confundir con el E-24 Municipal que consolida todos los puestos del municipio.

### Requirement 7: Notificaciones y Alertas

**User Story:** Como coordinador de puesto, quiero recibir notificaciones cuando hay nuevos formularios pendientes, para poder validarlos rápidamente.

#### Acceptance Criteria

1. WHEN un testigo envía un formulario E-14, THE Sistema SHALL mostrar una notificación visual en el dashboard del coordinador
2. THE Sistema SHALL mostrar un contador de formularios pendientes de validación
3. THE Sistema SHALL resaltar con un badge el número de formularios nuevos desde el último acceso
4. THE Sistema SHALL mostrar alertas cuando hay discrepancias significativas en los datos de un formulario
5. THE Sistema SHALL permitir al coordinador marcar notificaciones como leídas

### Requirement 8: Interfaz Responsive y Móvil

**User Story:** Como coordinador de puesto, quiero acceder al dashboard desde mi teléfono o tablet, para poder validar formularios desde cualquier lugar.

#### Acceptance Criteria

1. THE Sistema SHALL adaptar la interfaz del dashboard para pantallas de 768px o menos
2. THE Sistema SHALL mantener todas las funcionalidades principales en dispositivos móviles
3. THE Sistema SHALL optimizar el tamaño de botones y campos para interacción táctil
4. THE Sistema SHALL permitir zoom en las imágenes de formularios E-14 en dispositivos móviles
5. THE Sistema SHALL cargar datos de forma eficiente para conexiones móviles lentas

### Requirement 9: Seguridad y Control de Acceso

**User Story:** Como coordinador de puesto, quiero que solo yo pueda validar los formularios de mi puesto, para mantener la integridad del proceso.

#### Acceptance Criteria

1. THE Sistema SHALL verificar que el usuario tiene rol `coordinador_puesto` antes de mostrar el dashboard
2. THE Sistema SHALL mostrar solo formularios de las mesas del puesto asignado al coordinador
3. THE Sistema SHALL registrar en logs todas las acciones de validación y modificación
4. THE Sistema SHALL cerrar la sesión automáticamente después de 30 minutos de inactividad
5. THE Sistema SHALL requerir autenticación nuevamente para acciones críticas como validar o rechazar formularios

### Requirement 10: Historial y Auditoría

**User Story:** Como coordinador de puesto, quiero ver el historial de cambios de cada formulario, para tener trazabilidad completa del proceso.

#### Acceptance Criteria

1. THE Sistema SHALL mantener un registro de todos los cambios de estado de cada formulario
2. THE Sistema SHALL mostrar en el detalle del formulario: fecha de creación, fecha de envío, fecha de validación, y usuario responsable de cada acción
3. THE Sistema SHALL registrar las modificaciones realizadas por el coordinador con valores anteriores y nuevos
4. THE Sistema SHALL permitir al coordinador ver el historial completo de un formulario
5. THE Sistema SHALL mostrar comentarios y motivos de rechazo en el historial

### Requirement 11: Verificación de Presencia de Testigos

**User Story:** Como coordinador de puesto, quiero ver qué testigos han verificado su presencia en las mesas, para asegurar que todos los testigos estén en sus puestos asignados.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un indicador visual de presencia verificada para cada testigo en la lista de mesas
2. WHEN un testigo verifica su presencia, THE Sistema SHALL actualizar inmediatamente el estado en el dashboard del coordinador
3. THE Sistema SHALL mostrar la fecha y hora de verificación de presencia cuando el coordinador pasa el cursor sobre el indicador
4. THE Sistema SHALL resaltar las mesas cuyos testigos no han verificado su presencia
5. THE Sistema SHALL sincronizar el estado de presencia desde la base de datos cada 30 segundos
6. THE Sistema SHALL mostrar un contador de testigos presentes vs total de testigos asignados

### Requirement 12: Visualización de Incidentes del Puesto

**User Story:** Como coordinador de puesto, quiero ver todos los incidentes reportados por los testigos de mi puesto, para monitorear problemas en el proceso electoral.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de coordinador de puesto, THE Sistema SHALL mostrar una lista de todos los incidentes reportados por testigos de su puesto
2. THE Sistema SHALL mostrar para cada incidente: tipo, título, severidad, descripción, testigo que reportó, mesa, fecha y hora
3. THE Sistema SHALL usar colores distintivos según severidad: baja (verde), media (amarillo), alta (naranja), crítica (rojo)
4. THE Sistema SHALL permitir filtrar incidentes por severidad, tipo, mesa, o testigo
5. THE Sistema SHALL permitir al coordinador ver el detalle completo de cada incidente
6. THE Sistema SHALL mostrar un contador de incidentes por severidad en el dashboard
7. THE Sistema SHALL actualizar la lista de incidentes automáticamente cada 30 segundos
8. THE Sistema SHALL permitir al coordinador agregar comentarios o seguimiento a los incidentes

### Requirement 13: Visualización de Delitos Electorales del Puesto

**User Story:** Como coordinador de puesto, quiero ver todos los delitos electorales reportados por los testigos de mi puesto, para escalar a las autoridades competentes.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de coordinador de puesto, THE Sistema SHALL mostrar una lista de todos los delitos electorales reportados por testigos de su puesto
2. THE Sistema SHALL mostrar para cada delito: tipo, título, gravedad, descripción, testigos adicionales, testigo que reportó, mesa, fecha y hora
3. THE Sistema SHALL usar colores distintivos según gravedad: leve (amarillo), media (naranja), grave (rojo), muy grave (rojo oscuro)
4. THE Sistema SHALL permitir filtrar delitos por gravedad, tipo, mesa, o testigo
5. THE Sistema SHALL permitir al coordinador ver el detalle completo de cada delito
6. THE Sistema SHALL mostrar un contador de delitos por gravedad en el dashboard
7. THE Sistema SHALL actualizar la lista de delitos automáticamente cada 30 segundos
8. THE Sistema SHALL permitir al coordinador marcar delitos como escalados a autoridades
9. THE Sistema SHALL mostrar una advertencia visual prominente cuando hay delitos reportados

### Requirement 14: Gestión y Seguimiento de Reportes

**User Story:** Como coordinador de puesto, quiero gestionar el seguimiento de incidentes y delitos, para asegurar que todos sean atendidos adecuadamente.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de coordinador de puesto, THE Sistema SHALL permitir agregar comentarios de seguimiento a incidentes y delitos
2. THE Sistema SHALL permitir al coordinador cambiar el estado de incidentes (pendiente, en revisión, resuelto)
3. THE Sistema SHALL permitir al coordinador cambiar el estado de delitos (reportado, escalado, en investigación, resuelto)
4. THE Sistema SHALL registrar todos los cambios de estado con timestamp y usuario
5. THE Sistema SHALL notificar al testigo que reportó cuando el coordinador agrega un comentario
6. THE Sistema SHALL mostrar el historial completo de seguimiento de cada reporte
7. THE Sistema SHALL permitir al coordinador asignar prioridad a incidentes y delitos
8. THE Sistema SHALL generar reportes consolidados de incidentes y delitos del puesto

### Requirement 15: Alertas de Incidentes y Delitos Críticos

**User Story:** Como coordinador de puesto, quiero recibir alertas inmediatas cuando se reportan incidentes críticos o delitos, para poder responder rápidamente.

#### Acceptance Criteria

1. WHEN un testigo reporta un incidente con severidad crítica, THE Sistema SHALL mostrar una alerta visual prominente en el dashboard del coordinador
2. WHEN un testigo reporta un delito electoral, THE Sistema SHALL mostrar una alerta visual prominente en el dashboard del coordinador
3. THE Sistema SHALL reproducir un sonido de notificación cuando se recibe una alerta crítica
4. THE Sistema SHALL mostrar un contador de alertas no atendidas en el header del dashboard
5. THE Sistema SHALL permitir al coordinador marcar alertas como atendidas
6. THE Sistema SHALL mantener un historial de todas las alertas recibidas
7. THE Sistema SHALL enviar notificación por email al coordinador para delitos muy graves

### Requirement 16: Visualización de Evidencias Fotográficas de Incidentes y Delitos

**User Story:** Como coordinador de puesto, quiero ver las fotos de evidencia de los incidentes y delitos reportados, para evaluar mejor la situación y tomar decisiones informadas.

#### Acceptance Criteria

1. WHEN el Coordinador de Puesto visualiza un incidente, THE Sistema SHALL mostrar todas las fotos de evidencia asociadas en una galería responsive
2. WHEN el Coordinador de Puesto visualiza un delito, THE Sistema SHALL mostrar todas las fotos de evidencia asociadas en una galería responsive
3. THE Sistema SHALL mostrar la galería de fotos en formato grid: 2 columnas en móvil, 3 columnas en desktop
4. THE Sistema SHALL permitir hacer clic en cada foto para abrirla en tamaño completo en una nueva ventana
5. THE Sistema SHALL mostrar el nombre del archivo debajo de cada foto
6. THE Sistema SHALL cargar las fotos de forma eficiente sin bloquear la interfaz
7. THE Sistema SHALL mostrar un contador del número de evidencias fotográficas para cada incidente o delito

### Requirement 17: Visor de Imagen con Zoom para Formularios E-14

**User Story:** Como coordinador de puesto, quiero poder hacer zoom y manipular las imágenes de los formularios E-14, para poder leer con claridad todos los números y validar los datos con precisión.

#### Acceptance Criteria

1. WHEN el Coordinador de Puesto abre un formulario E-14 para validación, THE Sistema SHALL mostrar controles de zoom para la imagen del formulario
2. THE Sistema SHALL permitir hacer zoom in hasta 300% y zoom out hasta 50% con incrementos de 25%
3. THE Sistema SHALL permitir rotar la imagen en incrementos de 90 grados para corregir orientación
4. THE Sistema SHALL permitir arrastrar la imagen cuando el zoom es mayor a 100% para navegar por diferentes áreas
5. THE Sistema SHALL proporcionar un atajo de teclado (Ctrl + Rueda del mouse) para hacer zoom rápido
6. THE Sistema SHALL mostrar el porcentaje de zoom actual en el botón de reset
7. THE Sistema SHALL permitir abrir la imagen en una nueva ventana para comparación con múltiples formularios
8. THE Sistema SHALL resetear el zoom y rotación automáticamente al cerrar el modal de validación
9. THE Sistema SHALL mantener una transición suave al aplicar zoom y rotación
10. THE Sistema SHALL funcionar correctamente en dispositivos móviles con gestos táctiles
