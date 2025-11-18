# Correcciones Dashboard de Testigo

## Problemas Corregidos

### 1. ✅ Preview de Foto del Formulario E-14
**Problema:** La imagen no se mostraba después de tomarla y se salía del formulario

**Solución:**
- Movida la inicialización de `setupImagePreview()` para que se ejecute cada vez que se abre el modal
- Agregado manejo de errores en la lectura del archivo
- Prevenido el comportamiento por defecto que causaba que se saliera del formulario
- Mejorado el preview con `object-fit: contain` para mejor visualización

**Código modificado:**
```javascript
function setupImagePreview() {
    // Remover listeners anteriores clonando el elemento
    const newInput = input.cloneNode(true);
    input.parentNode.replaceChild(newInput, input);
    
    newInput.addEventListener('change', function(e) {
        e.preventDefault();  // Prevenir comportamiento por defecto
        e.stopPropagation();
        // ... resto del código
    });
}
```

### 2. ✅ Panel "Mi Mesa Asignada" Mejorado
**Problema:** Solo mostraba información básica, no la lista de mesas con formularios

**Solución:**
- Creada función `actualizarPanelMesas()` que muestra todas las mesas del testigo
- Muestra badge con cantidad de formularios E-14 por mesa
- Permite seleccionar mesa haciendo clic en el panel
- Actualiza automáticamente cuando se carga o envía un formulario

**Características:**
- Lista todas las mesas asignadas al testigo
- Muestra cantidad de formularios E-14 por mesa
- Badge verde si tiene formularios, gris si no
- Muestra cantidad de votantes registrados
- Resalta la mesa actualmente seleccionada
- Clickeable para cambiar de mesa rápidamente

**Ejemplo visual:**
```
Mis Mesas
┌─────────────────────────────────┐
│ Mesa 001                [1 E-14]│
│ Puesto 001 - Zona 001           │
│ 👥 350 votantes                 │
├─────────────────────────────────┤
│ Mesa 002              [Sin E-14]│
│ Puesto 001 - Zona 001           │
│ 👥 420 votantes                 │
└─────────────────────────────────┘
```

### 3. ✅ Verificación de Presencia con Notificación
**Problema:** El botón verificaba presencia pero no notificaba al coordinador

**Solución:**
- Mejorado el endpoint `/auth/verificar-presencia` para buscar y notificar al coordinador
- Busca automáticamente el coordinador del puesto
- Registra en logs la notificación (preparado para sistema de notificaciones futuro)
- Retorna información sobre si se notificó al coordinador

**Backend modificado:**
```python
@auth_bp.route('/verificar-presencia', methods=['POST'])
def verificar_presencia():
    # ... verificar presencia
    
    # Buscar coordinador del puesto
    coordinador = User.query.filter_by(
        ubicacion_id=ubicacion.id,
        rol='coordinador_puesto'
    ).first()
    
    if coordinador:
        print(f"NOTIFICACIÓN: Testigo {user.nombre} verificó presencia")
        print(f"  -> Coordinador: {coordinador.nombre}")
        coordinador_notificado = True
```

**Nuevo endpoint para coordinadores:**
- Agregado `/api/formularios/testigos-puesto` para que coordinadores vean testigos
- Muestra estado de presencia de cada testigo
- Muestra último acceso

## Archivos Modificados

### Frontend
1. **frontend/static/js/testigo-dashboard-new.js**
   - Función `setupImagePreview()` mejorada
   - Nueva función `actualizarPanelMesas()`
   - Nueva función `seleccionarMesaDesdePanel()`
   - Actualizada `loadUserProfile()` para cargar panel de mesas
   - Actualizada `loadForms()` para actualizar panel después de guardar
   - Actualizada `cambiarMesa()` para actualizar panel

### Backend
2. **backend/routes/auth.py**
   - Mejorado endpoint `/verificar-presencia` con notificación a coordinador
   - Agregada búsqueda de coordinador del puesto
   - Agregado logging de notificaciones

3. **backend/routes/formularios_e14.py**
   - Nuevo endpoint `/testigos-puesto` para coordinadores
   - Retorna lista de testigos con estado de presencia

## Cómo Probar

### 1. Probar Preview de Foto
1. Iniciar sesión como testigo
2. Clic en "Nuevo Formulario"
3. Clic en "Tomar Foto / Seleccionar Imagen"
4. Seleccionar una imagen
5. **Verificar:** La imagen debe aparecer en el preview
6. **Verificar:** No debe salirse del formulario

### 2. Probar Panel de Mesas
1. Iniciar sesión como testigo
2. Observar el panel lateral "Mis Mesas"
3. **Verificar:** Muestra todas las mesas asignadas
4. Crear un formulario E-14 para una mesa
5. **Verificar:** El badge de esa mesa cambia a "1 E-14"
6. Clic en otra mesa en el panel
7. **Verificar:** Cambia la mesa seleccionada y filtra formularios

### 3. Probar Verificación de Presencia
1. Iniciar sesión como testigo
2. Clic en "Verificar Mi Presencia en la Mesa"
3. Confirmar
4. **Verificar:** Mensaje de éxito
5. **Verificar:** Botón se oculta y muestra alerta verde
6. **Verificar en logs del servidor:** Debe aparecer mensaje de notificación al coordinador

### 4. Coordinador Ver Testigos (Nuevo)
1. Iniciar sesión como coordinador de puesto
2. Hacer request a `/api/formularios/testigos-puesto`
3. **Verificar:** Retorna lista de testigos con estado de presencia

## Mejoras Futuras Sugeridas

### Sistema de Notificaciones en Tiempo Real
- Implementar WebSockets o Server-Sent Events
- Notificaciones push al coordinador cuando testigo verifica presencia
- Notificaciones cuando testigo envía formulario E-14

### Dashboard del Coordinador
- Agregar sección "Testigos" en dashboard de coordinador de puesto
- Mostrar lista de testigos con estado de presencia
- Indicador visual de testigos activos/inactivos
- Botón para contactar testigo (llamada/mensaje)

### Geolocalización
- Verificar que el testigo esté físicamente en el puesto
- Registrar coordenadas GPS al verificar presencia
- Alertar si testigo está lejos del puesto asignado

## Estado Actual

✅ **Completado:**
- Preview de foto funciona correctamente
- Panel de mesas muestra lista completa con formularios
- Verificación de presencia notifica al coordinador (logs)
- Endpoint para coordinadores ver testigos

⚠️ **Pendiente (Opcional):**
- Sistema de notificaciones en tiempo real
- UI en dashboard de coordinador para ver testigos
- Geolocalización para verificar ubicación física
