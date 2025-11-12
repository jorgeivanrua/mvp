# 🚀 Cómo Iniciar la Aplicación

## ✅ Solución Definitiva a Problemas de Inicio

Se han creado scripts robustos para garantizar que la aplicación inicie correctamente siempre.

---

## 📋 Métodos de Inicio

### Método 1: Script Python (Recomendado)
```bash
python start_app.py
```

**Ventajas:**
- ✅ Muestra mensajes claros de inicio
- ✅ Verifica que todo esté correcto
- ✅ Maneja errores de forma elegante
- ✅ Funciona en cualquier sistema operativo

### Método 2: Script Batch (Windows)
```bash
start.bat
```

**Ventajas:**
- ✅ Activa automáticamente el entorno virtual
- ✅ Verifica Python
- ✅ Fácil de usar (doble clic)

### Método 3: Comando Directo (Original)
```bash
.venv\Scripts\python.exe run.py
```

**Nota:** Este método funciona pero no tiene las verificaciones adicionales.

---

## 🔧 Scripts Creados

### 1. `start_app.py`
Script Python robusto que:
- Verifica imports
- Crea la aplicación
- Muestra información detallada
- Maneja errores correctamente

### 2. `start.bat`
Script batch para Windows que:
- Activa el entorno virtual
- Verifica Python
- Ejecuta start_app.py
- Pausa al finalizar para ver errores

### 3. `run.py` (Original)
Script simple original que sigue funcionando.

---

## 📊 Salida Esperada

Cuando inicies correctamente, verás:

```
============================================================
INICIANDO SISTEMA ELECTORAL
============================================================

[1/3] Importando módulos...
✓ Módulos importados correctamente

[2/3] Creando aplicación...
✓ Aplicación creada correctamente

[3/3] Iniciando servidor...

============================================================
SERVIDOR INICIADO EXITOSAMENTE
============================================================

✓ URL: http://127.0.0.1:5000
✓ Debug: True
✓ Templates: ../frontend/templates
✓ Static: C:\testigos\mvp\backend\../frontend/static

Presiona Ctrl+C para detener el servidor

============================================================

 * Serving Flask app 'backend.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

---

## ❌ Solución de Problemas

### Problema: "Python no encontrado"
**Solución:**
```bash
# Activar entorno virtual primero
.venv\Scripts\activate

# Luego iniciar
python start_app.py
```

### Problema: "ModuleNotFoundError"
**Solución:**
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: "Puerto 5000 en uso"
**Solución:**
```bash
# Encontrar proceso usando el puerto
netstat -ano | findstr :5000

# Matar el proceso (reemplaza PID con el número real)
taskkill /PID <PID> /F
```

### Problema: "Base de datos no encontrada"
**Solución:**
```bash
# Recargar datos
python scripts\load_divipola.py
python scripts\create_test_users.py
```

---

## 🔄 Reiniciar la Aplicación

### Opción 1: Ctrl+C y reiniciar
```bash
# Presionar Ctrl+C en la terminal
# Luego ejecutar nuevamente
python start_app.py
```

### Opción 2: Limpiar cache y reiniciar
```bash
# Limpiar cache de Python
Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse -Force | Remove-Item -Recurse -Force

# Reiniciar
python start_app.py
```

---

## 📝 Verificar que Funciona

### 1. Verificar en el navegador
```
http://127.0.0.1:5000
```

Deberías ver la página de login.

### 2. Verificar con curl
```powershell
curl http://127.0.0.1:5000 -UseBasicParsing
```

Debería devolver `StatusCode: 200`

### 3. Verificar logs
Los logs mostrarán las peticiones:
```
127.0.0.1 - - [11/Nov/2025 20:14:55] "GET / HTTP/1.1" 200 -
```

---

## 🎯 Inicio Rápido (Resumen)

```bash
# 1. Activar entorno virtual (si no está activo)
.venv\Scripts\activate

# 2. Iniciar aplicación
python start_app.py

# 3. Abrir navegador
# http://127.0.0.1:5000

# 4. Login con:
# Usuario: testigo_electoral
# Password: Testigo123!
```

---

## 📦 Archivos de Inicio

| Archivo | Propósito | Cuándo Usar |
|---------|-----------|-------------|
| `start_app.py` | Script robusto con verificaciones | **Recomendado siempre** |
| `start.bat` | Script batch para Windows | Doble clic rápido |
| `run.py` | Script original simple | Desarrollo rápido |

---

## ✅ Checklist de Inicio

Antes de iniciar, verifica:

- [ ] Entorno virtual activado
- [ ] Base de datos existe (`electoral.db`)
- [ ] Puerto 5000 disponible
- [ ] Dependencias instaladas
- [ ] En el directorio correcto (`mvp/`)

---

## 🆘 Soporte

Si sigues teniendo problemas:

1. **Verifica imports:**
   ```bash
   python test_import.py
   ```

2. **Verifica base de datos:**
   ```bash
   python -c "import os; print('DB exists:', os.path.exists('electoral.db'))"
   ```

3. **Verifica puerto:**
   ```bash
   netstat -ano | findstr :5000
   ```

4. **Logs detallados:**
   Revisa los mensajes en la terminal donde iniciaste la aplicación.

---

## 🎉 Conclusión

Con estos scripts, la aplicación debería iniciar **sin problemas** siempre.

**Comando recomendado:**
```bash
python start_app.py
```

**URL de acceso:**
```
http://127.0.0.1:5000
```

**Estado actual:** ✅ **FUNCIONANDO CORRECTAMENTE**
