# ✅ Usuarios de Testing Configurados

## Resumen
Los usuarios de testing están completamente configurados y funcionando con el sistema de autenticación estándar basado en rol y ubicación jerárquica.

## Cambios Implementados

### 1. Eliminación del Endpoint de Testing
- ❌ Eliminado `/api/auth/login-testing`
- ✅ Los usuarios de testing usan `/api/auth/login` (endpoint estándar)
- **Razón:** Los usuarios de testing deben seguir el mismo flujo que los usuarios reales

### 2. Corrección de Búsqueda de Ubicación para Testigos
- **Archivo:** `backend/services/auth_service.py`
- **Cambio:** Los testigos ahora buscan ubicaciones de tipo `mesa` en lugar de `puesto`
- **Impacto:** Los testigos electorales pueden autenticarse correctamente

### 3. Eliminación de Archivos Innecesarios
- ❌ Eliminado `frontend/templates/auth/login-testing.html`

## Usuarios de Testing Disponibles

### 🔑 Super Admin
```json
{
  "rol": "super_admin",
  "password": "test123"
}
```
- **Permisos:** Acceso completo al sistema
- **Ubicación:** No requiere

### 🔍 Auditor Electoral
```json
{
  "rol": "auditor_electoral",
  "departamento_codigo": "TEST01",
  "password": "test123"
}
```
- **Permisos:** Auditoría a nivel departamental
- **Ubicación:** Departamento Test (TEST01)

### 👤 Coordinador Departamental
```json
{
  "rol": "coordinador_departamental",
  "departamento_codigo": "TEST01",
  "password": "test123"
}
```
- **Permisos:** Gestión a nivel departamental
- **Ubicación:** Departamento Test (TEST01)

### 👤 Coordinador Municipal
```json
{
  "rol": "coordinador_municipal",
  "departamento_codigo": "TEST01",
  "municipio_codigo": "TEST0101",
  "password": "test123"
}
```
- **Permisos:** Gestión a nivel municipal
- **Ubicación:** Municipio Test (TEST0101)

### 👤 Coordinador de Puesto
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
- **Permisos:** Gestión a nivel de puesto
- **Ubicación:** Puesto Test 1 (TEST0101001)

### 📝 Testigo Electoral
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
- **Permisos:** Registro de formularios y reportes
- **Ubicación:** Mesa 1 - Puesto Test 1 (TEST01010010001)

## Pruebas Realizadas

### ✅ Super Admin
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"rol":"super_admin","password":"test123"}'
```
**Resultado:** ✅ Login exitoso, tokens generados

### ✅ Testigo Electoral
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "rol":"testigo_electoral",
    "departamento_codigo":"TEST01",
    "municipio_codigo":"TEST0101",
    "zona_codigo":"TEST01Z1",
    "puesto_codigo":"TEST0101001",
    "password":"test123"
  }'
```
**Resultado:** ✅ Login exitoso, tokens generados

### ✅ Coordinador de Puesto
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "rol":"coordinador_puesto",
    "departamento_codigo":"TEST01",
    "municipio_codigo":"TEST0101",
    "zona_codigo":"TEST01Z1",
    "puesto_codigo":"TEST0101001",
    "password":"test123"
  }'
```
**Resultado:** ✅ Login exitoso, tokens generados

## Estructura de Ubicaciones de Testing

```
Departamento Test (TEST01)
└── Municipio Test (TEST0101)
    └── Zona TEST01Z1
        └── Puesto Test 1 (TEST0101001)
            └── Mesa 1 (TEST01010010001)
                - 300 votantes registrados
```

## Cómo Cargar los Datos de Testing

```bash
python load_basic_data.py
```

Este script:
1. Limpia la base de datos
2. Crea la estructura de ubicaciones
3. Crea los 6 usuarios de testing
4. Crea una campaña de prueba
5. Crea tipos de elección (Presidente, Senado)
6. Crea partidos políticos (PL, PC, PV)

## Próximos Pasos

1. ✅ Usuarios de testing configurados
2. ⏳ Probar login desde el frontend
3. ⏳ Verificar acceso a dashboards según rol
4. ⏳ Probar sistema de auditoría
5. ⏳ Probar registro de formularios
6. ⏳ Probar reportes de incidentes

## Notas Importantes

- Todos los usuarios de testing usan la contraseña: `test123`
- Los usuarios siguen el mismo flujo de autenticación que los usuarios reales
- La autenticación es basada en rol + ubicación jerárquica
- Los tokens JWT incluyen: rol, ubicacion_id, nombre
- Los testigos buscan ubicaciones de tipo `mesa`
- Los coordinadores de puesto buscan ubicaciones de tipo `puesto`
