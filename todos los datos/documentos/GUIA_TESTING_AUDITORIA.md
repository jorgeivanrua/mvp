# 🧪 Guía de Testing y Auditoría del Sistema Electoral

**Fecha:** 2025-11-14  
**Versión:** 2.0 - Sistema Completo de Auditoría Automatizada

---

## 📋 Descripción

Sistema completo de testing y auditoría que permite verificar todas las funcionalidades del sistema electoral con datos de prueba precargados y pruebas automatizadas.

---

## 🎯 Objetivo

Realizar una auditoría completa del sistema verificando:
- ✅ Funcionalidad de todos los roles
- ✅ Seguridad y permisos
- ✅ Flujos de trabajo completos
- ✅ Integridad de datos
- ✅ Rendimiento y estabilidad

---

## 🚀 Inicio Rápido

### 1. Cargar Datos de Prueba Completos

```bash
# Instalar dependencia para colores en consola
pip install colorama

# Cargar datos completos (usuarios, ubicaciones, partidos, formularios, incidentes)
python backend/scripts/load_complete_test_data.py
```

### 2. Ejecutar Auditoría Automatizada

```bash
# Asegúrate de que el servidor esté corriendo
python run.py

# En otra terminal, ejecutar las pruebas
python backend/tests/test_audit_system.py
```

---

## 📦 Datos de Prueba Cargados

### 👥 Usuarios (Todos los Roles)

| Usuario | Contraseña | Rol | Ubicación |
|---------|------------|-----|-----------|
| `admin_test` | `test123` | Super Admin | - |
| `auditor_test` | `test123` | Auditor Electoral | - |
| `coord_dept_test` | `test123` | Coordinador Departamental | Departamento Test |
| `coord_mun_test` | `test123` | Coordinador Municipal | Municipio Test |
| `coord_puesto_test_1` | `test123` | Coordinador Puesto | Puesto 1 |
| `coord_puesto_test_2` | `test123` | Coordinador Puesto | Puesto 2 |
| `coord_puesto_test_3` | `test123` | Coordinador Puesto | Puesto 3 |
| `testigo_test_1` a `testigo_test_15` | `test123` | Testigo Electoral | Mesas 1-15 |

### 📍 Ubicaciones (DIVIPOLA)
- **1 Departamento:** "Departamento Test"
- **1 Municipio:** "Municipio Test"
- **3 Puestos:** "Puesto de Votación 1, 2, 3"
- **15 Mesas:** 5 mesas por puesto

### 🗳️ Configuración Electoral

**Tipos de Elección:**
- Presidente de la República (uninominal, permite coaliciones)
- Senado de la República (lista cerrada/abierta, permite coaliciones)
- Cámara de Representantes (lista cerrada)
- Gobernador (uninominal, permite coaliciones)

**Partidos Políticos:**
- Partido Liberal (PL) - Rojo
- Partido Conservador (PC) - Azul
- Partido Verde (PV) - Verde
- Partido de la U (PU) - Amarillo
- Centro Democrático (CD) - Naranja
- Polo Democrático (PP) - Magenta

**Candidatos:**
- 6 Candidatos presidenciales (1 por partido)
- 30 Candidatos de Senado (5 por partido)
- 18 Candidatos de Cámara (3 por partido)
- **Total: 54 candidatos**

### 📝 Formularios E-14
- 10 formularios E-14 creados
- 8 formularios enviados
- 2 formularios en borrador
- Votos distribuidos aleatoriamente entre partidos

### ⚠️ Incidentes y Delitos
- 5 incidentes electorales (varios tipos y gravedades)
- 3 delitos electorales (gravedad alta/crítica)
- Estados: reportado, en revisión

### 📋 Logs de Auditoría
- 20 logs de acciones del sistema
- Incluye: login, logout, creación de formularios, etc.

### 📬 Notificaciones
- 10 notificaciones de prueba
- 5 leídas, 5 sin leer
- Varios niveles de prioridad

