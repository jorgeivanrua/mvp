# Comparación de Datos: Local vs Render

## Estado Actual

### Local (127.0.0.1:5000)
**Base de Datos:** SQLite (`electoral.db`)

**Departamentos disponibles:**
- TEST01 - Departamento Test

**Usuarios:**
- admin_test (super_admin)
- auditor_test (auditor_electoral)  
- coord_dept_test (coordinador_departamental)
- coord_mun_test (coordinador_municipal)
- coord_puesto_test (coordinador_puesto)
- testigo_test_1 (testigo_electoral)

**Contraseñas:** test123 ✅

### Render (mvp-b9uv.onrender.com)
**Base de Datos:** PostgreSQL

**Departamentos disponibles:**
- 44 - CAQUETA

**Municipios:**
- FLORENCIA

**Usuarios:**
- Usuarios de producción con contraseñas diferentes

**Contraseñas:** NO son test123 ❌

## ¿Por qué son diferentes?

### Diseño Intencional
- **Local:** Datos de testing para desarrollo rápido
- **Render:** Datos de producción reales

### Ventajas de mantenerlos separados
1. **Desarrollo más rápido** - Datos simples y controlados
2. **Sin riesgo** - No afectas datos de producción
3. **Testing predecible** - Siempre sabes qué datos hay

## Opciones

### Opción 1: Mantener Separados (Recomendado)

**Local:**
- Usar TEST01 para desarrollo
- Contraseña: test123
- Datos controlados

**Render:**
- Datos reales de CAQUETA
- Resetear contraseñas a test123 para testing

**Ventajas:**
- ✅ Desarrollo rápido
- ✅ Sin riesgo de corromper datos
- ✅ Testing predecible

### Opción 2: Sincronizar Datos

**Importar datos de Render a Local:**

1. **Exportar desde Render:**
```bash
# En Shell de Render
pg_dump $DATABASE_URL > backup.sql
```

2. **Descargar backup**

3. **Convertir PostgreSQL a SQLite:**
```bash
# Requiere herramientas de conversión
pgloader backup.sql sqlite://electoral.db
```

4. **Resetear contraseñas:**
```bash
python reset_all_passwords.py
```

**Desventajas:**
- ⚠️ Proceso complejo
- ⚠️ Requiere herramientas adicionales
- ⚠️ Puede causar problemas de compatibilidad

### Opción 3: Usar Render para Testing

**Trabajar directamente en Render:**

1. Resetear contraseñas en Render
2. Usar Render para todas las pruebas
3. No usar local

**Ventajas:**
- ✅ Datos reales
- ✅ Ambiente de producción

**Desventajas:**
- ⚠️ Más lento (requiere internet)
- ⚠️ Puede afectar datos de producción

## Recomendación

### Para Desarrollo: Usar Local con TEST01

**Razones:**
1. Más rápido
2. Datos controlados
3. Sin riesgo
4. Contraseñas conocidas

**Cómo usar:**
```
URL: http://localhost:5000/auth/login
Rol: Testigo Electoral
Departamento: TEST01
Municipio: TEST0101
Zona: TEST01Z1
Puesto: TEST0101001
Contraseña: test123
```

### Para Testing con Datos Reales: Usar Render

**Pasos:**
1. Resetear contraseñas en Render (Shell)
2. Usar datos de CAQUETA/FLORENCIA
3. Probar con datos reales

**Cómo usar:**
```
URL: https://mvp-b9uv.onrender.com/auth/login
Rol: Testigo Electoral
Departamento: CAQUETA
Municipio: FLORENCIA
Zona: CAQUETA - FLORENCIA - Zona 01
Puesto: I.E. JUAN BAUTISTA LA SALLE
Contraseña: test123 (después de resetear)
```

## Solución Inmediata

### Problema: "Quiero ver CAQUETA en local"

**Solución Rápida:** No es necesario

Los datos de TEST01 son suficientes para:
- Desarrollo
- Testing de funcionalidades
- Debugging
- Demostración

**Si realmente necesitas CAQUETA en local:**
1. Exportar datos de Render
2. Importar a local
3. Resetear contraseñas

**Pero es más fácil:**
- Usar Render directamente para testing con datos reales
- Usar local para desarrollo con TEST01

### Problema: "test123 no funciona en Render"

**Solución:**

1. **Ir a Render Shell:**
   - https://dashboard.render.com
   - Seleccionar servicio "mvp"
   - Click en "Shell"

2. **Ejecutar:**
```bash
python reset_all_passwords.py
```

3. **Verificar:**
```bash
# Deberías ver:
✅ TODAS LAS CONTRASEÑAS RESETEADAS
🔑 Contraseña universal: test123
```

4. **Probar login:**
   - https://mvp-b9uv.onrender.com/auth/login
   - Usar test123

## Conclusión

**Estado Actual:**
- ✅ Local funciona correctamente con TEST01
- ❌ Render necesita reseteo de contraseñas

**Acción Requerida:**
- Resetear contraseñas en Render usando Shell

**Resultado Esperado:**
- ✅ Local: TEST01 + test123
- ✅ Render: CAQUETA + test123

Ambos ambientes funcionando correctamente para sus propósitos.
