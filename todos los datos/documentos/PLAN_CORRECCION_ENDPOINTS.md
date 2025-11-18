# Plan de Corrección de Endpoints

**Fecha**: 2025-11-15  
**Estado**: Auditoría Completa Realizada

## Resumen Ejecutivo

📊 **Estado Actual**:
- ✅ Endpoints funcionando: **7/39** (17.9%)
- ❌ Endpoints faltantes: **32/39** (82.1%)
- 🔴 Blueprints faltantes: **5**
- ✅ Blueprints funcionando: **3** (super_admin, coordinador_municipal, testigo)

## Priorización de Correcciones

### 🔴 PRIORIDAD CRÍTICA - Blueprints Faltantes (5)

Estos blueprints deben crearse primero ya que sin ellos no se pueden implementar los endpoints:

1. **`backend/routes/coordinador_puesto.py`** - URGENTE
   - Rol más usado en operación diaria
   - 5 endpoints críticos para operación
   
2. **`backend/routes/admin.py`** - ALTA
   - Admin departamental necesita gestionar su departamento
   - 4 endpoints administrativos
   
3. **`backend/routes/coordinador_departamental.py`** - ALTA
   - Coordinación a nivel departamental
   - 3 endpoints de supervisión
   
4. **`backend/routes/admin_municipal.py`** - MEDIA
   - Gestión municipal
   - 4 endpoints administrativos
   
5. **`backend/routes/auditor.py`** - MEDIA
   - Auditoría y control
   - 4 endpoints de auditoría

### 🟠 PRIORIDAD ALTA - Endpoints Críticos (12)

Endpoints que bloquean funcionalidad básica:

#### Coordinador Puesto (5 endpoints)
- [ ] `GET /api/coordinador-puesto/stats` - Dashboard principal
- [ ] `GET /api/coordinador-puesto/mesas` - Ver mesas asignadas
- [ ] `GET /api/coordinador-puesto/testigos` - Gestionar testigos
- [ ] `GET /api/coordinador-puesto/incidentes` - Ver incidentes
- [ ] `GET /api/coordinador-puesto/formularios` - Ver formularios

#### Admin Departamental (4 endpoints)
- [ ] `GET /api/admin/stats` - Dashboard principal
- [ ] `GET /api/admin/usuarios` - Gestionar usuarios
- [ ] `GET /api/admin/ubicaciones` - Ver ubicaciones
- [ ] `GET /api/admin/formularios` - Ver formularios

#### Coordinador Departamental (3 endpoints)
- [ ] `GET /api/coordinador-departamental/stats` - Dashboard principal
- [ ] `GET /api/coordinador-departamental/municipios` - Ver municipios
- [ ] `GET /api/coordinador-departamental/resumen` - Resumen general

### 🟡 PRIORIDAD MEDIA - Endpoints Complementarios (14)

#### Admin Municipal (4 endpoints)
- [ ] `GET /api/admin-municipal/stats`
- [ ] `GET /api/admin-municipal/zonas`
- [ ] `GET /api/admin-municipal/puestos`
- [ ] `GET /api/admin-municipal/mesas`

#### Coordinador Municipal (4 endpoints)
- [ ] `GET /api/coordinador-municipal/stats`
- [ ] `GET /api/coordinador-municipal/zonas`
- [ ] `GET /api/coordinador-municipal/mesas`
- [ ] `GET /api/coordinador-municipal/formularios`

#### Auditor Electoral (4 endpoints)
- [ ] `GET /api/auditor/stats`
- [ ] `GET /api/auditor/inconsistencias`
- [ ] `GET /api/auditor/reportes`
- [ ] `GET /api/auditor/formularios`

#### Testigo Electoral (2 endpoints)
- [ ] `GET /api/testigo/formularios`
- [ ] `POST /api/testigo/formularios`

### 🟢 PRIORIDAD BAJA - Endpoints Administrativos (6)

#### Super Admin (6 endpoints)
- [ ] `GET /api/super-admin/usuarios`
- [ ] `GET /api/super-admin/ubicaciones`
- [ ] `GET /api/super-admin/partidos`
- [ ] `POST /api/super-admin/usuarios`
- [ ] `PUT /api/super-admin/usuarios/<id>`
- [ ] `DELETE /api/super-admin/usuarios/<id>`

## Plan de Implementación

### Fase 1: Blueprints Críticos (2-3 horas)

**Objetivo**: Crear estructura básica de blueprints faltantes

1. Crear `backend/routes/coordinador_puesto.py`
   - Estructura básica con decoradores
   - Endpoints stub que retornen datos mock
   
