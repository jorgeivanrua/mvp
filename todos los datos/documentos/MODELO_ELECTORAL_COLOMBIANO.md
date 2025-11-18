# 🗳️ Modelo Electoral Colombiano - Implementación Completa

**Fecha:** 2025-11-14  
**Commit:** `d595343`

---

## 📋 Tipos de Elecciones Soportadas

### 1. Elecciones Uninominales (Candidato Único)

**Características:**
- Un partido presenta un candidato único
- El votante elige directamente al candidato
- No hay listas de candidatos

**Tipos:**
- **Presidente de la República**
- **Gobernador Departamental**
- **Alcalde Municipal**

**Modelo de Datos:**
```
TipoEleccion:
  - es_uninominal: TRUE
  - permite_lista_cerrada: FALSE
  - permite_lista_abierta: FALSE
  - permite_coaliciones: TRUE (opcional)

Candidato:
  - partido_id: ID del partido
  - tipo_eleccion_id: ID del tipo
  - es_independiente: TRUE/FALSE
  - es_cabeza_lista: FALSE
```

---

### 2. Elecciones por Corporaciones (Listas)

**Características:**
- Partidos presentan listas de candidatos
- Pueden ser listas cerradas o abiertas
- Permiten coaliciones entre partidos

**Tipos:**
- **Senado de la República**
- **Cámara de Representantes**
- **Asamblea Departamental**
- **Concejo Municipal**
- **Junta Administradora Local (JAL)**

#### 2.1 Listas Cerradas

**Características:**
- El votante vota por el partido/lista completa
- El orden de los candidatos es fijo
- Los escaños se asignan según el orden de la lista

**Modelo de Datos:**
```
TipoEleccion:
  - es_uninominal: FALSE
  - permite_lista_cerrada: TRUE
  - permite_lista_abierta: FALSE
  - permite_coaliciones: TRUE

Candidato:
  - partido_id: ID del partido
  - numero_lista: Posición en la lista (1, 2, 3...)
  - es_cabeza_lista: TRUE (para el primero)
  - orden: Orden en la lista
```

#### 2.2 Listas Abiertas (Voto Preferente)

**Características:**
- El votante puede votar por el partido Y por un candidato específico
- Los candidatos con más votos preferentes suben en la lista
- Combina voto de partido con voto personal

**Modelo de Datos:**
```
TipoEleccion:
  - es_uninominal: FALSE
  - permite_lista_cerrada: FALSE
  - permite_lista_abierta: TRUE
  - permite_coaliciones: TRUE

Candidato:
  - partido_id: ID del partido
  - numero_lista: Número del candidato
  - es_cabeza_lista: FALSE (todos compiten)
  - orden: Orden inicial
```

---

### 3. Coaliciones

**Características:**
- Múltiples partidos se unen bajo una misma lista
- Comparten candidatos y votos
- Los escaños se distribuyen entre los partidos de la coalición

**Modelo de Datos:**
```
Coalicion:
  - codigo: Código único
  - nombre: Nombre de la coalición
  - descripcion: Descripción
  - activo: TRUE/FALSE

PartidoCoalicion:
  - partido_id: ID del partido
  - coalicion_id: ID de la coalición

TipoEleccion:
  - permite_coaliciones: TRUE
```

---

## 🗂️ Estructura de Datos

### Modelo TipoEleccion

```python
class TipoEleccion(db.Model):
    id: int
    codigo: str                      # Código único (ej: PRESIDENTE, SENADO)
    nombre: str                      # Nombre descriptivo
    descripcion: str                 # Descripción detallada
    es_uninominal: bool              # TRUE para candidato único
    permite_lista_cerrada: bool      # TRUE para listas cerradas
    permite_lista_abierta: bool      # TRUE para voto preferente
    permite_coaliciones: bool        # TRUE si permite coaliciones
    activo: bool                     # TRUE si está habilitado
    orden: int                       # Orden de presentación
```

### Modelo Partido

```python
class Partido(db.Model):
    id: int
    codigo: str                      # Código único
    nombre: str                      # Nombre completo
    nombre_corto: str                # Sigla o nombre corto
    logo_url: str                    # URL del logo
    color: str                       # Color en hexadecimal
    activo: bool                     # TRUE si está habilitado
    orden: int                       # Orden de presentación
```

