# 🔐 Guía Rápida de Credenciales

## ✅ Estado Actual

**Última verificación:** 2025-11-15 13:05  
**Estado:** ✅ Todas las contraseñas funcionando correctamente  
**Contraseña universal:** `test123`

## 🚀 Acceso Rápido

### Opción 1: Super Admin (Sin ubicación)
```
URL: https://mvp-b9uv.onrender.com/auth/login
Rol: Super Admin
Contraseña: test123
```

### Opción 2: Testigo Electoral (Con ubicación completa)
```
URL: https://mvp-b9uv.onrender.com/auth/login
Rol: Testigo Electoral
Departamento: CAQUETA
Municipio: FLORENCIA
Zona: CAQUETA - FLORENCIA - Zona 01
Puesto: I.E. JUAN BAUTISTA LA SALLE
Contraseña: test123
```

### Opción 3: Coordinador Departamental
```
URL: https://mvp-b9uv.onrender.com/auth/login
Rol: Coordinador Departamental
Departamento: CAQUETA
Contraseña: test123
```

## 📊 Todos los Usuarios

| # | Rol | Nombre | Departamento | Municipio | Contraseña |
|---|-----|--------|--------------|-----------|------------|
| 1 | Super Admin | Super Admin | - | - | test123 |
| 2 | Admin Departamental | Admin Departamental Caquetá | CAQUETA | - | test123 |
| 3 | Admin Municipal | Admin Municipal Florencia | CAQUETA | FLORENCIA | test123 |
| 4 | Coordinador Departamental | Coordinador Departamental Caquetá | CAQUETA | - | test123 |
| 5 | Coordinador Municipal | Coordinador Municipal Florencia | CAQUETA | FLORENCIA | test123 |
| 6 | Coordinador Puesto | Coordinador Puesto 01 | CAQUETA | FLORENCIA | test123 |
| 7 | Auditor Electoral | Auditor Electoral Caquetá | CAQUETA | - | test123 |
| 8 | Testigo Electoral | Testigo Electoral Puesto 01 | CAQUETA | FLORENCIA | test123 |

## 🌐 URLs

- **Producción (Render):** https://mvp-b9uv.onrender.com/auth/login
- **Local (Desarrollo):** http://localhost:5000/auth/login

## 📚 Documentación Completa

Para información detallada, consulta:

1. **[CREDENCIALES_USUARIOS.md](./CREDENCIALES_USUARIOS.md)**  
   Lista completa con detalles de cada usuario

2. **[RESUMEN_CREDENCIALES.md](./RESUMEN_CREDENCIALES.md)**  
   Resumen ejecutivo con tabla de usuarios

3. **[VERIFICACION_CONTRASEÑAS.md](./VERIFICACION_CONTRASEÑAS.md)**  
   Pruebas y verificación de que todo funciona

## 🔧 Herramientas

### Resetear contraseñas
```bash
# En Render
curl -X POST "https://mvp-b9uv.onrender.com/api/admin-tools/reset-passwords?admin_key=temp_admin_key_2024"

# En Local
curl -X POST "http://localhost:5000/api/admin-tools/reset-passwords?admin_key=temp_admin_key_2024"
```

### Verificar login
```bash
python verificar_login_local.py
```

### Sincronizar datos
```bash
python sync_auto.py
```

## ⚠️ Importante

- ✅ Contraseña verificada y funcionando: `test123`
- ✅ Funciona en Render y Local
- ✅ Todos los 8 usuarios tienen la misma contraseña
- ⚠️ Solo para desarrollo y testing
- ⚠️ En producción real usar contraseñas seguras individuales

## 🆘 Problemas Comunes

### "Credenciales inválidas"
1. Verifica que estés usando `test123` (minúsculas)
2. Verifica que hayas seleccionado el departamento correcto
3. Ejecuta el reseteo de contraseñas nuevamente

### "No se encuentra el departamento"
- Usa: **CAQUETA** (código: 44)
- Usa: **FLORENCIA** (código: 01)

### "Error de conexión"
- Render puede estar iniciando (plan gratuito)
- Espera 30-60 segundos e intenta nuevamente

---

**✅ Todo verificado y funcionando correctamente**  
**Última actualización:** 2025-11-15 13:05
