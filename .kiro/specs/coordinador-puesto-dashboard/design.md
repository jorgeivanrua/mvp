# Design Document - Dashboard Coordinador de Puesto

## Overview

El Dashboard del Coordinador de Puesto es una aplicación web que permite supervisar, validar y consolidar los formularios E-14 de todas las mesas de un puesto de votación. El sistema se construye sobre la arquitectura existente del sistema electoral, reutilizando componentes del dashboard del testigo y extendiendo la funcionalidad para incluir capacidades de validación y consolidación.

El coordinador de puesto actúa como el primer nivel de validación de datos, revisando los formularios enviados por los testigos antes de que sean consolidados a nivel municipal. El sistema debe ser eficiente, intuitivo y funcionar correctamente en dispositivos móviles.

## Architecture

### Frontend Architecture

```
frontend/
├── templates/
│   └── coordinador/
│       └── puesto.html              # Dashboard principal del coordinador
├── static/
│   ├── js/
│   │   ├── coordinador-puesto.js    # Lógica del dashboard
│   │   └── api-client.js            # Cliente API (reutilizado)
│   └── css/
│       └── coordinador.css          # Estilos específicos
```

### Backend Architecture

```
backend/
├── routes/
│   ├── formularios.py               # Rutas para gestión de formularios E-14
│   └── frontend.py                  # Ruta ya existe: /coordinador/puesto
├── services/
│   ├── formulario_service.py        # Lógica de negocio de formularios
│   └── validacion_service.py        # Validaciones y consolidación
└── models/
    ├── formulario_e14.py            # Modelo del formulario E-14
    ├── voto_partido.py              # Votos por partido
    ├── voto_candidato.py            # Votos por candidato
    └── historial_formulario.py      # Auditoría de cambios
```

### Data Flow

```
Testigo → Formulario E-14 (pendiente) → Coordinador Puesto → Validación/Rechazo
                                                            ↓
                                                    Formulario (validado)
                                                            ↓
                                                    Consolidado Puesto
                                                            ↓
                                                Coordinador Municipal
```

## Components and Interfaces

### 1. Dashboard Principal (puesto.html)

**Componentes:**

- **Header con información del puesto**
  - Nombre del puesto
  - Código del puesto
  - Total de mesas asignadas
  - Progreso de recolección (X/Y mesas reportadas)

- **Panel de Estadísticas**
  - Total de formularios pendientes (badge con número)
  - Total de formularios validados
  - Total de formularios rechazados
  - Porcentaje de avance

- **Tabla de Formularios**
  - Columnas: Mesa, Testigo, Estado, Total Votos, Fecha Envío, Acciones
  - Filtros: Todos, Pendiente, Validado, Rechazado
  - Ordenamiento por fecha, mesa, estado
  - Paginación (20 formularios por página)
  - Auto-refresh cada 30 segundos

- **Panel de Consolidado**
  - Gráfico de barras con votos por partido
  - Tabla resumen con totales
  - Solo incluye formularios validados
  - Botón para generar reporte PDF

- **Lista de Mesas**
  - Vista de todas las mesas del puesto
  - Indicador visual de estado (reportada/pendiente)
  - Información del testigo asignado

### 2. Modal de Validación de Formulario

**Componentes:**

- **Vista dividida (split view)**
  - Lado izquierdo: Imagen del formulario E-14 físico
    - Zoom in/out
    - Rotación de imagen
  - Lado derecho: Datos digitados
    - Información de la mesa
    - Datos de votación
    - Votos por partido y candidato

- **Panel de Validaciones Automáticas**
  - ✓ Total votos válidos = suma de votos por partido
  - ✓ Total votos = votos válidos + nulos + blancos
  - ✓ Total tarjetas = total votos + no marcadas
  - ⚠️ Alertas si hay discrepancias > 5%

- **Modo de Edición**
  - Campos editables para correcciones menores
  - Recálculo automático de totales
  - Registro de cambios en historial

- **Acciones**
  - Botón "Validar" (verde) - Aprueba el formulario
  - Botón "Rechazar" (rojo) - Requiere motivo
  - Botón "Editar y Validar" (amarillo) - Corrige y aprueba
  - Botón "Cerrar" - Sin cambios

### 3. Modal de Rechazo

**Componentes:**

- Campo de texto obligatorio para motivo de rechazo
- Sugerencias de motivos comunes:
  - "Imagen borrosa o ilegible"
  - "Totales no coinciden"
  - "Datos incompletos"
  - "Formulario duplicado"
- Botón "Confirmar Rechazo"
- Botón "Cancelar"

### 4. Panel de Consolidado

**Componentes:**

- **Resumen General**
  - Total de mesas validadas
  - Total de votos consolidados
  - Participación electoral (%)
  - Votos nulos y en blanco

