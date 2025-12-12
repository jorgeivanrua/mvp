# Guía de Prueba - Formulario E-14
**Fecha:** 2025-12-08  
**Objetivo:** Verificar que el formulario E-14 calcule correctamente y se envíe sin errores

## Pre-requisitos

1. ✅ Servidor corriendo (`python run.py` o similar)
2. ✅ Usuario testigo creado y con mesa asignada
3. ✅ Tipos de elección configurados
4. ✅ Partidos y candidatos registrados

## Pasos de Prueba

### 1. Iniciar Sesión como Testigo

1. Ir a `http://localhost:5000/login`
2. Ingresar credenciales de testigo
3. Verificar que cargue el dashboard

### 2. Verificar Presencia

1. Seleccionar una mesa del dropdown
2. Hacer clic en "Verificar Mi Presencia"
3. Verificar que aparezca el mensaje de éxito
4. Verificar que el botón "Nuevo Formulario" se habilite

### 3. Abrir Formulario E-14

1. Hacer clic en "Nuevo Formulario" (desktop) o "Capturar Formulario E-14" (móvil)
2. Verificar que se abra el modal
3. Verificar que la mesa esté pre-seleccionada

### 4. Llenar Datos Básicos

1. **Seleccionar Tipo de Elección**: Ej. "Alcalde"
2. **Esperar** a que carguen los partidos y candidatos
3. **Verificar** que aparezcan las pestañas de partidos

### 5. Ingresar Votos (Ejemplo Real)

**Escenario:** Mesa con 500 votantes registrados

#### Datos de Control:
```
Votantes Registrados: 500 (automático desde DIVIPOLA)
Votos Nulos: 15
Votos en Blanco: 5
Tarjetas No Marcadas: 50
```

#### Votos por Partido (ejemplo con 3 partidos):

**Partido 1 - Liberal:**
- Votos solo partido: 50
- Candidato 1: 30
- Candidato 2: 20
- **Total Partido 1: 100** ← Debe aparecer automáticamente

**Partido 2 - Conservador:**
- Votos solo partido: 40
- Candidato 1: 35
- Candidato 2: 25
- **Total Partido 2: 100** ← Debe aparecer automáticamente

**Partido 3 - Verde:**
- Votos solo partido: 60
- Candidato 1: 50
- Candidato 2: 40
- Candidato 3: 40
- **Total Partido 3: 190** ← Debe aparecer automáticamente

### 6. Verificar Cálculos Automáticos

Después de ingresar todos los votos, verificar que los totales sean:

```
✅ Votos Válidos: 390 (100 + 100 + 190)
✅ Total Votos: 410 (390 + 15 + 5)
✅ Total Tarjetas: 460 (410 + 50)
```

**IMPORTANTE:** 
- Total Tarjetas (460) < Votantes Registrados (500) ✅ CORRECTO
- Esto significa que 40 personas no votaron (abstención)

### 7. Verificar en Consola del Navegador

Abrir DevTools (F12) y verificar en la pestaña Console:

```
[calcularTotales] Iniciando cálculo...
[calcularTotales] Partido 1 - Total: 100 (partido: 50 + candidatos: 50)
[calcularTotales] Partido 2 - Total: 100 (partido: 40 + candidatos: 60)
[calcularTotales] Partido 3 - Total: 190 (partido: 60 + candidatos: 130)
[calcularTotales] Total votos válidos: 390
[calcularTotales] ✅ Badge actualizado a: 100
[calcularTotales] ✅ Badge actualizado a: 100
[calcularTotales] ✅ Badge actualizado a: 190
```

### 8. Enviar Formulario

1. Hacer clic en "Enviar Formulario"
2. **Verificar en consola** que aparezcan los logs:

```
[saveForm] Calculando totales antes de enviar...
[saveForm] ===== DATOS A ENVIAR =====
[saveForm] Votos válidos: 390
[saveForm] Votos nulos: 15
[saveForm] Votos blanco: 5
[saveForm] Total votos: 410
[saveForm] Tarjetas no marcadas: 50
[saveForm] Total tarjetas: 460
[saveForm] Validación: votos_validos + nulos + blanco = 410 (debe ser igual a total_votos: 410)
[saveForm] Validación: total_votos + tarjetas_no_marcadas = 460 (debe ser igual a total_tarjetas: 460)
```

