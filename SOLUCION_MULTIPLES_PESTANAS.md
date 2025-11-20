# Solución: Problemas con Múltiples Pestañas

## 🔴 Problema

Cuando abres múltiples pestañas del sistema con diferentes usuarios (por ejemplo, Super Admin en una pestaña y Testigo en otra), ocurren errores 403 y las pestañas se "crashean".

### ¿Por qué pasa esto?

1. **localStorage es compartido** entre todas las pestañas del mismo dominio
2. Cuando inicias sesión en una pestaña, el token JWT se guarda en localStorage
3. **Todas las pestañas usan el mismo localStorage**
4. Si inicias sesión como Testigo en una pestaña, sobrescribe el token del Super Admin en la otra pestaña
5. El Super Admin intenta acceder a sus endpoints con el token del Testigo
6. Resultado: **Error 403 "No tiene permisos"**

### Ejemplo del Problema

```
Pestaña 1: Super Admin
- Token guardado: super_admin_token_123
- Intenta acceder a /api/super-admin/stats

Pestaña 2: Testigo Electoral
- Login como testigo
- Token guardado: testigo_token_456
- ⚠️ SOBRESCRIBE el token en localStorage

Pestaña 1: Super Admin (ahora con token de testigo)
- Intenta acceder a /api/super-admin/stats
- Usa testigo_token_456 (incorrecto)
- ❌ Error 403: "No tiene permisos"
```

## ✅ Solución Implementada

### Session Manager

Se creó un **Session Manager** que detecta cuando el token cambia en localStorage y recarga automáticamente la página.

**Archivo**: `frontend/static/js/session-manager.js`

**Funcionalidad**:
1. Guarda el token y rol actual al cargar la página
2. Escucha cambios en localStorage (evento `storage`)
3. Verifica cada 5 segundos si el token cambió
4. Si detecta un cambio, muestra un mensaje y recarga la página

### Cómo Funciona

```javascript
// Al cargar la página
currentToken = localStorage.getItem('access_token');
currentRole = user.rol;

// Cada 5 segundos
newToken = localStorage.getItem('access_token');
if (newToken !== currentToken) {
    // Token cambió, recargar página
    window.location.reload();
}
```

### Flujo con Session Manager

```
Pestaña 1: Super Admin
- Token: super_admin_token_123
- Session Manager activo

Pestaña 2: Testigo Electoral
- Login como testigo
- Token guardado: testigo_token_456

Pestaña 1: Super Admin
- Session Manager detecta cambio de token
- Muestra mensaje: "Sesión Actualizada"
- Recarga la página automáticamente
- Redirige al login (token inválido)
```

## 📋 Mejores Prácticas

### ✅ Recomendaciones

1. **Usar una pestaña por usuario**
   - No abrir múltiples pestañas con diferentes usuarios
   - Si necesitas probar diferentes roles, usa ventanas de incógnito

2. **Cerrar sesión antes de cambiar de usuario**
   - Siempre cerrar sesión en todas las pestañas
   - Luego iniciar sesión con el nuevo usuario

3. **Usar perfiles de navegador diferentes**
   - Chrome: Crear perfiles diferentes para cada rol
   - Firefox: Usar contenedores (Multi-Account Containers)

4. **Usar navegadores diferentes**
   - Super Admin en Chrome
   - Testigo en Firefox
   - Coordinador en Edge

### ❌ Evitar

1. **No abrir múltiples pestañas con diferentes usuarios**
   - Causa conflictos de tokens
   - Genera errores 403

2. **No mantener sesiones abiertas sin usar**
   - Cerrar pestañas que no estés usando
   - Evita confusiones

## 🔧 Solución Manual

Si experimentas errores 403:

### Opción 1: Recargar la Página
1. Presiona `F5` o `Ctrl+R`
2. El Session Manager detectará el cambio
3. Te redirigirá al login

### Opción 2: Cerrar Sesión
1. Clic en "Cerrar Sesión"
2. Volver a iniciar sesión
3. Esto generará un nuevo token

### Opción 3: Limpiar localStorage
1. Abrir DevTools (F12)
2. Application → Local Storage
3. Eliminar `access_token`, `refresh_token`, `user_data`
4. Recargar la página

## 🎯 Solución Técnica Alternativa

### Opción 1: Tokens por Pestaña (Complejo)

En lugar de usar localStorage, usar sessionStorage:
- Cada pestaña tiene su propio sessionStorage
- Los tokens no se comparten entre pestañas
- **Desventaja**: Pierdes la sesión al cerrar la pestaña

### Opción 2: Namespace por Rol (Medio)

Guardar tokens con prefijo de rol:
```javascript
localStorage.setItem('token_super_admin', token);
localStorage.setItem('token_testigo', token);
```
- **Desventaja**: Más complejo de implementar

### Opción 3: Session Manager (Implementado) ✅

Detectar cambios y recargar:
- Simple de implementar
- No requiere cambios en el backend
- Funciona con el sistema actual

## 📊 Comparación de Soluciones

| Solución | Complejidad | Efectividad | Implementado |
|----------|-------------|-------------|--------------|
| Session Manager | Baja | Alta | ✅ Sí |
| sessionStorage | Media | Alta | ❌ No |
| Namespace por Rol | Alta | Media | ❌ No |
| Múltiples Dominios | Muy Alta | Muy Alta | ❌ No |

## 🚀 Resultado

Con el Session Manager implementado:

1. **Detección automática** de cambios de sesión
2. **Recarga automática** de la página
3. **Mensaje informativo** al usuario
4. **Sin errores 403** por tokens mezclados

## 📝 Notas Técnicas

### localStorage vs sessionStorage

**localStorage**:
- Compartido entre todas las pestañas
- Persiste al cerrar el navegador
- Usado actualmente

**sessionStorage**:
- Único por pestaña
- Se borra al cerrar la pestaña
- No compartido

### Evento storage

```javascript
window.addEventListener('storage', (e) => {
    // Se dispara cuando otra pestaña modifica localStorage
    if (e.key === 'access_token') {
        // Token cambió en otra pestaña
    }
});
```

**Limitación**: No se dispara en la misma pestaña que hizo el cambio.

**Solución**: Verificar cada 5 segundos con setInterval.

## 🔍 Debugging

Para ver los logs del Session Manager:

1. Abrir DevTools (F12)
2. Ir a Console
3. Buscar mensajes `[SessionManager]`

Ejemplo:
```
[SessionManager] Initialized
[SessionManager] Session changed detected
  Old token: eyJhbGciOiJIUzI1NiIs...
  New token: eyJhbGciOiJIUzI1NiIs...
  Old role: super_admin
  New role: testigo_electoral
[SessionManager] Reloading page due to session change...
```

## ✅ Conclusión

El Session Manager resuelve el problema de múltiples pestañas de forma simple y efectiva. Los usuarios verán un mensaje cuando la sesión cambie y la página se recargará automáticamente, evitando errores 403.
