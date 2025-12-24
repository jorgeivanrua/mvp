# Requirements Document - Sistema de Incidentes y Delitos Electorales

## Introduction

El Sistema de Incidentes y Delitos Electorales es un componente crítico del sistema electoral que permite reportar, gestionar y hacer seguimiento de irregularidades y violaciones durante el proceso electoral. Incluye reporte de incidentes menores, delitos graves, sistema de escalamiento automático, notificaciones a coordinadores, y herramientas de análisis y seguimiento. El sistema garantiza la transparencia y trazabilidad de todos los eventos que afecten la integridad del proceso electoral.

## Glossary

- **Sistema**: El sistema de recolección de datos electorales
- **Incidente Electoral**: Irregularidad o problema menor en el proceso electoral que no constituye delito
- **Delito Electoral**: Violación grave de la ley electoral que puede tener consecuencias penales
- **Testigo Electoral**: Usuario con rol `testigo_electoral` que puede reportar incidentes y delitos
- **Coordinador**: Usuario con rol coordinador que recibe y gestiona reportes
- **Reporte**: Documento formal que describe un incidente o delito electoral
- **Escalamiento**: Proceso de notificar a niveles superiores sobre eventos críticos
- **Seguimiento**: Monitoreo del estado y resolución de reportes
- **Evidencia**: Fotografías, documentos o testimonios que respaldan un reporte
- **Severidad**: Nivel de gravedad de un incidente (Baja, Media, Alta, Crítica)
- **Estado del Reporte**: Situación actual del reporte (Pendiente, En Revisión, Resuelto, Cerrado)
- **Tipo de Incidente**: Categoría específica de irregularidad electoral
- **Tipo de Delito**: Categoría específica de violación electoral grave
- **Notificación Automática**: Alerta enviada automáticamente a coordinadores
- **Dashboard de Seguimiento**: Interfaz para monitorear todos los reportes activos

## Requirements

### Requirement 1: Reporte de Incidentes Electorales

**User Story:** Como testigo electoral, quiero reportar incidentes electorales menores, para documentar irregularidades que afecten el proceso sin constituir delitos.

#### Acceptance Criteria

1. THE Sistema SHALL permitir al testigo seleccionar el tipo de incidente de una lista predefinida de 15 tipos
2. THE Sistema SHALL permitir al testigo ingresar una descripción detallada del incidente
3. THE Sistema SHALL capturar automáticamente la fecha, hora, y ubicación (puesto/mesa) del reporte
4. THE Sistema SHALL permitir al testigo adjuntar hasta 3 fotografías como evidencia
5. THE Sistema SHALL asignar automáticamente un número único de reporte
6. THE Sistema SHALL establecer la severidad inicial como "Media" para todos los incidentes
7. THE Sistema SHALL guardar el reporte localmente si no hay conexión y sincronizar cuando se restaure
8. THE Sistema SHALL mostrar confirmación al testigo cuando el reporte se envíe exitosamente

### Requirement 2: Tipos de Incidentes Electorales

**User Story:** Como sistema, quiero categorizar incidentes electorales en tipos específicos, para facilitar el análisis y seguimiento estadístico.

#### Acceptance Criteria

1. THE Sistema SHALL proporcionar los siguientes 15 tipos de incidentes predefinidos:
   - Retraso en apertura de mesa
   - Falta de material electoral
   - Problemas con urna o elementos
   - Ausencia de jurado de votación
   - Problemas de identificación de votantes
   - Alteración del orden público menor
   - Falla en sistemas tecnológicos
   - Problemas de accesibilidad
   - Irregularidades en conteo preliminar
   - Presencia de propaganda irregular
   - Problemas con representantes de partidos
   - Dificultades logísticas
   - Problemas climáticos o ambientales
   - Otros incidentes menores
   - Incidente no clasificado
2. THE Sistema SHALL permitir al super admin agregar, editar o desactivar tipos de incidentes
3. THE Sistema SHALL mantener estadísticas por tipo de incidente
4. THE Sistema SHALL validar que cada reporte tenga un tipo de incidente asignado

### Requirement 3: Reporte de Delitos Electorales

**User Story:** Como testigo electoral, quiero reportar delitos electorales graves, para documentar violaciones que requieran intervención legal inmediata.

