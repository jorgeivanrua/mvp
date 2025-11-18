# 🚀 Guía de Deploy en Render

## Preparación Previa

### 1. Asegúrate de tener estos archivos en tu repositorio:
- ✅ `render.yaml` - Configuración de Render
- ✅ `build.sh` - Script de construcción
- ✅ `requirements.txt` - Dependencias Python
- ✅ `run.py` - Punto de entrada de la aplicación
- ✅ Archivo CSV de datos (divipola.csv)

### 2. Sube tu código a GitHub
```bash
git init
git add .
git commit -m "Initial commit - Sistema Electoral"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

## Deploy en Render

### Paso 1: Crear cuenta en Render
1. Ve a https://render.com
2. Regístrate con tu cuenta de GitHub
3. Autoriza a Render para acceder a tus repositorios

### Paso 2: Crear nuevo Web Service
1. Click en "New +" → "Web Service"
2. Conecta tu repositorio de GitHub
3. Render detectará automáticamente el `render.yaml`

### Paso 3: Configuración Automática
Render usará la configuración de `render.yaml`:
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn run:app --bind 0.0.0.0:$PORT`
- **Environment**: Python 3.11
- **Plan**: Free

### Paso 4: Variables de Entorno
Render generará automáticamente:
- `SECRET_KEY` - Clave secreta de Flask
- `JWT_SECRET_KEY` - Clave para tokens JWT
- `FLASK_ENV=production` - Modo producción

### Paso 5: Deploy
1. Click en "Create Web Service"
2. Render comenzará el build (puede tardar 5-10 minutos)
3. Verás los logs en tiempo real

## ⚠️ Problemas Comunes

### Error: "divipola.csv not found"
**Solución**: Asegúrate de que el archivo CSV esté en el repositorio:
```bash
# Opción 1: En la raíz
cp "todos los datos/divipola.csv" divipola.csv

# Opción 2: Crear carpeta data
mkdir data
cp "todos los datos/divipola.csv" data/divipola.csv
```

### Error: "Permission denied: build.sh"
**Solución**: Dale permisos de ejecución:
```bash
git update-index --chmod=+x build.sh
git commit -m "Add execute permission to build.sh"
git push
```

### Error: "Database locked"
**Solución**: SQLite puede tener problemas en producción. Considera usar PostgreSQL:
1. En Render, agrega un PostgreSQL database
2. Render creará automáticamente `DATABASE_URL`
3. El código ya está preparado para usar PostgreSQL

## 🔄 Actualizar la Aplicación

Cada vez que hagas push a GitHub, Render desplegará automáticamente:
```bash
git add .
git commit -m "Descripción de cambios"
git push
```

## 📊 Monitoreo

### Ver logs en tiempo real:
1. Ve a tu servicio en Render
2. Click en "Logs"
3. Verás todos los logs de la aplicación

### Verificar estado:
- **URL**: Render te dará una URL como `https://tu-app.onrender.com`
- **Health Check**: Visita `/` para verificar que funciona

## 🗄️ Base de Datos

### SQLite (Actual)
- ✅ Fácil de configurar
- ⚠️ Los datos se pierden al redesplegar
- ⚠️ No recomendado para producción

### PostgreSQL (Recomendado)
1. En Render: "New +" → "PostgreSQL"
2. Conecta el database a tu web service
3. Render configurará `DATABASE_URL` automáticamente
4. El código ya maneja la conversión `postgres://` → `postgresql://`

## 🔐 Seguridad

### Cambiar contraseñas de usuarios de prueba:
Edita `scripts/create_test_users.py` antes del deploy:
```python
'password': 'TU_CONTRASEÑA_SEGURA_AQUI'
```

### Variables de entorno sensibles:
No incluyas en el código:
- Contraseñas
- API keys
- Tokens
Usa las variables de entorno de Render.

## 📱 Acceder a la Aplicación

Una vez desplegada:
1. Render te dará una URL: `https://testigos-electorales.onrender.com`
2. Accede al login: `https://testigos-electorales.onrender.com/`
3. Usa los usuarios de prueba creados

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs en Render
2. Verifica que todos los archivos estén en GitHub
3. Asegúrate de que `build.sh` tenga permisos de ejecución
4. Consulta la documentación de Render: https://render.com/docs

## ✅ Checklist Final

Antes de hacer deploy:
- [ ] Código subido a GitHub
- [ ] `divipola.csv` incluido en el repositorio
- [ ] `build.sh` tiene permisos de ejecución
- [ ] Contraseñas de prueba cambiadas (opcional)
- [ ] `.gitignore` configurado correctamente
- [ ] `requirements.txt` actualizado

¡Listo para desplegar! 🚀
