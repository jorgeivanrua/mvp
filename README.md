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

## 🔧 Instalación y Configuración

### Opción 1: Instalación Automática (Recomendada) ⚡

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Este script automáticamente:
- ✅ Crea el entorno virtual
- ✅ Instala todas las dependencias
- ✅ Inicializa la base de datos
- ✅ Carga las ubicaciones (DIVIPOLA)
- ✅ Crea los usuarios del sistema
- ✅ Aplica todas las migraciones
- ✅ Configura el sistema electoral

### Opción 2: Instalación Manual 🔧

#### 1. Clonar el repositorio
```bash
git clone https://github.com/jorgeivanrua/testigos.git
cd testigos/mvp
```

#### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Inicializar el sistema
```bash
python setup.py
```

## 🚀 Ejecutar la Aplicación

### Desarrollo Local

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**O directamente con Python:**
```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

### Despliegue en Render.com 🌐

1. **Conectar repositorio a Render**
   - Ve a [render.com](https://render.com)
   - Crea una nueva Web Service
   - Conecta tu repositorio de GitHub

2. **Configuración automática**
   - Render detectará automáticamente el archivo `render.yaml`
   - La inicialización se ejecutará automáticamente con `render_setup.py`

3. **Variables de entorno** (opcional)
   - `SECRET_KEY`: Se genera automáticamente
   - `JWT_SECRET_KEY`: Se genera automáticamente
   - `DATABASE_URL`: Para usar PostgreSQL (recomendado en producción)

4. **Archivo DIVIPOLA**
   - Coloca el archivo `divipola.csv` en la carpeta `todos los datos/`
   - O súbelo manualmente después del despliegue

## 👥 Usuarios del Sistema

Después de la inicialización, tendrás acceso con estas credenciales:

### Super Administrador
| Usuario | Contraseña | Descripción |
|---------|-----------|-------------|
| admin | admin123 | Acceso completo al sistema |

### Administradores
| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin_caqueta | admin123 | Admin Departamental |
| admin_florencia | admin123 | Admin Municipal |

### Coordinadores
| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| coord_dpto_caqueta | coord123 | Coordinador Departamental |
| coord_mun_florencia | coord123 | Coordinador Municipal |
| coord_puesto_XX | coord123 | Coordinador de Puesto |

### Testigos
| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| testigo_XX_1 | testigo123 | Testigo Electoral |
| testigo_XX_2 | testigo123 | Testigo Electoral |

### Auditor
| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| auditor_caqueta | auditor123 | Auditor Electoral |

⚠️ **IMPORTANTE**: Cambia todas las contraseñas después del primer acceso en producción

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

## 📖 Documentación

### Guías de Inicio
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - ⚡ Empieza en 2 minutos
- **[GUIA_DESPLIEGUE.md](GUIA_DESPLIEGUE.md)** - 🚀 Despliegue completo (Local, Render, Heroku, VPS)
- **[GUIA_PRUEBAS_MANUALES.md](GUIA_PRUEBAS_MANUALES.md)** - 🧪 Cómo probar el sistema

### Documentación Técnica
- [FORMULARIOS_E14_IMPLEMENTADOS.md](FORMULARIOS_E14_IMPLEMENTADOS.md) - Sistema de formularios
- [DASHBOARDS_IMPLEMENTADOS.md](DASHBOARDS_IMPLEMENTADOS.md) - Dashboards por rol
- [ESTADO_FINAL_SISTEMA.md](ESTADO_FINAL_SISTEMA.md) - Estado actual del proyecto

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

### ✅ Completado (v1.0.0 - Nov 22, 2025)
- ✅ Sistema de autenticación JWT
- ✅ Gestión de usuarios por rol
- ✅ Configuración electoral dinámica
- ✅ Formularios E-14 completos con todas las funcionalidades
- ✅ API REST completa
- ✅ Dashboards funcionales para todos los roles
- ✅ Verificación de presencia con geolocalización
- ✅ Sistema de sincronización offline
- ✅ Carga de imágenes de formularios
- ✅ Validación de formularios por coordinadores
- ✅ Reportes y estadísticas por rol
- ✅ Sistema de inicialización automatizado
- ✅ Scripts de despliegue para Render
- ✅ Documentación completa
- ✅ Correcciones de errores aplicadas

### 🎯 Estado Actual
**LISTO PARA PRODUCCIÓN** ✅

El sistema está completamente funcional y listo para:
- ✓ Desarrollo local
- ✓ Despliegue en Render
- ✓ Uso en producción

### 📋 Próximas Versiones
- v1.1: Formularios E-24, notificaciones, exportación
- v1.2: Modo completamente offline, PWA
- v2.0: App móvil nativa, ML para detección de anomalías

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
