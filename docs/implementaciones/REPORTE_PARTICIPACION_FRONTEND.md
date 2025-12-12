# Implementación Frontend - Reporte de Participación Horaria (E-11)
**Fecha:** 2025-12-08  
**Estado:** ✅ Frontend Testigo Completado  
**Fase:** 2 de 4

## Resumen

Se ha implementado completamente el frontend para testigos del sistema de Reporte de Participación Horaria (E-11). La pestaña de Participación es ahora la primera y principal del dashboard, ya que los testigos deben reportar cada hora.

## Cambios Realizados

### 1. Reorganización de Pestañas
**Archivo:** `frontend/templates/testigo/dashboard.html`

**Nuevo Orden:**
1. **Participación** (Principal) - Reportes cada hora
2. Formularios E-14 - Al final del día
3. Incidentes - Cuando ocurran
4. Delitos - Cuando ocurran

**Justificación:** La participación se reporta cada hora durante todo el día (8am-4pm), mientras que el formulario E-14 solo se envía una vez al final. Por eso Participación debe ser la pestaña principal.

### 2. Nueva Pestaña de Participación

**Elementos:**

#### A. Botón Principal
```html
<button class="btn btn-info" onclick="reportarParticipacion()">
    <i class="bi bi-plus-circle"></i> Reportar Participación
</button>
```

#### B. Instrucciones
- Horario de votación: 8:00 AM - 4:00 PM
- Frecuencia: Cada hora (ideal) o cada 2 horas (mínimo)
- Fuente: Formulario E-11 (registro de votantes)
- Dato: Número acumulado de personas que han votado

#### C. Histórico de Reportes
- Tabla con hora, personas votadas, porcentaje, observaciones
- Se actualiza automáticamente

#### D. Gráfico de Tendencia
- Gráfico de líneas con Chart.js
- Muestra evolución de participación por hora
- Solo se muestra si hay 2 o más reportes

#### E. Panel Lateral (Desktop)
- Información sobre el reporte
- Recordatorio de que los datos son acumulados
- Ejemplo de cómo reportar

### 3. Modal de Reporte

**Archivo:** `frontend/templates/testigo/dashboard.html`

**Campos:**
1. **Hora del Reporte** (datetime-local)
   - Se establece automáticamente a la hora actual
   - Se redondeará a la hora más cercana en el backend

2. **Personas que Han Votado** (number)
   - Total acumulado de personas que han votado
   - Mínimo: 0
   - Máximo: Votantes registrados

3. **Observaciones** (textarea, opcional)
   - Notas sobre el flujo de votantes
   - Ej: "Flujo normal", "Alta afluencia", etc.

4. **Información Calculada** (automática)
   - Votantes registrados
   - Porcentaje de participación

### 4. JavaScript

**Archivo:** `frontend/static/js/testigo-participacion.js`

**Funciones Principales:**

#### `reportarParticipacion()`
- Abre el modal de reporte
- Verifica que haya presencia verificada
- Establece hora actual
- Calcula porcentaje al cambiar personas votadas

#### `guardarReporteParticipacion()`
- Valida datos del formulario
- Envía al endpoint POST `/api/reporte-participacion`
- Muestra mensajes de éxito/error
- Recarga lista de reportes

#### `cargarReportesParticipacion()`
- Obtiene reportes del endpoint GET `/api/reporte-participacion/mesa/{id}`
- Muestra tabla de reportes
- Genera gráfico si hay datos

#### `mostrarReportesParticipacion(data)`
- Renderiza tabla HTML con reportes
- Formatea fechas y porcentajes
- Muestra mensaje si no hay reportes

#### `mostrarGraficoParticipacion(reportes)`
- Crea gráfico de líneas con Chart.js
- Muestra evolución de participación
- Destruye gráfico anterior si existe

### 5. Carga Automática

**Comportamiento:**
- Los reportes se cargan automáticamente al iniciar (después de 2 segundos)
- También se cargan al cambiar a la pestaña de Participación
- Se recarga la lista después de guardar un nuevo reporte

### 6. Navegación Móvil

**Actualizada:**
- Participación es el primer botón (activo por defecto)
- Icono: `bi-people-fill`
- Orden: Participación → Formularios → Incidentes → Delitos

## Flujo de Uso

### 1. Testigo Inicia Sesión
1. Dashboard se abre en pestaña "Participación" (principal)
2. Se cargan automáticamente los reportes existentes
3. Ve histórico de reportes del día

