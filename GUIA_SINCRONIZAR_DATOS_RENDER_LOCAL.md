# 📋 Guía: Sincronizar Datos de Render a Local

## Objetivo
Hacer que tu base de datos local tenga exactamente los mismos datos que Render (CAQUETA, FLORENCIA, etc.)

## Pasos

### Paso 1: Exportar Datos desde Render

1. **Ir al Dashboard de Render**
   ```
   https://dashboard.render.com
   ```

2. **Seleccionar el servicio "mvp"**

3. **Abrir Shell**
   - Click en "Shell" en el menú lateral izquierdo

4. **Ejecutar el script de exportación**
   ```bash
   python export_data_from_render.py
   ```

5. **Verificar la salida**
   Deberías ver algo como:
   ```
   ✅ EXPORTACIÓN COMPLETADA
   Archivo generado: render_data_export.json
   
   Resumen:
     - Ubicaciones: XXX
     - Usuarios: XXX
     - Campañas: XXX
     - Tipos de elección: XXX
     - Partidos: XXX
   ```

6. **Descargar el archivo**
   - El archivo `render_data_export.json` se generó en Render
   - Necesitas descargarlo a tu computadora
   
   **Opción A: Copiar contenido**
   ```bash
   cat render_data_export.json
   ```
   - Copiar todo el contenido
   - Crear archivo local `render_data_export.json`
   - Pegar el contenido

   **Opción B: Usar comando (si está disponible)**
   ```bash
   # Render puede tener limitaciones para descargar archivos
   # La opción A es más confiable
   ```

### Paso 2: Importar Datos a Local

1. **Verificar que tienes el archivo**
   ```bash
   # En tu proyecto local
   dir render_data_export.json
   ```

2. **Ejecutar el script de importación**
   ```bash
   python import_data_to_local.py
   ```

3. **Confirmar la importación**
   El script te preguntará:
   ```
   ⚠️  ADVERTENCIA: Esto eliminará todos los datos actuales en la BD local
   ¿Continuar? (si/no):
   ```
   
   Escribe: `si`

4. **Esperar a que termine**
   Verás el progreso:
   ```
   🔄 Limpiando base de datos local...
   ✓ Base de datos limpia
   
   📍 Importando ubicaciones...
   ✓ XXX ubicaciones importadas
   
   👥 Importando usuarios...
   ✓ XXX usuarios importados (contraseña: test123)
   
   📅 Importando campañas...
   ✓ XXX campañas importadas
   
   🗳️  Importando tipos de elección...
   ✓ XXX tipos de elección importados
   
   🏛️  Importando partidos...
   ✓ XXX partidos importados
   
   ✅ IMPORTACIÓN COMPLETADA
   ```

### Paso 3: Verificar

1. **Reiniciar el servidor local** (si está corriendo)
   ```bash
   # Detener el servidor (Ctrl+C)
   # Iniciar nuevamente
   python run.py
   ```

2. **Abrir el navegador**
   ```
   http://localhost:5000/auth/login
   ```

3. **Verificar que aparezcan los datos de Render**
   - Departamento: Deberías ver CAQUETA (no TEST01)
   - Municipio: Deberías ver FLORENCIA
   - Zonas y Puestos: Los mismos que en Render

4. **Probar login**
   ```
   Rol: Testigo Electoral
   Departamento: CAQUETA
   Municipio: FLORENCIA
   Zona: CAQUETA - FLORENCIA - Zona 01
   Puesto: I.E. JUAN BAUTISTA LA SALLE
   Contraseña: test123
   ```

## Solución Rápida: Resetear Contraseñas en Render

Si solo quieres que las contraseñas funcionen en Render (sin sincronizar datos):

1. **Ir a Render Shell**
   ```
   https://dashboard.render.com → mvp → Shell
   ```

2. **Ejecutar**
   ```bash
   python reset_all_passwords.py
   ```

3. **Listo**
   Ahora puedes usar `test123` en Render con los datos de CAQUETA

## Archivos Creados

- `export_data_from_render.py` - Script para exportar desde Render
- `import_data_to_local.py` - Script para importar a local
- `render_data_export.json` - Archivo con los datos (se genera al exportar)

## Notas Importantes

### ⚠️ Advertencias

1. **Backup**: El script eliminará todos los datos actuales en local
2. **Contraseñas**: Todos los usuarios tendrán contraseña `test123` en local
3. **Formularios**: Los formularios E-14 NO se exportan (solo estructura)

### ✅ Ventajas

1. Datos idénticos en local y Render
2. Puedes desarrollar con datos reales
3. Testing más realista

### ❌ Desventajas

1. Proceso manual (requiere copiar archivo)
2. Necesitas repetir si los datos cambian en Render
3. Más complejo que usar datos de testing

## Alternativa: Mantener Separados

Si prefieres mantener los ambientes separados:

**Local:**
- Datos de testing (TEST01)
- Desarrollo rápido
- Contraseña: test123

**Render:**
- Datos reales (CAQUETA)
- Testing con datos reales
- Contraseña: test123 (después de resetear)

## Troubleshooting

### Error: "No se encontró el archivo render_data_export.json"
**Solución:** Asegúrate de haber copiado el archivo a la raíz del proyecto

### Error: "Permission denied"
**Solución:** Verifica que tengas permisos de escritura en la carpeta

### Error: "Database is locked"
**Solución:** Cierra el servidor local antes de importar

### Los datos no aparecen
**Solución:** Reinicia el servidor local después de importar

## Resumen

**Para sincronizar datos:**
1. Exportar desde Render: `python export_data_from_render.py`
2. Copiar archivo a local
3. Importar en local: `python import_data_to_local.py`
4. Reiniciar servidor
5. ¡Listo!

**Para solo arreglar contraseñas en Render:**
1. Ir a Render Shell
2. Ejecutar: `python reset_all_passwords.py`
3. ¡Listo!
