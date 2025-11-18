# 🔐 Instrucciones de Login - Sistema Electoral

## ⚠️ IMPORTANTE: Cómo Hacer Login Correctamente

### ❌ ERROR COMÚN
**NO uses emails como contraseña**. El sistema NO usa emails.

### ✅ FORMA CORRECTA

El sistema usa **ubicación jerárquica** + **contraseña**, NO emails.

## 📝 Pasos para Login

### 1. Seleccionar Rol
Primero selecciona el rol del usuario:
- Super Admin
- Admin Departamental
- Admin Municipal
- Coordinador Departamental
- Coordinador Municipal
- Coordinador Puesto
- Auditor Electoral
- Testigo Electoral

### 2. Seleccionar Ubicación (según el rol)

**Para Super Admin:**
- No requiere ubicación
- Solo contraseña

**Para roles departamentales:**
- Departamento: CAQUETA

**Para roles municipales:**
- Departamento: CAQUETA
- Municipio: FLORENCIA

**Para roles de puesto:**
- Departamento: CAQUETA
- Municipio: FLORENCIA
- Zona: CAQUETA - FLORENCIA - Zona 01
- Puesto: I.E. JUAN BAUTISTA LA SALLE

### 3. Ingresar Contraseña

**Contraseña:** `test123`

**NO uses:**
- ❌ testigo@sistema-electoral.gov
- ❌ admin@sistema-electoral.gov
- ❌ Ningún email

**Usa:**
- ✅ test123

## 🎯 Ejemplos Completos

### Ejemplo 1: Super Admin
```
1. Rol: Super Admin
2. Contraseña: test123
3. Click en "Iniciar Sesión"
```

### Ejemplo 2: Testigo Electoral
```
1. Rol: Testigo Electoral
2. Departamento: CAQUETA
3. Municipio: FLORENCIA
4. Zona: CAQUETA - FLORENCIA - Zona 01
5. Puesto: I.E. JUAN BAUTISTA LA SALLE
6. Contraseña: test123
7. Click en "Iniciar Sesión"
```

### Ejemplo 3: Coordinador Departamental
```
1. Rol: Coordinador Departamental
2. Departamento: CAQUETA
3. Contraseña: test123
4. Click en "Iniciar Sesión"
```

## 🔍 Verificar que Funciona

### En Local (http://localhost:5000/auth/login)
1. Abre el navegador
2. Ve a: http://localhost:5000/auth/login
3. Selecciona "Super Admin"
4. Ingresa contraseña: `test123`
5. Click "Iniciar Sesión"
6. Deberías ver el dashboard

### En Render (https://mvp-b9uv.onrender.com/auth/login)
1. Abre el navegador
2. Ve a: https://mvp-b9uv.onrender.com/auth/login
3. Selecciona "Super Admin"
4. Ingresa contraseña: `test123`
5. Click "Iniciar Sesión"
6. Deberías ver el dashboard

## ❓ Preguntas Frecuentes

### ¿Por qué no funciona con email?
El sistema NO usa emails. Usa ubicación jerárquica (departamento, municipio, zona, puesto) para identificar al usuario.

### ¿Cuál es la contraseña?
La contraseña para TODOS los usuarios es: `test123`

### ¿Qué pasa si dice "Credenciales inválidas"?
Verifica que:
1. Hayas seleccionado el departamento correcto: CAQUETA
2. Hayas seleccionado el municipio correcto: FLORENCIA (si aplica)
3. Estés usando la contraseña: test123 (no un email)

### ¿Cómo sé qué ubicación seleccionar?
Depende del rol:
- **Super Admin**: No requiere ubicación
- **Departamental**: Solo departamento (CAQUETA)
- **Municipal**: Departamento + Municipio (CAQUETA + FLORENCIA)
- **Puesto**: Departamento + Municipio + Zona + Puesto

## 📊 Usuarios Disponibles

| Rol | Departamento | Municipio | Zona | Puesto | Contraseña |
|-----|--------------|-----------|------|--------|------------|
| Super Admin | - | - | - | - | test123 |
| Admin Departamental | CAQUETA | - | - | - | test123 |
| Admin Municipal | CAQUETA | FLORENCIA | - | - | test123 |
| Coordinador Departamental | CAQUETA | - | - | - | test123 |
| Coordinador Municipal | CAQUETA | FLORENCIA | - | - | test123 |
| Coordinador Puesto | CAQUETA | FLORENCIA | Zona 01 | I.E. JUAN BAUTISTA LA SALLE | test123 |
| Auditor Electoral | CAQUETA | - | - | - | test123 |
| Testigo Electoral | CAQUETA | FLORENCIA | Zona 01 | I.E. JUAN BAUTISTA LA SALLE | test123 |

## 🆘 Solución de Problemas

### Error: "Credenciales inválidas"
**Causa:** Contraseña incorrecta o ubicación incorrecta

**Solución:**
1. Verifica que estés usando `test123` como contraseña
2. Verifica que hayas seleccionado CAQUETA como departamento
3. Verifica que hayas seleccionado FLORENCIA como municipio (si aplica)

### Error: "No se encuentra el departamento"
**Causa:** Departamento no existe en la base de datos

**Solución:**
1. Usa exactamente: CAQUETA (en mayúsculas)
2. Si no aparece, ejecuta: `python sync_auto.py`

### El formulario no muestra opciones
**Causa:** JavaScript no está cargando o hay error en el navegador

**Solución:**
1. Abre la consola del navegador (F12)
2. Verifica si hay errores
3. Recarga la página (Ctrl+F5)

---

**✅ Recuerda: La contraseña es `test123`, NO un email**

**Última actualización:** 2025-11-15 15:20
