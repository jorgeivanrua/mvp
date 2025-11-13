# Design Document - Dashboard Coordinador Departamental

## Overview

El Dashboard del Coordinador Departamental permite supervisar todos los municipios de un departamento, consolidar resultados electorales a nivel departamental, y generar reportes oficiales. El diseño reutiliza extensamente la arquitectura del Dashboard Municipal, adaptándola para operar a nivel departamental (departamento → municipios en lugar de municipio → puestos).

### Objetivos del Diseño

1. Proporcionar vista consolidada de todos los municipios del departamento
2. Permitir drill-down desde departamento → municipio → puesto
3. Detectar anomalías a nivel departamental
4. Generar reportes departamentales oficiales
5. Facilitar comunicación con coordinadores municipales
6. Reutilizar máximo código del dashboard municipal

### Principios de Diseño

- **Máxima Reutilización**: Adaptar servicios y componentes del dashboard municipal
- **Escalabilidad**: Diseño que soporte departamentos con muchos municipios
- **Consistencia**: Interfaz similar al dashboard municipal para facilitar uso
- **Performance**: Optimización para grandes volúmenes de datos

## Architecture

El sistema reutiliza la arquitectura del dashboard municipal, operando a un nivel superior:

```
Dashboard Municipal:  Municipio → Puestos → Mesas
Dashboard Departamental: Departamento → Municipios → Puestos → Mesas
```

### Reutilización de Componentes

**Servicios Reutilizables:**
- `ConsolidadoService.calcular_consolidado_municipal()` - Para consolidados de municipios
- `MunicipalService.obtener_puestos_municipio()` - Para drill-down a municipios
- `DiscrepanciaService` - Adaptado para nivel departamental
- `E24Service` - Patrón similar para reportes departamentales

**Modelos Reutilizables:**
- Todos los modelos existentes (Location, FormularioE14, etc.)
- Nuevos modelos similares a E24Municipal pero para nivel departamental

## Components and Interfaces

### Backend Components

#### 1. Services - departamental_service.py

Nuevo servicio similar a MunicipalService pero para nivel departamental:

```python
class DepartamentalService:
    """Servicio para operaciones del coordinador departamental"""
    
    @staticmethod
    def obtener_municipios_departamento(departamento_id, filtros=None):
        """
        Obtener lista de municipios con estadísticas
        Similar a MunicipalService.obtener_puestos_municipio()
        """
        pass
    
    @staticmethod
    def calcular_consolidado_departamental(departamento_id, tipo_eleccion_id=None):
        """
        Calcular consolidado departamental
        Suma consolidados de todos los municipios
        """
        pass
    
    @staticmethod
    def comparar_municipios(municipio_ids):
        """
        Comparar estadísticas entre municipios
        Similar a MunicipalService.comparar_puestos()
        """
        pass
```

#### 2. Routes - coordinador_departamental.py

Endpoints similares al dashboard municipal:

```python
# GET /api/coordinador-departamental/municipios
# GET /api/coordinador-departamental/consolidado
# GET /api/coordinador-departamental/municipio/<id>
# GET /api/coordinador-departamental/discrepancias
# POST /api/coordinador-departamental/reporte-departamental
# GET /api/coordinador-departamental/comparacion
# GET /api/coordinador-departamental/estadisticas
# POST /api/coordinador-departamental/notificar
# GET /api/coordinador-departamental/exportar
```

#### 3. Models - Reporte Departamental

```python
class ReporteDepartamental(db.Model):
    """Reporte consolidado departamental"""
    __tablename__ = 'reportes_departamentales'
    
    id = db.Column(db.Integer, primary_key=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    coordinador_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'))
    
    # Datos consolidados
    total_municipios = db.Column(db.Integer)
    municipios_incluidos = db.Column(db.Integer)
    total_puestos = db.Column(db.Integer)
    total_mesas = db.Column(db.Integer)
    total_votantes_registrados = db.Column(db.Integer)
    total_votos = db.Column(db.Integer)
    votos_validos = db.Column(db.Integer)
    votos_nulos = db.Column(db.Integer)
    votos_blanco = db.Column(db.Integer)
    
    # Archivo PDF
    pdf_url = db.Column(db.String(500))
    pdf_hash = db.Column(db.String(64))
    version = db.Column(db.Integer, default=1)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Frontend Components

El frontend será prácticamente idéntico al dashboard municipal, solo cambiando:
- "Puestos" → "Municipios"
- "Coordinador de Puesto" → "Coordinador Municipal"
- "E-24 Municipal" → "Reporte Departamental"

## Implementation Strategy

### Fase 1: Reutilización Máxima
1. Copiar y adaptar `municipal_service.py` → `departamental_service.py`
2. Copiar y adaptar `coordinador_municipal.py` routes → `coordinador_departamental.py`
3. Crear modelo `ReporteDepartamental` basado en `FormularioE24Municipal`

### Fase 2: Frontend
1. Copiar `municipal.html` → `departamental.html`
2. Copiar `coordinador-municipal.js` → `coordinador-departamental.js`
3. Buscar y reemplazar terminología

### Fase 3: Integración
1. Registrar blueprint
2. Agregar ruta frontend
3. Testing

## Testing Strategy

Reutilizar tests del dashboard municipal adaptándolos para nivel departamental.

## Security Considerations

Idénticas al dashboard municipal, validando que el coordinador solo acceda a su departamento asignado.

## Performance Optimization

- Índices similares al dashboard municipal
- Caching de consolidados departamentales
- Paginación para departamentos con muchos municipios

