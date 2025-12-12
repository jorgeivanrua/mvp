# Corrección Cálculo de Votos en Dashboard Testigos
**Fecha:** 2025-12-08  
**Estado:** ✅ Completado

## Problema Identificado

El usuario reportó que en el dashboard de testigos:
- Los votos por partido y candidatos se suman internamente pero **no se muestran visiblemente**
- El badge del total por partido no se actualiza correctamente
- Los totales no aparecen aunque los cálculos se ejecutan

### Causa Raíz

1. **Falta de inicialización de `votosData`** en `renderVotacionConPestanas()`:
   - La función `renderVotacionTradicional()` SÍ inicializaba `votosData` para cada partido
   - La función `renderVotacionConPestanas()` NO lo hacía
   - Esto causaba que `calcularTotales()` no tuviera la estructura correcta

2. **Timing del cálculo inicial**:
   - `calcularTotales()` se ejecutaba antes de que el DOM estuviera completamente renderizado
   - Los badges `total_partido_${partidoId}` no existían cuando se intentaban actualizar

3. **Falta de logging detallado**:
   - No había suficiente información de debugging para identificar el problema

## Solución Implementada

### 1. Inicialización de `votosData` en `renderVotacionConPestanas()`

**Archivo:** `frontend/static/js/testigo-dashboard-v2.js`

Agregado al final de la función (después de `container.innerHTML = html;`):

```javascript
// ⭐ IMPORTANTE: Inicializar votosData para cada partido
partidos.forEach(partido => {
    const candidatos = candidatosPorPartido[partido.id] || [];
    votosData[partido.id] = {
        partido: partido,
        votosPartido: 0,
        candidatos: candidatos.map(c => ({ ...c, votos: 0 })),
        total: 0,
        esUninominal: esUninominal
    };
});

console.log('✅ votosData inicializado:', votosData);
```

### 2. Llamada a `calcularTotales()` después de renderizar

**Archivo:** `frontend/static/js/testigo-dashboard-v2.js`

Agregado al final de `renderVotacionForm()`:

```javascript
// ⭐ IMPORTANTE: Llamar calcularTotales() después de renderizar para inicializar los badges
// Usar setTimeout para asegurar que el DOM esté completamente actualizado
setTimeout(() => {
    console.log('🔄 Inicializando totales después de renderizar...');
    calcularTotales();
}, 100);
```

### 3. Logging mejorado en `calcularTotales()`

**Archivo:** `frontend/static/js/testigo-dashboard-v2.js`

Mejorado el logging al actualizar badges:

```javascript
// Actualizar display del total del partido
const totalSpan = document.getElementById(`total_partido_${partidoId}`);
console.log(`[calcularTotales] Badge total_partido_${partidoId}:`, totalSpan ? 'ENCONTRADO' : 'NO ENCONTRADO');
if (totalSpan) {
    const valorFormateado = Utils.formatNumber(data.total);
    totalSpan.textContent = valorFormateado;
    console.log(`[calcularTotales] ✅ Badge actualizado a: ${valorFormateado}`);
} else {
    console.error(`[calcularTotales] ❌ No se encontró el badge total_partido_${partidoId} en el DOM`);
}
```

## Fórmulas de Cálculo (Confirmadas)

Las fórmulas ya estaban correctas en el código:

```
Votos Válidos = Suma de todos los votos de partidos (partido + candidatos)
Total Votos = Votos Válidos + Votos Nulos + Votos en Blanco
Total Tarjetas = Total Votos + Tarjetas No Marcadas
```

**IMPORTANTE:** Los votos en blanco NO se incluyen en votos válidos (solo se suman al total de votos).

## Estructura del Badge del Total

El badge se muestra en cada pestaña de partido con:

```html
<div class="mt-3 pt-3 border-top">
    <div class="row align-items-center">
        <div class="col-8">
            <strong class="fs-5">Total ${partido.sigla}:</strong>
            <br><small class="text-muted">(Votos partido + Votos candidatos)</small>
        </div>
        <div class="col-4 text-end">
            <span id="total_partido_${partido.id}" class="badge bg-primary fs-4 px-3 py-2">0</span>
        </div>
    </div>
</div>
```

