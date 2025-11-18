# 📤 Guía de Carga Masiva - Super Admin Dashboard

## Descripción

El Super Admin Dashboard ahora incluye funcionalidades de carga masiva de datos desde archivos Excel, permitiendo configurar rápidamente todo el sistema electoral.

---

## 🎯 Funcionalidades Implementadas

### 1. Carga Masiva de Usuarios
- **Endpoint:** `POST /api/super-admin/upload/users`
- **Formato:** Excel (.xlsx, .xls)
- **Roles soportados:** testigo, coordinador_puesto, coordinador_municipal, coordinador_departamental, auditor, super_admin

### 2. Carga Masiva de DIVIPOLA (Ubicaciones)
- **Endpoint:** `POST /api/super-admin/upload/locations`
- **Formato:** Excel (.xlsx, .xls)
- **Tipos:** departamento, municipio, puesto, mesa

### 3. Carga Masiva de Partidos Políticos
- **Endpoint:** `POST /api/super-admin/upload/partidos`
- **Formato:** Excel (.xlsx, .xls)
- **Incluye:** nombre, sigla, color, número de lista

### 4. Carga Masiva de Candidatos
- **Endpoint:** `POST /api/super-admin/upload/candidatos`
- **Formato:** Excel (.xlsx, .xls)
- **Vincula:** candidato con partido y tipo de elección

---

## 📋 Formatos de Archivos Excel

### Usuarios (plantilla_usuarios.xlsx)

| nombre | password | rol | ubicacion_codigo |
|--------|----------|-----|------------------|
| Juan Perez | password123 | testigo | 001001001 |
| Maria Garcia | password456 | coordinador_puesto | 001001 |
| Carlos Lopez | password789 | coordinador_municipal | 001 |

**Columnas:**
- `nombre` (requerido): Nombre completo del usuario
- `password` (requerido): Contraseña inicial
- `rol` (requerido): Rol del usuario
- `ubicacion_codigo` (opcional): Código de la ubicación asignada

**Roles válidos:**
- `testigo`
- `coordinador_puesto`
- `coordinador_municipal`
- `coordinador_departamental`
- `auditor`
- `super_admin`

---

### DIVIPOLA - Ubicaciones (plantilla_divipola.xlsx)

| codigo | nombre | tipo | departamento_codigo | municipio_codigo | puesto_codigo |
|--------|--------|------|---------------------|------------------|---------------|
| 001 | Departamento 1 | departamento | | | |
| 001001 | Municipio 1 | municipio | 001 | | |
| 001001001 | Puesto 1 | puesto | 001 | 001001 | |
| 001001001001 | Mesa 1 | mesa | 001 | 001001 | 001001001 |

**Columnas:**
- `codigo` (requerido): Código único de la ubicación
- `nombre` (requerido): Nombre de la ubicación
- `tipo` (requerido): Tipo de ubicación
- `departamento_codigo` (opcional): Código del departamento padre
- `municipio_codigo` (opcional): Código del municipio padre
- `puesto_codigo` (opcional): Código del puesto padre

**Tipos válidos:**
- `departamento`
- `municipio`
- `puesto`
- `mesa`

**Importante:** Cargar en orden jerárquico (departamentos → municipios → puestos → mesas)

---

### Partidos Políticos (plantilla_partidos.xlsx)

| nombre | sigla | color | numero_lista |
|--------|-------|-------|--------------|
| Partido Liberal | PL | #FF0000 | 1 |
| Partido Conservador | PC | #0000FF | 2 |
| Partido Verde | PV | #00FF00 | 3 |

