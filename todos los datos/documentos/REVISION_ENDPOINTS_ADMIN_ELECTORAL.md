# Revisión de Endpoints de Administración Electoral

**Fecha**: 2025-11-15  
**Hora**: 19:00

## 🔍 Verificación Realizada

Se revisaron los endpoints del Super Admin para gestión de datos electorales:
- Tipos de elección
- Partidos políticos  
- Candidatos

## ✅ Endpoints Existentes

### 1. Tipos de Elección

#### GET `/api/super-admin/tipos-eleccion`
- ❌ **PROBLEMA**: Usa import incorrecto `from backend.models.tipo_eleccion import TipoEleccion`
- ✅ **CORRECTO**: `from backend.models.configuracion_electoral import TipoEleccion`

#### POST `/api/super-admin/tipos-eleccion`
- ✅ Usa import correcto
- ✅ Funcionalidad completa
- Permite crear tipos de elección con:
  - `codigo`, `nombre`, `descripcion`
  - `es_uninominal` (True/False)
  - `permite_lista_cerrada` (True/False)
  - `permite_lista_abierta` (True/False)
  - `permite_coaliciones` (True/False)

#### PUT `/api/super-admin/tipos-eleccion/<id>`
- ✅ Usa import correcto
- ✅ Permite actualizar todos los campos

### 2. Partidos Políticos

#### POST `/api/super-admin/upload/partidos`
- ❌ **PROBLEMA**: Usa import incorrecto `from backend.models.partido import Partido`
- ✅ **CORRECTO**: `from backend.models.configuracion_electoral import Partido`
- Carga masiva desde Excel
- Campos: `nombre`, `sigla`, `color`, `numero_lista`

### 3. Candidatos

#### POST `/api/super-admin/upload/candidatos`
- ❌ **PROBLEMA**: Usa múltiples imports incorrectos:
  - `from backend.models.candidato import Candidato`
  - `from backend.models.partido import Partido`
  - `from backend.models.tipo_eleccion import TipoEleccion`
- ✅ **CORRECTO**: Todos deben venir de `backend.models.configuracion_electoral`
- Carga masiva desde Excel
- Campos: `nombre`, `partido_nombre`, `tipo_eleccion_nombre`, `numero_lista`

## 🔴 Problemas Identificados

### 1. Imports Incorrectos
Los endpoints usan modelos que no existen:
- `backend.models.tipo_eleccion` ❌
- `backend.models.partido` ❌
- `backend.models.candidato` ❌

**Todos los modelos están en**: `backend.models.configuracion_electoral` ✅

### 2. Campos Faltantes en Carga de Candidatos
El endpoint de carga de candidatos no incluye campos importantes:
- `codigo` (requerido en el modelo)
- `es_independiente`
- `es_cabeza_lista`
- `foto_url`
- `activo`

### 3. Campos Faltantes en Carga de Partidos
El endpoint de carga de partidos usa campos antiguos:
- Usa `sigla` pero el modelo tiene `nombre_corto`
- Usa `numero_lista` pero el modelo no lo tiene
- Falta `codigo` (requerido en el modelo)
- Falta `logo_url`

## ✅ Estado Actual de la Base de Datos

Según la verificación realizada:
- ✅ **Tipos de elección**: 11 configurados correctamente
- ✅ **Partidos políticos**: 10 configurados correctamente
- ❌ **Candidatos**: 0 (ninguno cargado)

Esto significa que:
1. Los tipos de elección se cargaron correctamente (probablemente por script de inicialización)
2. Los partidos se cargaron correctamente (probablemente por script de inicialización)
3. Los candidatos NO se han cargado

## 📋 Correcciones Necesarias

### 1. Corregir Endpoint GET `/api/super-admin/tipos-eleccion`
```python
# ANTES (línea 748)
from backend.models.tipo_eleccion import TipoEleccion

# DESPUÉS
from backend.models.configuracion_electoral import TipoEleccion
```

### 2. Corregir Endpoint POST `/api/super-admin/upload/partidos`
```python
# ANTES (línea 527)
from backend.models.partido import Partido

# DESPUÉS
from backend.models.configuracion_electoral import Partido

# Y actualizar campos:
partido = Partido(
    codigo=row.get('codigo', row['nombre'].upper().replace(' ', '_')),
    nombre=row['nombre'],
    nombre_corto=row['nombre_corto'],  # Cambiar de 'sigla'
    color=row['color'],
    logo_url=row.get('logo_url'),
    activo=row.get('activo', True)
)
```

