# Manual de Funcionamiento - Sistema Electoral E-14/E-24

## Índice
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Flujo General de Operación](#flujo-general-de-operación)
4. [Funcionamiento por Rol](#funcionamiento-por-rol)
5. [Procesos Detallados](#procesos-detallados)
6. [Validaciones y Reglas de Negocio](#validaciones-y-reglas-de-negocio)
7. [Casos de Uso Completos](#casos-de-uso-completos)
8. [Seguridad y Control de Acceso](#seguridad-y-control-de-acceso)

---

## Introducción

### ¿Qué es el Sistema Electoral E-14/E-24?

El Sistema Electoral de Recolección y Alertas Tempranas es una aplicación web diseñada para digitalizar, validar y consolidar los resultados electorales desde las mesas de votación hasta los niveles departamentales.

### Objetivo Principal

Permitir que testigos electorales capturen digitalmente los formularios E-14 (actas de mesa) y que coordinadores validen estos datos en tiempo real, detectando inconsistencias y garantizando la transparencia del proceso electoral.

### Componentes del Sistema

- **Frontend Web**: Interfaz responsive accesible desde navegadores
- **Backend API REST**: Servidor Flask con lógica de negocio
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Sistema de Autenticación**: JWT tokens con roles y permisos
- **Sistema de Validación**: Reglas automáticas de integridad de datos

---

## Arquitectura del Sistema

### Capas de la Aplicación

```
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Dashboard   │  │  Formularios │  │    Admin     │  │
│  │   por Rol    │  │     E-14     │  │    Panel     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↕ HTTP/JSON
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE NEGOCIO                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Servicios de Negocio                 │   │
│  │  • AuthService (autenticación)                   │   │
│  │  • E14Service (gestión formularios)              │   │
│  │  • ValidationService (validaciones)              │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↕ ORM
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE DATOS                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Modelos de Datos                     │   │
│  │  • User (usuarios)                               │   │
│  │  • Location (ubicaciones DIVIPOLA)               │   │
│  │  • FormE14 (formularios)                         │   │
│  │  • FormE14History (auditoría)                    │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Tecnologías Utilizadas

- **Backend**: Python 3.9+, Flask 2.3.3, SQLAlchemy 2.0.23
- **Autenticación**: Flask-JWT-Extended 4.5.3, bcrypt 4.0.1
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Base de Datos**: SQLite (dev), PostgreSQL (prod)

---

## Flujo General de Operación

### Ciclo de Vida de un Formulario E-14


```
1. CAPTURA (Testigo Electoral)
   ↓
   [Testigo crea formulario E-14]
   Estado: BORRADOR
   ↓
   [Testigo completa datos y adjunta foto]
   ↓
   [Testigo envía formulario]
   Estado: ENVIADO
   ↓

2. VALIDACIÓN (Coordinador de Puesto)
   ↓
   [Coordinador revisa formulario]
   ↓
   ¿Datos correctos?
   ├─ SÍ → [Coordinador aprueba]
   │        Estado: APROBADO ✅
   │        (Formulario queda consolidado)
   │
   └─ NO → [Coordinador rechaza con justificación]
            Estado: RECHAZADO ❌
            ↓
            [Testigo corrige y reenvía]
            Estado: ENVIADO (nuevamente)
```

### Diagrama de Estados

```
    ┌──────────┐
    │ BORRADOR │ ← Estado inicial
    └────┬─────┘
         │ enviar()
         ↓
    ┌──────────┐
    │ ENVIADO  │ ← Esperando validación
    └────┬─────┘
         │
    ┌────┴────┐
    │         │
    ↓         ↓
┌─────────┐ ┌──────────┐
│APROBADO │ │RECHAZADO │
└─────────┘ └────┬─────┘
                 │ corregir()
                 ↓
            ┌──────────┐
            │ ENVIADO  │ ← Puede reenviarse
            └──────────┘
```

---

## Funcionamiento por Rol

### 1. TESTIGO ELECTORAL

#### Responsabilidades
- Capturar datos del formulario E-14 de su mesa asignada
- Fotografiar el formulario físico
- Enviar formulario para validación
- Corregir formularios rechazados

#### Acceso al Sistema
1. Ingresa a la URL del sistema (ej: http://localhost:5000)
2. Inicia sesión con email y contraseña en `/auth/login`
3. Es redirigido automáticamente a `/testigo/dashboard`

#### Dashboard Testigo
Al ingresar, el testigo ve:

**Estadísticas Personales:**
- Total de formularios creados
- Formularios pendientes (borrador + enviado)
- Formularios aprobados
- Formularios rechazados

**Lista de Formularios:**
- Todos los formularios E-14 que ha creado
- Estado actual de cada uno
- Fecha de creación
- Motivo de rechazo (si aplica)

**Acciones Disponibles:**
- ➕ Crear nuevo formulario E-14
- 👁️ Ver detalle de formularios existentes
- ✏️ Editar formularios en borrador
- 📤 Enviar formularios completados

#### Proceso de Captura de E-14

**Paso 1: Crear Formulario**
```
1. Click en "Crear Nuevo E-14"
2. Sistema muestra formulario vacío
3. Mesa asignada aparece automáticamente
```

**Paso 2: Ingresar Datos**
```
Campos obligatorios:
- Imagen del formulario (foto o PDF)
- Total votantes registrados
- Total de votos emitidos
- Votos nulos
- Votos no marcados
- Votos por cada partido (dinámico, se pueden agregar)

Campos opcionales:
- Observaciones adicionales
```

**Paso 3: Validación Automática**
```
El sistema valida en tiempo real:
✓ Total votos ≤ Votantes registrados en la mesa
✓ Suma de votos = Total de votos
✓ Todos los números son positivos
✓ Foto adjunta (obligatoria antes de enviar)
```

**Paso 4: Guardar o Enviar**
```
Opciones:
- "Guardar Borrador": Guarda sin enviar (puede editar después)
- "Enviar": Envía para validación (no se puede editar)
```

#### Restricciones del Testigo
- ❌ Solo puede crear E-14 de su mesa asignada
- ❌ No puede ver formularios de otras mesas
- ❌ No puede editar formularios enviados
- ❌ No puede aprobar/rechazar formularios
- ✅ Puede corregir formularios rechazados

---

### 2. COORDINADOR DE PUESTO

#### Responsabilidades
- Revisar formularios E-14 de todas las mesas de su puesto
- Validar datos contra formularios físicos
- Aprobar formularios correctos
- Rechazar o solicitar correcciones (con justificación)
- Gestionar formularios E-24 oficiales
- Monitorear progreso de captura

#### Dashboard Coordinador
Al ingresar a `/coordinador/dashboard`, el coordinador ve:

**Estadísticas del Puesto:**
- Total formularios E-14
- E-14 aprobados
- E-14 pendientes de revisión
- E-24 cargados

**Secciones Principales:**
1. **Formularios E-14 Pendientes de Revisión**
   - Tabla con: Mesa, Testigo, Fecha envío, Total votos, Estado
   - Botón "Revisar" para cada formulario

2. **Gestión de Formularios E-24**
   - Botón "Cargar Nuevo E-24"
   - Tabla de E-24 existentes con discrepancias
   - Acciones: Ver, Editar

**Acciones Disponibles:**
- Revisar E-14 (abre modal con imagen y datos)
- Aprobar E-14
- Solicitar correcciones
- Rechazar E-14
- Cargar E-24 oficial

#### Proceso de Validación

**Paso 1: Seleccionar Formulario**
```
1. Coordinador ve lista de formularios pendientes
2. Click en formulario para ver detalle completo
3. Sistema muestra:
   - Todos los datos capturados
   - Foto del formulario físico
   - Historial de cambios
   - Datos del testigo que lo creó
```

**Paso 2: Revisar Datos**
```
El coordinador verifica:
✓ Foto es legible y corresponde a la mesa
✓ Números coinciden con la foto
✓ Suma de votos es correcta
✓ Total no excede votantes registrados
✓ No hay inconsistencias evidentes
```

**Paso 3: Tomar Decisión**

**Opción A: APROBAR**
```
1. Click en botón "Aprobar" (verde con ícono ✓)
2. Opcionalmente agregar observaciones en campo de texto
3. Confirmar aprobación
4. Sistema:
   - Cambia estado a APROBADO
   - Registra quién aprobó y cuándo
   - Guarda en historial
   - Actualiza estadísticas del dashboard
```

**Opción B: SOLICITAR CORRECCIONES**
```
1. Click en botón "Corregir" (amarillo con ícono ✏️)
2. OBLIGATORIO: Ingresar observaciones detalladas
   Ejemplos:
   - "Verificar suma de votos del Partido A"
   - "Foto parcialmente ilegible en sección de nulos"
3. Confirmar solicitud
4. Sistema:
   - Cambia estado a EN_REVISION
   - Guarda observaciones
   - Permite al testigo corregir y reenviar
```

**Opción C: RECHAZAR**
```
1. Click en botón "Rechazar" (rojo con ícono ✗)
2. OBLIGATORIO: Ingresar motivo del rechazo
   Ejemplos:
   - "Suma de votos no coincide con total"
   - "Foto ilegible, solicitar nueva captura"
   - "Número de votos excede votantes registrados"
3. Confirmar rechazo
4. Sistema:
   - Cambia estado a RECHAZADO
   - Guarda motivo
   - Registra en historial
   - Permite al testigo crear nuevo formulario
```

#### Restricciones del Coordinador
- ❌ No puede crear formularios E-14
- ❌ No puede editar datos de formularios
- ❌ Solo ve formularios de su puesto asignado
- ✅ Puede aprobar/rechazar cualquier E-14 de su puesto
- ✅ Puede ver historial completo de cambios

---

### 3. SISTEMAS / SUPERADMIN

#### Responsabilidades
- Gestionar usuarios del sistema
- Asignar roles y ubicaciones
- Gestionar ubicaciones DIVIPOLA
- Monitorear estadísticas generales
- Configurar parámetros del sistema
- Generar reportes y respaldos

#### Dashboard Admin
Al ingresar a `/admin/dashboard`, el administrador ve:

**Estadísticas Globales (Tarjetas superiores):**
- Total de usuarios en el sistema
- Usuarios activos
- Total de ubicaciones registradas
- Formularios creados hoy

**Navegación por Pestañas:**

1. **Gestión de Usuarios** (pestaña activa por defecto)
   - Filtros: Por rol, por estado, búsqueda por nombre/email
   - Tabla con: Nombre, Email, Rol, Ubicación, Estado, Último acceso
   - Botón "Nuevo Usuario"
   - Acciones: Editar, Eliminar

2. **Ubicaciones**
   - Mapa interactivo de ubicaciones DIVIPOLA
   - Filtros: Por tipo, por departamento, búsqueda
   - Tabla de ubicaciones con coordenadas y votantes
   - Botón "Nueva Ubicación"
   - Botón "Exportar"

3. **Configuración del Sistema**
   - Umbral de discrepancia (%)
   - Timeout de escalamiento (horas)
   - Tamaño máximo de archivo (MB)
   - Intentos de login fallidos
   - Herramientas: Respaldar BD, Limpiar logs, Exportar datos

4. **Reportes**
   - Gráfico de usuarios por rol
   - Gráfico de actividad del sistema

#### Gestión de Usuarios

**Crear Usuario:**
```
1. Click en "Crear Usuario"
2. Completar formulario:
   - Nombre completo
   - Email (único en el sistema)
   - Rol (Testigo, Coordinador, Sistemas)
   - Ubicación asignada
3. Sistema:
   - Valida datos
   - Genera contraseña temporal
   - Crea usuario
   - Muestra contraseña temporal (copiar y entregar)
```

**Asignación de Ubicaciones:**
```
Según el rol:
- Testigo Electoral → Asignar a una MESA específica
- Coordinador Puesto → Asignar a un PUESTO
- Coordinador Municipal → Asignar a un MUNICIPIO
- Coordinador Departamental → Asignar a un DEPARTAMENTO
- Sistemas → Sin restricción (acceso total)
```

**Desactivar Usuario:**
```
1. Seleccionar usuario
2. Click en "Desactivar"
3. Ingresar justificación
4. Confirmar
5. Usuario no puede iniciar sesión
   (Datos históricos se conservan)
```

#### Privilegios del Admin
- ✅ Acceso completo a todos los formularios
- ✅ Puede aprobar/rechazar cualquier E-14
- ✅ Ve todas las ubicaciones
- ✅ Gestiona todos los usuarios
- ✅ Accede a logs y auditoría
- ✅ Genera reportes del sistema

---

## Procesos Detallados

### Proceso 1: Autenticación y Sesión



#### Login
```
1. Usuario ingresa a /login
2. Completa email y contraseña
3. Click en "Iniciar Sesión"

Backend:
4. Valida formato de email
5. Busca usuario en base de datos
6. Verifica que usuario esté activo
7. Verifica que no esté bloqueado
8. Compara contraseña con hash almacenado
9. Si es correcto:
   - Genera access_token (válido 1 hora)
   - Genera refresh_token (válido 7 días)
   - Actualiza último_acceso
   - Resetea intentos_fallidos
   - Retorna tokens + datos de usuario
10. Si es incorrecto:
    - Incrementa intentos_fallidos
    - Si intentos >= 5: Bloquea por 30 minutos
    - Retorna error

Frontend:
11. Guarda tokens en localStorage
12. Guarda datos de usuario
13. Redirige según rol:
    - Testigo → /dashboard/testigo
    - Coordinador → /dashboard/coordinador
    - Admin → /dashboard/admin
```

#### Manejo de Sesión
```
Cada petición al backend:
1. Frontend incluye access_token en header:
   Authorization: Bearer <token>

2. Backend valida token:
   - Verifica firma
   - Verifica expiración
   - Extrae user_id del token

3. Si token expirado:
   - Frontend usa refresh_token
   - Obtiene nuevo access_token
   - Reintenta petición original

4. Si refresh_token expirado:
   - Cierra sesión automáticamente
   - Redirige a login
```

#### Logout
```
1. Usuario click en "Cerrar Sesión"
2. Frontend:
   - Elimina tokens de localStorage
   - Elimina datos de usuario
   - Redirige a /login
3. Backend (opcional):
   - Agrega token a blacklist
   - Registra logout en logs
```

---

### Proceso 2: Captura Completa de E-14

#### Escenario: Testigo captura formulario de su mesa

**Contexto:**
- Testigo: Juan Pérez
- Mesa asignada: Mesa 001 - Colegio San José
- Votantes registrados: 300
- Hora: 4:30 PM (cierre de votación)

**Paso a Paso:**

**1. Acceso al Sistema**
```
16:30 - Juan ingresa a la aplicación
16:30 - Login: testigo.mesa001@sistema.com
16:30 - Sistema valida y redirige a dashboard
```

**2. Inicio de Captura**
```
16:31 - Juan ve su dashboard:
        • Total formularios: 0
        • Pendientes: 0
        • Aprobados: 0
        • Rechazados: 0

16:31 - Click en "Crear Nuevo E-14"
16:31 - Sistema muestra formulario vacío
        • Mesa: Mesa 001 - Colegio San José (automático)
        • Votantes registrados: 300 (informativo)
```

**3. Ingreso de Datos**
```
16:32 - Juan ingresa datos del formulario físico:
        • Total votos: 285
        • Partido A: 120 votos
        • Partido B: 95 votos
        • Partido C: 55 votos
        • Votos nulos: 10
        • Votos no marcados: 5

16:33 - Sistema valida en tiempo real:
        ✓ 285 ≤ 300 (OK)
        ✓ 120+95+55+10+5 = 285 (OK)
        ✓ Todos los números ≥ 0 (OK)
```

**4. Adjuntar Foto**
```
16:34 - Juan toma foto del formulario físico
16:34 - Click en "Adjuntar Foto"
16:34 - Selecciona archivo (e14_mesa001.jpg - 2.3 MB)
16:35 - Sistema:
        • Valida tamaño < 5MB ✓
        • Valida formato (jpg/png) ✓
        • Comprime imagen a 1.1 MB
        • Sube a servidor
        • Guarda URL: /uploads/e14/2024/11/e14_mesa001_abc123.jpg
```

**5. Guardar Borrador**
```
16:35 - Juan click en "Guardar Borrador"
16:35 - Sistema:
        • Crea registro en base de datos
        • Estado: BORRADOR
        • ID: 1
        • Crea entrada en historial
        • Retorna confirmación

16:35 - Juan ve mensaje: "Borrador guardado exitosamente"
```

**6. Revisión Final**
```
16:36 - Juan revisa datos ingresados
16:36 - Verifica foto adjunta
16:36 - Compara con formulario físico
16:36 - Todo correcto ✓
```

**7. Envío para Validación**
```
16:37 - Juan click en "Enviar Formulario"
16:37 - Sistema muestra confirmación:
        "¿Está seguro? No podrá editar después de enviar"
16:37 - Juan confirma

16:37 - Sistema:
        • Valida que tenga foto ✓
        • Valida datos nuevamente ✓
        • Cambia estado: BORRADOR → ENVIADO
        • Registra en historial
        • Timestamp: 2024-11-10 16:37:23

16:37 - Juan ve mensaje: "Formulario enviado exitosamente"
16:37 - Dashboard actualizado:
        • Total formularios: 1
        • Pendientes: 1 (enviado)
        • Estado: ENVIADO ⏳
```

**8. Notificación a Coordinador**
```
16:37 - Sistema notifica a coordinador del puesto
        (Aparece en su dashboard como pendiente)
```

---

### Proceso 3: Validación por Coordinador

#### Continuación del escenario anterior

**Contexto:**
- Coordinador: María García
- Puesto: Colegio San José (3 mesas)
- Formulario pendiente: E-14 #1 de Mesa 001

**Paso a Paso:**

**1. Acceso al Dashboard**
```
16:40 - María ingresa al sistema
16:40 - Login: coord.puesto001@sistema.com
16:40 - Dashboard muestra:
        • Pendientes: 1 (URGENTE - en rojo)
        • Aprobados hoy: 0
        • Rechazados hoy: 0
        • Mesas asignadas: 3
```

**2. Revisión de Pendientes**
```
16:41 - María ve lista de formularios
16:41 - Aparece: "Formulario E-14 #1"
        • Mesa: 001 - Colegio San José
        • Testigo: Juan Pérez
        • Total votos: 285
        • Estado: ENVIADO
        • Fecha: 10/11/2024 16:37
```

**3. Abrir Detalle**
```
16:41 - María click en formulario
16:41 - Sistema muestra modal con:

┌─────────────────────────────────────────┐
│ Formulario E-14 #1                      │
├─────────────────────────────────────────┤
│ Mesa: 001 - Colegio San José            │
│ Testigo: Juan Pérez                     │
│ Votantes registrados: 300               │
│                                         │
│ DATOS CAPTURADOS:                       │
│ • Total votos: 285                      │
│ • Partido A: 120                        │
│ • Partido B: 95                         │
│ • Partido C: 55                         │
│ • Votos nulos: 10                       │
│ • Votos no marcados: 5                  │
│                                         │
│ VALIDACIONES:                           │
│ ✓ Suma correcta: 285 = 285             │
│ ✓ No excede registrados: 285 ≤ 300     │
│                                         │
│ FOTO ADJUNTA:                           │
│ [Imagen del formulario físico]          │
│                                         │
│ HISTORIAL:                              │
│ • 16:35 - Creado por Juan Pérez         │
│ • 16:37 - Enviado por Juan Pérez        │
│                                         │
│ [Aprobar] [Rechazar] [Cancelar]         │
└─────────────────────────────────────────┘
```

**4. Verificación de Datos**
```
16:42 - María compara datos con foto:
        ✓ Foto es legible
        ✓ Corresponde a Mesa 001
        ✓ Números coinciden
        ✓ Firmas presentes en foto
        ✓ Suma verificada: 120+95+55+10+5 = 285
        ✓ Total no excede 300
```

**5. Decisión: APROBAR**
```
16:43 - María click en "Aprobar"
16:43 - Sistema muestra campo opcional:
        "Observaciones (opcional)"
16:43 - María escribe: "Datos verificados correctamente"
16:43 - Click en "Confirmar Aprobación"

16:43 - Sistema:
        • Cambia estado: ENVIADO → APROBADO
        • Registra aprobado_por: María García (ID: 2)
        • Registra aprobado_en: 2024-11-10 16:43:15
        • Guarda observaciones
        • Crea entrada en historial
        • Actualiza estadísticas

16:43 - María ve mensaje: "Formulario aprobado exitosamente"
16:43 - Dashboard actualizado:
        • Pendientes: 0
        • Aprobados hoy: 1
```

**6. Notificación a Testigo**
```
16:43 - Dashboard de Juan se actualiza:
        • Aprobados: 1 ✅
        • Estado del formulario: APROBADO
```

---

### Proceso 4: Rechazo y Corrección

#### Escenario: Formulario con error en suma

**Contexto:**
- Testigo: Pedro López (Mesa 002)
- Coordinador: María García
- Error: Suma de votos no coincide con total

**Captura con Error:**
```
17:00 - Pedro crea E-14 #2
17:01 - Ingresa datos:
        • Total votos: 290
        • Partido A: 130
        • Partido B: 85
        • Partido C: 60
        • Votos nulos: 10
        • Votos no marcados: 3
        
17:01 - Sistema valida:
        ✓ 290 ≤ 300 (OK)
        ✗ 130+85+60+10+3 = 288 ≠ 290 (ERROR!)
        
17:01 - Sistema muestra alerta:
        "⚠️ La suma de votos (288) no coincide con el total (290)"
        
17:02 - Pedro no nota el error y click "Enviar"
17:02 - Sistema NO permite enviar:
        "No se puede enviar. Corrija los errores primero"
```

**Corrección Inmediata:**
```
17:03 - Pedro revisa y encuentra error
17:03 - Corrige: Votos no marcados: 3 → 5
17:03 - Sistema valida:
        ✓ 130+85+60+10+5 = 290 (OK!)
        
17:04 - Pedro envía formulario exitosamente
```

**Validación por Coordinador:**
```
17:10 - María revisa E-14 #2
17:11 - Compara con foto
17:11 - Detecta: En la foto dice "Votos no marcados: 8"
17:11 - Pero en sistema dice: 5
17:11 - Discrepancia encontrada!
```

**Rechazo con Justificación:**
```
17:12 - María click en "Rechazar"
17:12 - Sistema solicita justificación (obligatoria)
17:12 - María escribe:
        "Los votos no marcados en la foto son 8, no 5.
         Por favor verificar y corregir este dato."
         
17:12 - Click en "Confirmar Rechazo"

17:12 - Sistema:
        • Cambia estado: ENVIADO → RECHAZADO
        • Guarda justificación
        • Registra en historial
        • Permite edición por testigo

17:12 - Dashboard de Pedro actualizado:
        • Rechazados: 1 ❌
        • Motivo visible en el formulario
```

**Corrección por Testigo:**
```
17:20 - Pedro ve formulario rechazado
17:20 - Lee justificación de María
17:20 - Verifica formulario físico
17:20 - Confirma: Efectivamente son 8 votos no marcados

17:21 - Pedro edita formulario:
        • Cambia: Votos no marcados: 5 → 8
        • Total votos: 290 → 293
        
17:21 - Sistema valida:
        ✓ 130+85+60+10+8 = 293 (OK)
        ✓ 293 ≤ 300 (OK)
        
17:22 - Pedro reenvía formulario
17:22 - Estado: RECHAZADO → ENVIADO

17:25 - María revisa nuevamente
17:25 - Datos ahora coinciden con foto
17:26 - María aprueba formulario
17:26 - Estado: ENVIADO → APROBADO ✅
```

---

## Validaciones y Reglas de Negocio

### Validaciones Automáticas

#### 1. Validación de Suma de Votos
```python
Regla: suma_votos == total_votos

Donde:
suma_votos = (votos_partido_1 + votos_partido_2 + votos_partido_3 + 
              votos_nulos + votos_no_marcados)

Ejemplo VÁLIDO:
Total: 285
Suma: 120 + 95 + 55 + 10 + 5 = 285 ✓

Ejemplo INVÁLIDO:
Total: 290
Suma: 120 + 95 + 55 + 10 + 5 = 285 ✗
Error: "La suma (285) no coincide con el total (290)"
```

#### 2. Validación de Votantes Registrados
```python
Regla: total_votos <= votantes_registrados

Ejemplo VÁLIDO:
Total votos: 285
Votantes registrados: 300 ✓

Ejemplo INVÁLIDO:
Total votos: 310
Votantes registrados: 300 ✗
Error: "Total de votos (310) excede votantes registrados (300)"
```

#### 3. Validación de Números Positivos
```python
Regla: todos los campos numéricos >= 0

Ejemplo INVÁLIDO:
Votos nulos: -5 ✗
Error: "votos_nulos no puede ser negativo"
```

#### 4. Validación de Unicidad
```python
Regla: Solo un E-14 APROBADO por mesa

Ejemplo:
Mesa 001 ya tiene E-14 #1 APROBADO
Intento de aprobar E-14 #5 para Mesa 001 ✗
Error: "Ya existe un formulario E-14 aprobado para esta mesa (ID: 1)"
```

### Reglas de Transición de Estados



```
TRANSICIONES PERMITIDAS:

1. BORRADOR → ENVIADO
   Quién: Testigo Electoral
   Condición: Debe tener foto adjunta
   
2. ENVIADO → APROBADO
   Quién: Coordinador de Puesto o Sistemas
   Condición: Datos validados correctamente
   
3. ENVIADO → RECHAZADO
   Quién: Coordinador de Puesto o Sistemas
   Condición: Justificación obligatoria
   
4. RECHAZADO → ENVIADO
   Quién: Testigo Electoral
   Condición: Correcciones realizadas

TRANSICIONES NO PERMITIDAS:

❌ BORRADOR → APROBADO (debe pasar por ENVIADO)
❌ APROBADO → RECHAZADO (no se puede revertir)
❌ APROBADO → BORRADOR (no se puede editar)
❌ RECHAZADO → APROBADO (debe reenviarse primero)
```

### Reglas de Permisos por Rol

#### Testigo Electoral
```
PUEDE:
✓ Crear E-14 de su mesa asignada
✓ Ver sus propios E-14
✓ Editar E-14 en estado BORRADOR
✓ Enviar E-14 (BORRADOR → ENVIADO)
✓ Reenviar E-14 rechazados (RECHAZADO → ENVIADO)
✓ Adjuntar/cambiar foto en BORRADOR

NO PUEDE:
✗ Ver E-14 de otras mesas
✗ Crear E-14 de mesas no asignadas
✗ Editar E-14 en estado ENVIADO
✗ Editar E-14 en estado APROBADO
✗ Aprobar/rechazar E-14
✗ Eliminar E-14
✗ Gestionar usuarios
```

#### Coordinador de Puesto
```
PUEDE:
✓ Ver todos los E-14 de su puesto
✓ Aprobar E-14 en estado ENVIADO
✓ Rechazar E-14 en estado ENVIADO
✓ Ver historial completo de E-14
✓ Ver estadísticas de su puesto
✓ Filtrar y buscar E-14

NO PUEDE:
✗ Crear E-14
✗ Editar datos de E-14
✗ Ver E-14 de otros puestos
✗ Eliminar E-14
✗ Gestionar usuarios
✗ Cambiar estado de E-14 aprobados
```

#### Sistemas / Superadmin
```
PUEDE:
✓ TODO lo anterior
✓ Ver todos los E-14 del sistema
✓ Gestionar usuarios (crear, editar, desactivar)
✓ Asignar roles y ubicaciones
✓ Ver estadísticas globales
✓ Acceder a logs y auditoría
✓ Aprobar/rechazar cualquier E-14
✓ Generar reportes

RESTRICCIONES:
⚠️ No puede eliminar E-14 aprobados (integridad)
⚠️ Cambios quedan registrados en auditoría
```

---

## Casos de Uso Completos

### Caso de Uso 1: Día Electoral Completo

**Escenario:** Puesto de votación con 3 mesas

**Actores:**
- 3 Testigos (uno por mesa)
- 1 Coordinador de Puesto
- 1 Administrador del Sistema

**Timeline:**

```
08:00 AM - Apertura de Votación
├─ Testigos llegan al puesto
├─ Verifican acceso al sistema
└─ Coordinador verifica conectividad

08:00 - 16:00 - Jornada de Votación
├─ Sistema disponible para consultas
├─ Testigos monitorean proceso
└─ Coordinador en standby

16:00 - Cierre de Votación
├─ Inicia conteo de votos
└─ Testigos preparan formularios físicos

16:30 - Inicio de Captura Digital
├─ Mesa 1: Testigo inicia captura E-14 #1
├─ Mesa 2: Testigo inicia captura E-14 #2
└─ Mesa 3: Testigo inicia captura E-14 #3

16:45 - Primeros Envíos
├─ Mesa 1: E-14 #1 ENVIADO ✓
├─ Mesa 2: E-14 #2 guardado como BORRADOR
└─ Mesa 3: E-14 #3 ENVIADO ✓

17:00 - Validación por Coordinador
├─ Coordinador revisa E-14 #1
├─ Aprueba E-14 #1 ✅
├─ Coordinador revisa E-14 #3
└─ Rechaza E-14 #3 (error en suma) ❌

17:15 - Correcciones
├─ Mesa 2: Testigo completa y envía E-14 #2
├─ Mesa 3: Testigo corrige E-14 #3
└─ Mesa 3: Reenvía E-14 #3

17:30 - Validación Final
├─ Coordinador aprueba E-14 #2 ✅
├─ Coordinador aprueba E-14 #3 (corregido) ✅
└─ Puesto completo: 3/3 mesas aprobadas

17:45 - Consolidación
├─ Coordinador verifica estadísticas
├─ Admin monitorea progreso nacional
└─ Datos listos para consolidación municipal

18:00 - Cierre del Proceso
├─ Todos los E-14 aprobados
├─ Testigos pueden retirarse
└─ Sistema genera reporte del puesto
```

**Métricas del Puesto:**
- Total formularios: 3
- Aprobados: 3 (100%)
- Rechazados inicialmente: 1 (corregido)
- Tiempo promedio de captura: 15 minutos
- Tiempo promedio de validación: 5 minutos
- Tiempo total del proceso: 1.5 horas

---

### Caso de Uso 2: Gestión de Usuarios por Admin

**Escenario:** Nuevo puesto de votación requiere usuarios

**Contexto:**
- Nuevo puesto: "Escuela Central"
- Ubicación: Bogotá, Puesto 025
- Requiere: 1 coordinador + 5 testigos

**Proceso:**

**1. Preparación de Ubicaciones**
```
Admin verifica en sistema:
✓ Departamento: Cundinamarca (25) existe
✓ Municipio: Bogotá (001) existe
✓ Puesto: 025 - Escuela Central existe
✓ Mesas: 001, 002, 003, 004, 005 existen
```

**2. Crear Coordinador**
```
09:00 - Admin accede a "Gestión de Usuarios"
09:01 - Click en "Crear Usuario"
09:01 - Completa formulario:
        • Nombre: "Roberto Sánchez"
        • Email: "roberto.sanchez@sistema.com"
        • Rol: "Coordinador de Puesto"
        • Ubicación: Puesto 025 - Escuela Central
        
09:02 - Click en "Guardar"
09:02 - Sistema:
        • Valida email único ✓
        • Crea usuario
        • Genera contraseña temporal: "Temp2024!"
        • Muestra contraseña en pantalla
        
09:02 - Admin copia contraseña
09:03 - Admin envía credenciales a Roberto:
        Email: roberto.sanchez@sistema.com
        Password: Temp2024!
        Instrucción: "Cambiar contraseña al primer login"
```

**3. Crear Testigos (5 usuarios)**
```
09:05 - Admin crea testigo para Mesa 001:
        • Nombre: "Ana Martínez"
        • Email: "ana.martinez@sistema.com"
        • Rol: "Testigo Electoral"
        • Ubicación: Mesa 001 - Escuela Central
        • Password temporal: "Temp2024!"
        
09:07 - Admin repite proceso para mesas 002-005
09:15 - Total creados: 5 testigos

Lista de testigos:
1. ana.martinez@sistema.com → Mesa 001
2. carlos.lopez@sistema.com → Mesa 002
3. diana.torres@sistema.com → Mesa 003
4. eduardo.ruiz@sistema.com → Mesa 004
5. fernanda.gomez@sistema.com → Mesa 005
```

**4. Entrega de Credenciales**
```
09:20 - Admin genera documento con credenciales
09:25 - Admin envía a coordinador Roberto
09:30 - Roberto distribuye credenciales a testigos
```

**5. Verificación de Acceso**
```
10:00 - Roberto hace primer login
10:01 - Sistema solicita cambio de contraseña
10:02 - Roberto establece nueva contraseña
10:03 - Accede a dashboard de coordinador
10:03 - Verifica que ve las 5 mesas asignadas ✓

10:10 - Cada testigo hace primer login
10:15 - Todos cambian contraseñas
10:20 - Todos verifican acceso a su mesa ✓
```

**6. Monitoreo por Admin**
```
10:30 - Admin verifica en dashboard:
        • Usuarios activos: +6 (1 coord + 5 testigos)
        • Últimos logins: 6 usuarios nuevos
        • Estado: Todos activos ✓
        • Ubicaciones asignadas: Correctas ✓
```

---

### Caso de Uso 3: Detección de Inconsistencia

**Escenario:** Coordinador detecta posible fraude

**Contexto:**
- Mesa 010 tiene 250 votantes registrados
- Testigo envía E-14 con 248 votos
- Coordinador tiene formulario físico diferente

**Detección:**
```
15:30 - Coordinador recibe E-14 #15
15:31 - Revisa datos digitales:
        • Total votos: 248
        • Partido A: 150
        • Partido B: 70
        • Partido C: 20
        • Nulos: 5
        • No marcados: 3
        
15:32 - Coordinador compara con formulario físico
15:33 - Detecta discrepancia:
        Formulario físico dice:
        • Partido A: 120 (no 150!)
        • Partido B: 100 (no 70!)
```

**Acción Inmediata:**
```
15:34 - Coordinador RECHAZA formulario
15:34 - Justificación detallada:
        "DISCREPANCIA GRAVE: Los votos del Partido A y B
         no coinciden con el formulario físico.
         Físico: A=120, B=100
         Digital: A=150, B=70
         Diferencia: 30 votos intercambiados
         Solicito verificación inmediata con jurados de mesa"
         
15:35 - Coordinador notifica a Admin
15:35 - Coordinador contacta al testigo por teléfono
```

**Investigación:**
```
15:40 - Testigo revisa formulario físico original
15:41 - Testigo confirma error de transcripción
15:42 - Testigo explica: "Confundí las columnas"
15:43 - Testigo corrige datos en sistema
15:45 - Testigo reenvía E-14 #15

15:50 - Coordinador revisa corrección:
        • Partido A: 120 ✓
        • Partido B: 100 ✓
        • Suma: 248 ✓
        • Coincide con físico ✓
        
15:52 - Coordinador APRUEBA con observación:
        "Corregido después de verificación.
         Error de transcripción confirmado y solucionado"
```

**Registro de Auditoría:**
```
Sistema registra en historial:
• 15:30 - E-14 #15 creado por testigo
• 15:34 - E-14 #15 rechazado por coordinador
  Motivo: Discrepancia con formulario físico
• 15:45 - E-14 #15 reenviado por testigo
  Cambios: Partido A (150→120), Partido B (70→100)
• 15:52 - E-14 #15 aprobado por coordinador
  Observación: Error corregido y verificado

Admin puede revisar este historial completo
```

---

## Seguridad y Control de Acceso

### Seguridad de Contraseñas

#### Requisitos de Contraseña
```
Mínimo 8 caracteres
Al menos 1 mayúscula
Al menos 1 minúscula
Al menos 1 número
Caracteres especiales recomendados

Ejemplos VÁLIDOS:
✓ Admin123!
✓ Testigo2024
✓ Coord@Puesto1

Ejemplos INVÁLIDOS:
✗ admin123 (sin mayúscula)
✗ ADMIN123 (sin minúscula)
✗ Admin (muy corta)
✗ password (muy común)
```

#### Almacenamiento Seguro
```
1. Usuario ingresa: "Admin123!"
2. Sistema aplica bcrypt con salt
3. Se almacena hash: "$2b$12$KIX..."
4. Contraseña original NUNCA se guarda
5. Comparación usa bcrypt.compare()
```

### Protección contra Ataques

#### Bloqueo por Intentos Fallidos
```
Intento 1: Contraseña incorrecta
→ intentos_fallidos = 1

Intento 2: Contraseña incorrecta
→ intentos_fallidos = 2

Intento 3: Contraseña incorrecta
→ intentos_fallidos = 3

Intento 4: Contraseña incorrecta
→ intentos_fallidos = 4

Intento 5: Contraseña incorrecta
→ intentos_fallidos = 5
→ bloqueado_hasta = ahora + 30 minutos
→ Mensaje: "Cuenta bloqueada por 30 minutos"

Durante bloqueo:
→ Login rechazado automáticamente
→ Mensaje: "Cuenta bloqueada. Intente en X minutos"

Después de 30 minutos:
→ Bloqueo se levanta automáticamente
→ intentos_fallidos se resetea a 0
```

#### Tokens JWT

**Access Token:**
```
Duración: 1 hora
Uso: Autenticar cada petición
Contenido:
{
  "user_id": 123,
  "rol": "testigo_electoral",
  "exp": 1699650000  // timestamp expiración
}

Si expira:
→ Frontend usa refresh_token
→ Obtiene nuevo access_token
→ Continúa operación
```

**Refresh Token:**
```
Duración: 7 días
Uso: Renovar access_token
Almacenamiento: localStorage (frontend)

Si expira:
→ Usuario debe hacer login nuevamente
→ Tokens anteriores invalidados
```

### Auditoría y Trazabilidad

#### Registro de Acciones
```
Cada acción importante se registra:

LOGIN:
• Usuario: juan.perez@sistema.com
• Timestamp: 2024-11-10 16:30:15
• IP: 192.168.1.100
• Resultado: Exitoso

CREAR E-14:
• Usuario: Juan Pérez (ID: 5)
• Acción: Crear formulario E-14
• Formulario: #1
• Mesa: 001
• Timestamp: 2024-11-10 16:35:00

APROBAR E-14:
• Usuario: María García (ID: 2)
• Acción: Aprobar formulario
• Formulario: #1
• Estado anterior: ENVIADO
• Estado nuevo: APROBADO
• Timestamp: 2024-11-10 16:43:15
• Observaciones: "Datos verificados correctamente"

RECHAZAR E-14:
• Usuario: María García (ID: 2)
• Acción: Rechazar formulario
• Formulario: #3
• Estado anterior: ENVIADO
• Estado nuevo: RECHAZADO
• Timestamp: 2024-11-10 17:12:30
• Justificación: "Suma de votos incorrecta"
```

#### Consulta de Auditoría
```
Admin puede consultar:
• Todas las acciones de un usuario
• Todas las acciones sobre un formulario
• Acciones en un rango de fechas
• Acciones por tipo (crear, aprobar, rechazar)
• Logins exitosos y fallidos
• Cambios en usuarios

Ejemplo de consulta:
"Mostrar todas las acciones del usuario juan.perez@sistema.com
 en los últimos 7 días"

Resultado:
1. 2024-11-10 16:30 - Login exitoso
2. 2024-11-10 16:35 - Crear E-14 #1
3. 2024-11-10 16:37 - Enviar E-14 #1
4. 2024-11-10 18:00 - Logout
```

---

## Resumen de Funcionamiento

### Flujo Simplificado

```
1. USUARIOS
   ↓
   Admin crea usuarios con roles y ubicaciones
   ↓
   Usuarios reciben credenciales temporales
   ↓
   Primer login: Cambio de contraseña obligatorio

2. CAPTURA
   ↓
   Testigo ingresa al sistema
   ↓
   Crea formulario E-14 de su mesa
   ↓
   Ingresa datos y adjunta foto
   ↓
   Sistema valida automáticamente
   ↓
   Testigo envía para aprobación

3. VALIDACIÓN
   ↓
   Coordinador ve formularios pendientes
   ↓
   Revisa datos y foto
   ↓
   Compara con formulario físico
   ↓
   Decide: Aprobar o Rechazar

4. CONSOLIDACIÓN
   ↓
   Formularios aprobados quedan consolidados
   ↓
   Admin monitorea estadísticas generales
   ↓
   Datos listos para siguiente nivel
```

### Principios Clave

1. **Validación en Tiempo Real**: Errores detectados inmediatamente
2. **Trazabilidad Completa**: Cada acción queda registrada
3. **Control de Acceso Estricto**: Cada rol ve solo lo necesario
4. **Proceso Reversible**: Formularios rechazados pueden corregirse
5. **Auditoría Permanente**: Historial completo de cambios
6. **Seguridad Robusta**: Contraseñas hasheadas, tokens JWT, bloqueos
7. **Integridad de Datos**: Validaciones automáticas y manuales

---

**Fin del Manual de Funcionamiento**

Para más información técnica, consultar:
- `DISEÑO_MVP.md` - Arquitectura técnica
- `REQUERIMIENTOS_MVP.md` - Especificaciones funcionales
- `TAREAS_MVP.md` - Plan de implementación
