# Flujo de Datos de Formularios E-14
**Fecha:** 2025-12-08  
**Estado:** ✅ Verificado y Funcionando

## Resumen

Los formularios E-14 que crean los testigos **SÍ se guardan en la base de datos** y están disponibles para todos los coordinadores y roles de supervisión. El flujo está completamente implementado.

## Flujo de Datos

### 1. Testigo Electoral Crea Formulario E-14

**Frontend:** `frontend/static/js/testigo-dashboard-v2.js`
- Función `saveForm()` recopila datos del formulario
- Construye objeto con:
  - Datos básicos (mesa, tipo elección, totales)
  - Votos por partido (`votos_partidos`)
  - Votos por candidato (`votos_candidatos`)
  - Estado (borrador/pendiente)

**API Call:**
```javascript
const response = await APIClient.createFormularioE14(data);
```

**Endpoint:** `POST /api/formularios`
- Archivo: `backend/routes/formularios_e14.py`
- Función: `crear_formulario()`
- Requiere rol: `testigo_electoral`

### 2. Backend Guarda en Base de Datos

**Servicio:** `backend/services/formulario_service.py`
- Función: `FormularioService.crear_formulario(data, testigo_id)`

**Tablas Afectadas:**

1. **`formulario_e14`** - Registro principal
   ```python
   formulario = FormularioE14(
       mesa_id=data['mesa_id'],
       testigo_id=testigo_id,
       tipo_eleccion_id=data['tipo_eleccion_id'],
       total_votantes_registrados=data['total_votantes_registrados'],
       total_votos=data['total_votos'],
       votos_validos=data['votos_validos'],
       votos_nulos=data['votos_nulos'],
       votos_blanco=data['votos_blanco'],
       tarjetas_no_marcadas=data['tarjetas_no_marcadas'],
       total_tarjetas=data['total_tarjetas'],
       estado=data.get('estado', 'borrador'),
       observaciones=data.get('observaciones', '')
   )
   ```

2. **`voto_partido`** - Votos por partido
   ```python
   for vp_data in data['votos_partidos']:
       voto_partido = VotoPartido(
           formulario_id=formulario.id,
           partido_id=vp_data['partido_id'],
           votos=vp_data['votos']
       )
   ```

3. **`voto_candidato`** - Votos por candidato
   ```python
   for vc_data in data['votos_candidatos']:
       voto_candidato = VotoCandidato(
           formulario_id=formulario.id,
           candidato_id=vc_data['candidato_id'],
           votos=vc_data['votos']
       )
   ```

4. **`historial_formulario`** - Auditoría
   ```python
   historial = HistorialFormulario(
       formulario_id=formulario.id,
       usuario_id=testigo_id,
       accion='creado',
       estado_nuevo='borrador',
       comentario='Formulario creado'
   )
   ```

**Commit:**
```python
db.session.commit()  # ✅ Persiste TODO en la BD
```

### 3. Coordinadores Acceden a los Datos

#### A. Coordinador de Puesto

**Endpoint:** `GET /api/coordinador-puesto/formularios`
- Archivo: `backend/routes/coordinador_puesto.py`
- Función: `get_formularios()`

**Acceso:**
- Ve todos los formularios de las mesas de su puesto
- Puede validar, rechazar o solicitar correcciones
- Genera formulario E-24 (consolidado del puesto)

**Query:**
```python
formularios = FormularioE14.query.filter(
    FormularioE14.mesa_id.in_(mesa_ids)
).all()
```

#### B. Coordinador Municipal

**Endpoint:** `GET /api/coordinador-municipal/consolidado`
- Archivo: `backend/routes/coordinador_municipal.py`
- Función: `obtener_consolidado()`

**Acceso:**
- Ve consolidado de todos los puestos del municipio
- Solo formularios validados (`estado='validado'`)
- Calcula totales por partido
- Genera E-24 municipal

**Query:**
```python
formularios = FormularioE14.query.filter(
    FormularioE14.mesa_id.in_(mesa_ids),
    FormularioE14.estado == 'validado'
).all()
```

**Consolidación:**
```python
# Consolidar votos por partido
votos_por_partido = {}
for formulario in formularios:
    votos_partidos = VotoPartido.query.filter_by(formulario_id=formulario.id).all()
    for vp in votos_partidos:
        if vp.partido_id not in votos_por_partido:
            votos_por_partido[vp.partido_id] = {
                'partido_id': vp.partido_id,
                'total_votos': 0
            }
        votos_por_partido[vp.partido_id]['total_votos'] += vp.votos
```