## Archivos Modificados

- ✅ `frontend/static/js/testigo-dashboard-v2.js`
  - Función `renderVotacionConPestanas()` - Agregada inicialización de `votosData`
  - Función `renderVotacionForm()` - Agregada llamada a `calcularTotales()` con timeout
  - Función `calcularTotales()` - Mejorado logging
  - Función `saveForm()` - Agregadas validaciones de seguridad para `votosData`

## Correcciones Adicionales (Error al Enviar)

### Problema
Al intentar enviar el formulario, se generaba un error porque:
- `votosData` podía estar vacío o no inicializado
- No había validación de que `data.candidatos` existiera antes de iterar

### Solución
1. **Validación antes de enviar**:
```javascript
// Validar que haya datos de votación
if (!votosData || Object.keys(votosData).length === 0) {
    Utils.showError('Debe seleccionar un tipo de elección y cargar los partidos primero');
    return;
}
```

2. **Validaciones de seguridad en construcción de votos**:
```javascript
Object.keys(votosData).forEach(partidoId => {
    const data = votosData[partidoId];
    
    if (!data) {
        console.warn(`[saveForm] No hay datos para partido ${partidoId}`);
        return;
    }
    
    // Votos del partido
    if (data.votosPartido && data.votosPartido > 0) {
        votosPartidos.push({
            partido_id: parseInt(partidoId),
            votos: data.votosPartido
        });
    }
    
    // Votos de candidatos
    if (data.candidatos && Array.isArray(data.candidatos)) {
        data.candidatos.forEach(candidato => {
            if (candidato.votos > 0) {
                votosCandidatos.push({
                    candidato_id: candidato.id,
                    votos: candidato.votos
                });
            }
        });
    }
});
```

3. **Logging mejorado**:
```javascript
console.log('[saveForm] votosData:', votosData);
console.log('[saveForm] votosPartidos:', votosPartidos);
console.log('[saveForm] votosCandidatos:', votosCandidatos);
```

## Pruebas Recomendadas

1. **Crear nuevo formulario E-14**:
   - Seleccionar tipo de elección con muchos candidatos (>20)
   - Verificar que se muestren pestañas por partido
   - Ingresar votos en "Votos solo partido"
   - Ingresar votos en candidatos
   - **Verificar que el badge del total se actualice automáticamente**

2. **Verificar cálculos**:
   - El total por partido debe ser: votos partido + suma de votos candidatos
   - Los votos válidos deben ser: suma de todos los totales de partidos
   - El total de votos debe ser: votos válidos + votos nulos + votos en blanco

3. **Verificar en consola**:
   - Abrir DevTools (F12)
   - Ver logs de `[calcularTotales]`
   - Verificar que los badges se encuentren y actualicen correctamente

## Corrección Adicional: Error 422 al Enviar

### Problema 1: Totales no calculados antes de enviar
Al intentar enviar el formulario, el backend rechazaba los datos con error 422 (UNPROCESSABLE ENTITY) porque:
- Los totales no coincidían con las validaciones del backend
- `calcularTotales()` no se ejecutaba antes de enviar
- Los valores de los inputs podían estar desactualizados

### Problema 2: Usuario no ingresaba "Tarjetas No Marcadas"
El usuario debe ingresar manualmente el valor de "Tarjetas No Marcadas" del formulario E-14 físico:
- Si el usuario no ingresa el valor, queda en 0
- La validación falla: `total_votos + tarjetas_no_marcadas ≠ total_tarjetas`
- Ejemplo: 383 votos + 0 no marcadas = 383, pero total_tarjetas puede ser mayor

**IMPORTANTE:** Las "Tarjetas No Marcadas" son tarjetas que SÍ se depositaron en la urna pero NO tienen ninguna marca (ni partido, ni candidato, ni nada). Son diferentes de:
- **Votos en Blanco**: Tarjetas marcadas intencionalmente como "voto en blanco"
- **Abstención**: Personas que no fueron a votar (no depositaron tarjeta)

