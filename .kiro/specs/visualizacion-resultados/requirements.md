# Requirements Document: Visualización de Resultados Electorales

## Introduction

Este documento especifica los requerimientos para la visualización de resultados electorales (votos por partido y candidato) en diferentes niveles jerárquicos del sistema. Los coordinadores deben poder ver resultados agregados según su nivel de responsabilidad, con capacidades de filtrado y búsqueda similares a las del mapa de geolocalización.

## Glossary

- **Coordinador de Puesto**: Usuario responsable de un puesto de votación específico
- **Coordinador Municipal**: Usuario responsable de todos los puestos en un municipio
- **Coordinador Departamental**: Usuario responsable de todos los municipios en un departamento
- **Super Admin**: Usuario con acceso a todos los niveles y departamentos
- **Tipo de Elección**: Categoría de elección (Presidencial, Senado, Cámara, etc.)
- **Agregación**: Suma de votos de múltiples formularios E-14
- **E-14**: Formulario de acta de escrutinio por mesa
- **E-24**: Formulario de consolidación por puesto o municipio

## Requirements

### Requirement 1: Visualización de Resultados por Nivel Jerárquico

**User Story:** Como coordinador, quiero ver los resultados electorales agregados según mi nivel de responsabilidad, para monitorear el proceso electoral en mi jurisdicción.

#### Acceptance Criteria

1. WHEN un Coordinador de Puesto accede a resultados THEN el sistema SHALL mostrar votos agregados de todas las mesas de su puesto
2. WHEN un Coordinador Municipal accede a resultados THEN el sistema SHALL mostrar votos agregados de todos los puestos de su municipio
3. WHEN un Coordinador Departamental accede a resultados THEN el sistema SHALL mostrar votos agregados de todos los municipios de su departamento
4. WHEN un Super Admin accede a resultados THEN el sistema SHALL mostrar votos agregados de todo el país
5. WHEN se agregan votos THEN el sistema SHALL calcular totales, porcentajes y estadísticas correctamente

### Requirement 2: Filtros por Tipo de Elección

**User Story:** Como coordinador, quiero filtrar resultados por tipo de elección, para ver resultados específicos de cada categoría electoral.

#### Acceptance Criteria

1. WHEN accedo a visualización de resultados THEN el sistema SHALL mostrar selector de tipo de elección
2. WHEN selecciono un tipo de elección THEN el sistema SHALL mostrar solo resultados de ese tipo
3. WHEN cambio de tipo de elección THEN el sistema SHALL actualizar resultados sin recargar página
4. WHEN no hay datos para un tipo THEN el sistema SHALL mostrar mensaje informativo
5. WHEN hay múltiples tipos THEN el sistema SHALL permitir comparación entre tipos

### Requirement 3: Visualización por Partido Político

**User Story:** Como coordinador, quiero ver resultados agregados por partido político, para analizar el desempeño de cada partido.

#### Acceptance Criteria

1. WHEN veo resultados THEN el sistema SHALL mostrar votos totales por partido
2. WHEN veo resultados THEN el sistema SHALL mostrar porcentaje de votos por partido
3. WHEN veo resultados THEN el sistema SHALL mostrar gráfico de barras o pastel
4. WHEN veo resultados THEN el sistema SHALL usar colores distintivos por partido
5. WHEN veo resultados THEN el sistema SHALL ordenar partidos por cantidad de votos

### Requirement 4: Visualización por Candidato

**User Story:** Como coordinador, quiero ver resultados agregados por candidato, para analizar el desempeño individual de candidatos.

#### Acceptance Criteria

1. WHEN veo resultados de candidatos THEN el sistema SHALL mostrar votos totales por candidato
2. WHEN veo resultados de candidatos THEN el sistema SHALL mostrar partido asociado
3. WHEN veo resultados de candidatos THEN el sistema SHALL mostrar foto del candidato si existe
4. WHEN veo resultados de candidatos THEN el sistema SHALL mostrar porcentaje de votos
5. WHEN veo resultados de candidatos THEN el sistema SHALL ordenar por cantidad de votos

### Requirement 5: Desglose Geográfico

**User Story:** Como coordinador, quiero ver desglose de resultados por ubicación geográfica, para identificar patrones territoriales.

#### Acceptance Criteria

1. WHEN soy Coordinador Municipal THEN el sistema SHALL mostrar desglose por puesto
2. WHEN soy Coordinador Departamental THEN el sistema SHALL mostrar desglose por municipio
3. WHEN soy Super Admin THEN el sistema SHALL mostrar desglose por departamento
4. WHEN hago clic en una ubicación THEN el sistema SHALL mostrar detalle de esa ubicación
5. WHEN veo desglose THEN el sistema SHALL mostrar mapa con resultados por ubicación

