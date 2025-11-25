# Implementation Plan - Dashboard Super Admin

## Overview

Este plan documenta la implementación del Dashboard del Super Admin. El sistema está 70% completado (18/25 tareas) con funcionalidades principales implementadas incluyendo gestión de usuarios, configuración electoral, personalización de fondos, y herramientas de administración.

## Tasks

- [x] 1. Crear estructura base del dashboard
  - Crear template HTML `frontend/templates/admin/super-admin-dashboard.html`
  - Implementar header con información del usuario
  - Crear navegación por pestañas (Usuarios, Configuración, Personalización, Herramientas)
  - Implementar diseño responsive
  - Agregar botón de cerrar sesión
  - _Requirements: 1.1, 19.1, 19.2, 20.1_

- [x] 2. Implementar estadísticas globales
  - Crear tarjetas de estadísticas en la parte superior
  - Mostrar total de usuarios por rol
  - Mostrar total de formularios E-14 por estado
  - Mostrar porcentaje de mesas con formularios validados
  - Mostrar actividad del sistema en últimas 24 horas
  - Actualizar estadísticas en tiempo real
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 3. Implementar gestión de usuarios
  - Crear template `frontend/templates/admin/gestion-usuarios.html`
  - Crear archivo `frontend/static/js/gestion-usuarios.js`
  - Implementar tabla de usuarios con filtros
  - Función `cargarUsuarios()` para listar usuarios
  - Función `crearUsuario()` con modal de creación
  - Función `editarUsuario()` con modal de edición
  - Función `desactivarUsuario()` con confirmación
  - Función `reactivarUsuario()` con confirmación
  - Función `resetearPassword()` con generación de contraseña temporal
  - Filtros por rol y estado
  - Búsqueda por nombre o email
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

- [x] 4. Implementar endpoints de gestión de usuarios
  - Crear archivo `backend/routes/gestion_usuarios.py`
  - Endpoint `GET /api/gestion-usuarios/usuarios` - Listar usuarios
  - Endpoint `POST /api/gestion-usuarios/usuarios` - Crear usuario
  - Endpoint `PUT /api/gestion-usuarios/usuarios/<id>` - Actualizar usuario
  - Endpoint `POST /api/gestion-usuarios/usuarios/<id>/desactivar` - Desactivar usuario
  - Endpoint `POST /api/gestion-usuarios/usuarios/<id>/reactivar` - Reactivar usuario
  - Endpoint `POST /api/gestion-usuarios/usuarios/<id>/reset-password` - Resetear contraseña
  - Validaciones de datos en backend
  - Registro en log de auditoría
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 20.3_

- [x] 5. Implementar configuración electoral
  - Crear template `frontend/templates/admin/configuracion.html`
  - Crear archivo `frontend/static/js/admin-configuracion.js`
  - Sección de tipos de elección con CRUD completo
  - Sección de partidos políticos con CRUD completo
  - Sección de candidatos con CRUD completo
  - Función `cargarTiposEleccion()` para listar tipos
  - Función `cargarPartidos()` para listar partidos
  - Función `cargarCandidatos()` para listar candidatos
  - Modales de creación y edición para cada entidad
  - Validación de códigos únicos
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4_

- [x] 6. Implementar endpoints de configuración electoral
  - Crear archivo `backend/routes/configuracion.py`
  - Endpoints para tipos de elección (GET, POST, PUT, DELETE)
  - Endpoints para partidos políticos (GET, POST, PUT, DELETE)
  - Endpoints para candidatos (GET, POST, PUT, DELETE)
  - Validación de códigos únicos
  - Aplicación inmediata de cambios en todo el sistema
  - Registro en log de auditoría
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 4.5, 20.2_

- [x] 7. Implementar personalización de fondos de login
  - Crear template `frontend/templates/admin/personalizacion-tab.html`
  - Crear archivo `frontend/static/js/personalizacion-sistema.js`
  - Crear archivo `frontend/static/css/personalizacion.css`
  - Modal para crear fondos con 3 tipos: gradientes, imágenes, colores sólidos
  - Preview en tiempo real del fondo
  - Grid de fondos actuales con acciones (activar, eliminar)
  - Grid de fondos predefinidos (7 fondos)
  - Función `crearFondo()` con validaciones
  - Función `activarFondo()` para cambiar fondo activo
  - Función `eliminarFondo()` con confirmación
  - Función `cargarFondos()` para listar fondos
  - Selector de colores para gradientes y colores sólidos
  - Selector de dirección para gradientes (6 opciones)
  - Subida de imágenes con validación de tipo y tamaño
  - _Requirements: 21.1, 21.2, 21.3, 21.4, 21.5, 21.6, 21.7, 21.8, 21.9, 21.10, 21.11, 21.12_

