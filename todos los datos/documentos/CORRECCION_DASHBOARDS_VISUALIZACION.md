# Corrección de Dashboards - Problemas de Visualización

## ❌ Problema Identificado

Los dashboards (coordinador municipal, etc.) tienen errores de visualización porque intentan cargar archivos CSS/JS que no existen:

### Archivos que Fallan (404)
```
❌ /static/css/bootstrap.min.css
❌ /static/css/bootstrap-icons.css  
❌ /static/css/dashboard.css
❌ /static/js/bootstrap.bundle.min.js
❌ /static/js/chart.min.js
```

## ✅ Solución

Los dashboards deben usar el template `base.html` que ya tiene configurados correctamente los CDN de Bootstrap y Bootstrap Icons.

### Opción 1: Usar Template Base (RECOMENDADO)

Actualizar cada dashboard para extender de `base.html`:

```html
{% extends "base.html" %}

{% block title %}Dashboard Coordinador Municipal{% endblock %}

{% block extra_css %}
<style>
    /* Estilos personalizados aquí */
</style>
{% endblock %}

{% block content %}
    <!-- Contenido del dashboard -->
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/coordinador-municipal.js') }}"></script>
{% endblock %}
```

### Opción 2: Actualizar Enlaces a CDN

Si no se puede usar `base.html`, actualizar los enlaces en cada dashboard:

```html
<!-- Bootstrap CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Bootstrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- jQuery (si es necesario) -->
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
```

## 📝 Dashboards que Necesitan Corrección

1. `frontend/templates/coordinador/municipal.html`
2. `frontend/templates/coordinador/puesto.html`
3. `frontend/templates/coordinador/departamental.html`
4. `frontend/templates/admin/dashboard.html`
5. `frontend/templates/auditor/dashboard.html`
6. Cualquier otro dashboard que no use `base.html`

## 🔧 Ejemplo de Corrección

### Antes (municipal.html):
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Coordinador Municipal</title>
    <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/bootstrap-icons.css">
    ...
</head>
<body>
    <!-- Contenido -->
</body>
</html>
```

### Después (usando base.html):
```html
{% extends "base.html" %}

{% block title %}Dashboard Coordinador Municipal{% endblock %}

{% block extra_css %}
<style>
    .badge-status {
        font-size: 0.75rem;
        padding: 0.25rem 0.5rem;
    }
    /* ... más estilos ... */
</style>
{% endblock %}

{% block content %}
    <nav class="navbar navbar-dark bg-primary">
        <!-- Navbar content -->
    </nav>
    
    <!-- Dashboard content -->
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/coordinador-municipal.js') }}"></script>
{% endblock %}
```

## ✅ Ventajas de Usar base.html

1. **CDN configurados**: Bootstrap y Bootstrap Icons ya están cargados
2. **Consistencia**: Todos los dashboards usan los mismos estilos
3. **Mantenimiento**: Un solo lugar para actualizar versiones
4. **Performance**: Los CDN son más rápidos
5. **Scripts comunes**: api-client.js, utils.js ya están cargados

## 🚀 Pasos para Corregir

### 1. Identificar Dashboards Problemáticos
```bash
# Buscar archivos que no usan base.html
grep -L "extends.*base.html" frontend/templates/**/*.html
```

### 2. Para Cada Dashboard:

a. **Hacer backup**:
```bash
cp frontend/templates/coordinador/municipal.html frontend/templates/coordinador/municipal.html.bak
```

b. **Actualizar para usar base.html**:
- Agregar `{% extends "base.html" %}`
- Mover estilos a `{% block extra_css %}`
- Mover contenido a `{% block content %}`
- Mover scripts a `{% block extra_js %}`

c. **Eliminar enlaces a archivos locales**:
- Quitar `/static/css/bootstrap.min.css`
- Quitar `/static/css/bootstrap-icons.css`
- Quitar `/static/js/bootstrap.bundle.min.js`

### 3. Verificar
```bash
# Iniciar aplicación
python run.py

# Abrir en navegador
http://127.0.0.1:5000/coordinador/municipal

# Verificar en F12 → Network que no hay errores 404
```

## 📋 Checklist de Verificación

Para cada dashboard corregido:

- [ ] Extiende de `base.html`
- [ ] No tiene enlaces a `/static/css/bootstrap.min.css`
- [ ] No tiene enlaces a `/static/css/bootstrap-icons.css`
- [ ] Los estilos personalizados están en `{% block extra_css %}`
- [ ] Los scripts personalizados están en `{% block extra_js %}`
- [ ] No hay errores 404 en F12 → Network
- [ ] El dashboard se ve correctamente
- [ ] Los botones funcionan
- [ ] Los iconos se muestran

## 🎯 Prioridad de Corrección

1. **Alta**: Dashboards que los usuarios usan frecuentemente
   - Testigo Electoral
   - Coordinador de Puesto
   - Coordinador Municipal

2. **Media**: Dashboards administrativos
   - Admin Municipal
   - Admin Departamental
   - Coordinador Departamental

3. **Baja**: Dashboards especiales
   - Auditor Electoral
   - Super Admin (ya usa base.html)

## 💡 Nota Importante

El archivo `base.html` ya tiene configurado correctamente:
- Bootstrap 5.3.0 desde CDN
- Bootstrap Icons 1.11.0 desde CDN
- jQuery 3.7.1 desde CDN
- api-client.js
- utils.js
- sync-manager.js

Por lo tanto, cualquier dashboard que extienda de `base.html` automáticamente tendrá acceso a todos estos recursos.

---

**Última actualización**: 2025-11-16 20:15:00  
**Estado**: 📝 DOCUMENTADO - Pendiente de implementación
**Prioridad**: 🔴 ALTA
