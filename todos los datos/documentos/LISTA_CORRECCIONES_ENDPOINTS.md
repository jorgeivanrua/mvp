# Lista de Correcciones de Endpoints

**Fecha**: 2025-11-15
**Total de correcciones**: 37

## 🔴 Blueprints Faltantes (5)

### Admin Departamental
- **Archivo**: `backend/routes/admin.py`
- **Acción**: Crear archivo backend/routes/admin.py

### Admin Municipal
- **Archivo**: `backend/routes/admin_municipal.py`
- **Acción**: Crear archivo backend/routes/admin_municipal.py

### Coordinador Departamental
- **Archivo**: `backend/routes/coordinador_departamental.py`
- **Acción**: Crear archivo backend/routes/coordinador_departamental.py

### Coordinador Puesto
- **Archivo**: `backend/routes/coordinador_puesto.py`
- **Acción**: Crear archivo backend/routes/coordinador_puesto.py

### Auditor Electoral
- **Archivo**: `backend/routes/auditor.py`
- **Acción**: Crear archivo backend/routes/auditor.py

## 🟠 Endpoints Faltantes (32)

### Super Admin (6 endpoints)

- [ ] `GET /api/super-admin/usuarios` - Lista de todos los usuarios
- [ ] `GET /api/super-admin/ubicaciones` - Lista de todas las ubicaciones
- [ ] `GET /api/super-admin/partidos` - Lista de partidos políticos
- [ ] `POST /api/super-admin/usuarios` - Crear nuevo usuario
- [ ] `PUT /api/super-admin/usuarios/<id>` - Actualizar usuario
- [ ] `DELETE /api/super-admin/usuarios/<id>` - Eliminar usuario

### Admin Departamental (4 endpoints)

- [ ] `GET /api/admin/stats` - Estadísticas del departamento
- [ ] `GET /api/admin/usuarios` - Usuarios del departamento
- [ ] `GET /api/admin/ubicaciones` - Ubicaciones del departamento
- [ ] `GET /api/admin/formularios` - Formularios del departamento

### Admin Municipal (4 endpoints)

- [ ] `GET /api/admin-municipal/stats` - Estadísticas del municipio
- [ ] `GET /api/admin-municipal/zonas` - Zonas del municipio
- [ ] `GET /api/admin-municipal/puestos` - Puestos del municipio
- [ ] `GET /api/admin-municipal/mesas` - Mesas del municipio

### Coordinador Departamental (3 endpoints)

- [ ] `GET /api/coordinador-departamental/stats` - Estadísticas departamentales
- [ ] `GET /api/coordinador-departamental/municipios` - Municipios del departamento
- [ ] `GET /api/coordinador-departamental/resumen` - Resumen de avance departamental

### Coordinador Municipal (4 endpoints)

- [ ] `GET /api/coordinador-municipal/stats` - Estadísticas municipales
- [ ] `GET /api/coordinador-municipal/zonas` - Zonas del municipio
- [ ] `GET /api/coordinador-municipal/mesas` - Mesas del municipio
- [ ] `GET /api/coordinador-municipal/formularios` - Formularios del municipio

### Coordinador Puesto (5 endpoints)

- [ ] `GET /api/coordinador-puesto/stats` - Estadísticas del puesto
- [ ] `GET /api/coordinador-puesto/mesas` - Mesas del puesto
- [ ] `GET /api/coordinador-puesto/testigos` - Testigos del puesto
- [ ] `GET /api/coordinador-puesto/incidentes` - Incidentes del puesto
- [ ] `GET /api/coordinador-puesto/formularios` - Formularios del puesto

### Testigo Electoral (2 endpoints)

- [ ] `GET /api/testigo/formularios` - Formularios del testigo
- [ ] `POST /api/testigo/formularios` - Crear formulario

### Auditor Electoral (4 endpoints)

- [ ] `GET /api/auditor/stats` - Estadísticas de auditoría
- [ ] `GET /api/auditor/inconsistencias` - Inconsistencias detectadas
- [ ] `GET /api/auditor/reportes` - Reportes de auditoría
- [ ] `GET /api/auditor/formularios` - Formularios para auditar

