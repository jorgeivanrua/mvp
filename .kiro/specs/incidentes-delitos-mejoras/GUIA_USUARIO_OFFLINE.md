# Guía de Usuario: Trabajo Offline

## 🌐 ¿Qué es el Modo Offline?

El sistema electoral ahora puede funcionar **sin conexión a internet**. Esto significa que puedes:

- ✅ Completar formularios E-14 y E-24
- ✅ Reportar incidentes y delitos
- ✅ Tomar fotos de evidencia
- ✅ Todo se guarda localmente y se sincroniza automáticamente cuando hay conexión

## 📱 ¿Cómo Funciona?

### Cuando Pierdes la Conexión

1. **Verás un mensaje**: "Modo Offline - Sin conexión"
2. **Un indicador rojo** aparecerá en la parte superior
3. **Puedes seguir trabajando** normalmente
4. **Tus datos se guardan** en tu dispositivo

### Cuando Recuperas la Conexión

1. **Verás un mensaje**: "Conexión restablecida. Sincronizando..."
2. **El sistema sincroniza automáticamente** todos los datos guardados
3. **Recibirás una confirmación** cuando termine

## 🎯 Casos de Uso

### Testigo Electoral

**Situación**: Estás en una mesa de votación en zona rural sin señal.

**Qué hacer**:
1. Completa el formulario E-14 para cada tipo de elección
   - Ejemplo: E-14 para Presidente
   - Ejemplo: E-14 para Diputados
   - Ejemplo: E-14 para Alcalde
2. Toma **todas las fotos necesarias** del acta (pueden ser varias páginas)
3. Presiona "Enviar" en cada formulario
4. Verás: "⚠️ Sin conexión. Formulario guardado localmente"
5. Cuando llegues a zona con señal, todos los formularios se enviarán automáticamente

**Importante**: 
- Cada tipo de elección tiene su propio E-14
- Puedes tomar múltiples fotos por acta (si tiene varias páginas)
- El sistema identifica automáticamente mesa + tipo de elección

### Coordinador de Puesto

**Situación**: Hay un corte de luz y se cayó el internet.

**Qué hacer**:
1. Continúa recibiendo formularios E-14 de los testigos
2. Genera el formulario E-24 consolidado
3. Todo se guarda localmente
4. Cuando vuelva la conexión, todo se sincroniza

### Reportar Incidentes

**Situación**: Necesitas reportar un incidente urgente pero no hay señal.

**Qué hacer**:
1. Abre el formulario de incidentes
2. Completa todos los campos
3. Toma fotos si es necesario
4. Envía el reporte
5. Se guardará localmente y se enviará cuando haya conexión

## 📊 Panel de Reportes Pendientes

### Ubicación
Esquina inferior izquierda de la pantalla

### Qué Muestra
- **Número de reportes pendientes**: Badge naranja con contador
- **Lista detallada**: Tipo, título y tiempo transcurrido
- **Estado**: Icono giratorio durante sincronización

### Acciones Disponibles
- **Expandir/Colapsar**: Click en el panel
- **Sincronizar Ahora**: Botón para forzar sincronización
- **Ver Detalles**: Click en cada reporte

## 🔄 Panel de Sincronización

### Ubicación
Esquina inferior derecha de la pantalla

### Qué Muestra
- **Pendientes**: Reportes esperando sincronización
- **Sincronizados**: Reportes ya enviados al servidor
- **Evidencia**: Fotos guardadas offline

### Acciones Disponibles
- **Sincronizar Ahora**: Fuerza sincronización inmediata
- **Limpiar Sincronizados**: Elimina datos ya enviados (libera espacio)
- **Ver Log**: Historial de sincronizaciones

## 💡 Consejos y Buenas Prácticas

### ✅ Hacer

1. **Verifica el indicador de conexión** antes de trabajar
2. **Revisa los reportes pendientes** regularmente
3. **Sincroniza manualmente** antes de reuniones importantes
4. **Mantén el navegador abierto** durante la sincronización
5. **Toma fotos de buena calidad** (se comprimen automáticamente)

### ❌ Evitar

1. **No cierres el navegador** si hay reportes pendientes
2. **No borres los datos del navegador** sin sincronizar
3. **No uses modo incógnito** (no guarda datos offline)
4. **No reportes el mismo incidente** múltiples veces
5. **No apagues el dispositivo** durante sincronización

## 🚨 Solución de Problemas

### "No se puede sincronizar"

**Posibles causas**:
- No hay conexión a internet
- Token de sesión expirado
- Servidor no disponible

**Solución**:
1. Verifica tu conexión a internet
2. Intenta sincronizar manualmente
3. Si persiste, cierra sesión y vuelve a iniciar
4. Contacta soporte técnico

### "Espacio de almacenamiento lleno"