### Validaciones del Backend
El backend valida que:
```python
# 1. votos_validos + votos_nulos + votos_blanco = total_votos
total_calculado = votos_validos + votos_nulos + votos_blanco
if total_calculado != total_votos:
    raise ValidationException()

# 2. total_votos + tarjetas_no_marcadas = total_tarjetas
total_tarjetas_calculado = total_votos + tarjetas_no_marcadas
if total_tarjetas_calculado != total_tarjetas:
    raise ValidationException()

# 3. total_votos <= total_votantes_registrados
if total_votos > total_votantes_registrados:
    raise ValidationException()
```

### Solución
1. **Ejecutar `calcularTotales()` antes de enviar**:
2. **Calcular automáticamente "Tarjetas No Marcadas"**:

#### 1. Ejecutar calcularTotales() antes de enviar:
```javascript
try {
    // ⭐ IMPORTANTE: Calcular totales ANTES de enviar para asegurar coherencia
    console.log('[saveForm] Calculando totales antes de enviar...');
    calcularTotales();
    
    const formData = new FormData(form);
    // ... resto del código
}
```

#### 2. El usuario DEBE ingresar "Tarjetas No Marcadas" manualmente:

**NO se calcula automáticamente** porque el testigo debe contarlas del formulario E-14 físico.

**Fórmulas correctas:**
```
Total Votos = Votos Válidos + Votos Nulos + Votos en Blanco
Total Tarjetas = Total Votos + Tarjetas No Marcadas
Total Tarjetas ≤ Votantes Registrados
```

**Ejemplo Real:**
```
Votantes Registrados: 1000 personas habilitadas
Votaron: 950 personas (50 no fueron a votar = abstención)

De las 950 tarjetas depositadas en la urna:
- 900 votos válidos (por partidos/candidatos)
- 30 votos nulos (mal marcados)
- 10 votos en blanco (marcaron "voto en blanco")
- 10 tarjetas no marcadas (depositaron sin marcar nada)

Cálculos:
✅ Total Votos = 900 + 30 + 10 = 940
✅ Total Tarjetas = 940 + 10 = 950
✅ 950 ≤ 1000 (válido, 50 personas no votaron)
```

**Diferencias importantes:**
- **Votos en Blanco**: Tarjeta marcada intencionalmente como "voto en blanco" (cuenta como voto)
- **Tarjetas No Marcadas**: Tarjeta depositada sin ninguna marca (cuenta como tarjeta pero no como voto)
- **Abstención**: Persona que no fue a votar (no depositó tarjeta)

#### 3. Logging detallado de validación:
```javascript
console.log('[saveForm] ===== DATOS A ENVIAR =====');
console.log('[saveForm] Validación: votos_validos + nulos + blanco =', 
    data.votos_validos + data.votos_nulos + data.votos_blanco, 
    '(debe ser igual a total_votos:', data.total_votos + ')');
console.log('[saveForm] Validación: total_votos + tarjetas_no_marcadas =', 
    data.total_votos + data.tarjetas_no_marcadas, 
    '(debe ser igual a total_tarjetas:', data.total_tarjetas + ')');
```

## Resultado Esperado

✅ El badge del total por partido ahora debe:
- Mostrarse correctamente en cada pestaña
- Actualizarse automáticamente al cambiar votos
- Mostrar la suma de votos partido + votos candidatos
- Incluir descripción "(Votos partido + Votos candidatos)"

✅ El envío del formulario ahora debe:
- Calcular totales automáticamente antes de enviar
- Validar coherencia de datos
- Mostrar logs detallados para debugging
- Pasar las validaciones del backend

## Notas Técnicas

- El timeout de 100ms es necesario porque `innerHTML` no actualiza el DOM inmediatamente
- La inicialización de `votosData` debe hacerse DESPUÉS de renderizar el HTML
- El logging detallado ayuda a identificar problemas de timing en el futuro
- `calcularTotales()` debe ejecutarse ANTES de enviar para asegurar coherencia con las validaciones del backend