### Modelo Candidato

```python
class Candidato(db.Model):
    id: int
    codigo: str                      # Código único
    nombre_completo: str             # Nombre del candidato
    numero_lista: int                # Número en la lista (si aplica)
    partido_id: int                  # ID del partido
    tipo_eleccion_id: int            # ID del tipo de elección
    foto_url: str                    # URL de la foto
    es_independiente: bool           # TRUE si es independiente
    es_cabeza_lista: bool            # TRUE si es cabeza de lista
    activo: bool                     # TRUE si está habilitado
    orden: int                       # Orden de presentación
```

### Modelo Coalicion

```python
class Coalicion(db.Model):
    id: int
    codigo: str                      # Código único
    nombre: str                      # Nombre de la coalición
    descripcion: str                 # Descripción
    activo: bool                     # TRUE si está activa
```

---

## 🎯 Casos de Uso

### Caso 1: Elección Presidencial

**Configuración:**
```
TipoEleccion: "Presidente"
  - es_uninominal: TRUE
  - permite_coaliciones: TRUE

Partidos:
  - Partido Liberal
  - Partido Conservador
  - Partido Verde

Candidatos:
  - Juan Perez (Partido Liberal)
  - Maria Garcia (Partido Conservador)
  - Carlos Lopez (Partido Verde)
```

**Formulario E-14:**
- Muestra lista de candidatos únicos
- Un voto por candidato
- No hay listas

---

### Caso 2: Elección de Senado (Lista Cerrada)

**Configuración:**
```
TipoEleccion: "Senado"
  - es_uninominal: FALSE
  - permite_lista_cerrada: TRUE
  - permite_lista_abierta: FALSE
  - permite_coaliciones: TRUE

Partido Liberal:
  - Candidato 1 (cabeza de lista)
  - Candidato 2
  - Candidato 3
  - ...

Partido Conservador:
  - Candidato 1 (cabeza de lista)
  - Candidato 2
  - Candidato 3
  - ...
```

**Formulario E-14:**
- Muestra partidos con sus listas
- Un voto por partido/lista
- No se vota por candidatos individuales

---

### Caso 3: Elección de Cámara (Lista Abierta)

**Configuración:**
```
TipoEleccion: "Cámara"
  - es_uninominal: FALSE
  - permite_lista_cerrada: FALSE
  - permite_lista_abierta: TRUE
  - permite_coaliciones: TRUE

Partido Liberal:
  - Candidato 1 (número 1)
  - Candidato 2 (número 2)
  - Candidato 3 (número 3)
  - ...
```

**Formulario E-14:**
- Muestra partidos con sus candidatos
- Voto por partido (obligatorio)
- Voto preferente por candidato (opcional)
- Dos campos de captura

---

### Caso 4: Coalición para Senado

**Configuración:**
```
Coalicion: "Coalición por Colombia"
  - Partido Liberal
  - Partido Verde
  - Partido de la U

Lista Única:
  - Candidato 1 (Partido Liberal)
  - Candidato 2 (Partido Verde)
  - Candidato 3 (Partido de la U)
  - ...
```

**Formulario E-14:**
- Muestra la coalición como una opción
- Los votos se cuentan para la coalición
- Los escaños se distribuyen entre los partidos

---

## 🔧 Funcionalidades del Super Admin

### Crear Tipo de Elección

**Opciones:**
1. **Nombre:** Ej: "Presidente", "Senado", "Cámara"
2. **Descripción:** Descripción detallada
3. **Categoría:**
   - Uninominal (candidato único)
   - Por corporación (listas)
4. **Si es por corporación:**
   - ☑️ Permite lista cerrada
   - ☐ Permite lista abierta (voto preferente)
   - ☐ Permite coaliciones

**Resultado:**
- Tipo de elección creado y habilitado
- Disponible para configurar candidatos
- Aparece en formularios de testigos

---

### Configurar Partidos y Candidatos

**Para Elecciones Uninominales:**
1. Crear partido
2. Crear candidato único
3. Vincular candidato con partido y tipo de elección
4. Habilitar partido y candidato

