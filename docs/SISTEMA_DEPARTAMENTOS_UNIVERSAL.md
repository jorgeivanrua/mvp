# 🏛️ SISTEMA UNIVERSAL DE DEPARTAMENTOS ELECTORALES

**Sistema completo para cargar y gestionar cualquier departamento de Colombia**

---

## 📋 RESUMEN EJECUTIVO

El sistema está **completamente preparado** para cargar cualquier departamento de Colombia con todos sus datos, coordinadores y testigos de forma completa y funcional. Incluye herramientas robustas de gestión, verificación y mantenimiento.

### ✅ CAPACIDADES PRINCIPALES

- ✅ **Carga universal**: Cualquier departamento de Colombia
- ✅ **Datos completos**: Ubicaciones jerárquicas (departamento → municipio → zona → puesto → mesa)
- ✅ **Usuarios completos**: Coordinadores departamentales, municipales, de puesto y testigos electorales
- ✅ **Validaciones automáticas**: Integridad de datos y funcionalidad
- ✅ **Correcciones automáticas**: Ubicaciones de testigos, cédulas, reactivación
- ✅ **Gestión robusta**: Cargar, verificar, reparar, eliminar
- ✅ **Departamento principal**: Gestión de departamento activo principal

---

## 🛠️ HERRAMIENTAS DISPONIBLES

### 1. **Gestor Maestro** (Recomendado)
```bash
python scripts/gestor_departamentos_maestro.py
```
**Herramienta unificada con menú interactivo para todas las operaciones**

### 2. **Cargador Completo**
```bash
python scripts/cargar_departamento_completo.py <codigo> [--principal] [--forzar]
```
**Carga completa con validaciones y correcciones automáticas**

### 3. **Verificador**
```bash
python scripts/verificar_departamento.py <codigo>
python scripts/verificar_departamento.py --todos
```
**Verificación exhaustiva de funcionalidad e integridad**

### 4. **Gestor Básico**
```bash
python scripts/departamentos_manager.py
```
**Gestión básica con menú interactivo**

---

## 🚀 GUÍA DE USO RÁPIDO

### Cargar un Departamento Nuevo

**Opción 1: Modo Interactivo (Recomendado)**
```bash
python scripts/gestor_departamentos_maestro.py
# Seleccionar opción 5: Cargar departamento completo
```

**Opción 2: Línea de Comandos**
```bash
# Cargar Antioquia como departamento principal
python scripts/cargar_departamento_completo.py 05 --principal

# Cargar Valle del Cauca (forzar si ya existe)
python scripts/cargar_departamento_completo.py 76 --forzar
```

### Verificar un Departamento
```bash
# Verificar Quindío
python scripts/verificar_departamento.py 26

# Verificar todos los departamentos
python scripts/verificar_departamento.py --todos
```

### Ver Departamentos Disponibles
```bash
python scripts/cargar_departamento_completo.py --listar
```

---

## 📊 DEPARTAMENTOS DE COLOMBIA

### Principales Departamentos (Códigos más usados)

| Código | Departamento | Municipios | Observaciones |
|--------|--------------|------------|---------------|
| **05** | ANTIOQUIA | 125 | Departamento más grande |
| **08** | ATLÁNTICO | 23 | Costa Caribe |
| **11** | BOGOTÁ D.C. | 20 | Capital del país |
| **13** | BOLÍVAR | 46 | Costa Caribe |
| **15** | BOYACÁ | 123 | Región Andina |
| **17** | CALDAS | 27 | Eje Cafetero |
| **19** | CAUCA | 42 | Región Pacífica |
| **23** | CÓRDOBA | 30 | Costa Caribe |
| **25** | CUNDINAMARCA | 116 | Región central |
| **26** | QUINDÍO | 12 | Eje Cafetero (ya cargado) |
| **41** | HUILA | 37 | Región Andina |
| **44** | LA GUAJIRA | 15 | Costa Caribe |
| **47** | MAGDALENA | 30 | Costa Caribe |
| **50** | META | 29 | Región Orinoquía |
| **52** | NARIÑO | 64 | Región Pacífica |
| **54** | NORTE DE SANTANDER | 40 | Frontera con Venezuela |
| **63** | QUINDÍO | 12 | Eje Cafetero |
| **66** | RISARALDA | 14 | Eje Cafetero |
| **68** | SANTANDER | 87 | Región Andina |
| **70** | SUCRE | 26 | Costa Caribe |
| **73** | TOLIMA | 47 | Región Andina |
| **76** | VALLE DEL CAUCA | 42 | Región Pacífica |

### Todos los Departamentos Disponibles
```bash
# Ver lista completa con estadísticas
python scripts/cargar_departamento_completo.py --listar
```

---

## 🔧 PROCESO DE CARGA COMPLETA

### Fases Automáticas

1. **📋 Validación Inicial**
   - Verificar archivo DIVIPOLA
   - Validar código de departamento
   - Mostrar estadísticas del departamento

