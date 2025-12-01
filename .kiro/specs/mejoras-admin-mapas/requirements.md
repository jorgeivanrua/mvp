# Requirements Document: Mejoras Admin y Mapas

## Introduction

Este documento especifica las mejoras necesarias para el dashboard de Super Admin y la visualización de mapas en el sistema electoral. El objetivo es mejorar la organización de la configuración del sistema y asegurar que todos los roles puedan visualizar los puestos de votación en los mapas.

## Glossary

- **Super Admin**: Usuario con permisos completos sobre el sistema
- **Puesto de Votación**: Ubicación física donde se realiza la votación
- **Mesa Electoral**: Unidad de votación dentro de un puesto
- **Partido Político**: Organización política que participa en las elecciones
- **Candidato**: Persona que se postula para un cargo electoral
- **Mapa Geolocalizado**: Visualización geográfica de puestos y usuarios

## Requirements

### Requirement 1: Visualización de Puestos en Mapas

**User Story:** Como usuario del sistema (cualquier rol), quiero ver todos los puestos de votación en el mapa, para tener una visión geográfica completa del proceso electoral.

#### Acceptance Criteria

1. WHEN un usuario accede a cualquier dashboard con mapa THEN el sistema SHALL mostrar todos los puestos de votación geolocalizados
2. WHEN un puesto tiene coordenadas GPS válidas THEN el sistema SHALL mostrar un marcador en el mapa
3. WHEN un usuario hace clic en un marcador de puesto THEN el sistema SHALL mostrar información detallada del puesto
4. WHEN hay incidentes o delitos en un puesto THEN el sistema SHALL mostrar indicadores visuales en el marcador
5. WHEN un puesto no tiene coordenadas GPS THEN el sistema SHALL registrar esto en logs pero no mostrar error al usuario

### Requirement 2: Reorganización de Configuración en Super Admin

**User Story:** Como Super Admin, quiero tener la configuración del sistema organizada en pestañas específicas, para gestionar eficientemente todos los aspectos del sistema electoral.

#### Acceptance Criteria

1. WHEN accedo a la pestaña de Configuración THEN el sistema SHALL mostrar sub-pestañas para diferentes categorías
2. WHEN selecciono la sub-pestaña "Partidos Políticos" THEN el sistema SHALL mostrar la gestión de partidos
3. WHEN selecciono la sub-pestaña "Candidatos" THEN el sistema SHALL mostrar la gestión de candidatos
4. WHEN selecciono la sub-pestaña "Tipos de Elección" THEN el sistema SHALL mostrar la gestión de tipos de elección
5. WHEN selecciono la sub-pestaña "Sistema" THEN el sistema SHALL mostrar configuraciones generales del sistema

### Requirement 3: Gestión de Partidos Políticos

**User Story:** Como Super Admin, quiero gestionar los partidos políticos participantes, para mantener actualizada la información electoral.

#### Acceptance Criteria

1. WHEN accedo a gestión de partidos THEN el sistema SHALL mostrar lista de todos los partidos registrados
2. WHEN creo un nuevo partido THEN el sistema SHALL solicitar nombre, sigla, color y logo
3. WHEN edito un partido THEN el sistema SHALL permitir modificar todos sus datos
4. WHEN elimino un partido THEN el sistema SHALL verificar que no tenga candidatos asociados
5. WHEN subo un logo de partido THEN el sistema SHALL validar formato y tamaño de imagen

### Requirement 4: Gestión de Candidatos

**User Story:** Como Super Admin, quiero gestionar los candidatos de las elecciones, para mantener actualizada la información de postulantes.

#### Acceptance Criteria

1. WHEN accedo a gestión de candidatos THEN el sistema SHALL mostrar lista de todos los candidatos registrados
2. WHEN creo un nuevo candidato THEN el sistema SHALL solicitar nombre, partido, tipo de elección y cargo
3. WHEN edito un candidato THEN el sistema SHALL permitir modificar todos sus datos
4. WHEN elimino un candidato THEN el sistema SHALL verificar que no tenga votos registrados
5. WHEN asocio un candidato a un partido THEN el sistema SHALL validar que el partido exista

### Requirement 5: Gestión de Tipos de Elección

**User Story:** Como Super Admin, quiero gestionar los tipos de elección, para configurar correctamente el proceso electoral.

