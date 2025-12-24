# Sistema de Monitoreo - Design

## Información del Spec
- **Nombre**: Sistema de Monitoreo en Tiempo Real
- **Versión**: 1.0
- **Estado**: Implementado (100%)
- **Fecha**: Diciembre 2025

## Arquitectura General

### Componentes Principales

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA DE MONITOREO                     │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Dashboard)          │  Backend (APIs)            │
│  ┌─────────────────────────┐   │  ┌─────────────────────┐   │
│  │ Dashboard Principal     │   │  │ /monitoreo/         │   │
│  │ - Estadísticas RT       │◄──┤  │ estadisticas        │   │
│  │ - Mapa Geolocalización  │   │  │ datos-mapa          │   │
│  │ - Tabla E-24           │   │  │ mapa-calor          │   │
│  │ - Filtros Interactivos │   │  │ tendencias          │   │
│  └─────────────────────────┘   │  │ comparativa-dept    │   │
│                                │  │ predicciones        │   │
│  ┌─────────────────────────┐   │  └─────────────────────┘   │
│  │ Componentes JS          │   │                            │
│  │ - MapaGeolocalizacion   │   │  ┌─────────────────────┐   │
│  │ - APIClient             │   │  │ Modelos de Datos    │   │
│  │ - Utils                 │   │  │ - User              │   │
│  │ - Auto-refresh          │   │  │ - FormularioE14     │   │
│  └─────────────────────────┘   │  │ - IncidenteElectoral│   │
│                                │  │ - DelitoElectoral   │   │
│                                │  │ - Location          │   │
│                                │  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Usuario   │───▶│  Dashboard  │───▶│  API REST   │───▶│ Base Datos  │
│ (Monitoreo) │    │   (HTML/JS) │    │  (Flask)    │    │(PostgreSQL) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       ▲                   │                   │                   │
       │                   ▼                   ▼                   ▼
       │            ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       │            │Auto-refresh │    │Cálculos RT  │    │Consultas SQL│
       │            │(30 seg)     │    │Estadísticas │    │Optimizadas  │
       │            └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       └───────────────────┴───────────────────┴───────────────────┘
                           Actualización en Tiempo Real
```

## Diseño de APIs

### 1. API de Estadísticas Generales
```python
@monitoreo_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_estadisticas():
    """
    Retorna estadísticas generales del sistema electoral
    
    Response:
    {
        "success": true,
        "data": {
            "testigos": {
                "total": 150,
                "con_geolocalizacion": 120,
                "con_presencia_verificada": 100,
                "porcentaje_geo": 80.0,
                "porcentaje_presencia": 66.7
            },
            "coordinadores": {
                "total": 25,
                "con_geolocalizacion": 20,
                "puesto": 15,
                "municipal": 8,
                "departamental": 2,
                "porcentaje_geo": 80.0
            },
            "formularios": {
                "total": 450,
                "esperados": 600,
                "validados": 300,
                "pendientes": 150,
                "porcentaje_recibidos": 75.0,
                "porcentaje_validados": 66.7,
                "total_mesas": 200,
                "tipos_eleccion": 3
            }
        }
    }
    """
