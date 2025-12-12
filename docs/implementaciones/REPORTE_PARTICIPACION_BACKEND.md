# Implementación Backend - Reporte de Participación Horaria (E-11)
**Fecha:** 2025-12-08  
**Estado:** ✅ Backend Completado  
**Fase:** 1 de 4

## Resumen

Se ha implementado completamente el backend para el sistema de Reporte de Participación Horaria (E-11), que permite a los testigos reportar cada hora cuántas personas han votado según el formulario E-11.

## Archivos Creados

### 1. Modelo de Datos
**Archivo:** `backend/models/reporte_participacion.py`

**Clase:** `ReporteParticipacion`

**Campos:**
- `id` - ID único del reporte
- `mesa_id` - ID de la mesa (FK)
- `testigo_id` - ID del testigo que reporta (FK)
- `hora_reporte` - Hora del reporte (redondeada a la hora)
- `personas_votadas` - Número acumulado de personas que han votado
- `porcentaje_participacion` - Calculado automáticamente
- `observaciones` - Notas opcionales
- `created_at` - Fecha de creación
- `updated_at` - Fecha de actualización

**Constraints:**
- Unique: `(mesa_id, hora_reporte)` - Solo un reporte por hora por mesa
- Índices en: `mesa_id`, `hora_reporte`, `testigo_id`

**Métodos:**
- `to_dict()` - Conversión básica a diccionario
- `to_dict_completo()` - Conversión con información de mesa y testigo

### 2. Migración
**Archivo:** `backend/migrations/create_reporte_participacion_table.py`

**Funciones:**
- `upgrade()` - Crea la tabla e índices
- `downgrade()` - Elimina la tabla

**Script de Aplicación:** `scripts/init/aplicar_migracion_reporte_participacion.py`

**Ejecutar:**
```bash
python scripts/init/aplicar_migracion_reporte_participacion.py
```

### 3. Servicio
**Archivo:** `backend/services/reporte_participacion_service.py`

**Clase:** `ReporteParticipacionService`

**Métodos:**

#### `crear_reporte(data, testigo_id)`
Crea un nuevo reporte de participación.

**Validaciones:**
- ✅ Mesa existe y es válida
- ✅ Testigo tiene acceso a la mesa
- ✅ Hora está entre 8:00 AM y 4:00 PM
- ✅ Hora no es futura
- ✅ Personas votadas >= 0
- ✅ Personas votadas <= votantes registrados
- ✅ Personas votadas >= reporte anterior (acumulado)
- ✅ No existe reporte para esta hora (solo uno por hora)

**Cálculos:**
- Redondea hora a la hora más cercana (ej: 10:35 → 10:00)
- Calcula porcentaje de participación automáticamente

#### `obtener_reportes_mesa(mesa_id)`
Obtiene todos los reportes de una mesa ordenados por hora.

**Retorna:**
- Información de la mesa
- Lista de reportes
- Último reporte
- Total de reportes

#### `obtener_participacion_puesto(puesto_id)`
Obtiene participación de todas las mesas de un puesto.

**Retorna:**
- Información del puesto
- Resumen (total personas votadas, porcentaje, mesas reportadas)
- Lista de mesas con su último reporte
- Tendencia por mesa

#### `_calcular_tendencia(mesa_id)` (privado)
Calcula la tendencia de participación comparando últimos 2 reportes.

**Tendencias:**
- `normal` - Crecimiento constante (20-100 personas/hora)
- `lenta` - Crecimiento bajo (<20 personas/hora)
- `rapida` - Crecimiento alto (>100 personas/hora)
- `estancada` - Sin crecimiento (0 personas/hora)
- `sin_datos` - No hay reportes suficientes

### 4. Rutas API
**Archivo:** `backend/routes/reporte_participacion.py`

**Blueprint:** `reporte_participacion_bp`

**Prefix:** `/api/reporte-participacion`

#### Endpoints:

##### 1. Crear Reporte
```
POST /api/reporte-participacion
```

**Rol:** `testigo_electoral`

**Body:**
```json
{
    "mesa_id": 123,
    "hora_reporte": "2024-03-10T10:00:00",
    "personas_votadas": 120,
    "observaciones": "Flujo normal"
}
```

**Response 201:**
```json
{
    "success": true,
    "message": "Reporte de participación creado exitosamente",
    "data": {
        "id": 456,
        "mesa_id": 123,
        "hora_reporte": "2024-03-10T10:00:00",
        "personas_votadas": 120,
        "porcentaje_participacion": 12.0,
        "mesa": {
            "id": 123,
            "codigo": "001",
            "nombre": "Mesa 1",
            "votantes_registrados": 1000
        },
        "testigo": {
            "id": 789,
            "nombre": "Juan Pérez"
        }
    }
}
```

##### 2. Obtener Reportes de Mesa
```
GET /api/reporte-participacion/mesa/{mesa_id}
```

**Rol:** Cualquier usuario autenticado

**Response 200:**
```json
{
    "success": true,
    "data": {
        "mesa": {
            "id": 123,
            "codigo": "001",
            "nombre": "Mesa 1",
            "votantes_registrados": 1000
        },
        "reportes": [
            {
                "id": 1,
                "hora_reporte": "2024-03-10T09:00:00",
                "personas_votadas": 45,
                "porcentaje_participacion": 4.5
            },
            {
                "id": 2,
                "hora_reporte": "2024-03-10T10:00:00",
                "personas_votadas": 120,
                "porcentaje_participacion": 12.0
            }
        ],
        "ultimo_reporte": {
            "id": 2,
            "hora_reporte": "2024-03-10T10:00:00",
            "personas_votadas": 120,
            "porcentaje_participacion": 12.0
        },
        "total_reportes": 2
    }
}
```

