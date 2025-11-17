# 🔐 Credenciales del Sistema Electoral

**Fecha:** 17 de Noviembre de 2025  
**Contraseña Universal:** `test123`

---

## 📊 Resumen

- **Total de usuarios:** 66
- **Contraseña para todos:** `test123`
- **Roles:** 7 tipos diferentes

---

## 👤 SUPER ADMIN (1 usuario)

### Usuario: Super Admin
- **ID:** 1
- **Contraseña:** `test123`
- **Ubicación:** Sin ubicación (acceso global)

**Login:**
```json
{
  "rol": "super_admin",
  "password": "test123"
}
```

---

## 🏛️ COORDINADOR DEPARTAMENTAL (1 usuario)

### Usuario: Coordinador Departamental Caquetá
- **ID:** 4
- **Contraseña:** `test123`
- **Ubicación:** CAQUETA (Departamento)

**Login:**
```json
{
  "rol": "coordinador_departamental",
  "departamento_codigo": "18",
  "password": "test123"
}
```

---

## 🏙️ COORDINADOR MUNICIPAL (2 usuarios)

### 1. Usuario: Coordinador Municipal Florencia
- **ID:** 5
- **Contraseña:** `test123`
- **Ubicación:** CAQUETA - FLORENCIA

**Login:**
```json
{
  "rol": "coordinador_municipal",
  "departamento_codigo": "18",
  "municipio_codigo": "01",
  "password": "test123"
}
```

### 2. Usuario: coord.mun.02
- **ID:** 10
- **Contraseña:** `test123`
- **Ubicación:** CAQUETA - FLORENCIA

**Login:** (mismo que el anterior)

---

## 🏫 COORDINADOR DE PUESTO (2 usuarios)

### 1. Usuario: Coordinador Puesto 01
- **ID:** 7
- **Contraseña:** `test123`
- **Ubicación:** I.E. JUAN BAUTISTA LA SALLE

**Login:**
```json
{
  "rol": "coordinador_puesto",
  "departamento_codigo": "18",
  "municipio_codigo": "01",
  "zona_codigo": "01",
  "puesto_codigo": "01",
  "password": "test123"
}
```

### 2. Usuario: coord.puesto.25
- **ID:** 9
- **Contraseña:** `test123`
- **Ubicación:** I.E. JUAN BAUTISTA MIGANI

**Login:**
```json
{
  "rol": "coordinador_puesto",
  "departamento_codigo": "18",
  "municipio_codigo": "01",
  "zona_codigo": "01",
  "puesto_codigo": "02",
  "password": "test123"
}
```

---

## 📋 TESTIGO ELECTORAL (56 usuarios)

**Nota:** Los testigos se autentican a nivel de puesto, no de mesa específica.

### Usuario de Prueba Principal: Testigo La Salle Mesa 01
- **ID:** 66
- **Contraseña:** `test123`
- **Ubicación:** ORTEGUAZA - SAN ANTONIO DE ATENAS. (Puesto)

**Login:**
```json
{
  "rol": "testigo_electoral",
  "departamento_codigo": "18",
  "municipio_codigo": "01",
  "zona_codigo": "99",
  "puesto_codigo": "06",
  "password": "test123"
}
```

### Otros 55 Testigos
Todos los testigos tienen:
- **Contraseña:** `test123`
- **Ubicaciones:** Distribuidos en diferentes puestos de votación de Florencia
- **Login:** Requiere códigos de departamento, municipio, zona y puesto según su ubicación

**Ejemplos de testigos:**
- Testigo I.E. JUAN BAUTISTA LA SALLE (ID: 8)
- Testigo I.E. JUAN BAUTISTA MIGANI (ID: 12)
- Testigo I.E. SAGRADO CORAZON DE JESUS (ID: 13)
- Testigo I.E. HOOVER CUELLAR CASTILLO (ID: 14)
- ... (51 testigos más)

---

## 🔍 AUDITOR ELECTORAL (1 usuario)

### Usuario: Auditor Electoral Caquetá
- **ID:** 6
- **Contraseña:** `test123`
- **Ubicación:** CAQUETA (Departamento)

**Login:**
```json
{
  "rol": "auditor_electoral",
  "departamento_codigo": "18",
  "password": "test123"
}
```

---

## 🏢 ADMIN DEPARTAMENTAL (1 usuario)

### Usuario: Admin Departamental Caquetá
- **ID:** 2
- **Contraseña:** `test123`
- **Ubicación:** Sin ubicación (acceso global)

**Login:**
```json
{
  "rol": "admin_departamental",
  "password": "test123"
}
```

---

## 🏘️ ADMIN MUNICIPAL (2 usuarios)

### 1. Usuario: Admin Municipal Florencia
- **ID:** 3
- **Contraseña:** `test123`
- **Ubicación:** Sin ubicación (acceso global)

**Login:**
```json
{
  "rol": "admin_municipal",
  "password": "test123"
}
```

### 2. Usuario: admin.mun.02
- **ID:** 11
- **Contraseña:** `test123`
- **Ubicación:** Sin ubicación (acceso global)

**Login:** (mismo que el anterior)

---

## 📝 Notas Importantes

### Estructura de Login por Rol

1. **Super Admin:** Solo requiere rol y contraseña
2. **Admin Departamental/Municipal:** Solo requiere rol y contraseña (sin ubicación)
3. **Coordinador Departamental:** Requiere código de departamento
4. **Coordinador Municipal:** Requiere código de departamento y municipio
5. **Coordinador de Puesto:** Requiere departamento, municipio, zona y puesto
6. **Testigo Electoral:** Requiere departamento, municipio, zona y puesto (se autentica a nivel de puesto)
7. **Auditor Electoral:** Requiere código de departamento

### Códigos de Ubicación

- **Departamento Caquetá:** `18`
- **Municipio Florencia:** `01`
- **Zonas:** `01`, `02`, `03`, `04`, `90`, `98`, `99`
- **Puestos:** `01` a `09` (varía por zona)

### Seguridad

⚠️ **IMPORTANTE:** Todas las contraseñas están configuradas como `test123` para facilitar las pruebas del sistema. En producción, cada usuario debe tener una contraseña única y segura.

---

## 🔄 Resetear Contraseñas

Si necesitas resetear todas las contraseñas a `test123`:

```bash
python reset_passwords_simple.py
```

---

## ✅ Estado de Verificación

- ✅ Todos los usuarios tienen contraseña `test123`
- ✅ Todos los usuarios están activos
- ✅ Todas las ubicaciones son válidas
- ✅ Login probado y funcional para todos los roles
