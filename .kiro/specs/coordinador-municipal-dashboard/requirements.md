# Requirements Document - Dashboard Coordinador Municipal

## Introduction

El Dashboard del Coordinador Municipal es una interfaz web que permite a los coordinadores municipales supervisar, consolidar y generar reportes de todos los puestos de votación dentro de su municipio. El sistema proporciona una vista consolidada de los resultados electorales, permite identificar puestos con problemas, y facilita la generación del formulario E-24 (consolidado municipal).

## Glossary

- **Sistema**: El sistema de recolección de datos electorales
- **Coordinador Municipal**: Usuario con rol `coordinador_municipal` responsable de supervisar todos los puestos de un municipio
- **Coordinador de Puesto**: Usuario responsable de validar formularios E-14 de un puesto específico
- **Formulario E-14**: Documento que registra votos por mesa electoral
- **Formulario E-24**: Documento que consolida votos de todas las mesas de un puesto
- **Consolidado Municipal**: Suma total de votos de todos los puestos de un municipio
- **Puesto de Votación**: Ubicación física donde se agrupan múltiples mesas electorales
- **Dashboard**: Interfaz principal del coordinador municipal
- **Discrepancia**: Diferencia significativa entre datos esperados y reportados
- **Cobertura**: Porcentaje de puestos que han completado el reporte

## Requirements

### Requirement 1: Visualización de Puestos del Municipio

**User Story:** Como coordinador municipal, quiero ver todos los puestos de votación de mi municipio con su estado de reporte, para supervisar el progreso de la recolección de datos.

#### Acceptance Criteria

1. WHEN el Coordinador Municipal accede al Dashboard, THE Sistema SHALL mostrar una lista de todos los puestos de votación del municipio asignado
2. THE Sistema SHALL mostrar para cada puesto: código, nombre, total de mesas, mesas reportadas, coordinador asignado, y estado general
3. THE Sistema SHALL calcular y mostrar el porcentaje de cobertura (puestos con datos completos / total de puestos)
4. THE Sistema SHALL resaltar visualmente los puestos con problemas o retrasos significativos
5. THE Sistema SHALL actualizar la lista de puestos cada 60 segundos sin recargar la página

### Requirement 2: Visualización de Consolidado Municipal

**User Story:** Como coordinador municipal, quiero ver los resultados consolidados de todo mi municipio, para tener una visión general de los resultados electorales.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un panel con el consolidado de votos de todos los puestos validados del municipio
2. THE Sistema SHALL mostrar votos por partido sumando todos los puestos con formularios validados
3. THE Sistema SHALL mostrar un gráfico de barras con la distribución de votos por partido a nivel municipal
4. THE Sistema SHALL mostrar el total de votantes registrados, votos emitidos, y porcentaje de participación
5. THE Sistema SHALL actualizar el consolidado automáticamente cuando un puesto completa su reporte
6. THE Sistema SHALL mostrar solo datos de formularios en estado "validado"

### Requirement 3: Detalle de Puesto Individual

**User Story:** Como coordinador municipal, quiero ver el detalle de un puesto específico, para revisar sus formularios y estadísticas.

#### Acceptance Criteria

1. WHEN el Coordinador Municipal selecciona un puesto, THE Sistema SHALL mostrar todos los formularios E-14 validados de ese puesto
2. THE Sistema SHALL mostrar el consolidado de votos del puesto seleccionado
3. THE Sistema SHALL mostrar la lista de mesas del puesto con su estado de reporte
4. THE Sistema SHALL mostrar el coordinador de puesto asignado y su información de contacto
5. THE Sistema SHALL permitir al coordinador municipal ver la imagen de cualquier formulario E-14 del puesto

### Requirement 4: Identificación de Discrepancias

**User Story:** Como coordinador municipal, quiero identificar puestos con discrepancias o anomalías, para poder investigar y corregir problemas.

#### Acceptance Criteria

