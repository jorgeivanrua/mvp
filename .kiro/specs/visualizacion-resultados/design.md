# Design Document: Visualización de Resultados Electorales

## Overview

Este diseño implementa un sistema completo de visualización de resultados electorales con agregación jerárquica, filtros avanzados y actualización en tiempo real. El sistema permite a coordinadores de diferentes niveles ver resultados agregados de su jurisdicción con capacidades de análisis y exportación.

## Architecture

### Backend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Flask Application                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Resultados  │  │  Agregación  │  │  Estadísticas│     │
│  │   Routes     │  │   Service    │  │   Service    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│  ┌──────▼──────────────────▼──────────────────▼───────┐    │
│  │              Service Layer                          │    │
│  │  - ResultadosService                                │    │
│  │  - AgregacionService                                │    │
│  │  - EstadisticasService                              │    │
│  │  - ExportacionService                               │    │
│  └──────┬──────────────────────────────────────────────┘    │
│         │                                                    │
│  ┌──────▼──────────────────────────────────────────────┐    │
│  │              Data Access Layer                       │    │
│  │  - FormularioE14 Model                              │    │
│  │  - VotoPartido Model                                │    │
│  │  - VotoCandidato Model                              │    │
│  │  - PartidoPolitico Model                            │    │
│  │  - Candidato Model                                  │    │
│  └──────┬──────────────────────────────────────────────┘    │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
    ┌─────▼─────┐
    │ PostgreSQL │
    └───────────┘
```

### Frontend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Dashboard de Resultados                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Filtros y Controles                        │   │
│  │  [Tipo Elección] [Búsqueda] [Filtros Estado]        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Estadísticas Generales                     │   │
│  │  Total Votos | Participación | Progreso Reporte     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────────────┐    │
│  │  Resultados por    │  │  Resultados por            │    │
│  │  Partido           │  │  Candidato                 │    │
│  │  - Gráfico Barras  │  │  - Lista con fotos         │    │
│  │  - Tabla Votos     │  │  - Porcentajes             │    │
│  └────────────────────┘  └────────────────────────────┘    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Desglose Geográfico                        │   │
│  │  - Mapa con resultados por ubicación                 │   │
│  │  - Tabla con desglose detallado                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Backend Services

#### ResultadosService
```python
class ResultadosService:
    @staticmethod
    def obtener_resultados_por_nivel(user, tipo_eleccion_id, filtros=None):
        """
        Obtiene resultados agregados según nivel del usuario
        
        Args:
            user: Usuario actual
            tipo_eleccion_id: ID del tipo de elección
            filtros: Dict con filtros opcionales
            
        Returns:
            Dict con resultados agregados
        """
        
    @staticmethod
    def obtener_resultados_por_partido(user, tipo_eleccion_id):
        """Obtiene votos agregados por partido"""
        
    @staticmethod
    def obtener_resultados_por_candidato(user, tipo_eleccion_id):
        """Obtiene votos agregados por candidato"""
        
    @staticmethod
    def obtener_desglose_geografico(user, tipo_eleccion_id):
        """Obtiene desglose de resultados por ubicación"""
```

#### AgregacionService
```python
class AgregacionService:
    @staticmethod
    def agregar_votos_puesto(puesto_id, tipo_eleccion_id):
        """Agrega votos de todas las mesas de un puesto"""
        
    @staticmethod
    def agregar_votos_municipio(municipio_codigo, tipo_eleccion_id):
        """Agrega votos de todos los puestos de un municipio"""
        
    @staticmethod
    def agregar_votos_departamento(departamento_codigo, tipo_eleccion_id):
        """Agrega votos de todos los municipios de un departamento"""
        
    @staticmethod
    def agregar_votos_nacional(tipo_eleccion_id):
        """Agrega votos de todo el país"""
```

#### EstadisticasService
```python
class EstadisticasService:
    @staticmethod
    def calcular_estadisticas_generales(resultados):
        """
        Calcula estadísticas generales
        
        Returns:
            {
                'total_votos_validos': int,
                'total_votos_nulos': int,
                'total_votos_blancos': int,
                'porcentaje_participacion': float,
                'mesas_reportadas': int,
                'mesas_totales': int,
                'progreso_reporte': float
            }
        """
        
    @staticmethod
    def calcular_porcentajes_partido(votos_partidos):
        """Calcula porcentajes por partido"""
        
    @staticmethod
    def calcular_porcentajes_candidato(votos_candidatos):
        """Calcula porcentajes por candidato"""
