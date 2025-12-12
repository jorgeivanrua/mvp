# Conceptos del Formulario E-14
**Fecha:** 2025-12-08  
**Propósito:** Explicar los conceptos electorales del formulario E-14

## Campos del Formulario E-14

### 1. Votantes Registrados
**Definición:** Total de personas habilitadas para votar en esta mesa según el censo electoral (DIVIPOLA).

**Características:**
- ✅ Se carga automáticamente desde la base de datos
- ✅ Campo de solo lectura
- ✅ Representa el máximo de votos posibles

**Ejemplo:** 1000 personas registradas en la mesa

---

### 2. Votos Válidos
**Definición:** Votos emitidos correctamente por partidos políticos y/o candidatos.

**Cálculo:**
```
Votos Válidos = Suma de todos los votos por partidos + Suma de todos los votos por candidatos
```

**Características:**
- ✅ Se calcula automáticamente
- ✅ Campo de solo lectura
- ✅ NO incluye votos nulos ni votos en blanco

**Ejemplo:** 900 votos válidos

---

### 3. Votos Nulos
**Definición:** Tarjetas depositadas que fueron marcadas incorrectamente y no se pueden contar.

**Ejemplos de votos nulos:**
- Tarjeta marcada en múltiples opciones cuando solo se permite una
- Tarjeta con marcas ambiguas o ilegibles
- Tarjeta con mensajes o dibujos que invalidan el voto
- Tarjeta dañada o alterada

**Características:**
- ❌ El usuario DEBE ingresar este valor manualmente
- ❌ Se cuenta del formulario E-14 físico
- ✅ Cuenta como voto emitido (la persona sí votó)

**Ejemplo:** 30 votos nulos

---

### 4. Votos en Blanco
**Definición:** Tarjetas depositadas donde el votante marcó intencionalmente la opción "VOTO EN BLANCO".

**Características:**
- ❌ El usuario DEBE ingresar este valor manualmente
- ❌ Se cuenta del formulario E-14 físico
- ✅ Cuenta como voto emitido (la persona sí votó)
- ✅ Es diferente de "Tarjetas No Marcadas"

**Diferencia con Tarjetas No Marcadas:**
- **Voto en Blanco**: El votante MARCÓ la opción "voto en blanco" (intencional)
- **Tarjeta No Marcada**: El votante NO marcó nada (puede ser error u olvido)

**Ejemplo:** 10 votos en blanco

---

### 5. Total Votos
**Definición:** Total de votos emitidos en la mesa.

**Cálculo:**
```
Total Votos = Votos Válidos + Votos Nulos + Votos en Blanco
```

**Características:**
- ✅ Se calcula automáticamente
- ✅ Campo de solo lectura
- ✅ Representa cuántas personas votaron (excluyendo tarjetas no marcadas)

**Ejemplo:** 900 + 30 + 10 = 940 votos

---

### 6. Tarjetas No Marcadas
**Definición:** Tarjetas que SÍ fueron depositadas en la urna pero NO tienen ninguna marca (ni partido, ni candidato, ni voto en blanco).

**Características:**
- ❌ El usuario DEBE ingresar este valor manualmente
- ❌ Se cuenta del formulario E-14 físico
- ✅ Cuenta como tarjeta depositada
- ❌ NO cuenta como voto emitido

**Posibles causas:**
- Votante depositó la tarjeta por error sin marcar
- Votante no quiso marcar ninguna opción (diferente de voto en blanco)
- Tarjeta en blanco depositada accidentalmente

**Diferencia con Voto en Blanco:**
- **Voto en Blanco**: Tarjeta MARCADA con la opción "voto en blanco" ✅ Cuenta como voto
- **Tarjeta No Marcada**: Tarjeta SIN NINGUNA marca ❌ NO cuenta como voto

**Ejemplo:** 10 tarjetas no marcadas

---

### 7. Total Tarjetas
**Definición:** Total de tarjetas depositadas en la urna.

**Cálculo:**
```
Total Tarjetas = Total Votos + Tarjetas No Marcadas
```

**Características:**
- ✅ Se calcula automáticamente
- ✅ Campo de solo lectura
- ✅ Debe ser ≤ Votantes Registrados

**Ejemplo:** 940 + 10 = 950 tarjetas

---

## Validaciones del Sistema

### Validación 1: Suma de Votos
```
Votos Válidos + Votos Nulos + Votos en Blanco = Total Votos
```

**Ejemplo:**
```
900 + 30 + 10 = 940 ✅
```

### Validación 2: Suma de Tarjetas
```
Total Votos + Tarjetas No Marcadas = Total Tarjetas
```

