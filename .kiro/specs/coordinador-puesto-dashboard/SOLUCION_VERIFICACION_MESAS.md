# Solución: Verificación de Presencia y Sincronización de Mesas

## Análisis Completado

### Estado Actual

**✅ Modelo User - CORRECTO**
- Los campos `presencia_verificada` y `presencia_verificada_at` ya existen
- El método `verificar_presencia()` ya está implementado
- Ubicación: `backend/models/user.py` líneas 24-25

**✅ Endpoint de Verificación - EXISTE**
- El endpoint `/api/auth/verificar-presencia` ya está implementado
- Ubicación: `backend/routes/auth.py` línea 185

**✅ Frontend - CORRECTO**
- El código JavaScript ya muestra el ícono de presencia
- Ubicación: `frontend/static/js/coordinador-puesto.js` línea ~700

**✅ Backend Endpoint Mesas - CORRECTO**
- El endpoint `/api/formularios/mesas` ya envía los datos de presencia
- Ubicación: `backend/routes/formularios_e14.py` línea ~280

**✅ Modelo Location - CORRECTO**
- Las mesas se relacionan con puestos mediante `puesto_codigo`
- El query usa el filtro correcto

## Problemas Identificados

### 1. Verificación de Presencia No Se Muestra

**Causa Real:**
El problema NO es de código, sino de **datos o flujo**:

1. **Los testigos no están verificando su presencia**: El botón existe en el dashboard del testigo pero puede que no lo estén usando
2. **Los datos no se están guardando**: El endpoint puede tener un error al guardar
3. **La sesión no se está actualizando**: Después de verificar presencia, el perfil no se recarga

**Solución:**
1. Verificar que el endpoint `/api/auth/verificar-presencia` esté guardando correctamente en la BD
2. Agregar logs para debug
3. Verificar que el testigo pueda ver el botón de verificación
4. Asegurar que después de verificar, el estado se actualice en el dashboard del coordinador

### 2. Cantidad de Mesas No Coincide

**Causas Posibles:**

1. **Las mesas no están creadas en la BD**: Si las mesas no existen en la tabla `locations`, no se mostrarán
2. **El `puesto_codigo` no coincide**: Las mesas pueden tener un código de puesto diferente al del coordinador
3. **Las mesas están inactivas**: El query no filtra por `activo=True`
4. **Problema de datos**: Los códigos pueden estar mal escritos (espacios, mayúsculas, etc.)

**Solución:**
1. Agregar filtro `activo=True` al query de mesas
2. Agregar logs para ver qué mesas se están obteniendo
3. Crear script de verificación de datos
4. Normalizar códigos (trim, lowercase) antes de comparar

## Implementación de Soluciones

### Solución 1: Mejorar Endpoint de Verificación de Presencia

**Archivo:** `backend/routes/auth.py`

Agregar logs y verificación:

```python
@auth_bp.route('/verificar-presencia', methods=['POST'])
@jwt_required()
def verificar_presencia():
    """Verificar presencia del testigo en la mesa"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Verificar que sea testigo
        if user.rol != 'testigo':
            return jsonify({
                'success': False,
                'error': 'Solo los testigos pueden verificar presencia'
            }), 403
        
        # Marcar presencia
        user.verificar_presencia()
        db.session.commit()
        
        # Log para debug
        print(f"Presencia verificada para testigo {user.id} - {user.nombre}")
        
        return jsonify({
            'success': True,
            'message': 'Presencia verificada exitosamente',
            'data': {
                'presencia_verificada': user.presencia_verificada,
                'presencia_verificada_at': user.presencia_verificada_at.isoformat() if user.presencia_verificada_at else None
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error verificando presencia: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### Solución 2: Mejorar Query de Mesas

**Archivo:** `backend/routes/formularios_e14.py`

Agregar filtro de activo y logs:

```python
@formularios_bp.route('/mesas', methods=['GET'])
@jwt_required()
@role_required(['coordinador_puesto'])
def obtener_mesas_puesto():
    """Obtener lista de mesas del puesto con estado de reporte"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user or not user.ubicacion_id:
            return jsonify({
                'success': False,
                'error': 'Usuario sin ubicación asignada'
            }), 400
        
        ubicacion = Location.query.get(user.ubicacion_id)
        
        if not ubicacion or ubicacion.tipo != 'puesto':
            return jsonify({
                'success': False,
                'error': 'Coordinador no asignado a un puesto válido'
            }), 400
        
        # Log para debug
        print(f"Buscando mesas para puesto: {ubicacion.puesto_codigo}")
        
        # Obtener todas las mesas del puesto (ACTIVAS)
        mesas = Location.query.filter_by(
            puesto_codigo=ubicacion.puesto_codigo,
            tipo='mesa',
            activo=True  # <-- AGREGAR ESTE FILTRO
        ).all()
        
        print(f"Mesas encontradas: {len(mesas)}")
        
        # ... resto del código ...
```

### Solución 3: Script de Verificación de Datos

**Archivo:** `backend/scripts/verificar_mesas.py` (NUEVO)

```python
"""
Script para verificar integridad de datos de mesas
"""
from backend.database import db
from backend.models.location import Location
from backend.models.user import User

def verificar_mesas_puesto(puesto_codigo):
    """Verificar mesas de un puesto"""
    
    # Buscar puesto
    puesto = Location.query.filter_by(
        puesto_codigo=puesto_codigo,
        tipo='puesto'
    ).first()
    
    if not puesto:
        print(f"❌ Puesto {puesto_codigo} no encontrado")
        return
    
    print(f"✅ Puesto encontrado: {puesto.nombre_completo}")
    print(f"   ID: {puesto.id}")
    print(f"   Código: {puesto.puesto_codigo}")
    
    # Buscar mesas
    mesas = Location.query.filter_by(
        puesto_codigo=puesto_codigo,
        tipo='mesa'
    ).all()
    
    print(f"\n📊 Total de mesas: {len(mesas)}")
    
    for mesa in mesas:
        print(f"\n  Mesa {mesa.mesa_codigo}:")
        print(f"    - ID: {mesa.id}")
        print(f"    - Nombre: {mesa.nombre_completo}")
        print(f"    - Activa: {mesa.activo}")
        print(f"    - Votantes: {mesa.total_votantes_registrados}")
        
        # Buscar testigo asignado
        testigo = User.query.filter_by(
            ubicacion_id=mesa.id,
            rol='testigo'
        ).first()
        
        if testigo:
            print(f"    - Testigo: {testigo.nombre}")
            print(f"    - Presencia: {'✅ Verificada' if testigo.presencia_verificada else '❌ No verificada'}")
            if testigo.presencia_verificada_at:
                print(f"    - Verificada en: {testigo.presencia_verificada_at}")
        else:
            print(f"    - ⚠️  Sin testigo asignado")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: python verificar_mesas.py <puesto_codigo>")
        sys.exit(1)
    
    puesto_codigo = sys.argv[1]
    verificar_mesas_puesto(puesto_codigo)
```

### Solución 4: Actualizar Frontend para Recargar Después de Verificar

**Archivo:** `frontend/static/js/testigo-dashboard-new.js`

```javascript
async function verificarPresencia() {
    if (!confirm('¿Confirma que está presente en la mesa asignada?')) {
        return;
    }
    
    try {
        const response = await APIClient.post('/auth/verificar-presencia', {});
        
        if (response.success) {
            Utils.showSuccess('Presencia verificada exitosamente');
            
            // Ocultar botón y mostrar alerta de verificación
            document.getElementById('btnVerificarPresencia').classList.add('d-none');
            document.getElementById('alertaPresenciaVerificada').classList.remove('d-none');
            
            // Mostrar fecha de verificación
            const fecha = new Date(response.data.presencia_verificada_at);
            document.getElementById('presenciaFecha').textContent = 
                `Verificado el ${fecha.toLocaleDateString()} a las ${fecha.toLocaleTimeString()}`;
            
            // AGREGAR: Recargar perfil para actualizar el estado
            await loadUserProfile();
        }
    } catch (error) {
        console.error('Error verificando presencia:', error);
        Utils.showError('Error al verificar presencia: ' + error.message);
    }
}
```

## Plan de Implementación

### Fase 1: Verificación y Debug (Inmediato)

1. ✅ Revisar modelos - COMPLETADO
2. ✅ Revisar endpoints - COMPLETADO
3. ⏳ Agregar logs en endpoints
4. ⏳ Crear script de verificación
5. ⏳ Ejecutar script con datos reales

### Fase 2: Correcciones (Si se encuentran problemas)

1. Agregar filtro `activo=True` en query de mesas
2. Normalizar códigos antes de comparar
3. Corregir datos inconsistentes en BD
4. Agregar manejo de errores mejorado

### Fase 3: Mejoras de UX

1. Agregar tooltip con fecha de verificación
2. Agregar contador de testigos presentes
3. Agregar auto-refresh más frecuente para presencia
4. Agregar notificación cuando testigo verifica presencia

## Comandos para Testing

### 1. Verificar datos de un puesto

```bash
python backend/scripts/verificar_mesas.py PUESTO001
```

### 2. Verificar presencia de un testigo (desde consola Python)

```python
from backend.database import db
from backend.models.user import User

# Buscar testigo
testigo = User.query.filter_by(rol='testigo').first()
print(f"Testigo: {testigo.nombre}")
print(f"Presencia: {testigo.presencia_verificada}")

# Verificar presencia manualmente
testigo.verificar_presencia()
db.session.commit()
print("Presencia verificada!")
```

### 3. Ver mesas de un puesto (desde consola Python)

```python
from backend.models.location import Location

puesto_codigo = "PUESTO001"
mesas = Location.query.filter_by(
    puesto_codigo=puesto_codigo,
    tipo='mesa',
    activo=True
).all()

print(f"Mesas encontradas: {len(mesas)}")
for mesa in mesas:
    print(f"  - {mesa.mesa_codigo}: {mesa.nombre_completo}")
```

## Próximos Pasos

1. **Ejecutar script de verificación** con datos reales del puesto
2. **Revisar logs** del endpoint de mesas para ver qué se está retornando
3. **Probar flujo completo**:
   - Testigo verifica presencia
   - Coordinador recarga dashboard
   - Verificar que aparece el ícono
4. **Corregir datos** si es necesario
5. **Actualizar tareas** en `tasks.md` con los hallazgos

## Archivos a Modificar

1. `backend/routes/auth.py` - Agregar logs
2. `backend/routes/formularios_e14.py` - Agregar filtro activo y logs
3. `backend/scripts/verificar_mesas.py` - CREAR NUEVO
4. `frontend/static/js/testigo-dashboard-new.js` - Recargar perfil después de verificar
5. `.kiro/specs/coordinador-puesto-dashboard/tasks.md` - Actualizar con nuevas tareas
