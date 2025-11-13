# Requirements Document - Dashboard Coordinador de Puesto

## Introduction

El Dashboard del Coordinador de Puesto es una interfaz web que permite a los coordinadores de puesto de votación supervisar, validar y consolidar los formularios E-14 enviados por los testigos electorales de todas las mesas bajo su responsabilidad. El sistema debe proporcionar herramientas de validación, visualización de datos en tiempo real, y generación de reportes consolidados por puesto.

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

1. THE Sistema SHALL mostrar una lista de todas las mesas asignadas al puesto del coordinador
2. THE Sistema SHALL indicar para cada mesa: código, testigo asignado, estado del reporte, y última actualización
3. THE Sistema SHALL resaltar visualmente las mesas que no han enviado formularios
4. THE Sistema SHALL mostrar un indicador de progreso general (mesas reportadas vs total de mesas)
5. THE Sistema SHALL permitir al coordinador ver los detalles de contacto del testigo asignado a cada mesa

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
