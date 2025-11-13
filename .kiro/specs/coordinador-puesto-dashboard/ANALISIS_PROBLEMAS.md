# Análisis de Problemas - Dashboard Coordinador de Puesto

## Fecha: 2025-11-12

## Problemas Identificados

### 1. Verificación de Presencia del Testigo No Se Muestra

**Descripción:**
La verificación de presencia del testigo no se está mostrando correctamente en el dashboard del coordinador de puesto, aunque el código frontend ya tiene la lógica para mostrar el ícono de presencia.

**Análisis:**
- El código JavaScript en `coordinador-puesto.js` línea ~700 ya incluye lógica para mostrar el ícono de presencia:
  ```javascript
  const presenciaIcon = mesa.testigo_presente ? 
    '<i class="bi bi-check-circle-fill text-success"></i>' : 
    '<i class="bi bi-person"></i>';
  ```
- El endpoint `/api/formularios/mesas` en `backend/routes/formularios_e14.py` línea ~280 ya incluye los campos:
  ```python
  'testigo_presente': testigo.presencia_verificada if testigo else False,
  'testigo_presente_desde': testigo.presencia_verificada_at.isoformat() if testigo and testigo.presencia_verificada_at else None,
  ```

**Causa Probable:**
- El modelo `User` puede no tener los campos `presencia_verificada` y `presencia_verificada_at`
- El endpoint de verificación de presencia puede no estar actualizando estos campos correctamente
- Falta migración de base de datos para agregar estos campos

**Solución Requerida:**
1. Verificar que el modelo `User` tenga los campos `presencia_verificada` y `presencia_verificada_at`
2. Verificar que el endpoint `/api/auth/verificar-presencia` actualice estos campos
3. Crear migración si los campos no existen
4. Probar el flujo completo: testigo verifica presencia → coordinador ve el ícono

---

### 2. Cantidad de Mesas No Coincide con la Base de Datos

**Descripción:**
La cantidad de mesas mostradas en el dashboard del coordinador de puesto no coincide con la cantidad real de mesas del puesto en la base de datos.

**Análisis:**
- El endpoint `/api/formularios/mesas` obtiene las mesas con:
  ```python
  mesas = Location.query.filter_by(
      puesto_codigo=ubicacion.puesto_codigo,
      tipo='mesa'
  ).all()
  ```
- Esto debería traer todas las mesas del puesto

**Causas Probables:**
1. **Datos inconsistentes en la BD**: Las mesas pueden no tener el `puesto_codigo` correcto
2. **Filtro incorrecto**: El filtro puede estar usando el campo equivocado
3. **Mesas no creadas**: Las mesas pueden no estar creadas en la base de datos
4. **Problema de jerarquía**: Las mesas pueden estar usando `parent_id` en lugar de `puesto_codigo`

**Solución Requerida:**
1. Verificar la estructura de la tabla `locations` y cómo se relacionan las mesas con los puestos
2. Revisar si se debe usar `parent_id` o `puesto_codigo` para filtrar
3. Verificar que todas las mesas del puesto estén creadas en la BD
4. Agregar logs para debug del query
5. Crear script de verificación de integridad de datos

---

## Plan de Acción

### Prioridad Alta

1. **Verificar modelo User**
   - Revisar `backend/models/user.py`
   - Confirmar existencia de campos `presencia_verificada` y `presencia_verificada_at`
   - Crear migración si no existen

2. **Verificar endpoint de verificación de presencia**
   - Revisar `backend/routes/auth.py`
   - Confirmar que el endpoint `/api/auth/verificar-presencia` existe y funciona
   - Verificar que actualiza los campos correctamente

3. **Verificar estructura de locations**
   - Revisar `backend/models/location.py`
   - Confirmar cómo se relacionan mesas con puestos
   - Verificar si se usa `parent_id` o `puesto_codigo`

4. **Corregir query de mesas**
   - Actualizar el filtro en `/api/formularios/mesas` si es necesario
   - Agregar logs para debug
   - Probar con datos reales

### Prioridad Media

5. **Crear script de verificación**
   - Script para verificar integridad de datos de locations
   - Script para verificar que todas las mesas tengan testigos asignados
   - Script para verificar coherencia de códigos

6. **Mejorar UI de presencia**
   - Agregar tooltip con fecha/hora de verificación
   - Agregar contador de testigos presentes
   - Agregar alerta si faltan testigos por verificar presencia

### Prioridad Baja

7. **Documentación**
   - Documentar el flujo de verificación de presencia
   - Documentar la estructura de locations
   - Crear guía de troubleshooting

---

## Archivos a Revisar

1. `backend/models/user.py` - Verificar campos de presencia
2. `backend/models/location.py` - Verificar relación mesas-puestos
3. `backend/routes/auth.py` - Verificar endpoint de verificación
4. `backend/routes/formularios_e14.py` - Verificar query de mesas
5. `frontend/static/js/coordinador-puesto.js` - Ya tiene la lógica correcta
6. `backend/migrations/` - Crear migración si es necesario

---

## Preguntas para el Usuario

1. ¿Cuántas mesas debería tener cada puesto?
2. ¿Las mesas ya están creadas en la base de datos?
3. ¿Los testigos ya están asignados a las mesas?
4. ¿El endpoint de verificación de presencia ya fue implementado?
5. ¿Se puede acceder a la base de datos para verificar los datos?

---

## Próximos Pasos

1. Revisar los modelos mencionados
2. Identificar exactamente qué está faltando
3. Crear las migraciones necesarias
4. Implementar las correcciones
5. Probar el flujo completo
6. Actualizar las tareas en `tasks.md`
