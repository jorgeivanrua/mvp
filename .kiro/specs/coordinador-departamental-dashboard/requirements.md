# Requirements Document - Dashboard Coordinador Departamental

## Introduction

El Dashboard del Coordinador Departamental es una interfaz web que permite a los coordinadores departamentales supervisar todos los municipios de su departamento, consolidar resultados a nivel departamental, y generar reportes oficiales. El sistema proporciona una vista de alto nivel del proceso electoral departamental con capacidad de drill-down a municipios y puestos específicos.

## Glossary

- **Sistema**: El sistema de recolección de datos electorales
- **Coordinador Departamental**: Usuario con rol `coordinador_departamental` responsable de supervisar todos los municipios de un departamento
- **Coordinador Municipal**: Usuario responsable de supervisar todos los puestos de un municipio
- **Consolidado Departamental**: Suma total de votos de todos los municipios del departamento
- **Municipio**: División administrativa que agrupa múltiples puestos de votación
- **Departamento**: División administrativa de primer nivel en Colombia
- **Dashboard**: Interfaz principal del coordinador departamental
- **Drill-down**: Capacidad de navegar desde vista general a detalles específicos
- **Cobertura**: Porcentaje de municipios que han completado el reporte

## Requirements

### Requirement 1: Visualización de Municipios del Departamento

**User Story:** Como coordinador departamental, quiero ver todos los municipios de mi departamento con su estado de reporte, para supervisar el progreso electoral a nivel departamental.

#### Acceptance Criteria

1. WHEN el Coordinador Departamental accede al Dashboard, THE Sistema SHALL mostrar una lista de todos los municipios del departamento asignado
2. THE Sistema SHALL mostrar para cada municipio: código, nombre, total de puestos, puestos reportados, coordinador asignado, y estado general
3. THE Sistema SHALL calcular y mostrar el porcentaje de cobertura departamental (municipios completos / total de municipios)
4. THE Sistema SHALL resaltar visualmente los municipios con problemas o retrasos significativos
5. THE Sistema SHALL actualizar la lista de municipios cada 60 segundos sin recargar la página

### Requirement 2: Consolidado Departamental

**User Story:** Como coordinador departamental, quiero ver los resultados consolidados de todo mi departamento, para tener una visión general de los resultados electorales.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un panel con el consolidado de votos de todos los municipios del departamento
2. THE Sistema SHALL mostrar votos por partido sumando todos los municipios con datos validados
3. THE Sistema SHALL mostrar un gráfico de barras con la distribución de votos por partido a nivel departamental
4. THE Sistema SHALL mostrar el total de votantes registrados, votos emitidos, y porcentaje de participación departamental
5. THE Sistema SHALL actualizar el consolidado automáticamente cuando un municipio completa su reporte
6. THE Sistema SHALL mostrar solo datos de formularios en estado "validado"

### Requirement 3: Drill-down a Municipio y Puesto

**User Story:** Como coordinador departamental, quiero navegar desde la vista departamental hasta municipios y puestos específicos, para investigar detalles cuando sea necesario.

#### Acceptance Criteria

1. WHEN el Coordinador Departamental selecciona un municipio, THE Sistema SHALL mostrar el dashboard completo de ese municipio
2. THE Sistema SHALL permitir navegar desde un municipio a un puesto específico
3. THE Sistema SHALL mantener visible un breadcrumb (Departamento > Municipio > Puesto) para facilitar la navegación
4. THE Sistema SHALL permitir regresar a la vista departamental desde cualquier nivel
5. THE Sistema SHALL recordar la ruta de navegación durante la sesión

### Requirement 4: Mapa Geográfico de Resultados

**User Story:** Como coordinador departamental, quiero ver un mapa del departamento con resultados por municipio, para identificar visualmente patrones geográficos.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un mapa del departamento con los municipios coloreados según el partido ganador
2. WHEN el Coordinador Departamental hace clic en un municipio del mapa, THE Sistema SHALL mostrar los detalles de ese municipio
3. THE Sistema SHALL mostrar en el mapa el porcentaje de avance de cada municipio mediante intensidad de color
4. THE Sistema SHALL permitir alternar entre vista de mapa y vista de lista
5. THE Sistema SHALL actualizar el mapa en tiempo real cuando se actualizan datos

