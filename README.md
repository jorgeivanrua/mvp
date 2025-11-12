# 🗳️ Sistema de Testigos Electorales - MVP

Sistema web para la gestión y registro de formularios E-14 (Actas de Escrutinio) por parte de testigos electorales en Colombia.

## 🚀 Características Principales

### ✅ Sistema Completo de Configuración Electoral
- Gestión de tipos de elección (Senado, Cámara, Concejo, etc.)
- Administración de partidos políticos con colores y logos
- Registro de candidatos por tipo de elección
- Gestión de coaliciones políticas

### ✅ Formularios E-14 Dinámicos
- Registro de actas de escrutinio con datos en tiempo real
- Carga dinámica de partidos y candidatos según tipo de elección
- Cálculos automáticos de totales y validaciones
- Sistema de estados (pendiente, validado, rechazado)
- Validación por coordinadores y administradores

### ✅ Dashboards por Rol
- **Admin**: Configuración electoral completa
- **Coordinador**: Validación de formularios (en desarrollo)
- **Testigo**: Registro de formularios E-14

### ✅ Seguridad
- Autenticación JWT
- Permisos por rol
- Validación de datos en backend y frontend

## 📋 Requisitos

- Python 3.8+
- SQLite (incluido)
- Navegador web moderno

## 🔧 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/jorgeivanrua/testigos.git
cd testigos/mvp
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus configuraciones
```

### 6. Inicializar base de datos
```bash
# Crear estructura de base de datos
python scripts/init_db.py

# Cargar datos de ubicaciones (DIVIPOLA)
python scripts/load_divipola.py

# Crear usuarios de prueba
python scripts/create_test_users.py

# Cargar configuración electoral
python scripts/init_configuracion_electoral.py

# Crear tablas de formularios E-14
python scripts/create_formularios_e14_tables.py
```

## 🚀 Ejecutar la Aplicación

### Opción 1: Script de inicio (Windows)
```bash
start.bat
```

### Opción 2: Python directo
```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 👥 Usuarios de Prueba

Después de ejecutar `create_test_users.py`:

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin@test.com | admin123 | Administrador |
| coordinador@test.com | coord123 | Coordinador |
| testigo@test.com | test123 | Testigo |

## 📁 Estructura del Proyecto

```
mvp/
├── backend/
│   ├── models/          # Modelos de datos
│   ├── routes/          # Endpoints API
│   ├── services/        # Lógica de negocio
│   └── utils/           # Utilidades
├── frontend/
│   ├── static/
│   │   ├── css/        # Estilos
│   │   └── js/         # JavaScript
│   └── templates/       # HTML templates
├── scripts/             # Scripts de inicialización
├── instance/            # Base de datos SQLite
└── requirements.txt     # Dependencias Python
```

## 🔑 Funcionalidades por Rol

### Administrador
- ✅ Gestión completa de configuración electoral
- ✅ Crear/editar tipos de elección
- ✅ Crear/editar partidos políticos
- ✅ Crear/editar candidatos
- ✅ Gestionar coaliciones
- ✅ Eliminar formularios

### Coordinador
- ✅ Validar formularios E-14
- ✅ Rechazar formularios con observaciones
- 🔄 Dashboard de validación (en desarrollo)

### Testigo Electoral
- ✅ Registrar formularios E-14
- ✅ Ver sus propios formularios
- ✅ Editar formularios pendientes
- ✅ Carga dinámica de configuración electoral

## 📊 API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/profile` - Obtener perfil

### Configuración Electoral
- `GET /api/configuracion/tipos-eleccion` - Listar tipos de elección
- `POST /api/configuracion/tipos-eleccion` - Crear tipo de elección
- `GET /api/configuracion/partidos` - Listar partidos
- `POST /api/configuracion/partidos` - Crear partido
- `GET /api/configuracion/candidatos` - Listar candidatos
- `POST /api/configuracion/candidatos` - Crear candidato

### Formularios E-14
- `GET /api/formularios-e14` - Listar formularios
- `POST /api/formularios-e14` - Crear formulario
- `GET /api/formularios-e14/{id}` - Ver formulario
- `PUT /api/formularios-e14/{id}` - Actualizar formulario
- `POST /api/formularios-e14/{id}/validar` - Validar/rechazar
- `DELETE /api/formularios-e14/{id}` - Eliminar formulario

## 📖 Documentación Adicional

- [FORMULARIOS_E14_IMPLEMENTADOS.md](FORMULARIOS_E14_IMPLEMENTADOS.md) - Documentación completa del sistema de formularios
- [DASHBOARDS_IMPLEMENTADOS.md](DASHBOARDS_IMPLEMENTADOS.md) - Guía de dashboards
- [COMO_INICIAR.md](COMO_INICIAR.md) - Guía de inicio rápido

## 🛠️ Tecnologías Utilizadas

### Backend
- Flask 3.0.0
- Flask-SQLAlchemy
- Flask-JWT-Extended
- SQLite

### Frontend
- Bootstrap 5.3
- JavaScript ES6+
- Bootstrap Icons

## 🔄 Estado del Proyecto

### ✅ Completado
- Sistema de autenticación JWT
- Gestión de usuarios por rol
- Configuración electoral dinámica
- Formularios E-14 completos
- API REST completa
- Dashboards funcionales

### 🔄 En Desarrollo
- Sistema de carga de imágenes
- Dashboard de validación para coordinadores
- Reportes y estadísticas

### 📋 Pendiente
- Formularios E-24
- Sistema de notificaciones
- Exportación de datos
- Modo offline

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

Jorge Iván Rúa

## 📧 Contacto

Para preguntas o soporte, contactar a través de GitHub Issues.

---

**Nota**: Este es un MVP (Producto Mínimo Viable) en desarrollo activo. Algunas funcionalidades están en proceso de implementación.