1. THE Sistema SHALL calcular y mostrar discrepancias entre votantes registrados y votos emitidos por puesto
2. THE Sistema SHALL alertar cuando un puesto tiene una participación anormalmente alta (> 95%) o baja (< 30%)
3. THE Sistema SHALL identificar puestos donde la suma de votos por partido no coincide con el total de votos válidos
4. THE Sistema SHALL mostrar un indicador visual (badge) en puestos con discrepancias significativas
5. THE Sistema SHALL permitir filtrar la lista de puestos para mostrar solo aquellos con discrepancias

### Requirement 5: Generación de Formulario E-24 Municipal

**User Story:** Como coordinador municipal, quiero generar el formulario E-24 consolidado de mi municipio, para reportar oficialmente los resultados.

#### Acceptance Criteria

1. THE Sistema SHALL proporcionar un botón para generar el formulario E-24 Municipal del municipio
2. WHEN el Coordinador Municipal solicita el E-24 Municipal, THE Sistema SHALL validar que al menos el 80% de los puestos tengan datos completos
3. THE Sistema SHALL generar un documento PDF con el formato oficial del E-24 Municipal
4. THE Sistema SHALL incluir en el E-24 Municipal: datos del municipio, votos por partido consolidados, total de mesas, firma digital del coordinador
5. THE Sistema SHALL registrar la fecha y hora de generación del E-24 Municipal
6. THE Sistema SHALL permitir regenerar el E-24 Municipal si se actualizan datos después de la primera generación

**Nota:** El E-24 Municipal consolida todos los E-24 de Puesto del municipio.

### Requirement 6: Comunicación con Coordinadores de Puesto

**User Story:** Como coordinador municipal, quiero ver la información de contacto de los coordinadores de puesto, para poder comunicarme con ellos cuando sea necesario.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar el nombre y teléfono del coordinador asignado a cada puesto
2. WHEN el Coordinador Municipal selecciona un puesto, THE Sistema SHALL mostrar la información completa del coordinador de puesto
3. THE Sistema SHALL mostrar la última vez que el coordinador de puesto accedió al sistema
4. THE Sistema SHALL permitir al coordinador municipal enviar notificaciones a coordinadores de puesto específicos
5. THE Sistema SHALL resaltar puestos donde el coordinador no ha accedido en las últimas 2 horas

### Requirement 7: Filtrado y Búsqueda de Puestos

**User Story:** Como coordinador municipal, quiero filtrar y buscar puestos, para encontrar rápidamente información específica.

#### Acceptance Criteria

1. THE Sistema SHALL permitir filtrar puestos por estado (completo, incompleto, con discrepancias)
2. THE Sistema SHALL permitir buscar puestos por código o nombre
3. THE Sistema SHALL permitir filtrar puestos por zona electoral
4. THE Sistema SHALL permitir ordenar puestos por nombre, código, o porcentaje de avance
5. THE Sistema SHALL mantener los filtros aplicados durante la sesión del usuario

### Requirement 8: Estadísticas y Métricas

**User Story:** Como coordinador municipal, quiero ver estadísticas detalladas del proceso electoral, para monitorear el desempeño general.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar el total de puestos, mesas, y votantes registrados del municipio
2. THE Sistema SHALL mostrar el número de formularios E-14 en cada estado (pendiente, validado, rechazado)
3. THE Sistema SHALL calcular y mostrar el tiempo promedio de validación de formularios por puesto
4. THE Sistema SHALL mostrar la tasa de rechazo de formularios por puesto
5. THE Sistema SHALL mostrar un gráfico de línea de tiempo con el progreso de recolección de datos durante el día

### Requirement 9: Exportación de Datos

**User Story:** Como coordinador municipal, quiero exportar los datos consolidados, para análisis externo y reportes oficiales.

#### Acceptance Criteria

1. THE Sistema SHALL permitir exportar el consolidado municipal en formato CSV
2. THE Sistema SHALL permitir exportar el consolidado municipal en formato Excel (XLSX)
3. THE Sistema SHALL permitir exportar la lista de puestos con sus estadísticas en formato CSV
4. THE Sistema SHALL incluir en las exportaciones: fecha de generación, nombre del coordinador, y timestamp
5. THE Sistema SHALL registrar cada exportación en el log de auditoría

