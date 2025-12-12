# Implementación: Evidencias Fotográficas Múltiples para Incidentes y Delitos

## Resumen

Se ha implementado un sistema completo de evidencias fotográficas múltiples para incidentes y delitos electorales, permitiendo a los usuarios subir, organizar y validar múltiples fotos como evidencia de los reportes realizados.

## Funcionalidades Implementadas

### Para Reportadores (Testigos, Coordinadores):
- ✅ Subir múltiples fotos como evidencia
- ✅ Categorizar evidencias por tipo (personas, documentos, ubicación, etc.)
- ✅ Clasificar por tipo de evidencia (directa, indirecta, contextual)
- ✅ Asignar niveles de relevancia (baja, media, alta, crítica)
- ✅ Agregar descripciones detalladas a cada evidencia
- ✅ Navegación entre evidencias fotográficas
- ✅ Establecer evidencia principal
- ✅ Eliminar evidencias propias

### Para Coordinadores y Auditores:
- ✅ Revisar todas las evidencias de un reporte
- ✅ Validar o rechazar evidencias individualmente
- ✅ Validación masiva de todas las evidencias
- ✅ Agregar comentarios de validación
- ✅ Ver metadatos de captura y geolocalización
- ✅ Estadísticas de evidencias por reporte

## Archivos Creados

### Backend:

1. **`backend/models/incidentes_delitos_fotos.py`**
   - Modelo para almacenar múltiples evidencias fotográficas
   - Campos: categoría, tipo de evidencia, relevancia, validación, metadatos

2. **`backend/services/incidentes_delitos_fotos_service.py`**
   - Lógica de negocio para manejo de evidencias
   - Validaciones, subida, eliminación, validación, metadatos

3. **`backend/routes/incidentes_delitos_fotos.py`**
   - Endpoints REST para todas las operaciones de evidencias
   - Rutas: subir, obtener, eliminar, validar, metadatos

4. **`backend/migrations/add_incidentes_delitos_fotos_table.py`**
   - Migración para crear tabla de evidencias fotográficas
   - Migra evidencias existentes desde campo `evidencia_url`

### Frontend:

5. **`frontend/static/js/incidentes-delitos-fotos.js`**
   - Clase JavaScript para manejo completo de evidencias
   - Navegación, subida, validación, categorización

6. **`frontend/templates/components/incidentes-delitos-fotos.html`**
   - Componente HTML reutilizable para visor de evidencias
   - Controles avanzados de categorización y validación

7. **`frontend/templates/reportes/evidencias-fotograficas.html`**
   - Página completa para gestión de evidencias fotográficas
   - Integra el componente con información del reporte

8. **`frontend/templates/components/boton-evidencias-fotograficas.html`**
   - Botón para acceder a evidencias desde dashboards
   - Versiones simple, card e inline

### Scripts:

9. **`scripts/aplicar_migracion_evidencias_fotos.py`**
   - Script para aplicar la migración de evidencias

## API Endpoints

### Evidencias Fotográficas (`/api/evidencias-fotos/`)

| Método | Endpoint | Descripción | Roles |
|--------|----------|-------------|-------|
| POST | `/subir/{tipo_reporte}/{reporte_id}` | Subir nueva evidencia | Testigos, Coordinadores, Auditores |
| GET | `/{tipo_reporte}/{reporte_id}` | Obtener todas las evidencias | Todos |
| DELETE | `/eliminar/{foto_id}` | Eliminar evidencia | Testigos, Coordinadores, Auditores |
| POST | `/validar/{foto_id}` | Validar/rechazar evidencia | Coordinadores, Auditores |
| POST | `/principal/{foto_id}` | Establecer evidencia principal | Testigos, Coordinadores, Auditores |
| PUT | `/metadatos/{foto_id}` | Actualizar metadatos | Testigos, Coordinadores, Auditores |
| GET | `/info/{tipo_reporte}/{reporte_id}` | Info del reporte | Todos |
| POST | `/validacion-masiva/{tipo_reporte}/{reporte_id}` | Validar todas las evidencias | Coordinadores, Auditores |
| GET | `/categorias` | Obtener categorías disponibles | Todos |

## Categorías de Evidencia

### Tipos de Categoría:
- **General**: Evidencia general del hecho
- **Personas**: Personas involucradas en el incidente/delito
- **Documentos**: Documentos relevantes (actas, formularios, etc.)
- **Ubicación**: Evidencia del lugar donde ocurrió el hecho
- **Material Electoral**: Material electoral involucrado
- **Daños**: Daños o alteraciones observadas
- **Multitud**: Multitudes o aglomeraciones
- **Autoridades**: Presencia de autoridades
- **Otros**: Otras evidencias no categorizadas

### Tipos de Evidencia:
- **Directa**: Evidencia directa del hecho reportado
- **Indirecta**: Evidencia indirecta o circunstancial
- **Contextual**: Evidencia de contexto o ambiente

### Niveles de Relevancia:
- **Baja**: Relevancia baja para el caso
- **Media**: Relevancia media
- **Alta**: Alta relevancia para el caso
- **Crítica**: Relevancia crítica (especialmente para delitos)

## Instalación y Configuración

### 1. Aplicar Migración

```bash
# Ejecutar migración
python scripts/aplicar_migracion_evidencias_fotos.py
```

### 2. Configurar Directorio de Uploads

Asegúrese de que el directorio `uploads/evidencias/` tenga permisos de escritura:

```bash
mkdir -p uploads/evidencias
chmod 755 uploads/evidencias
```

### 3. Integrar en Dashboard

Para integrar el botón de evidencias en dashboards:

```html
<!-- En el template del dashboard -->
{% set reporte_id = incidente.id if incidente else delito.id %}
{% set tipo_reporte = 'incidente' if incidente else 'delito' %}
{% set total_evidencias = reporte.total_fotos if reporte else 0 %}
{% include 'components/boton-evidencias-fotograficas.html' %}
```

### 4. Página Completa de Evidencias

Para mostrar la página completa de gestión de evidencias:

```html
<!-- Enlace desde cualquier parte -->
<a href="/{{ tipo_reporte }}/{{ reporte.id }}/evidencias" target="_blank">
    Ver Evidencias Fotográficas
</a>
```

## Uso del Componente

### Inicialización Básica

```javascript
// Inicializar componente de evidencias
const evidenciasFotos = inicializarIncidentesDelitosFotos(tipoReporte, reporteId, esCoordinador);
```

### Integración en Página Existente

```html
<!-- Incluir CSS y JS -->
<script src="{{ url_for('static', filename='js/incidentes-delitos-fotos.js') }}"></script>

<!-- Incluir componente -->
{% include 'components/incidentes-delitos-fotos.html' %}

<!-- Inicializar -->
<script>
window.evidenciasFotos = inicializarIncidentesDelitosFotos('incidente', {{ reporte.id }}, false);
</script>
```

## Validaciones y Seguridad

### Validaciones de Archivo:
- ✅ Tipos permitidos: JPG, PNG, WebP
- ✅ Tamaño máximo: 15MB (mayor que formularios por ser evidencias)
- ✅ Hash SHA-256 para integridad
- ✅ Detección de duplicados por reporte

### Seguridad:
- ✅ Autenticación JWT requerida
- ✅ Validación de roles por endpoint
- ✅ Solo el creador o coordinadores/auditores pueden eliminar
- ✅ Solo coordinadores y auditores pueden validar
- ✅ Cadena de custodia con metadatos de captura

## Flujo de Trabajo

### Para Reportadores:

1. **Crear Incidente o Delito Electoral**
2. **Acceder a "Evidencias Fotográficas"**
3. **Subir múltiples fotos como evidencia**
4. **Categorizar cada evidencia apropiadamente**
5. **Asignar niveles de relevancia**
6. **Agregar descripciones detalladas**
7. **Establecer evidencia principal**
8. **Enviar reporte para revisión**

### Para Coordinadores/Auditores:

1. **Recibir reporte con evidencias**
2. **Abrir página de evidencias fotográficas**
3. **Revisar cada evidencia individualmente**
4. **Verificar categorización y relevancia**
5. **Validar evidencias auténticas y relevantes**
6. **Rechazar evidencias problemáticas con comentarios**
7. **Usar validación masiva si todas están correctas**

## Características Técnicas

### Almacenamiento:
- Archivos físicos en `/uploads/evidencias/`
- Metadatos completos en base de datos
- URLs relativas para portabilidad
- Organización por tipo de reporte

### Metadatos Capturados:
- Información de archivo (tamaño, tipo, resolución)
- Geolocalización de captura (si disponible)
- Fecha y hora de captura
- Dispositivo utilizado
- Hash de integridad

### Rendimiento:
- Carga lazy de imágenes grandes
- Miniaturas para navegación rápida
- Estadísticas agregadas por reporte
- Caché de consultas frecuentes

### Compatibilidad:
- Responsive design para móviles
- Soporte para touch en navegación
- Fallbacks para navegadores antiguos
- Accesibilidad mejorada

## Diferencias con Fotos de Formularios

### Características Específicas para Evidencias:
- **Categorización avanzada** por tipo de evidencia
- **Niveles de relevancia** para priorización
- **Metadatos de captura** para cadena de custodia
- **Tamaño máximo mayor** (15MB vs 10MB)
- **Validación por coordinadores y auditores** (no solo coordinadores)
- **Clasificación legal** para delitos electorales

### Flujo de Validación:
- Evidencias de **incidentes**: Validación por coordinadores
- Evidencias de **delitos**: Validación por coordinadores y auditores
- **Cadena de custodia** documentada
- **Comentarios obligatorios** para rechazos

## Próximas Mejoras

### Funcionalidades Futuras:
- [ ] Marcas de agua automáticas con información del reporte
- [ ] Exportación de evidencias en formato legal
- [ ] Firma digital de evidencias
- [ ] Integración con sistemas de denuncia formal
- [ ] Reconocimiento automático de contenido

### Optimizaciones:
- [ ] Compresión inteligente por relevancia
- [ ] Backup automático en múltiples ubicaciones
- [ ] Sincronización con autoridades competentes
- [ ] Análisis automático de calidad de evidencias

## Aspectos Legales

### Para Delitos Electorales:
- **Cadena de custodia** documentada automáticamente
- **Metadatos forenses** preservados
- **Integridad verificable** con hashes SHA-256
- **Trazabilidad completa** de validaciones
- **Exportación en formatos legales** (futuro)

### Consideraciones de Privacidad:
- Evidencias solo visibles para roles autorizados
- Eliminación segura de archivos físicos
- Anonimización opcional de personas en fotos
- Cumplimiento con regulaciones de protección de datos

## Soporte y Mantenimiento

### Logs y Monitoreo:
- Registro de todas las operaciones de evidencias
- Alertas por evidencias críticas sin validar
- Métricas de uso por tipo de reporte
- Monitoreo de integridad de archivos

### Backup y Recuperación:
- Backup automático de evidencias críticas
- Verificación periódica de integridad
- Restauración con preservación de metadatos
- Redundancia para evidencias de delitos

## Conclusión

El sistema de evidencias fotográficas múltiples proporciona una solución robusta y legalmente sólida para la documentación visual de incidentes y delitos electorales, mejorando significativamente la capacidad de investigación y la transparencia del proceso electoral.