### Requirement 5: Comparación entre Municipios

**User Story:** Como coordinador departamental, quiero comparar resultados entre diferentes municipios, para identificar patrones o anomalías a nivel departamental.

#### Acceptance Criteria

1. THE Sistema SHALL permitir seleccionar múltiples municipios para comparación
2. THE Sistema SHALL mostrar un gráfico comparativo de votos por partido entre los municipios seleccionados
3. THE Sistema SHALL mostrar una tabla comparativa con estadísticas clave de cada municipio
4. THE Sistema SHALL calcular y mostrar la desviación estándar de participación entre municipios
5. THE Sistema SHALL resaltar municipios con resultados significativamente diferentes al promedio departamental

### Requirement 6: Identificación de Anomalías Departamentales

**User Story:** Como coordinador departamental, quiero identificar municipios con anomalías o discrepancias, para poder investigar y tomar acciones correctivas.

#### Acceptance Criteria

1. THE Sistema SHALL calcular y mostrar discrepancias entre votantes registrados y votos emitidos por municipio
2. THE Sistema SHALL alertar cuando un municipio tiene una participación anormalmente alta (> 95%) o baja (< 30%)
3. THE Sistema SHALL identificar municipios con alta tasa de rechazo de formularios (> 15%)
4. THE Sistema SHALL mostrar un indicador visual en municipios con anomalías
5. THE Sistema SHALL generar un reporte de anomalías con recomendaciones de acción

### Requirement 7: Generación de Reporte Departamental

**User Story:** Como coordinador departamental, quiero generar el reporte consolidado oficial del departamento, para reportar los resultados a nivel nacional.

#### Acceptance Criteria

1. THE Sistema SHALL proporcionar un botón para generar el reporte departamental oficial
2. WHEN el Coordinador Departamental solicita el reporte, THE Sistema SHALL validar que al menos el 90% de los municipios tengan datos completos
3. THE Sistema SHALL generar un documento PDF con el formato oficial del reporte departamental
4. THE Sistema SHALL incluir en el reporte: datos del departamento, votos por partido consolidados, total de municipios, firma digital del coordinador
5. THE Sistema SHALL registrar la fecha y hora de generación del reporte
6. THE Sistema SHALL permitir regenerar el reporte si se actualizan datos

### Requirement 8: Comunicación con Coordinadores Municipales

**User Story:** Como coordinador departamental, quiero ver la información de contacto de los coordinadores municipales, para poder comunicarme con ellos cuando sea necesario.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar el nombre y teléfono del coordinador asignado a cada municipio
2. WHEN el Coordinador Departamental selecciona un municipio, THE Sistema SHALL mostrar la información completa del coordinador municipal
3. THE Sistema SHALL mostrar la última vez que cada coordinador municipal accedió al sistema
4. THE Sistema SHALL permitir al coordinador departamental enviar notificaciones a coordinadores municipales específicos
5. THE Sistema SHALL resaltar municipios donde el coordinador no ha accedido en las últimas 4 horas

### Requirement 9: Estadísticas y Métricas Departamentales

**User Story:** Como coordinador departamental, quiero ver estadísticas detalladas del proceso electoral departamental, para monitorear el desempeño general.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar el total de municipios, puestos, mesas, y votantes registrados del departamento
2. THE Sistema SHALL mostrar el número de formularios E-14 en cada estado a nivel departamental
3. THE Sistema SHALL calcular y mostrar el tiempo promedio de validación de formularios por municipio
4. THE Sistema SHALL mostrar la tasa de rechazo de formularios por municipio
5. THE Sistema SHALL mostrar un gráfico de línea de tiempo con el progreso de recolección de datos durante el día

