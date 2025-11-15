# 🔐 Credenciales de Usuarios - Sistema Electoral

**Fecha de generación:** 2025-11-15 12:54:12

**⚠️ IMPORTANTE:** Todas las contraseñas han sido reseteadas a `test123`

---

## 🌐 URLs de Acceso

- **Producción (Render):** https://mvp-b9uv.onrender.com/auth/login
- **Local (Desarrollo):** http://localhost:5000/auth/login

---

## 📊 Resumen

**Total de usuarios:** 8

- **Admin Departamental:** 1 usuario(s)
- **Admin Municipal:** 1 usuario(s)
- **Auditor Electoral:** 1 usuario(s)
- **Coordinador Departamental:** 1 usuario(s)
- **Coordinador Municipal:** 1 usuario(s)
- **Coordinador Puesto:** 1 usuario(s)
- **Super Admin:** 1 usuario(s)
- **Testigo Electoral:** 1 usuario(s)

---

## 👥 Usuarios por Rol

### Super Admin

**Usuario:** Super Admin

```
Nombre: Super Admin
Rol: super_admin
Ubicación: Sin ubicación asignada
Contraseña: test123
```

---

### Admin Departamental

**Usuario:** Admin Departamental Caquetá

```
Nombre: Admin Departamental Caquetá
Rol: admin_departamental
Departamento: CAQUETA (código: 44)
Contraseña: test123
```

---

### Admin Municipal

**Usuario:** Admin Municipal Florencia

```
Nombre: Admin Municipal Florencia
Rol: admin_municipal
Departamento: CAQUETA (código: 44)
Municipio: FLORENCIA (código: 01)
Contraseña: test123
```

---

### Coordinador Departamental

**Usuario:** Coordinador Departamental Caquetá

```
Nombre: Coordinador Departamental Caquetá
Rol: coordinador_departamental
Departamento: CAQUETA (código: 44)
Contraseña: test123
```

---

### Coordinador Municipal

**Usuario:** Coordinador Municipal Florencia

```
Nombre: Coordinador Municipal Florencia
Rol: coordinador_municipal
Departamento: CAQUETA (código: 44)
Municipio: FLORENCIA (código: 01)
Contraseña: test123
```

---

### Coordinador Puesto

**Usuario:** Coordinador Puesto 01

```
Nombre: Coordinador Puesto 01
Rol: coordinador_puesto
Departamento: CAQUETA (código: 44)
Municipio: FLORENCIA (código: 01)
Zona: CAQUETA - FLORENCIA - Zona 01
Puesto: I.E. JUAN BAUTISTA LA SALLE (código: 01)
Contraseña: test123
```

---

### Auditor Electoral

**Usuario:** Auditor Electoral Caquetá

```
Nombre: Auditor Electoral Caquetá
Rol: auditor_electoral
Departamento: CAQUETA (código: 44)
Contraseña: test123
```

---

### Testigo Electoral

**Usuario:** Testigo Electoral Puesto 01

```
Nombre: Testigo Electoral Puesto 01
Rol: testigo_electoral
Departamento: CAQUETA (código: 44)
Municipio: FLORENCIA (código: 01)
Zona: CAQUETA - FLORENCIA - Zona 01
Puesto: I.E. JUAN BAUTISTA LA SALLE (código: 01)
Contraseña: test123
```

---

## 📝 Instrucciones de Uso

### Para Render (Producción)

1. Ir a: https://mvp-b9uv.onrender.com/auth/login
2. Seleccionar el rol del usuario
3. Seleccionar departamento y municipio según corresponda
4. Ingresar contraseña: `test123`

### Para Local (Desarrollo)

1. Asegurarse de que el servidor esté corriendo: `python run.py`
2. Ir a: http://localhost:5000/auth/login
3. Seleccionar el rol del usuario
4. Seleccionar departamento y municipio según corresponda
5. Ingresar contraseña: `test123`

---

## ⚠️ Notas de Seguridad

- **Esta contraseña es solo para desarrollo y testing**
- En producción real, cada usuario debe tener su propia contraseña segura
- Las contraseñas están hasheadas con bcrypt en la base de datos
- Para cambiar contraseñas en producción, usar el panel de Super Admin

---

## 📌 Información Adicional

### Departamento Principal
- **CAQUETA** (código: 44)
  - 16 municipios
  - 38 zonas
  - 150 puestos de votación
  - 196 mesas

### Municipio Principal
- **FLORENCIA** (código: 01)
  - Capital del departamento de Caquetá
  - Múltiples zonas y puestos de votación

---

## 🆘 Soporte

Si tienes problemas para acceder:

1. Verifica que estés usando la contraseña correcta: `test123`
2. Verifica que hayas seleccionado el departamento y municipio correctos
3. Si el problema persiste, ejecuta el script de reseteo:
   ```bash
   python sync_auto.py
   ```
