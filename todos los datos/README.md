# MVP - Sistema Electoral E-14/E-24
## Funcionalidad Mínima Viable

Este directorio contiene la implementación mínima funcional del sistema electoral con:

### Componentes Incluidos

1. **Autenticación y Usuarios**
   - Login/Logout con JWT
   - Gestión de usuarios por roles
   - Control de acceso basado en roles

2. **Roles Implementados**
   - Testigo Electoral (captura E-14)
   - Coordinador de Puesto (validación E-14 y gestión E-24)
   - Sistemas/Superadmin (administración completa)

3. **Gestión de Ubicaciones (DIVIPOLA)**
   - Jerarquía: Departamento → Municipio → Puesto → Mesa
   - Asignación de usuarios a ubicaciones

4. **Formularios E-14**
   - Captura de datos por testigos
   - Validación automática
   - Aprobación/rechazo por coordinadores

5. **Dashboards**
   - Dashboard de testigo (mis formularios)
   - Dashboard de coordinador (formularios pendientes)
   - Dashboard de admin (estadísticas generales)

### Estructura de Archivos

```
mvp/
├── README.md                          # Este archivo
├── REQUERIMIENTOS_MVP.md              # Requerimientos funcionales
├── DISEÑO_MVP.md                      # Diseño técnico
├── TAREAS_MVP.md                      # Plan de implementación
├── backend/                           # Código backend
│   ├── models/                        # Modelos de datos
│   ├── routes/                        # Endpoints API
│   ├── services/                      # Lógica de negocio
│   └── utils/                         # Utilidades
├── frontend/                          # Código frontend
│   ├── templates/                     # Plantillas HTML
│   ├── static/                        # CSS/JS/Imágenes
│   └── components/                    # Componentes reutilizables
└── scripts/                           # Scripts de inicialización
    ├── init_mvp_db.py                # Inicializar BD
    └── load_sample_data.py           # Datos de prueba
```

### Instalación Rápida

```bash
# 1. Activar entorno virtual
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Inicializar base de datos MVP
python mvp/scripts/init_mvp_db.py

# 4. Cargar datos de prueba
python mvp/scripts/load_sample_data.py

# 5. Ejecutar aplicación
python run.py
```

### Usuarios de Prueba

Después de ejecutar `load_sample_data.py`:

- **Superadmin**: admin@sistema.com / Admin123!
- **Coordinador**: coord.puesto1@sistema.com / Coord123!
- **Testigo**: testigo.mesa1@sistema.com / Testigo123!

### Flujo Básico

1. **Testigo** inicia sesión → Accede a su dashboard → Crea formulario E-14
2. **Coordinador** inicia sesión → Ve formularios pendientes → Aprueba/Rechaza
3. **Admin** inicia sesión → Ve estadísticas → Gestiona usuarios

### Endpoints Principales

```
POST   /api/auth/login              # Iniciar sesión
GET    /api/auth/profile            # Perfil usuario
POST   /api/e14/forms               # Crear E-14
GET    /api/e14/forms               # Listar E-14
PUT    /api/e14/forms/:id/approve   # Aprobar E-14
GET    /api/coordination/dashboard  # Dashboard coordinador
GET    /api/admin/stats             # Estadísticas admin
```

### Validaciones Implementadas

- Total votos ≤ Votantes registrados
- Suma de votos = Total votos
- Unicidad por mesa
- Formato de datos correcto

### Próximos Pasos (Post-MVP)

- Formularios E-24
- Detección de discrepancias
- Sistema de alertas
- Coordinadores municipales y departamentales
- Auditoría completa
- Reportes avanzados
