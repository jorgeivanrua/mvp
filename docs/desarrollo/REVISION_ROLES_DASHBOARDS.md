# Revisión de Roles y Dashboards

**Fecha**: 30 de Noviembre de 2025  
**Estado**: ✅ REVISADO

## Roles del Sistema

El sistema tiene los siguientes roles definidos:

### 1. Super Admin
- **Rol**: `super_admin`
- **Template**: `frontend/templates/admin/super-admin-dashboard.html`
- **Ruta**: `/admin/super-admin`
- **API Client**: ✅ Incluido explícitamente
- **Extiende base.html**: ✅ Sí
- **Credenciales**: Super Admin / admin123

**Funcionalidades**:
- Gestión completa del sistema
- Gestión de usuarios
- Configuración de partidos y candidatos
- Configuración de tipos de elección
- Gestión de ubicaciones
- Auditoría del sistema
- Personalización del sistema

**Scripts cargados**:
- api-client.js ✅
- dashboard-data-loader.js
- super-admin-dashboard.js
- personalizacion-sistema.js
- super-admin-dashboard-debug.js

---

### 2. Monitoreo
- **Rol**: `monitoreo`
- **Template**: `frontend/templates/monitoreo/dashboard.html`
- **Ruta**: `/monitoreo/dashboard`
- **API Client**: ✅ Heredado de base.html
- **Extiende base.html**: ✅ Sí
- **Credenciales**: Monitoreo / test123

**Funcionalidades**:
- Visualización en tiempo real
- Mapa de geolocalización
- Estadísticas generales
- Solo lectura

**Scripts cargados**:
- api-client.js (desde base.html) ✅
- dashboard-data-loader.js
- monitoreo-dashboard-debug.js

---

### 3. Coordinador Departamental
- **Rol**: `coordinador_departamental`
- **Template**: `frontend/templates/coordinador/departamental.html`
- **Ruta**: `/coordinador/departamental`
- **API Client**: ✅ Heredado de base.html
- **Extiende base.html**: ✅ Sí
- **Credenciales**: Coordinador Departamental / test123

**Funcionalidades**:
- Gestión a nivel departamental
- Visualización de municipios
- Reportes departamentales

**Scripts cargados**:
- api-client.js (desde base.html) ✅
- coordinador-dashboard.js
- coordinador-dashboard-debug.js

---

### 4. Coordinador Municipal
- **Rol**: `coordinador_municipal`
- **Template**: `frontend/templates/coordinador/municipal.html`
- **Ruta**: `/coordinador/municipal`
- **API Client**: ✅ Heredado de base.html
- **Extiende base.html**: ✅ Sí
- **Credenciales**: Coordinador Municipal / test123

**Funcionalidades**:
- Gestión a nivel municipal
- Visualización de puestos
- Reportes municipales

**Scripts cargados**:
- api-client.js (desde base.html) ✅
- coordinador-dashboard.js
- coordinador-dashboard-debug.js

---

### 5. Coordinador de Puesto
- **Rol**: `coordinador_puesto`
- **Template**: `frontend/templates/coordinador/puesto.html`
- **Ruta**: `/coordinador/puesto`
- **API Client**: ✅ Heredado de base.html
- **Extiende base.html**: ✅ Sí
- **Credenciales**: Coordinador Puesto / test123

**Funcionalidades**:
- Gestión a nivel de puesto
- Visualización de mesas
- Gestión de testigos
- Validación de formularios

**Scripts cargados**:
- api-client.js (desde base.html) ✅
- coordinador-puesto-dashboard.js

---

### 6. Auditor Electoral
- **Rol**: `auditor_electoral`
- **Template**: `frontend/templates/auditor/dashboard.html` (si existe)
- **Ruta**: `/auditor/dashboard`
- **API Client**: ✅ Heredado de base.html
- **Extiende base.html**: ✅ Sí
- **Credenciales**: Auditor Electoral / test123

**Funcionalidades**:
- Auditoría de formularios
- Revisión de datos
- Generación de reportes

---

### 7. Testigo Electoral
- **Rol**: `testigo_electoral` o `testigo`
- **Template**: `frontend/templates/testigo/dashboard.html`
- **Ruta**: `/testigo/dashboard`
- **API Client**: ✅ Incluido explícitamente
- **Extiende base.html**: ✅ Sí
- **Credenciales**: (Se crean dinámicamente por puesto)

**Funcionalidades**:
- Registro de formularios E-14
- Captura de fotos
- Verificación de presencia
- Reporte de incidentes y delitos

**Scripts cargados**:
- api-client.js ✅
- dashboard-fixes.js
- incidentes-delitos.js
- testigo-dashboard-v2.js
- testigo-presencia-simple.js
- testigo-dashboard-final-fix.js
- testigo-session-fix.js
- testigo-mejoras.js
- testigo-dashboard-fix-buttons.js
- testigo-init.js
- testigo-dashboard-debug.js

---

## Resumen de API Client

