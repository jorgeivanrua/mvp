# Implementación: Fotos Múltiples para Formularios E-14

## Resumen

Se ha implementado un sistema completo para que los testigos puedan tomar y guardar múltiples fotos del formulario E-14, y que los coordinadores de puesto puedan ver estas fotos una por una para verificar y validar.

## Funcionalidades Implementadas

### Para Testigos Electorales:
- ✅ Subir múltiples fotos por formulario E-14
- ✅ Navegación entre fotos (anterior/siguiente)
- ✅ Establecer foto principal
- ✅ Eliminar fotos propias
- ✅ Agregar descripción a cada foto
- ✅ Reordenar fotos por importancia

### Para Coordinadores de Puesto:
- ✅ Ver todas las fotos de un formulario
- ✅ Navegación individual foto por foto
- ✅ Validar o rechazar fotos individualmente
- ✅ Validación masiva de todas las fotos
- ✅ Agregar comentarios de validación
- ✅ Ver estado de validación de cada foto

## Archivos Creados

### Backend:

1. **`backend/models/formulario_fotos.py`**
   - Modelo para almacenar múltiples fotos por formulario
   - Campos: URL, hash, tamaño, orden, validación, etc.

2. **`backend/services/formulario_fotos_service.py`**
   - Lógica de negocio para manejo de fotos
   - Validaciones, subida, eliminación, validación

3. **`backend/routes/formulario_fotos.py`**
   - Endpoints REST para todas las operaciones de fotos
   - Rutas: subir, obtener, eliminar, validar, reordenar

4. **`backend/migrations/add_formulario_fotos_table.py`**
   - Migración para crear tabla de fotos
   - Migra fotos existentes desde campo `imagen_url`

### Frontend:

5. **`frontend/static/js/formulario-fotos.js`**
   - Clase JavaScript para manejo completo de fotos
   - Navegación, subida, validación, interfaz

6. **`frontend/templates/components/formulario-fotos.html`**
   - Componente HTML reutilizable para visor de fotos
   - Controles de navegación y validación

7. **`frontend/templates/testigo/formulario-fotos.html`**
   - Página completa para gestión de fotos
   - Integra el componente con información del formulario

8. **`frontend/templates/components/boton-fotos-formulario.html`**
   - Botón para acceder a fotos desde dashboard
   - Versiones simple y como card

### Scripts:

9. **`scripts/aplicar_migracion_fotos.py`**
   - Script para aplicar la migración de fotos

## API Endpoints

### Fotos de Formularios (`/api/formulario-fotos/`)

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| POST | `/subir/{formulario_id}` | Subir nueva foto | Testigo, Coordinadores |
| GET | `/formulario/{formulario_id}` | Obtener todas las fotos | Todos |
| DELETE | `/eliminar/{foto_id}` | Eliminar foto | Testigo, Coordinadores |
| POST | `/validar/{foto_id}` | Validar/rechazar foto | Coordinadores |
| POST | `/principal/{foto_id}` | Establecer foto principal | Testigo, Coordinadores |
| POST | `/reordenar/{formulario_id}` | Reordenar fotos | Testigo, Coordinadores |
| GET | `/info/{formulario_id}` | Info del formulario | Todos |
| POST | `/validacion-masiva/{formulario_id}` | Validar todas las fotos | Coordinadores |

## Instalación y Configuración

### 1. Aplicar Migración

```bash
# Ejecutar migración
python scripts/aplicar_migracion_fotos.py
```

### 2. Configurar Directorio de Uploads

Asegúrese de que el directorio `uploads/formularios/` tenga permisos de escritura:

```bash
mkdir -p uploads/formularios
chmod 755 uploads/formularios
```

### 3. Integrar en Dashboard

Para integrar el botón de fotos en el dashboard del testigo:

```html
<!-- En el template del dashboard -->
{% set formulario_id = formulario.id if formulario else None %}
{% set total_fotos = formulario.total_fotos if formulario else 0 %}
{% include 'components/boton-fotos-formulario.html' %}
```

### 4. Página Completa de Fotos

Para mostrar la página completa de gestión de fotos:

```html
<!-- Enlace desde cualquier parte -->
<a href="/formulario/{{ formulario.id }}/fotos" target="_blank">
    Ver Fotos del Formulario
</a>
```

## Uso del Componente

### Inicialización Básica

```javascript
// Inicializar componente de fotos
const formularioFotos = inicializarFormularioFotos(formularioId, esCoordinador);
```

### Integración en Página Existente

```html
<!-- Incluir CSS y JS -->
<script src="{{ url_for('static', filename='js/formulario-fotos.js') }}"></script>

<!-- Incluir componente -->
{% include 'components/formulario-fotos.html' %}

<!-- Inicializar -->
<script>
window.formularioFotos = inicializarFormularioFotos({{ formulario.id }}, false);
</script>
```

## Validaciones y Seguridad

### Validaciones de Archivo:
- ✅ Tipos permitidos: JPG, PNG, WebP
- ✅ Tamaño máximo: 10MB
- ✅ Hash SHA-256 para integridad
- ✅ Detección de duplicados

### Seguridad:
- ✅ Autenticación JWT requerida
- ✅ Validación de roles por endpoint
- ✅ Solo el creador o coordinadores pueden eliminar
- ✅ Solo coordinadores pueden validar

## Flujo de Trabajo

### Para Testigos:

1. **Crear Formulario E-14**
2. **Acceder a "Gestionar Fotos"**
3. **Subir múltiples fotos del formulario**
4. **Navegar y organizar fotos**
5. **Establecer foto principal**
6. **Enviar formulario para validación**

### Para Coordinadores:

1. **Recibir formulario con fotos**
2. **Abrir página de fotos del formulario**
3. **Revisar cada foto individualmente**
4. **Validar fotos correctas**
5. **Rechazar fotos con problemas**
6. **Usar validación masiva si todas están bien**

## Características Técnicas

### Almacenamiento:
- Archivos físicos en `/uploads/formularios/`
- Metadatos en base de datos
- URLs relativas para portabilidad

### Rendimiento:
- Carga lazy de imágenes
- Miniaturas para navegación rápida
- Caché de consultas frecuentes

### Compatibilidad:
- Responsive design para móviles
- Soporte para touch en navegación
- Fallbacks para navegadores antiguos

## Próximas Mejoras

### Funcionalidades Futuras:
- [ ] Compresión automática de imágenes
- [ ] Marcas de agua con información de mesa
- [ ] Exportación de fotos en PDF
- [ ] Sincronización offline
- [ ] Reconocimiento OCR de números

### Optimizaciones:
- [ ] CDN para servir imágenes
- [ ] Thumbnails automáticos
- [ ] Carga progresiva
- [ ] Backup automático en la nube

## Soporte y Mantenimiento

### Logs y Monitoreo:
- Errores de subida se registran en logs
- Métricas de uso de almacenamiento
- Alertas por fallos de validación

### Backup:
- Incluir directorio `uploads/` en backups
- Verificar integridad con hashes SHA-256
- Restauración automática de metadatos

## Conclusión

El sistema de fotos múltiples proporciona una solución completa y robusta para la documentación visual de formularios E-14, mejorando significativamente la transparencia y verificabilidad del proceso electoral.