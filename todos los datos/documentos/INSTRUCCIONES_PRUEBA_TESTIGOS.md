# Instrucciones de Prueba - Sistema de Testigos

## ✅ Configuración Completada

Se han realizado las siguientes configuraciones:

1. ✅ Migración de BD ejecutada (campos de presencia agregados)
2. ✅ 3 testigos de prueba creados
3. ✅ Endpoint para testigos implementado
4. ✅ Guardado local de formularios implementado
5. ✅ Sincronización con servidor implementada

## 🧪 Pruebas a Realizar

### Paso 1: Iniciar el Servidor

```bash
python backend/app.py
```

El servidor debería iniciar en: `http://localhost:5000`

### Paso 2: Probar Login de Testigo

1. Abrir navegador en: `http://localhost:5000/login`
2. Usar credenciales:
   - **Usuario**: `Testigo Mesa 01`
   - **Contraseña**: `testigo123`
3. Hacer clic en "Iniciar Sesión"

**Resultado Esperado:**
- Redirección a `/testigo/dashboard`
- Ver información de la mesa asignada
- Ver botón "Verificar Mi Presencia en la Mesa"

### Paso 3: Verificar Presencia del Testigo

1. En el dashboard del testigo, hacer clic en **"Verificar Mi Presencia en la Mesa"**
2. Confirmar en el diálogo

**Resultado Esperado:**
- Mensaje de éxito: "Presencia verificada exitosamente"
- El botón desaparece
- Aparece alerta verde: "Presencia verificada"
- Se muestra fecha y hora de verificación

### Paso 4: Crear Formulario E14 (Borrador Local)

1. Hacer clic en **"Nuevo Formulario"**
2. Seleccionar:
   - Mesa: Mesa 01
   - Tipo de Elección: (seleccionar uno disponible)
3. Esperar a que carguen partidos y candidatos
4. Ingresar datos de votación:
   - Votos Nulos: 10
   - Votos en Blanco: 5
   - Tarjetas No Marcadas: 15
   - Votos por partido/candidato: (ingresar algunos valores)
5. Hacer clic en **"Guardar Borrador"**

**Resultado Esperado:**
- Mensaje: "Borrador guardado localmente"
- El formulario aparece en la tabla con estado "Guardado Localmente" (badge azul)
- El formulario se guarda en localStorage del navegador

### Paso 5: Enviar Formulario al Servidor

1. Crear otro formulario (o editar el borrador)
2. Llenar todos los datos requeridos
3. Hacer clic en **"Enviar para Revisión"**

**Resultado Esperado:**
- Mensaje: "Formulario E-14 enviado para revisión"
- El formulario aparece con estado "Pendiente" (badge amarillo)
- El borrador local se elimina automáticamente

### Paso 6: Probar Guardado Sin Conexión

1. **Desconectar internet** o detener el servidor
2. Crear un nuevo formulario
3. Llenar datos
4. Hacer clic en **"Enviar para Revisión"**

**Resultado Esperado:**
- Aparece diálogo: "No se pudo enviar el formulario. ¿Desea guardarlo localmente?"
- Al aceptar: "Formulario guardado localmente"
- El formulario aparece con estado "Guardado Localmente"

### Paso 7: Sincronizar Borradores

1. **Reconectar internet** o reiniciar el servidor
2. Recargar el dashboard del testigo
3. Debería aparecer un **indicador flotante** en la esquina inferior derecha:
   - "X formulario(s) pendiente(s) de sincronizar"
   - Botón "Sincronizar"
4. Hacer clic en **"Sincronizar"**

**Resultado Esperado:**
- Mensaje: "X formulario(s) sincronizado(s) exitosamente"
- Los formularios locales se envían al servidor
- Cambian de estado "Guardado Localmente" a "Pendiente"
- El indicador flotante desaparece

### Paso 8: Verificar en Dashboard del Coordinador

1. Cerrar sesión del testigo
2. Iniciar sesión como coordinador de puesto:
   - **Usuario**: `Coordinador Puesto 01`
   - **Contraseña**: (la que hayas configurado)