#### Acceptance Criteria

1. WHEN accedo a gestión de tipos de elección THEN el sistema SHALL mostrar lista de todos los tipos configurados
2. WHEN creo un nuevo tipo de elección THEN el sistema SHALL solicitar nombre, descripción y nivel
3. WHEN edito un tipo de elección THEN el sistema SHALL permitir modificar sus datos
4. WHEN elimino un tipo de elección THEN el sistema SHALL verificar que no tenga formularios E-14 asociados
5. WHEN activo/desactivo un tipo de elección THEN el sistema SHALL reflejar el cambio en los formularios

### Requirement 6: Indicadores Visuales en Mapas

**User Story:** Como usuario del sistema, quiero ver indicadores visuales en los puestos del mapa, para identificar rápidamente situaciones que requieren atención.

#### Acceptance Criteria

1. WHEN un puesto tiene incidentes críticos THEN el sistema SHALL mostrar un indicador rojo pulsante
2. WHEN un puesto tiene delitos reportados THEN el sistema SHALL mostrar un indicador naranja
3. WHEN un puesto tiene formularios pendientes THEN el sistema SHALL mostrar un indicador amarillo
4. WHEN un puesto está completamente reportado THEN el sistema SHALL mostrar un indicador verde
5. WHEN hago clic en un indicador THEN el sistema SHALL mostrar detalles de incidentes/delitos/formularios

### Requirement 7: Filtros de Mapa

**User Story:** Como usuario del sistema, quiero filtrar la visualización del mapa, para enfocarme en información específica.

#### Acceptance Criteria

1. WHEN activo filtro "Solo con incidentes" THEN el sistema SHALL mostrar únicamente puestos con incidentes
2. WHEN activo filtro "Solo con delitos" THEN el sistema SHALL mostrar únicamente puestos con delitos
3. WHEN activo filtro "Pendientes de reporte" THEN el sistema SHALL mostrar únicamente puestos sin formularios
4. WHEN desactivo todos los filtros THEN el sistema SHALL mostrar todos los puestos
5. WHEN aplico múltiples filtros THEN el sistema SHALL aplicar lógica AND entre filtros

### Requirement 8: Configuración General del Sistema

**User Story:** Como Super Admin, quiero configurar parámetros generales del sistema, para personalizar el comportamiento de la aplicación.

#### Acceptance Criteria

1. WHEN accedo a configuración general THEN el sistema SHALL mostrar parámetros configurables
2. WHEN modifico el nombre del sistema THEN el sistema SHALL actualizar el título en todas las páginas
3. WHEN modifico el logo del sistema THEN el sistema SHALL actualizar el logo en navbar
4. WHEN configuro zona horaria THEN el sistema SHALL usar esa zona para todas las fechas
5. WHEN guardo cambios de configuración THEN el sistema SHALL aplicarlos inmediatamente

### Requirement 9: Búsqueda en Mapa

**User Story:** Como usuario del sistema, quiero buscar puestos específicos en el mapa, para localizarlos rápidamente.

#### Acceptance Criteria

1. WHEN ingreso un código de puesto THEN el sistema SHALL centrar el mapa en ese puesto
2. WHEN ingreso un nombre de municipio THEN el sistema SHALL mostrar todos los puestos de ese municipio
3. WHEN ingreso un código de mesa THEN el sistema SHALL mostrar el puesto que contiene esa mesa
4. WHEN no se encuentra el puesto buscado THEN el sistema SHALL mostrar mensaje informativo
5. WHEN encuentro un puesto THEN el sistema SHALL resaltar su marcador temporalmente

### Requirement 10: Exportación de Datos de Configuración

**User Story:** Como Super Admin, quiero exportar la configuración del sistema, para crear respaldos o migrar a otro ambiente.

#### Acceptance Criteria

1. WHEN solicito exportar partidos THEN el sistema SHALL generar archivo JSON con todos los partidos
2. WHEN solicito exportar candidatos THEN el sistema SHALL generar archivo JSON con todos los candidatos
3. WHEN solicito exportar tipos de elección THEN el sistema SHALL generar archivo JSON con los tipos
4. WHEN solicito exportar configuración completa THEN el sistema SHALL generar archivo con toda la configuración
5. WHEN importo un archivo de configuración THEN el sistema SHALL validar formato y aplicar cambios