- [x] 8. Implementar modelos de personalización
  - Crear archivo `backend/models/configuracion_sistema.py`
  - Modelo `ConfiguracionSistema` con campos de configuración general
  - Modelo `FondoLogin` con campos: nombre, tipo, configuracion_json, activo, es_predefinido
  - Relación entre modelos
  - Métodos de validación
  - _Requirements: 21.1, 21.2, 21.3, 21.4_

- [x] 9. Implementar endpoints de personalización
  - Crear archivo `backend/routes/configuracion_sistema.py`
  - Endpoint `GET /api/config-sistema/fondos` - Listar fondos
  - Endpoint `GET /api/config-sistema/fondos/activo` - Obtener fondo activo (público)
  - Endpoint `POST /api/config-sistema/fondos` - Crear fondo
  - Endpoint `PUT /api/config-sistema/fondos/<id>/activar` - Activar fondo
  - Endpoint `DELETE /api/config-sistema/fondos/<id>` - Eliminar fondo
  - Endpoint `POST /api/config-sistema/fondos/upload` - Subir imagen
  - Validación de tipos de archivo (PNG, JPG, JPEG, GIF, WEBP)
  - Validación de tamaño máximo (5MB)
  - Sanitización de nombres de archivo con UUID
  - Almacenamiento en `frontend/static/uploads/fondos/`
  - _Requirements: 21.1, 21.7, 21.8, 21.9, 21.10, 21.11, 21.12_

- [x] 10. Crear fondos predefinidos
  - Crear migración para insertar 7 fondos predefinidos
  - Fondo 1: Bandera de Colombia (gradiente amarillo-azul-rojo)
  - Fondo 2: Azul Institucional (color sólido)
  - Fondo 3: Amarillo Vibrante (color sólido)
  - Fondo 4: Rojo Patriótico (color sólido)
  - Fondo 5: Azul Oscuro (color sólido)
  - Fondo 6: Gradiente Amanecer (naranja-rosa-morado)
  - Fondo 7: Gradiente Océano (azul-turquesa)
  - Marcar Bandera de Colombia como activo por defecto
  - _Requirements: 21.6_

- [x] 11. Integrar fondo activo en página de login
  - Modificar `frontend/templates/auth/login.html`
  - Cargar fondo activo al iniciar página
  - Función `cargarFondoActivo()` en JavaScript
  - Aplicar fondo según tipo (gradiente, imagen, color)
  - Manejo de errores si no hay fondo activo
  - _Requirements: 21.9_

- [x] 12. Implementar herramientas de administración
  - Crear archivo `backend/routes/admin_tools.py`
  - Endpoint `GET /api/admin-tools/health` - Estado de salud del sistema
  - Endpoint `POST /api/admin-tools/diagnostico` - Ejecutar diagnóstico
  - Endpoint `POST /api/admin-tools/limpiar-datos` - Limpiar datos antiguos
  - Endpoint `GET /api/admin-tools/storage` - Estadísticas de almacenamiento
  - Mostrar métricas de base de datos, memoria, CPU
  - Registro de operaciones en log de auditoría
  - _Requirements: 22.4, 22.5, 22.6, 22.7, 22.8_

- [x] 13. Implementar importación masiva de datos
  - Crear archivo `backend/routes/admin_data_import.py`
  - Endpoint `POST /api/admin-import/usuarios` - Importar usuarios desde CSV
  - Endpoint `POST /api/admin-import/ubicaciones` - Importar ubicaciones desde CSV
  - Validación de formato CSV
  - Validación de datos por fila
  - Reporte de errores por fila
  - Registro de importaciones en log de auditoría
  - _Requirements: 22.1, 22.2, 22.3, 22.8_

- [x] 14. Implementar gestión de campañas electorales
  - Agregar modelo `Campana` en `backend/models/configuracion_electoral.py`
  - Campos: nombre, fecha_inicio, fecha_fin, descripcion, activa
  - Relaciones con partidos, candidatos, tipos de elección
  - Endpoints CRUD para campañas
  - Validación de una sola campaña activa
  - Filtrado de formularios E-14 por campaña
  - _Requirements: 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7_

- [x] 15. Implementar monitoreo del sistema
  - Crear archivo `backend/routes/monitoreo.py`
  - Endpoint `GET /api/monitoreo/metricas` - Métricas de rendimiento
  - Endpoint `GET /api/monitoreo/usuarios-conectados` - Usuarios en línea
  - Endpoint `GET /api/monitoreo/requests` - Requests por minuto
  - Endpoint `GET /api/monitoreo/alertas` - Alertas del sistema
  - Mostrar tiempo de respuesta, uso de CPU, uso de memoria
  - Alertar cuando sistema está bajo alta carga
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 16. Implementar logs y auditoría
  - Crear modelo `AuditLog` en `backend/models/coordinador_municipal.py`
  - Campos: usuario_id, accion, detalles, timestamp, nivel_severidad
  - Endpoint `GET /api/admin/logs` - Consultar logs
  - Filtros por usuario, acción, fecha, severidad
  - Exportación de logs en CSV y JSON
  - Retención de logs por 90 días
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 20.1, 20.2, 20.3, 20.4, 20.5, 20.6_

