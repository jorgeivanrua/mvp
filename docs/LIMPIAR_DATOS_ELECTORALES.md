# Funcionalidad: Limpiar Datos Electorales

## Descripción
Nueva funcionalidad en el Super Admin Dashboard que permite limpiar todos los datos electorales (reportes y formularios) manteniendo la estructura base del sistema.

## Ubicación
- **Dashboard:** Super Admin → Vista General → Testing & Diagnóstico
- **Botón:** "Limpiar Datos Electorales" (color amarillo/warning)
- **Ruta API:** `POST /api/admin/limpiar-datos-electorales`

## Funcionalidad

### ¿Qué se ELIMINA?
- ✅ **Formularios E-14** y todas sus fotos asociadas
- ✅ **Reportes de participación** horaria (E-11)
- ✅ **Incidentes electorales** reportados
- ✅ **Delitos electorales** reportados
- ✅ **Evidencias fotográficas** de incidentes y delitos
- ✅ **Votos por candidato** registrados
- ✅ **Verificaciones de presencia** de testigos (se resetean)

### ¿Qué se CONSERVA?
- ✅ **Usuarios** y sus contraseñas
- ✅ **Ubicaciones** (DIVIPOLA completa)
- ✅ **Partidos políticos**
- ✅ **Candidatos**
- ✅ **Tipos de elección**
- ✅ **Configuración del sistema**

## Proceso de Confirmación

### 1. Modal de Confirmación
- Se muestra un modal detallado con:
  - Lista de datos que se eliminarán
  - Lista de datos que se conservarán
  - Checkbox de confirmación obligatorio
  - Botones de cancelar/confirmar

### 2. Validaciones
- Solo usuarios con rol `super_admin` pueden ejecutar
- Requiere confirmación explícita mediante checkbox
- Doble confirmación de seguridad

### 3. Proceso de Limpieza
1. Cuenta registros antes de eliminar
2. Elimina en orden correcto (respetando foreign keys):
   - Fotos de incidentes/delitos
   - Delitos electorales
   - Incidentes electorales
   - Votos por candidato
   - Fotos de formularios
   - Formularios E-14
   - Reportes de participación
3. Resetea verificaciones de presencia de testigos
4. Confirma cambios en base de datos

### 4. Reporte de Resultados
- Muestra estadísticas detalladas de registros eliminados
- Confirma que la BD está lista para nuevos datos
- Actualiza automáticamente las estadísticas del dashboard

## Casos de Uso

### 1. Preparación para Nueva Jornada Electoral
- Limpiar datos de pruebas o jornadas anteriores
- Mantener toda la configuración y usuarios
- Dejar sistema listo para nueva recolección de datos

### 2. Reset de Datos de Prueba
- Eliminar formularios y reportes de testing
- Conservar estructura de usuarios y ubicaciones
- Permitir nuevas pruebas desde cero

### 3. Limpieza Post-Electoral
- Archivar datos importantes externamente
- Limpiar sistema para próxima elección
- Mantener configuración base intacta

## Seguridad

### Restricciones de Acceso
- Solo `super_admin` puede ejecutar
- Validación de JWT token
- Verificación de rol en backend

### Confirmaciones Múltiples
- Modal con información detallada
- Checkbox de confirmación obligatorio
- Botón deshabilitado hasta confirmar

### Auditoría
- Registra estadísticas antes/después
- Muestra resumen completo de operación
- Logs de seguridad en backend

## Implementación Técnica

### Backend
- **Archivo:** `backend/routes/admin_tools.py`
- **Función:** `limpiar_datos_electorales()`
- **Método:** `POST`
- **Autenticación:** JWT + role_required(['super_admin'])

### Frontend
- **Modal:** `limpiarDatosModal` en super-admin-dashboard.html
- **JavaScript:** `limpiarDatosElectorales()` y `confirmarLimpiezaDatos()`
- **Estilo:** Bootstrap modal con colores de advertencia

### Modelos Afectados
```python
# Eliminados
FormularioE14, VotoCandidato
FormularioFoto
ReporteParticipacion
IncidenteElectoral, DelitoElectoral
IncidenteDelitoFoto

# Conservados
User, Location
PartidoPolitico, Candidato
TipoEleccion
```

## Resultado Final
Después de ejecutar la limpieza:
- ✅ Base de datos lista para nuevos datos
- ✅ Testigos deben verificar presencia nuevamente
- ✅ Coordinadores ven estadísticas en cero
- ✅ Sistema completamente funcional
- ✅ Toda la configuración intacta

## Notas Importantes
- **Irreversible:** No hay función de deshacer
- **Backup recomendado:** Exportar BD antes de limpiar
- **Re-verificación:** Testigos deben verificar presencia nuevamente
- **Estadísticas:** Se actualizan automáticamente después de la limpieza