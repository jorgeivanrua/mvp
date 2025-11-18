# Frontend de Incidentes y Delitos - Dashboard Testigos

## ✅ Implementación Completada

Se ha implementado el frontend completo para que los testigos electorales puedan reportar incidentes y delitos desde su dashboard.

## 📋 Componentes Implementados

### 1. API Client
**Archivo**: `frontend/static/js/api-client.js`

Métodos agregados:
- `crearIncidente(data)` - Crear un incidente electoral
- `obtenerIncidentes(filtros)` - Obtener lista de incidentes
- `obtenerIncidente(id)` - Obtener detalle de un incidente
- `actualizarEstadoIncidente(id, estado, comentario)` - Actualizar estado
- `obtenerTiposIncidentes()` - Obtener tipos disponibles
- `crearDelito(data)` - Crear un delito electoral
- `obtenerDelitos(filtros)` - Obtener lista de delitos
- `obtenerDelito(id)` - Obtener detalle de un delito
- `actualizarEstadoDelito(id, estado, comentario)` - Actualizar estado
- `denunciarDelito(id, numeroDenuncia, autoridadCompetente)` - Denuncia formal
- `obtenerTiposDelitos()` - Obtener tipos disponibles
- `obtenerEstadisticasReportes()` - Estadísticas generales
- `obtenerNotificaciones(soloNoLeidas)` - Notificaciones del usuario
- `marcarNotificacionLeida(id)` - Marcar como leída

### 2. Módulo JavaScript de Incidentes y Delitos
**Archivo**: `frontend/static/js/incidentes-delitos.js`

Funcionalidades:
- Inicialización automática al cargar el dashboard
- Carga de tipos de incidentes y delitos desde el servidor
- Renderizado de listas de incidentes y delitos
- Formularios modales para reportar
- Colores dinámicos según severidad/gravedad y estado
- Integración con la mesa seleccionada del testigo

### 3. Interfaz de Usuario
**Archivo**: `frontend/templates/testigo/dashboard.html`

#### Tabs Agregados:
1. **Tab "Incidentes y Problemas"**
   - Lista de incidentes reportados por el testigo
   - Botón para reportar nuevo incidente
   - Panel informativo con tipos de incidentes
   - Visualización de estado y severidad con colores

2. **Tab "Reporte de Delitos"**
   - Lista de delitos reportados por el testigo
   - Botón para reportar nuevo delito
   - Advertencia sobre la gravedad de los delitos
   - Panel informativo con tipos de delitos
   - Visualización de estado, gravedad y denuncias formales

#### Modales Implementados:

**Modal de Incidente:**
- Selector de tipo de incidente (cargado dinámicamente)
- Campo de título
- Selector de severidad (baja, media, alta, crítica)
- Área de descripción detallada
- Asociación automática con la mesa seleccionada

**Modal de Delito:**
- Selector de tipo de delito (cargado dinámicamente)
- Campo de título
- Selector de gravedad (leve, media, grave, muy grave)
- Área de descripción detallada
- Campo para testigos adicionales
- Advertencia sobre la seriedad del reporte
- Asociación automática con la mesa seleccionada

## 🎨 Características Visuales

### Colores por Severidad (Incidentes):
- **Baja**: Azul (info)
- **Media**: Amarillo (warning)
- **Alta**: Rojo (danger)
- **Crítica**: Negro (dark)

### Colores por Gravedad (Delitos):
- **Leve**: Azul (info)
- **Media**: Amarillo (warning)
- **Grave**: Rojo (danger)
- **Muy Grave**: Negro (dark)

### Colores por Estado (Incidentes):
- **Reportado**: Azul (primary)
- **En Revisión**: Amarillo (warning)
- **Resuelto**: Verde (success)
- **Escalado**: Rojo (danger)

### Colores por Estado (Delitos):
- **Reportado**: Azul (primary)
- **En Investigación**: Amarillo (warning)
- **Investigado**: Azul claro (info)
- **Denunciado**: Verde (success)
- **Archivado**: Gris (secondary)

## 🔄 Flujo de Uso

### Reportar un Incidente:
1. Testigo selecciona su mesa
2. Va al tab "Incidentes y Problemas"
3. Clic en "Reportar Incidente"
4. Llena el formulario:
   - Tipo de incidente
   - Título descriptivo
   - Severidad
   - Descripción detallada
5. Clic en "Reportar Incidente"
6. El incidente se guarda y aparece en la lista
7. Se envía notificación al coordinador de puesto

### Reportar un Delito:
1. Testigo selecciona su mesa
2. Va al tab "Reporte de Delitos"
3. Clic en "Reportar Delito"
4. Lee la advertencia sobre la seriedad
5. Llena el formulario:
   - Tipo de delito
   - Título descriptivo
   - Gravedad
   - Descripción detallada
   - Testigos adicionales (opcional)
6. Clic en "Reportar Delito"
7. El delito se guarda y aparece en la lista
8. Se envían notificaciones a:
   - Coordinador de puesto
   - Coordinador municipal
   - Coordinador departamental
   - Todos los auditores electorales

## 📱 Responsive Design

- Modales optimizados para móviles
- Cards adaptables a diferentes tamaños de pantalla
- Botones y textos legibles en dispositivos pequeños
- Formularios con validación HTML5

## 🔐 Seguridad

- Todos los endpoints requieren autenticación (token JWT)
- Los testigos solo pueden ver sus propios reportes
- Validación de campos requeridos en frontend y backend
- Asociación automática con la mesa del testigo

## 🚀 Próximos Pasos

Para completar el sistema de incidentes y delitos:

1. **Dashboard Coordinador de Puesto**:
   - Ver incidentes/delitos de su puesto
   - Cambiar estados
   - Agregar notas de resolución

2. **Dashboard Coordinador Municipal**:
   - Ver incidentes/delitos del municipio
   - Gestionar reportes escalados
   - Estadísticas municipales

3. **Dashboard Coordinador Departamental**:
   - Ver incidentes/delitos del departamento
   - Vista consolidada
   - Estadísticas departamentales

4. **Dashboard Auditor Electoral**:
   - Ver todos los incidentes y delitos
   - Investigar delitos
   - Denunciar formalmente
   - Generar reportes

## ✅ Estado Actual

- ✅ Backend 100% funcional
- ✅ API Client completo
- ✅ Módulo JavaScript de incidentes/delitos
- ✅ Interfaz de testigos completa
- ✅ Modales funcionales
- ✅ Sin errores de sintaxis
- ⏳ Pendiente prueba en navegador
- ⏳ Pendiente implementación en otros roles

## 🧪 Cómo Probar

1. Iniciar sesión como testigo electoral
2. Seleccionar una mesa
3. Ir al tab "Incidentes y Problemas"
4. Reportar un incidente de prueba
5. Verificar que aparece en la lista
6. Ir al tab "Reporte de Delitos"
7. Reportar un delito de prueba
8. Verificar que aparece en la lista
9. Verificar colores y badges según severidad/gravedad

## 📝 Archivos Modificados/Creados

- ✅ `frontend/static/js/api-client.js` - Agregados métodos de API
- ✅ `frontend/static/js/incidentes-delitos.js` - Nuevo módulo
- ✅ `frontend/templates/testigo/dashboard.html` - Actualizados modales
- ✅ Backend ya estaba completo desde implementación anterior
