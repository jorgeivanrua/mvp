# 🔍 FLUJO COMPLETO DEL SISTEMA ELECTORAL - VERIFICADO

**Fecha:** 2025-11-16  
**Estado:** ✅ VERIFICADO Y DOCUMENTADO

---

## 📋 ÍNDICE

1. [Autenticación](#autenticación)
2. [Testigo Electoral](#testigo-electoral)
3. [Coordinador de Puesto](#coordinador-de-puesto)
4. [Admin Municipal](#admin-municipal)
5. [Coordinador Departamental](#coordinador-departamental)
6. [Auditor Electoral](#auditor-electoral)
7. [Super Admin](#super-admin)

---

## 🔐 AUTENTICACIÓN

### Login Jerárquico

**Endpoint:** `POST /api/auth/login`

**Body:**
```json
{
  "rol": "string",
  "departamento_codigo": "string",  // Opcional según rol
  "municipio_codigo": "string",     // Opcional según rol
  "puesto_codigo": "string",        // Opcional según rol
  "password": "string"
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "nombre": "Testigo Electoral",
    "rol": "testigo_electoral"
  }
}
```

### Verificar Presencia

**Endpoint:** `POST /api/auth/verificar-presencia`

**Headers:** `Authorization: Bearer {token}`

**Respuesta:**
```json
{
  "success": true,
  "message": "Presencia verificada exitosamente",
  "data": {
    "presencia_verificada": true,
    "presencia_verificada_at": "2025-11-16T12:00:00",
    "coordinador_notificado": true
  }
}
```

---

## 👁️ TESTIGO ELECTORAL

### 1. Login

```json
{
  "rol": "testigo_electoral",
  "departamento_codigo": "44",
  "municipio_codigo": "01",
  "puesto_codigo": "001",
  "password": "test123"
}
```

### 2. Verificar Presencia

**Endpoint:** `POST /api/auth/verificar-presencia`

### 3. Obtener Información del Puesto/Mesas

**Endpoint:** `GET /api/testigo/mesa`

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "puesto": {
      "id": 402,
      "nombre_completo": "CAQUETA - FLORENCIA - Colegio Nacional",
      "tipo": "puesto"
    },
    "mesas": [
      {
        "id": 403,
        "mesa_codigo": "001",
        "mesa_nombre": "Mesa 1",
        "total_votantes_registrados": 300
      },
      {
        "id": 404,
        "mesa_codigo": "002",
        "mesa_nombre": "Mesa 2",
        "total_votantes_registrados": 300
      }
    ]
  }
}
```

### 4. Obtener Tipos de Elección

**Endpoint:** `GET /api/testigo/tipos-eleccion`

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "codigo": "PRESIDENTE",
      "nombre": "Presidente",
      "es_uninominal": true,
      "permite_lista_cerrada": false
    }
  ]
}
```

### 5. Obtener Partidos Políticos

**Endpoint:** `GET /api/testigo/partidos`

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Partido Liberal",
      "sigla": "PL",
      "color": "#FF0000"
    }
  ]
}
```

### 6. Obtener Candidatos

**Endpoint:** `GET /api/testigo/candidatos?tipo_eleccion_id=1`

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "partido": "Partido Liberal",
      "partido_id": 1,
      "numero_lista": 1
    }
  ]
}
```

### 7. Registrar Formulario E-14

**Endpoint:** `POST /api/formularios`

**Body:**
```json
{
  "mesa_id": 403,
  "tipo_eleccion_id": 1,
  "total_votantes_registrados": 300,
  "total_votos": 367,
  "votos_validos": 350,
  "votos_nulos": 5,
  "votos_blanco": 10,
  "tarjetas_no_marcadas": 2,
  "total_tarjetas": 367,
  "estado": "pendiente",
  "observaciones": "Sin novedad",
  "votos_partidos": [
    {
      "partido_id": 1,
      "votos": 150
    },
    {
      "partido_id": 2,
      "votos": 120
    }
  ],
  "votos_candidatos": [
    {
      "candidato_id": 1,
      "votos": 150
    },
    {
      "candidato_id": 2,
      "votos": 120
    }
  ]
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Formulario creado exitosamente",
  "data": {
    "id": 1,
    "mesa_id": 403,
    "tipo_eleccion_id": 1,
    "estado": "pendiente",
    "created_at": "2025-11-16T12:00:00"
  }
}
```

### 8. Registrar Incidente

**Endpoint:** `POST /api/incidentes`

**Body:**
```json
{
  "tipo": "retraso_apertura",
  "descripcion": "La mesa abrió 30 minutos tarde",
  "gravedad": "media",
  "mesa_id": 403,
  "evidencia_fotografica": false
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Incidente registrado exitosamente",
  "data": {
    "id": 1,
    "tipo": "retraso_apertura",
    "estado": "reportado",
    "created_at": "2025-11-16T12:00:00"
  }
}
```

### 9. Registrar Delito Electoral

**Endpoint:** `POST /api/delitos`

**Body:**
```json
{
  "tipo_delito": "compra_votos",
  "descripcion": "Se observó entrega de dinero a votantes",
  "gravedad": "alta",
  "mesa_id": 403,
  "evidencia_fotografica": true,
  "testigos_adicionales": 2,
  "requiere_denuncia_formal": true
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Delito electoral registrado exitosamente",
  "data": {
    "id": 1,
    "tipo_delito": "compra_votos",
    "estado": "reportado",
    "created_at": "2025-11-16T12:00:00"
  }
}
```

### 10. Consultar Mis Formularios

**Endpoint:** `GET /api/formularios/mis-formularios`

### 11. Consultar Mis Incidentes

**Endpoint:** `GET /api/incidentes?usuario_id={user_id}`

### 12. Consultar Mis Delitos

**Endpoint:** `GET /api/delitos?usuario_id={user_id}`

---

## 👮 COORDINADOR DE PUESTO

### 1. Login

```json
{
  "rol": "coordinador_puesto",
  "departamento_codigo": "44",
  "municipio_codigo": "01",
  "puesto_codigo": "001",
  "password": "test123"
}
```

### 2. Consultar Mesas del Puesto

**Endpoint:** `GET /api/coordinador-puesto/mesas`

### 3. Consultar Formularios del Puesto

**Endpoint:** `GET /api/formularios/puesto`

### 4. Consultar Incidentes del Puesto

**Endpoint:** `GET /api/incidentes?puesto_id={puesto_id}`

### 5. Consultar Delitos del Puesto

**Endpoint:** `GET /api/delitos?puesto_id={puesto_id}`

### 6. Consultar Testigos del Puesto

**Endpoint:** `GET /api/formularios/testigos-puesto`

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 10,
      "nombre": "Testigo Electoral Mesa 001",
      "presencia_verificada": true,
      "presencia_verificada_at": "2025-11-16T08:00:00",
      "formularios_registrados": 2
    }
  ]
}
```

### 7. Estadísticas del Puesto

**Endpoint:** `GET /api/coordinador-puesto/estadisticas`

---

## 🏛️ ADMIN MUNICIPAL

### 1. Login

```json
{
  "rol": "admin_municipal",
  "departamento_codigo": "44",
  "municipio_codigo": "01",
  "password": "test123"
}
```

### 2. Consultar Puestos del Municipio

**Endpoint:** `GET /api/admin-municipal/puestos`

### 3. Consultar Formularios del Municipio

**Endpoint:** `GET /api/admin-municipal/formularios-e14`

### 4. Estadísticas Municipales

**Endpoint:** `GET /api/admin-municipal/estadisticas`

---

## 🗺️ COORDINADOR DEPARTAMENTAL

### 1. Login

```json
{
  "rol": "coordinador_departamental",
  "departamento_codigo": "44",
  "password": "test123"
}
```

### 2. Consultar Municipios del Departamento

**Endpoint:** `GET /api/coordinador-departamental/municipios`

### 3. Consultar Formularios del Departamento

**Endpoint:** `GET /api/coordinador-departamental/formularios-e14`

### 4. Estadísticas Departamentales

**Endpoint:** `GET /api/coordinador-departamental/estadisticas`

---

## 🔍 AUDITOR ELECTORAL

### 1. Login

```json
{
  "rol": "auditor_electoral",
  "password": "test123"
}
```

### 2. Consultar Todos los Formularios

**Endpoint:** `GET /api/auditor/formularios-e14`

### 3. Consultar Todos los Incidentes

**Endpoint:** `GET /api/incidentes` (sin filtros)

### 4. Consultar Todos los Delitos

**Endpoint:** `GET /api/delitos` (sin filtros)

### 5. Detectar Inconsistencias

**Endpoint:** `GET /api/auditor/inconsistencias`

### 6. Resultados por Tipo de Elección

**Endpoint:** `GET /api/auditor/resultados?tipo_eleccion_id=1`

### 7. Estadísticas Generales

**Endpoint:** `GET /api/auditor/estadisticas`

---

## ⚙️ SUPER ADMIN

### 1. Login

```json
{
  "rol": "super_admin",
  "password": "test123"
}
```

### 2. Gestionar Campañas

- **GET** `/api/super-admin/campanas` - Listar campañas
- **POST** `/api/super-admin/campanas` - Crear campaña
- **PUT** `/api/super-admin/campanas/{id}` - Actualizar campaña

### 3. Gestionar Tipos de Elección

- **GET** `/api/super-admin/tipos-eleccion` - Listar tipos
- **POST** `/api/super-admin/tipos-eleccion` - Crear tipo
- **PUT** `/api/super-admin/tipos-eleccion/{id}` - Actualizar tipo

### 4. Gestionar Partidos

- **GET** `/api/super-admin/partidos` - Listar partidos
- **POST** `/api/super-admin/partidos` - Crear partido
- **PUT** `/api/super-admin/partidos/{id}` - Actualizar partido

### 5. Gestionar Candidatos

- **GET** `/api/super-admin/candidatos` - Listar candidatos
- **POST** `/api/super-admin/candidatos` - Crear candidato
- **PUT** `/api/super-admin/candidatos/{id}` - Actualizar candidato

### 6. Gestionar Usuarios

- **GET** `/api/super-admin/usuarios` - Listar usuarios
- **POST** `/api/super-admin/usuarios` - Crear usuario
- **PUT** `/api/super-admin/usuarios/{id}` - Actualizar usuario

### 7. Estadísticas Globales

**Endpoint:** `GET /api/super-admin/estadisticas`

---

## 📊 FLUJO COMPLETO DE DATOS

### 1. Día de Elecciones - Mañana

```
1. Testigo llega al puesto
2. Login con credenciales
3. Verificar presencia → Notifica al coordinador
4. Consultar mesas disponibles
5. Seleccionar mesa asignada
```

### 2. Durante la Votación

```
1. Registrar incidentes en tiempo real
2. Registrar delitos si se observan
3. Monitorear participación
```

### 3. Cierre de Mesa

```
1. Obtener tipos de elección
2. Para cada tipo de elección:
   a. Obtener partidos
   b. Obtener candidatos (si aplica)
   c. Registrar Formulario E-14:
      - Votos por partido
      - Votos por candidato (uninominales)
      - Votos nulos, blancos, no marcados
      - Total votantes
