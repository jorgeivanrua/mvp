# Implementation Plan - Sistema de Geolocalización y Verificación de Presencia

## Estado de Implementación

**Estado General:** ✅ COMPLETADO (100%)
**Fecha de Inicio:** 2025-11-18
**Fecha de Finalización:** 2025-11-23
**Implementado por:** Equipo de Desarrollo

---

## Tareas Completadas

- [x] 1. Extender modelo User con campos de geolocalización
- [x] 1.1 Agregar campos de verificación de presencia
  - Agregar campo presencia_verificada (Boolean, default False)
  - Agregar campo presencia_verificada_at (DateTime, nullable)
  - _Archivo: backend/models/user.py_
  - _Requirements: 1.2, 1.3_

- [x] 1.2 Agregar campos de geolocalización
  - Agregar campo ultima_latitud (Float, nullable)
  - Agregar campo ultima_longitud (Float, nullable)
  - Agregar campo ultima_geolocalizacion_at (DateTime, nullable)
  - Agregar campo precision_geolocalizacion (Float, nullable)
  - _Archivo: backend/models/user.py_
  - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [x] 1.3 Implementar método verificar_presencia()
  - Actualizar presencia_verificada a True
  - Actualizar presencia_verificada_at con timestamp actual
  - _Archivo: backend/models/user.py_
  - _Requirements: 1.2, 1.3_

- [x] 2. Crear API REST endpoints
- [x] 2.1 Crear Blueprint verificacion_bp
  - Configurar prefix /api/verificacion
  - Importar dependencias necesarias
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: Todos_

- [x] 2.2 Implementar POST /presencia
  - Requerir autenticación JWT
  - Obtener user_id del token
  - Extraer latitud y longitud del request body
  - Actualizar presencia_verificada a True
  - Actualizar presencia_verificada_at con timestamp actual
  - Actualizar ultimo_acceso con timestamp actual
  - Guardar coordenadas GPS si se proporcionan
  - Guardar timestamp de geolocalización
  - Retornar success con datos de ubicación
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_

- [x] 2.3 Implementar POST /ping
  - Requerir autenticación JWT
  - Obtener user_id del token
  - Actualizar ultimo_acceso con timestamp actual
  - Si no ha verificado presencia, marcarla como verificada
  - Retornar success con ultimo_acceso
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 2.4 Implementar GET /estado-equipo
  - Requerir autenticación JWT
  - Requerir rol de coordinador (coordinador_puesto, coordinador_municipal, coordinador_departamental, super_admin)
  - Obtener ubicación del coordinador
  - Filtrar equipo según rol del coordinador
  - Para coordinador_puesto: obtener testigos del puesto
  - Para coordinador_municipal: obtener coordinadores_puesto del municipio
  - Para coordinador_departamental: obtener coordinadores_municipal del departamento
  - Para super_admin: obtener todos los coordinadores_departamental
  - Calcular minutos de inactividad para cada usuario
  - Determinar estado de cada usuario (activo/inactivo/ausente)
  - Calcular estadísticas (total, presentes, inactivos, ausentes, porcentaje)
  - Retornar equipo y estadísticas
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 2.5 Implementar GET /usuarios-geolocalizados
  - Requerir autenticación JWT
  - Requerir rol de coordinador o auditor
  - Construir query base: usuarios activos con coordenadas no nulas
  - Filtrar según rol del usuario que consulta
  - Para coordinador_puesto: solo testigos del puesto
  - Para coordinador_municipal: coordinadores_puesto y testigos del municipio
  - Para coordinador_departamental: todos los coordinadores y testigos del departamento
  - Para super_admin: todos los usuarios
  - Para auditor_electoral: todos los usuarios que puede auditar
  - Formatear respuesta con: id, nombre, rol, latitud, longitud, timestamps, estado, ubicación
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 9.1, 9.5_

- [x] 3. Implementar funciones de lógica de negocio
- [x] 3.1 Implementar calcular_minutos_inactivo()
  - Recibir ultimo_acceso como parámetro
  - Si es None, retornar None
  - Calcular diferencia entre now() y ultimo_acceso
  - Convertir a minutos (total_seconds / 60)
  - Retornar como entero
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: 4.5, 6.5_

