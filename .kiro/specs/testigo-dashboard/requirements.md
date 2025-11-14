# Requirements Document - Dashboard Testigo Electoral

## Introduction

El Dashboard del Testigo Electoral es una interfaz web móvil-first diseñada para que los testigos electorales reporten datos desde las mesas de votación. Permite crear formularios E-14, reportar incidentes y delitos electorales, y verificar presencia en la mesa asignada. El sistema funciona offline con sincronización automática cuando hay conexión.

## Glossary

- **Sistema**: El sistema de recolección de datos electorales
- **Testigo Electoral**: Usuario con rol `testigo_electoral` asignado a una o más mesas de votación
- **Formulario E-14**: Formulario oficial de reporte de resultados por mesa
- **Mesa**: Ubicación específica donde se realiza la votación
- **Puesto Electoral**: Conjunto de mesas en una misma ubicación física
- **Dashboard**: Interfaz principal del testigo electoral
- **Sincronización**: Proceso de enviar datos guardados localmente al servidor
- **Borrador**: Formulario guardado localmente que no ha sido enviado
- **Incidente**: Problema o irregularidad en el proceso electoral
- **Delito Electoral**: Violación grave de la ley electoral

## Requirements

### Requirement 1: Visualización de Mesas Asignadas

**User Story:** Como testigo electoral, quiero ver todas las mesas que tengo asignadas, para saber dónde debo reportar datos.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de testigo electoral, THE Sistema SHALL mostrar todas las mesas asignadas al testigo
2. THE Sistema SHALL mostrar para cada mesa: código, puesto, número de votantes registrados
3. THE Sistema SHALL indicar visualmente qué mesas ya tienen formularios E-14 reportados
4. THE Sistema SHALL permitir al testigo seleccionar una mesa para trabajar con ella
5. THE Sistema SHALL mostrar un panel lateral con la lista de mesas y su estado

### Requirement 2: Verificación de Presencia

**User Story:** Como testigo electoral, quiero verificar mi presencia en la mesa, para registrar que estoy cumpliendo mi función.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de testigo electoral, THE Sistema SHALL mostrar un botón de "Verificar Presencia"
2. WHEN el testigo hace clic en verificar presencia, THE Sistema SHALL registrar la fecha y hora de verificación
3. THE Sistema SHALL mostrar confirmación visual de presencia verificada
4. THE Sistema SHALL notificar al coordinador de puesto sobre la verificación
5. THE Sistema SHALL permitir verificar presencia solo una vez por día

### Requirement 3: Creación de Formularios E-14

**User Story:** Como testigo electoral, quiero crear formularios E-14 para reportar los resultados de votación de mi mesa.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de testigo electoral, THE Sistema SHALL permitir crear formularios E-14 para sus mesas asignadas
2. THE Sistema SHALL permitir seleccionar el tipo de elección (presidencial, congreso, etc.)
3. THE Sistema SHALL cargar automáticamente los partidos y candidatos según el tipo de elección
4. THE Sistema SHALL permitir ingresar votos por partido y por candidato
5. THE Sistema SHALL calcular automáticamente totales: votos válidos, total votos, total tarjetas
6. THE Sistema SHALL validar que los totales sean consistentes
7. THE Sistema SHALL permitir tomar foto del formulario físico E-14
8. THE Sistema SHALL permitir agregar observaciones opcionales

### Requirement 4: Guardado de Borradores

**User Story:** Como testigo electoral, quiero guardar borradores de formularios, para poder completarlos más tarde sin perder información.

#### Acceptance Criteria

1. WHERE el usuario está creando un formulario E-14, THE Sistema SHALL permitir guardar como borrador
2. THE Sistema SHALL guardar borradores localmente en el dispositivo
3. THE Sistema SHALL permitir editar borradores guardados
4. THE Sistema SHALL mostrar borradores con badge distintivo en la lista
5. THE Sistema SHALL permitir eliminar borradores
6. THE Sistema SHALL sincronizar borradores con el servidor cuando haya conexión

### Requirement 5: Envío de Formularios para Revisión

**User Story:** Como testigo electoral, quiero enviar formularios completos para revisión, para que sean validados por el coordinador.

#### Acceptance Criteria

1. WHERE el usuario ha completado un formulario E-14, THE Sistema SHALL permitir enviarlo para revisión
2. THE Sistema SHALL validar que todos los campos requeridos estén completos antes de enviar
3. WHEN el formulario es enviado, THE Sistema SHALL cambiar su estado a "pendiente"
4. THE Sistema SHALL mostrar confirmación de envío exitoso
5. THE Sistema SHALL notificar al coordinador de puesto sobre el nuevo formulario
6. IF el envío falla por falta de conexión, THE Sistema SHALL guardar localmente y sincronizar después

### Requirement 6: Visualización de Formularios Enviados

