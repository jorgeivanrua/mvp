# ✅ Usuarios de Testing Configurados

## Estado
Los usuarios de testing están configurados en la base de datos y usan el endpoint de login estándar `/api/auth/login`.

## Endpoint
```
POST /api/auth/login
Content-Type: application/json

Body:
{
  "rol": "rol_usuario",
  "departamento_codigo": "TEST01",
  "municipio_codigo": "TEST0101",  // opcional según rol
  "zona_codigo": "TEST01Z1",       // opcional según rol
  "puesto_codigo": "TEST0101001",  // opcional según rol
  "password": "contraseña"
}
```

## Respuesta Exitosa
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "user": {
      "id": 1,
      "nombre": "admin_test",
      "rol": "super_admin",
      "ubicacion_id": null,
      "activo": true
    }
  }
}
```

## Credenciales de Prueba

### Super Admin
- **Contraseña:** `test123`
- **Rol:** `super_admin`
- **Login:**
  ```json
  {
    "rol": "super_admin",
    "password": "test123"
  }
  ```

### Auditor Electoral
- **Contraseña:** `test123`
- **Rol:** `auditor_electoral`
- **Login:**
  ```json
  {
    "rol": "auditor_electoral",
    "departamento_codigo": "TEST01",
    "password": "test123"
  }
  ```

### Coordinador Departamental
- **Contraseña:** `test123`
- **Rol:** `coordinador_departamental`
- **Ubicación:** Departamento Test (TEST01)
- **Login:**
  ```json
  {
    "rol": "coordinador_departamental",
    "departamento_codigo": "TEST01",
    "password": "test123"
  }
  ```

### Coordinador Municipal
- **Contraseña:** `test123`
- **Rol:** `coordinador_municipal`
- **Ubicación:** Municipio Test (TEST0101)
- **Login:**
  ```json
  {
    "rol": "coordinador_municipal",
    "departamento_codigo": "TEST01",
    "municipio_codigo": "TEST0101",
    "password": "test123"
  }
  ```

### Coordinador de Puesto
- **Contraseña:** `test123`
- **Rol:** `coordinador_puesto`
- **Ubicación:** Puesto Test 1 (TEST0101001)
- **Login:**
  ```json
  {
    "rol": "coordinador_puesto",
    "departamento_codigo": "TEST01",
    "municipio_codigo": "TEST0101",
    "zona_codigo": "TEST01Z1",
    "puesto_codigo": "TEST0101001",
    "password": "test123"
  }
  ```

### Testigo Electoral
- **Contraseña:** `test123`
- **Rol:** `testigo_electoral`
- **Ubicación:** Mesa 1 - Puesto Test 1 (TEST01010010001)
- **Login:**
  ```json
  {
    "rol": "testigo_electoral",
    "departamento_codigo": "TEST01",
    "municipio_codigo": "TEST0101",
    "zona_codigo": "TEST01Z1",
    "puesto_codigo": "TEST0101001",
    "password": "test123"
  }
  ```

## Pruebas Realizadas

### ✅ Prueba 1: Login Super Admin
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"rol":"super_admin","password":"test123"}'
```
**Resultado:** ✅ Exitoso - Tokens generados correctamente

### ✅ Prueba 2: Login Testigo Electoral
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"rol":"testigo_electoral","departamento_codigo":"TEST01","municipio_codigo":"TEST0101","zona_codigo":"TEST01Z1","puesto_codigo":"TEST0101001","password":"test123"}'
```
**Resultado:** ✅ Exitoso - Tokens generados correctamente

## Cambios Realizados

### 1. Eliminación del Endpoint de Testing
- **Archivo:** `backend/routes/auth.py`
- **Cambio:** Eliminado endpoint `/login-testing` - Los usuarios de testing usan el endpoint estándar `/login`
- **Razón:** Los usuarios de testing deben seguir el mismo flujo de autenticación que los usuarios normales

## Funcionalidades del Sistema de Autenticación

1. ✅ Autenticación basada en rol y ubicación jerárquica
2. ✅ Validación de datos de entrada
3. ✅ Búsqueda de usuario por rol y ubicación
4. ✅ Verificación de contraseña
5. ✅ Manejo de intentos fallidos
6. ✅ Verificación de bloqueo de cuenta
7. ✅ Generación de tokens JWT (access y refresh)
8. ✅ Actualización de último acceso
9. ✅ Reset de intentos fallidos en login exitoso

## Próximos Pasos

1. Probar el login desde el frontend con los usuarios de testing
2. Verificar que los tokens funcionen con endpoints protegidos
3. Probar el sistema de auditoría con estos usuarios
4. Verificar que cada rol tenga acceso a sus funcionalidades correspondientes

## Servidor
El servidor Flask está corriendo en: `http://localhost:5000`
