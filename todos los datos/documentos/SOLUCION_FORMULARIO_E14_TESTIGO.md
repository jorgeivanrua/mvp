# Solución: Formulario E14 del Testigo - Guardado Local y Envío

## Problema Identificado

El formulario E14 en el dashboard del testigo no guardaba ni enviaba los datos. Los problemas encontrados fueron:

1. **Falta de endpoint para testigos**: El endpoint `/api/formularios/puesto` solo estaba disponible para coordinadores de puesto, no para testigos.
2. **Sin funcionalidad de guardado local**: No había implementación de localStorage para guardar borradores cuando no hay conexión.
3. **Sin sincronización**: No había mecanismo para sincronizar borradores guardados localmente con el servidor.

## Solución Implementada

### 1. Backend - Nuevo Endpoint para Testigos

**Archivo**: `backend/routes/formularios_e14.py`

Se agregó un nuevo endpoint `/api/formularios/mis-formularios` que permite a los testigos obtener sus propios formularios:

```python
@formularios_bp.route('/mis-formularios', methods=['GET'])
@jwt_required()
@role_required(['testigo'])
def obtener_mis_formularios():
    """
    Obtener formularios del testigo actual
    
    Query params:
        mesa_id: Filtrar por mesa (opcional)
        estado: Filtrar por estado (opcional)
        page: Número de página (default: 1)
        per_page: Resultados por página (default: 20)
    """
```

### 2. Frontend - API Client Actualizado

**Archivo**: `frontend/static/js/api-client.js`

Se actualizó el método `getFormulariosE14()` para usar el nuevo endpoint:

```javascript
static async getFormulariosE14(params = {}) {
    // Para testigos, usar endpoint específico
    return this.get('/formularios/mis-formularios', params);
}
```

### 3. Frontend - Guardado Local Implementado

**Archivo**: `frontend/static/js/testigo-dashboard-new.js`

Se implementaron las siguientes funcionalidades:

#### a) Guardado en localStorage

```javascript
function guardarBorradorLocal(data)
function obtenerBorradoresLocales()
function eliminarBorradorLocal(mesaId, tipoEleccionId)
```

#### b) Sincronización con el servidor

```javascript
async function sincronizarBorradoresLocales()
```

Esta función:
- Lee todos los borradores guardados localmente
- Intenta enviarlos al servidor uno por uno
- Elimina los borradores que se sincronizaron exitosamente
- Muestra un resumen de la sincronización

#### c) Edición de borradores locales

```javascript
async function editarBorradorLocal(localId)
function eliminarBorradorLocalPorId(localId)
```

#### d) Indicador visual de sincronización

```javascript
function mostrarIndicadorSincronizacion(cantidad)
```

Muestra un indicador flotante en la esquina inferior derecha cuando hay borradores pendientes de sincronizar.

### 4. Flujo de Guardado Mejorado

La función `saveForm()` ahora maneja dos escenarios:

#### Guardar como Borrador
- Guarda inmediatamente en localStorage
- No requiere conexión a internet
- Muestra mensaje: "Borrador guardado localmente"

#### Enviar para Revisión
- Intenta enviar al servidor
- Si tiene éxito: elimina el borrador local (si existe)
- Si falla: ofrece guardar localmente para enviar después

```javascript
async function saveForm(accion = 'borrador') {
    // ... construcción de datos ...
    
    // Si es borrador, guardar en localStorage
    if (accion === 'borrador') {
        guardarBorradorLocal(data);
        Utils.showSuccess('Borrador guardado localmente');
        return;
    }
    
    // Si es enviar, intentar enviar al servidor
    try {
        const response = await APIClient.createFormularioE14(data);
        if (response.success) {
            eliminarBorradorLocal(data.mesa_id, data.tipo_eleccion_id);
            Utils.showSuccess('Formulario E-14 enviado para revisión');
        }
    } catch (error) {
        // Ofrecer guardar localmente si falla
        if (confirm('No se pudo enviar. ¿Guardar localmente?')) {
            guardarBorradorLocal(data);
            Utils.showSuccess('Formulario guardado localmente');
        }
    }
}
```

### 5. Visualización de Formularios

La tabla de formularios ahora muestra:
- **Formularios del servidor**: Con estados pendiente, validado, rechazado
- **Borradores locales**: Con estado "Guardado Localmente" (badge azul)

Los borradores locales tienen:
- Botón de editar
- Botón de eliminar
- Se pueden sincronizar manualmente

### 6. Template Actualizado

**Archivo**: `frontend/templates/testigo/dashboard.html`

Se agregó el contenedor de alertas:

```html
<div id="alert-container" class="mb-3"></div>
```

## Características Implementadas

### ✅ Guardado Local
- Los borradores se guardan en localStorage del navegador
- Funcionan sin conexión a internet
- Persisten entre sesiones del navegador

### ✅ Sincronización Manual
- Botón flotante aparece cuando hay borradores pendientes
- Muestra la cantidad de formularios por sincronizar
- Sincroniza todos los borradores con un clic

### ✅ Gestión de Borradores
- Editar borradores locales
- Eliminar borradores locales
- Ver estado de cada formulario

### ✅ Manejo de Errores
- Si falla el envío, ofrece guardar localmente
- Mensajes claros de éxito/error
- Indicadores visuales del estado

## Uso para el Testigo

### Guardar Borrador (sin conexión)
1. Llenar el formulario E14
2. Clic en "Guardar Borrador"
3. El formulario se guarda localmente
4. Aparece en la tabla con estado "Guardado Localmente"

### Enviar Formulario (con conexión)
1. Llenar el formulario E14
2. Clic en "Enviar para Revisión"
3. Si hay conexión: se envía al servidor
4. Si no hay conexión: se ofrece guardar localmente

### Sincronizar Borradores
1. Cuando hay conexión, aparece un indicador flotante
2. Clic en "Sincronizar"
3. Todos los borradores se envían al servidor
4. Los exitosos se eliminan del almacenamiento local

## Estructura de Datos en localStorage

```javascript
{
  "formularios_e14_borradores": {
    "123_1": {  // key: mesa_id_tipo_eleccion_id
      "mesa_id": 123,
      "tipo_eleccion_id": 1,
      "total_votos": 500,
      "votos_validos": 480,
      // ... otros campos ...
      "saved_at": "2025-11-12T10:30:00.000Z",
      "local_id": "123_1"
    }
  }
}
```

## Próximos Pasos Sugeridos

1. **Upload de imágenes**: Implementar guardado de fotos del formulario E14
2. **Sincronización automática**: Detectar cuando vuelve la conexión y sincronizar automáticamente
3. **Validación offline**: Validar datos antes de guardar localmente
4. **Compresión de imágenes**: Optimizar fotos antes de enviar
5. **Service Worker**: Implementar PWA para mejor experiencia offline

## Archivos Modificados

1. `backend/routes/formularios_e14.py` - Nuevo endpoint para testigos
2. `frontend/static/js/api-client.js` - Método actualizado
3. `frontend/static/js/testigo-dashboard-new.js` - Funcionalidad completa de guardado local
4. `frontend/templates/testigo/dashboard.html` - Contenedor de alertas

## Testing

Para probar la funcionalidad:

1. **Guardar borrador sin conexión**:
   - Desconectar internet
   - Llenar formulario
   - Guardar borrador
   - Verificar que aparece en la tabla

2. **Sincronizar con conexión**:
   - Reconectar internet
   - Clic en botón "Sincronizar"
   - Verificar que se envía al servidor

3. **Editar borrador local**:
   - Clic en "Editar" de un borrador local
   - Modificar datos
   - Guardar nuevamente
