# 🚀 Inicio Rápido - Sistema Electoral

## ✅ Estado Actual

**Aplicación**: ✅ Corriendo  
**Puerto**: 5000  
**URL**: http://localhost:5000  
**Estado**: Listo para usar

---

## 🔐 Acceso Inmediato

### 1. Abrir el Navegador

Ir a: **http://localhost:5000**

### 2. Iniciar Sesión como Super Admin

**Credenciales**:
- **Usuario**: `super_admin`
- **Contraseña**: `admin123`

### 3. Verificar Dashboard

El dashboard debe mostrar:
- ✅ Estadísticas globales
- ✅ Lista de usuarios
- ✅ Partidos políticos
- ✅ Candidatos
- ✅ Tipos de elección

**Abrir consola del navegador (F12)** y verificar logs:
```
[Super Admin Init Fix] Cargando correcciones...
[Fix] Cargando usuarios...
[Fix] X usuarios recibidos
[Fix] ✓ Usuarios renderizados
[Fix] Cargando partidos...
[Fix] ✓ Partidos renderizados
[Fix] Cargando candidatos...
[Fix] ✓ Candidatos renderizados
```

---

## 📋 Primeros Pasos

### Paso 1: Inicializar Datos Electorales (NUEVO ✨)

1. En el dashboard, ir a la sección **"Testing & Diagnóstico"**
2. Hacer clic en **"Inicializar Datos Electorales"**
3. Confirmar la acción
4. Esperar a que se carguen:
   - 7 Tipos de Elección
   - 10 Partidos Políticos
   - 6 Candidatos de ejemplo

**Resultado**: Sistema configurado con datos básicos en segundos

### Paso 2: Cargar Datos del Caquetá (NUEVO ✨)

1. En la misma sección **"Testing & Diagnóstico"**
2. Hacer clic en **"Cargar Datos del Caquetá"**
3. Confirmar la acción
4. Esperar a que se carguen ~73 candidatos reales:
   - Senado 2022 (~30 candidatos)
   - Cámara Caquetá 2022 (~22 candidatos)
   - Asamblea Departamental 2023 (~21 candidatos)

**Resultado**: Sistema con datos electorales reales del Caquetá

### Paso 3: Cargar Logos de Partidos

1. Ir a la pestaña **"Configuración"**
2. En la sección "Partidos Políticos"
3. Hacer clic en el botón **"Cargar Logos"** (icono de imagen verde)
4. Confirmar la acción
5. Verificar que los logos se cargaron

**Partidos soportados**:
- Partido Liberal
- Partido Conservador
- Centro Democrático
- Pacto Histórico
- Cambio Radical
- Partido de la U
- Alianza Verde
- Polo Democrático
- MIRA
- Comunes

### Paso 4: Verificar Configuración

Ejecutar estas consultas SQL para verificar datos:

```sql
-- Verificar tipos de elección
SELECT * FROM tipos_eleccion WHERE activo = 1;

-- Verificar partidos
SELECT nombre, nombre_corto, activo, logo_url FROM partidos WHERE activo = 1;

-- Verificar candidatos
SELECT c.nombre_completo, p.nombre as partido, t.nombre as tipo_eleccion
FROM candidatos c
JOIN partidos p ON c.partido_id = p.id
JOIN tipos_eleccion t ON c.tipo_eleccion_id = t.id
WHERE c.activo = 1;

-- Verificar usuarios
SELECT nombre, rol, activo FROM users WHERE activo = 1;
```

### Paso 5: Crear Usuarios de Prueba

Si necesitas crear usuarios adicionales:

1. En el dashboard, ir a "Gestión de Usuarios"
2. Hacer clic en "Crear Usuario"
3. Llenar formulario:
   - Nombre
   - Rol
   - Ubicación (si aplica)
   - Contraseña
4. Guardar

---

## 🗺️ Otros Dashboards

### Dashboard de Monitoreo

**URL**: http://localhost:5000/monitoreo/dashboard

**Credenciales**:
- Usuario: `monitoreo`
- Contraseña: `test123`

**Características**:
- Mapa en tiempo real con geolocalización
- Estadísticas globales
- Alertas automáticas
- Gráficos de tendencias

### Dashboard de Testigo

**URL**: http://localhost:5000/testigo/dashboard

**Credenciales**: Depende de los testigos creados

**Características**:
- Ver su mesa asignada
- Crear formularios E-14
- Registrar votos
- Reportar incidentes
- Verificar presencia (GPS)

### Dashboard de Coordinador

**URL**: http://localhost:5000/coordinador/puesto (o municipal, departamental)

**Credenciales**: Depende de los coordinadores creados

**Características**:
- Ver formularios de su jurisdicción
- Validar E-14
- Ver consolidado en tabla automática
- Generar E-24
- Gestionar incidentes

---

## 📚 Documentación Disponible

### Para Comenzar
1. **INICIO_RAPIDO.md** (este documento)
2. **CHECKLIST_SUPER_ADMIN.md** - Lista de verificación
3. **INDICE_DOCUMENTACION.md** - Índice completo

### Para Entender el Sistema
1. **ARQUITECTURA.md** - Arquitectura completa
2. **ROLES_Y_FLUJOS.md** - 7 roles y flujos
3. **TIPOS_ELECCIONES_COLOMBIA.md** - Tipos de elecciones
4. **FLUJO_DATOS_ELECTORALES.md** - Flujo de datos

### Para Configurar
1. **CHECKLIST_SUPER_ADMIN.md** - Paso a paso
2. **GUIA_LOGOS_PARTIDOS.md** - Gestión de logos
3. **VERIFICACION_FLUJO_COMPLETO.md** - Verificación exhaustiva

### Para Resolver Problemas
1. **TROUBLESHOOTING.md** - Problemas comunes
2. **SEGURIDAD.md** - Seguridad del sistema

---

## 🔍 Verificación Rápida

### Checklist de 5 Minutos

- [ ] Aplicación corriendo en http://localhost:5000
- [ ] Login como super_admin funciona
- [ ] Hacer clic en "Inicializar Datos Electorales"
- [ ] Hacer clic en "Cargar Datos del Caquetá"
- [ ] Dashboard muestra 10 partidos
- [ ] Dashboard muestra ~79 candidatos (6 básicos + 73 del Caquetá)
- [ ] Dashboard muestra 7 tipos de elección
- [ ] Dashboard muestra usuarios
- [ ] No hay errores en consola del navegador (F12)

### Si algo no funciona

1. **Verificar que la aplicación está corriendo**:
   ```powershell
   netstat -ano | Select-String ":5000"
   ```

2. **Ver logs del servidor**:
   - Revisar la terminal donde está corriendo
   - Buscar errores en rojo

3. **Consultar documentación**:
   - Ver `TROUBLESHOOTING.md`
   - Ver `VERIFICACION_FLUJO_COMPLETO.md`

---

## 🎯 Próximos Pasos

1. ✅ Verificar que todo funciona
2. ✅ Inicializar datos electorales (1 clic)
3. ✅ Cargar datos del Caquetá (1 clic)
4. ⏳ Cargar logos de partidos (1 clic)
5. ⏳ Crear usuarios de prueba
6. ⏳ Hacer pruebas completas

**Tiempo estimado de configuración inicial**: 5 minutos

---

**Última actualización**: 30 de Noviembre de 2025  
**Versión**: 1.0  
**Estado**: ✅ Sistema Listo

**URL de acceso**: http://localhost:5000  
**Usuario**: super_admin  
**Contraseña**: admin123