**Columnas:**
- `nombre` (requerido): Nombre completo del partido
- `sigla` (requerido): Sigla o abreviatura
- `color` (requerido): Color en formato hexadecimal (#RRGGBB)
- `numero_lista` (opcional): Número de lista electoral

---

### Candidatos (plantilla_candidatos.xlsx)

| nombre | partido_nombre | tipo_eleccion_nombre | numero_lista |
|--------|----------------|----------------------|--------------|
| Juan Perez | Partido Liberal | Presidente | 1 |
| Maria Garcia | Partido Conservador | Senado | 2 |
| Carlos Lopez | Partido Verde | Cámara | 3 |

**Columnas:**
- `nombre` (requerido): Nombre completo del candidato
- `partido_nombre` (requerido): Nombre del partido (debe existir previamente)
- `tipo_eleccion_nombre` (requerido): Tipo de elección (debe existir previamente)
- `numero_lista` (opcional): Número de lista del candidato

**Prerequisitos:**
- Los partidos deben estar creados antes de cargar candidatos
- Los tipos de elección deben estar creados antes de cargar candidatos

---

## 🚀 Cómo Usar

### Paso 1: Acceder al Super Admin Dashboard
1. Iniciar sesión como super_admin
2. Navegar a la sección "Configuración"
3. Localizar la sección "Carga Masiva de Datos"

### Paso 2: Descargar Plantillas
1. Hacer clic en el botón "Plantilla" de cada tipo de dato
2. Se descargará un archivo CSV con el formato correcto
3. Abrir el archivo en Excel
4. Completar con los datos reales
5. Guardar como archivo Excel (.xlsx)

### Paso 3: Cargar Datos
1. Hacer clic en el botón "Cargar" del tipo de dato correspondiente
2. Seleccionar el archivo Excel preparado
3. Esperar a que se procese el archivo
4. Revisar el resultado de la carga

### Paso 4: Verificar Resultados
El sistema mostrará:
- Total de registros procesados
- Total de registros creados exitosamente
- Total de errores encontrados
- Lista detallada de errores (si los hay)

---

## 📊 Orden Recomendado de Carga

Para configurar el sistema desde cero, seguir este orden:

1. **DIVIPOLA (Ubicaciones)**
   - Cargar departamentos
   - Cargar municipios
   - Cargar puestos
   - Cargar mesas

2. **Partidos Políticos**
   - Cargar todos los partidos

3. **Tipos de Elección**
   - Crear manualmente o cargar

4. **Candidatos**
   - Cargar candidatos (requiere partidos y tipos de elección)

5. **Usuarios**
   - Cargar testigos y coordinadores (requiere ubicaciones)

---

## ⚠️ Consideraciones Importantes

### Validaciones
- **Nombres únicos:** No se permiten duplicados en nombres de usuarios, partidos, etc.
- **Códigos únicos:** Los códigos de ubicación deben ser únicos
- **Referencias válidas:** Los códigos de ubicación padre deben existir
- **Formato de colores:** Deben estar en formato hexadecimal (#RRGGBB)

### Manejo de Errores
- Si un registro falla, los demás continúan procesándose
- Se muestra un reporte detallado de errores por fila
- Los registros exitosos se guardan en la base de datos
- Los registros con error se pueden corregir y volver a cargar

### Performance
- Archivos grandes (>1000 registros) pueden tardar varios segundos
- Se recomienda dividir archivos muy grandes en lotes
- El sistema procesa los registros secuencialmente

---

## 🔧 Requisitos Técnicos

### Backend
- Python 3.8+
- pandas==2.1.4
- openpyxl==3.1.2
- psutil==5.9.6

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Permisos
- Solo usuarios con rol `super_admin` pueden cargar datos masivamente
- Se requiere autenticación JWT válida

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Cargar 100 Testigos
1. Descargar plantilla de usuarios
2. Completar 100 filas con datos de testigos
3. Asignar rol "testigo" a todos
4. Asignar códigos de ubicación (mesas)
5. Cargar archivo
6. Verificar que los 100 usuarios fueron creados

### Ejemplo 2: Cargar DIVIPOLA Completa
1. Preparar archivo con estructura jerárquica:
   - 32 departamentos
   - 1,122 municipios
   - N puestos de votación
   - M mesas de votación
2. Ordenar por tipo (departamento → municipio → puesto → mesa)
3. Cargar archivo
4. Verificar jerarquía correcta

### Ejemplo 3: Cargar Candidatos de Múltiples Partidos
1. Asegurarse de que los partidos existen
2. Asegurarse de que los tipos de elección existen
3. Preparar archivo con candidatos
4. Vincular cada candidato con su partido y tipo de elección
5. Cargar archivo
6. Verificar que los candidatos aparecen en la configuración

---

## 🐛 Solución de Problemas

### Error: "Faltan columnas requeridas"
**Solución:** Verificar que el archivo Excel tiene todas las columnas requeridas con los nombres exactos.

### Error: "Usuario ya existe"
**Solución:** Verificar que no hay nombres duplicados en el archivo o en la base de datos.

### Error: "Ubicación no encontrada"
**Solución:** Verificar que el código de ubicación existe en la base de datos antes de asignar usuarios.

### Error: "Partido no encontrado"
**Solución:** Cargar los partidos antes de cargar los candidatos.

### Error: "El archivo debe ser Excel"
**Solución:** Guardar el archivo como .xlsx o .xls, no como .csv.

---

## 📈 Mejoras Futuras

- [ ] Validación previa del archivo antes de procesar
- [ ] Previsualización de datos antes de cargar
- [ ] Actualización masiva (no solo creación)
- [ ] Eliminación masiva con confirmación
- [ ] Exportación de datos existentes a Excel
- [ ] Plantillas con datos de ejemplo más completos
- [ ] Carga asíncrona con barra de progreso
- [ ] Notificaciones por email al completar carga
- [ ] Historial de cargas masivas
- [ ] Rollback de cargas erróneas

---

## 📞 Soporte

Para problemas o dudas sobre la carga masiva de datos:
1. Revisar esta guía completa
2. Verificar los logs del servidor
3. Contactar al equipo de desarrollo

---

**Última actualización:** 2025-11-14  
**Versión:** 1.0.0  
**Estado:** ✅ Funcional y probado