### Requirement 10: Ranking de Municipios

**User Story:** Como coordinador departamental, quiero ver un ranking de municipios por diferentes métricas, para identificar los de mejor y peor desempeño.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un ranking de municipios por porcentaje de avance
2. THE Sistema SHALL mostrar un ranking de municipios por tasa de participación electoral
3. THE Sistema SHALL mostrar un ranking de municipios por tiempo promedio de validación
4. THE Sistema SHALL mostrar un ranking de municipios por tasa de rechazo de formularios
5. THE Sistema SHALL permitir al coordinador ordenar el ranking por cualquier métrica

### Requirement 11: Exportación de Datos Departamentales

**User Story:** Como coordinador departamental, quiero exportar los datos consolidados departamentales, para análisis externo y reportes oficiales.

#### Acceptance Criteria

1. THE Sistema SHALL permitir exportar el consolidado departamental en formato CSV
2. THE Sistema SHALL permitir exportar el consolidado departamental en formato Excel (XLSX)
3. THE Sistema SHALL permitir exportar la lista de municipios con sus estadísticas en formato CSV
4. THE Sistema SHALL incluir en las exportaciones: fecha de generación, nombre del coordinador, y timestamp
5. THE Sistema SHALL registrar cada exportación en el log de auditoría

### Requirement 12: Panel de Control en Tiempo Real

**User Story:** Como coordinador departamental, quiero ver métricas en tiempo real del proceso electoral, para tomar decisiones informadas rápidamente.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un panel con métricas clave actualizadas en tiempo real
2. THE Sistema SHALL mostrar el número de formularios validados en la última hora
3. THE Sistema SHALL mostrar el número de municipios que han completado su reporte
4. THE Sistema SHALL mostrar alertas activas que requieren atención
5. THE Sistema SHALL actualizar las métricas cada 30 segundos automáticamente

### Requirement 13: Interfaz Responsive

**User Story:** Como coordinador departamental, quiero acceder al dashboard desde diferentes dispositivos, para poder supervisar el proceso desde cualquier lugar.

#### Acceptance Criteria

1. THE Sistema SHALL adaptar la interfaz del dashboard para pantallas de 768px o menos
2. THE Sistema SHALL mantener todas las funcionalidades principales en dispositivos móviles
3. THE Sistema SHALL optimizar mapas y gráficos para visualización en pantallas pequeñas
4. THE Sistema SHALL permitir zoom en mapas y datos en dispositivos móviles
5. THE Sistema SHALL cargar datos de forma eficiente para conexiones móviles

### Requirement 14: Seguridad y Control de Acceso

**User Story:** Como coordinador departamental, quiero que solo yo pueda ver los datos de mi departamento, para mantener la confidencialidad del proceso.

#### Acceptance Criteria

1. THE Sistema SHALL verificar que el usuario tiene rol `coordinador_departamental` antes de mostrar el dashboard
2. THE Sistema SHALL mostrar solo datos de municipios del departamento asignado al coordinador
3. THE Sistema SHALL registrar en logs todas las acciones de visualización y exportación
4. THE Sistema SHALL cerrar la sesión automáticamente después de 30 minutos de inactividad
5. THE Sistema SHALL requerir autenticación nuevamente para acciones críticas como generar reportes oficiales

### Requirement 15: Notificaciones y Alertas Departamentales

**User Story:** Como coordinador departamental, quiero recibir notificaciones sobre eventos importantes a nivel departamental, para poder actuar rápidamente.

#### Acceptance Criteria

1. WHEN un municipio completa su reporte, THE Sistema SHALL mostrar una notificación al coordinador departamental
2. WHEN se detecta una anomalía significativa en un municipio, THE Sistema SHALL generar una alerta prioritaria
3. THE Sistema SHALL mostrar un contador de municipios pendientes de completar
4. THE Sistema SHALL resaltar municipios que no han reportado avances en las últimas 4 horas
5. THE Sistema SHALL permitir al coordinador configurar alertas personalizadas por tipo de evento