**User Story:** Como testigo electoral, quiero ver el estado de mis formularios enviados, para saber si fueron validados o rechazados.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar una lista de todos los formularios del testigo
2. THE Sistema SHALL mostrar para cada formulario: mesa, estado, total votos, fecha
3. THE Sistema SHALL usar badges de colores para indicar estado: pendiente (azul), validado (verde), rechazado (rojo), borrador (gris)
4. THE Sistema SHALL permitir ver detalles de formularios enviados
5. THE Sistema SHALL actualizar automáticamente el estado de los formularios

### Requirement 7: Reporte de Incidentes

**User Story:** Como testigo electoral, quiero reportar incidentes en el proceso electoral, para documentar problemas que ocurran.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de testigo electoral, THE Sistema SHALL permitir reportar incidentes
2. THE Sistema SHALL permitir seleccionar el tipo de incidente de una lista predefinida
3. THE Sistema SHALL requerir título, severidad (baja/media/alta/crítica), y descripción
4. THE Sistema SHALL asociar el incidente a la mesa seleccionada
5. THE Sistema SHALL guardar incidentes localmente si no hay conexión
6. THE Sistema SHALL sincronizar incidentes automáticamente cuando haya conexión

### Requirement 8: Reporte de Delitos Electorales

**User Story:** Como testigo electoral, quiero reportar delitos electorales, para alertar a las autoridades sobre violaciones graves.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de testigo electoral, THE Sistema SHALL permitir reportar delitos electorales
2. THE Sistema SHALL mostrar advertencia sobre la gravedad de reportar delitos
3. THE Sistema SHALL permitir seleccionar el tipo de delito de una lista predefinida
4. THE Sistema SHALL requerir título, gravedad (leve/media/grave/muy grave), y descripción detallada
5. THE Sistema SHALL permitir agregar nombres de testigos adicionales opcionales
6. THE Sistema SHALL guardar delitos localmente si no hay conexión
7. THE Sistema SHALL sincronizar delitos automáticamente cuando haya conexión
8. THE Sistema SHALL notificar a coordinadores y autoridades sobre delitos reportados

### Requirement 9: Visualización de Incidentes y Delitos

**User Story:** Como testigo electoral, quiero ver los incidentes y delitos que he reportado, para hacer seguimiento.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar pestañas separadas para incidentes y delitos
2. THE Sistema SHALL mostrar para cada incidente: tipo, título, severidad, descripción, fecha, estado de sincronización
3. THE Sistema SHALL mostrar para cada delito: tipo, título, gravedad, descripción, testigos, fecha, estado de sincronización
4. THE Sistema SHALL usar colores distintivos según severidad/gravedad
5. THE Sistema SHALL indicar visualmente si están sincronizados o pendientes

### Requirement 10: Sincronización Automática

**User Story:** Como testigo electoral, quiero que mis datos se sincronicen automáticamente, para no perder información si pierdo conexión.

#### Acceptance Criteria

1. THE Sistema SHALL guardar todos los datos localmente primero
2. THE Sistema SHALL intentar sincronizar con el servidor inmediatamente
3. IF la sincronización falla, THE Sistema SHALL guardar localmente y reintentar después
4. THE Sistema SHALL sincronizar automáticamente al cargar el dashboard
5. THE Sistema SHALL sincronizar automáticamente cada 5 minutos
6. THE Sistema SHALL mostrar un indicador flotante con datos pendientes de sincronizar
7. THE Sistema SHALL permitir sincronización manual con un botón

### Requirement 11: Indicador de Sincronización

**User Story:** Como testigo electoral, quiero ver cuántos datos tengo pendientes de sincronizar, para saber si necesito buscar conexión.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un indicador flotante cuando hay datos pendientes
2. THE Sistema SHALL mostrar la cantidad total de registros pendientes
3. THE Sistema SHALL desglosar por tipo: formularios, incidentes, delitos
4. THE Sistema SHALL incluir un botón de sincronización manual en el indicador
5. THE Sistema SHALL ocultar el indicador cuando no hay datos pendientes
6. THE Sistema SHALL actualizar el indicador automáticamente cada 30 segundos

### Requirement 12: Interfaz Móvil-First

**User Story:** Como testigo electoral, quiero usar el sistema desde mi teléfono, para reportar desde la mesa de votación.

#### Acceptance Criteria

1. THE Sistema SHALL adaptar la interfaz para pantallas de 768px o menos
2. THE Sistema SHALL usar inputs optimizados para móvil (teclado numérico para números)
3. THE Sistema SHALL permitir tomar fotos directamente con la cámara del dispositivo
4. THE Sistema SHALL usar botones grandes y fáciles de tocar
5. THE Sistema SHALL minimizar el scroll necesario en formularios
6. THE Sistema SHALL funcionar correctamente en orientación vertical y horizontal

### Requirement 13: Cálculos Automáticos en Formularios

**User Story:** Como testigo electoral, quiero que el sistema calcule automáticamente los totales, para evitar errores de suma.