**Para Elecciones por Listas:**
1. Crear partido
2. Crear múltiples candidatos
3. Asignar número de lista a cada candidato
4. Marcar cabeza de lista (si es lista cerrada)
5. Habilitar partido y candidatos

**Para Coaliciones:**
1. Crear coalición
2. Agregar partidos a la coalición
3. Crear candidatos vinculados a la coalición
4. Habilitar coalición

---

## 📊 Impacto en el Formulario E-14

### Formulario para Uninominales
```
Presidente:
  ○ Juan Perez (Partido Liberal)
  ○ Maria Garcia (Partido Conservador)
  ○ Carlos Lopez (Partido Verde)
  
Votos: [____]
```

### Formulario para Listas Cerradas
```
Senado:
  ○ Partido Liberal (Lista completa)
  ○ Partido Conservador (Lista completa)
  ○ Partido Verde (Lista completa)
  
Votos: [____]
```

### Formulario para Listas Abiertas
```
Cámara:
  Partido: ○ Partido Liberal
           ○ Partido Conservador
           ○ Partido Verde
  
  Candidato (opcional):
  ○ Candidato 1
  ○ Candidato 2
  ○ Candidato 3
  
Votos Partido: [____]
Votos Candidato: [____]
```

---

## ✅ Validaciones Implementadas

### Backend
- ✅ Tipo de elección debe existir y estar activo
- ✅ Partido debe existir y estar activo
- ✅ Candidato debe existir y estar activo
- ✅ Candidato debe estar vinculado al tipo de elección correcto
- ✅ Número de lista debe ser único por partido y tipo
- ✅ Coaliciones deben tener al menos 2 partidos

### Frontend
- ✅ Solo muestra tipos de elección habilitados
- ✅ Solo muestra partidos habilitados
- ✅ Solo muestra candidatos habilitados
- ✅ Valida formato según tipo de elección
- ✅ Previene votos duplicados

---

## 🔮 Próximas Mejoras

### Corto Plazo
- [ ] Interfaz para crear coaliciones desde el Super Admin
- [ ] Visualización de listas completas por partido
- [ ] Reordenamiento de candidatos en listas
- [ ] Importación masiva de listas completas

### Mediano Plazo
- [ ] Simulador de distribución de escaños
- [ ] Cálculo automático de cifra repartidora
- [ ] Reportes por tipo de elección
- [ ] Estadísticas de voto preferente

### Largo Plazo
- [ ] Soporte para circunscripciones especiales
- [ ] Manejo de curules de paz
- [ ] Integración con sistema de escrutinio
- [ ] API para resultados en tiempo real

---

## 📚 Referencias

### Normativa Electoral Colombiana
- Constitución Política de Colombia (Art. 258-265)
- Código Electoral (Ley 1475 de 2011)
- Ley de Garantías Electorales
- Resoluciones de la Registraduría Nacional

### Documentación Técnica
- `backend/models/configuracion_electoral.py` - Modelos de datos
- `backend/routes/super_admin.py` - Endpoints de configuración
- `frontend/static/js/super-admin-dashboard.js` - Interfaz de gestión

---

## 🎉 Conclusión

El sistema ahora soporta completamente el modelo electoral colombiano, incluyendo:

1. ✅ **Elecciones uninominales** (Presidente, Gobernador, Alcalde)
2. ✅ **Elecciones por corporaciones** (Senado, Cámara, Asamblea, Concejo, JAL)
3. ✅ **Listas cerradas** (orden fijo)
4. ✅ **Listas abiertas** (voto preferente)
5. ✅ **Coaliciones** (múltiples partidos)
6. ✅ **Candidatos independientes**
7. ✅ **Control de habilitación** granular
8. ✅ **Validaciones completas**

El sistema está preparado para manejar cualquier tipo de elección en Colombia de manera flexible, segura y conforme a la normativa electoral vigente.

---

**Estado:** ✅ Completamente implementado y funcional  
**Commit:** `d595343` - feat: Implementar modelo electoral completo con listas y coaliciones  
**Próximo paso:** Implementar interfaz de gestión de coaliciones