### 📅 Campaña
- **Nombre:** "Campaña Electoral Test 2024"
- **Estado:** Activa
- **Colores:** Naranja (#FF5722) y Amarillo (#FFC107)
- **Tipo:** Partido completo

---

## 🧪 Sistema de Pruebas Automatizadas

### Pruebas Implementadas

#### 1. Super Admin
- ✅ Login y autenticación
- ✅ Acceso al dashboard
- ✅ Listar usuarios
- ✅ Crear nuevo usuario
- ✅ Actualizar usuario
- ✅ Gestión de campañas
- ✅ Configuración electoral
- ✅ Estadísticas globales

#### 2. Testigo Electoral
- ✅ Login y autenticación
- ✅ Verificación de presencia
- ✅ Acceso al dashboard
- ✅ Crear formulario E-14
- ✅ Enviar formulario
- ✅ Reportar incidente
- ✅ Ver historial de formularios

#### 3. Coordinador de Puesto
- ✅ Login y autenticación
- ✅ Acceso al dashboard
- ✅ Ver formularios pendientes
- ✅ Consolidar E-24 Puesto
- ✅ Ver incidentes del puesto
- ✅ Estadísticas del puesto

#### 4. Coordinador Municipal
- ✅ Login y autenticación
- ✅ Acceso al dashboard
- ✅ Ver consolidados de puestos
- ✅ Consolidar E-24 Municipal
- ✅ Ver incidentes municipales
- ✅ Enviar notificaciones

#### 5. Coordinador Departamental
- ✅ Login y autenticación
- ✅ Acceso al dashboard
- ✅ Ver consolidados municipales
- ✅ Consolidar reporte departamental
- ✅ Estadísticas departamentales

#### 6. Auditor Electoral
- ✅ Login y autenticación
- ✅ Acceso al dashboard de auditoría
- ✅ Ver logs de auditoría
- ✅ Ver todos los formularios
- ✅ Ver incidentes y delitos
- ✅ Generar reportes

#### 7. Seguridad y Permisos
- ✅ Acceso denegado sin autenticación
- ✅ Testigo no puede acceder a funciones de admin
- ✅ Login rechazado con credenciales incorrectas
- ✅ Protección contra inyección SQL básica

---

## 📊 Interpretación de Resultados

### Colores en la Consola

- 🟢 **Verde (✅):** Prueba exitosa
- 🔴 **Rojo (❌):** Prueba fallida
- 🟡 **Amarillo (⚠️):** Advertencia (funcionalidad opcional no disponible)
- 🔵 **Cyan (ℹ️):** Información

### Resumen Final

Al final de la ejecución verás:
```
═══════════════════════════════════════════════════════════
  RESUMEN DE AUDITORÍA
═══════════════════════════════════════════════════════════

✅ Pruebas exitosas: XX
❌ Pruebas fallidas: XX
⚠️  Advertencias: XX

📊 Tasa de éxito: XX.X%
```

**Criterio de Éxito:** Tasa de éxito >= 90%

---

## 🔧 Pruebas Manuales Complementarias

### Testing como Super Admin

**Pasos:**
1. Login con `admin_test / test123`
2. Verificar dashboard principal
3. **Gestión de Usuarios:**
   - Crear nuevo usuario
   - Editar usuario existente
   - Desactivar/activar usuario
   - Cambiar contraseña
4. **Gestión de Ubicaciones:**
   - Ver estructura DIVIPOLA
   - Crear nueva ubicación
   - Editar ubicación
5. **Gestión de Partidos:**
   - Crear nuevo partido
   - Editar partido
   - Activar/desactivar partido
6. **Gestión de Candidatos:**
   - Crear nuevo candidato
   - Asignar a partido
   - Configurar número de lista
7. **Carga Masiva:**
   - Descargar plantilla Excel
   - Cargar datos desde Excel
   - Verificar importación

### Testing como Testigo

**Pasos:**
1. Login con `testigo_test_1 / test123`
2. **Verificar Presencia:**
   - Hacer clic en "Verificar Presencia"
   - Confirmar verificación
3. **Crear Formulario E-14:**
   - Llenar datos de votación
   - Agregar votos por partido
   - Agregar votos por candidato
   - Guardar como borrador
4. **Enviar Formulario:**
   - Revisar datos
   - Enviar formulario
   - Verificar confirmación
5. **Reportar Incidente:**
   - Seleccionar tipo de incidente
   - Describir situación
   - Adjuntar evidencia (opcional)
   - Enviar reporte
6. **Modo Offline:**
   - Desconectar internet
   - Crear formulario
   - Verificar que se guarda localmente
   - Reconectar y verificar sincronización

### Testing como Coordinador de Puesto

**Pasos:**
1. Login con `coord_puesto_test_1 / test123`
2. **Ver Formularios:**
   - Listar formularios del puesto
   - Filtrar por estado
   - Ver detalles de formulario
3. **Validar Formulario:**
   - Seleccionar formulario pendiente
   - Revisar datos
   - Aprobar formulario
4. **Rechazar Formulario:**
   - Seleccionar formulario con error
   - Agregar comentario
   - Rechazar formulario
5. **Consolidar E-24 Puesto:**
   - Verificar que todas las mesas reportaron
   - Generar consolidado
   - Revisar totales
6. **Gestionar Incidentes:**
   - Ver incidentes del puesto
   - Actualizar estado
   - Agregar seguimiento

### Testing como Coordinador Municipal

**Pasos:**
1. Login con `coord_mun_test / test123`
2. **Ver Puestos:**
   - Listar puestos del municipio
   - Ver estado de cada puesto
   - Ver porcentaje de avance
3. **Consolidar E-24 Municipal:**
   - Verificar consolidados de puestos
   - Generar consolidado municipal
   - Revisar totales
4. **Enviar Notificaciones:**
   - Seleccionar destinatarios
   - Escribir mensaje
   - Enviar notificación
5. **Ver Estadísticas:**
   - Gráficos por puesto
   - Comparativas
   - Exportar datos

### Testing como Auditor

**Pasos:**
1. Login con `auditor_test / test123`
2. **Dashboard de Auditoría:**
   - Ver resumen general
   - Verificar métricas clave
3. **Logs de Auditoría:**
   - Filtrar por usuario
   - Filtrar por acción
   - Filtrar por fecha
   - Exportar logs
4. **Auditar Formularios:**
   - Ver todos los formularios
   - Identificar discrepancias
   - Generar reporte de inconsistencias
5. **Analizar Incidentes:**
   - Ver mapa de incidentes
   - Filtrar por gravedad
   - Generar reporte de incidentes

---

## 🔒 Verificación de Seguridad

### Checklist de Seguridad

- [ ] **Autenticación:**
  - [ ] No se puede acceder sin login
  - [ ] Tokens JWT expiran correctamente
  - [ ] Logout invalida el token
  
- [ ] **Autorización:**
  - [ ] Cada rol solo accede a sus funciones
  - [ ] Testigo no puede ver datos de otros testigos
  - [ ] Coordinadores solo ven su jurisdicción
  
- [ ] **Validación de Datos:**
  - [ ] Formularios validan datos requeridos
  - [ ] No se aceptan valores negativos
  - [ ] Totales se calculan correctamente
  
- [ ] **Protección contra Ataques:**
  - [ ] Protección contra SQL Injection
  - [ ] Protección contra XSS
  - [ ] Protección contra CSRF
  - [ ] Rate limiting en endpoints críticos
  
- [ ] **Auditoría:**
  - [ ] Todas las acciones se registran
  - [ ] Logs incluyen usuario, acción, timestamp
  - [ ] Logs no se pueden modificar

---

## 📈 Métricas de Rendimiento

### Tiempos de Respuesta Esperados

| Endpoint | Tiempo Esperado | Tiempo Máximo |
|----------|----------------|---------------|
| Login | < 500ms | 1s |
| Dashboard | < 1s | 2s |
| Listar formularios | < 1s | 3s |
| Crear formulario | < 500ms | 1s |
| Consolidar E-24 | < 2s | 5s |
| Generar reporte | < 3s | 10s |

### Carga del Sistema

- **Usuarios concurrentes:** Hasta 100
- **Formularios por segundo:** Hasta 10
- **Tamaño de base de datos:** Hasta 10GB
- **Tiempo de backup:** < 5 minutos

---

## 🐛 Troubleshooting

### Error: "No se puede conectar al servidor"

**Solución:**
```bash
# Verificar que el servidor esté corriendo
curl http://localhost:5000

# Si no responde, iniciar el servidor
python run.py
```

### Error: "Credenciales incorrectas"

**Solución:**
1. Verificar que los datos de prueba se cargaron:
   ```bash
   python backend/scripts/load_complete_test_data.py
   ```
2. Verificar usuario y contraseña: `admin_test / test123`

### Error: "Algunos tests fallan"

**Solución:**
1. Revisar logs del servidor
2. Verificar que todos los endpoints estén implementados
3. Verificar que la base de datos tenga datos
4. Revisar el código de error específico

### Error: "ModuleNotFoundError: colorama"

**Solución:**
```bash
pip install colorama
```

---

## 📝 Checklist de Auditoría Completa

### Preparación
- [ ] Base de datos limpia
- [ ] Servidor corriendo
- [ ] Datos de prueba cargados
- [ ] Dependencias instaladas

### Pruebas Automatizadas
- [ ] Ejecutar `test_audit_system.py`
- [ ] Tasa de éxito >= 90%
- [ ] Documentar errores encontrados

### Pruebas Manuales por Rol
- [ ] Super Admin: Todas las funcionalidades
- [ ] Auditor: Visualización y reportes
- [ ] Coordinador Departamental: Consolidado
- [ ] Coordinador Municipal: Gestión de puestos
- [ ] Coordinador Puesto: Validación de formularios
- [ ] Testigo: Captura de datos

### Seguridad
- [ ] Verificar autenticación
- [ ] Verificar autorización
- [ ] Verificar validación de datos
- [ ] Verificar protección contra ataques

### Rendimiento
- [ ] Medir tiempos de respuesta
- [ ] Probar con múltiples usuarios
- [ ] Verificar uso de memoria
- [ ] Verificar uso de CPU

### Documentación
- [ ] Documentar resultados
- [ ] Documentar bugs encontrados
- [ ] Documentar mejoras sugeridas
- [ ] Generar reporte final

---

## ✅ Reporte de Auditoría

### Plantilla de Reporte

```markdown
# Reporte de Auditoría - [Fecha]

## Resumen Ejecutivo
- Tasa de éxito: XX%
- Pruebas ejecutadas: XX
- Pruebas exitosas: XX
- Pruebas fallidas: XX
- Advertencias: XX

## Bugs Encontrados
1. [Descripción del bug]
   - Severidad: Alta/Media/Baja
   - Pasos para reproducir
   - Comportamiento esperado
   - Comportamiento actual

## Mejoras Sugeridas
1. [Descripción de la mejora]
   - Prioridad: Alta/Media/Baja
   - Beneficio esperado

## Conclusiones
[Conclusiones generales de la auditoría]

## Recomendaciones
[Recomendaciones para el equipo de desarrollo]
```

---

## 🎓 Mejores Prácticas

### Antes de Testing
1. ✅ Crear backup de la base de datos
2. ✅ Usar una base de datos de desarrollo
3. ✅ No usar en producción
4. ✅ Documentar el plan de testing

### Durante Testing
1. ✅ Probar cada funcionalidad sistemáticamente
2. ✅ Documentar cualquier error encontrado
3. ✅ Verificar en diferentes navegadores
4. ✅ Probar en modo offline
5. ✅ Tomar capturas de pantalla de errores

### Después de Testing
1. ✅ Ejecutar auditoría final
2. ✅ Limpiar datos de prueba si es necesario
3. ✅ Documentar resultados
4. ✅ Reportar bugs encontrados
5. ✅ Generar reporte de auditoría

---

## 📚 Recursos Adicionales

### Scripts Disponibles

- `backend/scripts/load_complete_test_data.py` - Carga datos completos
- `backend/tests/test_audit_system.py` - Pruebas automatizadas
- `backend/scripts/load_test_data.py` - Carga datos básicos (legacy)

### Documentación Relacionada

- `SISTEMA_CAMPANAS_MULTITENANCY.md` - Sistema de campañas
- `MODELO_ELECTORAL_COLOMBIANO.md` - Modelo electoral
- `GUIA_CARGA_MASIVA_SUPER_ADMIN.md` - Carga masiva de datos

---

## ✅ Conclusión

El sistema de testing y auditoría automatizada permite verificar de manera completa y sistemática todas las funcionalidades del sistema electoral. Con datos de prueba precargados, usuarios para cada rol, y pruebas automatizadas, es posible realizar testing exhaustivo antes de desplegar en producción.

**Ventajas del Sistema:**
- ✅ Pruebas automatizadas (ahorra tiempo)
- ✅ Datos realistas precargados
- ✅ Cobertura completa de roles
- ✅ Verificación de seguridad
- ✅ Reportes detallados con colores
- ✅ Fácil de ejecutar

---

**Estado:** ✅ Completamente implementado  
**Versión:** 2.0  
**Última actualización:** 2025-11-14  
**Próximo paso:** Ejecutar auditoría completa y documentar resultados