#### Acceptance Criteria

1. THE Sistema SHALL permitir al testigo seleccionar el tipo de delito de una lista predefinida de 10 tipos
2. THE Sistema SHALL requerir descripción detallada obligatoria para reportes de delitos
3. THE Sistema SHALL capturar automáticamente la fecha, hora, y ubicación del reporte
4. THE Sistema SHALL permitir al testigo adjuntar hasta 5 fotografías como evidencia para delitos
5. THE Sistema SHALL asignar automáticamente severidad "Alta" o "Crítica" según el tipo de delito
6. THE Sistema SHALL generar alerta inmediata a coordinadores para todos los delitos reportados
7. THE Sistema SHALL requerir confirmación adicional del testigo antes de enviar reporte de delito
8. THE Sistema SHALL crear número de reporte con prefijo "DEL-" para identificar delitos

### Requirement 4: Tipos de Delitos Electorales

**User Story:** Como sistema, quiero categorizar delitos electorales en tipos específicos, para facilitar el escalamiento y respuesta apropiada.

#### Acceptance Criteria

1. THE Sistema SHALL proporcionar los siguientes 10 tipos de delitos predefinidos:
   - Compra y venta de votos
   - Coacción o intimidación a votantes
   - Suplantación de identidad electoral
   - Alteración o destrucción de material electoral
   - Fraude en el conteo de votos
   - Violencia física en centro de votación
   - Amenazas a funcionarios electorales
   - Propaganda electoral prohibida
   - Acceso no autorizado a sistemas electorales
   - Otros delitos electorales graves
2. THE Sistema SHALL asignar automáticamente nivel de severidad por tipo de delito:
   - Compra de votos, Coacción, Fraude: Severidad "Crítica"
   - Suplantación, Alteración material, Violencia: Severidad "Alta"
   - Amenazas, Propaganda prohibida, Acceso no autorizado: Severidad "Alta"
   - Otros delitos: Severidad "Alta"
3. THE Sistema SHALL permitir al super admin configurar niveles de severidad por tipo
4. THE Sistema SHALL mantener estadísticas detalladas por tipo de delito

### Requirement 5: Sistema de Severidad y Escalamiento

**User Story:** Como coordinador, quiero que el sistema escale automáticamente reportes según su severidad, para priorizar la atención de eventos críticos.

#### Acceptance Criteria

1. THE Sistema SHALL clasificar todos los reportes en 4 niveles de severidad: Baja, Media, Alta, Crítica
2. WHEN se reporta un delito de severidad "Crítica", THE Sistema SHALL notificar inmediatamente a coordinador puesto, municipal y departamental
3. WHEN se reporta un delito de severidad "Alta", THE Sistema SHALL notificar a coordinador puesto y municipal
4. WHEN se reporta un incidente de severidad "Media", THE Sistema SHALL notificar solo a coordinador puesto
5. WHEN se reporta un incidente de severidad "Baja", THE Sistema SHALL registrar sin notificación automática
6. THE Sistema SHALL permitir al coordinador cambiar manualmente el nivel de severidad con justificación
7. THE Sistema SHALL registrar todos los cambios de severidad en el historial del reporte

### Requirement 6: Gestión de Estados de Reportes

**User Story:** Como coordinador, quiero gestionar el estado de los reportes, para hacer seguimiento del progreso de resolución.

#### Acceptance Criteria

1. THE Sistema SHALL manejar los siguientes estados de reportes:
   - Pendiente: Recién creado, esperando revisión
   - En Revisión: Coordinador está investigando
   - En Proceso: Se están tomando acciones correctivas
   - Resuelto: Problema solucionado, esperando confirmación
   - Cerrado: Caso completamente finalizado
   - Rechazado: Reporte inválido o duplicado
2. THE Sistema SHALL permitir al coordinador cambiar el estado con comentarios obligatorios
3. THE Sistema SHALL notificar al testigo reportante cuando cambie el estado de su reporte
4. THE Sistema SHALL registrar timestamp y usuario responsable de cada cambio de estado
5. THE Sistema SHALL calcular tiempo promedio de resolución por tipo de reporte
6. THE Sistema SHALL mostrar reportes pendientes con prioridad en dashboard de coordinador

