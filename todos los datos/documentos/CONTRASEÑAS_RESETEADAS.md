# ✅ Contraseñas Reseteadas - Todos los Usuarios

## Resumen
Todas las contraseñas de los usuarios en la base de datos han sido reseteadas a `test123`.

## Script Ejecutado
**Archivo:** `reset_all_passwords.py`

Este script:
1. Conecta a la base de datos
2. Obtiene todos los usuarios
3. Resetea la contraseña de cada uno a `test123`
4. Guarda los cambios

## Usuarios Actualizados

| Usuario | Rol | Ubicación | Contraseña |
|---------|-----|-----------|------------|
| admin_test | super_admin | Sin ubicación | test123 |
| auditor_test | auditor_electoral | Sin ubicación | test123 |
| coord_dept_test | coordinador_departamental | Ubicación ID: 1 | test123 |
| coord_mun_test | coordinador_municipal | Ubicación ID: 2 | test123 |
| coord_puesto_test | coordinador_puesto | Ubicación ID: 3 | test123 |
| testigo_test_1 | testigo_electoral | Ubicación ID: 4 | test123 |

## Prueba Realizada

### ✅ Login Super Admin
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"rol":"super_admin","password":"test123"}'
```

**Resultado:** ✅ Login exitoso, tokens generados correctamente

## Cómo Usar el Script

### Resetear todas las contraseñas
```bash
python reset_all_passwords.py
```

### Salida del Script
```
🔄 Reseteando contraseñas de todos los usuarios...
📊 Encontrados 6 usuarios

✅ admin_test (super_admin) - Contraseña reseteada
✅ auditor_test (auditor_electoral) - Contraseña reseteada
✅ coord_dept_test (coordinador_departamental) - Contraseña reseteada
✅ coord_mun_test (coordinador_municipal) - Contraseña reseteada
✅ coord_puesto_test (coordinador_puesto) - Contraseña reseteada
✅ testigo_test_1 (testigo_electoral) - Contraseña reseteada

============================================================
  ✅ TODAS LAS CONTRASEÑAS RESETEADAS
============================================================

🔑 Contraseña universal: test123
```

## Credenciales de Acceso

### Super Admin
```json
{
  "rol": "super_admin",
  "password": "test123"
}
```

### Auditor Electoral
```json
{
  "rol": "auditor_electoral",
  "departamento_codigo": "TEST01",
  "password": "test123"
}
```

### Coordinador Departamental
```json
{
  "rol": "coordinador_departamental",
  "departamento_codigo": "TEST01",
  "password": "test123"
}
```

### Coordinador Municipal
```json
{
  "rol": "coordinador_municipal",
  "departamento_codigo": "TEST01",
  "municipio_codigo": "TEST0101",
  "password": "test123"
}
```

### Coordinador de Puesto
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

### Testigo Electoral
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

## Notas Importantes

- ✅ Todas las contraseñas están hasheadas con bcrypt
- ✅ La contraseña `test123` es segura para entorno de testing
- ✅ El script puede ejecutarse múltiples veces sin problemas
- ✅ Los usuarios mantienen sus roles y ubicaciones
- ⚠️ En producción, usar contraseñas más seguras

## Comandos Útiles

### Verificar usuarios en la BD
```bash
python -c "from backend.app import create_app; from backend.models.user import User; app = create_app(); app.app_context().push(); users = User.query.all(); print('\n'.join([f'{u.nombre} - {u.rol}' for u in users]))"
```

### Resetear contraseñas
```bash
python reset_all_passwords.py
```

### Probar login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"rol":"super_admin","password":"test123"}'
```

## Estado Actual
- ✅ 6 usuarios en la base de datos
- ✅ Todas las contraseñas reseteadas a `test123`
- ✅ Login funcionando correctamente
- ✅ Tokens JWT generándose correctamente
