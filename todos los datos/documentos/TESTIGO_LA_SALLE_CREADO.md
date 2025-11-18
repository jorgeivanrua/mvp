# TESTIGO CREADO - I.E. JUAN BAUTISTA LA SALLE

## ✅ Testigo Creado Exitosamente

### 📋 Credenciales de Acceso

```
Nombre: Testigo La Salle Mesa 01
Contraseña: test123
Rol: Testigo Electoral
```

### 📍 Ubicación Asignada

- **Departamento:** CAQUETÁ (código 18)
- **Municipio:** FLORENCIA (código 01)
- **Zona:** 01
- **Puesto Electoral:** I.E. JUAN BAUTISTA LA SALLE
- **Mesa:** Mesa 1
- **Total Votantes:** 2,675

### 🔐 Cómo Iniciar Sesión

1. Ir a la pantalla de login del sistema
2. Seleccionar los siguientes datos:
   - **Rol:** Testigo Electoral
   - **Departamento:** CAQUETA
   - **Municipio:** FLORENCIA
   - **Zona:** CAQUETA - FLORENCIA - Zona 01
   - **Puesto Electoral:** I.E. JUAN BAUTISTA LA SALLE
   - **Contraseña:** test123

### 📊 Datos Cargados en el Sistema

#### Departamento Caquetá
- ✅ 1 Departamento
- ✅ 16 Municipios
- ✅ 38 Zonas
- ✅ 150 Puestos
- ✅ 196 Mesas

#### Florencia
- ✅ 51 Puestos electorales
- ✅ Múltiples mesas por puesto

### 🎯 Funcionalidades Disponibles para el Testigo

Una vez que inicie sesión, el testigo podrá:

1. **Registrar Presencia**
   - Marcar su presencia en la mesa electoral
   - El sistema registra fecha y hora

2. **Crear Formulario E14**
   - Ingresar votos por candidato
   - Ingresar votos por partido
   - Registrar votos blancos y nulos
   - Agregar observaciones
   - Tomar foto del formulario físico

3. **Guardar Borradores**
   - Guardar formularios localmente (offline)
   - Sincronizar cuando haya conexión

4. **Reportar Incidentes**
   - Reportar irregularidades
   - Adjuntar evidencias fotográficas

5. **Reportar Delitos Electorales**
   - Reportar delitos observados
   - Clasificar por gravedad

### 📝 Flujo de Trabajo del Testigo

```
1. LOGIN
   ↓
2. REGISTRAR PRESENCIA
   ↓
3. ESPERAR INICIO DE VOTACIÓN
   ↓
4. DURANTE LA VOTACIÓN
   - Observar el proceso
   - Reportar incidentes si es necesario
   ↓
5. AL CIERRE
   - Obtener copia del formulario E14
   - Ingresar datos al sistema
   - Tomar foto del formulario
   ↓
6. ENVIAR FORMULARIO
   - Estado: "pendiente"
   - Va al Coordinador de Puesto
   ↓
7. COORDINADOR VALIDA
   - Aprueba → Estado: "validado"
   - Rechaza → Testigo debe corregir
```

### 🔄 Estados del Formulario E14

- **borrador:** Guardado localmente, no enviado
- **pendiente:** Enviado, esperando validación
- **validado:** Aprobado por coordinador
- **rechazado:** Devuelto para corrección

### 📱 Endpoints Disponibles para Testigo

```
POST   /api/testigo/registrar-presencia
POST   /api/formularios
GET    /api/formularios/mis-formularios
PUT    /api/formularios/{id}
GET    /api/configuracion/candidatos
POST   /api/testigo/incidentes
POST   /api/testigo/delitos
GET    /api/testigo/stats
```

### 🗂️ Estructura de Datos del Formulario E14

```json
{
  "mesa_id": 607,
  "tipo_eleccion_id": 1,
  "total_votantes_registrados": 2675,
  "total_votos": 2500,
  "votos_validos": 2450,
  "votos_nulos": 30,
  "votos_blanco": 20,
  "tarjetas_no_marcadas": 175,
  "total_tarjetas": 2675,
  "estado": "pendiente",
  "observaciones": "Votación transcurrió con normalidad",
  "votos_candidatos": [
    {
      "candidato_id": 1,
      "votos": 1200
    },
    {
      "candidato_id": 2,
      "votos": 1250
    }
  ],
  "votos_partidos": [
    {
      "partido_id": 1,
      "votos": 1200
    },
    {
      "partido_id": 2,
      "votos": 1250
    }
  ]
}
```

### ⚠️ Validaciones del Sistema

El sistema valida automáticamente:
- ✅ Total de votos = votos válidos + votos nulos + votos blancos
- ✅ Suma de votos por candidato = votos válidos
- ✅ Total de votos ≤ total de votantes registrados
- ✅ Todos los campos obligatorios completos

### 🆘 Soporte

Para más información consultar:
- `GUIA_FLUJO_ROLES_SISTEMA_ELECTORAL.md` - Guía completa de roles
- `CREDENCIALES_USUARIOS.md` - Todas las credenciales del sistema
- `GUIA_COMPLETA_SISTEMA_ELECTORAL.md` - Documentación técnica

---

**Fecha de Creación:** 2025-11-17
**Sistema:** Sistema Electoral - Caquetá