### Requirement 7: Adjuntar Evidencias Fotográficas

**User Story:** Como testigo electoral, quiero adjuntar fotografías como evidencia, para respaldar mis reportes con pruebas visuales.

#### Acceptance Criteria

1. THE Sistema SHALL permitir adjuntar hasta 3 fotografías para incidentes y hasta 5 para delitos
2. THE Sistema SHALL aceptar formatos de imagen: JPG, JPEG, PNG, WEBP
3. THE Sistema SHALL limitar el tamaño máximo de cada imagen a 5MB
4. THE Sistema SHALL comprimir automáticamente imágenes mayores a 2MB manteniendo calidad legible
5. THE Sistema SHALL generar thumbnails de 150x150px para vista previa
6. THE Sistema SHALL almacenar imágenes con nombres únicos usando UUID
7. THE Sistema SHALL permitir al testigo eliminar fotografías antes de enviar el reporte
8. THE Sistema SHALL mostrar progreso de subida para cada imagen

### Requirement 8: Notificaciones Automáticas a Coordinadores

**User Story:** Como coordinador, quiero recibir notificaciones automáticas de reportes, para responder rápidamente a incidentes y delitos.

#### Acceptance Criteria

1. WHEN se reporta un delito, THE Sistema SHALL enviar notificación inmediata por email y en dashboard
2. WHEN se reporta un incidente de severidad alta, THE Sistema SHALL enviar notificación en dashboard
3. THE Sistema SHALL incluir en la notificación: tipo, severidad, ubicación, descripción resumida, y número de reporte
4. THE Sistema SHALL mostrar notificaciones no leídas con badge numérico en dashboard
5. THE Sistema SHALL permitir al coordinador marcar notificaciones como leídas
6. THE Sistema SHALL mantener historial de notificaciones por 30 días
7. THE Sistema SHALL agrupar notificaciones similares para evitar spam

### Requirement 9: Dashboard de Seguimiento para Coordinadores

**User Story:** Como coordinador, quiero un dashboard de seguimiento de reportes, para monitorear y gestionar todos los incidentes y delitos de mi jurisdicción.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar tabla de reportes con filtros por estado, tipo, severidad, y fecha
2. THE Sistema SHALL mostrar estadísticas resumidas: total reportes, por estado, por tipo, tiempo promedio resolución
3. THE Sistema SHALL permitir al coordinador ver detalles completos de cualquier reporte
4. THE Sistema SHALL permitir al coordinador cambiar estado y agregar comentarios de seguimiento
5. THE Sistema SHALL mostrar reportes críticos y pendientes con prioridad visual
6. THE Sistema SHALL actualizar dashboard automáticamente cada 30 segundos
7. THE Sistema SHALL permitir al coordinador exportar reportes en formato CSV o PDF

### Requirement 10: Comentarios y Seguimiento de Reportes

**User Story:** Como coordinador, quiero agregar comentarios de seguimiento a reportes, para documentar acciones tomadas y comunicar progreso.

#### Acceptance Criteria

1. THE Sistema SHALL permitir al coordinador agregar comentarios ilimitados a cualquier reporte
2. THE Sistema SHALL requerir comentario obligatorio al cambiar estado de reporte
3. THE Sistema SHALL mostrar historial cronológico de comentarios con autor y timestamp
4. THE Sistema SHALL permitir al coordinador marcar comentarios como "Visibles para testigo" o "Internos"
5. THE Sistema SHALL notificar al testigo cuando se agreguen comentarios visibles
6. THE Sistema SHALL permitir al testigo responder a comentarios del coordinador
7. THE Sistema SHALL mantener thread de conversación entre testigo y coordinador

### Requirement 11: Búsqueda y Filtrado de Reportes

**User Story:** Como coordinador, quiero buscar y filtrar reportes, para encontrar rápidamente casos específicos o analizar patrones.

#### Acceptance Criteria