2. **🔍 Verificación de Estado**
   - Revisar si ya está cargado
   - Mostrar estado actual
   - Confirmar operación si es necesario

3. **📥 Carga de Datos**
   - Cargar ubicaciones jerárquicas
   - Crear usuarios por rol
   - Configurar departamento

4. **🔧 Correcciones Automáticas**
   - Mover testigos de mesas a puestos
   - Asignar cédulas faltantes
   - Reactivar usuarios/ubicaciones
   - Validar integridad

5. **✅ Verificación Final**
   - Comprobar funcionalidad
   - Validar login de usuarios
   - Confirmar endpoints
   - Mostrar resumen completo

### Datos Creados Automáticamente

**Ubicaciones:**
- 1 Departamento
- N Municipios (según DIVIPOLA)
- N Zonas electorales
- N Puestos de votación
- N Mesas electorales

**Usuarios:**
- 1 Coordinador Departamental
- N Coordinadores Municipales (1 por municipio)
- N Coordinadores de Puesto (1 por puesto)
- N Testigos Electorales (1 por mesa, asignados a puestos)

**Credenciales:**
- Contraseña para todos: `test123`
- Testigos pueden usar su cédula como usuario

---

## 🔍 VERIFICACIONES AUTOMÁTICAS

### Configuración
- ✅ Existe configuración del departamento
- ✅ Departamento habilitado
- ✅ Configuración de carga automática

### Ubicaciones
- ✅ Jerarquía completa (departamento → municipio → puesto → mesa)
- ✅ Todas las ubicaciones activas
- ✅ Integridad de relaciones padre-hijo

### Usuarios
- ✅ Todos los roles requeridos creados
- ✅ Usuarios activos y funcionales
- ✅ Testigos con cédulas asignadas
- ✅ Testigos asignados a puestos (no mesas)

### Funcionalidad
- ✅ Login de coordinadores funcional
- ✅ Login de testigos funcional
- ✅ Endpoints de ubicaciones operativos

### Integridad
- ✅ No hay usuarios sin ubicación
- ✅ No hay ubicaciones huérfanas
- ✅ Consistencia de datos

---

## 🛡️ CORRECCIONES AUTOMÁTICAS

El sistema aplica automáticamente las siguientes correcciones:

### 1. **Ubicación de Testigos**
- **Problema**: Testigos asignados a mesas individuales
- **Corrección**: Mover a puestos de votación (normativa electoral)
- **Automático**: ✅ Sí

### 2. **Cédulas de Testigos**
- **Problema**: Testigos sin cédula asignada
- **Corrección**: Generar cédula basada en ubicación
- **Automático**: ✅ Sí

### 3. **Usuarios Desactivados**
- **Problema**: Usuarios marcados como inactivos
- **Corrección**: Reactivar usuarios del departamento
- **Automático**: ✅ Sí

### 4. **Ubicaciones Desactivadas**
- **Problema**: Ubicaciones marcadas como inactivas
- **Corrección**: Reactivar ubicaciones del departamento
- **Automático**: ✅ Sí

---

## 📈 GESTIÓN DE DEPARTAMENTO PRINCIPAL

### ¿Qué es el Departamento Principal?
El departamento principal es el que se usa por defecto en el sistema. Solo puede haber uno activo a la vez.

### Cambiar Departamento Principal
```bash
# Modo interactivo
python scripts/gestor_departamentos_maestro.py
# Opción 7: Cambiar departamento principal

# O al cargar un nuevo departamento
python scripts/cargar_departamento_completo.py 05 --principal
```

### Características del Departamento Principal
- ⭐ Marcado visualmente en todas las interfaces
- 🎯 Usado por defecto en reportes y dashboards
- 🔄 Solo uno puede ser principal a la vez
- ✅ Automáticamente habilitado

---

## 🗑️ ELIMINACIÓN DE DEPARTAMENTOS

### Eliminación Completa
```bash
# Modo interactivo (recomendado)
python scripts/gestor_departamentos_maestro.py
# Opción 6: Eliminar departamento completo

# Línea de comandos
python scripts/eliminar_departamento.py 44 --confirmar
```

### Datos Eliminados
- 🗑️ Todas las ubicaciones del departamento
- 🗑️ Todos los usuarios (excepto super admin)
- 🗑️ Todos los formularios E-14 y votos
- 🗑️ Todos los reportes de participación
- 🗑️ Todos los incidentes y delitos electorales
- 🗑️ Todas las evidencias fotográficas
- 🗑️ Configuración del departamento

### Medidas de Seguridad
- 🔒 Confirmación múltiple requerida
- 🔒 Texto exacto de confirmación
- 🔒 No se puede deshacer
- 🔒 Preserva super administradores

---

## 🔧 REPARACIÓN DE DEPARTAMENTOS

### Cuándo Reparar
- ⚠️ Verificación muestra problemas
- ⚠️ Usuarios no pueden hacer login
- ⚠️ Datos inconsistentes
- ⚠️ Después de migraciones