2. Crear `backend/routes/admin.py`
   - Estructura básica
   - Endpoints stub
   
3. Crear `backend/routes/coordinador_departamental.py`
   - Estructura básica
   - Endpoints stub

4. Registrar blueprints en `backend/app.py`

5. Probar que todos los endpoints retornen 200 (aunque sea con datos mock)

### Fase 2: Implementar Endpoints Stats (2-3 horas)

**Objetivo**: Todos los dashboards muestran estadísticas básicas

Implementar endpoint `/stats` para cada rol:
- Coordinador Puesto
- Admin Departamental
- Coordinador Departamental
- Admin Municipal
- Coordinador Municipal
- Auditor Electoral

**Estructura básica de stats**:
```python
{
  "total_mesas": 0,
  "total_formularios": 0,
  "formularios_completados": 0,
  "formularios_pendientes": 0,
  "porcentaje_avance": 0,
  "ultima_actualizacion": "2025-11-15T17:00:00"
}
```

### Fase 3: Implementar Endpoints de Listado (3-4 horas)

**Objetivo**: Mostrar listas de entidades relacionadas

Para cada rol, implementar endpoints que listen:
- Mesas
- Testigos
- Formularios
- Ubicaciones (zonas, puestos, municipios)

### Fase 4: Implementar Endpoints de Gestión (2-3 horas)

**Objetivo**: Permitir operaciones CRUD básicas

- Testigo: Crear/editar formularios
- Super Admin: CRUD de usuarios
- Coordinador Puesto: Gestionar incidentes

### Fase 5: Pruebas y Ajustes (2 horas)

**Objetivo**: Verificar funcionamiento completo

1. Ejecutar `revision_completa_roles.py`
2. Verificar que todos los endpoints retornen 200
3. Probar flujos completos por rol
4. Ajustar permisos y validaciones

## Estimación Total

- **Tiempo estimado**: 11-15 horas
- **Complejidad**: Media
- **Riesgo**: Bajo (estructura ya definida)

## Plantilla de Blueprint

```python
"""
Rutas para [ROL]
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.location import Location
from backend.database import db

[rol]_bp = Blueprint('[rol]', __name__)


@[rol]_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Estadísticas del [rol]"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or user.rol != '[rol]':
            return jsonify({
                'success': False,
                'error': 'No autorizado'
            }), 403
        
        # TODO: Implementar lógica de stats
        stats = {
            'total_mesas': 0,
            'total_formularios': 0,
            'formularios_completados': 0,
            'porcentaje_avance': 0
        }
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

## Checklist de Implementación

### Blueprints
- [ ] coordinador_puesto.py
- [ ] admin.py
- [ ] coordinador_departamental.py
- [ ] admin_municipal.py
- [ ] auditor.py

### Registro en app.py
- [ ] Importar blueprints
- [ ] Registrar con prefijos correctos
- [ ] Verificar orden de registro

### Endpoints por Prioridad
- [ ] Todos los `/stats` (6 endpoints)
- [ ] Coordinador Puesto completo (5 endpoints)
- [ ] Admin Departamental completo (4 endpoints)
- [ ] Coordinador Departamental completo (3 endpoints)
- [ ] Admin Municipal completo (4 endpoints)
- [ ] Coordinador Municipal faltantes (4 endpoints)
- [ ] Auditor Electoral completo (4 endpoints)
- [ ] Testigo Electoral faltantes (2 endpoints)
- [ ] Super Admin faltantes (6 endpoints)

### Pruebas
- [ ] Ejecutar `revision_completa_roles.py`
- [ ] Verificar 100% de endpoints funcionando
- [ ] Probar login + operación básica por rol
- [ ] Documentar endpoints en README

## Notas Importantes

1. **Usar testigo.py como referencia**: Es el único blueprint 100% funcional
2. **Mantener consistencia**: Todos los endpoints deben seguir el mismo patrón
3. **Validar permisos**: Cada endpoint debe verificar el rol del usuario
4. **Manejo de errores**: Try-catch en todos los endpoints
5. **Respuestas consistentes**: Siempre retornar `{success: bool, data/error: any}`

## Archivos de Referencia

- ✅ `backend/routes/testigo.py` - Blueprint completo y funcional
- ✅ `backend/routes/super_admin.py` - Endpoints complejos
- ✅ `backend/routes/coordinador_municipal.py` - Endpoints parciales
- ✅ `LISTA_CORRECCIONES_ENDPOINTS.md` - Lista detallada
- ✅ `auditoria_endpoints.json` - Datos completos de auditoría