**Ejemplo:**
```
940 + 10 = 950 ✅
```

### Validación 3: No Exceder Votantes
```
Total Tarjetas ≤ Votantes Registrados
```

**Ejemplo:**
```
950 ≤ 1000 ✅
```

---

## Ejemplo Completo

### Escenario Real:

**Mesa con 1000 votantes registrados**

**Participación:**
- 950 personas fueron a votar
- 50 personas NO fueron a votar (abstención)

**De las 950 tarjetas depositadas:**
- 900 votos válidos (por partidos/candidatos)
- 30 votos nulos (mal marcados)
- 10 votos en blanco (marcaron "voto en blanco")
- 10 tarjetas no marcadas (sin ninguna marca)

**Cálculos:**

```
Votos Válidos: 900 (automático)
Votos Nulos: 30 (manual)
Votos en Blanco: 10 (manual)
Tarjetas No Marcadas: 10 (manual)

Total Votos = 900 + 30 + 10 = 940 (automático)
Total Tarjetas = 940 + 10 = 950 (automático)

Validaciones:
✅ 900 + 30 + 10 = 940
✅ 940 + 10 = 950
✅ 950 ≤ 1000
```

**Interpretación:**
- 950 personas votaron (participación: 95%)
- 50 personas no votaron (abstención: 5%)
- De los 950 que votaron:
  * 900 votos válidos (94.7%)
  * 30 votos nulos (3.2%)
  * 10 votos en blanco (1.1%)
  * 10 tarjetas no marcadas (1.1%)

---

## Campos que el Usuario DEBE Ingresar Manualmente

1. ❌ **Votos Nulos** - Del formulario E-14 físico
2. ❌ **Votos en Blanco** - Del formulario E-14 físico
3. ❌ **Tarjetas No Marcadas** - Del formulario E-14 físico
4. ❌ **Votos por Partido** - Del formulario E-14 físico
5. ❌ **Votos por Candidato** - Del formulario E-14 físico

## Campos Calculados Automáticamente

1. ✅ **Votantes Registrados** - Desde DIVIPOLA
2. ✅ **Votos Válidos** - Suma de votos por partidos y candidatos
3. ✅ **Total Votos** - Votos válidos + nulos + en blanco
4. ✅ **Total Tarjetas** - Total votos + tarjetas no marcadas
5. ✅ **Total por Partido** - Votos partido + votos candidatos del partido

---

## Errores Comunes

### Error 1: Confundir "Voto en Blanco" con "Tarjeta No Marcada"
❌ **Incorrecto:** Contar tarjetas sin marca como votos en blanco  
✅ **Correcto:** 
- Voto en Blanco = Tarjeta MARCADA con opción "voto en blanco"
- Tarjeta No Marcada = Tarjeta SIN NINGUNA marca

### Error 2: No ingresar "Tarjetas No Marcadas"
❌ **Incorrecto:** Dejar el campo en 0 cuando hay tarjetas no marcadas  
✅ **Correcto:** Contar y registrar todas las tarjetas no marcadas del E-14 físico

### Error 3: Pensar que Total Tarjetas = Votantes Registrados
❌ **Incorrecto:** Asumir que todos votaron  
✅ **Correcto:** Total Tarjetas ≤ Votantes Registrados (puede haber abstención)

### Error 4: Incluir abstención en "Tarjetas No Marcadas"
❌ **Incorrecto:** Contar personas que no votaron como tarjetas no marcadas  
✅ **Correcto:** Solo contar tarjetas que SÍ fueron depositadas en la urna

---

## Flujo de Llenado del Formulario

1. **Seleccionar Mesa** - Se carga automáticamente "Votantes Registrados"
2. **Seleccionar Tipo de Elección** - Se cargan partidos y candidatos
3. **Ingresar Votos por Partido** - Para cada partido
4. **Ingresar Votos por Candidato** - Para cada candidato
5. **Verificar Total por Partido** - Se calcula automáticamente (partido + candidatos)
6. **Ingresar Votos Nulos** - Del E-14 físico
7. **Ingresar Votos en Blanco** - Del E-14 físico
8. **Ingresar Tarjetas No Marcadas** - Del E-14 físico
9. **Verificar Totales** - Se calculan automáticamente
10. **Enviar Formulario** - Se validan las sumas

---

## Conclusión

El formulario E-14 digital replica exactamente el formulario E-14 físico, con la ventaja de:
- ✅ Calcular automáticamente los totales
- ✅ Validar que las sumas sean correctas
- ✅ Prevenir errores de digitación
- ✅ Consolidar datos en tiempo real

El testigo debe transcribir fielmente los datos del formulario físico al sistema digital.
