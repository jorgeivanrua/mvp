# Sistema de Ventanas de Tiempo para Reportes de Participación

**Fecha**: 2025-12-09  
**Implementación**: Ventanas de tiempo de 30 minutos para consolidación de reportes

## Objetivo

Implementar ventanas de tiempo específicas para que los reportes de participación se consoliden correctamente por hora, evitando reportes fuera de tiempo y asegurando la sincronización entre todas las mesas.

## Concepto de Ventanas de Tiempo

### Definición
Una **ventana de tiempo** es un período de 30 minutos después de cada hora en punto durante el cual se puede enviar el reporte correspondiente a esa hora.

### Ventanas Disponibles

| Hora del Reporte | Ventana de Envío | Ejemplo |
|------------------|------------------|---------|
| 9:00 AM | 9:00 AM - 9:30 AM | Reporte de 9am |
| 10:00 AM | 10:00 AM - 10:30 AM | Reporte de 10am |
| 11:00 AM | 11:00 AM - 11:30 AM | Reporte de 11am |
| 12:00 PM | 12:00 PM - 12:30 PM | Reporte de 12pm |
| 1:00 PM | 1:00 PM - 1:30 PM | Reporte de 1pm |
| 2:00 PM | 2:00 PM - 2:30 PM | Reporte de 2pm |
| 3:00 PM | 3:00 PM - 3:30 PM | Reporte de 3pm |
| 4:00 PM | 4:00 PM - 4:30 PM | Reporte de 4pm (cierre) |

## Reglas de Validación

### Backend (Python)

**Archivo**: `backend/services/reporte_participacion_service.py`

```python
# Calcular la ventana de tiempo permitida
hora_redondeada_objetivo = hora_reporte.replace(minute=0, second=0, microsecond=0)
inicio_ventana = hora_redondeada_objetivo
fin_ventana = hora_redondeada_objetivo.replace(minute=30)

# Validar que la hora actual esté dentro de la ventana
if not (inicio_ventana <= hora_actual <= fin_ventana):
    raise ValidationException({
        'hora_reporte': [
            f'El reporte de {hora_objetivo_str} solo se puede enviar entre {inicio_str} y {fin_str}. '
            f'Por favor espere hasta la ventana de tiempo correspondiente.'
        ]
    })
```

**Validaciones:**
1. La hora actual debe estar dentro de la ventana de 30 minutos
2. No se puede enviar un reporte fuera de su ventana
3. No se puede enviar un reporte de una hora futura
4. No se puede enviar un reporte de una hora pasada (ventana cerrada)

### Frontend (JavaScript)

**Archivo**: `frontend/static/js/testigo-participacion.js`

```javascript
function obtenerVentanaTiempo() {
    const ahora = new Date();
    const hora = ahora.getHours();
    const minutos = ahora.getMinutes();
    
    return {
        horaReporte: hora,
        enVentana: minutos <= 30,
        minutosRestantes: minutos <= 30 ? 30 - minutos : 0,
        proximaVentana: minutos > 30 ? hora + 1 : hora
    };
}
```

**Validaciones:**
1. Verificar ventana antes de abrir el modal
2. Verificar ventana antes de enviar el reporte
3. Mostrar mensaje si la ventana está cerrada
4. Indicar cuándo se abre la próxima ventana

## Interfaz de Usuario

### Indicador de Ventana en Dashboard

```
┌─────────────────────────────────────────────────┐
│ ⏰ Ventana de Tiempo: 9:00 AM - 9:30 AM (ABIERTA)│
│ Puede reportar ahora. Tiempo restante: 15 min   │
└─────────────────────────────────────────────────┘
```

**Estados:**
- **Verde (ABIERTA)**: Puede reportar ahora
- **Rojo (CERRADA)**: Ventana cerrada, muestra próxima ventana

### Modal de Reporte

```
┌─────────────────────────────────────────────────┐
│ 📤 Enviar Reporte de Participación              │
├─────────────────────────────────────────────────┤
│ ⚠️ Ventana de tiempo: 9:00 AM - 9:30 AM         │
│    Tiempo restante: 15 minutos                  │
│                                                 │
│ Hora del Reporte: [9:00 AM] (automático)       │
│ Personas Votadas: [___]                         │
│ Observaciones: [___]                            │
│                                                 │
│ [Cancelar]  [📤 Enviar Reporte]                 │
└─────────────────────────────────────────────────┘
```

**Características:**
- Hora del reporte es automática (no editable)
- Muestra ventana de tiempo actual
- Muestra tiempo restante
- Alerta si la ventana está por cerrar

### Mensajes de Error

**Ventana Cerrada:**
```
⚠️ La ventana de tiempo ha cerrado.
Próxima ventana: 10:00 AM - 10:30 AM
```

**Intentando Reportar Fuera de Ventana:**
```
❌ El reporte de 9:00 AM solo se puede enviar entre 9:00 AM y 9:30 AM.
Por favor espere hasta la ventana de tiempo correspondiente.
```

## Flujo de Usuario

### Caso 1: Usuario Reporta Dentro de Ventana

```
1. Usuario entra a pestaña "Participación"
   ↓
2. Ve indicador: "9:00 AM - 9:30 AM (ABIERTA)"
   ↓
3. Hace clic en "Reportar Participación"
   ↓
4. Modal se abre con hora automática: 9:00 AM
   ↓
5. Ingresa número de personas votadas
   ↓
6. Hace clic en "Enviar Reporte"
   ↓
7. ✅ Reporte enviado exitosamente
```