#### Acceptance Criteria

1. WHEN el testigo ingresa votos por partido o candidato, THE Sistema SHALL calcular automáticamente votos válidos
2. THE Sistema SHALL calcular automáticamente el total de votos sumando válidos, nulos y blancos
3. THE Sistema SHALL calcular automáticamente el total de tarjetas sumando votos y tarjetas no marcadas
4. THE Sistema SHALL mostrar el partido con más votos en la mesa
5. THE Sistema SHALL actualizar cálculos en tiempo real mientras el testigo ingresa datos
6. THE Sistema SHALL cargar automáticamente el total de votantes registrados de la mesa

### Requirement 14: Validaciones de Formularios

**User Story:** Como testigo electoral, quiero que el sistema valide mis datos, para evitar enviar formularios con errores.

#### Acceptance Criteria

1. THE Sistema SHALL validar que se haya seleccionado una mesa
2. THE Sistema SHALL validar que se haya seleccionado un tipo de elección
3. THE Sistema SHALL validar que los campos numéricos sean números válidos
4. THE Sistema SHALL validar que no haya valores negativos
5. THE Sistema SHALL mostrar mensajes de error claros cuando hay validaciones fallidas
6. THE Sistema SHALL prevenir el envío de formularios con errores de validación

### Requirement 15: Gestión de Múltiples Mesas

**User Story:** Como testigo electoral, quiero poder reportar datos de múltiples mesas, para cubrir todas mis asignaciones.

#### Acceptance Criteria

1. WHERE el testigo está asignado a múltiples mesas, THE Sistema SHALL permitir cambiar entre mesas
2. THE Sistema SHALL mostrar claramente qué mesa está seleccionada
3. THE Sistema SHALL filtrar formularios por mesa seleccionada
4. THE Sistema SHALL permitir crear formularios para cualquier mesa asignada
5. THE Sistema SHALL prevenir crear múltiples formularios E-14 para la misma mesa y tipo de elección

### Requirement 16: Instrucciones y Ayuda

**User Story:** Como testigo electoral, quiero ver instrucciones claras, para saber cómo usar el sistema correctamente.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un panel de instrucciones en el dashboard
2. THE Sistema SHALL listar los pasos para crear un formulario E-14
3. THE Sistema SHALL mostrar tooltips en campos complejos
4. THE Sistema SHALL usar iconos intuitivos para acciones comunes
5. THE Sistema SHALL mostrar mensajes de confirmación para acciones importantes

### Requirement 17: Manejo de Errores y Conexión

**User Story:** Como testigo electoral, quiero que el sistema funcione sin conexión, para poder reportar incluso sin internet.

#### Acceptance Criteria

1. THE Sistema SHALL funcionar completamente offline
2. THE Sistema SHALL guardar todos los datos en localStorage del navegador
3. THE Sistema SHALL mostrar mensajes claros cuando no hay conexión
4. THE Sistema SHALL reintentar automáticamente cuando se recupera la conexión
5. THE Sistema SHALL nunca perder datos por falta de conexión
6. THE Sistema SHALL mostrar el estado de conexión en la interfaz

### Requirement 18: Seguridad y Cierre de Sesión

**User Story:** Como testigo electoral, quiero cerrar sesión de forma segura, para proteger los datos cuando no estoy usando el sistema.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un botón de cerrar sesión visible
2. WHEN el testigo cierra sesión, THE Sistema SHALL limpiar tokens de autenticación
3. THE Sistema SHALL cerrar sesión automáticamente después de 30 minutos de inactividad
4. THE Sistema SHALL mantener datos locales no sincronizados después de cerrar sesión
5. THE Sistema SHALL requerir login nuevamente para acceder al dashboard

### Requirement 19: Tipos de Incidentes y Delitos

**User Story:** Como testigo electoral, quiero seleccionar de una lista de tipos predefinidos, para reportar incidentes y delitos de forma estandarizada.

#### Acceptance Criteria

1. THE Sistema SHALL cargar tipos de incidentes desde el servidor
2. THE Sistema SHALL cargar tipos de delitos desde el servidor
3. THE Sistema SHALL mostrar los tipos en selectores dropdown
4. THE Sistema SHALL incluir una opción "Otros" para casos no contemplados
5. THE Sistema SHALL actualizar los tipos disponibles sin requerir actualización de la app

### Requirement 20: Resumen de Mesa

**User Story:** Como testigo electoral, quiero ver un resumen de los datos de mi mesa, para verificar que todo esté correcto antes de enviar.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar un resumen automático mientras se completa el formulario
2. THE Sistema SHALL mostrar el total de votos en la mesa
3. THE Sistema SHALL mostrar el partido con más votos en la mesa
4. THE Sistema SHALL aclarar que el ganador se calcula a nivel municipal (E-24)
5. THE Sistema SHALL actualizar el resumen en tiempo real