- [x] 3.2 Implementar determinar_estado_usuario()
  - Recibir usuario como parámetro
  - Si ultimo_acceso es None, retornar 'ausente'
  - Calcular minutos de inactividad
  - Si < 15 minutos, retornar 'activo'
  - Si entre 15 y 60 minutos, retornar 'inactivo'
  - Si > 60 minutos, retornar 'ausente'
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 4. Implementar componentes de frontend
- [x] 4.1 Crear botón "Verificar Presencia"
  - Botón visible en dashboard de todos los roles
  - Icono de ubicación
  - Texto "Verificar Presencia"
  - Event listener en click
  - _Archivo: frontend/templates/testigo_dashboard.html (y otros dashboards)_
  - _Requirements: 1.1_

- [x] 4.2 Implementar función verificarPresencia()
  - Solicitar permiso de geolocalización del navegador
  - Usar navigator.geolocation.getCurrentPosition()
  - Configurar opciones: enableHighAccuracy=true, timeout=10000, maximumAge=0
  - Extraer latitude, longitude, accuracy de position.coords
  - Enviar POST a /api/verificacion/presencia con coordenadas
  - Incluir token JWT en headers
  - Mostrar mensaje de éxito si success=true
  - Iniciar ping automático después de verificación exitosa
  - Manejar errores con manejarErrorGPS()
  - _Archivo: frontend/templates/testigo_dashboard.html (script section)_
  - _Requirements: 1.1, 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 4.3 Implementar función manejarErrorGPS()
  - Recibir error de geolocalización
  - Switch según error.code
  - PERMISSION_DENIED: "Permiso de ubicación denegado..."
  - POSITION_UNAVAILABLE: "GPS no disponible en este dispositivo"
  - TIMEOUT: "Tiempo de espera agotado. Intente nuevamente."
  - Default: "Error desconocido al obtener ubicación"
  - Mostrar mensaje de error al usuario
  - _Archivo: frontend/templates/testigo_dashboard.html (script section)_
  - _Requirements: 11.1, 11.2, 11.3, 11.5_

- [x] 4.4 Implementar ping automático
  - Variable global pingInterval
  - Función iniciarPingAutomatico()
  - Limpiar intervalo anterior si existe
  - Crear setInterval cada 5 minutos (5 * 60 * 1000 ms)
  - Enviar POST a /api/verificacion/ping con token JWT
  - Manejar errores silenciosamente (console.error)
  - Event listener en beforeunload para detener ping
  - _Archivo: frontend/templates/testigo_dashboard.html (script section)_
  - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [x] 4.5 Crear sección "Estado del Equipo" en dashboards de coordinadores
  - Sección visible solo para coordinadores
  - Título "Estado del Equipo"
  - Tabla con columnas: Nombre, Rol, Ubicación, Último Acceso, Estado
  - Indicadores de color según estado (verde=activo, amarillo=inactivo, rojo=ausente)
  - Panel de estadísticas con: Total, Presentes, Inactivos, Ausentes, % Presencia
  - Botón "Actualizar" para refrescar datos
  - _Archivo: frontend/templates/coordinador_puesto_dashboard.html (y otros coordinadores)_
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 4.6 Implementar función cargarEstadoEquipo()
  - Enviar GET a /api/verificacion/estado-equipo con token JWT
  - Parsear respuesta JSON
  - Limpiar tabla existente
  - Iterar sobre data.equipo
  - Crear fila por cada usuario con: nombre, rol, ubicación, último acceso, estado
  - Aplicar clase CSS según estado (badge-success, badge-warning, badge-danger)
  - Actualizar estadísticas en panel
  - Manejar errores y mostrar mensaje
  - _Archivo: frontend/templates/coordinador_puesto_dashboard.html (script section)_
  - _Requirements: 6.5, 7.5_

- [x] 4.7 Crear página de mapa de usuarios geolocalizados
  - Página dedicada para mapa
  - Contenedor div#map con altura 600px
  - Incluir Leaflet.js CSS y JS
  - Botón "Ver Mapa" en dashboards de coordinadores
  - _Archivo: frontend/templates/mapa_usuarios.html_
  - _Requirements: 8.1, 8.2_

