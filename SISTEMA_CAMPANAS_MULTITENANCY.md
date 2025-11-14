# 🎯 Sistema de Campañas y Multi-Tenancy

**Fecha:** 2025-11-14  
**Commit:** `8965fe5`

---

## 📋 Descripción General

El sistema ahora soporta **múltiples campañas electorales independientes** en la misma base de datos, permitiendo:

1. **Campañas separadas** para diferentes elecciones
2. **Reset de datos** sin afectar la estructura
3. **Temas personalizados** por campaña, rol o tipo de elección
4. **Una campaña activa** a la vez
5. **Datos aislados** entre campañas

---

## 🗂️ Modelo de Datos

### Tabla: campanas

```sql
CREATE TABLE campanas (
    id INTEGER PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    color_primario VARCHAR(7) DEFAULT '#1e3c72',
    color_secundario VARCHAR(7) DEFAULT '#2a5298',
    logo_url VARCHAR(500),
    es_candidato_unico BOOLEAN DEFAULT FALSE,
    es_partido_completo BOOLEAN DEFAULT FALSE,
    activa BOOLEAN DEFAULT FALSE,
    completada BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    created_by INTEGER REFERENCES users(id)
);
```

### Tabla: configuracion_temas

```sql
CREATE TABLE configuracion_temas (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    aplica_a_rol VARCHAR(50),
    aplica_a_tipo_eleccion_id INTEGER REFERENCES tipos_eleccion(id),
    campana_id INTEGER REFERENCES campanas(id),
    color_primario VARCHAR(7) DEFAULT '#1e3c72',
    color_secundario VARCHAR(7) DEFAULT '#2a5298',
    color_acento VARCHAR(7) DEFAULT '#28a745',
    color_fondo VARCHAR(7) DEFAULT '#f8f9fa',
    color_texto VARCHAR(7) DEFAULT '#212529',
    logo_url VARCHAR(500),
    favicon_url VARCHAR(500),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP
);
```

---

## 🎯 Casos de Uso

### Caso 1: Campaña Presidencial 2026


**Configuración:**
- Nombre: "Campaña Presidencial 2026"
- Tipo: Candidato único
- Color primario: Azul del partido
- Color secundario: Blanco
- Solo tipo de elección "Presidente" habilitado

**Resultado:**
- Testigos solo ven formulario presidencial
- Colores del partido en toda la interfaz
- Datos aislados de otras campañas

### Caso 2: Campaña Partido Completo

**Configuración:**
- Nombre: "Campaña Partido Liberal 2027"
- Tipo: Partido completo
- Múltiples tipos de elección habilitados
- Colores del partido (rojo)

**Resultado:**
- Testigos ven todos los tipos habilitados
- Interfaz con colores del partido
- Datos consolidados por partido

### Caso 3: Reset para Nueva Elección

**Escenario:**
- Campaña anterior completada
- Necesita reutilizar el sistema

**Proceso:**
1. Crear nueva campaña
2. Activar nueva campaña
3. Resetear campaña anterior (opcional)
4. Cargar nuevos datos

---

## ✅ Funcionalidades Implementadas

### Backend

**Endpoints de Campañas:**
- `GET /api/super-admin/campanas` - Listar campañas
- `POST /api/super-admin/campanas` - Crear campaña
- `PUT /api/super-admin/campanas/<id>/activar` - Activar campaña
- `POST /api/super-admin/campanas/<id>/reset` - Resetear datos
- `DELETE /api/super-admin/campanas/<id>` - Eliminar campaña

**Endpoints de Temas:**
- `GET /api/super-admin/temas` - Listar temas
- `POST /api/super-admin/temas` - Crear tema

### Frontend

**Interfaz de Gestión:**
- Tab "Campañas" en Super Admin
- Crear nueva campaña con modal
- Activar/Desactivar campañas
- Reset de datos con confirmación
- Eliminar campañas con confirmación
- Visualización de colores personalizados

---

## 🔒 Seguridad

### Confirmaciones Requeridas

**Reset de Campaña:**
- Requiere escribir "CONFIRMAR_RESET"
- Elimina formularios, incidentes, delitos
- No elimina usuarios ni configuración

**Eliminación de Campaña:**
- Requiere escribir "CONFIRMAR_ELIMINACION"
- No se puede eliminar campaña activa
- Elimina todos los datos asociados

### Validaciones

- Solo una campaña activa a la vez
- No se puede eliminar campaña activa
- Confirmación explícita para acciones destructivas
- Logs de auditoría de todas las acciones

---

## 🎨 Sistema de Temas

### Temas por Rol

**Ejemplo: Testigo**
- Color primario: Verde
- Color secundario: Verde claro
- Enfoque en captura de datos

**Ejemplo: Coordinador**
- Color primario: Azul
- Color secundario: Azul claro
- Enfoque en supervisión

### Temas por Tipo de Elección

**Ejemplo: Presidente**
- Colores institucionales
- Logo presidencial
- Interfaz formal

**Ejemplo: Senado**
- Colores del congreso
- Logo legislativo
- Interfaz corporativa

---

## 📊 Estado Final

**Commit:** `8965fe5`  
**Estado:** ✅ Completamente implementado

**Capacidades:**
- Sistema de campañas ✅
- Multi-tenancy ✅
- Reset de datos ✅
- Temas personalizados ✅
- Colores por rol ✅
- Colores por tipo de elección ✅
- Seguridad robusta ✅

El sistema está listo para manejar múltiples campañas electorales de manera segura y eficiente! 🎉
