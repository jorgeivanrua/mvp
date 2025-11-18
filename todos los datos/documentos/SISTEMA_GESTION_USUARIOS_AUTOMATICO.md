# Sistema de Gestión Automática de Usuarios

## Descripción

Sistema completo para crear usuarios (testigos, coordinadores, administradores) automáticamente basándose en la estructura jerárquica de DIVIPOLA.

## Endpoints API

### 1. Crear Testigos para un Puesto

**POST** `/api/gestion-usuarios/crear-testigos-puesto`

Crea testigos para todas las mesas de un puesto específico.

**Permisos:** super_admin, admin_departamental, admin_municipal, coordinador_puesto

**Body:**
```json
{
  "puesto_id": 4
}
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "puesto": "CAQUETA - FLORENCIA - Zona 01 - I.E. JUAN BAUTISTA LA SALLE",
    "testigos_creados": [
      {
        "username": "testigo.001.01",
        "password": "Abc123!@#XyZ",
        "mesa": "CAQUETA - FLORENCIA - Zona 01 - I.E. JUAN BAUTISTA LA SALLE - Mesa 01",
        "mesa_codigo": "01",
        "votantes_registrados": 2675
      }
    ],
    "testigos_existentes": [],
    "total_creados": 1,
    "total_existentes": 0
  }
}
```

### 2. Crear Coordinador de Puesto

**POST** `/api/gestion-usuarios/crear-coordinador-puesto`

Crea un coordinador para un puesto específico.

**Permisos:** super_admin, admin_departamental, admin_municipal

**Body:**
```json
{
  "puesto_id": 4
}
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "username": "coord.puesto.001",
    "password": "Xyz789!@#AbC",
    "puesto": "CAQUETA - FLORENCIA - Zona 01 - I.E. JUAN BAUTISTA LA SALLE",
    "rol": "coordinador_puesto"
  }
}
```

### 3. Crear Usuarios Municipales

**POST** `/api/gestion-usuarios/crear-usuarios-municipio`

Crea coordinador y/o admin municipal.

**Permisos:** super_admin, admin_departamental

**Body:**
```json
{
  "municipio_id": 2,
  "crear_coordinador": true,
  "crear_admin": true
}
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "municipio": "CAQUETA - FLORENCIA",
    "usuarios_creados": [
      {
        "rol": "coordinador_municipal",
        "username": "coord.mun.18001",
        "password": "Def456!@#GhI"
      },
      {
        "rol": "admin_municipal",
        "username": "admin.mun.18001",
        "password": "Jkl789!@#MnO"
      }
    ]
  }
}
```

### 4. Crear Usuarios Departamentales

**POST** `/api/gestion-usuarios/crear-usuarios-departamento`

Crea coordinador y/o admin departamental.

**Permisos:** super_admin

**Body:**
```json
{
  "departamento_id": 1,
  "crear_coordinador": true,
  "crear_admin": true
}
```

### 5. Listar Usuarios por Ubicación

**GET** `/api/gestion-usuarios/listar-usuarios-ubicacion/<ubicacion_id>`

Lista todos los usuarios de una ubicación específica.

**Permisos:** super_admin, admin_departamental, admin_municipal, coordinador_puesto

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "ubicacion": "CAQUETA - FLORENCIA - Zona 01 - I.E. JUAN BAUTISTA LA SALLE",
    "tipo": "puesto",
    "usuarios": [
      {
        "id": 8,
        "username": "coord.puesto.001",
        "rol": "coordinador_puesto",
        "activo": true,
        "ultimo_acceso": "2025-11-16T15:30:00"
      }
    ]
  }
}
```

### 6. Resetear Contraseña

**POST** `/api/gestion-usuarios/resetear-password/<usuario_id>`

Resetea la contraseña de un usuario y genera una nueva.

**Permisos:** super_admin, admin_departamental, admin_municipal

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "username": "testigo.001.01",
    "nueva_password": "Pqr123!@#StU"
  }
}
```