- [x] 17. Implementar gestión de ubicaciones DIVIPOLA
  - Endpoints para crear departamentos, municipios, puestos, mesas
  - Endpoints para editar ubicaciones existentes
  - Validación de códigos DIVIPOLA únicos
  - Carga masiva desde CSV
  - Mantenimiento de integridad referencial
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 18. Implementar vista nacional de resultados
  - Endpoint `GET /api/super-admin/resultados-nacionales` - Consolidado nacional
  - Cálculo de votos por partido sumando todos los departamentos
  - Estadísticas nacionales: total votantes, participación, votos válidos
  - Navegación a cualquier departamento, municipio, puesto
  - Actualización en tiempo real
  - _Requirements: 6.1, 6.2, 6.4, 6.5, 6.6_

- [ ] 19. Implementar mapa de Colombia con resultados
  - Integrar librería de mapas (Leaflet o Google Maps)
  - Cargar mapa de Colombia con departamentos
  - Mostrar resultados por departamento con colores
  - Tooltip con información al pasar mouse
  - Click en departamento para ver detalles
  - _Requirements: 6.3_

- [ ] 20. Implementar gestión de permisos y roles
  - Endpoint `GET /api/admin/roles` - Listar roles
  - Endpoint `GET /api/admin/roles/<id>/permisos` - Ver permisos de rol
  - Endpoint `PUT /api/admin/roles/<id>/permisos` - Modificar permisos
  - Validación de seguridad en cambios de permisos
  - Aplicación inmediata de cambios
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 21. Implementar respaldos y recuperación
  - Endpoint `POST /api/admin/respaldos` - Crear respaldo manual
  - Endpoint `GET /api/admin/respaldos` - Listar respaldos
  - Endpoint `GET /api/admin/respaldos/<id>/descargar` - Descargar respaldo
  - Endpoint `POST /api/admin/respaldos/configurar` - Configurar respaldos automáticos
  - Alertas si respaldo falla
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 22. Implementar gestión de configuración del sistema
  - Endpoint `GET /api/admin/configuracion` - Obtener configuración
  - Endpoint `PUT /api/admin/configuracion` - Actualizar configuración
  - Parámetros: tiempo de sesión, tamaño máximo archivos, intentos login
  - Validación de valores
  - Aplicación sin reinicio
  - Historial de cambios
  - Revertir a valores anteriores
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 23. Implementar análisis de uso del sistema
  - Endpoint `GET /api/admin/analisis-uso` - Estadísticas de uso
  - Estadísticas por rol (logins, formularios, validaciones)
  - Horarios de mayor uso
  - Usuarios más activos y menos activos
  - Funcionalidades más utilizadas
  - Generación de reportes en PDF
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ] 24. Implementar gestión de notificaciones
  - Endpoint `POST /api/admin/notificaciones` - Enviar notificación
  - Endpoint `GET /api/admin/notificaciones` - Historial de notificaciones
  - Envío a usuarios específicos o grupos
  - Título, mensaje, nivel de prioridad
  - Programación de envío futuro
  - Ver qué usuarios han leído notificaciones
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ] 25. Implementar configuración de temas visuales
  - Agregar modelo `ConfiguracionTema` en `backend/models/configuracion_electoral.py`
  - Campos: nombre, color_primario, color_secundario, color_acento, rol, tipo_eleccion
  - Endpoints CRUD para temas
  - Asignación de temas a roles o tipos de elección
  - Preview de tema antes de aplicar
  - Validación de contraste para accesibilidad
  - Aplicación automática según rol de usuario
  - _Requirements: 24.1, 24.2, 24.3, 24.4, 24.5, 24.6_

## Estado Actual

✅ **Dashboard Super Admin 70% Funcional**

18 de 25 tareas completadas. El sistema tiene implementadas las funcionalidades principales de gestión de usuarios, configuración electoral, personalización de fondos, y herramientas de administración.

### Funcionalidades Implementadas

- ✅ **Gestión completa de usuarios**
  - Crear, editar, desactivar, reactivar usuarios
  - Resetear contraseñas
  - Filtros y búsqueda
  - Asignación de roles y ubicaciones
  - Registro en log de auditoría

- ✅ **Configuración electoral completa**
  - Gestión de tipos de elección
  - Gestión de partidos políticos
  - Gestión de candidatos
  - Validación de códigos únicos
  - Aplicación inmediata de cambios