**Solución**:
1. Abre el panel de sincronización
2. Click en "Limpiar Sincronizados"
3. Esto elimina datos ya enviados al servidor
4. Libera espacio para nuevos reportes

### "Reporte duplicado"

**Causa**: Enviaste el mismo reporte online y offline

**Prevención**:
- Espera la confirmación antes de reenviar
- Revisa los reportes pendientes
- No uses el botón "Atrás" del navegador

### "Fotos no se suben"

**Posibles causas**:
- Fotos muy grandes
- Conexión lenta
- Límite de tamaño excedido

**Solución**:
1. El sistema comprime automáticamente
2. Si falla, intenta con menos fotos
3. Verifica tu conexión
4. Intenta sincronizar manualmente

## 📱 Indicadores Visuales

### 🔴 Rojo - Sin Conexión
- **Ubicación**: Parte superior derecha
- **Significado**: No hay internet
- **Acción**: Puedes seguir trabajando, se guardará localmente

### 🟢 Verde - Conectado
- **Ubicación**: Aparece brevemente al reconectar
- **Significado**: Conexión restaurada
- **Acción**: Sincronización automática en progreso

### 🟠 Naranja - Pendientes
- **Ubicación**: Badge en panel de reportes
- **Significado**: Hay reportes sin sincronizar
- **Acción**: Se sincronizarán automáticamente

### 🔵 Azul - Sincronizando
- **Ubicación**: Icono giratorio
- **Significado**: Sincronización en progreso
- **Acción**: Espera a que termine

## 📋 Checklist Diario

### Al Iniciar el Día
- [ ] Verificar conexión a internet
- [ ] Revisar reportes pendientes del día anterior
- [ ] Sincronizar manualmente si hay pendientes
- [ ] Verificar espacio de almacenamiento

### Durante el Día
- [ ] Monitorear indicador de conexión
- [ ] Revisar panel de pendientes cada hora
- [ ] Sincronizar manualmente en zonas con buena señal
- [ ] Tomar fotos de evidencia inmediatamente

### Al Finalizar el Día
- [ ] Sincronizar todos los reportes pendientes
- [ ] Verificar que no queden pendientes
- [ ] Limpiar datos sincronizados si es necesario
- [ ] Reportar problemas técnicos

## 🎓 Preguntas Frecuentes

### ¿Cuánto espacio usa el almacenamiento offline?
Depende de las fotos. Un formulario sin fotos usa ~5KB. Con fotos puede ser 1-5MB por reporte.

### ¿Por qué veo varios E-14 de la misma mesa?
Porque cada tipo de elección tiene su propio formulario E-14. Por ejemplo:
- Mesa 001-A → E-14 Presidente
- Mesa 001-A → E-14 Diputados
- Mesa 001-A → E-14 Alcalde

Esto es normal y correcto. El sistema los identifica claramente para evitar confusiones.

### ¿Cuántos reportes puedo guardar offline?
Depende del espacio disponible en tu dispositivo. Típicamente 100-500 reportes con fotos.

### ¿Qué pasa si cierro el navegador con reportes pendientes?
Los datos se mantienen. Al abrir nuevamente, se sincronizarán automáticamente.

### ¿Puedo usar múltiples dispositivos?
Sí, pero cada dispositivo sincroniza independientemente. No compartas la misma sesión.

### ¿Los datos offline están seguros?
Sí, están encriptados por el navegador y solo accesibles con tu sesión.

### ¿Cuánto tiempo se guardan los datos offline?
Los datos sincronizados se limpian automáticamente después de 7 días.

### ¿Puedo trabajar offline en cualquier navegador?
Funciona en navegadores modernos (Chrome, Firefox, Safari, Edge). No en Internet Explorer.

### ¿Qué pasa si hay un error durante la sincronización?
El sistema reintenta automáticamente hasta 3 veces. Si falla, el reporte queda pendiente.

## 📞 Soporte

Si tienes problemas:

1. **Revisa esta guía** primero
2. **Intenta sincronizar manualmente**
3. **Captura pantalla** del error
4. **Contacta soporte técnico** con:
   - Descripción del problema
   - Captura de pantalla
   - Número de reportes pendientes
   - Tipo de dispositivo y navegador

## 🎯 Resumen Rápido

| Situación | Qué Hacer |
|-----------|-----------|
| Sin conexión | Trabaja normal, se guarda localmente |
| Conexión restaurada | Espera sincronización automática |
| Reportes pendientes | Revisa panel inferior izquierdo |
| Sincronización lenta | Espera o intenta en mejor zona |
| Error de sincronización | Intenta manualmente o contacta soporte |
| Espacio lleno | Limpia datos sincronizados |

---

**Recuerda**: El sistema está diseñado para que trabajes sin preocuparte por la conexión. ¡Confía en la sincronización automática!

**Última actualización**: Diciembre 2024