##### 3. Obtener Participación de Puesto
```
GET /api/reporte-participacion/puesto/{puesto_id}
```

**Roles:** `coordinador_puesto`, `coordinador_municipal`, `monitoreo`, `super_admin`

**Response 200:**
```json
{
    "success": true,
    "data": {
        "puesto": {
            "id": 10,
            "nombre": "Escuela Central",
            "total_mesas": 5,
            "total_votantes": 5000
        },
        "resumen": {
            "total_personas_votadas": 600,
            "porcentaje_participacion": 12.0,
            "mesas_reportadas": 5,
            "ultimo_reporte": "2024-03-10T10:00:00"
        },
        "mesas": [
            {
                "mesa_id": 123,
                "mesa_codigo": "001",
                "votantes_registrados": 1000,
                "ultimo_reporte": {
                    "hora_reporte": "2024-03-10T10:00:00",
                    "personas_votadas": 120,
                    "porcentaje_participacion": 12.0
                },
                "tendencia": "normal"
            }
        ]
    }
}
```

##### 4. Obtener Mis Reportes (Testigo)
```
GET /api/reporte-participacion/mi-mesa
```

**Rol:** `testigo_electoral`

**Response:** Igual que endpoint 2, pero para la mesa del testigo actual

### 5. Registro en Aplicación
**Archivo:** `backend/app.py`

Blueprint registrado en la función `register_blueprints()`.

## Validaciones Implementadas

### 1. Horario de Votación
- ✅ Solo se permiten reportes entre 8:00 AM y 4:00 PM
- ✅ No se permiten reportes futuros

### 2. Datos Acumulados
- ✅ Cada reporte debe tener >= personas que el reporte anterior
- ✅ Los reportes son acumulados (no incrementales)

### 3. Límites
- ✅ Personas votadas no puede exceder votantes registrados
- ✅ Solo un reporte por hora por mesa
- ✅ Personas votadas >= 0

### 4. Permisos
- ✅ Solo testigos pueden crear reportes
- ✅ Coordinadores pueden ver reportes de su jurisdicción
- ✅ Monitoreo puede ver todos los reportes

## Cálculos Automáticos

### Porcentaje de Participación
```python
porcentaje = (personas_votadas / votantes_registrados) * 100
```

### Redondeo de Hora
```python
hora_redondeada = hora_reporte.replace(minute=0, second=0, microsecond=0)
```

### Tendencia
```python
crecimiento = ultimo.personas_votadas - penultimo.personas_votadas

if crecimiento == 0: return 'estancada'
elif crecimiento < 20: return 'lenta'
elif crecimiento > 100: return 'rapida'
else: return 'normal'
```

## Ejemplo de Uso

### Crear Reporte (Testigo)
```bash
curl -X POST http://localhost:5000/api/reporte-participacion \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "mesa_id": 123,
    "hora_reporte": "2024-03-10T10:00:00",
    "personas_votadas": 120,
    "observaciones": "Flujo normal de votantes"
  }'
```

### Obtener Reportes de Mesa
```bash
curl -X GET http://localhost:5000/api/reporte-participacion/mesa/123 \
  -H "Authorization: Bearer {token}"
```

### Obtener Participación de Puesto (Coordinador)
```bash
curl -X GET http://localhost:5000/api/reporte-participacion/puesto/10 \
  -H "Authorization: Bearer {token}"
```

## Próximos Pasos

### Fase 2: Frontend Testigo (Siguiente)
- [ ] Agregar pestaña "Participación" en dashboard testigo
- [ ] Crear formulario de reporte
- [ ] Mostrar histórico de reportes
- [ ] Implementar gráfico de tendencia
- [ ] Agregar notificaciones horarias

### Fase 3: Frontend Coordinadores
- [ ] Agregar sección de participación en coordinador de puesto
- [ ] Crear tabla de mesas con participación
- [ ] Implementar alertas de baja participación
- [ ] Agregar mapa de calor en coordinador municipal

### Fase 4: Monitoreo
- [ ] Dashboard de participación nacional
- [ ] Estadísticas en tiempo real
- [ ] Sistema de alertas automáticas
- [ ] Proyecciones de participación final

## Pruebas Recomendadas

1. **Crear reporte válido**
   - Verificar que se crea correctamente
   - Verificar cálculo de porcentaje

2. **Validaciones**
   - Intentar crear reporte fuera de horario (debe fallar)
   - Intentar crear reporte con personas > votantes (debe fallar)
   - Intentar crear reporte con personas < reporte anterior (debe fallar)
   - Intentar crear dos reportes en la misma hora (debe fallar)

3. **Consultas**
   - Obtener reportes de mesa
   - Obtener participación de puesto
   - Verificar cálculo de tendencias

4. **Permisos**
   - Verificar que solo testigos pueden crear reportes
   - Verificar que coordinadores pueden ver reportes

## Notas Técnicas

- Los reportes son **acumulados**, no incrementales
- La hora se redondea automáticamente a la hora más cercana
- El porcentaje se calcula automáticamente
- La tendencia se calcula comparando últimos 2 reportes
- Solo se permite un reporte por hora por mesa

## Estado Actual

✅ **Backend Completado (Fase 1)**
- Modelo de datos
- Migración
- Servicio con validaciones
- Rutas API
- Registro en aplicación

⏳ **Pendiente (Fases 2-4)**
- Frontend testigo
- Frontend coordinadores
- Dashboard monitoreo