### Caso 2: Usuario Intenta Reportar Fuera de Ventana

```
1. Usuario entra a pestaña "Participación"
   ↓
2. Ve indicador: "Ventana cerrada"
   ↓
3. Ve: "Próxima ventana: 10:00 AM - 10:30 AM"
   ↓
4. Hace clic en "Reportar Participación"
   ↓
5. ⚠️ Sistema muestra alerta:
   "La ventana de tiempo ha cerrado.
    Próxima ventana: 10:00 AM - 10:30 AM"
   ↓
6. Modal NO se abre
   ↓
7. Usuario espera hasta la próxima ventana
```

### Caso 3: Ventana Se Cierra Mientras Usuario Está en Modal

```
1. Usuario abre modal a las 9:28 AM
   ↓
2. Ingresa datos
   ↓
3. A las 9:31 AM hace clic en "Enviar"
   ↓
4. ❌ Sistema valida y rechaza:
   "La ventana de tiempo ha cerrado.
    Próxima ventana: 10:00 AM - 10:30 AM"
   ↓
5. Usuario debe esperar hasta la próxima ventana
```

## Beneficios

### 1. Consolidación Correcta
- Todos los reportes de una hora se agrupan correctamente
- No hay confusión sobre a qué hora pertenece cada reporte

### 2. Sincronización
- Todas las mesas reportan en la misma ventana
- Los coordinadores ven datos consolidados por hora

### 3. Prevención de Errores
- No se pueden enviar reportes atrasados
- No se pueden enviar reportes adelantados
- No se pueden enviar múltiples reportes para la misma hora

### 4. Claridad para Usuarios
- Saben exactamente cuándo pueden reportar
- Ven cuánto tiempo les queda
- Saben cuándo es la próxima ventana

## Consideraciones Técnicas

### Zonas Horarias
- El sistema usa UTC en el backend
- El frontend convierte a hora local del usuario
- Las ventanas se calculan en hora local

### Actualización en Tiempo Real
- El indicador de ventana se actualiza cada 60 segundos
- Muestra tiempo restante en minutos
- Cambia de color según estado (verde/rojo)

### Validación Doble
- Frontend valida antes de abrir modal
- Frontend valida antes de enviar
- Backend valida al recibir el reporte
- Esto previene errores de sincronización de reloj

### Tolerancia
- La ventana es de exactamente 30 minutos
- No hay período de gracia adicional
- Esto asegura consistencia en todos los reportes

## Casos Especiales

### Primer Reporte del Día
- Ventana: 9:00 AM - 9:30 AM
- Es el primer reporte después de la apertura (8:00 AM)
- Da tiempo para que las mesas se organicen

### Último Reporte del Día
- Ventana: 4:00 PM - 4:30 PM
- Es el reporte de cierre
- Coincide con el cierre de votación (4:00 PM)

### Reporte Perdido
- Si un testigo no reporta en una ventana, pierde esa hora
- Debe esperar hasta la próxima ventana
- El sistema mostrará un "gap" en el histórico

### Múltiples Intentos
- Solo se permite un reporte por hora por mesa
- Si ya existe un reporte para esa hora, se rechaza
- El testigo debe esperar hasta la próxima hora

## Monitoreo y Alertas

### Para Coordinadores
- Ver qué mesas han reportado en la ventana actual
- Ver qué mesas NO han reportado
- Alertas automáticas si una mesa no reporta

### Para Monitoreo
- Dashboard con porcentaje de mesas que han reportado
- Mapa de calor de reportes recibidos
- Alertas si el porcentaje es bajo

## Implementación

### Fase 1: Backend ✅
- Validación de ventanas de tiempo
- Mensajes de error claros
- Cálculo de ventanas

### Fase 2: Frontend ✅
- Indicador de ventana en dashboard
- Validación antes de abrir modal
- Validación antes de enviar
- Actualización en tiempo real

### Fase 3: Monitoreo (Pendiente)
- Dashboard de coordinadores
- Alertas automáticas
- Estadísticas de reportes

## Pruebas

### Casos de Prueba

1. **Reportar dentro de ventana**: ✅ Debe funcionar
2. **Reportar fuera de ventana**: ❌ Debe rechazar
3. **Reportar en el minuto 30**: ✅ Debe funcionar (límite superior)
4. **Reportar en el minuto 31**: ❌ Debe rechazar
5. **Reportar dos veces en la misma hora**: ❌ Debe rechazar el segundo
6. **Cambio de hora mientras está en modal**: ❌ Debe rechazar si se cierra la ventana

## Documentación para Usuarios

### Guía Rápida para Testigos

**¿Cuándo puedo reportar?**
- Solo en los primeros 30 minutos de cada hora
- Ejemplo: Para reportar a las 9am, debe hacerlo entre 9:00am y 9:30am

**¿Qué pasa si pierdo la ventana?**
- Debe esperar hasta la próxima hora
- El sistema le mostrará cuándo es la próxima ventana

**¿Puedo reportar varias veces en la misma hora?**
- No, solo un reporte por hora por mesa

**¿Qué pasa si el sistema rechaza mi reporte?**
- Verifique que esté dentro de la ventana de tiempo
- Verifique que no haya reportado ya en esa hora
- Espere hasta la próxima ventana si es necesario