- **Gráfico de Resultados**
  - Gráfico de barras horizontal
  - Colores por partido
  - Porcentajes y números absolutos

- **Tabla Detallada**
  - Partido, Votos, Porcentaje
  - Ordenado de mayor a menor
  - Exportable a CSV

- **Generación de Reporte**
  - Botón "Generar Reporte PDF"
  - Incluye firma digital del coordinador
  - Timestamp de generación

## Data Models

### FormularioE14

```python
class FormularioE14(db.Model):
    __tablename__ = 'formularios_e14'
    
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    testigo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo_eleccion_id = db.Column(db.Integer, db.ForeignKey('tipos_eleccion.id'), nullable=False)
    
    # Datos de votación
    total_votantes_registrados = db.Column(db.Integer, nullable=False)
    total_votos = db.Column(db.Integer, nullable=False)
    votos_validos = db.Column(db.Integer, nullable=False)
    votos_nulos = db.Column(db.Integer, nullable=False)
    votos_blanco = db.Column(db.Integer, nullable=False)
    tarjetas_no_marcadas = db.Column(db.Integer, nullable=False)
    total_tarjetas = db.Column(db.Integer, nullable=False)
    
    # Estado y validación
    estado = db.Column(db.String(20), nullable=False, default='borrador')
    # Estados: borrador, pendiente, validado, rechazado
    
    validado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    validado_at = db.Column(db.DateTime)
    motivo_rechazo = db.Column(db.Text)
    
    # Imagen del formulario
    imagen_url = db.Column(db.String(500))
    imagen_hash = db.Column(db.String(64))  # SHA-256 para integridad
    
    # Observaciones
    observaciones = db.Column(db.Text)
    
    # Auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    mesa = db.relationship('Location', foreign_keys=[mesa_id])
    testigo = db.relationship('User', foreign_keys=[testigo_id])
    validado_por = db.relationship('User', foreign_keys=[validado_por_id])
    tipo_eleccion = db.relationship('TipoEleccion')
    votos_partidos = db.relationship('VotoPartido', back_populates='formulario', cascade='all, delete-orphan')
    votos_candidatos = db.relationship('VotoCandidato', back_populates='formulario', cascade='all, delete-orphan')
    historial = db.relationship('HistorialFormulario', back_populates='formulario', cascade='all, delete-orphan')
```

### VotoPartido

```python
class VotoPartido(db.Model):
    __tablename__ = 'votos_partidos'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    formulario = db.relationship('FormularioE14', back_populates='votos_partidos')
    partido = db.relationship('Partido')
```

### VotoCandidato

```python
class VotoCandidato(db.Model):
    __tablename__ = 'votos_candidatos'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidatos.id'), nullable=False)
    votos = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    formulario = db.relationship('FormularioE14', back_populates='votos_candidatos')
    candidato = db.relationship('Candidato')
```

### HistorialFormulario

```python
class HistorialFormulario(db.Model):
    __tablename__ = 'historial_formularios'
    
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios_e14.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accion = db.Column(db.String(50), nullable=False)
    # Acciones: creado, enviado, validado, rechazado, editado
    
    estado_anterior = db.Column(db.String(20))
    estado_nuevo = db.Column(db.String(20))
    cambios = db.Column(db.JSON)  # Detalles de cambios realizados
    comentario = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    formulario = db.relationship('FormularioE14', back_populates='historial')
    usuario = db.relationship('User')
```

## API Endpoints

### GET /api/formularios/puesto

Obtener todos los formularios del puesto del coordinador.

**Query Parameters:**
- `estado` (opcional): filtrar por estado
- `page` (opcional): número de página
- `per_page` (opcional): resultados por página

**Response:**
```json
{
  "success": true,
  "data": {
    "formularios": [
      {
        "id": 1,
        "mesa_codigo": "001",
        "mesa_nombre": "Mesa 001 - Escuela Central",
        "testigo_nombre": "Juan Pérez",
        "testigo_id": 5,
        "estado": "pendiente",
        "total_votos": 250,
        "created_at": "2025-11-12T10:30:00",
        "updated_at": "2025-11-12T10:30:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 45,
      "pages": 3
    },
    "estadisticas": {
      "total": 45,
      "pendientes": 12,
      "validados": 30,
      "rechazados": 3,
      "mesas_reportadas": 45,
      "total_mesas": 50
    }
  }
}
```

### GET /api/formularios/:id