- [x] 4.8 Implementar función cargarMapaUsuarios()
  - Inicializar mapa Leaflet centrado en Colombia [4.6097, -74.0817]
  - Agregar capa de tiles de OpenStreetMap
  - Enviar GET a /api/verificacion/usuarios-geolocalizados con token JWT
  - Parsear respuesta JSON
  - Iterar sobre data.data
  - Llamar agregarMarcadorUsuario() por cada usuario
  - Manejar errores y mostrar mensaje
  - _Archivo: frontend/templates/mapa_usuarios.html (script section)_
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 4.9 Implementar función agregarMarcadorUsuario()
  - Determinar color según estado (green=activo, yellow=inactivo, red=ausente)
  - Crear circleMarker en [latitud, longitud]
  - Configurar radio=8, fillColor según estado, color=#000, weight=1
  - Agregar marcador al mapa
  - Crear popup con: nombre, rol, ubicación, último acceso, estado, coordenadas
  - Formatear coordenadas con 6 decimales (toFixed(6))
  - Bind popup al marcador
  - Agregar marcador a array markers
  - _Archivo: frontend/templates/mapa_usuarios.html (script section)_
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 5. Crear migraciones de base de datos
- [x] 5.1 Crear migración para agregar campos de verificación de presencia
  - ALTER TABLE users ADD COLUMN presencia_verificada BOOLEAN DEFAULT FALSE NOT NULL
  - ALTER TABLE users ADD COLUMN presencia_verificada_at TIMESTAMP
  - _Requirements: 1.2, 1.3_

- [x] 5.2 Crear migración para agregar campos de geolocalización
  - ALTER TABLE users ADD COLUMN ultima_latitud FLOAT
  - ALTER TABLE users ADD COLUMN ultima_longitud FLOAT
  - ALTER TABLE users ADD COLUMN ultima_geolocalizacion_at TIMESTAMP
  - ALTER TABLE users ADD COLUMN precision_geolocalizacion FLOAT
  - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [x] 5.3 Crear índices para optimización
  - CREATE INDEX idx_users_presencia_verificada ON users(presencia_verificada)
  - CREATE INDEX idx_users_ultimo_acceso ON users(ultimo_acceso)
  - CREATE INDEX idx_users_geolocalizacion ON users(ultima_latitud, ultima_longitud) WHERE ultima_latitud IS NOT NULL AND ultima_longitud IS NOT NULL
  - _Requirements: Performance_

- [x] 6. Registrar blueprint en aplicación
- [x] 6.1 Registrar verificacion_bp en app.py
  - Importar blueprint
  - Registrar con app.register_blueprint()
  - _Archivo: backend/app.py o backend/routes/__init__.py_
  - _Requirements: Todos_

- [x] 7. Implementar validaciones
- [x] 7.1 Validar coordenadas GPS
  - Validar latitud en rango [-90, 90]
  - Validar longitud en rango [-180, 180]
  - Validar que ambas coordenadas estén presentes o ambas ausentes
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 7.2 Validar permisos de acceso
  - Verificar que coordinador_puesto solo vea testigos de su puesto
  - Verificar que coordinador_municipal solo vea coordinadores de su municipio
  - Verificar que coordinador_departamental solo vea coordinadores de su departamento
  - Usar decorador @role_required para endpoints protegidos
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 8.3, 8.4, 8.5_

- [x] 8. Implementar manejo de errores
- [x] 8.1 Manejar errores de GPS en frontend
  - Capturar errores de navigator.geolocation
  - Mostrar mensajes específicos según tipo de error
  - Permitir reintentar verificación
  - _Archivo: frontend/templates/testigo_dashboard.html (script section)_
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 8.2 Manejar errores de backend
  - Try-catch en todos los endpoints
  - Rollback de transacciones en caso de error
  - Retornar mensajes de error descriptivos
  - Logging de errores para debugging
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: Todos_

- [x] 9. Optimizaciones de rendimiento
- [x] 9.1 Optimizar queries de base de datos
  - Usar índices para filtrado rápido
  - Evitar N+1 queries con joins
  - Filtrar en base de datos en lugar de en memoria
  - _Archivo: backend/routes/verificacion_presencia.py_
  - _Requirements: Performance_

- [x] 9.2 Optimizar carga de mapa
  - Cargar solo usuarios con coordenadas válidas
  - Limitar número de marcadores si es necesario
  - Usar clustering para muchos marcadores
  - _Archivo: frontend/templates/mapa_usuarios.html (script section)_
  - _Requirements: Performance_

