# Gestión de Departamentos Electorales

Este directorio contiene scripts para la carga y eliminación completa de departamentos electorales de forma fácil, fluida y coherente.

## 🎯 Objetivo

Permitir cargar o eliminar cualquier departamento (como Quindío) de forma completa, incluyendo:
- Ubicaciones (departamento, municipios, zonas, puestos, mesas)
- Usuarios (coordinadores y testigos)
- Datos electorales (formularios, reportes, incidentes)
- Configuración del departamento

## 📁 Scripts Disponibles

### 1. Gestor Principal
- **`departamentos_manager.py`** - Gestor unificado con menú interactivo

### 2. Scripts Específicos para Quindío
- **`cargar_quindio.py`** - Cargar Quindío de forma simplificada
- **`eliminar_quindio.py`** - Eliminar Quindío de forma simplificada

### 3. Scripts Genéricos
- **`cargar_departamento.py`** - Cargar cualquier departamento
- **`eliminar_departamento.py`** - Eliminar cualquier departamento

## 🚀 Uso Rápido

### Cargar Quindío como departamento principal
```bash
python scripts/cargar_quindio.py --principal
```

### Cargar cualquier departamento
```bash
# Listar departamentos disponibles
python scripts/cargar_departamento.py --listar

# Cargar Caquetá como departamento secundario
python scripts/cargar_departamento.py 44

# Cargar Antioquia como departamento principal
python scripts/cargar_departamento.py 05 --principal
```

### Eliminar departamentos
```bash
# Eliminar Quindío (requiere confirmación)
python scripts/eliminar_quindio.py --confirmar

# Eliminar cualquier departamento
python scripts/eliminar_departamento.py 44 --confirmar

# Ver estado actual de departamentos
python scripts/eliminar_departamento.py --estado
```

### Gestor interactivo
```bash
python scripts/departamentos_manager.py
```

## 📋 Códigos de Departamentos Comunes

| Código | Departamento |
|--------|-------------|
| 05     | ANTIOQUIA   |
| 08     | ATLÁNTICO   |
| 11     | BOGOTÁ D.C. |
| 13     | BOLÍVAR     |
| 15     | BOYACÁ      |
| 17     | CALDAS      |
| 18     | CAQUETÁ     |
| 19     | CAUCA       |
| 20     | CESAR       |
| 23     | CÓRDOBA     |
| 25     | CUNDINAMARCA|
| 26     | QUINDÍO     |
| 27     | RISARALDA   |
| 41     | HUILA       |
| 44     | LA GUAJIRA  |
| 47     | MAGDALENA   |
| 50     | META        |
| 52     | NARIÑO      |
| 54     | NORTE DE SANTANDER |
| 63     | QUINDÍO     |
| 66     | RISARALDA   |
| 68     | SANTANDER   |
| 70     | SUCRE       |
| 73     | TOLIMA      |
| 76     | VALLE DEL CAUCA |

## ⚙️ Características del Sistema

### ✅ Carga Completa
- **Ubicaciones jerárquicas**: Departamento → Municipios → Zonas → Puestos → Mesas
- **Usuarios automáticos**: Coordinadores departamentales, municipales, de puesto y testigos
- **Datos geográficos**: Coordenadas, direcciones, información demográfica
- **Configuración**: Habilitación automática del departamento

### ✅ Eliminación Completa
- **Datos electorales**: Formularios E-14, votos, reportes de participación
- **Incidentes y delitos**: Reportes y evidencias fotográficas
- **Usuarios**: Coordinadores y testigos (excepto super_admin)
- **Ubicaciones**: Todas las ubicaciones del departamento
- **Configuración**: Configuración del departamento

### ✅ Seguridad
- **Confirmaciones múltiples**: Evita eliminaciones accidentales
- **Transacciones**: Rollback automático en caso de error
- **Validaciones**: Verificación de existencia antes de procesar
- **Logs detallados**: Información completa del proceso

## 🔐 Credenciales por Defecto

Todos los usuarios creados tienen la contraseña: **`test123`**

### Tipos de usuarios creados:
- **Coordinador Departamental**: 1 por departamento
- **Coordinadores Municipales**: 1 por municipio
- **Coordinadores de Puesto**: 1 por puesto de votación
- **Testigos Electorales**: 1 por mesa de votación

## 📊 Ejemplo de Flujo Completo

### 1. Cargar Quindío como principal
```bash
python scripts/cargar_quindio.py --principal
```

### 2. Cargar Caquetá como secundario
```bash
python scripts/cargar_departamento.py 18
```

### 3. Ver estado del sistema
```bash
python scripts/eliminar_departamento.py --estado
```

### 4. Eliminar Caquetá
```bash
python scripts/eliminar_departamento.py 18 --confirmar
```

## 🛠️ Solución de Problemas

### Error: "Archivo divipola.csv no encontrado"
- Verificar que existe el archivo `data/divipola.csv`
- Ejecutar desde el directorio raíz del proyecto

### Error: "Departamento no encontrado"
- Usar `--listar` para ver departamentos disponibles
- Verificar que el código sea correcto (ej: '26' para Quindío)

### Error: "Error de importación"
- Ejecutar desde el directorio raíz del proyecto
- Verificar que las dependencias estén instaladas

### Error de base de datos
- Verificar conexión a la base de datos
- Revisar variables de entorno en `.env`

## 🔄 Migración de Datos

Para migrar de un departamento a otro:

1. **Respaldar datos importantes** (si es necesario)
2. **Eliminar departamento actual**:
   ```bash
   python scripts/eliminar_departamento.py <codigo_actual> --confirmar
   ```
3. **Cargar nuevo departamento**:
   ```bash
   python scripts/cargar_departamento.py <codigo_nuevo> --principal
   ```

## 📝 Notas Importantes

- **Un solo departamento principal**: Solo puede haber un departamento marcado como principal
- **Eliminación irreversible**: Los datos eliminados no se pueden recuperar
- **Transacciones atómicas**: Si hay error, se revierten todos los cambios
- **Usuarios únicos**: Cada usuario está vinculado a su ubicación específica
- **Cédulas automáticas**: Los testigos reciben cédulas generadas automáticamente

## 🆘 Soporte

Para problemas o dudas:
1. Revisar los logs de error detallados
2. Verificar la documentación del proyecto
3. Contactar al equipo de desarrollo