### Requirement 6: Filtros de Progreso

**User Story:** Como coordinador, quiero filtrar ubicaciones por estado de reporte, para identificar áreas que requieren atención.

#### Acceptance Criteria

1. WHEN activo filtro "Completados" THEN el sistema SHALL mostrar solo ubicaciones con 100% de mesas reportadas
2. WHEN activo filtro "En Progreso" THEN el sistema SHALL mostrar ubicaciones con reporte parcial
3. WHEN activo filtro "Pendientes" THEN el sistema SHALL mostrar ubicaciones sin reportes
4. WHEN activo múltiples filtros THEN el sistema SHALL aplicar lógica AND
5. WHEN limpio filtros THEN el sistema SHALL mostrar todas las ubicaciones

### Requirement 7: Búsqueda de Ubicaciones

**User Story:** Como coordinador, quiero buscar ubicaciones específicas, para acceder rápidamente a sus resultados.

#### Acceptance Criteria

1. WHEN ingreso código de puesto THEN el sistema SHALL mostrar resultados de ese puesto
2. WHEN ingreso nombre de municipio THEN el sistema SHALL mostrar resultados de ese municipio
3. WHEN ingreso código de mesa THEN el sistema SHALL mostrar resultados del puesto que contiene esa mesa
4. WHEN no se encuentra ubicación THEN el sistema SHALL mostrar mensaje informativo
5. WHEN encuentro ubicación THEN el sistema SHALL resaltar en mapa y tabla

### Requirement 8: Estadísticas Agregadas

**User Story:** Como coordinador, quiero ver estadísticas agregadas de mi jurisdicción, para tener una visión general del proceso.

#### Acceptance Criteria

1. WHEN veo resultados THEN el sistema SHALL mostrar total de votos válidos
2. WHEN veo resultados THEN el sistema SHALL mostrar total de votos nulos
3. WHEN veo resultados THEN el sistema SHALL mostrar total de votos en blanco
4. WHEN veo resultados THEN el sistema SHALL mostrar porcentaje de participación
5. WHEN veo resultados THEN el sistema SHALL mostrar progreso de reporte (mesas reportadas/total)

### Requirement 9: Comparación Temporal

**User Story:** Como coordinador, quiero comparar resultados en diferentes momentos, para ver evolución del conteo.

#### Acceptance Criteria

1. WHEN veo resultados THEN el sistema SHALL mostrar timestamp de última actualización
2. WHEN veo resultados THEN el sistema SHALL permitir ver histórico de actualizaciones
3. WHEN veo histórico THEN el sistema SHALL mostrar cambios en votos por partido
4. WHEN veo histórico THEN el sistema SHALL mostrar gráfico de evolución temporal
5. WHEN hay cambios significativos THEN el sistema SHALL resaltar diferencias

### Requirement 10: Exportación de Resultados

**User Story:** Como coordinador, quiero exportar resultados, para análisis externo o respaldo.

#### Acceptance Criteria

1. WHEN solicito exportar THEN el sistema SHALL generar archivo Excel con resultados
2. WHEN solicito exportar THEN el sistema SHALL generar archivo PDF con gráficos
3. WHEN solicito exportar THEN el sistema SHALL generar archivo CSV con datos crudos
4. WHEN exporto THEN el sistema SHALL incluir filtros aplicados en nombre de archivo
5. WHEN exporto THEN el sistema SHALL incluir timestamp de generación

### Requirement 11: Actualización en Tiempo Real

**User Story:** Como coordinador, quiero que los resultados se actualicen automáticamente, para ver información actualizada sin recargar.

#### Acceptance Criteria

1. WHEN hay nuevos formularios E-14 THEN el sistema SHALL actualizar resultados automáticamente
2. WHEN hay cambios en validación THEN el sistema SHALL reflejar cambios en resultados
3. WHEN se actualiza THEN el sistema SHALL mostrar notificación de actualización
4. WHEN se actualiza THEN el sistema SHALL mantener filtros y vista actual
5. WHEN hay error de conexión THEN el sistema SHALL mostrar indicador de desconexión

### Requirement 12: Visualización Responsiva

**User Story:** Como coordinador, quiero acceder a resultados desde cualquier dispositivo, para monitorear desde campo.

#### Acceptance Criteria

1. WHEN accedo desde móvil THEN el sistema SHALL adaptar interfaz a pantalla pequeña
2. WHEN accedo desde tablet THEN el sistema SHALL optimizar disposición de gráficos
3. WHEN accedo desde desktop THEN el sistema SHALL mostrar vista completa con múltiples paneles
4. WHEN cambio orientación THEN el sistema SHALL reorganizar elementos
5. WHEN uso touch THEN el sistema SHALL responder a gestos táctiles

