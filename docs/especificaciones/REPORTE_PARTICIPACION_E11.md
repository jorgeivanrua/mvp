# Reporte de Participación Horaria (E-11)
**Fecha:** 2025-12-08  
**Estado:** 📋 Especificación  
**Prioridad:** Alta

## Objetivo

Permitir que los testigos reporten cada hora cuántas personas han votado (según el formulario E-11), para que el monitoreo tenga visibilidad en tiempo real de la participación electoral y pueda tomar acciones.

## Contexto Electoral

### Formulario E-11
- **Nombre:** Registro de Votantes
- **Propósito:** Cada votante firma cuando va a votar para verificar que está habilitado
- **Uso:** El testigo cuenta las firmas para saber cuántas personas han votado hasta el momento

### Horario de Votación
- **Inicio:** 8:00 AM
- **Cierre:** 4:00 PM
- **Duración:** 8 horas

### Frecuencia de Reporte
- **Ideal:** Cada hora (9am, 10am, 11am, 12pm, 1pm, 2pm, 3pm, 4pm)
- **Mínimo:** Cada 2 horas
- **Dato:** Número acumulado de personas que han votado hasta ese momento

## Casos de Uso

### Caso 1: Testigo Reporta Participación
**Actor:** Testigo Electoral

**Flujo:**
1. Testigo cuenta las firmas en el E-11
2. Ingresa al sistema
3. Selecciona "Reportar Participación"
4. Ingresa:
   - Hora del reporte (ej: 10:00 AM)
   - Número de personas que han votado hasta ese momento
5. Sistema guarda el reporte
6. Sistema muestra histórico de reportes

**Ejemplo:**
```
9:00 AM  - 45 personas han votado
10:00 AM - 120 personas han votado
11:00 AM - 210 personas han votado
12:00 PM - 350 personas han votado
1:00 PM  - 480 personas han votado
2:00 PM  - 620 personas han votado
3:00 PM  - 750 personas han votado
4:00 PM  - 850 personas han votado (cierre)
```

### Caso 2: Coordinador de Puesto Monitorea Participación
**Actor:** Coordinador de Puesto

**Flujo:**
1. Coordinador ingresa al dashboard
2. Ve tabla con todas las mesas del puesto
3. Para cada mesa ve:
   - Último reporte de participación
   - Hora del último reporte
   - Porcentaje de participación
   - Tendencia (gráfico)
4. Identifica mesas con baja participación
5. Toma acciones (llamar al testigo, enviar apoyo, etc.)

### Caso 3: Coordinador Municipal Monitorea Participación
**Actor:** Coordinador Municipal

**Flujo:**
1. Coordinador ingresa al dashboard
2. Ve mapa con todos los puestos del municipio
3. Puestos coloreados según participación:
   - Verde: Participación alta (>70%)
   - Amarillo: Participación media (40-70%)
   - Rojo: Participación baja (<40%)
4. Ve gráficos de tendencia por zona
5. Identifica zonas con problemas
6. Coordina acciones

### Caso 4: Monitoreo Global Supervisa Participación
**Actor:** Monitoreo

**Flujo:**
1. Monitoreo ingresa al dashboard
2. Ve mapa de calor de todo el país
3. Ve estadísticas en tiempo real:
   - Participación nacional
   - Participación por departamento
   - Participación por municipio
   - Tendencias horarias
4. Genera alertas automáticas
5. Coordina respuestas

## Modelo de Datos

### Tabla: `reporte_participacion`

```sql
CREATE TABLE reporte_participacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa_id INTEGER NOT NULL,
    testigo_id INTEGER NOT NULL,
    hora_reporte DATETIME NOT NULL,
    personas_votadas INTEGER NOT NULL,
    porcentaje_participacion DECIMAL(5,2),
    observaciones TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (mesa_id) REFERENCES location(id),
    FOREIGN KEY (testigo_id) REFERENCES user(id),
    
    -- Un testigo solo puede hacer un reporte por hora por mesa
    UNIQUE(mesa_id, hora_reporte)
);

CREATE INDEX idx_reporte_participacion_mesa ON reporte_participacion(mesa_id);
CREATE INDEX idx_reporte_participacion_hora ON reporte_participacion(hora_reporte);
CREATE INDEX idx_reporte_participacion_testigo ON reporte_participacion(testigo_id);
```

### Campos:
- `mesa_id`: Mesa donde se reporta
- `testigo_id`: Testigo que reporta
- `hora_reporte`: Hora del reporte (ej: 2024-03-10 10:00:00)
- `personas_votadas`: Número acumulado de personas que han votado
- `porcentaje_participacion`: Calculado automáticamente (personas_votadas / votantes_registrados * 100)
- `observaciones`: Notas opcionales del testigo

## API Endpoints

### 1. Crear Reporte de Participación
```
POST /api/testigo/reporte-participacion
```

