# 🚀 Configuración de Render - Guía Completa

## 📋 Configuración en Render Dashboard

### 1. Build Command
```bash
pip install -r requirements.txt
```

### 2. Pre-Deploy Command
```bash
python backend/scripts/load_complete_test_data.py
```

### 3. Start Command
```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

### 4. Environment Variables

Agregar estas variables en la sección "Environment":

```bash
FLASK_ENV=production
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_cambiar_esto
JWT_SECRET_KEY=otra_clave_secreta_para_jwt_cambiar_esto
DATABASE_URL=sqlite:///electoral.db
PYTHONUNBUFFERED=1
PORT=10000
```

---

## 🔧 Solución de Problemas Comunes

### Problema 1: CSS no carga (502 Bad Gateway)

**Causa:** Gunicorn no está configurado correctamente para servir archivos estáticos.

**Solución:** Asegúrate de que el Start Command incluya el bind correcto:
```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

### Problema 2: Base de datos vacía

**Causa:** La BD no se inicializa en el primer despliegue.

**Solución:** Usar el Pre-Deploy Command:
```bash
python backend/scripts/load_complete_test_data.py
```

### Problema 3: Archivos estáticos no se encuentran

**Causa:** Las rutas de archivos estáticos no están configuradas correctamente.

**Solución:** Verificar que en `backend/app.py` esté:
```python
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
```

---

## 📦 Estructura de Archivos Requerida

```
proyecto/
├── backend/
│   ├── app.py              # Factory de Flask
│   ├── config.py           # Configuración
│   └── scripts/
│       └── load_complete_test_data.py
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   └── mobile-responsive.css
│   │   └── js/
│   └── templates/
├── run.py                  # Punto de entrada
├── requirements.txt        # Dependencias
└── electoral.db           # Base de datos (se crea automáticamente)
```

---

## ✅ Verificación Post-Despliegue

### 1. Verificar que la app esté corriendo
```
https://tu-app.onrender.com
```

### 2. Verificar logs en Render
- Ir a "Logs" en el dashboard
- Buscar mensajes de error
- Verificar que Gunicorn haya iniciado

### 3. Verificar archivos estáticos
```
https://tu-app.onrender.com/static/css/main.css
https://tu-app.onrender.com/static/css/mobile-responsive.css
```

### 4. Verificar base de datos
- Intentar hacer login con usuario de prueba
- Verificar que los departamentos se carguen

---

## 🔑 Credenciales de Prueba

Después de ejecutar `load_complete_test_data.py`:

### Super Admin
- Usuario: `admin`
- Contraseña: `admin123`

### Testigo Electoral
- Usuario: `testigo1`
- Contraseña: `test123`

### Coordinador Puesto
- Usuario: `coord_puesto1`
- Contraseña: `test123`

---

## 🐛 Debugging

### Ver logs en tiempo real
En Render Dashboard → Logs → Ver logs en vivo

### Comandos útiles en Shell de Render
```bash
# Ver estructura de archivos
ls -la

# Ver contenido de requirements.txt
cat requirements.txt

# Verificar que gunicorn esté instalado
pip list | grep gunicorn

# Ver variables de entorno
env | grep FLASK

# Verificar base de datos
ls -la *.db

# Probar inicio manual
python run.py
```

---

## 📱 Optimizaciones Móviles

Los archivos CSS responsivos ya están incluidos:
- `frontend/static/css/mobile-responsive.css`
- Incluido automáticamente en `base.html`

---

## 🔄 Auto-Deploy

Render está configurado para desplegar automáticamente cuando haces push a GitHub:
1. Haces commit y push
2. Render detecta el cambio
3. Ejecuta Build Command
4. Ejecuta Pre-Deploy Command (si está configurado)
5. Ejecuta Start Command
6. App desplegada ✅

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Render
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que el Start Command sea correcto
4. Verifica que la base de datos se haya inicializado

---

## 🎯 Checklist de Configuración

- [ ] Build Command configurado
- [ ] Pre-Deploy Command configurado
- [ ] Start Command configurado
- [ ] Variables de entorno configuradas
- [ ] Auto-Deploy habilitado
- [ ] Base de datos inicializada
- [ ] CSS cargando correctamente
- [ ] Login funcionando
- [ ] Dashboards cargando