1. THE Sistema SHALL permitir búsqueda por número de reporte, descripción, o nombre del testigo
2. THE Sistema SHALL permitir filtrar por tipo de reporte (incidente/delito), tipo específico, severidad, y estado
3. THE Sistema SHALL permitir filtrar por rango de fechas y ubicación (puesto/mesa)
4. THE Sistema SHALL permitir filtrar por testigo reportante o coordinador asignado
5. THE Sistema SHALL mostrar resultados de búsqueda con paginación
6. THE Sistema SHALL permitir guardar filtros frecuentes como "vistas personalizadas"
7. THE Sistema SHALL mostrar contador de resultados para cada filtro aplicado

### Requirement 12: Reportes Estadísticos y Análisis

**User Story:** Como coordinador departamental, quiero reportes estadísticos de incidentes y delitos, para analizar patrones y tomar decisiones informadas.

#### Acceptance Criteria

1. THE Sistema SHALL generar reportes estadísticos por período (día, semana, mes)
2. THE Sistema SHALL mostrar gráficos de incidentes y delitos por tipo y severidad
3. THE Sistema SHALL mostrar tendencias temporales de reportes (gráfico de líneas)
4. THE Sistema SHALL mostrar distribución geográfica de reportes (mapa de calor)
5. THE Sistema SHALL calcular métricas: tiempo promedio de resolución, tasa de resolución, reportes por testigo
6. THE Sistema SHALL permitir comparar estadísticas entre períodos diferentes
7. THE Sistema SHALL permitir exportar reportes estadísticos en formato PDF con gráficos

### Requirement 13: Integración con Dashboard de Testigo

**User Story:** Como testigo electoral, quiero acceder fácilmente al reporte de incidentes desde mi dashboard, para reportar eventos rápidamente cuando ocurran.

#### Acceptance Criteria

1. THE Sistema SHALL mostrar botones prominentes "Reportar Incidente" y "Reportar Delito" en dashboard de testigo
2. THE Sistema SHALL mostrar el historial de reportes del testigo con estados actuales
3. THE Sistema SHALL permitir al testigo ver detalles y seguimiento de sus reportes
4. THE Sistema SHALL mostrar notificaciones cuando coordinadores respondan a reportes del testigo
5. THE Sistema SHALL permitir al testigo agregar información adicional a reportes existentes
6. THE Sistema SHALL mostrar estadísticas personales: total reportes, resueltos, pendientes
7. THE Sistema SHALL funcionar offline y sincronizar reportes cuando se restaure conexión

### Requirement 14: Validación y Prevención de Duplicados

**User Story:** Como sistema, quiero validar reportes y prevenir duplicados, para mantener la calidad e integridad de los datos.

#### Acceptance Criteria

1. THE Sistema SHALL detectar posibles reportes duplicados basado en tipo, ubicación, y tiempo (dentro de 30 minutos)
2. WHEN se detecta posible duplicado, THE Sistema SHALL mostrar alerta al testigo con reportes similares
3. THE Sistema SHALL permitir al testigo confirmar que no es duplicado o cancelar el reporte
4. THE Sistema SHALL validar que la descripción tenga mínimo 20 caracteres para incidentes y 50 para delitos
5. THE Sistema SHALL validar que se seleccione un tipo válido de incidente o delito
6. THE Sistema SHALL rechazar reportes con contenido ofensivo o inapropiado usando filtros automáticos
7. THE Sistema SHALL permitir al coordinador marcar reportes como duplicados y vincularlos al original

### Requirement 15: Auditoría y Trazabilidad

**User Story:** Como auditor, quiero trazabilidad completa de todos los reportes, para garantizar transparencia y accountability del proceso.

#### Acceptance Criteria

1. THE Sistema SHALL registrar en log de auditoría: creación, modificación, y eliminación de reportes
2. THE Sistema SHALL registrar todos los cambios de estado con usuario responsable y timestamp
3. THE Sistema SHALL registrar todos los accesos a reportes con detalles del usuario
4. THE Sistema SHALL mantener historial inmutable de versiones de cada reporte
5. THE Sistema SHALL permitir al auditor ver timeline completo de cualquier reporte
6. THE Sistema SHALL registrar intentos de acceso no autorizado a reportes
7. THE Sistema SHALL generar reportes de auditoría con todas las acciones por período

### Requirement 16: Configuración del Sistema de Reportes

**User Story:** Como super admin, quiero configurar parámetros del sistema de reportes, para ajustar el comportamiento según necesidades operativas.

#### Acceptance Criteria

