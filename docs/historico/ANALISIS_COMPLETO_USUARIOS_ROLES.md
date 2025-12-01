# 👥 Análisis Completo: Usuarios y Roles del Sistema

## 📊 Resumen Ejecutivo

**Total de usuarios**: 13  
**Usuarios activos**: 13  
**Roles en uso**: 7 de 9 definidos  
**Usuarios con GPS**: 0 (normal en desarrollo)

## 🎭 Roles Definidos en el Sistema

### 1. **super_admin** (2 usuarios)
- **Descripción**: Administrador principal del sistema
- **Geolocalización**: Opcional
- **Dashboard**: `/admin/super-admin-dashboard`
- **Permisos**: Todos (crear, editar, eliminar, configurar)
- **Usuarios**:
  - `Super Admin` (último acceso: 2025-11-30)
  - `super_admin` (nunca accedió)

### 2. **monitoreo** (2 usuarios) ⭐
- **Descripción**: Supervisión en tiempo real
- **Geolocalización**: Solo lectura (ve todos)
- **Dashboard**: `/monitoreo/dashboard`
- **Permisos**: Solo lectura (supervisión)
- **Usuarios**:
  - `Monitoreo` (nunca accedió)
  - `monitoreo` (último acceso: 2025-11-29)

### 3. **auditor_electoral** (2 usuarios)
- **Descripción**: Auditoría del proceso electoral
- **Geolocalización**: Activa (envía su ubicación)
- **Dashboard**: `/auditor/dashboard`
- **Permisos**: Solo lectura (auditoría)
- **Usuarios**:
  - `Auditor Electoral` (nunca accedió)
  - `auditor` (nunca accedió)

### 4. **coordinador_departamental** (2 usuarios)
- **Descripción**: Coordinación a nivel departamental
- **Geolocalización**: Activa (envía su ubicación)
- **Dashboard**: `/coordinador/departamental`
- **Permisos**: Supervisión de su departamento
- **Usuarios**:
  - `Coordinador Departamental` (nunca accedió)
  - `coord_dept` (nunca accedió)

### 5. **coordinador_municipal** (2 usuarios)
- **Descripción**: Coordinación a nivel municipal
- **Geolocalización**: Activa (envía su ubicación)
- **Dashboard**: `/coordinador/municipal`
- **Permisos**: Supervisión de su municipio
- **Usuarios**:
  - `Coordinador Municipal` (nunca accedió)
  - `coord_mun` (nunca accedió)

### 6. **coordinador_puesto** (2 usuarios)
- **Descripción**: Coordinación de puesto de votación
- **Geolocalización**: Activa (envía su ubicación)
- **Dashboard**: `/coordinador/puesto`
- **Permisos**: Supervisión de su puesto
- **Usuarios**:
  - `Coordinador Puesto` (nunca accedió)
  - `coord_puesto` (nunca accedió)

### 7. **testigo_electoral** (1 usuario)
- **Descripción**: Testigo en mesa de votación
- **Geolocalización**: Activa (envía su ubicación)
- **Dashboard**: `/testigo/dashboard`
- **Permisos**: Registro de votos e incidentes
- **Usuarios**:
  - `testigo1` (nunca accedió)

### 8. **admin_departamental** (0 usuarios) ⚠️
- **Descripción**: Administrador departamental
- **Geolocalización**: Opcional
- **Dashboard**: `/admin/departamental`
- **Permisos**: Administración de su departamento
- **Estado**: Sin usuarios creados

### 9. **admin_municipal** (0 usuarios) ⚠️
- **Descripción**: Administrador municipal
- **Geolocalización**: Opcional
- **Dashboard**: `/admin/municipal`
- **Permisos**: Administración de su municipio
- **Estado**: Sin usuarios creados

## 📋 Usuarios Básicos del Sistema

Los **usuarios básicos** son usuarios fijos del sistema que no se pueden eliminar y solo el super admin puede modificar. Actualmente hay **12 usuarios básicos**:

1. `monitoreo` (monitoreo)
2. `auditor` (auditor_electoral)
3. `coord_dept` (coordinador_departamental)
4. `coord_mun` (coordinador_municipal)
5. `coord_puesto` (coordinador_puesto)
6. `Super Admin` (super_admin)
7. `super_admin` (super_admin)
8. `Monitoreo` (monitoreo)
9. `Coordinador Departamental` (coordinador_departamental)
10. `Coordinador Municipal` (coordinador_municipal)
11. `Coordinador Puesto` (coordinador_puesto)
12. `Auditor Electoral` (auditor_electoral)

## 🗺️ Geolocalización por Rol

### Roles con Geolocalización Activa (Envían GPS)
1. **testigo_electoral** - Verifica presencia en mesa
2. **coordinador_puesto** - Supervisa puesto
3. **coordinador_municipal** - Supervisa municipio
4. **coordinador_departamental** - Supervisa departamento
5. **auditor_electoral** - Auditoría en campo

### Roles con Geolocalización Pasiva (Solo Ven)
6. **monitoreo** - Dashboard de supervisión
7. **super_admin** - Administración general

### Roles sin Geolocalización
8. **admin_departamental** - Administración de escritorio
9. **admin_municipal** - Administración de escritorio

## 🔐 Credenciales de Acceso

### Usuarios Principales

| Usuario | Rol | Contraseña | Dashboard |
|---------|-----|------------|-----------|
| Super Admin | super_admin | admin123 | /admin/super-admin-dashboard |
| Monitoreo | monitoreo | test123 | /monitoreo/dashboard |
| Coordinador Departamental | coordinador_departamental | test123 | /coordinador/departamental |
| Coordinador Municipal | coordinador_municipal | test123 | /coordinador/municipal |
| Coordinador Puesto | coordinador_puesto | test123 | /coordinador/puesto |
| Auditor Electoral | auditor_electoral | test123 | /auditor/dashboard |

### Usuarios Alternativos

| Usuario | Rol | Contraseña |
|---------|-----|------------|
| super_admin | super_admin | test123 |
| monitoreo | monitoreo | test123 |
| coord_dept | coordinador_departamental | test123 |
| coord_mun | coordinador_municipal | test123 |
| coord_puesto | coordinador_puesto | test123 |
| auditor | auditor_electoral | test123 |
| testigo1 | testigo_electoral | test123 |

## 📊 Estadísticas Detalladas

### Por Estado
- **Activos**: 13 (100%)
- **Inactivos**: 0 (0%)
- **Bloqueados**: 0 (0%)
- **Con intentos fallidos**: 1 (7.7%)

### Por Ubicación
- **Con ubicación asignada**: 0 (0%)
- **Sin ubicación**: 13 (100%)

### Por Geolocalización
- **Con GPS activo**: 0 (0%)
- **Sin GPS**: 13 (100%)
- **Nota**: Normal en desarrollo, se activa al iniciar sesión

### Por Presencia (Solo Testigos)
- **Presencia verificada**: 0 de 1 (0%)
- **Sin verificar**: 1 de 1 (100%)

## 🎯 Matriz de Permisos

| Acción | Super Admin | Monitoreo | Auditor | Coord. Depto | Coord. Muni | Coord. Puesto | Testigo | Admin Depto | Admin Muni |
|--------|-------------|-----------|---------|--------------|-------------|---------------|---------|-------------|------------|
| Configurar sistema | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ |
| Ver todos los usuarios | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ |
| Ver geolocalización | ✅ | ✅ | ✅* | ✅* | ✅* | ✅* | ❌ | ⚠️ | ⚠️ |
| Enviar geolocalización | ⚠️ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| Validar formularios | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ⚠️ | ⚠️ |
| Registrar votos | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Reportar incidentes | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |
| Resolver incidentes | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ⚠️ | ⚠️ |
| Exportar reportes | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ⚠️ | ⚠️ |
| Crear usuarios | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ |

**Leyenda**:
- ✅ = Permitido
- ❌ = No permitido
- ⚠️ = Rol sin usuarios (no implementado)
- \* = Solo de su área asignada

## 🔄 Flujo de Trabajo por Rol

### 1. Super Admin
```
1. Login → /admin/super-admin-dashboard
2. Configurar sistema (partidos, candidatos, tipos de elección)
3. Crear usuarios y asignar ubicaciones
4. Supervisar todo el proceso
5. Validar formularios de cualquier nivel
6. Resolver incidentes críticos
7. Exportar reportes finales
```