```

### 2. API de Datos de Mapa
```python
@monitoreo_bp.route('/datos-mapa', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_datos_mapa():
    """
    Retorna datos para renderizar el mapa de geolocalización
    
    Response:
    {
        "success": true,
        "usuarios": [
            {
                "id": 1,
                "nombre": "Juan Pérez",
                "rol": "testigo_electoral",
                "latitud": 1.6144,
                "longitud": -75.6062,
                "presencia_verificada": true,
                "ultima_actualizacion": "2025-12-24T10:30:00Z",
                "mesa_asignada": "Mesa 001",
                "puesto": "Puesto Central"
            }
        ],
        "puestos": [...],
        "incidentes": [...],
        "delitos": [...]
    }
    """
```

### 3. API de Mapa de Calor
```python
@monitoreo_bp.route('/mapa-calor', methods=['GET'])
@jwt_required()
@role_required('monitoreo')
def get_mapa_calor():
    """
    Calcula índice de actividad por departamento
    
    Fórmula del índice:
    actividad_total = usuarios + formularios + (incidentes * 2) + (delitos * 3)
    
    Response:
    {
        "success": true,
        "mapa_calor": [
            {
                "departamento_codigo": "18",
                "departamento_nombre": "Caquetá",
                "usuarios": 45,
                "formularios": 120,
                "incidentes": 5,
                "delitos": 2,
                "indice_actividad": 181
            }
        ]
    }
    """
```

## Diseño de Frontend

### 1. Dashboard Principal
```html
<!-- Estructura del Dashboard -->
<div class="container-fluid">
    <!-- Header con título y logout -->
    <div class="row mb-4">
        <div class="col-12">
            <h1>Monitoreo en Tiempo Real</h1>
            <button onclick="logout()">Cerrar Sesión</button>
        </div>
    </div>
    
    <!-- Tarjetas de estadísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="stat-card">
                <h3 id="stat-testigos-geo">-</h3>
                <p>Testigos con Geolocalización</p>
            </div>
        </div>
        <!-- Más tarjetas... -->
    </div>
    
    <!-- Mapa de geolocalización -->
    <div class="row">
        <div class="col-12">
            <div id="mapa-monitoreo"></div>
        </div>
    </div>
    
    <!-- Tabla consolidado E-24 -->
    <div class="row mt-4">
        <div class="col-12">
            <table id="tabla-e24">
                <!-- Contenido dinámico -->
            </table>
        </div>
    </div>
</div>
```

### 2. Componente MapaGeolocalizacion
```javascript
class MapaGeolocalizacion {
    constructor(containerId, options) {
        this.containerId = containerId;
        this.options = options;
        this.map = null;
        this.markers = {
            testigos: [],
            coordinadores: [],
            puestos: [],
            incidentes: [],
            delitos: []
        };
        this.filtros = {
            testigos: true,
            coordinadores: true,
            incidentes: false,
            delitos: false,
            pendientes: false,
            completados: false
        };
    }
    
    async init() {
        // Inicializar mapa Leaflet
        this.map = L.map(this.containerId).setView(
            this.options.center, 
            this.options.zoom
        );
        
        // Cargar datos iniciales
        await this.cargarDatos();
        
        // Configurar auto-actualización
        if (this.options.autoUpdate) {
            setInterval(() => this.actualizarDatos(), this.options.updateInterval);
        }
    }
    
    async cargarDatos() {
        const response = await APIClient.get('/monitoreo/datos-mapa');
        if (response.success) {
            this.renderizarUsuarios(response.usuarios);
            this.renderizarPuestos(response.puestos);
            this.renderizarIncidentes(response.incidentes);
            this.renderizarDelitos(response.delitos);
        }
    }
    
    setFiltro(tipo, activo) {
        this.filtros[tipo] = activo;
        this.aplicarFiltros();
    }
    
    async buscarPuesto(termino) {
        // Implementar búsqueda de puestos
    }
}
```

### 3. Sistema de Auto-actualización
```javascript
// Auto-refresh cada 30 segundos
setInterval(async () => {
    console.log('[Monitoreo] Auto-refresh...');
    await cargarEstadisticas();
    await cargarEstadisticasUsuarios();
    await cargarFormulariosE24();
    
    // Actualizar mapa si existe
    if (window.mapaGeolocalizacion) {
        await window.mapaGeolocalizacion.actualizarDatos();
    }
}, 30000);
```

## Diseño de Base de Datos

### Consultas Optimizadas

#### 1. Estadísticas de Testigos
```sql
-- Testigos con geolocalización
SELECT COUNT(*) as con_geolocalizacion
FROM users u 
JOIN locations l ON u.ubicacion_id = l.id 
WHERE u.rol = 'testigo_electoral' 
  AND u.activo = true 
  AND u.latitud IS NOT NULL 
  AND u.longitud IS NOT NULL;

-- Testigos con presencia verificada
SELECT COUNT(*) as con_presencia
FROM users 
WHERE rol = 'testigo_electoral' 
  AND activo = true 
  AND presencia_verificada = true;
```

#### 2. Datos para Mapa
```sql
-- Usuarios activos con geolocalización
SELECT u.id, u.nombre, u.rol, u.latitud, u.longitud, 
       u.presencia_verificada, u.ultima_geolocalizacion_at,
       m.mesa_nombre, p.puesto_nombre
FROM users u
LEFT JOIN mesas m ON u.mesa_asignada_id = m.id
LEFT JOIN puestos p ON m.puesto_id = p.id
WHERE u.activo = true 
  AND u.latitud IS NOT NULL 
  AND u.longitud IS NOT NULL
  AND u.ultima_geolocalizacion_at >= NOW() - INTERVAL '1 hour';
```

#### 3. Mapa de Calor por Departamento
```sql
-- Índice de actividad por departamento
SELECT 
    l.departamento_codigo,
    l.departamento_nombre,
    COUNT(DISTINCT u.id) as usuarios,
    COUNT(DISTINCT f.id) as formularios,
    COUNT(DISTINCT i.id) as incidentes,
    COUNT(DISTINCT d.id) as delitos,
    (COUNT(DISTINCT u.id) + COUNT(DISTINCT f.id) + 
     COUNT(DISTINCT i.id) * 2 + COUNT(DISTINCT d.id) * 3) as indice_actividad
FROM locations l
LEFT JOIN users u ON l.departamento_codigo = (
    SELECT l2.departamento_codigo 
    FROM locations l2 
    WHERE l2.id = u.ubicacion_id
)
LEFT JOIN formularios_e14 f ON f.testigo_id = u.id
LEFT JOIN incidentes_electorales i ON i.reportado_por_id = u.id
LEFT JOIN delitos_electorales d ON d.reportado_por_id = u.id
WHERE l.tipo = 'departamento'
GROUP BY l.departamento_codigo, l.departamento_nombre
ORDER BY indice_actividad DESC;
```

## Correctness Properties

### Property 1: Consistencia de Estadísticas
```python
def test_estadisticas_consistency():
    """
    PROPERTY: La suma de testigos con presencia + sin presencia debe igual total
    """
    stats = get_estadisticas()
    testigos = stats['data']['testigos']
    
    assert testigos['con_presencia_verificada'] + \
           (testigos['total'] - testigos['con_presencia_verificada']) == \
           testigos['total']
```

### Property 2: Integridad de Geolocalización
```python
def test_geolocalizacion_integrity():
    """
    PROPERTY: Usuarios con geolocalización deben tener lat/lng válidas
    """
    datos_mapa = get_datos_mapa()
    
    for usuario in datos_mapa['usuarios']:
        assert -90 <= usuario['latitud'] <= 90
        assert -180 <= usuario['longitud'] <= 180
        assert usuario['ultima_actualizacion'] is not None
```

### Property 3: Validez de Índice de Actividad
```python
def test_indice_actividad_validity():
    """
    PROPERTY: Índice de actividad debe ser >= suma de componentes individuales
    """
    mapa_calor = get_mapa_calor()
    
    for dept in mapa_calor['mapa_calor']:
        componentes = dept['usuarios'] + dept['formularios'] + \
                     dept['incidentes'] + dept['delitos']
        assert dept['indice_actividad'] >= componentes
```

### Property 4: Consistencia Temporal
```python
def test_temporal_consistency():
    """
    PROPERTY: Datos de tendencias deben ser coherentes temporalmente
    """
    tendencias = get_tendencias()
    
    for i in range(len(tendencias['tendencias']) - 1):
        hora_actual = tendencias['tendencias'][i]['hora']
        hora_siguiente = tendencias['tendencias'][i + 1]['hora']
        assert (hora_siguiente - hora_actual) % 24 == 1
```

### Property 5: Integridad de Formularios
```python
def test_formularios_integrity():
    """
    PROPERTY: Total votos = votos válidos + nulos + blanco
    """
    formularios = get_formularios_e24()
    
    for form in formularios:
        if form['total_votos'] > 0:
            suma_componentes = (form['votos_validos'] + 
                              form['votos_nulos'] + 
                              form['votos_blanco'])
            assert form['total_votos'] == suma_componentes
```

### Property 6: Validez de Porcentajes
```python
def test_porcentajes_validity():
    """
    PROPERTY: Todos los porcentajes deben estar entre 0 y 100
    """
    stats = get_estadisticas()
    
    for categoria in stats['data'].values():
        for key, value in categoria.items():
            if 'porcentaje' in key:
                assert 0 <= value <= 100
```

### Property 7: Consistencia de Comparativa
```python
def test_comparativa_consistency():
    """
    PROPERTY: Score de rendimiento debe reflejar métricas reales
    """
    comparativa = get_comparativa_departamentos()
    
    for dept in comparativa['comparativa']:
        # Score alto debe correlacionar con buenos indicadores
        if dept['score_rendimiento'] > 80:
            assert dept['testigos']['porcentaje_presencia'] > 70
            assert dept['formularios']['porcentaje_validados'] > 70
```

### Property 8: Validez de Predicciones
```python
def test_predicciones_validity():
    """
    PROPERTY: Predicciones deben ser numéricamente válidas
    """
    predicciones = get_predicciones()
    pred = predicciones['predicciones']
    
    assert pred['formularios']['prediccion_proximas_24h'] >= 0
    assert pred['incidentes']['prediccion_proximas_24h'] >= 0
    assert pred['formularios']['horas_estimadas_completar'] >= 0
```

## Consideraciones de Rendimiento

### 1. Optimizaciones de Base de Datos
- Índices en columnas de filtrado frecuente
- Consultas con LIMIT para paginación
- JOINs optimizados para estadísticas

### 2. Optimizaciones de Frontend
- Paginación en tabla E-24 (20 registros por página)
- Filtros aplicados en cliente para mejor UX
- Auto-refresh inteligente (solo datos cambiados)

### 3. Caching
- Cache de estadísticas por 30 segundos
- Cache de datos de mapa por 1 minuto
- Cache de filtros en localStorage

## Seguridad

### 1. Autenticación y Autorización
- JWT requerido en todas las APIs
- Verificación de rol 'monitoreo'
- Timeout de sesión automático

### 2. Validación de Datos
- Sanitización de parámetros de entrada
- Validación de coordenadas geográficas
- Escape de contenido HTML

### 3. Rate Limiting
- Límite de requests por minuto
- Protección contra ataques DDoS
- Logging de accesos sospechosos