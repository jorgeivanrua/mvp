# ✅ Fix: Redirección Incorrecta después del Login

## Problema Identificado

Cuando un usuario iniciaba sesión desde `https://mvp-b9uv.onrender.com/auth/login`, después del login exitoso era redirigido a `/login` en lugar de al dashboard correspondiente.

## Causa Raíz

Había referencias hardcodeadas a `/login` en múltiples archivos JavaScript que deberían apuntar a `/auth/login`.

### Archivos Afectados

1. `frontend/static/js/api-client.js` - Redirección en error 401
2. `frontend/static/js/testigo-dashboard-new.js` - Función logout
3. `frontend/static/js/super-admin-dashboard.js` - Función logout
4. `frontend/static/js/coordinador-municipal.js` - Función logout
5. `frontend/static/js/coordinador-departamental.js` - Función logout
6. `frontend/static/js/admin-dashboard.js` - Verificación de auth y logout
7. `frontend/static/js/coordinador-puesto.js` - Función logout

## Solución Implementada

### Cambio 1: api-client.js
**Antes:**
```javascript
if (window.location.pathname !== '/login' && window.location.pathname !== '/') {
    window.location.href = '/login';
}
```

**Después:**
```javascript
if (window.location.pathname !== '/login' && window.location.pathname !== '/auth/login' && window.location.pathname !== '/') {
    window.location.href = '/auth/login';
}
```

### Cambio 2: Todos los dashboards
**Antes:**
```javascript
window.location.href = '/login';
```

**Después:**
```javascript
window.location.href = '/auth/login';
```

## Rutas Correctas

### Frontend (HTML)
- ✅ `/auth/login` - Página de login principal (CORRECTA)
- ❌ `/login` - Ruta alternativa (debe redirigir a /auth/login)

### Backend
Ambas rutas están configuradas en `backend/routes/frontend.py`:
```python
@frontend_bp.route('/login')
@frontend_bp.route('/auth/login')
def login():
    return render_template('auth/login.html')
```

## Flujo Correcto

### 1. Login Exitoso
```
Usuario → /auth/login → Ingresa credenciales → Login exitoso
→ Redirección al dashboard según rol
```

### 2. Sesión Expirada (401)
```
Usuario en dashboard → Token expirado → Error 401
→ Redirección a /auth/login
```

### 3. Logout
```
Usuario → Click en logout → Limpiar localStorage
→ Redirección a /auth/login
```

## Verificación

### URLs a Probar

1. **Login Principal:**
   ```
   https://mvp-b9uv.onrender.com/auth/login
   ```

2. **Login después de sesión expirada:**
   - Iniciar sesión
   - Esperar a que expire el token
   - Debería redirigir a `/auth/login`

3. **Logout:**
   - Iniciar sesión
   - Click en botón de logout
   - Debería redirigir a `/auth/login`

## Archivos Modificados

```
frontend/static/js/api-client.js
frontend/static/js/testigo-dashboard-new.js
frontend/static/js/super-admin-dashboard.js
frontend/static/js/coordinador-municipal.js
frontend/static/js/coordinador-departamental.js
frontend/static/js/admin-dashboard.js
frontend/static/js/coordinador-puesto.js
```

## Commit

```
fix: Corregir redirecciones de /login a /auth/login en todos los archivos JS
```

## Resultado Esperado

✅ Después del login exitoso, el usuario debe ser redirigido al dashboard correspondiente a su rol:

- Super Admin → `/admin/dashboard`
- Coordinador Departamental → `/coordinador/departamental`
- Coordinador Municipal → `/coordinador/municipal`
- Coordinador de Puesto → `/coordinador/puesto`
- Testigo Electoral → `/testigo/dashboard`
- Auditor Electoral → `/auditor/dashboard`

✅ En caso de sesión expirada o logout, el usuario debe ser redirigido a `/auth/login`

## Notas Importantes

1. **Caché del Navegador:** Puede ser necesario hacer un hard refresh (Ctrl+Shift+R) para ver los cambios
2. **Render Deploy:** Los cambios se aplicarán automáticamente en el próximo deploy
3. **Consistencia:** Todas las redirecciones ahora apuntan a `/auth/login`

## Testing

### Pasos para Verificar

1. Ir a `https://mvp-b9uv.onrender.com/auth/login`
2. Seleccionar rol: Testigo Electoral
3. Completar ubicación
4. Contraseña: `test123`
5. Click en "Iniciar Sesión"
6. **Verificar:** Debe redirigir a `/testigo/dashboard` (NO a `/login`)

### Si Persiste el Problema

1. Limpiar caché del navegador
2. Verificar que Render haya deployado los cambios
3. Revisar la consola del navegador para errores
4. Verificar que el token se esté guardando en localStorage

## Estado

✅ **CORREGIDO** - Todos los archivos JavaScript actualizados para usar `/auth/login`