### 2. Monitoreo
```
1. Login → /monitoreo/dashboard
2. Ver mapa con todos los usuarios en tiempo real
3. Recibir alertas automáticas
4. Ver estadísticas globales
5. Exportar reportes de supervisión
6. NO puede modificar nada (solo lectura)
```

### 3. Coordinador Departamental
```
1. Login → /coordinador/departamental
2. Enviar geolocalización automática
3. Ver testigos y coordinadores de su departamento
4. Validar formularios E-24 departamentales
5. Supervisar coordinadores municipales
6. Resolver incidentes de su departamento
7. Exportar reportes departamentales
```

### 4. Coordinador Municipal
```
1. Login → /coordinador/municipal
2. Enviar geolocalización automática
3. Ver testigos y coordinadores de su municipio
4. Validar formularios E-24 municipales
5. Supervisar coordinadores de puesto
6. Resolver incidentes de su municipio
7. Exportar reportes municipales
```

### 5. Coordinador de Puesto
```
1. Login → /coordinador/puesto
2. Enviar geolocalización automática
3. Ver testigos de su puesto
4. Validar formularios E-14 de su puesto
5. Supervisar mesas de votación
6. Resolver incidentes de su puesto
7. Consolidar E-24 de puesto
```

### 6. Testigo Electoral
```
1. Login → /testigo/dashboard
2. Verificar presencia en mesa
3. Enviar geolocalización automática
4. Registrar votos en formulario E-14
5. Reportar incidentes
6. Reportar delitos electorales
7. Enviar formulario final
```

### 7. Auditor Electoral
```
1. Login → /auditor/dashboard
2. Enviar geolocalización automática
3. Ver formularios de su área
4. Reportar incidentes
5. Exportar reportes de auditoría
6. NO puede modificar formularios (solo lectura)
```

## 🛠️ Comandos Útiles

### Crear Usuarios Básicos
```bash
python scripts/init_system.py
```

### Resetear Contraseñas
```bash
python scripts/init_system.py --reset-passwords
```

### Verificar Usuarios
```bash
python test_usuarios_roles.py
```

### Crear Usuario de Monitoreo
```bash
python scripts/verificar_monitoreo.py
```

## ⚠️ Observaciones Importantes

### Usuarios Duplicados
Hay usuarios duplicados con diferentes nombres pero mismo rol:
- 2 super_admin: `Super Admin` y `super_admin`
- 2 monitoreo: `Monitoreo` y `monitoreo`
- 2 de cada coordinador
- 2 auditores

**Recomendación**: Mantener solo un usuario por rol básico o documentar claramente el propósito de cada uno.

### Roles sin Usuarios
- `admin_departamental`: 0 usuarios
- `admin_municipal`: 0 usuarios

**Recomendación**: Decidir si estos roles son necesarios o eliminarlos del sistema.

### Sin Ubicaciones Asignadas
Ningún usuario tiene ubicación asignada actualmente.

**Recomendación**: Asignar ubicaciones a coordinadores y testigos para que el sistema funcione correctamente.

### Sin Geolocalización
Ningún usuario ha compartido su ubicación aún.

**Recomendación**: Normal en desarrollo. Se activará automáticamente al iniciar sesión desde dispositivos móviles.

## 📝 Recomendaciones Finales

### Inmediatas
1. ✅ Decidir sobre usuarios duplicados
2. ✅ Asignar ubicaciones a usuarios operativos
3. ✅ Documentar credenciales de acceso
4. ✅ Cambiar contraseñas por defecto en producción

### A Mediano Plazo
1. ⚠️ Implementar o eliminar roles admin_departamental y admin_municipal
2. ⚠️ Crear más testigos para pruebas
3. ⚠️ Probar geolocalización en dispositivos móviles
4. ⚠️ Implementar rotación de contraseñas

### Seguridad
1. 🔒 Cambiar todas las contraseñas "test123" en producción
2. 🔒 Implementar 2FA para super_admin
3. 🔒 Auditar accesos regularmente
4. 🔒 Implementar políticas de contraseñas fuertes

---

**Fecha**: 30 de Noviembre de 2025  
**Versión**: 1.0.0  
**Estado**: ✅ DOCUMENTADO Y VERIFICADO