### 2. Testigo Reporta Participación (Cada Hora)
1. Hace clic en "Reportar Participación"
2. Modal se abre con hora actual
3. Cuenta firmas en E-11
4. Ingresa número total de personas que han votado
5. (Opcional) Agrega observaciones
6. Ve porcentaje calculado automáticamente
7. Hace clic en "Guardar Reporte"
8. Sistema valida y guarda
9. Lista se actualiza automáticamente
10. Gráfico se actualiza si hay 2+ reportes

### 3. Testigo Ve Tendencia
1. Tabla muestra todos los reportes del día
2. Gráfico muestra evolución visual
3. Puede ver si la participación es normal, lenta o rápida

## Validaciones Frontend

1. **Presencia Verificada:**
   - No puede reportar sin verificar presencia
   - Mensaje: "Debe verificar su presencia en una mesa primero"

2. **Campos Requeridos:**
   - Hora del reporte
   - Personas votadas

3. **Cálculo Automático:**
   - Porcentaje de participación
   - Se muestra en tiempo real al escribir

## Validaciones Backend (Ya Implementadas)

1. Hora entre 8:00 AM y 4:00 PM
2. Hora no futura
3. Personas votadas >= 0
4. Personas votadas <= votantes registrados
5. Personas votadas >= reporte anterior (acumulado)
6. Solo un reporte por hora

## Ejemplo de Uso Real

### Escenario: Día de Votación

**8:00 AM** - Apertura
- Testigo verifica presencia
- Dashboard abre en pestaña "Participación"

**9:00 AM** - Primer Reporte
- Cuenta 45 firmas en E-11
- Reporta: 45 personas votadas
- Sistema calcula: 4.5% de participación

**10:00 AM** - Segundo Reporte
- Cuenta 120 firmas en total (45 + 75 nuevas)
- Reporta: 120 personas votadas (acumulado)
- Sistema calcula: 12% de participación
- Gráfico se muestra con tendencia

**11:00 AM** - Tercer Reporte
- Cuenta 210 firmas en total
- Reporta: 210 personas votadas
- Sistema calcula: 21% de participación
- Gráfico muestra tendencia creciente

**...continúa cada hora hasta 4:00 PM**

**4:00 PM** - Cierre
- Último reporte de participación
- Luego pasa a pestaña "Formularios E-14" para enviar resultados finales

## Integración con Chart.js

**Librería:** Chart.js (ya incluida en base.html)

**Configuración:**
```javascript
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['9:00', '10:00', '11:00', ...],
        datasets: [{
            label: 'Personas que Han Votado',
            data: [45, 120, 210, ...],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1,
            fill: true
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
```

## Archivos Modificados

1. ✅ `frontend/templates/testigo/dashboard.html`
   - Reorganizadas pestañas (Participación primera)
   - Agregado contenido de pestaña Participación
   - Agregado modal de reporte
   - Actualizada navegación móvil

2. ✅ `frontend/static/js/testigo-participacion.js` (NUEVO)
   - Funciones de reporte
   - Carga de datos
   - Renderizado de tabla
   - Generación de gráfico

## Próximos Pasos

### Fase 3: Frontend Coordinadores (Pendiente)
- [ ] Vista de participación en coordinador de puesto
- [ ] Tabla de mesas con último reporte
- [ ] Alertas de mesas sin reportes
- [ ] Mapa de calor en coordinador municipal

### Fase 4: Monitoreo (Pendiente)
- [ ] Dashboard de participación nacional
- [ ] Estadísticas en tiempo real
- [ ] Sistema de alertas automáticas
- [ ] Proyecciones de participación final

## Pruebas Recomendadas

1. **Verificar Orden de Pestañas:**
   - Participación debe ser la primera
   - Debe estar activa por defecto

2. **Crear Reporte:**
   - Abrir modal
   - Ingresar datos
   - Verificar cálculo de porcentaje
   - Guardar y verificar que aparece en lista

3. **Ver Gráfico:**
   - Crear 2 o más reportes
   - Verificar que aparece gráfico
   - Verificar que muestra tendencia correcta

4. **Validaciones:**
   - Intentar reportar sin presencia verificada
   - Verificar mensajes de error

5. **Responsive:**
   - Verificar en móvil
   - Verificar navegación inferior
   - Verificar que Participación es el primer botón

## Notas Técnicas

- Los reportes son **acumulados**, no incrementales
- La hora se redondea automáticamente en el backend
- El porcentaje se calcula en tiempo real en el frontend
- El gráfico solo se muestra si hay 2 o más reportes
- Chart.js se usa para visualización de tendencias

## Estado Actual

✅ **Backend Completado (Fase 1)**
✅ **Frontend Testigo Completado (Fase 2)**
⏳ **Pendiente (Fases 3-4)**
- Frontend coordinadores
- Dashboard monitoreo