Obtener detalles completos de un formulario.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "mesa": {
      "id": 10,
      "codigo": "001",
      "nombre": "Mesa 001 - Escuela Central",
      "total_votantes_registrados": 300
    },
    "testigo": {
      "id": 5,
      "nombre": "Juan Pérez"
    },
    "tipo_eleccion": {
      "id": 1,
      "nombre": "Alcaldía",
      "es_uninominal": true
    },
    "total_votantes_registrados": 300,
    "total_votos": 250,
    "votos_validos": 240,
    "votos_nulos": 5,
    "votos_blanco": 5,
    "tarjetas_no_marcadas": 50,
    "total_tarjetas": 300,
    "estado": "pendiente",
    "imagen_url": "/uploads/formularios/e14_001.jpg",
    "observaciones": "Proceso normal",
    "votos_partidos": [
      {
        "partido_id": 1,
        "partido_nombre": "Partido A",
        "partido_color": "#FF0000",
        "votos": 100
      }
    ],
    "votos_candidatos": [
      {
        "candidato_id": 1,
        "candidato_nombre": "María García",
        "partido_id": 1,
        "votos": 100
      }
    ],
    "validaciones": {
      "suma_votos_partidos": 240,
      "coincide_votos_validos": true,
      "coincide_total_votos": true,
      "coincide_total_tarjetas": true,
      "discrepancia_porcentaje": 0
    },
    "historial": [
      {
        "id": 1,
        "usuario_nombre": "Juan Pérez",
        "accion": "creado",
        "created_at": "2025-11-12T10:00:00"
      },
      {
        "id": 2,
        "usuario_nombre": "Juan Pérez",
        "accion": "enviado",
        "estado_anterior": "borrador",
        "estado_nuevo": "pendiente",
        "created_at": "2025-11-12T10:30:00"
      }
    ],
    "created_at": "2025-11-12T10:00:00",
    "updated_at": "2025-11-12T10:30:00"
  }
}
```

### PUT /api/formularios/:id/validar

Validar un formulario (cambiar estado a validado).

**Body:**
```json
{
  "cambios": {
    "votos_nulos": 6,
    "votos_partidos": [
      {
        "partido_id": 1,
        "votos": 101
      }
    ]
  },
  "comentario": "Corrección menor en votos nulos"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Formulario validado exitosamente",
  "data": {
    "id": 1,
    "estado": "validado",
    "validado_por_id": 3,
    "validado_at": "2025-11-12T11:00:00"
  }
}
```

### PUT /api/formularios/:id/rechazar

Rechazar un formulario.

**Body:**
```json
{
  "motivo": "Imagen borrosa, no se pueden leer los números claramente"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Formulario rechazado",
  "data": {
    "id": 1,
    "estado": "rechazado",
    "motivo_rechazo": "Imagen borrosa, no se pueden leer los números claramente"
  }
}
```

### GET /api/formularios/consolidado

Obtener datos consolidados del puesto.

**Response:**
```json
{
  "success": true,
  "data": {
    "puesto": {
      "codigo": "P001",
      "nombre": "Escuela Central",
      "total_mesas": 50,
      "mesas_validadas": 45
    },
    "resumen": {
      "total_votantes_registrados": 15000,
      "total_votos": 12500,
      "votos_validos": 12000,
      "votos_nulos": 250,
      "votos_blanco": 250,
      "participacion_porcentaje": 83.33
    },
    "votos_por_partido": [
      {
        "partido_id": 1,
        "partido_nombre": "Partido A",
        "partido_color": "#FF0000",
        "total_votos": 5000,
        "porcentaje": 41.67
      },
      {
        "partido_id": 2,
        "partido_nombre": "Partido B",
        "partido_color": "#0000FF",
        "total_votos": 4500,
        "porcentaje": 37.50
      }
    ]
  }
}
```

### GET /api/formularios/mesas

Obtener lista de mesas del puesto con estado de reporte.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "mesa_id": 10,
      "mesa_codigo": "001",
      "mesa_nombre": "Mesa 001 - Escuela Central",
      "testigo_id": 5,
      "testigo_nombre": "Juan Pérez",
      "testigo_telefono": "3001234567",
      "tiene_formulario": true,
      "estado_formulario": "validado",
      "ultima_actualizacion": "2025-11-12T10:30:00"
    },
    {
      "mesa_id": 11,
      "mesa_codigo": "002",
      "mesa_nombre": "Mesa 002 - Escuela Central",
      "testigo_id": 6,
      "testigo_nombre": "María López",
      "testigo_telefono": "3007654321",
      "tiene_formulario": false,
      "estado_formulario": null,
      "ultima_actualizacion": null
    }
  ]
}
```

### POST /api/formularios/reporte-pdf

Generar reporte PDF consolidado del puesto.

**Response:**
```json
{
  "success": true,
  "data": {
    "url": "/downloads/reportes/puesto_P001_20251112.pdf",
    "filename": "puesto_P001_20251112.pdf",
    "generated_at": "2025-11-12T12:00:00"
  }
}
```

## Error Handling

### Validación de Permisos