3. Confirmar envío
```

### 4. Supervisión (Coordinador Puesto)

```
1. Ver mesas del puesto
2. Ver testigos y su presencia
3. Ver formularios registrados
4. Ver incidentes reportados
5. Generar reporte del puesto
```

### 5. Consolidación (Admin Municipal)

```
1. Ver todos los puestos
2. Ver formularios municipales
3. Detectar puestos sin reportar
4. Generar consolidado municipal
```

### 6. Auditoría (Auditor)

```
1. Ver todos los formularios
2. Detectar inconsistencias:
   - Votos > votantes registrados
   - Suma de votos ≠ total votos
   - Formularios duplicados
3. Analizar incidentes y delitos
4. Generar resultados oficiales
5. Producir informes de auditoría
```

---

## ✅ VALIDACIONES IMPLEMENTADAS

### Formulario E-14

1. ✅ Total votos = votos_partidos + votos_nulos + votos_blancos
2. ✅ Total votos ≤ total_votantes_registrados
3. ✅ Votos por candidato = votos por partido (uninominales)
4. ✅ No duplicar formularios (misma mesa + tipo elección)
5. ✅ Mesa pertenece al puesto del testigo

### Incidentes

1. ✅ Tipo de incidente válido
2. ✅ Gravedad: baja, media, alta
3. ✅ Descripción obligatoria
4. ✅ Mesa válida

### Delitos

1. ✅ Tipo de delito válido
2. ✅ Gravedad: media, alta, crítica
3. ✅ Descripción detallada obligatoria
4. ✅ Seguimiento de estado
5. ✅ Opción de denuncia formal

---

## 🔒 SEGURIDAD

### Autenticación

- ✅ JWT con expiración
- ✅ Refresh tokens
- ✅ Bloqueo por intentos fallidos (5 intentos)
- ✅ Timeout de 30 minutos

### Autorización

- ✅ Role-based access control (RBAC)
- ✅ Validación de ubicación jerárquica
- ✅ Testigo solo ve su puesto
- ✅ Coordinador solo ve su ámbito
- ✅ Auditor ve todo (solo lectura)

### Auditoría

- ✅ Logs de todas las operaciones
- ✅ Historial de cambios en formularios
- ✅ Trazabilidad completa
- ✅ Timestamps en todas las operaciones

---

## 📱 FUNCIONALIDADES OFFLINE

### Sincronización

1. ✅ Almacenamiento local de formularios
2. ✅ Cola de sincronización
3. ✅ Retry automático
4. ✅ Resolución de conflictos

---

## 🎯 ESTADO ACTUAL

### ✅ Completado

- Autenticación jerárquica
- Registro de formularios E-14
- Registro de incidentes
- Registro de delitos
- Consultas por rol
- Validaciones de datos
- Endpoints de auditoría
- Gestión de configuración

### 🚧 Pendiente

- Dashboard frontend completo
- Selector de mesa en UI
- Reportes PDF
- Gráficas y visualizaciones
- Notificaciones push
- Exportación de datos

---

*Documento generado: 2025-11-16*
*Última actualización: 2025-11-16 12:50:00*