3. **Verificar respuesta exitosa**:
```
✓ Formulario E-14 enviado exitosamente para revisión
```

4. **Verificar que el modal se cierre**
5. **Verificar que el formulario aparezca en la tabla** con estado "Pendiente"

## Casos de Error a Probar

### Error 1: Totales No Coinciden

**Escenario:** Modificar manualmente un total

1. Ingresar votos normalmente
2. Cambiar manualmente el campo "Total Votos" a un valor incorrecto
3. Intentar enviar
4. **Resultado esperado:** Error 422 con mensaje de validación

### Error 2: Más Votos que Votantes

**Escenario:** Ingresar más votos que votantes registrados

1. Ingresar votos que sumen más de 500
2. Intentar enviar
3. **Resultado esperado:** Error 422 indicando que excede votantes registrados

### Error 3: Sin Tipo de Elección

**Escenario:** Intentar enviar sin seleccionar tipo de elección

1. No seleccionar tipo de elección
2. Intentar enviar
3. **Resultado esperado:** Mensaje "Debe seleccionar un tipo de elección y cargar los partidos primero"

## Verificación en Base de Datos

Después de enviar exitosamente, verificar en la BD:

### Tabla `formulario_e14`:
```sql
SELECT * FROM formulario_e14 WHERE testigo_id = [tu_testigo_id] ORDER BY created_at DESC LIMIT 1;
```

Debe mostrar:
- `estado`: 'pendiente'
- `total_votos`: 410
- `votos_validos`: 390
- `votos_nulos`: 15
- `votos_blanco`: 5
- `total_tarjetas`: 460

### Tabla `voto_partido`:
```sql
SELECT * FROM voto_partido WHERE formulario_id = [formulario_id];
```

Debe mostrar 3 registros con votos: 50, 40, 60

### Tabla `voto_candidato`:
```sql
SELECT * FROM voto_candidato WHERE formulario_id = [formulario_id];
```

Debe mostrar 7 registros (2+2+3 candidatos) con sus respectivos votos

## Verificación en Coordinador de Puesto

1. Iniciar sesión como coordinador de puesto
2. Ir a la sección de formularios
3. **Verificar** que aparezca el formulario con estado "Pendiente"
4. **Verificar** que se puedan ver los detalles completos
5. **Verificar** que se pueda validar o rechazar

## Checklist Final

- [ ] El badge del total por partido se muestra correctamente
- [ ] El badge se actualiza automáticamente al cambiar votos
- [ ] Los totales automáticos (Votos Válidos, Total Votos, Total Tarjetas) se calculan correctamente
- [ ] Los logs en consola muestran los cálculos correctos
- [ ] El formulario se envía sin errores 422
- [ ] El formulario aparece en la tabla con estado "Pendiente"
- [ ] Los datos se guardan correctamente en la BD
- [ ] El coordinador de puesto puede ver el formulario

## Problemas Comunes y Soluciones

### Problema: Badge no se actualiza
**Solución:** Verificar en consola que aparezca "✅ Badge actualizado". Si no aparece, puede ser un problema de timing.

### Problema: Error 422 al enviar
**Solución:** Verificar en consola los logs de validación. Los totales deben coincidir exactamente.

### Problema: "Debe seleccionar un tipo de elección"
**Solución:** Asegurarse de seleccionar un tipo de elección y esperar a que carguen los partidos.

### Problema: Botón "Nuevo Formulario" deshabilitado
**Solución:** Verificar presencia primero. El botón solo se habilita después de verificar presencia.

## Notas Importantes

1. **No todas las personas votan**: Es normal que Total Tarjetas < Votantes Registrados
2. **No todos los votos son válidos**: Votos Válidos + Nulos + Blanco = Total Votos
3. **Tarjetas no marcadas**: Son las tarjetas que no se usaron (abstención)
4. **Cálculos automáticos**: Se ejecutan automáticamente al cambiar cualquier valor
5. **Validación antes de enviar**: `calcularTotales()` se ejecuta automáticamente antes de enviar

## Resultado Esperado

✅ Formulario E-14 creado exitosamente  
✅ Datos guardados en BD  
✅ Visible para coordinador de puesto  
✅ Listo para validación  
✅ Contribuye al consolidado municipal (E-24)