```

### Backend Routes

#### Resultados Routes (`/api/resultados`)
- `GET /api/resultados/general` - Obtener resultados generales según nivel de usuario
- `GET /api/resultados/partidos` - Obtener resultados por partido
- `GET /api/resultados/candidatos` - Obtener resultados por candidato
- `GET /api/resultados/desglose` - Obtener desglose geográfico
- `GET /api/resultados/estadisticas` - Obtener estadísticas agregadas
- `GET /api/resultados/historico` - Obtener histórico de actualizaciones
- `POST /api/resultados/exportar` - Exportar resultados en formato especificado

### Frontend Components

#### ResultadosVisualizacion.js
```javascript
class ResultadosVisualizacion {
    constructor(containerId, options) {
        this.containerId = containerId;
        this.tipoEleccionActual = null;
        this.filtrosActivos = {
            completados: false,
            enProgreso: false,
            pendientes: false
        };
        this.options = options;
    }
    
    async init() {
        // Inicializar componente
    }
    
    async cargarResultados(tipoEleccionId) {
        // Cargar resultados del tipo de elección
    }
    
    async cargarResultadosPartidos() {
        // Cargar y mostrar resultados por partido
    }
    
    async cargarResultadosCandidatos() {
        // Cargar y mostrar resultados por candidato
    }
    
    async cargarDesgloseGeografico() {
        // Cargar desglose por ubicación
    }
    
    renderGraficoPartidos(datos) {
        // Renderizar gráfico de barras/pastel
    }
    
    renderTablaCandidatos(datos) {
        // Renderizar tabla de candidatos
    }
    
    renderMapaResultados(datos) {
        // Renderizar mapa con resultados
    }
    
    aplicarFiltros() {
        // Aplicar filtros de estado
    }
    
    buscarUbicacion(termino) {
        // Buscar ubicación específica
    }
    
    exportarResultados(formato) {
        // Exportar resultados en formato especificado
    }
    
