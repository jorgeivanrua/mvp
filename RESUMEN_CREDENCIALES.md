# 🔐 Resumen - Credenciales Actualizadas

## ✅ Acción Completada

**Fecha:** 2025-11-15 12:55
**Acción:** Reseteo masivo de contraseñas en Render

## 📊 Resultado

- ✅ **8 usuarios actualizados** en Render
- ✅ **8 usuarios actualizados** en Local
- ✅ **Contraseña única:** `test123` para todos

## 🌐 Ambientes Sincronizados

### Render (Producción)
- URL: https://mvp-b9uv.onrender.com/auth/login
- Estado: ✅ Contraseñas reseteadas
- Usuarios: 8
- Contraseña: test123

### Local (Desarrollo)
- URL: http://localhost:5000/auth/login
- Estado: ✅ Contraseñas reseteadas
- Usuarios: 8
- Contraseña: test123

## 👥 Usuarios Disponibles

| Rol | Nombre | Departamento | Municipio | Contraseña |
|-----|--------|--------------|-----------|------------|
| Super Admin | Super Admin | - | - | test123 |
| Admin Departamental | Admin Departamental Caquetá | CAQUETA | - | test123 |
| Admin Municipal | Admin Municipal Florencia | CAQUETA | FLORENCIA | test123 |
| Coordinador Departamental | Coordinador Departamental Caquetá | CAQUETA | - | test123 |
| Coordinador Municipal | Coordinador Municipal Florencia | CAQUETA | FLORENCIA | test123 |
| Coordinador Puesto | Coordinador Puesto 01 | CAQUETA | FLORENCIA | test123 |
| Auditor Electoral | Auditor Electoral Caquetá | CAQUETA | - | test123 |
| Testigo Electoral | Testigo Electoral Puesto 01 | CAQUETA | FLORENCIA | test123 |

## 📝 Documento Completo

Para ver las credenciales detalladas de todos los usuarios, consulta:
**[CREDENCIALES_USUARIOS.md](./CREDENCIALES_USUARIOS.md)**

## 🚀 Cómo Usar

### Acceso Rápido - Testigo Electoral
```
URL: https://mvp-b9uv.onrender.com/auth/login
Rol: Testigo Electoral
Departamento: CAQUETA
Municipio: FLORENCIA
Zona: CAQUETA - FLORENCIA - Zona 01
Puesto: I.E. JUAN BAUTISTA LA SALLE
Contraseña: test123
```

### Acceso Rápido - Super Admin
```
URL: https://mvp-b9uv.onrender.com/auth/login
Rol: Super Admin
Contraseña: test123
```

## 🔧 Herramientas Disponibles

### Resetear Contraseñas Nuevamente
```bash
# Via API
curl -X POST "https://mvp-b9uv.onrender.com/api/admin-tools/reset-passwords?admin_key=temp_admin_key_2024"

# Via Script
python sync_auto.py
```

### Verificar Estado
```bash
# Ver estadísticas de Render
curl "https://mvp-b9uv.onrender.com/api/admin-tools/stats?admin_key=temp_admin_key_2024"

# Ver estadísticas de Local
curl "http://localhost:5000/api/admin-tools/stats?admin_key=temp_admin_key_2024"
```

## ⚠️ Importante

- Esta contraseña (`test123`) es **solo para desarrollo y testing**
- En producción real, cada usuario debe tener su propia contraseña segura
- Las contraseñas están hasheadas con bcrypt en la base de datos
- Para cambiar contraseñas individuales, usar el panel de Super Admin

## 📌 Próximos Pasos

1. ✅ Probar acceso con cada rol
2. ✅ Verificar funcionalidades de cada dashboard
3. ⏳ Configurar contraseñas seguras para producción real
4. ⏳ Implementar sistema de recuperación de contraseñas

---

**Estado:** ✅ Completado
**Última actualización:** 2025-11-15 12:55