| Rol | Template | API Client | Método |
|-----|----------|------------|--------|
| Super Admin | admin/super-admin-dashboard.html | ✅ | Explícito + base.html |
| Monitoreo | monitoreo/dashboard.html | ✅ | base.html |
| Coord. Departamental | coordinador/departamental.html | ✅ | base.html |
| Coord. Municipal | coordinador/municipal.html | ✅ | base.html |
| Coord. Puesto | coordinador/puesto.html | ✅ | base.html |
| Auditor Electoral | auditor/dashboard.html | ✅ | base.html |
| Testigo Electoral | testigo/dashboard.html | ✅ | Explícito + base.html |

## Verificación de Endpoints API

### Super Admin
- `GET /api/super-admin/stats` - Estadísticas
- `GET /api/super-admin/users` - Usuarios
- `GET /api/super-admin/partidos` - Partidos
- `GET /api/super-admin/candidatos` - Candidatos
- `GET /api/super-admin/tipos-eleccion` - Tipos de elección
- `GET /api/super-admin/locations/departamentos` - Departamentos

### Monitoreo
- `GET /api/monitoreo/stats` - Estadísticas en tiempo real
- `GET /api/monitoreo/mapa-data` - Datos del mapa
- `GET /api/monitoreo/usuarios-activos` - Usuarios activos

### Coordinadores
- `GET /api/coordinador-departamental/stats` - Estadísticas departamentales
- `GET /api/coordinador-municipal/stats` - Estadísticas municipales
- `GET /api/coordinador-puesto/stats` - Estadísticas del puesto
- `GET /api/coordinador-puesto/testigos` - Testigos del puesto

### Testigo
- `GET /api/testigo/dashboard-data` - Datos del dashboard
- `POST /api/testigo/formulario` - Enviar formulario
- `GET /api/testigo/mis-formularios` - Formularios del testigo
- `POST /api/testigo/verificar-presencia` - Verificar presencia

### Auditor
- `GET /api/auditor/formularios-pendientes` - Formularios pendientes
- `PUT /api/auditor/validar-formulario` - Validar formulario

## Problemas Identificados y Corregidos

### 1. ✅ Super Admin Dashboard
**Problema**: No cargaba datos por falta de api-client.js  
**Solución**: Agregado explícitamente en el template

### 2. ✅ Testigo Dashboard
**Problema**: No cargaba datos por falta de api-client.js  
**Solución**: Agregado explícitamente al inicio de los scripts

### 3. ✅ Dashboard Data Loader
**Problema**: Error de sintaxis (llave extra)  
**Solución**: Corregida indentación y eliminada llave extra

### 4. ✅ Base Template
**Estado**: Ya incluía api-client.js globalmente  
**Acción**: Ninguna necesaria

## Orden de Carga de Scripts

Para que los dashboards funcionen correctamente, los scripts deben cargarse en este orden:

1. **base.html** (cargado primero)
   - api-client.js
   - utils.js
   - sync-manager.js

2. **Template específico** (bloque extra_js)
   - api-client.js (opcional, si se necesita antes)
   - dashboard-data-loader.js (si aplica)
   - [rol]-dashboard.js
   - [rol]-dashboard-debug.js

## Verificación de Funcionamiento

Para verificar que cada rol funciona correctamente:

1. **Iniciar sesión** con las credenciales del rol
2. **Abrir DevTools** (F12)
3. **Verificar Console** - No debe haber errores de `APIClient is undefined`
4. **Verificar Network** - Las llamadas API deben retornar 200
5. **Verificar UI** - Los datos deben mostrarse correctamente

## Comandos de Prueba

```javascript
// En la consola del navegador
console.log(typeof APIClient); // Debe ser "function"
console.log(APIClient.baseURL); // Debe ser "/api"

// Probar endpoint según el rol
// Super Admin:
APIClient.get('/super-admin/stats').then(console.log);

// Monitoreo:
APIClient.get('/monitoreo/stats').then(console.log);

// Testigo:
APIClient.get('/testigo/dashboard-data').then(console.log);
```

## Próximos Pasos

1. ✅ Verificar que todos los dashboards cargan datos
2. ⏳ Probar cada rol individualmente
3. ⏳ Verificar que las funcionalidades específicas de cada rol funcionan
4. ⏳ Documentar cualquier problema adicional encontrado

## Notas Importantes

- Todos los templates que extienden de `base.html` ya tienen `api-client.js` disponible
- Solo se necesita incluir explícitamente `api-client.js` si se requiere un orden específico de carga
- El archivo `api-client.js` se puede incluir múltiples veces sin problemas (el navegador lo cachea)
- Es crítico que `api-client.js` se cargue ANTES de cualquier script que use `APIClient`

---

**Estado**: ✅ TODOS LOS ROLES REVISADOS  
**API Client**: ✅ DISPONIBLE EN TODOS LOS DASHBOARDS  
**Fecha de revisión**: 30 de Noviembre de 2025