## Script de Línea de Comandos

### Listar Puestos Disponibles

```bash
python crear_usuarios_automatico.py listar
```

Muestra todos los puestos con:
- Código del puesto
- Nombre del puesto
- Municipio
- Número de mesas
- Testigos creados vs total de mesas

### Crear Testigos para un Puesto

```bash
python crear_usuarios_automatico.py crear 001
```

Crea testigos para todas las mesas del puesto especificado y:
- Genera credenciales seguras automáticamente
- Guarda las credenciales en un archivo `credenciales_testigos_001.txt`
- Muestra resumen en consola

## Formato de Usernames

El sistema genera usernames automáticamente siguiendo este patrón:

- **Testigos:** `testigo.<puesto>.<mesa>`
  - Ejemplo: `testigo.001.01`

- **Coordinador de Puesto:** `coord.puesto.<puesto>`
  - Ejemplo: `coord.puesto.001`

- **Coordinador Municipal:** `coord.mun.<municipio_codigo>`
  - Ejemplo: `coord.mun.18001`

- **Admin Municipal:** `admin.mun.<municipio_codigo>`
  - Ejemplo: `admin.mun.18001`

- **Coordinador Departamental:** `coord.dept.<departamento_codigo>`
  - Ejemplo: `coord.dept.18`

- **Admin Departamental:** `admin.dept.<departamento_codigo>`
  - Ejemplo: `admin.dept.18`

## Generación de Contraseñas

Las contraseñas se generan automáticamente con:
- 12 caracteres de longitud
- Combinación de letras mayúsculas, minúsculas, números y símbolos
- Seguridad criptográfica usando `secrets` module

Ejemplo: `Abc123!@#XyZ`

## Flujo de Trabajo Recomendado

### 1. Crear Estructura Departamental

```bash
# Desde el Super Admin
POST /api/gestion-usuarios/crear-usuarios-departamento
{
  "departamento_id": 1,
  "crear_coordinador": true,
  "crear_admin": true
}
```

### 2. Crear Estructura Municipal

```bash
# Desde Admin Departamental o Super Admin
POST /api/gestion-usuarios/crear-usuarios-municipio
{
  "municipio_id": 2,
  "crear_coordinador": true,
  "crear_admin": true
}
```

### 3. Crear Coordinadores de Puesto

```bash
# Para cada puesto
POST /api/gestion-usuarios/crear-coordinador-puesto
{
  "puesto_id": 4
}
```

### 4. Crear Testigos por Puesto

```bash
# Opción A: Desde la API
POST /api/gestion-usuarios/crear-testigos-puesto
{
  "puesto_id": 4
}

# Opción B: Desde línea de comandos
python crear_usuarios_automatico.py crear 001
```

## Ventajas del Sistema

1. **Automatización Completa:** No es necesario crear usuarios manualmente
2. **Basado en DIVIPOLA:** Usa la estructura real de ubicaciones
3. **Seguridad:** Contraseñas generadas criptográficamente
4. **Trazabilidad:** Usernames descriptivos que indican ubicación
5. **Escalable:** Puede crear cientos de usuarios en segundos
6. **Prevención de Duplicados:** Verifica usuarios existentes antes de crear
7. **Documentación Automática:** Genera archivos con credenciales

## Ejemplo Completo

### Crear todos los usuarios para Florencia, Caquetá

```bash
# 1. Listar puestos disponibles
python crear_usuarios_automatico.py listar

# 2. Crear testigos para el puesto 001
python crear_usuarios_automatico.py crear 001

# 3. Verificar credenciales generadas
cat credenciales_testigos_001.txt
```

## Notas Importantes

- Las contraseñas se muestran **solo una vez** al crear el usuario
- Guarda las credenciales en un lugar seguro
- Los usuarios pueden cambiar su contraseña después del primer login
- Los administradores pueden resetear contraseñas cuando sea necesario
- El sistema previene la creación de usuarios duplicados
