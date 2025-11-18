# MANUAL COMPLETO DEL SISTEMA ELECTORAL
## Sistema de Gestión Electoral - Caquetá 2027

---

## TABLA DE CONTENIDOS

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Roles y Permisos](#roles-y-permisos)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Manual del Super Administrador](#manual-del-super-administrador)
6. [Manual del Coordinador](#manual-del-coordinador)
7. [Manual del Testigo Electoral](#manual-del-testigo-electoral)
8. [Gestión de Base de Datos](#gestión-de-base-de-datos)
9. [Despliegue en Producción](#despliegue-en-producción)
10. [Solución de Problemas](#solución-de-problemas)
11. [API Reference](#api-reference)

---

## INTRODUCCIÓN

### ¿Qué es este sistema?

Sistema web para la gestión y reporte de resultados electorales en tiempo real durante las elecciones regionales de Caquetá 2027.

### Características principales

- ✅ Gestión de testigos electorales por puesto de votación
- ✅ Registro de formularios E-14 desde dispositivos móviles
- ✅ Verificación de presencia de testigos
- ✅ Dashboard en tiempo real para coordinadores
- ✅ Panel de administración completo
- ✅ Optimizado para dispositivos móviles
- ✅ Sistema de roles y permisos
- ✅ Datos precargados de DIVIPOLA (Caquetá completo)

### Tecnologías utilizadas

- **Backend**: Python Flask
- **Base de datos**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Despliegue**: Render.com
- **Almacenamiento**: WhiteNoise para archivos estáticos

---

## ARQUITECTURA DEL SISTEMA

### Estructura de Directorios

```
sistema-electoral/
├── backend/
│   ├── app.py                 # Aplicación Flask principal
│   ├── init_app.py           # Inicialización de la app
│   ├── config.py             # Configuración
│   ├── models/               # Modelos de base de datos
│   │   ├── user.py
│   │   ├── testigo.py
│   │   ├── formulario.py
│   │   └── divipola.py
│   ├── routes/               # Rutas/Endpoints
│   │   ├── auth.py
│   │   ├── testigo.py
│   │   ├── coordinador.py
│   │   ├── super_admin.py
│   │   └── init_db_route.py
│   └── scripts/              # Scripts de carga de datos
│       └── load_basic_data_simple.py
├── frontend/
│   ├── templates/            # Plantillas HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── testigo/
│   │   ├── coordinador/
│   │   └── super_admin/
│   └── static/
│       ├── css/
│       │   ├── styles.css
│       │   └── mobile-responsive.css
│       └── js/
│           ├── api-client.js
│           ├── testigo-dashboard-v2.js
│           ├── testigo-presencia-simple.js
│           ├── coordinador-dashboard.js
│           └── super-admin-dashboard.js
├── instance/
│   └── electoral.db          # Base de datos SQLite
├── run.py                    # Punto de entrada
├── render.yaml               # Configuración de Render
└── upload_db_to_render.py    # Script para subir BD

```

### Flujo de Datos

1. **Testigo** → Registra presencia → Llena formulario E-14 → Envía a servidor
2. **Servidor** → Valida datos → Guarda en BD → Notifica coordinadores
3. **Coordinador** → Visualiza datos en tiempo real → Monitorea progreso
4. **Super Admin** → Gestiona configuración → Administra usuarios

---

## ROLES Y PERMISOS

### 1. Super Administrador

**Permisos:**
- ✅ Gestión completa de usuarios (crear, editar, eliminar)
- ✅ Configuración de partidos políticos
- ✅ Configuración de tipos de elección
- ✅ Gestión de candidatos
- ✅ Asignación de testigos a puestos
- ✅ Visualización de todos los datos
- ✅ Reseteo de contraseñas
- ✅ Inicialización de base de datos

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

### 2. Coordinador

**Permisos:**
- ✅ Visualización de dashboard en tiempo real
- ✅ Monitoreo de testigos asignados
- ✅ Visualización de formularios E-14
- ✅ Reportes y estadísticas
- ✅ Gestión de testigos de su zona
- ❌ No puede modificar configuración del sistema

**Credenciales de ejemplo:**
- Usuario: `coord_zona01`
- Contraseña: `coord123`

### 3. Testigo Electoral

**Permisos:**
- ✅ Registro de presencia en puesto de votación
- ✅ Llenado de formularios E-14
- ✅ Visualización de sus propios formularios
- ✅ Acceso solo a su puesto asignado
- ❌ No puede ver datos de otros testigos
- ❌ No puede modificar datos enviados

**Credenciales de ejemplo:**
- Usuario: `testigo_001`
- Contraseña: `testigo123`

---

## INSTALACIÓN Y CONFIGURACIÓN

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Instalación Local

#### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd sistema-electoral
```

#### 2. Crear entorno virtual

```bash
python -m venv venv
```

#### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 5. Inicializar base de datos

**Opción A: Desde la interfaz web**
1. Ejecutar `python run.py`
2. Abrir navegador en `http://localhost:5000`
3. Ir a `/init-db`
4. Hacer clic en "Inicializar Base de Datos"

**Opción B: Desde línea de comandos**
```bash
python backend/scripts/load_basic_data_simple.py
```

#### 6. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

### Configuración Inicial

#### 1. Cambiar contraseña del admin

```python
# En consola Python o script
from backend.models.user import User
from backend.app import db

admin = User.query.filter_by(username='admin').first()
admin.set_password('nueva_contraseña_segura')
db.session.commit()
```

#### 2. Crear usuarios coordinadores

Desde el panel de Super Admin:
1. Login como admin
2. Ir a "Gestión de Usuarios"
3. Clic en "Crear Usuario"
4. Llenar formulario con rol "coordinador"

#### 3. Crear testigos

Desde el panel de Super Admin:
1. Ir a "Gestión de Testigos"
2. Clic en "Crear Testigo"
3. Asignar a puesto de votación específico

---

## MANUAL DEL SUPER ADMINISTRADOR

### Acceso al Panel

1. Ir a `http://tu-dominio.com`
2. Ingresar credenciales de admin
3. Serás redirigido a `/super-admin/dashboard`

### Gestión de Partidos Políticos

#### Crear Partido

1. En el dashboard, ir a sección "Partidos Políticos"
2. Clic en "Agregar Partido"
3. Llenar formulario:
   - **Nombre**: Nombre completo del partido
   - **Sigla**: Siglas (ej: "PC", "PL", "PDA")
   - **Color**: Color hexadecimal (ej: #FF0000)
   - **Logo URL**: URL del logo (opcional)
4. Clic en "Guardar"

#### Editar Partido

1. En la lista de partidos, clic en botón "Editar"
2. Modificar campos necesarios
3. Clic en "Guardar Cambios"

#### Activar/Desactivar Partido

1. En la lista de partidos, usar toggle "Activo/Inactivo"
2. Los partidos inactivos no aparecen en formularios

### Gestión de Tipos de Elección

#### Tipos Disponibles

1. **Presidencia** (Uninominal)
2. **Senado** (Por listas)
3. **Cámara de Representantes** (Por listas)
4. **Gobernación** (Uninominal)
5. **Asamblea Departamental** (Por listas)
6. **Alcaldía** (Uninominal)
7. **Concejo Municipal** (Por listas)
8. **JAL - Juntas Administradoras Locales** (Por listas)
9. **Concejo de Juventudes** (Por listas)

#### Crear Tipo de Elección

1. Ir a sección "Tipos de Elección"
2. Clic en "Agregar Tipo"
3. Llenar formulario:
   - **Nombre**: Nombre del tipo
   - **Descripción**: Descripción detallada
   - **Tipo de votación**: Uninominal o Por listas
   - **Permite múltiples votos**: Sí/No
4. Clic en "Guardar"

#### Editar Tipo de Elección

1. Clic en botón "Editar" del tipo
2. Modificar campos
3. Guardar cambios

### Gestión de Candidatos

#### Crear Candidato

1. Ir a sección "Candidatos"
2. Clic en "Agregar Candidato"
3. Llenar formulario:
   - **Nombre completo**: Nombre del candidato
   - **Partido**: Seleccionar de lista
   - **Tipo de elección**: Seleccionar de lista
   - **Número de lista**: Solo para elecciones por listas
   - **Foto URL**: URL de foto (opcional)
4. Clic en "Guardar"

#### Editar Candidato

1. Clic en botón "Editar"
2. Modificar información
3. Guardar cambios

#### Activar/Desactivar Candidato

1. Usar toggle en la lista de candidatos
2. Candidatos inactivos no aparecen en formularios

### Gestión de Usuarios

#### Crear Usuario

1. Ir a "Gestión de Usuarios"
2. Clic en "Crear Usuario"
3. Llenar formulario:
   - **Username**: Nombre de usuario único
   - **Email**: Correo electrónico
   - **Contraseña**: Contraseña temporal
   - **Rol**: super_admin, coordinador, o testigo
   - **Zona**: Solo para coordinadores
4. Clic en "Crear"

#### Resetear Contraseña

1. En lista de usuarios, clic en "Resetear Contraseña"
2. Ingresar nueva contraseña
3. Confirmar

#### Eliminar Usuario

1. Clic en botón "Eliminar"
2. Confirmar acción
3. **Nota**: No se puede eliminar el usuario admin principal

### Gestión de Testigos

#### Crear Testigo

1. Ir a "Gestión de Testigos"
2. Clic en "Crear Testigo"
3. Llenar formulario:
   - **Nombre completo**
   - **Cédula**
   - **Teléfono**
   - **Email**
   - **Departamento**: Seleccionar (ej: Caquetá)
   - **Municipio**: Seleccionar
   - **Zona**: Seleccionar
   - **Puesto de votación**: Seleccionar
   - **Usuario**: Asociar con cuenta de usuario
4. Clic en "Guardar"

#### Asignar Testigo a Puesto

1. Editar testigo existente
2. Cambiar "Puesto de votación"
3. Guardar cambios

#### Ver Testigos por Zona

1. Usar filtro "Zona" en la lista
2. Ver todos los testigos de esa zona

---

## MANUAL DEL COORDINADOR

### Acceso al Dashboard

1. Ingresar con credenciales de coordinador
2. Serás redirigido a `/coordinador/dashboard`

### Dashboard Principal

#### Vista General

El dashboard muestra:
- **Total de testigos asignados** a tu zona
- **Testigos presentes** (han registrado presencia)
- **Formularios recibidos** (E-14 completados)
- **Porcentaje de cobertura**

#### Mapa de Calor

- Verde: Puestos con testigo presente y formularios enviados
- Amarillo: Puestos con testigo presente sin formularios
- Rojo: Puestos sin testigo presente

### Monitoreo de Testigos

#### Ver Lista de Testigos

1. En el dashboard, sección "Mis Testigos"
2. Ver tabla con:
   - Nombre del testigo
   - Puesto asignado
   - Estado de presencia
   - Formularios enviados
   - Última actividad

#### Filtrar Testigos

1. Usar filtros:
   - Por municipio
   - Por estado (presente/ausente)
   - Por puestos con/sin formularios

#### Contactar Testigo

1. En la lista, ver teléfono del testigo
2. Clic en número para llamar (en móvil)
3. Ver email para contacto

### Visualización de Formularios E-14

#### Ver Formularios Recibidos

1. Ir a sección "Formularios E-14"
2. Ver lista de todos los formularios de tu zona
3. Información mostrada:
   - Puesto de votación
   - Mesa
   - Testigo que reportó
   - Hora de envío
   - Estado (completo/incompleto)

#### Ver Detalle de Formulario

1. Clic en formulario específico
2. Ver información completa:
   - Datos de la mesa
   - Votantes registrados
   - Votos por candidato/partido
   - Votos en blanco
   - Votos nulos
   - Votos no marcados
   - Total de votos

#### Exportar Datos

1. Clic en "Exportar a Excel"
2. Seleccionar rango de fechas
3. Descargar archivo

### Reportes y Estadísticas

#### Reporte de Cobertura

- Ver porcentaje de puestos cubiertos
- Identificar puestos sin testigo
- Ver puestos sin formularios

#### Reporte de Resultados

- Consolidado de votos por candidato
- Consolidado por partido
- Comparación entre municipios

#### Alertas

El sistema muestra alertas para:
- ⚠️ Testigos que no han registrado presencia
- ⚠️ Puestos sin formularios después de cierta hora
- ⚠️ Formularios con inconsistencias

---

## MANUAL DEL TESTIGO ELECTORAL

### Preparación Antes del Día de Elecciones

#### 1. Verificar Credenciales

- Recibir usuario y contraseña del coordinador
- Probar acceso al sistema antes del día de elecciones
- Guardar credenciales de forma segura

#### 2. Verificar Asignación

- Confirmar puesto de votación asignado
- Verificar dirección del puesto
- Conocer las mesas asignadas al puesto

#### 3. Preparar Dispositivo

- Cargar completamente el celular/tablet
- Llevar cargador portátil
- Verificar conexión a internet
- Probar acceso al sistema

### Día de Elecciones - Paso a Paso

#### PASO 1: Llegar al Puesto de Votación

1. Llegar temprano (antes de las 8:00 AM)
2. Ubicar las mesas asignadas
3. Presentarse con los jurados de votación

#### PASO 2: Registrar Presencia

1. Abrir navegador en el celular
2. Ir a la URL del sistema
3. Ingresar usuario y contraseña
4. Clic en "Iniciar Sesión"
5. En el dashboard, clic en **"Registrar Presencia"**
6. Confirmar ubicación y hora
7. El botón "Nuevo Formulario" se habilitará automáticamente

**⚠️ IMPORTANTE**: Debes registrar presencia antes de poder enviar formularios.

#### PASO 3: Esperar Cierre de Votación

- Las mesas cierran a las 4:00 PM
- Permanecer en el puesto hasta el cierre
- Observar el proceso de escrutinio

#### PASO 4: Llenar Formulario E-14

Una vez cierren las mesas y se complete el escrutinio:

1. En el dashboard, clic en **"Nuevo Formulario E-14"**

2. **Seleccionar Mesa**:
   - Elegir el número de mesa del selector
   - Los votantes registrados se cargan automáticamente

3. **Información de la Mesa**:
   - Verificar que los datos sean correctos
   - Número de votantes registrados (precargado)

4. **Seleccionar Tipo de Elección**:
   - Elegir el tipo (ej: Gobernación, Asamblea, etc.)
   - Los candidatos se cargan automáticamente

5. **Registrar Votos por Candidato**:
   - Ingresar número de votos para cada candidato
   - Verificar que los números coincidan con el E-14 físico
   - El sistema suma automáticamente

6. **Registrar Otros Votos**:
   - **Votos en blanco**: Tarjetas depositadas sin marcar
   - **Votos nulos**: Tarjetas marcadas incorrectamente
   - **Votos no marcados**: Tarjetas no utilizadas

7. **Verificar Totales**:
   - El sistema calcula automáticamente el total
   - Verificar que coincida con el E-14 físico
   - Si hay diferencias, revisar los números

8. **Enviar Formulario**:
   - Clic en "Enviar Formulario"
   - Esperar confirmación
   - Guardar número de confirmación

#### PASO 5: Formularios Adicionales

Si hay múltiples tipos de elección:

1. Repetir proceso para cada tipo
2. Usar el mismo número de mesa
3. Cambiar tipo de elección
4. Ingresar votos correspondientes

### Consejos Importantes

#### ✅ Hacer

- Llegar temprano al puesto
- Registrar presencia inmediatamente
- Tomar fotos del E-14 físico como respaldo
- Verificar conexión a internet antes de enviar
- Enviar formularios lo más pronto posible
- Guardar confirmaciones de envío
- Contactar al coordinador si hay problemas

#### ❌ No Hacer

- No compartir tu usuario y contraseña
- No registrar datos de otras mesas sin autorización
- No modificar datos después de enviar
- No abandonar el puesto antes del cierre
- No enviar datos sin verificar

### Solución de Problemas Comunes

#### No puedo iniciar sesión

1. Verificar usuario y contraseña
2. Verificar conexión a internet
3. Contactar al coordinador

#### El botón "Nuevo Formulario" está deshabilitado

1. Debes registrar presencia primero
2. Clic en "Registrar Presencia"
3. Esperar confirmación
4. El botón se habilitará automáticamente

#### No aparecen los candidatos

1. Verificar que seleccionaste el tipo de elección correcto
2. Algunos tipos pueden no tener candidatos configurados
3. Contactar al coordinador

#### Error al enviar formulario

1. Verificar conexión a internet
2. Verificar que todos los campos estén llenos
3. Verificar que los totales sean correctos
4. Intentar nuevamente
5. Si persiste, contactar coordinador

#### Los totales no coinciden

1. Revisar cada número ingresado
2. Verificar votos en blanco, nulos y no marcados
3. Comparar con E-14 físico
4. Corregir antes de enviar

---

## GESTIÓN DE BASE DE DATOS

### Estructura de la Base de Datos

#### Tablas Principales

1. **users**: Usuarios del sistema
2. **testigos**: Testigos electorales
3. **partidos**: Partidos políticos
4. **tipos_eleccion**: Tipos de elección
5. **candidatos**: Candidatos por tipo de elección
6. **formularios_e14**: Formularios E-14 enviados
7. **votos**: Votos registrados por candidato
8. **departamentos**: Departamentos (DIVIPOLA)
9. **municipios**: Municipios (DIVIPOLA)
10. **zonas**: Zonas electorales
11. **puestos_votacion**: Puestos de votación
12. **mesas**: Mesas de votación

### Backup de Base de Datos

#### Backup Manual

```bash
# Copiar archivo de base de datos
cp instance/electoral.db instance/electoral_backup_$(date +%Y%m%d).db
```

#### Backup Automático

El sistema crea backups automáticos:
- Antes de cada inicialización
- Ubicación: `instance/backups/`
- Formato: `electoral_backup_YYYYMMDD_HHMMSS.db`

### Restaurar Base de Datos

```bash
# Restaurar desde backup
cp instance/backups/electoral_backup_20270318.db instance/electoral.db

# Reiniciar aplicación
python run.py
```

### Inicializar Base de Datos

#### Desde Interfaz Web

1. Ir a `http://tu-dominio.com/init-db`
2. Clic en "Inicializar Base de Datos"
3. Esperar confirmación
4. Verificar que se cargaron los datos

#### Desde Línea de Comandos

```bash
python backend/scripts/load_basic_data_simple.py
```

### Datos Precargados

El script de inicialización carga:

1. **Usuario Admin**:
   - Username: `admin`
   - Password: `admin123`
   - Rol: super_admin

2. **Departamento Caquetá** con todos sus municipios:
   - Florencia (capital)
   - Albania
   - Belén de los Andaquíes
   - Cartagena del Chairá
   - Curillo
   - El Doncello
   - El Paujil
   - La Montañita
   - Milán
   - Morelia
   - Puerto Rico
   - San José del Fragua
   - San Vicente del Caguán
   - Solano
   - Solita
   - Valparaíso

3. **Zonas Electorales**: 01 a 10

4. **Puestos de Votación**: Precargados por municipio

5. **Mesas**: Mesas 1-10 por cada puesto

6. **Partidos Políticos**: Principales partidos de Colombia

7. **Tipos de Elección**: 9 tipos configurados

### Consultas SQL Útiles

#### Ver total de formularios por municipio

```sql
SELECT m.nombre, COUNT(f.id) as total_formularios
FROM formularios_e14 f
JOIN puestos_votacion p ON f.puesto_id = p.id
JOIN municipios m ON p.municipio_id = m.id
GROUP BY m.nombre;
```

#### Ver testigos sin presencia registrada

```sql
SELECT t.nombre, t.cedula, p.nombre as puesto
FROM testigos t
LEFT JOIN puestos_votacion p ON t.puesto_id = p.id
WHERE t.presencia_registrada = 0;
```

#### Ver votos por candidato

```sql
SELECT c.nombre, SUM(v.votos) as total_votos
FROM votos v
JOIN candidatos c ON v.candidato_id = c.id
GROUP BY c.nombre
ORDER BY total_votos DESC;
```

---

## DESPLIEGUE EN PRODUCCIÓN

### Despliegue en Render.com

#### Requisitos Previos

1. Cuenta en Render.com
2. Repositorio Git del proyecto
3. Base de datos preparada localmente

#### Configuración Inicial

El archivo `render.yaml` ya está configurado con:

```yaml
services:
  - type: web
    name: sistema-electoral
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn run:app"
```

#### Pasos de Despliegue

1. **Conectar Repositorio**:
   - Ir a Render.com
   - Clic en "New +"
   - Seleccionar "Web Service"
   - Conectar repositorio Git

2. **Configurar Variables de Entorno**:
   ```
   FLASK_ENV=production
   SECRET_KEY=tu_clave_secreta_muy_segura
   DATABASE_URL=sqlite:///instance/electoral.db
   ```

3. **Desplegar**:
   - Clic en "Create Web Service"
   - Esperar a que termine el build
   - Verificar que el servicio esté "Live"

#### Subir Base de Datos a Render

Usar el script `upload_db_to_render.py`:

```bash
python upload_db_to_render.py
```

El script:
1. Comprime la BD con gzip
2. La sube a Render via API
3. Render la descomprime automáticamente
4. Reinicia el servicio

#### Inicialización Automática

El sistema se auto-inicializa en cada inicio:
- Verifica si existe `instance/electoral.db`
- Si no existe, ejecuta `load_basic_data_simple.py`
- Carga todos los datos de Caquetá

### Configuración de Dominio

#### Dominio Personalizado

1. En Render, ir a Settings
2. Sección "Custom Domain"
3. Agregar tu dominio
4. Configurar DNS según instrucciones

#### SSL/HTTPS

- Render proporciona SSL automático
- Certificados Let's Encrypt gratuitos
- Renovación automática

### Monitoreo en Producción

#### Logs

Ver logs en tiempo real:
```bash
# En Render dashboard
Logs → View Logs
```

#### Métricas

Render proporciona:
- CPU usage
- Memory usage
- Request count
- Response times

### Mantenimiento

#### Actualizar Código

```bash
git add .
git commit -m "Actualización"
git push origin main
```

Render detecta el push y redespliega automáticamente.

#### Actualizar Base de Datos

```bash
# Subir nueva versión de BD
python upload_db_to_render.py
```

#### Resetear Contraseñas en Producción

Usar el endpoint especial:
```
POST /api/reset-passwords-production
Body: {
  "secret_key": "tu_clave_secreta",
  "username": "admin",
  "new_password": "nueva_contraseña"
}
```

### Backup en Producción

#### Descargar BD desde Render

```bash
# Usar Render CLI o API
curl https://tu-app.onrender.com/api/download-db \
  -H "Authorization: Bearer tu_token" \
  -o electoral_backup.db
```

#### Programar Backups Automáticos

Configurar cron job en Render:
```yaml
services:
  - type: cron
    name: backup-db
    schedule: "0 2 * * *"  # Diario a las 2 AM
    command: "python scripts/backup_db.py"
```

---

## SOLUCIÓN DE PROBLEMAS

### Problemas Comunes y Soluciones

#### 1. No puedo iniciar sesión

**Síntomas**: Error "Usuario o contraseña incorrectos"

**Soluciones**:
```python
# Resetear contraseña del admin
from backend.models.user import User
from backend.app import db, app

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    admin.set_password('admin123')
    db.session.commit()
    print("Contraseña reseteada")
```

#### 2. Base de datos no se inicializa

**Síntomas**: Error al acceder a `/init-db`

**Soluciones**:
```bash
# Eliminar BD corrupta
rm instance/electoral.db

# Crear carpeta instance si no existe
mkdir instance

# Ejecutar script de inicialización
python backend/scripts/load_basic_data_simple.py
```

#### 3. Botón "Nuevo Formulario" deshabilitado

**Síntomas**: No se puede crear formulario E-14

**Soluciones**:
1. Verificar que el testigo haya registrado presencia
2. Revisar en consola del navegador (F12) si hay errores
3. Verificar que el endpoint `/api/testigo/registrar-presencia` funcione

```javascript
// Verificar en consola del navegador
fetch('/api/testigo/registrar-presencia', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
})
.then(r => r.json())
.then(d => console.log(d));
```

#### 4. No aparecen candidatos en formulario

**Síntomas**: Lista de candidatos vacía

**Soluciones**:
1. Verificar que el tipo de elección tenga candidatos asignados
2. Verificar que los candidatos estén activos
3. Revisar en Super Admin → Candidatos

```sql
-- Verificar candidatos por tipo de elección
SELECT c.nombre, te.nombre as tipo_eleccion
FROM candidatos c
JOIN tipos_eleccion te ON c.tipo_eleccion_id = te.id
WHERE c.activo = 1;
```

#### 5. Error al enviar formulario

**Síntomas**: "Error al guardar formulario"

**Soluciones**:
1. Verificar conexión a internet
2. Revisar logs del servidor
3. Verificar que todos los campos estén llenos
4. Verificar que los totales sean correctos

```bash
# Ver logs en tiempo real
tail -f logs/app.log
```

#### 6. Archivos estáticos no cargan (CSS/JS)

**Síntomas**: Página sin estilos

**Soluciones**:
```python
# Verificar configuración de WhiteNoise en config.py
WHITENOISE_ENABLED = True
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'frontend', 'static')

# Recolectar archivos estáticos
python manage.py collectstatic
```

#### 7. Error de CORS en producción

**Síntomas**: Errores de Cross-Origin en consola

**Soluciones**:
```python
# En backend/app.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

#### 8. Base de datos bloqueada

**Síntomas**: "Database is locked"

**Soluciones**:
```bash
# Verificar procesos usando la BD
lsof instance/electoral.db

# Matar procesos si es necesario
kill -9 <PID>

# Reiniciar aplicación
python run.py
```

#### 9. Memoria insuficiente en Render

**Síntomas**: Servicio se reinicia constantemente

**Soluciones**:
1. Upgrade a plan con más memoria
2. Optimizar consultas SQL
3. Implementar caché
4. Reducir tamaño de BD

#### 10. Testigos duplicados

**Síntomas**: Mismo testigo aparece múltiples veces

**Soluciones**:
```sql
-- Encontrar duplicados
SELECT cedula, COUNT(*) as count
FROM testigos
GROUP BY cedula
HAVING count > 1;

-- Eliminar duplicados (mantener el primero)
DELETE FROM testigos
WHERE id NOT IN (
    SELECT MIN(id)
    FROM testigos
    GROUP BY cedula
);
```

### Comandos de Diagnóstico

#### Verificar estado del sistema

```bash
# Ver versión de Python
python --version

# Ver paquetes instalados
pip list

# Verificar BD
sqlite3 instance/electoral.db ".tables"

# Ver tamaño de BD
ls -lh instance/electoral.db

# Verificar puerto en uso
netstat -an | grep 5000
```

#### Verificar datos en BD

```bash
# Entrar a SQLite
sqlite3 instance/electoral.db

# Comandos útiles
.tables                    # Ver todas las tablas
.schema users             # Ver estructura de tabla
SELECT COUNT(*) FROM testigos;  # Contar testigos
.quit                     # Salir
```

### Logs y Debugging

#### Habilitar modo debug

```python
# En run.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### Ver logs en navegador

1. Abrir DevTools (F12)
2. Ir a pestaña "Console"
3. Ver errores JavaScript
4. Ir a pestaña "Network" para ver requests

#### Logs del servidor

```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Buscar errores
grep ERROR logs/app.log

# Ver últimas 100 líneas
tail -n 100 logs/app.log
```

---

## API REFERENCE

### Autenticación

#### POST /api/auth/login

Iniciar sesión en el sistema.

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "super_admin"
  },
  "redirect": "/super-admin/dashboard"
}
```

#### POST /api/auth/logout

Cerrar sesión.

**Response:**
```json
{
  "success": true,
  "message": "Sesión cerrada"
}
```

### Endpoints del Testigo

#### POST /api/testigo/registrar-presencia

Registrar presencia del testigo en el puesto.

**Request:**
```json
{
  "testigo_id": 1,
  "puesto_id": 1,
  "timestamp": "2027-03-18T08:00:00"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Presencia registrada correctamente"
}
```

#### GET /api/testigo/tipos-eleccion

Obtener tipos de elección disponibles.

**Response:**
```json
{
  "success": true,
  "tipos": [
    {
      "id": 1,
      "nombre": "Gobernación",
      "descripcion": "Elección de Gobernador",
      "tipo_votacion": "uninominal"
    }
  ]
}
```

#### GET /api/testigo/partidos

Obtener partidos políticos activos.

**Response:**
```json
{
  "success": true,
  "partidos": [
    {
      "id": 1,
      "nombre": "Partido Liberal",
      "sigla": "PL",
      "color": "#FF0000"
    }
  ]
}
```

#### GET /api/testigo/candidatos?tipo_eleccion_id=1

Obtener candidatos por tipo de elección.

**Response:**
```json
{
  "success": true,
  "candidatos": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "partido_id": 1,
      "partido_nombre": "Partido Liberal",
      "numero_lista": null
    }
  ]
}
```

#### POST /api/testigo/formulario-e14

Enviar formulario E-14.

**Request:**
```json
{
  "testigo_id": 1,
  "puesto_id": 1,
  "mesa_numero": 1,
  "tipo_eleccion_id": 1,
  "votantes_registrados": 300,
  "votos": [
    {
      "candidato_id": 1,
      "votos": 150
    },
    {
      "candidato_id": 2,
      "votos": 100
    }
  ],
  "votos_blanco": 20,
  "votos_nulos": 10,
  "votos_no_marcados": 20
}
```

**Response:**
```json
{
  "success": true,
  "message": "Formulario guardado correctamente",
  "formulario_id": 123
}
```

#### GET /api/testigo/mis-formularios

Obtener formularios enviados por el testigo.

**Response:**
```json
{
  "success": true,
  "formularios": [
    {
      "id": 123,
      "mesa_numero": 1,
      "tipo_eleccion": "Gobernación",
      "fecha_envio": "2027-03-18T16:30:00",
      "total_votos": 300
    }
  ]
}
```

### Endpoints del Coordinador

#### GET /api/coordinador/dashboard-data

Obtener datos del dashboard del coordinador.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_testigos": 50,
    "testigos_presentes": 45,
    "formularios_recibidos": 120,
    "cobertura_porcentaje": 90
  }
}
```

#### GET /api/coordinador/testigos?zona_id=1

Obtener testigos de una zona.

**Response:**
```json
{
  "success": true,
  "testigos": [
    {
      "id": 1,
      "nombre": "María García",
      "cedula": "123456789",
      "puesto": "Colegio San José",
      "presencia": true,
      "formularios_enviados": 3
    }
  ]
}
```

#### GET /api/coordinador/formularios?zona_id=1

Obtener formularios de una zona.

**Response:**
```json
{
  "success": true,
  "formularios": [
    {
      "id": 123,
      "testigo": "María García",
      "puesto": "Colegio San José",
      "mesa": 1,
      "tipo_eleccion": "Gobernación",
      "fecha_envio": "2027-03-18T16:30:00"
    }
  ]
}
```

### Endpoints del Super Admin

#### GET /api/super-admin/partidos

Obtener todos los partidos.

**Response:**
```json
{
  "success": true,
  "partidos": [
    {
      "id": 1,
      "nombre": "Partido Liberal",
      "sigla": "PL",
      "color": "#FF0000",
      "activo": true
    }
  ]
}
```

#### POST /api/super-admin/partidos

Crear nuevo partido.

**Request:**
```json
{
  "nombre": "Nuevo Partido",
  "sigla": "NP",
  "color": "#00FF00",
  "logo_url": "https://ejemplo.com/logo.png"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Partido creado correctamente",
  "partido_id": 10
}
```

#### PUT /api/super-admin/partidos/:id

Actualizar partido.

**Request:**
```json
{
  "nombre": "Partido Actualizado",
  "sigla": "PA",
  "color": "#0000FF"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Partido actualizado correctamente"
}
```

#### DELETE /api/super-admin/partidos/:id

Eliminar partido (soft delete).

**Response:**
```json
{
  "success": true,
  "message": "Partido desactivado correctamente"
}
```

#### GET /api/super-admin/candidatos

Obtener todos los candidatos.

**Response:**
```json
{
  "success": true,
  "candidatos": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "partido": "Partido Liberal",
      "tipo_eleccion": "Gobernación",
      "activo": true
    }
  ]
}
```

#### POST /api/super-admin/candidatos

Crear nuevo candidato.

**Request:**
```json
{
  "nombre": "Pedro González",
  "partido_id": 1,
  "tipo_eleccion_id": 1,
  "numero_lista": null,
  "foto_url": "https://ejemplo.com/foto.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Candidato creado correctamente",
  "candidato_id": 50
}
```

#### GET /api/super-admin/usuarios

Obtener todos los usuarios.

**Response:**
```json
{
  "success": true,
  "usuarios": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@ejemplo.com",
      "role": "super_admin",
      "activo": true
    }
  ]
}
```

#### POST /api/super-admin/usuarios

Crear nuevo usuario.

**Request:**
```json
{
  "username": "nuevo_usuario",
  "email": "usuario@ejemplo.com",
  "password": "password123",
  "role": "coordinador",
  "zona_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "Usuario creado correctamente",
  "usuario_id": 25
}
```

### Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Datos inválidos
- **401 Unauthorized**: No autenticado
- **403 Forbidden**: Sin permisos
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

### Manejo de Errores

Todas las respuestas de error siguen este formato:

```json
{
  "success": false,
  "error": "Descripción del error",
  "code": "ERROR_CODE"
}
```

---