### Requirement 10: Interfaz Responsive

**User Story:** Como coordinador municipal, quiero acceder al dashboard desde diferentes dispositivos, para poder supervisar el proceso desde cualquier lugar.

#### Acceptance Criteria

1. THE Sistema SHALL adaptar la interfaz del dashboard para pantallas de 768px o menos
2. THE Sistema SHALL mantener todas las funcionalidades principales en dispositivos móviles
3. THE Sistema SHALL optimizar gráficos y tablas para visualización en pantallas pequeñas
4. THE Sistema SHALL permitir zoom en gráficos y datos en dispositivos móviles
5. THE Sistema SHALL cargar datos de forma eficiente para conexiones móviles

### Requirement 11: Seguridad y Control de Acceso

**User Story:** Como coordinador municipal, quiero que solo yo pueda ver los datos de mi municipio, para mantener la confidencialidad del proceso.

#### Acceptance Criteria

1. THE Sistema SHALL verificar que el usuario tiene rol `coordinador_municipal` antes de mostrar el dashboard
2. THE Sistema SHALL mostrar solo datos de puestos del municipio asignado al coordinador
3. THE Sistema SHALL registrar en logs todas las acciones de visualización y exportación
4. THE Sistema SHALL cerrar la sesión automáticamente después de 30 minutos de inactividad
5. THE Sistema SHALL requerir autenticación nuevamente para acciones críticas como generar E-24

### Requirement 12: Notificaciones y Alertas

**User Story:** Como coordinador municipal, quiero recibir notificaciones sobre eventos importantes, para poder actuar rápidamente.

#### Acceptance Criteria

1. WHEN un puesto completa su reporte, THE Sistema SHALL mostrar una notificación al coordinador municipal
2. WHEN se detecta una discrepancia significativa en un puesto, THE Sistema SHALL generar una alerta
3. THE Sistema SHALL mostrar un contador de puestos pendientes de completar
4. THE Sistema SHALL resaltar puestos que no han reportado en las últimas 3 horas
5. THE Sistema SHALL permitir al coordinador configurar alertas personalizadas

### Requirement 13: Comparación entre Puestos

**User Story:** Como coordinador municipal, quiero comparar resultados entre diferentes puestos, para identificar patrones o anomalías.

#### Acceptance Criteria

1. THE Sistema SHALL permitir seleccionar múltiples puestos para comparación
2. THE Sistema SHALL mostrar un gráfico comparativo de votos por partido entre los puestos seleccionados
3. THE Sistema SHALL mostrar una tabla comparativa con estadísticas clave de cada puesto
4. THE Sistema SHALL calcular y mostrar la desviación estándar de participación entre puestos
5. THE Sistema SHALL resaltar puestos con resultados significativamente diferentes al promedio municipal

### Requirement 14: Historial y Auditoría

**User Story:** Como coordinador municipal, quiero ver el historial de cambios a nivel municipal, para tener trazabilidad completa del proceso.

#### Acceptance Criteria

1. THE Sistema SHALL mantener un registro de todas las generaciones del formulario E-24
2. THE Sistema SHALL mostrar el historial de validaciones de formularios por puesto
3. THE Sistema SHALL registrar todas las exportaciones de datos realizadas
4. THE Sistema SHALL permitir al coordinador ver el log de accesos al sistema por coordinadores de puesto
5. THE Sistema SHALL mostrar una línea de tiempo con eventos importantes del proceso electoral

### Requirement 15: Selector de Puesto para Supervisión

**User Story:** Como coordinador municipal, quiero poder seleccionar diferentes puestos desde mi dashboard, para supervisar cada uno en detalle sin perder el contexto municipal.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un selector de puesto en el dashboard del coordinador municipal
2. WHEN el Coordinador Municipal selecciona un puesto, THE Sistema SHALL mostrar los detalles y formularios de ese puesto
3. THE Sistema SHALL mantener visible el consolidado municipal mientras se revisa un puesto específico
4. THE Sistema SHALL permitir al coordinador regresar a la vista general del municipio fácilmente
5. THE Sistema SHALL recordar el último puesto seleccionado durante la sesión