3. Ir a `/coordinador/puesto`

**Resultado Esperado:**
- Ver lista de mesas del puesto
- Ver **ícono de verificación de presencia** (✅) junto al nombre del testigo
- Ver formularios enviados por el testigo con estado "Pendiente"
- Poder revisar y validar los formularios

## 🔍 Verificaciones Adicionales

### Verificar Datos en la Base de Datos

```bash
# Ver testigos creados
python -c "import sys; sys.path.insert(0, '.'); from backend.database import db; from backend.models.user import User; from backend.app import create_app; app = create_app(); app.app_context().push(); testigos = User.query.filter_by(rol='testigo_electoral').all(); [print(f'{t.id}: {t.nombre} - Presencia: {t.presencia_verificada}') for t in testigos]"

# Ver formularios creados
python -c "import sys; sys.path.insert(0, '.'); from backend.database import db; from backend.models.formulario_e14 import FormularioE14; from backend.app import create_app; app = create_app(); app.app_context().push(); forms = FormularioE14.query.all(); print(f'Total formularios: {len(forms)}'); [print(f'{f.id}: Mesa {f.mesa_id} - Estado: {f.estado}') for f in forms]"
```

### Verificar Estado de Mesas

```bash
python backend/scripts/verificar_mesas.py 01
```

## 📝 Checklist de Pruebas

- [ ] Login de testigo funciona
- [ ] Dashboard del testigo carga correctamente
- [ ] Botón de verificación de presencia funciona
- [ ] Crear formulario E14 funciona
- [ ] Guardar borrador local funciona
- [ ] Enviar formulario al servidor funciona
- [ ] Guardado sin conexión funciona
- [ ] Sincronización de borradores funciona
- [ ] Coordinador ve ícono de presencia verificada
- [ ] Coordinador ve formularios pendientes
- [ ] Coordinador puede validar formularios

## 🐛 Problemas Comunes

### Error: "CHECK constraint failed: check_rol_valido"
**Solución**: El rol debe ser `testigo_electoral`, no `testigo`

### Error: "no such column: users.presencia_verificada"
**Solución**: Ejecutar la migración:
```bash
python backend/migrations/add_presencia_verificada_to_users.py
```

### Formularios no aparecen en el dashboard
**Solución**: Verificar que el endpoint `/api/formularios/mis-formularios` esté funcionando

### Sincronización no funciona
**Solución**: Verificar que haya conexión al servidor y que los borradores estén en localStorage

## 📊 Datos de Prueba

### Testigos Creados:
1. **Testigo Mesa 01** - Mesa ID: 5 - Password: testigo123
2. **Testigo Mesa 02** - Mesa ID: 6 - Password: testigo123
3. **Testigo Mesa 03** - Mesa ID: 7 - Password: testigo123

### Puesto:
- **Código**: 01
- **Nombre**: CAQUETA - FLORENCIA - Zona 01 - I.E. JUAN BAUTISTA LA SALLE
- **Departamento**: 44 (Caquetá)
- **Municipio**: 01 (Florencia)
- **Zona**: 01

### Mesas:
- **Mesa 01**: 2,675 votantes registrados
- **Mesa 02**: 2,674 votantes registrados
- **Mesa 03**: 2,674 votantes registrados

## 🎯 Resultado Final Esperado

Al completar todas las pruebas:

1. ✅ Los 3 testigos pueden iniciar sesión
2. ✅ Los 3 testigos han verificado su presencia
3. ✅ Se han creado formularios E14 (algunos locales, algunos en servidor)
4. ✅ La sincronización funciona correctamente
5. ✅ El coordinador ve los íconos de presencia
6. ✅ El coordinador puede validar formularios

## 📞 Soporte

Si encuentras algún problema durante las pruebas, verifica:

1. Que el servidor esté corriendo
2. Que la migración se haya ejecutado
3. Que los testigos existan en la BD
4. Que las mesas estén correctamente configuradas
5. Los logs del navegador (F12 → Console)
6. Los logs del servidor

---

**Fecha de creación**: 2025-11-12
**Versión**: 1.0
