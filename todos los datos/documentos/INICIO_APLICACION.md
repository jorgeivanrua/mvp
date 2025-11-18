# 🚀 Guía de Inicio de la Aplicación

## Inicio en Local (Desarrollo)

### Windows

```bash
# Opción 1: Usar script batch
start_local.bat

# Opción 2: Comando directo
python run.py
```

### Linux/Mac

```bash
# Opción 1: Usar script bash
chmod +x start_local.sh
./start_local.sh

# Opción 2: Comando directo
python run.py
```

### Configuración Local

La aplicación se iniciará con:
- **URL**: http://localhost:5000
- **Modo**: Development
- **Debug**: Activado
- **Base de datos**: SQLite local (`electoral.db`)
- **Puerto**: 5000 (configurable con variable `PORT`)

## Inicio en Render (Producción)

### Configuración Automática

Render ejecutará automáticamente:
```bash
./start.sh
```

Este script:
1. Configura variables de entorno de producción
2. Inicializa la base de datos PostgreSQL
3. Inicia Gunicorn con 4 workers

### Variables de Entorno en Render

Asegúrate de configurar:
- `DATABASE_URL`: URL de PostgreSQL (automática en Render)
- `SECRET_KEY`: Clave secreta para Flask
- `JWT_SECRET_KEY`: Clave secreta para JWT
- `FLASK_ENV`: production
- `DEBUG`: False

## Estructura de Archivos

```
mvp/
├── run.py                 # Punto de entrada principal
├── start_local.bat        # Script de inicio Windows
├── start_local.sh         # Script de inicio Linux/Mac
├── start.sh              # Script de inicio Render
├── backend/
│   ├── app.py            # Factory de la aplicación
│   ├── config.py         # Configuraciones
│   └── ...
└── ...
```

## Verificación del Inicio

### 1. Verificar que el servidor está corriendo

```bash
# En otra terminal
curl http://localhost:5000/
```

Deberías ver la página de inicio del sistema.

### 2. Verificar la API

```bash
curl http://localhost:5000/api/public/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "message": "Sistema Electoral API funcionando"
}
```

### 3. Acceder al sistema

Abre tu navegador en:
- **Local**: http://localhost:5000
- **Render**: https://tu-app.onrender.com

## Credenciales de Prueba

```
Super Admin:
  Usuario: super_admin
  Contraseña: admin123

Coordinador de Puesto:
  Usuario: Coordinador Puesto 01
  Contraseña: coord123

Testigo Electoral:
  Usuario: Testigo Mesa 01
  Contraseña: testigo123
```

## Solución de Problemas

### Error: "No module named 'backend'"

**Solución**: Ejecuta desde la raíz del proyecto:
```bash
python run.py
```

### Error: "Address already in use"

**Solución**: El puerto 5000 está ocupado. Cambia el puerto:
```bash
# Windows
set PORT=5001
python run.py

# Linux/Mac
PORT=5001 python run.py
```

### Error: "Database not found"

**Solución**: Inicializa la base de datos:
```bash
python init_render_db.py
```

### Error: "ModuleNotFoundError"

**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Logs y Debugging

### Ver logs en tiempo real (Local)

Los logs se muestran en la consola donde ejecutaste `run.py`

### Ver logs en Render

1. Ve al dashboard de Render
2. Selecciona tu servicio
3. Click en "Logs"

## Detener la Aplicación

### Local

- Presiona `Ctrl+C` en la terminal donde está corriendo
- En Windows con el script batch, presiona cualquier tecla después de `Ctrl+C`

### Render

La aplicación se detiene automáticamente cuando:
- Haces un nuevo deploy
- Detienes el servicio desde el dashboard

## Reiniciar la Aplicación

### Local

1. Detén la aplicación (`Ctrl+C`)
2. Vuelve a ejecutar el script de inicio

### Render

1. Ve al dashboard
2. Click en "Manual Deploy" → "Deploy latest commit"
3. O haz un push a la rama main para deploy automático

## Modos de Ejecución

### Development (Local)

```bash
export FLASK_ENV=development
export DEBUG=True
python run.py
```

Características:
- Debug activado
- Recarga automática de código
- Logs detallados
- SQLite local

### Production (Render)

```bash
export FLASK_ENV=production
export DEBUG=False
gunicorn run:app
```

Características:
- Debug desactivado
- Múltiples workers
- PostgreSQL
- Logs optimizados

## Comandos Útiles

```bash
# Ver procesos Python corriendo
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python

# Matar proceso por puerto
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

## Próximos Pasos

1. ✅ Iniciar la aplicación
2. ✅ Verificar que carga correctamente
3. ✅ Hacer login con credenciales de prueba
4. ✅ Explorar los diferentes dashboards
5. ✅ Probar funcionalidades básicas

---

**Nota**: Para más información sobre el sistema, consulta `PRUEBA_SISTEMA_COMPLETO_EXITOSA.md`
