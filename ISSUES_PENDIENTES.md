# Issues Pendientes del Sistema

## 🔴 Críticos (Bloquean funcionalidad principal)

### 1. Formulario E-14 no carga datos de mesa verificada
**Problema**: Cuando el testigo verifica presencia, el formulario E-14 no carga automáticamente los datos de la mesa (votantes registrados, etc.)

**Causa**: La función `showCreateForm()` carga correctamente la mesa, pero puede haber un problema de timing o de carga de datos.

**Solución propuesta**:
- Verificar que `mesaSeleccionadaDashboard` tenga todos los datos necesarios
- Asegurar que `total_votantes_registrados` se cargue correctamente
- Agregar más logs para debugging

**Archivo afectado**: `frontend/static/js/testigo-dashboard-v2.js`

---

### 2. Super Admin: Botones no funcionan
**Problema**: Muchos botones en el dashboard del Super Admin no tienen funcionalidad o no cargan datos.

**Botones afectados**:
- Crear Usuario
- Configurar Sistema
- Exportar Datos
- Crear Respaldo
- Cargar Datos de Prueba
- Auditoría del Sistema

**Causa**: Funciones JavaScript no implementadas o endpoints del backend faltantes.

**Solución propuesta**:
- Implementar funciones JavaScript faltantes
- Crear endpoints del backend necesarios
- O deshabilitar botones que no están implementados

**Archivo afectado**: `frontend/static/js/super-admin-dashboard.js`

---

### 3. No hay interacción con otros roles
**Problema**: Los dashboards de otros roles (Coordinador Municipal, Coordinador Departamental, etc.) no cargan datos o no tienen funcionalidad.

**Roles afectados**:
- Coordinador Municipal
- Coordinador Departamental
- Admin Municipal
- Admin Departamental
- Auditor Electoral

**Causa**: Dashboards no implementados completamente o endpoints faltantes.

**Solución propuesta**:
- Revisar cada dashboard individualmente
- Implementar funcionalidad básica
- Agregar mensajes de "En desarrollo" si no está listo

---

## 🟡 Importantes (Afectan experiencia de usuario)

### 4. Mensajes de error no claros
**Problema**: Cuando hay errores 403 o problemas de autenticación, los mensajes no son claros.

**Solución propuesta**:
- Mejorar mensajes de error en APIClient
- Agregar tooltips explicativos
- Mostrar sugerencias de solución

---

### 5. Validación de formularios incompleta
**Problema**: Los formularios no validan correctamente los datos antes de enviar.

**Solución propuesta**:
- Agregar validación client-side
- Validar que los totales coincidan
- Mostrar errores específicos

---

## 🟢 Mejoras (Nice to have)

### 6. UI/UX inconsistente
**Problema**: Algunos dashboards tienen estilos diferentes, botones en lugares diferentes, etc.

**Solución propuesta**:
- Estandarizar estilos
- Usar componentes reutilizables
- Crear guía de estilos

---

### 7. Falta de feedback visual
**Problema**: Cuando se hacen acciones (guardar, eliminar, etc.), no siempre hay feedback visual claro.

**Solución propuesta**:
- Agregar spinners de carga
- Mostrar mensajes de éxito/error
- Usar animaciones sutiles

---

## 📋 Plan de Acción Recomendado

### Fase 1: Críticos (Esta semana)
1. ✅ Corregir login y autenticación
2. ✅ Corregir creación de usuarios
3. ✅ Resolver conflictos de múltiples pestañas
4. 🔄 Corregir formulario E-14 del testigo
5. 🔄 Implementar funciones básicas del Super Admin

### Fase 2: Importantes (Próxima semana)
1. Implementar dashboards de coordinadores
2. Mejorar mensajes de error
3. Agregar validación de formularios

### Fase 3: Mejoras (Cuando haya tiempo)
1. Estandarizar UI/UX
2. Agregar feedback visual
3. Optimizar rendimiento

---

## 🔧 Debugging Recomendado

### Para Formulario E-14:
```javascript
// En la consola del navegador (F12)
console.log('presenciaVerificada:', presenciaVerificada);
console.log('mesaSeleccionadaDashboard:', mesaSeleccionadaDashboard);
console.log('userLocation:', userLocation);
```

### Para Super Admin:
```javascript
// Verificar qué funciones están definidas
console.log('loadTestData:', typeof loadTestData);
console.log('runSystemAudit:', typeof runSystemAudit);
console.log('exportAllData:', typeof exportAllData);
```

---

## 📝 Notas

- Priorizar funcionalidad sobre estética
- Hacer commits pequeños y frecuentes
- Probar cada cambio antes de hacer push
- Documentar decisiones importantes

---

## ✅ Completados

1. ✅ Login basado en ubicación
2. ✅ Creación de usuarios fijos
3. ✅ Contraseñas simples
4. ✅ Session Manager (deshabilitado)
5. ✅ Documentación de credenciales
