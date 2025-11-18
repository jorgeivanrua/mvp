# Guía Completa del Sistema Electoral E-14/E-24

## 📋 Índice

1. [Visión General del Sistema](#visión-general)
2. [Arquitectura](#arquitectura)
3. [Roles y Permisos](#roles-y-permisos)
4. [Endpoints API](#endpoints-api)
5. [Dashboards](#dashboards)
6. [Flujo de Trabajo](#flujo-de-trabajo)
7. [Guía de Uso por Rol](#guía-de-uso-por-rol)
8. [Credenciales de Acceso](#credenciales-de-acceso)

---

## 🎯 Visión General del Sistema

### Propósito
Sistema web para la gestión y consolidación de resultados electorales en el departamento de Caquetá, Colombia, utilizando los formularios E-14 (mesa) y E-24 (consolidados).

### Tecnologías
- **Backend**: Python Flask + SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, JavaScript (Vanilla)
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Autenticación**: JWT (JSON Web Tokens)

### Características Principales
- ✅ Gestión jerárquica de ubicaciones (DIVIPOLA)
- ✅ Registro de votos por mesa (E-14)
- ✅ Consolidación automática (E-24)
- ✅ Sistema de roles y permisos
- ✅ Reportes de incidentes y delitos electorales
- ✅ Validación y auditoría de datos
- ✅ Gestión automática de usuarios

---

## 🏗️ Arquitectura

### Estructura del Proyecto

```
mvp/
├── backend/
│   ├── app.py                 # Aplicación Flask principal
│   ├── config.py              # Configuración
│   ├── database.py            # Configuración de BD
│   ├── models/                # Modelos de datos
│   │   ├── user.py
│   │   ├── location.py
│   │   ├── formulario_e14.py
│   │   └── ...
│   ├── routes/                # Endpoints API
│   │   ├── auth.py           # Autenticación
│   │   ├── locations.py      # Ubicaciones
│   │   ├── testigo.py        # Testigo electoral
│   │   ├── coordinador_puesto.py
│   │   ├── coordinador_municipal.py
│   │   ├── coordinador_departamental.py
│   │   ├── admin.py
│   │   ├── auditor.py
│   │   └── gestion_usuarios.py
│   ├── services/              # Lógica de negocio
│   └── utils/                 # Utilidades
├── frontend/
│   ├── templates/             # Templates HTML
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── testigo/
│   │   ├── coordinador/
│   │   └── admin/
│   └── static/
│       ├── css/
│       └── js/
│           ├── api-client.js
│           ├── utils.js
│           ├── login-fixed.js
│           └── ...
└── run.py                     # Punto de entrada
```

### Flujo de Datos

```
Usuario → Login → JWT Token → Dashboard → API Endpoints → Base de Datos
                                    ↓
                              Validaciones
                                    ↓
                              Consolidación
                                    ↓
                              Reportes
```

---

## 👥 Roles y Permisos

### Jerarquía de Roles

```
Super Admin
    ├── Admin Departamental
    │   └── Admin Municipal
    │       └── Coordinador Municipal
    │           └── Coordinador de Puesto
    │               └── Testigo Electoral
    └── Auditor Electoral (transversal)
```

### 1. Super Admin
**Alcance**: Todo el sistema

**Permisos**:
- ✅ Gestión completa de usuarios
- ✅ Configuración del sistema
- ✅ Acceso a todos los datos
- ✅ Gestión de campañas
- ✅ Creación de usuarios automática

**Dashboard**: `/admin/super-admin`

### 2. Admin Departamental
**Alcance**: Departamento completo (CAQUETÁ)

**Permisos**:
- ✅ Ver todos los municipios
- ✅ Gestionar usuarios municipales
- ✅ Consolidar datos departamentales
- ✅ Generar reportes departamentales

**Dashboard**: `/admin/dashboard`

### 3. Admin Municipal
**Alcance**: Un municipio específico

**Permisos**:
- ✅ Ver todos los puestos del municipio
- ✅ Gestionar usuarios del municipio
- ✅ Consolidar datos municipales
- ✅ Validar formularios E-14

**Dashboard**: `/admin/dashboard`

### 4. Coordinador Departamental
**Alcance**: Departamento completo

**Permisos**:
- ✅ Monitorear todos los municipios
- ✅ Ver estadísticas departamentales
- ✅ Reportar incidentes departamentales

**Dashboard**: `/coordinador/departamental`

### 5. Coordinador Municipal
**Alcance**: Un municipio específico

**Permisos**:
- ✅ Monitorear todos los puestos del municipio
- ✅ Ver estadísticas municipales
- ✅ Generar E-24 municipal
- ✅ Reportar incidentes municipales

**Dashboard**: `/coordinador/municipal`

### 6. Coordinador de Puesto
**Alcance**: Un puesto de votación específico

**Permisos**:
- ✅ Ver todas las mesas del puesto
- ✅ Monitorear testigos
- ✅ Validar formularios E-14
- ✅ Generar E-24 de puesto
- ✅ Reportar incidentes del puesto

**Dashboard**: `/coordinador/puesto`

### 7. Testigo Electoral
**Alcance**: Una mesa específica

**Permisos**:
- ✅ Registrar formulario E-14 de su mesa
- ✅ Subir fotos del E-14
- ✅ Reportar incidentes de la mesa
- ✅ Ver su propio formulario

**Dashboard**: `/testigo/dashboard`

### 8. Auditor Electoral
**Alcance**: Transversal (puede ver todo pero no modificar)

**Permisos**:
- ✅ Ver todos los formularios
- ✅ Generar reportes de auditoría
- ✅ Detectar inconsistencias
- ✅ Ver logs del sistema

**Dashboard**: `/auditor/dashboard`

---

## 🔌 Endpoints API

### Autenticación

#### POST /api/auth/login
**Descripción**: Iniciar sesión

**Request**:
```json
{
  "rol": "testigo_electoral",
  "password": "test123",
  "departamento_codigo": "44",
  "municipio_codigo": "01",
  "zona_codigo": "01",
  "puesto_codigo": "01"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "user": {
      "id": 1,
      "nombre": "testigo.01.01",
      "rol": "testigo_electoral"
    }
  }
}
```

#### POST /api/auth/logout
**Descripción**: Cerrar sesión

#### GET /api/auth/profile
**Descripción**: Obtener perfil del usuario autenticado

---

### Ubicaciones (Públicas)

#### GET /api/locations/departamentos
**Descripción**: Listar departamentos

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "departamento_codigo": "44",
      "departamento_nombre": "CAQUETA"
    }
  ]
}
```

#### GET /api/locations/municipios?departamento_codigo=44
**Descripción**: Listar municipios de un departamento

#### GET /api/locations/zonas?municipio_codigo=01
**Descripción**: Listar zonas de un municipio

#### GET /api/locations/puestos?zona_codigo=01
**Descripción**: Listar puestos de una zona

#### GET /api/locations/mesas?puesto_codigo=01
**Descripción**: Listar mesas de un puesto (requiere auth)

---

### Gestión de Usuarios (Requiere Auth)

#### GET /api/gestion-usuarios/puestos
**Descripción**: Listar puestos para gestión

**Roles**: super_admin, admin_departamental, admin_municipal

#### POST /api/gestion-usuarios/crear-testigos-puesto
**Descripción**: Crear testigos para un puesto

**Request**:
```json
{
  "puesto_id": 4,
  "cantidad": 3
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "puesto": "CAQUETA - FLORENCIA - I.E. JUAN BAUTISTA LA SALLE",
    "total_mesas": 3,
    "testigos_creados": [
      {
        "username": "testigo.01.01",
        "password": "kK2#ls$dLCs7",
        "numero": 1
      }
    ],
    "total_creados": 1,
    "espacios_disponibles": 2
  }
}
```

#### POST /api/gestion-usuarios/crear-coordinador-puesto
**Descripción**: Crear coordinador de puesto

#### POST /api/gestion-usuarios/crear-usuarios-municipio
**Descripción**: Crear coordinador y admin municipal

#### POST /api/gestion-usuarios/crear-usuarios-departamento
**Descripción**: Crear coordinador y admin departamental

---

### Formularios E-14 (Testigo)

#### GET /api/testigo/mi-mesa
**Descripción**: Obtener información de la mesa asignada

#### POST /api/testigo/formulario-e14
**Descripción**: Crear/actualizar formulario E-14

**Request**:
```json
{
  "mesa_id": 5,
  "total_votos": 450,
  "votos_partidos": [
    {"partido_id": 1, "votos": 120},
    {"partido_id": 2, "votos": 200}
  ],
  "votos_candidatos": [
    {"candidato_id": 1, "votos": 120}
  ],
  "votos_nulos": 10,
  "votos_blancos": 20,
  "tarjetas_no_marcadas": 100
}
```

#### POST /api/testigo/subir-foto
**Descripción**: Subir foto del formulario E-14

---

### Coordinador de Puesto

#### GET /api/coordinador-puesto/mesas
**Descripción**: Listar mesas del puesto

#### GET /api/coordinador-puesto/estadisticas
**Descripción**: Estadísticas del puesto

#### POST /api/coordinador-puesto/validar-e14/{id}
**Descripción**: Validar formulario E-14

#### POST /api/coordinador-puesto/generar-e24
**Descripción**: Generar E-24 del puesto

---

### Coordinador Municipal

#### GET /api/coordinador-municipal/puestos
**Descripción**: Listar puestos del municipio

#### GET /api/coordinador-municipal/estadisticas
**Descripción**: Estadísticas municipales

#### POST /api/coordinador-municipal/generar-e24
**Descripción**: Generar E-24 municipal

---

### Incidentes y Delitos

#### POST /api/incidentes
**Descripción**: Reportar incidente electoral

#### GET /api/incidentes
**Descripción**: Listar incidentes

#### POST /api/delitos
**Descripción**: Reportar delito electoral

#### GET /api/delitos
**Descripción**: Listar delitos

---

## 📊 Dashboards

### 1. Dashboard Testigo Electoral
**URL**: `/testigo/dashboard`

**Secciones**:
- 📝 Formulario E-14
- 📸 Subir fotos
- 📊 Resumen de votos
- ⚠️ Reportar incidentes

**Funcionalidades**:
- Registrar votos por partido y candidato
- Validar totales automáticamente
- Subir múltiples fotos del E-14
- Reportar incidentes de la mesa

### 2. Dashboard Coordinador de Puesto
**URL**: `/coordinador/puesto`

**Secciones**:
- 📊 Estadísticas del puesto
- 📋 Lista de mesas
- ✅ Validación de E-14
- 📄 Generar E-24 de puesto
- ⚠️ Incidentes del puesto

**Funcionalidades**:
- Ver avance por mesa
- Validar formularios E-14
- Detectar discrepancias
- Generar consolidado E-24

### 3. Dashboard Coordinador Municipal
**URL**: `/coordinador/municipal`

**Secciones**:
- 📊 Estadísticas municipales
- 🏢 Lista de puestos
- 📈 Consolidado municipal
- ⚠️ Alertas y discrepancias

**Funcionalidades**:
- Monitorear todos los puestos
- Ver avance municipal
- Comparar puestos
- Generar E-24 municipal

### 4. Dashboard Coordinador Departamental
**URL**: `/coordinador/departamental`

**Secciones**:
- 📊 Estadísticas departamentales
- 🏛️ Lista de municipios
- 📈 Consolidado departamental
- 🗺️ Mapa de avance

**Funcionalidades**:
- Monitorear todos los municipios
- Ver avance departamental
- Comparar municipios
- Exportar datos

### 5. Dashboard Admin/Super Admin
**URL**: `/admin/super-admin`

**Secciones**:
- 👥 Gestión de usuarios
- ⚙️ Configuración del sistema
- 📊 Estadísticas globales
- 🔍 Auditoría

**Funcionalidades**:
- Crear usuarios automáticamente
- Configurar partidos y candidatos
- Ver logs del sistema
- Gestionar campañas

### 6. Dashboard Auditor Electoral
**URL**: `/auditor/dashboard`

**Secciones**:
- 🔍 Auditoría de formularios
- 📊 Reportes de inconsistencias
- 📈 Análisis estadístico
- 📋 Logs del sistema

**Funcionalidades**:
- Detectar anomalías
- Generar reportes de auditoría
- Ver historial de cambios
- Exportar datos para análisis

---

## 🔄 Flujo de Trabajo

### Flujo Principal: Día de Elecciones

```
1. PREPARACIÓN (Antes del día)
   ├── Super Admin crea usuarios
   ├── Se asignan testigos a mesas
   ├── Se configuran partidos y candidatos
   └── Se verifica conectividad

2. DÍA DE ELECCIONES
   ├── Testigos hacen login
   ├── Seleccionan su mesa
   ├── Esperan cierre de votación
   └── Registran resultados (E-14)

3. REGISTRO DE VOTOS (Por Testigo)
   ├── Ingresar votos por partido
   ├── Ingresar votos por candidato
   ├── Ingresar votos nulos/blancos
   ├── Subir fotos del E-14
   └── Enviar formulario

4. VALIDACIÓN (Coordinador de Puesto)
   ├── Revisar E-14 de cada mesa
   ├── Validar totales
   ├── Solicitar correcciones si hay errores
   └── Aprobar formularios

5. CONSOLIDACIÓN PUESTO
   ├── Generar E-24 de puesto
   ├── Verificar totales
   └── Enviar a nivel municipal

6. CONSOLIDACIÓN MUNICIPAL
   ├── Revisar E-24 de todos los puestos
   ├── Generar E-24 municipal
   └── Enviar a nivel departamental

7. CONSOLIDACIÓN DEPARTAMENTAL
   ├── Revisar E-24 de todos los municipios
   ├── Generar E-24 departamental
   └── Resultados finales

8. AUDITORÍA
   ├── Auditor revisa todo el proceso
   ├── Detecta inconsistencias
   ├── Genera reportes
   └── Certifica resultados
```

### Flujo de Gestión de Usuarios

```
1. Super Admin accede a /admin/gestion-usuarios

2. Selecciona tipo de usuario a crear:
   ├── Testigos por Puesto
   ├── Coordinador de Puesto
   ├── Usuarios Municipales
   └── Usuarios Departamentales

3. Selecciona ubicación (puesto/municipio/departamento)

4. Sistema genera usuarios automáticamente:
   ├── Username: testigo.{puesto}.{numero}
   ├── Password: Aleatorio seguro (12 caracteres)
   └── Asignación a ubicación

5. Sistema muestra credenciales:
   ├── Modal con username y password
   ├── Opción de copiar
   └── Opción de descargar

6. Admin distribuye credenciales a los usuarios
```

### Flujo de Validación de E-14

```
1. Testigo registra E-14
   ├── Ingresa votos
   ├── Sistema valida totales
   └── Sube fotos

2. Sistema verifica:
   ├── Total votos = suma de todos los votos
   ├── No hay valores negativos
   └── Campos requeridos completos

3. Coordinador de Puesto revisa:
   ├── Ve formulario y fotos
   ├── Compara con otros datos
   └── Decide: Aprobar o Rechazar

4. Si hay discrepancias:
   ├── Coordinador marca discrepancia
   ├── Testigo recibe notificación
   ├── Testigo corrige
   └── Se repite validación

5. Una vez aprobado:
   ├── E-14 queda bloqueado
   ├── Se incluye en consolidado
   └── Pasa a nivel superior
```

---

## 📖 Guía de Uso por Rol

### Para Testigos Electorales

**1. Acceso al Sistema**
```
URL: http://sistema.com/auth/login
Rol: Testigo Electoral
Departamento: CAQUETA
Municipio: [Tu municipio]
Zona: [Tu zona]
Puesto: [Tu puesto]
Contraseña: [Proporcionada por coordinador]
```

**2. Seleccionar Mesa**
- Al entrar, selecciona tu mesa del dropdown
- Verifica que sea la correcta

**3. Registrar Votos**
- Espera al cierre de votación
- Ingresa votos por cada partido
- Ingresa votos por cada candidato
- Ingresa votos nulos, blancos y tarjetas no marcadas
- El sistema valida automáticamente los totales

**4. Subir Fotos**
- Toma fotos claras del E-14 físico
- Sube mínimo 2 fotos (anverso y reverso)
- Verifica que se vean todos los números

**5. Enviar Formulario**
- Revisa todos los datos
- Haz clic en "Enviar Formulario"
- Espera confirmación

**6. Reportar Incidentes**
- Si hay irregularidades, usa el botón "Reportar Incidente"
- Describe detalladamente lo ocurrido
- Sube fotos si es posible

### Para Coordinadores de Puesto

**1. Monitorear Avance**
- Ve el dashboard con todas las mesas
- Identifica mesas pendientes (en rojo)
- Contacta testigos que no han reportado

**2. Validar Formularios**
- Revisa cada E-14 recibido
- Compara con fotos
- Verifica totales

**3. Gestionar Discrepancias**
- Si encuentras errores, marca como "Requiere Corrección"
- Agrega comentario explicando el error
- Notifica al testigo

**4. Generar E-24**
- Cuando todos los E-14 estén validados
- Haz clic en "Generar E-24 de Puesto"
- Revisa el consolidado
- Confirma y envía

### Para Coordinadores Municipales

**1. Monitorear Puestos**
- Ve todos los puestos del municipio
- Identifica puestos con retrasos
- Contacta coordinadores de puesto

**2. Revisar Consolidados**
- Verifica E-24 de cada puesto
- Compara datos entre puestos
- Detecta anomalías

**3. Generar E-24 Municipal**
- Cuando todos los puestos estén completos
- Genera consolidado municipal
- Revisa totales
- Envía a nivel departamental

### Para Super Admin

**1. Crear Usuarios**
- Accede a /admin/gestion-usuarios
- Selecciona tipo de usuario
- Elige ubicación
- Genera usuarios
- Descarga credenciales
- Distribuye a coordinadores

**2. Configurar Sistema**
- Agrega partidos políticos
- Agrega candidatos
- Configura parámetros
- Gestiona campañas

**3. Monitorear Sistema**
- Ve estadísticas globales
- Revisa logs
- Detecta problemas
- Toma acciones correctivas

---

## 🔑 Credenciales de Acceso

### Usuarios de Prueba

#### Super Admin
```
Rol: super_admin
Password: admin123
```

#### Testigos (Formato)
```
Username: testigo.{puesto_codigo}.{numero}
Ejemplo: testigo.01.01
Password: [Generado automáticamente]
```

#### Coordinadores de Puesto (Formato)
```
Username: coord.puesto.{puesto_codigo}
Ejemplo: coord.puesto.01
Password: [Generado automáticamente]
```

#### Coordinadores Municipales (Formato)
```
Username: coord.mun.{municipio_codigo}
Ejemplo: coord.mun.01
Password: [Generado automáticamente]
```

### Contraseña de Testing
Para pruebas, todos los usuarios usan:
```
Password: test123
```

---

## 🚀 Inicio Rápido

### 1. Iniciar Aplicación
```bash
python run.py
```

### 2. Acceder al Sistema
```
URL: http://127.0.0.1:5000
```

### 3. Login como Super Admin
```
http://127.0.0.1:5000/auth/login
Rol: super_admin
Password: admin123
```

### 4. Crear Usuarios
```
http://127.0.0.1:5000/admin/gestion-usuarios
```

### 5. Distribuir Credenciales
- Descarga el archivo de credenciales
- Envía a cada coordinador/testigo

### 6. Día de Elecciones
- Testigos hacen login
- Registran resultados
- Coordinadores validan
- Sistema consolida automáticamente

---

## 📞 Soporte

### Problemas Comunes

**1. No puedo hacer login**
- Verifica que el rol sea correcto
- Verifica la contraseña
- Verifica que hayas seleccionado la ubicación correcta

**2. Los selectores están vacíos**
- Refresca la página (Ctrl+F5)
- Verifica que la aplicación esté corriendo
- Abre la consola del navegador (F12) y busca errores

**3. El formulario no se envía**
- Verifica que todos los campos estén completos
- Verifica que los totales cuadren
- Revisa la consola del navegador

**4. No veo mi dashboard**
- Verifica que hayas hecho login correctamente
- Verifica que tu rol tenga permisos
- Limpia el caché del navegador

---

**Última actualización**: 2025-11-16 20:30:00  
**Versión del Sistema**: 1.0  
**Estado**: ✅ PRODUCCIÓN