### 3. Corregir Endpoint POST `/api/super-admin/upload/candidatos`
```python
# ANTES (líneas 630-632)
from backend.models.candidato import Candidato
from backend.models.partido import Partido
from backend.models.tipo_eleccion import TipoEleccion

# DESPUÉS
from backend.models.configuracion_electoral import Candidato, Partido, TipoEleccion

# Y actualizar campos:
candidato = Candidato(
    codigo=row.get('codigo', f"{tipo_eleccion.codigo}_{partido.codigo}_{index}"),
    nombre_completo=row['nombre'],
    numero_lista=row.get('numero_lista'),
    partido_id=partido.id,
    tipo_eleccion_id=tipo_eleccion.id,
    foto_url=row.get('foto_url'),
    es_independiente=row.get('es_independiente', False),
    es_cabeza_lista=row.get('es_cabeza_lista', False),
    activo=row.get('activo', True)
)
```

## 🎯 Recomendaciones

### 1. Crear Script de Carga de Candidatos de Prueba
Ya que no hay candidatos en la BD, crear un script que cargue candidatos de prueba:

```python
# load_candidatos_prueba.py
candidatos_prueba = [
    # Presidencia
    {"codigo": "PRES_LIB_001", "nombre_completo": "Juan Pérez García", 
     "partido_id": 1, "tipo_eleccion_id": 1, "es_cabeza_lista": True},
    {"codigo": "PRES_CON_001", "nombre_completo": "María López Rodríguez", 
     "partido_id": 2, "tipo_eleccion_id": 1, "es_cabeza_lista": True},
    # ... más candidatos
]
```

### 2. Actualizar Formato de Excel para Carga Masiva

**Para Partidos**:
```
codigo | nombre | nombre_corto | color | logo_url | activo
LIBERAL | Partido Liberal | Liberal | #FF0000 | | true
```

**Para Candidatos**:
```
codigo | nombre | partido_nombre | tipo_eleccion_nombre | numero_lista | es_independiente | es_cabeza_lista | activo
PRES_LIB_001 | Juan Pérez | Partido Liberal | Presidencia | 1 | false | true | true
```

### 3. Verificar Endpoints Funcionando

Después de las correcciones, probar:
1. GET `/api/super-admin/tipos-eleccion` - Debe retornar 11 tipos
2. POST `/api/super-admin/upload/partidos` - Cargar partidos desde Excel
3. POST `/api/super-admin/upload/candidatos` - Cargar candidatos desde Excel

## ✅ Endpoints del Testigo

El testigo ya tiene acceso a:
- ✅ GET `/api/testigo/tipos-eleccion` - Funciona correctamente
- ✅ GET `/api/testigo/partidos` - Funciona correctamente
- ✅ GET `/api/testigo/candidatos` - **NUEVO** - Agregado en esta sesión

## 📊 Resumen

| Componente | Estado BD | Endpoint Admin | Endpoint Testigo |
|------------|-----------|----------------|------------------|
| Tipos de Elección | ✅ 11 | ⚠️ Import incorrecto | ✅ Funciona |
| Partidos | ✅ 10 | ⚠️ Import incorrecto | ✅ Funciona |
| Candidatos | ❌ 0 | ⚠️ Import incorrecto | ✅ Funciona |

## 🔧 Próximos Pasos

1. **Corregir imports** en los 3 endpoints del Super Admin
2. **Actualizar campos** en endpoints de carga masiva
3. **Cargar candidatos de prueba** en la base de datos
4. **Probar flujo completo** de formulario E-14 con candidatos

## ✅ Conclusión

Los endpoints existen pero tienen **imports incorrectos** que deben corregirse. Una vez corregidos, el sistema estará listo para:
- Gestionar tipos de elección desde el admin
- Cargar partidos masivamente
- Cargar candidatos masivamente
- Usar candidatos en formularios E-14

**Prioridad**: ALTA - Corregir imports para que los endpoints funcionen correctamente.