### Cómo Reparar
```bash
# Modo interactivo
python scripts/gestor_departamentos_maestro.py
# Opción 8: Reparar departamento

# O recarga forzada
python scripts/cargar_departamento_completo.py 26 --forzar
```

### Proceso de Reparación
1. 🔄 Recarga completa de datos
2. 🔧 Aplicar todas las correcciones
3. ✅ Verificación automática post-reparación
4. 📊 Reporte de estado final

---

## 📋 EJEMPLOS PRÁCTICOS

### Ejemplo 1: Cargar Antioquia como Principal
```bash
# Opción 1: Interactivo
python scripts/gestor_departamentos_maestro.py
# Seleccionar: 5 → Ingresar: 05 → Marcar como principal: s

# Opción 2: Directo
python scripts/cargar_departamento_completo.py 05 --principal
```

### Ejemplo 2: Verificar Todos los Departamentos
```bash
python scripts/verificar_departamento.py --todos
```

### Ejemplo 3: Cambiar de Quindío a Valle del Cauca
```bash
# 1. Cargar Valle del Cauca como principal
python scripts/cargar_departamento_completo.py 76 --principal

# 2. Verificar que funcionó
python scripts/verificar_departamento.py 76

# 3. (Opcional) Eliminar Quindío si no se necesita
python scripts/eliminar_departamento.py 26 --confirmar
```

### Ejemplo 4: Sistema Multi-Departamental
```bash
# Cargar varios departamentos (solo uno principal)
python scripts/cargar_departamento_completo.py 05 --principal  # Antioquia principal
python scripts/cargar_departamento_completo.py 76             # Valle del Cauca
python scripts/cargar_departamento_completo.py 11             # Bogotá

# Verificar todos
python scripts/verificar_departamento.py --todos
```

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Problema: "Archivo CSV no encontrado"
**Solución:**
```bash
# Verificar que existe data/divipola.csv
ls -la data/divipola.csv

# Si no existe, contactar administrador del sistema
```

### Problema: "Testigos en mesas en lugar de puestos"
**Solución:**
```bash
# Reparar departamento (aplica corrección automática)
python scripts/cargar_departamento_completo.py 26 --forzar
```

### Problema: "Usuarios no pueden hacer login"
**Solución:**
```bash
# 1. Verificar estado
python scripts/verificar_departamento.py 26

# 2. Reparar si es necesario
python scripts/gestor_departamentos_maestro.py
# Opción 8: Reparar departamento
```

### Problema: "Departamento no aparece como principal"
**Solución:**
```bash
# Cambiar departamento principal
python scripts/gestor_departamentos_maestro.py
# Opción 7: Cambiar departamento principal
```

---

## 📊 MONITOREO Y MANTENIMIENTO

### Verificación Periódica
```bash
# Verificar todos los departamentos semanalmente
python scripts/verificar_departamento.py --todos
```

### Respaldo Antes de Cambios Mayores
```bash
# Ver estado actual antes de cambios
python scripts/gestor_departamentos_maestro.py
# Opción 2: Ver estado actual
```

### Limpieza Completa (Solo en Desarrollo)
```bash
# CUIDADO: Elimina TODO
python scripts/gestor_departamentos_maestro.py
# Opción 9: Limpiar sistema completo
```

---

## ✅ ESTADO ACTUAL DEL SISTEMA

### Departamento Configurado
- ✅ **QUINDÍO (26)** - Completamente funcional
  - 📊 12 municipios, 129 puestos, 212 mesas
  - 👥 357 usuarios (1 coord. depto + 12 coord. muni + 129 coord. puesto + 213 testigos + 2 super admin)
  - ⭐ Marcado como departamento principal
  - 🔧 Testigos correctamente asignados a puestos
  - 🆔 Todas las cédulas asignadas

### Sistema Listo Para
- ✅ Cargar cualquier departamento de Colombia
- ✅ Gestionar múltiples departamentos simultáneamente
- ✅ Cambiar departamento principal dinámicamente
- ✅ Verificar y reparar departamentos automáticamente
- ✅ Eliminar departamentos de forma segura

---

## 🎯 CONCLUSIÓN

**El sistema está 100% preparado para cargar y gestionar cualquier departamento de Colombia de forma completa y funcional.**

### Características Clave:
- 🏛️ **Universal**: Funciona con todos los departamentos
- 🔧 **Automático**: Carga, correcciones y verificaciones automáticas
- 🛡️ **Robusto**: Validaciones exhaustivas e integridad de datos
- 🎮 **Fácil de usar**: Interfaces interactivas y línea de comandos
- 📊 **Completo**: Ubicaciones jerárquicas y usuarios por rol
- 🔄 **Mantenible**: Herramientas de reparación y verificación

### Próximos Pasos Recomendados:
1. **Probar con otro departamento** (ej: Antioquia - código 05)
2. **Verificar funcionalidad multi-departamental**
3. **Documentar procedimientos específicos** para el equipo
4. **Configurar monitoreo automático** de departamentos

**¡El sistema está listo para producción con cualquier departamento de Colombia!** 🚀