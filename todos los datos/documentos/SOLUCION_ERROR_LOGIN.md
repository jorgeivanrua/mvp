# 🔧 Solución al Error de Login

## Problema Identificado

El error ocurría porque:
1. El modelo `Location` cambió su estructura (de `codigo`, `nombre` a `departamento_codigo`, `municipio_codigo`, etc.)
2. Los scripts de carga de datos usaban la estructura antigua
3. El endpoint `/auth/profile` intentaba acceder a atributos que no existían

## Cambios Realizados

### 1. Corregido `backend/routes/auth.py`
- Simplificado el endpoint `/auth/profile` para usar `location.to_dict()`
- Esto evita errores al acceder a atributos que pueden no existir

### 2. Actualizado `backend/scripts/load_test_data.py`
- Corregida la creación de ubicaciones para usar la nueva estructura
- Corregidos los roles de usuarios ('auditor' → 'auditor_electoral', 'testigo' → 'testigo_electoral')
- Agregados coordinadores para todos los puestos

### 3. Actualizado `backend/scripts/load_complete_test_data.py`
- Corregida la creación de ubicaciones para usar la nueva estructura
- Mejorado el manejo de errores

### 4. Creado `reset_and_load_data.py`
- Script simple para limpiar y recargar la base de datos

## Solución Rápida

### Opción 1: Script Automático (Recomendado)

```bash
python reset_and_load_data.py
```

Este script:
1. Limpia la base de datos
2. Recrea las tablas
3. Carga datos de prueba completos
4. Muestra las credenciales de acceso

### Opción 2: Manual

```bash
# 1. Limpiar base de datos
python -c "from backend.app import create_app; from backend.database import db; app = create_app(); ctx = app.app_context(); ctx.push(); db.drop_all(); db.create_all(); print('✅ Base de datos limpia')"

# 2. Cargar datos de prueba
python backend/scripts/load_complete_test_data.py
```

## Verificación

Después de ejecutar el script, deberías poder:

1. **Iniciar sesión con cualquier rol:**
   - Super Admin: `admin_test / test123`
   - Auditor: `auditor_test / test123`
   - Coordinador Departamental: `coord_dept_test / test123`
   - Coordinador Municipal: `coord_mun_test / test123`
   - Coordinador Puesto: `coord_puesto_test / test123`
   - Testigo: `testigo_test_1 / test123`

2. **Acceder al dashboard sin errores**

3. **Ver los datos correctamente cargados**

## Estructura de Datos Cargados

### Ubicaciones
```
Departamento Test (TEST01)
└── Municipio Test (TEST0101)
    ├── Puesto de Votación 1 (TEST0101001)
    │   ├── Mesa 1 (TEST01010010001)
    │   ├── Mesa 2 (TEST01010010002)
    │   ├── Mesa 3 (TEST01010010003)
    │   ├── Mesa 4 (TEST01010010004)
    │   └── Mesa 5 (TEST01010010005)
    ├── Puesto de Votación 2 (TEST0101002)
    │   └── ... (5 mesas)
    └── Puesto de Votación 3 (TEST0101003)
        └── ... (5 mesas)
```

### Usuarios
- 1 Super Admin
- 1 Auditor Electoral
- 1 Coordinador Departamental
- 1 Coordinador Municipal
- 3 Coordinadores de Puesto (uno por puesto)
- 15 Testigos Electorales (uno por mesa)

**Total: 22 usuarios**

### Datos Electorales
- 1 Campaña activa
- 4 Tipos de elección
- 6 Partidos políticos
- 54 Candidatos
- 10 Formularios E-14 (con datos realistas)
- 5 Incidentes electorales
- 3 Delitos electorales
- 20 Logs de auditoría
- 10 Notificaciones

## Problemas Comunes

### Error: "No module named 'backend'"

**Solución:**
```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd /ruta/al/proyecto
python reset_and_load_data.py
```

### Error: "Could not connect to database"

**Solución:**
1. Verifica que PostgreSQL esté corriendo
2. Verifica las credenciales en `.env`
3. Verifica que la base de datos exista

### Error: "Token inválido" después de recargar datos

**Solución:**
1. Cierra sesión en el navegador
2. Limpia localStorage:
   - Abre DevTools (F12)
   - Consola: `localStorage.clear()`
   - Recarga la página
3. Inicia sesión nuevamente

## Próximos Pasos

Una vez que el login funcione correctamente:

1. **Ejecutar auditoría completa:**
   ```bash
   python backend/tests/test_audit_system.py
   ```

2. **Probar cada rol manualmente:**
   - Verifica que cada dashboard cargue correctamente
   - Prueba las funcionalidades principales
   - Reporta cualquier error encontrado

3. **Revisar logs del servidor:**
   - Busca errores o advertencias
   - Verifica que las consultas SQL sean correctas

## Notas Técnicas

### Cambios en el Modelo Location

**Antes:**
```python
Location(
    codigo='TEST01',
    nombre='Departamento Test',
    tipo='departamento'
)
```

**Ahora:**
```python
Location(
    departamento_codigo='TEST01',
    departamento_nombre='Departamento Test',
    nombre_completo='Departamento Test',
    tipo='departamento'
)
```

### Cambios en Roles de Usuario

**Antes:**
- `auditor` → **Ahora:** `auditor_electoral`
- `testigo` → **Ahora:** `testigo_electoral`

Estos cambios aseguran consistencia con el modelo `User` que define los roles válidos.

## Contacto

Si el problema persiste después de seguir estos pasos:
1. Revisa los logs del servidor
2. Verifica la consola del navegador (F12)
3. Comparte el error específico para más ayuda

---

**Estado:** ✅ Solucionado  
**Fecha:** 2025-11-14  
**Archivos modificados:**
- `backend/routes/auth.py`
- `backend/scripts/load_test_data.py`
- `backend/scripts/load_complete_test_data.py`
- `reset_and_load_data.py` (nuevo)
