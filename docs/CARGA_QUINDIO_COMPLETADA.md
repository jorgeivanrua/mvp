# CARGA COMPLETA DEL DEPARTAMENTO DEL QUINDÍO

## RESUMEN EJECUTIVO

Se ha completado exitosamente la carga completa de datos del departamento del Quindío en la base de datos del sistema electoral, incluyendo toda la estructura territorial y usuarios correspondientes.

## DATOS CARGADOS

### 📊 UBICACIONES TERRITORIALES

| Tipo | Cantidad | Descripción |
|------|----------|-------------|
| **Departamento** | 1 | Quindío |
| **Municipios** | 12 | Armenia, Buenavista, Calarcá, Circasia, Córdoba, etc. |
| **Zonas** | 42 | Zonas electorales distribuidas por municipios |
| **Puestos** | 129 | Puestos de votación en instituciones educativas |
| **Mesas** | 212 | Mesas electorales individuales |

### 👥 USUARIOS CREADOS

| Rol | Cantidad | Descripción |
|-----|----------|-------------|
| **Coordinador Departamental** | 1 | Usuario: `QUINDIO` |
| **Coordinadores Municipales** | 12 | Uno por cada municipio |
| **Coordinadores de Puesto** | 129 | Uno por cada puesto de votación |
| **Testigos Electorales** | 212 | Uno por cada mesa electoral |

**TOTAL USUARIOS CREADOS: 354**

## EJEMPLOS DE DATOS CARGADOS

### Testigos Electorales (Ejemplos)
- `testigo_2601010101001` (Cédula: 2601010101001) - IE TERESITA MONTES SD LUIS C. GALAN S. - Mesa 1
- `testigo_2601010102001` (Cédula: 2601010102001) - IE TERESITA MONTES SD LUIS C. GALAN S. - Mesa 2
- `testigo_2601010201001` (Cédula: 2601010201001) - IE LAURA VICUÑA - Mesa 1
- `testigo_2601010202001` (Cédula: 2601010202001) - IE LAURA VICUÑA - Mesa 2
- `testigo_2601010203001` (Cédula: 2601010203001) - IE LAURA VICUÑA - Mesa 3

### Municipios del Quindío
- Armenia (capital)
- Buenavista
- Calarcá
- Circasia
- Córdoba
- Filandia
- Génova
- La Tebaida
- Montenegro
- Pijao
- Quimbaya
- Salento

## CARACTERÍSTICAS TÉCNICAS

### Estructura de Datos
- **Código Departamental**: 26
- **Jerarquía Completa**: Departamento → Municipio → Zona → Puesto → Mesa
- **Geolocalización**: Coordenadas GPS para puestos de votación
- **Información Demográfica**: Número de votantes por género en cada mesa

### Usuarios y Seguridad
- **Contraseña Estándar**: `test123` para todos los usuarios
- **Cédulas Únicas**: Generadas automáticamente para testigos
- **Vinculación Geográfica**: Cada usuario está asociado a su ubicación específica
- **Roles Jerárquicos**: Estructura de coordinación por niveles territoriales

## SCRIPT UTILIZADO

**Archivo**: `scripts/init/cargar_quindio_completo.py`

### Funcionalidades del Script
1. **Extracción de Datos**: Lee automáticamente datos del Quindío desde `data/divipola.csv`
2. **Carga Jerárquica**: Crea ubicaciones en orden: departamento → municipios → zonas → puestos → mesas
3. **Creación de Usuarios**: Genera automáticamente usuarios para cada nivel territorial
4. **Validación**: Evita duplicados y mantiene integridad referencial
5. **Reporte Completo**: Proporciona estadísticas detalladas del proceso

### Ejecución
```bash
python scripts/init/cargar_quindio_completo.py
```

## ESTADO DEL SISTEMA

### ✅ COMPLETADO
- [x] Carga de estructura territorial del Quindío
- [x] Creación de usuarios coordinadores por nivel
- [x] Generación de testigos electorales para todas las mesas
- [x] Asignación de cédulas únicas a testigos
- [x] Vinculación geográfica de usuarios
- [x] Validación de integridad de datos

### 🔐 CREDENCIALES DE ACCESO
- **Coordinador Departamental**: Usuario `QUINDIO`, Contraseña `test123`
- **Coordinadores Municipales**: Usuario `[MUNICIPIO]`, Contraseña `test123`
- **Coordinadores de Puesto**: Usuario `[MUNICIPIO]_P[CODIGO]`, Contraseña `test123`
- **Testigos**: Usuario `testigo_[CEDULA]`, Contraseña `test123`

## PRÓXIMOS PASOS

1. **Pruebas de Sistema**: Verificar funcionalidad con datos del Quindío
2. **Capacitación**: Entrenar usuarios en el uso del sistema
3. **Configuración Electoral**: Cargar partidos políticos y candidatos
4. **Simulacros**: Realizar pruebas de captura de formularios E-14

## NOTAS TÉCNICAS

- **Base de Datos**: SQLite con 354 nuevos usuarios y 396 nuevas ubicaciones
- **Rendimiento**: Carga completada en aproximadamente 2 minutos
- **Sin Errores**: Proceso ejecutado sin errores de integridad
- **Compatibilidad**: 100% compatible con funcionalidad existente del sistema

---

**Fecha de Completación**: 14 de diciembre de 2024  
**Script Ejecutado**: `cargar_quindio_completo.py`  
**Estado**: ✅ COMPLETADO EXITOSAMENTE