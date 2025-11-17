# GUÍA COMPLETA: FLUJO DE ROLES Y DATOS DEL SISTEMA ELECTORAL

## 📋 ÍNDICE
1. [Super Admin](#1-super-admin)
2. [Testigo Electoral](#2-testigo-electoral)
3. [Coordinador de Puesto](#3-coordinador-de-puesto)
4. [Coordinador Municipal](#4-coordinador-municipal)
5. [Coordinador Departamental](#5-coordinador-departamental)
6. [Auditor Electoral](#6-auditor-electoral)
7. [Flujo Completo de Datos](#7-flujo-completo-de-datos)

---

## 1. SUPER ADMIN

### 🎯 Responsabilidades
- Configuración inicial del sistema
- Gestión de campañas electorales
- Gestión de partidos y candidatos
- Creación masiva de usuarios
- Supervisión general del sistema
- Monitoreo de estadísticas globales

### 📥 Cómo Ingresa Datos

#### A. Configuración Electoral
**Interfaz:** Dashboard Super Admin → Configuración Electoral
**Endpoint:** `POST /api/super-admin/campanas`
```json
{
  "nombre": "Elecciones Presidenciales 2026",
  "fecha_inicio": "2026-01-01",
  "fecha_fin": "2026-05-30",
  "activa": true
}
```

#### B. Crear Partidos
**Interfaz:** Dashboard Super Admin → Gestión de Partidos
**Endpoint:** `POST /api/configuracion/partidos`
```json
{
  "nombre": "Partido Liberal",
  "sigla": "PL",
  "numero_lista": 1,
  "color": "#FF0000",
  "logo_url": "https://...",
  "activo": true
}
```

#### C. Crear Candidatos
**Interfaz:** Dashboard Super Admin → Gestión de Candidatos
**Endpoint:** `POST /api/configuracion/candidatos`
```json
{
  "nombre_completo": "Juan Pérez",
  "partido_id": 1,
  "tipo_eleccion_id": 1,
  "numero_lista": 101,
  "foto_url": "https://...",
  "activo": true
}
```

#### D. Crear Usuarios Masivamente
**Interfaz:** Dashboard Super Admin → Gestión de Usuarios → Carga Masiva
**Endpoint:** `POST /api/gestion-usuarios/crear-masivo`
```json
{
  "usuarios": [
    {
      "username": "testigo_001",
      "nombre": "María García",
      "rol": "testigo_electoral",
      "ubicacion_id": 123,
      "email": "maria@example.com"
    }
  ]
}
```

### 📤 Qué Recibe
- Estadísticas globales del sistema
- Total de formularios E14 por estado
- Resumen de incidentes y delitos
- Estado de todas las campañas
- Métricas de participación

**Endpoint:** `GET /api/super-admin/stats`
```json
{
  "total_usuarios": 1500,
  "total_formularios": 850,
  "formularios_validados": 720,
  "formularios_pendientes": 130,
  "total_incidentes": 45,
  "total_delitos": 12,
  "porcentaje_avance": 85.5
}
```

### 🔄 A Dónde Van Sus Datos
- **Partidos y Candidatos** → Disponibles para todos los roles
- **Usuarios creados** → Pueden hacer login según su rol
- **Campañas** → Activan/desactivan funcionalidades del sistema
- **Configuraciones** → Afectan el comportamiento global

---

## 2. TESTIGO ELECTORAL

### 🎯 Responsabilidades
- Registrar su presencia en la mesa
- Crear formularios E14 con resultados de votación
- Reportar incidentes y delitos
- Tomar fotos del formulario físico E14
- Enviar datos desde la mesa electoral

### 📥 Cómo Ingresa Datos

#### A. Registrar Presencia
**Interfaz:** Dashboard Testigo → Botón "Registrar Presencia"
**Endpoint:** `POST /api/testigo/registrar-presencia`
```json
{
  "ubicacion_actual": {
    "latitud": 4.6097,
    "longitud": -74.0817
  }
}
```

#### B. Crear Formulario E14
**Interfaz:** Dashboard Testigo → Formulario E14
**Endpoint:** `POST /api/formularios`
```json
{
  "mesa_id": 123,
  "tipo_eleccion_id": 1,
  "total_votantes_registrados": 300,
  "total_votos": 285,
  "votos_validos": 270,
  "votos_nulos": 10,
  "votos_blanco": 5,
  "tarjetas_no_marcadas": 15,
  "total_tarjetas": 300,
  "estado": "pendiente",
  "observaciones": "Votación transcurrió con normalidad",
  "votos_candidatos": [
    {
      "candidato_id": 1,
      "votos": 120
    },
    {
      "candidato_id": 2,
      "votos": 150
    }
  ],
  "votos_partidos": [
    {
      "partido_id": 1,
      "votos": 120
    },
    {
      "partido_id": 2,
      "votos": 150
    }
  ]
}
```

#### C. Reportar Incidente
**Interfaz:** Dashboard Testigo → Reportar Incidente
**Endpoint:** `POST /api/testigo/incidentes`
```json
{
  "tipo": "retraso_apertura",
  "descripcion": "Mesa abrió 30 minutos tarde",
  "gravedad": "media",
  "ubicacion_id": 123,
  "foto_url": "https://..."
}
```

#### D. Reportar Delito
**Interfaz:** Dashboard Testigo → Reportar Delito
**Endpoint:** `POST /api/testigo/delitos`
```json
{
  "tipo": "compra_votos",
  "descripcion": "Se observó entrega de dinero",
  "gravedad": "alta",
  "ubicacion_id": 123,
  "evidencia_url": "https://..."
}
```

### 📤 Qué Recibe
- Lista de candidatos disponibles para su tipo de elección
- Estado de sus formularios enviados
- Confirmación de recepción de reportes
- Notificaciones de validación/rechazo

**Endpoints de consulta:**
- `GET /api/configuracion/candidatos` - Candidatos disponibles
- `GET /api/formularios/mis-formularios` - Sus formularios
- `GET /api/testigo/stats` - Sus estadísticas

### 🔄 A Dónde Van Sus Datos
- **Formulario E14** → Coordinador de Puesto (para validación)
- **Incidentes/Delitos** → Coordinadores y Auditores
- **Presencia** → Visible para Coordinador de Puesto
- **Fotos** → Almacenadas para auditoría

### 💾 Funcionalidad Offline
El testigo puede:
- Guardar borradores localmente (LocalStorage)
- Trabajar sin conexión
- Sincronizar cuando recupere conexión

---

## 3. COORDINADOR DE PUESTO

### 🎯 Responsabilidades
- Supervisar todas las mesas de su puesto
- Validar o rechazar formularios E14 de testigos
- Monitorear presencia de testigos
- Gestionar incidentes del puesto
- Generar consolidado del puesto (E24)

### 📥 Cómo Ingresa Datos

#### A. Validar Formulario E14
**Interfaz:** Dashboard Coordinador Puesto → Formularios Pendientes → Validar
**Endpoint:** `PUT /api/formularios/{id}/validar`
```json
{
  "cambios": {
    "votos_nulos": 12,
    "observaciones": "Corrección de votos nulos"
  },
  "comentario": "Se corrigió conteo de votos nulos"
}
```

#### B. Rechazar Formulario E14
**Interfaz:** Dashboard Coordinador Puesto → Formularios Pendientes → Rechazar
**Endpoint:** `PUT /api/formularios/{id}/rechazar`
```json
{
  "motivo": "Inconsistencia en totales. Total de votos no coincide con suma de candidatos."
}
```

#### C. Reportar Incidente del Puesto
**Interfaz:** Dashboard Coordinador Puesto → Incidentes
**Endpoint:** `POST /api/coordinador-puesto/incidentes`
```json
{
  "tipo": "falla_electrica",
  "descripcion": "Corte de luz en el puesto",
  "gravedad": "alta",
  "mesas_afectadas": [123, 124, 125]
}
```

### 📤 Qué Recibe
- Lista de todas las mesas de su puesto
- Formularios E14 pendientes de validación
- Estado de presencia de testigos
- Estadísticas del puesto

**Endpoints de consulta:**
- `GET /api/coordinador-puesto/stats` - Estadísticas del puesto
- `GET /api/formularios/puesto` - Formularios del puesto
- `GET /api/formularios/mesas` - Mesas con estado
- `GET /api/coordinador-puesto/testigos` - Testigos del puesto
- `GET /api/formularios/consolidado` - Consolidado del puesto

**Ejemplo de respuesta de stats:**
```json
{
  "total_mesas": 10,
  "total_testigos": 10,
  "testigos_presentes": 9,
  "total_formularios": 8,
  "formularios_completados": 6,
  "formularios_pendientes": 2,
  "porcentaje_avance": 80.0,
  "puesto": {
    "id": 5,
    "nombre": "Puesto 01 - Escuela Central",
    "codigo": "01"
  }
}
```

### 🔄 A Dónde Van Sus Datos
- **Formularios validados** → Consolidado municipal
- **Formularios rechazados** → Devueltos al testigo
- **Incidentes** → Coordinador Municipal y Auditores
- **Consolidado E24** → Coordinador Municipal

---

## 4. COORDINADOR MUNICIPAL

### 🎯 Responsabilidades
- Supervisar todos los puestos del municipio
- Consolidar resultados de todos los puestos
- Revisar formularios E24 de puestos
- Gestionar incidentes municipales
- Generar consolidado municipal (E26)


### 📥 Cómo Ingresa Datos

#### A. Validar Consolidado de Puesto
**Interfaz:** Dashboard Coordinador Municipal → Puestos → Validar Consolidado
**Endpoint:** `PUT /api/coordinador-municipal/consolidados/{puesto_id}/validar`
```json
{
  "aprobado": true,
  "comentario": "Consolidado correcto"
}
```

#### B. Solicitar Corrección
**Interfaz:** Dashboard Coordinador Municipal → Puestos → Solicitar Corrección
**Endpoint:** `PUT /api/coordinador-municipal/consolidados/{puesto_id}/corregir`
```json
{
  "motivo": "Discrepancia entre E14 y E24 en mesa 5",
  "detalles": "Revisar conteo de votos nulos"
}
```

### 📤 Qué Recibe
- Lista de todos los puestos del municipio
- Consolidados de cada puesto (E24)
- Formularios E14 de todas las mesas
- Estadísticas municipales

**Endpoints de consulta:**
- `GET /api/coordinador-municipal/stats` - Estadísticas municipales
- `GET /api/coordinador-municipal/puestos` - Puestos con estado
- `GET /api/coordinador-municipal/consolidado` - Consolidado municipal
- `GET /api/coordinador-municipal/incidentes` - Incidentes del municipio

### 🔄 A Dónde Van Sus Datos
- **Consolidado municipal** → Coordinador Departamental
- **Validaciones** → Confirmadas en el sistema
- **Solicitudes de corrección** → Coordinadores de Puesto

---

## 5. COORDINADOR DEPARTAMENTAL

### 🎯 Responsabilidades
- Supervisar todos los municipios del departamento
- Consolidar resultados departamentales
- Revisar consolidados municipales (E26)
- Gestionar incidentes departamentales
- Generar consolidado departamental (E28)

### 📥 Cómo Ingresa Datos

#### A. Validar Consolidado Municipal
**Interfaz:** Dashboard Coordinador Departamental → Municipios → Validar
**Endpoint:** `PUT /api/coordinador-departamental/consolidados/{municipio_id}/validar`
```json
{
  "aprobado": true,
  "comentario": "Consolidado municipal aprobado"
}
```

### 📤 Qué Recibe
- Lista de todos los municipios del departamento
- Consolidados municipales (E26)
- Estadísticas departamentales
- Resumen de incidentes

**Endpoints de consulta:**
- `GET /api/coordinador-departamental/stats` - Estadísticas departamentales
- `GET /api/coordinador-departamental/municipios` - Municipios con estado
- `GET /api/coordinador-departamental/consolidado` - Consolidado departamental

### 🔄 A Dónde Van Sus Datos
- **Consolidado departamental** → Sistema nacional
- **Validaciones** → Confirmadas en el sistema
- **Reportes** → Auditores y Super Admin

---

## 6. AUDITOR ELECTORAL

### 🎯 Responsabilidades
- Auditar todos los formularios del sistema
- Revisar inconsistencias
- Generar reportes de auditoría
- Monitorear integridad de datos
- Acceso de solo lectura a todo el sistema

### 📥 Cómo Ingresa Datos

#### A. Crear Reporte de Auditoría
**Interfaz:** Dashboard Auditor → Crear Reporte
**Endpoint:** `POST /api/auditor/reportes`
```json
{
  "tipo": "inconsistencia",
  "titulo": "Discrepancia en Puesto 05",
  "descripcion": "Se detectó diferencia entre E14 y E24",
  "gravedad": "alta",
  "formularios_afectados": [123, 124],
  "recomendaciones": "Revisar conteo manual"
}
```

### 📤 Qué Recibe
- Acceso a TODOS los formularios E14
- Todos los consolidados (E24, E26, E28)
- Todos los incidentes y delitos
- Historial de cambios (auditoría)
- Estadísticas globales

**Endpoints de consulta:**
- `GET /api/auditor/stats` - Estadísticas globales
- `GET /api/auditor/formularios` - Todos los formularios
- `GET /api/auditor/inconsistencias` - Inconsistencias detectadas
- `GET /api/auditor/historial/{formulario_id}` - Historial de cambios
- `GET /api/auditor/reportes` - Reportes de auditoría

### 🔄 A Dónde Van Sus Datos
- **Reportes de auditoría** → Super Admin y Coordinadores
- **Alertas** → Notificaciones a roles relevantes
- **Recomendaciones** → Para corrección de datos

---

## 7. FLUJO COMPLETO DE DATOS

### 📊 Flujo Principal: Formulario E14

```
1. TESTIGO ELECTORAL (Mesa)
   ↓ Crea formulario E14
   ↓ POST /api/formularios
   ↓ Estado: "pendiente"
   
2. COORDINADOR DE PUESTO
   ↓ Recibe notificación
   ↓ GET /api/formularios/puesto
   ↓ Revisa formulario
   ↓
   ├─→ PUT /api/formularios/{id}/validar
   │   Estado: "validado"
   │   ↓
   │   Consolidado de Puesto (E24)
   │   ↓
   │
   └─→ PUT /api/formularios/{id}/rechazar
       Estado: "rechazado"
       ↓
       Notificación a Testigo
       ↓
       Testigo corrige y reenvía

3. COORDINADOR MUNICIPAL
   ↓ Recibe consolidados de puestos
   ↓ GET /api/coordinador-municipal/puestos
   ↓ Valida consolidados E24
   ↓ Genera consolidado municipal (E26)
   
4. COORDINADOR DEPARTAMENTAL
   ↓ Recibe consolidados municipales
   ↓ GET /api/coordinador-departamental/municipios
   ↓ Valida consolidados E26
   ↓ Genera consolidado departamental (E28)
   
5. AUDITOR ELECTORAL
   ↓ Monitorea todo el proceso
   ↓ GET /api/auditor/formularios
   ↓ Detecta inconsistencias
   ↓ POST /api/auditor/reportes
   
6. SUPER ADMIN
   ↓ Supervisa sistema completo
   ↓ GET /api/super-admin/stats
   ↓ Toma decisiones finales
```

### 🔄 Flujo de Incidentes

```
TESTIGO o COORDINADOR
   ↓ Reporta incidente
   ↓ POST /api/testigo/incidentes
   ↓
   ├─→ COORDINADOR DE PUESTO
   │   ↓ Ve incidentes de su puesto
   │   ↓ GET /api/coordinador-puesto/incidentes
   │
   ├─→ COORDINADOR MUNICIPAL
   │   ↓ Ve incidentes del municipio
   │   ↓ GET /api/coordinador-municipal/incidentes
   │
   ├─→ AUDITOR
   │   ↓ Ve todos los incidentes
   │   ↓ GET /api/auditor/incidentes
   │
   └─→ SUPER ADMIN
       ↓ Ve todos los incidentes
       ↓ GET /api/super-admin/incidentes
```

### 📈 Estados del Formulario E14

```
borrador → El testigo está llenando el formulario (guardado local)
   ↓
pendiente → Enviado, esperando validación del coordinador
   ↓
   ├─→ validado → Aprobado por coordinador, va a consolidado
   │
   └─→ rechazado → Devuelto al testigo para corrección
           ↓
       pendiente → Testigo corrige y reenvía
```

### 🗄️ Estructura de Datos

```
DIVIPOLA (Ubicaciones)
├── Departamento (ej: Caquetá - código 18)
│   ├── Municipio (ej: Florencia - código 001)
│   │   ├── Zona (ej: Urbana - código 01)
│   │   │   ├── Puesto (ej: Puesto 01 - código 01)
│   │   │   │   ├── Mesa 1 (código 001)
│   │   │   │   ├── Mesa 2 (código 002)
│   │   │   │   └── Mesa N

USUARIOS
├── Super Admin (sin ubicación específica)
├── Auditor Electoral (sin ubicación específica)
├── Coordinador Departamental (ubicación_id = Departamento)
├── Coordinador Municipal (ubicación_id = Municipio)
├── Coordinador de Puesto (ubicación_id = Puesto)
└── Testigo Electoral (ubicación_id = Mesa)

FORMULARIOS E14
├── mesa_id (FK a Location tipo 'mesa')
├── testigo_id (FK a User rol 'testigo_electoral')
├── tipo_eleccion_id (FK a TipoEleccion)
├── estado (borrador/pendiente/validado/rechazado)
├── votos_candidatos (relación 1:N con VotoCandidato)
└── votos_partidos (relación 1:N con VotoPartido)
```

### 🔐 Permisos por Rol

| Acción | Super Admin | Auditor | Coord. Depto | Coord. Muni | Coord. Puesto | Testigo |
|--------|-------------|---------|--------------|-------------|---------------|---------|
| Crear E14 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Validar E14 | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Ver todos E14 | ✅ | ✅ | ✅ (depto) | ✅ (muni) | ✅ (puesto) | ✅ (propios) |
| Crear usuarios | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Configurar candidatos | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Reportar incidentes | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Ver reportes auditoría | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## 📱 EJEMPLOS PRÁCTICOS

### Ejemplo 1: Testigo Registra Votos

**Paso 1:** Testigo inicia sesión
```bash
POST /api/auth/login
{
  "username": "testigo_mesa_001",
  "password": "test123"
}
```

**Paso 2:** Obtiene candidatos disponibles
```bash
GET /api/configuracion/candidatos
```

**Paso 3:** Llena formulario E14
```bash
POST /api/formularios
{
  "mesa_id": 123,
  "tipo_eleccion_id": 1,
  "total_votos": 285,
  "votos_candidatos": [
    {"candidato_id": 1, "votos": 120},
    {"candidato_id": 2, "votos": 150}
  ],
  "estado": "pendiente"
}
```

### Ejemplo 2: Coordinador Valida Formulario

**Paso 1:** Coordinador ve formularios pendientes
```bash
GET /api/formularios/puesto?estado=pendiente
```

**Paso 2:** Revisa detalles del formulario
```bash
GET /api/formularios/123
```

**Paso 3:** Valida el formulario
```bash
PUT /api/formularios/123/validar
{
  "comentario": "Formulario correcto"
}
```

### Ejemplo 3: Auditor Revisa Inconsistencias

**Paso 1:** Obtiene todos los formularios
```bash
GET /api/auditor/formularios
```

**Paso 2:** Detecta inconsistencia
```bash
GET /api/auditor/inconsistencias
```

**Paso 3:** Crea reporte
```bash
POST /api/auditor/reportes
{
  "tipo": "inconsistencia",
  "descripcion": "Total de votos no coincide",
  "formularios_afectados": [123]
}
```

---

## 🎓 RESUMEN RÁPIDO

### ¿Quién crea qué?

- **Super Admin** → Campañas, Partidos, Candidatos, Usuarios
- **Testigo** → Formularios E14, Incidentes, Delitos
- **Coordinador Puesto** → Validaciones, Consolidado E24
- **Coordinador Municipal** → Consolidado E26
- **Coordinador Departamental** → Consolidado E28
- **Auditor** → Reportes de auditoría

### ¿Quién ve qué?

- **Super Admin** → TODO
- **Auditor** → TODO (solo lectura)
- **Coordinador Departamental** → Su departamento completo
- **Coordinador Municipal** → Su municipio completo
- **Coordinador Puesto** → Su puesto completo
- **Testigo** → Solo su mesa y sus formularios

### Flujo de validación

```
Testigo → Coordinador Puesto → Coordinador Municipal → Coordinador Departamental → Sistema Nacional
          (valida E14)         (valida E24)            (valida E26)
                                                                    
Auditor → Monitorea todo el proceso en paralelo
```

---

## 📞 SOPORTE

Para más información sobre endpoints específicos, consultar:
- `backend/routes/` - Código fuente de endpoints
- `CREDENCIALES_USUARIOS.md` - Usuarios de prueba
- `GUIA_COMPLETA_SISTEMA_ELECTORAL.md` - Documentación técnica
