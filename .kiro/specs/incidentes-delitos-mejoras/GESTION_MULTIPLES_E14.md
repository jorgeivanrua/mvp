# Gestión de Múltiples Formularios E-14

## 📋 Concepto Fundamental

### Una Mesa, Múltiples Elecciones

En el sistema electoral, **una misma mesa de votación** puede tener **múltiples tipos de elecciones** simultáneas:

- 🗳️ **Elección Presidencial**
- 🗳️ **Diputados Nacionales**
- 🗳️ **Senadores**
- 🗳️ **Alcalde**
- 🗳️ **Concejales**
- 🗳️ **Otras elecciones locales**

### Un E-14 por Tipo de Elección

**Cada tipo de elección requiere su propio formulario E-14**, por lo tanto:

```
Mesa 001-A puede tener:
├── E-14 para Presidente
├── E-14 para Diputados
├── E-14 para Alcalde
└── E-14 para Concejales
```

## 🔍 Identificación Única

### Estructura del Identificador

Cada formulario E-14 se identifica de forma única mediante:

```
Identificador = mesa_id + tipo_eleccion_id + timestamp
```

**Ejemplo**:
```
E14_M123_T1_1701234567890
│   │    │  └─ Timestamp (momento de creación)
│   │    └─ Tipo de elección ID (1 = Presidente)
│   └─ Mesa ID (123)
└─ Tipo de formulario (E14)
```

### Metadatos Almacenados

Cada formulario E-14 offline incluye:

```javascript
{
    tipo: 'formulario_e14',
    mesa_id: 123,
    mesa_codigo: '001-A',
    mesa_display: 'Mesa 001-A',
    tipo_eleccion_id: 1,
    tipo_eleccion_nombre: 'Elección Presidencial',
    tipo_eleccion_display: 'Presidente',
    identificador_unico: 'E14_M123_T1_1701234567890',
    // ... datos del formulario
}
```

## 📸 Gestión de Fotos Múltiples

### Múltiples Páginas por Acta

Un acta E-14 puede tener **varias páginas**, por lo tanto se pueden tomar **múltiples fotos**:

```
Acta E-14 - Mesa 001-A - Presidente
├── Página 1/3 (Votos por partido)
├── Página 2/3 (Votos por candidato)
└── Página 3/3 (Firmas y observaciones)
```

### Metadatos de Cada Foto

Cada foto incluye información completa:

```javascript
{
    file_data: "data:image/jpeg;base64,...",
    filename: "acta_001A_presidente_pag1.jpg",
    mime_type: "image/jpeg",
    tipo_reporte: "formulario_e14",
    
    // Identificación
    mesa_id: 123,
    mesa_codigo: "001-A",
    tipo_eleccion_id: 1,
    tipo_eleccion_nombre: "Elección Presidencial",
    
    // Paginación
    numero_pagina: 1,
    total_paginas: 3,
    
    // Descripción completa
    descripcion: "Acta E-14 - Mesa 001-A - Elección Presidencial - Página 1/3",
    
    fecha_captura: "2024-12-01T15:30:00.000Z"
}
```

## 👁️ Visualización para Usuarios

### Panel de Reportes Pendientes

Los coordinadores verán cada E-14 claramente identificado:

```
┌─────────────────────────────────────┐
│ 📄 E-14: Mesa 001-A                │
│    Elección Presidencial            │
│    🕐 hace 5 minutos                │
│    📸 3 fotos                       │
│    [Sincronizando...]               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 📄 E-14: Mesa 001-A                │
│    Diputados Nacionales             │
│    🕐 hace 3 minutos                │
│    📸 2 fotos                       │
│    [Sincronizando...]               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 📄 E-14: Mesa 001-A                │
│    Alcalde Municipal                │
│    🕐 hace 1 minuto                 │
│    📸 1 foto                        │
│    [Sincronizando...]               │
└─────────────────────────────────────┘
```

### Lista de Formularios Sincronizados

En el dashboard, los formularios se agrupan por mesa:

```
Mesa 001-A
├── ✅ E-14 Presidente (3 fotos) - Sincronizado
├── ✅ E-14 Diputados (2 fotos) - Sincronizado
├── ⏳ E-14 Alcalde (1 foto) - Pendiente
└── ❌ E-14 Concejales - Sin reportar
```

## 🔄 Flujo de Trabajo

### Para Testigos

1. **Completar E-14 por cada tipo de elección**
   ```
   Paso 1: Seleccionar mesa → 001-A
   Paso 2: Seleccionar tipo → Presidente
   Paso 3: Ingresar votos
   Paso 4: Tomar fotos (todas las páginas)
   Paso 5: Enviar
   
   Repetir para cada tipo de elección
   ```

2. **Tomar todas las fotos necesarias**
   - Foto 1: Primera página del acta
   - Foto 2: Segunda página del acta
   - Foto 3: Tercera página del acta
   - etc.