1. WHERE el usuario tiene rol de Super Admin, THE Sistema SHALL permitir configurar tipos de incidentes y delitos
2. THE Sistema SHALL permitir configurar niveles de severidad y reglas de escalamiento
3. THE Sistema SHALL permitir configurar plantillas de notificaciones por email
4. THE Sistema SHALL permitir configurar límites de archivos adjuntos (cantidad y tamaño)
5. THE Sistema SHALL permitir configurar tiempo de retención de reportes y evidencias
6. THE Sistema SHALL permitir configurar filtros de contenido inapropiado
7. THE Sistema SHALL aplicar cambios de configuración inmediatamente sin reinicio

### Requirement 17: Exportación y Respaldo de Reportes

**User Story:** Como coordinador departamental, quiero exportar reportes para análisis externo, para compartir información con autoridades competentes.

#### Acceptance Criteria

1. THE Sistema SHALL permitir exportar reportes individuales en formato PDF con todas las evidencias
2. THE Sistema SHALL permitir exportar lotes de reportes en formato CSV con filtros aplicados
3. THE Sistema SHALL incluir en exportaciones: metadatos completos, historial de estados, y comentarios
4. THE Sistema SHALL generar archivos ZIP con reportes PDF y evidencias fotográficas organizadas
5. THE Sistema SHALL permitir programar exportaciones automáticas periódicas
6. THE Sistema SHALL registrar todas las exportaciones en log de auditoría
7. THE Sistema SHALL permitir al super admin crear respaldos completos del sistema de reportes

### Requirement 18: Acceso Móvil Optimizado

**User Story:** Como testigo electoral, quiero reportar incidentes desde mi dispositivo móvil, para documentar eventos inmediatamente cuando ocurran.

#### Acceptance Criteria

1. THE Sistema SHALL optimizar la interfaz de reportes para pantallas móviles (320px+)
2. THE Sistema SHALL permitir capturar fotografías directamente desde la cámara del dispositivo
3. THE Sistema SHALL funcionar correctamente en navegadores móviles (Chrome, Safari, Firefox)
4. THE Sistema SHALL optimizar la subida de imágenes para conexiones móviles lentas
5. THE Sistema SHALL mostrar progreso de envío de reportes con indicadores visuales claros
6. THE Sistema SHALL funcionar offline en móviles y sincronizar cuando haya conexión
7. THE Sistema SHALL adaptar formularios para entrada táctil con validación en tiempo real

### Requirement 19: Seguridad y Privacidad de Reportes

**User Story:** Como testigo electoral, quiero que mis reportes sean seguros y confidenciales, para proteger mi identidad y la integridad de la información.

#### Acceptance Criteria

1. THE Sistema SHALL encriptar todos los reportes antes de almacenarlos en la base de datos
2. THE Sistema SHALL limitar el acceso a reportes según jerarquía: testigo ve solo sus reportes, coordinadores ven su jurisdicción
3. THE Sistema SHALL registrar todos los accesos a reportes en log de auditoría
4. THE Sistema SHALL permitir reportes anónimos para casos sensibles (solo para delitos)
5. THE Sistema SHALL proteger la identidad del testigo en reportes anónimos
6. THE Sistema SHALL usar HTTPS para todas las comunicaciones de reportes
7. THE Sistema SHALL eliminar automáticamente evidencias fotográficas después de período de retención configurado

### Requirement 20: Integración con Otros Módulos del Sistema

**User Story:** Como coordinador, quiero que el sistema de reportes se integre con otros módulos, para tener una vista completa del proceso electoral.

#### Acceptance Criteria

1. THE Sistema SHALL vincular reportes con formularios E-14 de la misma mesa cuando sea relevante
2. THE Sistema SHALL mostrar reportes relacionados en el dashboard de validación de formularios
3. THE Sistema SHALL integrar con sistema de geolocalización para validar ubicación de reportes
4. THE Sistema SHALL notificar sobre reportes cuando coordinadores revisen formularios de mesas afectadas
5. THE Sistema SHALL incluir estadísticas de reportes en dashboard general de coordinadores
6. THE Sistema SHALL permitir crear reportes desde el módulo de validación de formularios
7. THE Sistema SHALL sincronizar estados de reportes con otros módulos relevantes