#### C. Coordinador Departamental

**Endpoint:** Similar al municipal pero a nivel departamento
- Consolida datos de todos los municipios del departamento

#### D. Monitoreo (Rol Global)

**Endpoint:** `GET /api/monitoreo/estadisticas`
- Archivo: `backend/routes/monitoreo.py`
- Función: `get_estadisticas()`

**Acceso:**
- Ve estadísticas de TODOS los formularios del sistema
- Contadores por estado (validados, pendientes, rechazados)
- Formularios de la última hora
- Comparativas por departamento

**Query:**
```python
formularios_total = FormularioE14.query.count()
formularios_validados = FormularioE14.query.filter_by(estado='validado').count()
formularios_pendientes = FormularioE14.query.filter_by(estado='pendiente').count()
```

#### E. Super Admin y Auditor

**Endpoint:** `GET /api/formularios/todos`
- Archivo: `backend/routes/formularios_e14.py`
- Función: `obtener_todos_formularios()`

**Acceso:**
- Acceso completo a TODOS los formularios
- Filtros por estado, municipio, tipo de elección
- Incluye información completa de votos

## Estados del Formulario

1. **`borrador`** - Guardado localmente o en servidor, no enviado
2. **`pendiente`** - Enviado por testigo, esperando validación
3. **`validado`** - Aprobado por coordinador de puesto
4. **`rechazado`** - Rechazado por coordinador (con motivo)
5. **`correccion_solicitada`** - Requiere corrección del testigo

## Validaciones Implementadas

### En el Backend (`FormularioService.crear_formulario`)

1. ✅ Validación de campos requeridos
2. ✅ Validación de que la mesa existe
3. ✅ Validación de que el testigo tiene acceso a la mesa
4. ✅ Validación de unicidad (una mesa solo puede tener un formulario por tipo de elección)
5. ✅ Validación de coherencia de datos:
   ```python
   FormularioService._validar_coherencia_datos(data)
   ```

### En el Frontend (`testigo-dashboard-v2.js`)

1. ✅ Validación de que `votosData` esté inicializado
2. ✅ Validación de que haya una mesa seleccionada
3. ✅ Validación de que haya un tipo de elección seleccionado
4. ✅ Cálculo automático de totales
5. ✅ Validación de formulario HTML5

## Sincronización Offline

**Archivo:** `frontend/static/js/formularios-offline.js`

- Los formularios se pueden guardar localmente si no hay conexión
- Se sincronizan automáticamente cuando hay conexión
- El testigo puede trabajar sin internet

## Estructura de Datos Completa

### Objeto enviado al backend:

```javascript
{
    mesa_id: 123,
    tipo_eleccion_id: 1,
    total_votantes_registrados: 500,
    total_votos: 450,
    votos_validos: 430,
    votos_nulos: 15,
    votos_blanco: 5,
    tarjetas_no_marcadas: 50,
    total_tarjetas: 500,
    estado: 'pendiente',
    observaciones: 'Sin novedades',
    votos_partidos: [
        { partido_id: 1, votos: 150 },
        { partido_id: 2, votos: 120 }
    ],
    votos_candidatos: [
        { candidato_id: 10, votos: 80 },
        { candidato_id: 11, votos: 70 },
        { candidato_id: 20, votos: 60 }
    ]
}
```

## Fórmulas de Cálculo

```
Votos Válidos = Suma de todos los votos de partidos (partido + candidatos)
Total Votos = Votos Válidos + Votos Nulos + Votos en Blanco
Total Tarjetas = Total Votos + Tarjetas No Marcadas
```

**IMPORTANTE:** Los votos en blanco NO se incluyen en votos válidos.

## Conclusión

✅ **Los datos SÍ se guardan en la base de datos**
✅ **Todos los coordinadores tienen acceso según su nivel**
✅ **El flujo está completamente implementado y funcionando**
✅ **Hay validaciones en frontend y backend**
✅ **Hay soporte para trabajo offline**
✅ **Hay auditoría completa (historial)**

El sistema está diseñado para que:
1. Los testigos capturen datos en las mesas
2. Los coordinadores de puesto validen y consoliden
3. Los coordinadores municipales generen E-24 municipal
4. Los coordinadores departamentales consoliden a nivel departamento
5. Monitoreo y Super Admin supervisen todo el proceso

**No hay ningún problema con el guardado de datos.** El error que experimentaste era solo un problema de validación en el frontend que ya fue corregido.