- ✅ **Personalización de fondos de login**
  - 3 tipos de fondos: gradientes, imágenes, colores sólidos
  - 7 fondos predefinidos
  - Preview en tiempo real
  - Subida de imágenes con validación
  - Activación y eliminación de fondos
  - Carga dinámica en página de login

- ✅ **Herramientas de administración**
  - Estado de salud del sistema
  - Diagnóstico del sistema
  - Limpieza de datos antiguos
  - Estadísticas de almacenamiento
  - Importación masiva de usuarios y ubicaciones

- ✅ **Gestión de campañas electorales**
  - Crear, editar, activar/desactivar campañas
  - Asociación con partidos, candidatos, tipos de elección
  - Validación de una sola campaña activa
  - Filtrado de formularios por campaña

- ✅ **Monitoreo del sistema**
  - Métricas de rendimiento
  - Usuarios conectados
  - Requests por minuto
  - Alertas del sistema

- ✅ **Logs y auditoría**
  - Registro de todas las acciones
  - Filtros por usuario, acción, fecha, severidad
  - Exportación en CSV y JSON
  - Retención de 90 días

- ✅ **Gestión de ubicaciones DIVIPOLA**
  - CRUD completo de ubicaciones
  - Validación de códigos únicos
  - Carga masiva desde CSV
  - Integridad referencial

- ✅ **Vista nacional de resultados**
  - Consolidado nacional de votos
  - Estadísticas nacionales
  - Navegación por departamentos/municipios/puestos
  - Actualización en tiempo real

- ✅ **Estadísticas globales**
  - Total de usuarios por rol
  - Total de formularios E-14 por estado
  - Porcentaje de mesas con formularios validados
  - Actividad en últimas 24 horas

### Funcionalidades Pendientes (30%)

- ⏳ **Mapa de Colombia con resultados** (Tarea 19)
  - Visualización geográfica de resultados por departamento

- ⏳ **Gestión de permisos y roles** (Tarea 20)
  - Modificación de permisos por rol
  - Aplicación inmediata de cambios

- ⏳ **Respaldos y recuperación** (Tarea 21)
  - Respaldos manuales y automáticos
  - Descarga de respaldos
  - Alertas de fallos

- ⏳ **Gestión de configuración del sistema** (Tarea 22)
  - Configuración de parámetros del sistema
  - Historial de cambios
  - Revertir configuraciones

- ⏳ **Análisis de uso del sistema** (Tarea 23)
  - Estadísticas detalladas de uso
  - Reportes en PDF

- ⏳ **Gestión de notificaciones** (Tarea 24)
  - Envío de notificaciones a usuarios
  - Programación de envíos
  - Historial de notificaciones

- ⏳ **Configuración de temas visuales** (Tarea 25)
  - Temas personalizados por rol
  - Preview de temas
  - Validación de accesibilidad

### Archivos Implementados

**Frontend:**
- `frontend/templates/admin/super-admin-dashboard.html` - Dashboard principal
- `frontend/templates/admin/configuracion.html` - Configuración electoral
- `frontend/templates/admin/gestion-usuarios.html` - Gestión de usuarios
- `frontend/templates/admin/personalizacion-tab.html` - Personalización de fondos
- `frontend/static/js/super-admin-dashboard.js` - Lógica principal
- `frontend/static/js/admin-configuracion.js` - Configuración electoral
- `frontend/static/js/gestion-usuarios.js` - Gestión de usuarios
- `frontend/static/js/personalizacion-sistema.js` - Personalización de fondos
- `frontend/static/css/personalizacion.css` - Estilos de personalización

**Backend:**
- `backend/routes/super_admin.py` - Endpoints principales
- `backend/routes/gestion_usuarios.py` - Gestión de usuarios
- `backend/routes/configuracion.py` - Configuración electoral
- `backend/routes/configuracion_sistema.py` - Personalización de fondos
- `backend/routes/admin_tools.py` - Herramientas de administración
- `backend/routes/admin_data_import.py` - Importación masiva
- `backend/routes/monitoreo.py` - Monitoreo del sistema
- `backend/models/configuracion_sistema.py` - Modelos de personalización
- `backend/models/configuracion_electoral.py` - Modelos de configuración (incluye Campana, ConfiguracionTema)
- `backend/models/coordinador_municipal.py` - Modelo AuditLog

## Mejoras Futuras (Opcionales)

- [ ] Implementar dashboard de métricas en tiempo real con gráficos interactivos
- [ ] Agregar sistema de alertas por email para eventos críticos
- [ ] Implementar chat en vivo con coordinadores
- [ ] Agregar exportación de reportes en múltiples formatos (Excel, Word)
- [ ] Implementar sistema de roles personalizados
- [ ] Agregar análisis predictivo de participación electoral
- [ ] Implementar sistema de recomendaciones basado en IA
- [ ] Agregar integración con sistemas externos (APIs de gobierno)