    actualizarAutomaticamente() {
        // Actualizar resultados en tiempo real
    }
}
```

## Data Models

### API Response Formats

#### Resultados Generales Response
```json
{
  "success": true,
  "data": {
    "tipo_eleccion": {
      "id": 1,
      "nombre": "Presidencial",
      "nivel": "nacional"
    },
    "estadisticas": {
      "total_votos_validos": 1500000,
      "total_votos_nulos": 50000,
      "total_votos_blancos": 25000,
      "porcentaje_participacion": 75.5,
      "mesas_reportadas": 850,
      "mesas_totales": 1000,
      "progreso_reporte": 85.0
    },
    "ultima_actualizacion": "2024-12-05T14:30:00Z"
  }
}
```

#### Resultados por Partido Response
```json
{
  "success": true,
  "data": {
    "partidos": [
      {
        "partido_id": 1,
        "nombre": "Partido A",
        "sigla": "PA",
        "color": "#FF0000",
        "logo_url": "/uploads/partidos/logo_pa.png",
        "total_votos": 600000,
        "porcentaje": 40.0,
        "posicion": 1
      },
      {
        "partido_id": 2,
        "nombre": "Partido B",
        "sigla": "PB",
        "color": "#00FF00",
        "logo_url": "/uploads/partidos/logo_pb.png",
        "total_votos": 450000,
        "porcentaje": 30.0,
        "posicion": 2
      }
    ],
    "total_votos": 1500000
  }
}
```

#### Resultados por Candidato Response
```json
{
  "success": true,
  "data": {
    "candidatos": [
      {
        "candidato_id": 1,
        "nombre_completo": "Juan Pérez",
        "partido": {
          "id": 1,
          "nombre": "Partido A",
          "sigla": "PA",
          "color": "#FF0000"
        },
        "cargo": "Presidente",
        "foto_url": "/uploads/candidatos/foto_1.jpg",
        "total_votos": 600000,
        "porcentaje": 40.0,
        "posicion": 1
      }
    ],
    "total_votos": 1500000
  }
}
```

#### Desglose Geográfico Response
```json
{
  "success": true,
  "data": {
    "nivel": "municipal",
    "ubicaciones": [
      {
        "codigo": "P001",
        "nombre": "Puesto Central",
        "latitud": -17.3935,
        "longitud": -66.1570,
        "mesas_reportadas": 10,
        "mesas_totales": 10,
        "progreso": 100.0,
        "resultados_partidos": [
          {
            "partido_id": 1,
            "total_votos": 3500,
            "porcentaje": 45.0
          }
        ],
        "total_votos": 7800
      }
    ]
  }
}
```

## Correctness Properties

### Aggregation Properties

Property 41: Vote aggregation is accurate
*For any* set of E-14 forms, the aggregated vote totals should equal the sum of individual form votes
**Validates: Requirements 1.5**

Property 42: Hierarchical aggregation is consistent
*For any* hierarchical level, aggregated votes should match the sum of votes from child levels
**Validates: Requirements 1.1, 1.2, 1.3, 1.4**

Property 43: Percentage calculations are correct
*For any* set of votes, calculated percentages should sum to 100% (excluding nulls and blanks)
**Validates: Requirements 3.2, 4.4**

### Filter Properties

Property 44: Election type filter shows only matching results
*For any* election type selected, only results for that type should be displayed
**Validates: Requirements 2.2**

Property 45: Progress filters use AND logic
*For any* combination of progress filters, only locations matching all active filters should be shown
**Validates: Requirements 6.4**

Property 46: Search returns matching locations
*For any* valid location code or name, search should return all matching locations
**Validates: Requirements 7.1, 7.2, 7.3**

### Real-time Update Properties

Property 47: New forms trigger result updates
*For any* new validated E-14 form, results should update automatically within configured interval
**Validates: Requirements 11.1**

Property 48: Updates preserve user context
*For any* automatic update, active filters and view state should be maintained
**Validates: Requirements 11.4**

## Implementation Plan

### Phase 1: Backend - Aggregation Service
1. Implement AgregacionService with hierarchical aggregation
2. Implement caching strategy for aggregated results
3. Add database indexes for performance
4. Write property tests for aggregation accuracy

### Phase 2: Backend - Results Routes
1. Implement GET /api/resultados/general endpoint
2. Implement GET /api/resultados/partidos endpoint
3. Implement GET /api/resultados/candidatos endpoint
4. Implement GET /api/resultados/desglose endpoint
5. Add permission checks based on user level

### Phase 3: Frontend - Results Visualization Component
1. Create ResultadosVisualizacion.js class
2. Implement data loading methods
3. Implement Chart.js integration for graphs
4. Implement table rendering for detailed results
5. Implement map integration for geographic breakdown

### Phase 4: Frontend - Filters and Search
1. Add election type selector
2. Add progress filters (completed, in progress, pending)
3. Add location search functionality
4. Implement filter application logic
5. Add clear filters button

### Phase 5: Real-time Updates
1. Implement WebSocket connection for live updates
2. Add update notification UI
3. Implement automatic refresh logic
4. Add connection status indicator
5. Handle reconnection scenarios

### Phase 6: Export Functionality
1. Implement Excel export with openpyxl
2. Implement PDF export with ReportLab
3. Implement CSV export
4. Add export button UI
5. Add download progress indicator

### Phase 7: Testing and Optimization
1. Write property-based tests for all aggregation logic
2. Write integration tests for end-to-end flows
3. Optimize database queries with proper indexes
4. Implement result caching with Redis
5. Load testing with large datasets

## Performance Considerations

### Database Optimization
- Create materialized views for common aggregations
- Add composite indexes on (tipo_eleccion_id, ubicacion)
- Implement query result caching (5 minute TTL)
- Use database-level aggregation functions
- Partition large tables by election type

### Frontend Optimization
- Lazy load detailed results on demand
- Implement virtual scrolling for large lists
- Cache chart renderings
- Debounce search input (300ms)
- Use Web Workers for heavy calculations

### Caching Strategy
- Cache aggregated results: 5 minutes
- Cache party/candidate lists: 10 minutes
- Cache geographic breakdown: 3 minutes
- Invalidate on new validated forms
- Use Redis for distributed caching

## Security Considerations

### Authorization
- Verify user level before returning results
- Filter results based on user jurisdiction
- Prevent access to other jurisdictions
- Log all result access attempts
- Rate limit API requests

### Data Integrity
- Validate all aggregation calculations
- Detect and flag anomalies in vote counts
- Audit trail for result modifications
- Prevent manipulation of aggregated data
- Verify form validation status before aggregation

