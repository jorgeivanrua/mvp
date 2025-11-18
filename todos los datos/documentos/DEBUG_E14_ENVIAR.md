# Debug: Botón "Enviar para Revisión" del E-14

## Problema
El botón "Enviar para Revisión" no hace nada cuando se hace clic.

## Cambios Realizados

### 1. Agregados console.log para debugging
Se agregaron logs en la función `saveForm` para rastrear el flujo:

```javascript
async function saveForm(accion = 'borrador') {
    console.log('saveForm called with accion:', accion);
    // ... más logs
}
```

### 2. Corregido error de telefono
Se eliminaron referencias al campo `telefono` que no existe en el modelo User:
- `backend/services/municipal_service.py`
- `backend/services/departamental_service.py`
- `backend/routes/formularios_e14.py`

## Pasos para Debuggear

### 1. Abrir Consola del Navegador
1. Presionar F12 en el navegador
2. Ir a la pestaña "Console"
3. Limpiar la consola (icono de 🚫)

### 2. Intentar Enviar Formulario
1. Llenar un formulario E-14 completo
2. Hacer clic en "Enviar para Revisión"
3. Observar los mensajes en la consola

### 3. Verificar Logs Esperados

Si todo funciona correctamente, deberías ver:
```
saveForm called with accion: enviar
Mesa ID: [número]
Disabling buttons...
FormData created
Saving form data: {...}
```

### 4. Posibles Problemas y Soluciones

#### Problema 1: No aparece ningún log
**Causa**: El evento onclick no se está disparando
**Solución**: 
- Verificar que el botón tenga el atributo `onclick="saveForm('enviar')"`
- Verificar que no haya errores de JavaScript previos

#### Problema 2: Aparece "Form validation failed"
**Causa**: Algún campo requerido no está lleno
**Solución**:
- Verificar que todos los campos con asterisco (*) estén llenos
- Verificar que los campos calculados automáticamente tengan valores
- Campos requeridos:
  - Mesa
  - Tipo de Elección
  - Votos Nulos
  - Votos en Blanco
  - Tarjetas No Marcadas
  - Al menos un voto para algún partido

#### Problema 3: Error en la consola
**Causa**: Error de JavaScript
**Solución**:
- Leer el mensaje de error completo
- Verificar la línea del error
- Buscar el error en el código

#### Problema 4: Error de red (500, 404, etc.)
**Causa**: Problema en el backend
**Solución**:
- Verificar que el servidor esté corriendo
- Verificar los logs del servidor
- Verificar que la ruta `/api/formularios` exista

## Verificaciones Adicionales

### 1. Verificar que el formulario tenga ID correcto
```html
<form id="e14Form" enctype="multipart/form-data">
```

### 2. Verificar que los botones tengan onclick correcto
```html
<button type="button" class="btn btn-warning" onclick="saveForm('borrador')">
<button type="button" class="btn btn-primary" onclick="saveForm('enviar')">
```

### 3. Verificar que Utils esté definido
En la consola, escribir:
```javascript
typeof Utils
```
Debería devolver: `"object"`

### 4. Verificar que APIClient esté definido
En la consola, escribir:
```javascript
typeof APIClient
```
Debería devolver: `"function"`

## Solución Temporal

Si el problema persiste, puedes probar:

### Opción 1: Guardar como borrador primero
1. Llenar el formulario
2. Hacer clic en "Guardar Borrador"
3. Si funciona, el problema está en la validación del envío
4. Cerrar el modal
5. Editar el borrador
6. Intentar enviar de nuevo

### Opción 2: Verificar en la base de datos
```bash
python -c "from backend.app import create_app; from backend.database import db; from backend.models.formulario_e14 import FormularioE14; app = create_app(); app.app_context().push(); print(FormularioE14.query.all())"
```

## Archivos Modificados

1. `frontend/static/js/testigo-dashboard-new.js` - Agregados console.log
2. `backend/services/municipal_service.py` - Eliminado telefono
3. `backend/services/departamental_service.py` - Eliminado telefono
4. `backend/routes/formularios_e14.py` - Eliminado telefono

## Próximos Pasos

1. Probar en el navegador con la consola abierta
2. Reportar los logs que aparecen
3. Si hay error, copiar el mensaje completo
4. Verificar el estado de los botones (si se deshabilitan)
5. Verificar si aparece algún mensaje de Utils (success, error, info)