3. **El sistema identifica automáticamente**
   - Mesa específica
   - Tipo de elección específico
   - Número de página
   - Total de páginas

### Para Coordinadores

1. **Revisar reportes pendientes**
   - Ver claramente mesa + tipo de elección
   - Verificar número de fotos
   - Confirmar que no faltan E-14

2. **Validar completitud**
   ```
   Mesa 001-A:
   ✅ Presidente - OK
   ✅ Diputados - OK
   ❌ Alcalde - FALTA
   ```

3. **Sincronizar cuando hay conexión**
   - Automático al recuperar señal
   - Manual con botón "Sincronizar"

## 🎯 Casos de Uso

### Caso 1: Testigo en Zona Rural

**Situación**: Mesa 001-A, sin señal, 4 tipos de elecciones

**Proceso**:
1. Completa E-14 Presidente → Guarda offline
2. Completa E-14 Diputados → Guarda offline
3. Completa E-14 Alcalde → Guarda offline
4. Completa E-14 Concejales → Guarda offline
5. Sale de la zona rural
6. Sistema sincroniza automáticamente los 4 E-14

**Resultado**: 4 formularios E-14 sincronizados correctamente, cada uno identificado por mesa + tipo de elección.

### Caso 2: Acta con Múltiples Páginas

**Situación**: Acta E-14 de Presidente tiene 3 páginas

**Proceso**:
1. Completa formulario E-14 Presidente
2. Toma foto página 1 → Sistema marca "1/3"
3. Toma foto página 2 → Sistema marca "2/3"
4. Toma foto página 3 → Sistema marca "3/3"
5. Envía formulario

**Resultado**: 1 formulario E-14 con 3 fotos, cada una identificada con su número de página.

### Caso 3: Coordinador Revisando

**Situación**: Coordinador debe verificar que todas las mesas reportaron

**Vista**:
```
Mesa 001-A
├── ✅ Presidente (3 fotos)
├── ✅ Diputados (2 fotos)
├── ✅ Alcalde (1 foto)
└── ✅ Concejales (2 fotos)

Mesa 002-B
├── ✅ Presidente (2 fotos)
├── ⏳ Diputados (pendiente)
├── ❌ Alcalde (sin reportar)
└── ✅ Concejales (1 foto)
```

**Acción**: Contactar testigo de Mesa 002-B para E-14 de Alcalde.

## 🔒 Prevención de Errores

### Validaciones Implementadas

1. **No duplicar E-14**
   - Sistema verifica mesa + tipo de elección
   - Alerta si ya existe un E-14 para esa combinación
   - Permite editar en lugar de duplicar

2. **Identificación clara**
   - Cada E-14 muestra mesa Y tipo de elección
   - Imposible confundir entre diferentes elecciones
   - Metadatos completos en cada foto

3. **Trazabilidad completa**
   - Timestamp de creación
   - Usuario que reportó
   - Número de fotos
   - Estado de sincronización

## 📊 Estadísticas

El sistema proporciona estadísticas detalladas:

```javascript
{
    total_e14: 120,
    por_tipo_eleccion: {
        presidente: 30,
        diputados: 30,
        alcalde: 30,
        concejales: 30
    },
    por_estado: {
        sincronizados: 100,
        pendientes: 15,
        errores: 5
    },
    fotos_totales: 250,
    promedio_fotos_por_e14: 2.08
}
```

## 🚀 Beneficios

1. **Claridad**: Cada E-14 claramente identificado
2. **Completitud**: Fácil verificar que no faltan E-14
3. **Trazabilidad**: Saber exactamente qué se reportó
4. **Flexibilidad**: Múltiples fotos por acta
5. **Confiabilidad**: Sincronización automática
6. **Organización**: Agrupación por mesa y tipo

## 📝 Notas Técnicas

### Almacenamiento

- Cada E-14 se almacena independientemente
- Las fotos se comprimen automáticamente
- Metadatos completos en cada registro
- Limpieza automática después de sincronizar

### Sincronización

- Orden: Por timestamp de creación
- Prioridad: E-14 antes que incidentes/delitos
- Retry: Hasta 3 intentos por formulario
- Evidencia: Se sincroniza después del formulario

### Rendimiento

- Compresión de imágenes: ~70% reducción
- Almacenamiento típico: 2-3 MB por E-14 con fotos
- Tiempo de sincronización: ~5-10 segundos por E-14
- Capacidad offline: 100-200 E-14 con fotos

## ✅ Checklist de Implementación

- [x] Identificador único por mesa + tipo de elección
- [x] Metadatos completos en cada E-14
- [x] Soporte para múltiples fotos por acta
- [x] Numeración de páginas en fotos
- [x] Visualización clara en panel de pendientes
- [x] Agrupación por mesa en dashboard
- [x] Validación de duplicados
- [x] Sincronización independiente por E-14
- [x] Estadísticas detalladas
- [x] Documentación completa

---

**Fecha**: Diciembre 2024  
**Versión**: 1.0  
**Estado**: ✅ Implementado y documentado