**Body:**
```json
{
    "mesa_id": 123,
    "hora_reporte": "2024-03-10T10:00:00",
    "personas_votadas": 120,
    "observaciones": "Flujo normal de votantes"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 456,
        "mesa_id": 123,
        "hora_reporte": "2024-03-10T10:00:00",
        "personas_votadas": 120,
        "porcentaje_participacion": 12.0,
        "created_at": "2024-03-10T10:05:00"
    }
}
```

### 2. Obtener Reportes de una Mesa
```
GET /api/testigo/reporte-participacion?mesa_id=123
```

**Response:**
```json
{
    "success": true,
    "data": {
        "mesa": {
            "id": 123,
            "codigo": "001",
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
            "hora": "2024-03-10T10:00:00",
            "personas_votadas": 120,
            "porcentaje": 12.0
        }
    }
}
```

### 3. Obtener Participación del Puesto
```
GET /api/coordinador-puesto/participacion
```

**Response:**
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
                    "hora": "2024-03-10T10:00:00",
                    "personas_votadas": 120,
                    "porcentaje": 12.0
                },
                "tendencia": "normal"
            }
        ]
    }
}
```

### 4. Obtener Participación Municipal
```
GET /api/coordinador-municipal/participacion
```

### 5. Obtener Participación Nacional (Monitoreo)
```
GET /api/monitoreo/participacion
```

## Interfaz de Usuario

### Dashboard Testigo - Nueva Pestaña "Participación"

**Elementos:**
1. **Botón "Reportar Participación"** (destacado)
2. **Formulario de Reporte:**
   - Hora (selector o automático)
   - Número de personas que han votado
   - Observaciones (opcional)
3. **Histórico de Reportes:**
   - Tabla con hora, personas votadas, porcentaje
   - Gráfico de tendencia
4. **Indicador de Próximo Reporte:**
   - "Próximo reporte sugerido: 11:00 AM"
   - Notificación cada hora

### Dashboard Coordinador de Puesto - Sección "Participación"

**Elementos:**
1. **Resumen General:**
   - Total personas votadas en el puesto
   - Porcentaje de participación
   - Último reporte
2. **Tabla de Mesas:**
   - Mesa | Votantes | Último Reporte | Personas Votadas | % | Tendencia
   - Colores según participación
3. **Gráfico de Tendencia:**
   - Líneas por mesa
   - Comparación con meta

### Dashboard Coordinador Municipal - Mapa de Participación

**Elementos:**
1. **Mapa con Puestos:**
   - Coloreados según participación
   - Popup con detalles
2. **Estadísticas:**
   - Participación por zona
   - Comparación con elecciones anteriores
3. **Alertas:**
   - Puestos con baja participación
   - Puestos sin reportes recientes

### Dashboard Monitoreo - Vista Nacional

**Elementos:**
1. **Mapa de Calor:**
   - Participación por departamento/municipio
2. **Estadísticas en Tiempo Real:**
   - Participación nacional
   - Tendencias horarias
   - Proyecciones
3. **Alertas Automáticas:**
   - Zonas con baja participación
   - Zonas sin reportes

## Validaciones

1. **Hora del Reporte:**
   - Debe estar entre 8:00 AM y 4:00 PM
   - No puede ser futura
   - Solo un reporte por hora por mesa

2. **Personas Votadas:**
   - Debe ser >= 0
   - Debe ser <= votantes registrados
   - Debe ser >= reporte anterior (acumulado)

3. **Frecuencia:**
   - Máximo un reporte por hora por mesa
   - Mínimo 1 hora entre reportes

## Notificaciones y Alertas

### Para Testigos:
- Recordatorio cada hora para reportar
- Alerta si no ha reportado en 2 horas

### Para Coordinadores:
- Alerta si una mesa no reporta en 2 horas
- Alerta si participación < 30% a las 12pm
- Alerta si participación < 50% a las 2pm

### Para Monitoreo:
- Alerta si zona completa tiene baja participación
- Alerta si hay caída súbita en reportes

## Cálculos y Métricas

### Porcentaje de Participación:
```
% = (personas_votadas / votantes_registrados) * 100
```

### Tendencia:
```
- Normal: Crecimiento constante
- Lenta: Crecimiento menor al esperado
- Rápida: Crecimiento mayor al esperado
- Estancada: Sin crecimiento en última hora
```

### Proyección Final:
```
Proyección = (personas_votadas / horas_transcurridas) * 8
```

## Beneficios

1. **Visibilidad en Tiempo Real:**
   - Monitoreo sabe cuántas personas están votando
   - Puede identificar problemas temprano

2. **Toma de Decisiones:**
   - Enviar más personal a mesas con alta afluencia
   - Investigar mesas con baja participación
   - Coordinar logística

3. **Prevención de Problemas:**
   - Detectar mesas sin actividad
   - Identificar zonas con problemas
   - Actuar antes del cierre

4. **Análisis Histórico:**
   - Comparar con elecciones anteriores
   - Identificar patrones
   - Mejorar planificación futura

## Diferencia con Formulario E-14

| Aspecto | Reporte Participación (E-11) | Formulario E-14 |
|---------|------------------------------|-----------------|
| **Cuándo** | Durante el día (cada hora) | Al final del día |
| **Fuente** | Firmas en E-11 | Conteo de votos |
| **Dato** | Cuántas personas han votado | Votos por partido/candidato |
| **Propósito** | Monitoreo en tiempo real | Resultados oficiales |
| **Frecuencia** | Múltiples reportes | Un solo formulario |
| **Editable** | Sí (hasta cierre) | No (una vez enviado) |

## Implementación Sugerida

### Fase 1: Backend
1. Crear modelo `ReporteParticipacion`
2. Crear endpoints API
3. Implementar validaciones
4. Crear servicios de cálculo

### Fase 2: Frontend Testigo
1. Agregar pestaña "Participación"
2. Crear formulario de reporte
3. Mostrar histórico
4. Implementar notificaciones

### Fase 3: Frontend Coordinadores
1. Agregar sección de participación
2. Crear tablas y gráficos
3. Implementar alertas
4. Agregar mapa de calor

### Fase 4: Monitoreo
1. Dashboard de participación nacional
2. Mapa de calor
3. Estadísticas en tiempo real
4. Sistema de alertas automáticas

## Prioridad de Implementación

🔴 **Alta Prioridad:**
- Backend completo
- Frontend testigo (reporte básico)
- Frontend coordinador puesto (vista básica)

🟡 **Media Prioridad:**
- Frontend coordinador municipal
- Gráficos y tendencias
- Notificaciones

🟢 **Baja Prioridad:**
- Dashboard monitoreo avanzado
- Proyecciones
- Análisis histórico

## Próximos Pasos

1. ✅ Especificación completa (este documento)
2. ⏳ Crear migración de base de datos
3. ⏳ Implementar modelo y endpoints backend
4. ⏳ Crear interfaz testigo
5. ⏳ Crear interfaz coordinadores
6. ⏳ Pruebas y validación


## Actualización 2025-12-09: Flujo de Envío Directo

### Cambio Importante
Los reportes de participación **NO se guardan como borradores**. Se envían directamente a los coordinadores para monitoreo en tiempo real.

### Flujo Actualizado:

1. **Testigo reporta participación**:
   - Ingresa número de personas que han votado
   - Hora del reporte (se redondea a la hora más cercana)
   - Observaciones opcionales
   - **Hace clic en "Enviar Reporte"** (no hay opción de guardar)

2. **Sistema valida**:
   - Hora dentro del horario de votación (8am-4pm)
   - Número no negativo
   - Si excede votantes registrados, pide confirmación
   - Es mayor o igual al reporte anterior (acumulado)
   - Solo un reporte por hora

3. **Sistema calcula**:
   - Porcentaje de participación automático
   - Tendencia (normal, lenta, rápida, estancada)

4. **Sistema distribuye inmediatamente**:
   - Reporte guardado en base de datos
   - Asociado a mesa y testigo
   - **Disponible inmediatamente para coordinadores**:
     - Coordinador de Puesto: Ve todas las mesas de su puesto
     - Coordinador Municipal: Ve todos los puestos del municipio
     - Coordinador Departamental: Ve todos los municipios
     - Monitoreo: Vista consolidada en tiempo real

### Interfaz Actualizada:

**Modal de Reporte:**
```
┌─────────────────────────────────────────┐
│ 📤 Enviar Reporte de Participación      │
├─────────────────────────────────────────┤
│ ℹ️ Este reporte se enviará directamente │
│    a los coordinadores para monitoreo   │
│    en tiempo real.                      │
│                                         │
│ Hora del Reporte: [10:00 AM]           │
│ Personas Votadas: [120]                 │
│ Observaciones: [Flujo normal]           │
│                                         │
│ ℹ️ Votantes Registrados: 1000           │
│    Porcentaje: 12%                      │
│                                         │
│ [Cancelar]  [📤 Enviar Reporte]         │
└─────────────────────────────────────────┘
```

**Botón único:** "Enviar Reporte" (no hay "Guardar Borrador")

### Beneficios del Envío Directo:

1. **Simplicidad**: Un solo botón, un solo flujo
2. **Tiempo Real**: Los coordinadores ven los datos inmediatamente
3. **Sin Confusión**: No hay estados intermedios (borrador vs enviado)
4. **Monitoreo Efectivo**: Datos actualizados al instante
5. **Menos Errores**: No se pueden olvidar reportes en borrador

### Validación Especial:

Si el número de personas votadas excede los votantes registrados, el sistema:
1. Muestra un diálogo de confirmación
2. Permite enviar de todas formas (puede haber errores en el registro)
3. Marca el reporte para revisión posterior
