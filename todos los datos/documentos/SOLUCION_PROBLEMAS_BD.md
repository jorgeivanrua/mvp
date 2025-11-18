# 🔧 Solución a Problemas de Base de Datos

## Problemas Identificados

### 1. ❌ Local muestra "Departamento Test" en lugar de datos reales
**Causa:** La base de datos local solo tiene datos de testing (TEST01)

### 2. ❌ En Render la contraseña test123 no funciona
**Causa:** Los usuarios en Render tienen contraseñas diferentes

## Soluciones

### Solución 1: Cargar Datos Reales en Local

#### Opción A: Usar datos de testing (Recomendado para desarrollo)
Los datos de testing ya están cargados y funcionan correctamente:
- Departamento: TEST01
- Municipio: TEST0101
- Contraseña: test123

**No requiere acción** - El sistema funciona con estos datos

#### Opción B: Cargar datos de CAQUETA/FLORENCIA en local

**Paso 1:** Verificar si tienes un archivo SQL con los datos de producción
```bash
# Buscar archivos SQL
dir *.sql
```

**Paso 2:** Si tienes los datos, importarlos
```bash
# Ejemplo con SQLite
sqlite3 electoral.db < datos_caqueta.sql
```

**Paso 3:** Crear usuarios para CAQUETA/FLORENCIA
```bash
python backend/scripts/crear_usuarios_florencia.py
```

**Paso 4:** Resetear contraseñas
```bash
python reset_all_passwords.py
```

### Solución 2: Resetear Contraseñas en Render

#### Opción A: Usar el Shell de Render (Recomendado)

**Paso 1:** Ir al Dashboard de Render
```
https://dashboard.render.com
```

**Paso 2:** Seleccionar el servicio "mvp"

**Paso 3:** Click en "Shell" en el menú lateral

**Paso 4:** Ejecutar el script de reseteo
```bash
python reset_all_passwords.py
```

**Paso 5:** Verificar la salida
Deberías ver:
```
✅ TODAS LAS CONTRASEÑAS RESETEADAS
🔑 Contraseña universal: test123
```

#### Opción B: Usar el Endpoint Temporal (Solo Testing)

**⚠️ IMPORTANTE:** Este endpoint solo funciona en ambiente de desarrollo

**Paso 1:** Hacer una petición POST al endpoint
```bash
curl -X POST https://mvp-b9uv.onrender.com/api/auth/reset-all-passwords-test123
```

**Paso 2:** Verificar la respuesta
```json
{
  "success": true,
  "message": "X contraseñas reseteadas a test123",
  "users_updated": X
}
```

**⚠️ Nota:** Este endpoint está bloqueado en producción por seguridad

#### Opción C: Actualizar Contraseñas Manualmente via SQL

Si tienes acceso a la base de datos de Render:

**Paso 1:** Conectar a la base de datos PostgreSQL

**Paso 2:** Ejecutar el siguiente SQL:
```sql
-- Generar hash de test123 con bcrypt
-- Hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztP.yQZqVpQu

UPDATE users 
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztP.yQZqVpQu'
WHERE activo = true;
```

**⚠️ Advertencia:** Esto cambiará TODAS las contraseñas a test123

## Verificación

### Verificar Datos en Local

```bash
# Ver departamentos disponibles
python -c "from backend.app import create_app; from backend.models.location import Location; app = create_app(); app.app_context().push(); locs = Location.query.filter_by(tipo='departamento').all(); print('\n'.join([f'{l.departamento_codigo} - {l.departamento_nombre}' for l in locs]))"
```

**Salida esperada:**
```
TEST01 - Departamento Test
```
O si cargaste datos de producción:
```
44 - CAQUETA
```

### Verificar Usuarios en Local

```bash
# Ver usuarios disponibles
python -c "from backend.app import create_app; from backend.models.user import User; app = create_app(); app.app_context().push(); users = User.query.all(); print('\n'.join([f'{u.nombre} - {u.rol}' for u in users]))"
```

### Probar Login en Render

**URL:** https://mvp-b9uv.onrender.com/auth/login

**Credenciales de prueba:**
```
Rol: Testigo Electoral
Departamento: CAQUETA
Municipio: FLORENCIA
Zona: CAQUETA - FLORENCIA - Zona 01
Puesto: I.E. JUAN BAUTISTA LA SALLE
Contraseña: test123
```

## Recomendaciones

### Para Desarrollo Local

1. **Usar datos de testing (TEST01)**
   - Más rápido y simple
   - Datos controlados
   - Contraseñas conocidas (test123)

2. **Mantener base de datos separada**
   - Local: electoral.db (SQLite)
   - Render: PostgreSQL

### Para Producción (Render)

1. **Resetear contraseñas solo en testing**
   - No usar test123 en producción real
   - Usar contraseñas seguras

2. **Eliminar endpoint temporal**
   - Comentar o eliminar `/reset-all-passwords-test123`
   - Solo para ambiente de desarrollo

3. **Backup de base de datos**
   - Hacer backup antes de cambios masivos
   - Render hace backups automáticos

## Scripts Disponibles

### reset_all_passwords.py
```bash
python reset_all_passwords.py
```
Resetea todas las contraseñas a test123 en la BD actual

### load_basic_data.py
```bash
python load_basic_data.py
```
Carga datos de testing (TEST01) en la BD local

### crear_usuarios_florencia.py
```bash
python backend/scripts/crear_usuarios_florencia.py
```
Crea usuarios para CAQUETA/FLORENCIA (requiere que las ubicaciones ya existan)

## Solución Rápida

### Para Local (Usar datos de testing)
```bash
# Ya está configurado, no requiere acción
# Usar: TEST01, test123
```

### Para Render (Resetear contraseñas)
```bash
# Opción 1: Shell de Render
python reset_all_passwords.py

# Opción 2: Endpoint temporal (si está habilitado)
curl -X POST https://mvp-b9uv.onrender.com/api/auth/reset-all-passwords-test123
```

## Estado Actual

### Local
- ✅ Datos de testing (TEST01) cargados
- ✅ Contraseñas: test123
- ✅ Funcionando correctamente

### Render
- ✅ Datos de producción (CAQUETA) cargados
- ❌ Contraseñas: NO son test123
- ⏳ Requiere reseteo de contraseñas

## Próximos Pasos

1. **Decidir estrategia de datos:**
   - ¿Usar TEST01 en local? (Recomendado)
   - ¿O cargar datos de CAQUETA en local?

2. **Resetear contraseñas en Render:**
   - Usar Shell de Render
   - Ejecutar reset_all_passwords.py

3. **Verificar funcionamiento:**
   - Probar login en ambos ambientes
   - Verificar que test123 funcione

## Contacto y Soporte

Si los problemas persisten:
1. Verificar logs del servidor
2. Revisar errores en consola del navegador
3. Verificar conectividad a la base de datos
4. Contactar al administrador del sistema
