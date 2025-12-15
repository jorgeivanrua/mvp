# Instrucciones para Probar el Modal de Validación

## 🎯 Problema Identificado

El error 404 ocurre porque **el usuario logueado no es el coordinador correcto** para el puesto donde está el formulario.

## 📋 Datos del Sistema

### Formulario de Prueba
- **ID:** 1
- **Mesa:** 01 (ID: 75591)
- **Puesto:** 01 - I.E. JUAN BAUTISTA LA SALLE
- **Estado:** pendiente
- **Imagen:** `/static/images/sample-e14.svg`
- **Votos por partido:** 2 registros
- **Votos por candidatos:** 3 registros

### Coordinador Correcto
- **Nombre:** FLORENCIA_P01
- **ID:** 31
- **Ubicación:** 75590 (Puesto I.E. JUAN BAUTISTA LA SALLE)
- **Rol:** coordinador_puesto

## 🔐 Pasos para Probar Correctamente

### 1. **Cerrar Sesión Actual**
```
1. Ir a cualquier dashboard
2. Hacer clic en "Cerrar Sesión"
3. O limpiar localStorage en DevTools:
   - F12 → Application → Local Storage → Clear All
```

### 2. **Iniciar Sesión como Coordinador Correcto**
```
URL: http://localhost:5000/auth/login
Usuario: FLORENCIA_P01
Contraseña: [usar la contraseña del sistema]
```

### 3. **Navegar al Dashboard de Coordinador**
```
URL: http://localhost:5000/coordinador/puesto
```

### 4. **Verificar en Consola del Navegador**
```
F12 → Console
Buscar estos logs:
✅ 👤 User profile loaded: {rol: "coordinador_puesto", nombre: "FLORENCIA_P01"}
✅ 📍 User location: {puesto_codigo: "01", ...}
```

### 5. **Probar el Modal**
```
1. Buscar el formulario en la tabla
2. Hacer clic en el botón "Ver" (ojo)
3. Verificar en consola:
   ✅ 🔍 Cargando formulario ID: 1
   ✅ 📡 Respuesta del servidor: {success: true, data: {...}}
```

## 🔍 Debugging en Consola

### Verificar Autenticación
```javascript
// En consola del navegador:
console.log('Token:', localStorage.getItem('access_token'));
console.log('Usuario:', JSON.parse(localStorage.getItem('user_data') || '{}'));
```

### Verificar Permisos
```javascript
// Probar endpoint manualmente:
fetch('/api/coordinador-puesto/formularios/1', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        'Content-Type': 'application/json'
    }
})
.then(r => r.json())
.then(console.log);
```

## 🚨 Posibles Problemas y Soluciones

### Error 403 (Forbidden)
**Causa:** Usuario logueado no es coordinador de puesto o no tiene permisos para ese formulario
**Solución:** 
1. Verificar que el usuario sea `coordinador_puesto`
2. Verificar que el usuario esté asignado al puesto correcto

### Error 404 (Not Found)
**Causa:** Endpoint incorrecto o servidor no funcionando
**Solución:**
1. Verificar que el servidor esté corriendo en puerto 5000
2. Verificar que las URLs tengan el prefijo `/api`

### Error 401 (Unauthorized)
**Causa:** Token de autenticación inválido o expirado
**Solución:**
1. Cerrar sesión y volver a iniciar
2. Limpiar localStorage y autenticarse nuevamente

## 🎯 Resultado Esperado

### Al Abrir el Modal Correctamente:
1. **Foto del formulario** - SVG simulando E-14
2. **Tabla de candidatos** - 3 candidatos con números y partidos
3. **Resumen por partidos** - 2 partidos con totales
4. **Validaciones automáticas** - Verificaciones matemáticas
5. **Controles de foto** - Zoom, rotación, nueva ventana

### Logs en Consola:
```
🔍 Cargando formulario ID: 1
👤 Usuario actual: {rol: "coordinador_puesto", nombre: "FLORENCIA_P01"}
📍 Ubicación del usuario: {puesto_codigo: "01", ...}
📡 Respuesta del servidor: {success: true, data: {...}}
📋 Datos completos del formulario: {...}
🗳️ Votos por partido: [{partido_nombre: "...", votos: ...}, ...]
👥 Votos por candidatos: [{candidato_nombre: "...", votos: ...}, ...]
📸 Imagen URL: /static/images/sample-e14.svg
```

## 🔧 Si Persiste el Problema

### Verificar Backend
```bash
# Verificar que el servidor esté corriendo
curl http://localhost:5000/api/coordinador-puesto/formularios

# Debería retornar error 401 (sin token) no 404
```

### Crear Usuario de Prueba
```python
# Si necesitas crear un usuario específico:
python -c "
from backend.app import create_app
from backend.models.user import User
from backend.database import db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    user = User(
        nombre='TEST_COORD_P01',
        cedula='99999999',
        password_hash=generate_password_hash('test123'),
        rol='coordinador_puesto',
        ubicacion_id=75590,  # Puesto del formulario
        activo=True
    )
    db.session.add(user)
    db.session.commit()
    print(f'Usuario creado: cedula=99999999, password=test123')
"
```

## 📞 Contacto para Soporte

Si después de seguir estos pasos el problema persiste:

1. **Capturar logs completos** de la consola del navegador
2. **Verificar el rol del usuario** logueado
3. **Confirmar que el servidor** esté corriendo en puerto 5000
4. **Probar con el usuario correcto** (FLORENCIA_P01)

El modal debería funcionar correctamente siguiendo estos pasos. 🚀