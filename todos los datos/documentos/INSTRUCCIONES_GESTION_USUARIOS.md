# Instrucciones para Usar la Gestión de Usuarios

## 🔐 Acceso a la Interfaz

### Paso 1: Iniciar Sesión

1. Abrir el navegador y navegar a: http://127.0.0.1:5000/auth/login
2. Ingresar credenciales de Super Admin:
   - **Rol**: super_admin
   - **Contraseña**: admin123
3. Hacer clic en "Iniciar Sesión"

### Paso 2: Acceder a Gestión de Usuarios

Una vez autenticado, navegar a:
```
http://127.0.0.1:5000/admin/gestion-usuarios
```

O desde el dashboard del Super Admin, buscar el enlace a "Gestión de Usuarios"

---

## 📋 Uso de la Interfaz

### Tab 1: Testigos por Puesto

1. Seleccionar un puesto de votación del dropdown
2. Hacer clic en "Crear Testigos para este Puesto"
3. Se crearán testigos para todas las mesas del puesto
4. Las credenciales se mostrarán en un modal
5. Descargar o copiar las credenciales

### Tab 2: Coordinadores de Puesto

1. Seleccionar un puesto de votación
2. Hacer clic en "Crear Coordinador"
3. Se creará un coordinador para ese puesto
4. Guardar las credenciales mostradas

### Tab 3: Usuarios Municipales

1. Seleccionar un municipio
2. Elegir qué usuarios crear (coordinador y/o admin)
3. Hacer clic en "Crear Usuarios"
4. Guardar las credenciales

### Tab 4: Usuarios Departamentales

1. Seleccionar un departamento
2. Elegir qué usuarios crear (coordinador y/o admin)
3. Hacer clic en "Crear Usuarios"
4. Guardar las credenciales

---

## 🔧 Solución de Problemas

### Los selectores están vacíos

**Problema**: Los dropdowns no muestran opciones

**Solución**:
1. Abrir la consola del navegador (F12)
2. Verificar si hay errores de JavaScript
3. Verificar que estés autenticado (debe haber un token en localStorage)
4. Refrescar la página (F5)

**Verificar autenticación**:
```javascript
// En la consola del navegador:
console.log(localStorage.getItem('access_token'));
```

Si no hay token, volver a iniciar sesión.

### Error 401 (No autorizado)

**Causa**: Token expirado o no válido

**Solución**:
1. Cerrar sesión
2. Volver a iniciar sesión
3. Intentar nuevamente

### Error 404 (No encontrado)

**Causa**: El endpoint no existe o la aplicación no está corriendo

**Solución**:
1. Verificar que la aplicación esté corriendo: http://127.0.0.1:5000
2. Verificar que el servidor Flask esté activo
3. Revisar los logs del servidor

---

## 🧪 Prueba Manual Rápida

### Desde la Consola del Navegador

1. Abrir http://127.0.0.1:5000/auth/login
2. Iniciar sesión como super_admin
3. Abrir la consola del navegador (F12)
4. Ejecutar:

```javascript
// Verificar token
console.log('Token:', localStorage.getItem('access_token'));

// Probar endpoint de puestos
fetch('/api/gestion-usuarios/puestos', {
    headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
    }
})
.then(r => r.json())
.then(data => {
    console.log('Puestos:', data.puestos.length);
    console.log('Primer puesto:', data.puestos[0]);
});
```

Si esto funciona, los selectores deberían poblarse automáticamente.

---

## 📝 Notas Importantes

1. **Credenciales**: Las contraseñas solo se muestran UNA VEZ. Asegúrate de guardarlas.

2. **Duplicados**: El sistema previene la creación de usuarios duplicados. Si intentas crear un usuario que ya existe, recibirás un error.

3. **Permisos**: Solo usuarios con rol `super_admin`, `admin_departamental` o `admin_municipal` pueden acceder a esta funcionalidad.

4. **Seguridad**: Las contraseñas generadas tienen 12 caracteres con letras, números y símbolos especiales.

---

## 🚀 Acceso Directo (Para Testing)

Si necesitas acceder rápidamente sin pasar por el login:

```bash
# Ejecutar script de prueba
python test_crear_usuarios_completo.py
```

Este script creará usuarios automáticamente y mostrará las credenciales en la terminal.

---

## 📞 Soporte

Si los problemas persisten:

1. Verificar logs del servidor Flask
2. Revisar la consola del navegador (F12 → Console)
3. Verificar que la base de datos tenga datos de DIVIPOLA
4. Ejecutar: `python test_gestion_usuarios.py` para verificar el sistema

---

**Última actualización**: 2025-11-16 18:20:00
