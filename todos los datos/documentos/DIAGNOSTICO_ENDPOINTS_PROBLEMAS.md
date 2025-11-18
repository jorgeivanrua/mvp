# Diagnóstico de Endpoints - Problemas Encontrados

## Fecha: 2025-11-15

## Resumen Ejecutivo

✅ **Sistema jerárquico de login funcionando**: 5 de 8 roles pueden autenticarse correctamente
❌ **Todos los endpoints retornan 404**: Ningún endpoint de roles está implementado
⚠️ **3 roles con timeout en login**: super_admin, admin_departamental, admin_municipal

## Resultados del Diagnóstico

### Logins Exitosos (5/8)
1. ✅ **coordinador_departamental** - Login OK
2. ✅ **coordinador_municipal** - Login OK  
3. ✅ **coordinador_puesto** - Login OK
4. ✅ **testigo_electoral** - Login OK
5. ✅ **auditor_electoral** - Login OK

### Logins con Problemas (3/8)
1. ❌ **super_admin** - Timeout (10s)
2. ❌ **admin_departamental** - Timeout (10s)
3. ❌ **admin_municipal** - Timeout (10s)

### Endpoints Probados (0/9 funcionando)
Todos los endpoints retornan **404 Not Found**:

#### Coordinador Departamental
- GET /api/coordinador-departamental/stats → 404

#### Coordinador Municipal  
- GET /api/coordinador-municipal/stats → 404
- GET /api/coordinador-municipal/puestos → 500 (error interno)

#### Coordinador Puesto
- GET /api/coordinador-puesto/stats → 404
- GET /api/coordinador-puesto/mesas → 404
- GET /api/coordinador-puesto/incidentes → 404

#### Testigo Electoral
- GET /api/testigo/info → 404
- GET /api/testigo/mesa → 404

#### Auditor Electoral
- GET /api/auditor/stats → 404

## Análisis de Problemas

### 1. Timeouts en Login (super_admin, admin_departamental, admin_municipal)

**Causa probable**: La función `_find_location_by_hierarchy` en `auth_service.py` está haciendo queries lentas o entrando en bucle infinito para estos roles.

**Código problemático**:
```python
# Para admin_departamental
if rol in ['admin_departamental', 'coordinador_departamental', 'auditor_electoral']:
    query = query.filter_by(tipo='departamento')
```

**Solución**:
- Agregar logs de debug
- Optimizar queries con índices
- Agregar timeout a nivel de query
- Verificar que existan ubicaciones tipo 'departamento' en la BD

### 2. Endpoints 404 Not Found

**Causa**: Los blueprints de rutas no están registrados o las rutas no existen.

**Archivos a revisar**:
- `backend/routes/__init__.py` - Registro de blueprints
- `backend/routes/coordinador_departamental.py` - ¿Existe?
- `backend/routes/coordinador_municipal.py` - ¿Existe?
- `backend/routes/coordinador_puesto.py` - ¿Existe?
- `backend/routes/testigo.py` - ¿Existe?
- `backend/routes/auditor.py` - ¿Existe?

**Solución**:
- Crear los blueprints faltantes
- Implementar los endpoints básicos (stats, info, etc.)
- Registrar blueprints en `app.py`

### 3. Error 500 en /api/coordinador-municipal/puestos

**Causa**: Endpoint existe pero tiene error interno (probablemente excepción no manejada).

**Solución**:
- Revisar logs del servidor
- Agregar manejo de errores
- Verificar que la query de puestos funcione correctamente

## Acciones Correctivas Prioritarias

### Prioridad 1: Corregir Timeouts en Login
1. Agregar logs en `_find_location_by_hierarchy`
2. Verificar datos de ubicaciones en BD
3. Optimizar queries con `.first()` temprano
4. Agregar timeout a queries

### Prioridad 2: Implementar Endpoints Faltantes
1. Crear blueprints para cada rol
2. Implementar endpoints básicos (stats, info)
3. Registrar blueprints en app.py
4. Probar cada endpoint

### Prioridad 3: Corregir Error 500
1. Revisar endpoint `/api/coordinador-municipal/puestos`
2. Agregar manejo de errores
3. Validar datos de entrada

## Sistema Jerárquico de Login - Funcionando ✅

El sistema de login basado en ubicación jerárquica **SÍ está funcionando** para la mayoría de roles:

```python
# Ejemplo de login exitoso
{
    "rol": "coordinador_municipal",
    "departamento_codigo": "44",
    "municipio_codigo": "01",
    "password": "test123"
}
```

**Ubicaciones jerárquicas por rol**:
- super_admin: Sin ubicación
- admin_departamental: departamento_codigo
- admin_municipal: departamento_codigo + municipio_codigo
- coordinador_departamental: departamento_codigo
- coordinador_municipal: departamento_codigo + municipio_codigo
- coordinador_puesto: departamento_codigo + municipio_codigo + zona_codigo + puesto_codigo
- testigo_electoral: departamento_codigo + municipio_codigo + zona_codigo + puesto_codigo
- auditor_electoral: departamento_codigo

## Próximos Pasos

1. ✅ Corregir timeouts en login (super_admin, admin_departamental, admin_municipal)
2. ⬜ Implementar todos los endpoints faltantes
3. ⬜ Actualizar frontend para usar sistema jerárquico
4. ⬜ Crear documentación de API completa
5. ⬜ Pruebas end-to-end de todos los roles
