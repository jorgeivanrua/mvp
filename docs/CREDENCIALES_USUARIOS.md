# 🔑 CREDENCIALES DE USUARIOS DEL SISTEMA ELECTORAL

## 🚨 **SISTEMA DE LOGIN UNIFICADO**

**Todos los usuarios usan la misma URL**: http://localhost:5000/login

El formulario cambia dinámicamente según el **rol seleccionado**:
- **Administradores/Coordinadores**: Muestran campos de ubicación
- **Testigos**: Muestran campo de cédula

---

## 👥 **USUARIOS DEL SISTEMA**

### 🔴 **SUPER ADMINISTRADOR**
- **URL**: http://localhost:5000/login
- **Rol**: `super_admin`
- **Ubicación**: No requiere
- **Contraseña**: `admin123`

### 🟡 **MONITOREO**
- **URL**: http://localhost:5000/login
- **Rol**: `monitoreo`
- **Ubicación**: No requiere
- **Contraseña**: `test123`

### 🟢 **COORDINADOR DEPARTAMENTAL**
- **URL**: http://localhost:5000/login
- **Rol**: `coordinador_departamental`
- **Departamento**: Código del departamento
- **Contraseña**: `test123`

### 🔵 **COORDINADOR MUNICIPAL**
- **URL**: http://localhost:5000/login
- **Rol**: `coordinador_municipal`
- **Departamento**: Código del departamento
- **Municipio**: Código del municipio
- **Contraseña**: `test123`

### 🟣 **COORDINADOR DE PUESTO**
- **URL**: http://localhost:5000/login
- **Rol**: `coordinador_puesto`
- **Departamento**: `26` (Putumayo)
- **Municipio**: `2601` (Mocoa)
- **Zona**: `260101`
- **Puesto**: `26010103`
- **Contraseña**: `test123`

### 🟠 **AUDITOR ELECTORAL**
- **URL**: http://localhost:5000/login
- **Rol**: `auditor_electoral`
- **Departamento**: Código del departamento
- **Contraseña**: `test123`

### 🗳️ **TESTIGOS ELECTORALES**
- **URL**: http://localhost:5000/login
- **Rol**: `testigo_electoral`
- **Cédula**: Número de cédula del testigo (ej: `2601010101001`)
- **Contraseña**: `test123`

**✅ TESTIGOS DISPONIBLES**: 212 testigos registrados con cédulas únicas

**Ejemplos de cédulas disponibles:**
- `2601010101001`
- `2601010102001`
- `2601010201001`
- `2601010202001`
- ... (212 testigos en total)

**FLUJO ESPECIAL PARA TESTIGOS:**
1. Login con cédula (NO necesitan ubicación)
2. Acceden al dashboard sin ubicación fija
3. Se verifican en una mesa específica
4. La mesa se guarda para futuras sesiones

---

## 🚀 **CÓMO HACER LOGIN**

### **Paso a paso:**
1. Ve a: **http://localhost:5000/login**
2. **Selecciona el rol** en el dropdown
3. **El formulario cambia automáticamente**:
   - **Si eliges admin/coordinador**: Aparecen campos de ubicación
   - **Si eliges testigo**: Aparece campo de cédula
4. Completa los campos requeridos
5. Ingresa la contraseña
6. Haz clic en "Iniciar Sesión"

---

## 📋 **CREDENCIALES RÁPIDAS PARA PRUEBAS**

```
SUPER ADMIN:
- Rol: super_admin
- Contraseña: admin123

COORDINADOR DE PUESTO:
- Rol: coordinador_puesto
- Departamento: 26
- Municipio: 2601
- Zona: 260101
- Puesto: 26010103
- Contraseña: test123

MONITOREO:
- Rol: monitoreo
- Contraseña: test123

TESTIGO:
- Rol: testigo_electoral
- Cédula: 2601010101001 (o cualquier cédula de los 212 disponibles)
- Contraseña: test123
```

---

## ⚠️ **NOTAS IMPORTANTES**

- **Una sola URL de login**: http://localhost:5000/login
- **Formulario dinámico** que cambia según el rol
- **Los testigos están configurados** - 212 testigos disponibles con login por cédula
- **Las contraseñas están hasheadas** por seguridad
- **Cambiar contraseñas** en producción

---

**Sistema Electoral - Versión MVP**  
**Estado**: ✅ Completamente funcional  
**Servidor**: http://localhost:5000