- [x] 10. Documentación
- [x] 10.1 Documentar API endpoints
  - Documentar request/response de cada endpoint
  - Documentar códigos de error
  - Documentar autenticación requerida
  - _Archivo: Este documento (design.md)_

- [x] 10.2 Documentar modelos de datos
  - Documentar campos de User relacionados con geolocalización
  - Documentar métodos de User
  - _Archivo: Este documento (design.md)_

- [x] 10.3 Documentar funciones de lógica de negocio
  - Documentar calcular_minutos_inactivo()
  - Documentar determinar_estado_usuario()
  - _Archivo: Este documento (design.md)_

---

## Resumen de Implementación

### Archivos Creados/Modificados

1. **backend/models/user.py** - Extendido con campos de geolocalización
2. **backend/routes/verificacion_presencia.py** - API REST completa (4 endpoints)
3. **frontend/templates/testigo_dashboard.html** - Botón de verificación y ping automático
4. **frontend/templates/coordinador_puesto_dashboard.html** - Estado del equipo
5. **frontend/templates/coordinador_municipal_dashboard.html** - Estado del equipo
6. **frontend/templates/coordinador_departamental_dashboard.html** - Estado del equipo
7. **frontend/templates/mapa_usuarios.html** - Mapa interactivo con usuarios geolocalizados
8. **backend/migrations/** - Migraciones de base de datos

### Funcionalidades Implementadas

✅ Verificación manual de presencia con GPS
✅ Captura de coordenadas GPS (latitud, longitud, precisión)
✅ Tracking de última ubicación
✅ Clasificación de estado de usuarios (activo/inactivo/ausente)
✅ Ping automático cada 5 minutos
✅ Vista de estado del equipo con estadísticas
✅ Mapa interactivo de usuarios geolocalizados
✅ Filtrado por rol y jurisdicción
✅ Marcadores de colores según estado
✅ Popups con información detallada
✅ Manejo de errores de GPS
✅ Validaciones de seguridad
✅ Optimizaciones de rendimiento

### Endpoints Implementados

1. `POST /api/verificacion/presencia` - Verificar presencia con GPS
2. `POST /api/verificacion/ping` - Ping automático
3. `GET /api/verificacion/estado-equipo` - Estado del equipo (protegido)
4. `GET /api/verificacion/usuarios-geolocalizados` - Usuarios en mapa (protegido)

### Modelos de Datos

**User Model (Extendido):**
- presencia_verificada (Boolean)
- presencia_verificada_at (DateTime)
- ultima_latitud (Float)
- ultima_longitud (Float)
- ultima_geolocalizacion_at (DateTime)
- precision_geolocalizacion (Float)

### Funciones de Lógica de Negocio

1. **calcular_minutos_inactivo(ultimo_acceso)** - Calcula minutos desde último acceso
2. **determinar_estado_usuario(usuario)** - Determina estado (activo/inactivo/ausente)

### Componentes de Frontend

1. **Botón "Verificar Presencia"** - Captura GPS y envía al backend
2. **Ping Automático** - Envía ping cada 5 minutos
3. **Tabla "Estado del Equipo"** - Muestra equipo con estados
4. **Panel de Estadísticas** - Muestra total, presentes, inactivos, ausentes, %
5. **Mapa Interactivo** - Muestra usuarios geolocalizados con marcadores de colores
6. **Popups de Marcadores** - Información detallada de cada usuario

---

## Notas de Implementación

- El sistema está 100% funcional y en producción
- Todos los endpoints están protegidos con autenticación JWT
- Los coordinadores solo pueden ver usuarios bajo su jurisdicción
- El ping automático se inicia después de la primera verificación de presencia
- El mapa usa Leaflet.js con tiles de OpenStreetMap
- Los estados se calculan dinámicamente basados en ultimo_acceso
- Las coordenadas se formatean con 6 decimales para precisión
- Los índices de base de datos optimizan las queries de geolocalización
- El sistema maneja errores de GPS con mensajes específicos
- El ping se detiene automáticamente al cerrar el navegador

---

**Fecha de Creación:** 2025-11-25
**Última Actualización:** 2025-11-25
**Estado:** ✅ COMPLETADO
**Implementado por:** Equipo de Desarrollo