- Solo coordinadores de puesto pueden acceder al dashboard
- Solo pueden ver/validar formularios de su puesto asignado
- Retornar 403 Forbidden si intentan acceder a formularios de otro puesto

### Validación de Estados

- Solo formularios en estado "pendiente" pueden ser validados o rechazados
- Formularios "validados" no pueden ser editados (solo visualizados)
- Formularios "rechazados" vuelven a estado "borrador" para el testigo

### Validación de Datos

- Verificar que los totales sean coherentes antes de validar
- Alertar si hay discrepancias > 5% entre imagen y datos
- Validar que el motivo de rechazo no esté vacío

### Manejo de Errores

```javascript
try {
  const response = await APIClient.validarFormulario(id, data);
  Utils.showSuccess('Formulario validado exitosamente');
  loadForms();
} catch (error) {
  if (error.status === 403) {
    Utils.showError('No tiene permisos para validar este formulario');
  } else if (error.status === 400) {
    Utils.showError('Datos inválidos: ' + error.message);
  } else {
    Utils.showError('Error al validar formulario');
  }
}
```

## Testing Strategy

### Unit Tests

1. **Servicios de Validación**
   - Validar cálculos de totales
   - Validar coherencia de datos
   - Validar cambios de estado

2. **Modelos**
   - Crear formulario con votos
   - Actualizar estado de formulario
   - Registrar historial de cambios

### Integration Tests

1. **API Endpoints**
   - GET /api/formularios/puesto con diferentes filtros
   - PUT /api/formularios/:id/validar con y sin cambios
   - PUT /api/formularios/:id/rechazar con motivo
   - GET /api/formularios/consolidado

2. **Permisos y Seguridad**
   - Verificar que solo coordinadores de puesto pueden acceder
   - Verificar que solo ven formularios de su puesto
   - Verificar que no pueden validar formularios de otros puestos

### Frontend Tests

1. **Componentes**
   - Renderizado de tabla de formularios
   - Filtrado y ordenamiento
   - Modal de validación
   - Panel de consolidado

2. **Interacciones**
   - Validar formulario
   - Rechazar formulario
   - Editar y validar formulario
   - Generar reporte PDF

### Manual Testing

1. **Flujo Completo**
   - Login como coordinador de puesto
   - Ver lista de formularios pendientes
   - Abrir formulario para validación
   - Comparar imagen con datos
   - Validar o rechazar formulario
   - Ver consolidado actualizado
   - Generar reporte PDF

2. **Responsive Design**
   - Probar en móvil (< 768px)
   - Probar en tablet (768px - 1024px)
   - Probar en desktop (> 1024px)
   - Verificar zoom de imágenes en móvil

3. **Performance**
   - Cargar 50+ formularios
   - Auto-refresh cada 30 segundos
   - Generar consolidado con 50 mesas
   - Generar PDF con datos completos

## Security Considerations

1. **Autenticación y Autorización**
   - JWT tokens con expiración de 1 hora
   - Refresh tokens con expiración de 7 días
   - Verificar rol y ubicación en cada request

2. **Integridad de Datos**
   - Hash SHA-256 de imágenes de formularios
   - Registro completo de auditoría en historial
   - No permitir eliminar formularios validados

3. **Validación de Entrada**
   - Sanitizar todos los inputs del usuario
   - Validar rangos numéricos (votos >= 0)
   - Validar que motivo de rechazo no esté vacío

4. **Rate Limiting**
   - Limitar requests de validación a 10 por minuto
   - Limitar generación de PDFs a 5 por hora
   - Proteger contra ataques de fuerza bruta

## Performance Optimization

1. **Frontend**
   - Lazy loading de imágenes de formularios
   - Paginación de tabla de formularios
   - Debounce en filtros y búsqueda
   - Cache de datos de consolidado (5 minutos)

2. **Backend**
   - Índices en columnas: mesa_id, estado, created_at
   - Query optimization con eager loading
   - Cache de consolidados con Redis (opcional)
   - Compresión de imágenes al subir

3. **Database**
   - Índice compuesto: (mesa_id, estado)
   - Índice en: validado_por_id, validado_at
   - Particionamiento por fecha (opcional para gran volumen)

## Deployment Considerations

1. **Environment Variables**
   - `UPLOAD_FOLDER`: Directorio para imágenes de formularios
   - `MAX_UPLOAD_SIZE`: Tamaño máximo de imagen (5MB)
   - `PDF_TEMPLATE_PATH`: Ruta a plantilla de reporte PDF

2. **File Storage**
   - Usar almacenamiento persistente para imágenes
   - Considerar S3 o similar para producción
   - Backup diario de imágenes de formularios

3. **Monitoring**
   - Log de todas las validaciones y rechazos
   - Alertas si tasa de rechazo > 20%
   - Monitoreo de tiempo de respuesta de APIs
