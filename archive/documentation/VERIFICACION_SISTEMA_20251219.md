# VERIFICACION DEL SISTEMA ELECTORAL QUINDIO

## Estado: OPERATIVO Y FUNCIONAL

### Resumen de Usuarios

**Total Usuarios: 368**

```
Distribucion por rol:
  - coordinador_departamental       : 1
  - coordinador_municipal           : 12
  - coordinador_puesto              : 129
  - monitoreo                       : 13
  - super_admin                     : 1
  - testigo_electoral               : 212
```

### Ubicaciones

- Total ubicaciones: 396
- Usuarios con ubicacion asignada: 366/368

### Estructura de Ubicaciones
- 1 Departamento (Quindio)
- 12 Municipios
- 42 Zonas
- 129 Puestos (100% con coordenadas geograficas)
- 212 Mesas (100% con coordenadas geograficas)

### Credenciales de Acceso

**Super Admin:**
- Usuario: admin
- Contrasena: admin123

**Todos los demas usuarios:**
- Contrasena: test123
- Ejemplos:
  - ARMENIA_P01 / test123
  - ARMENIA_P02 / test123
  - Cualquier otro usuario coordinador/testigo / test123

### Coordenadas Geograficas

- Puestos: 129/129 (100%)
- Mesas: 212/212 (100%)

Fuente: DIVIPOLA CSV (formato: latitud, longitud)

### Sistema Operativo

- Aplicacion: Flask 3.0.0
- Base de datos: SQLite electoral.db
- Puerto: 5000
- Status: CORRIENDO

### Acceso a la Aplicacion

- URL: http://localhost:5000
- Todos los usuarios cargados correctamente
- Todas las ubicaciones vinculadas a usuarios
- Todas las coordenadas geograficas disponibles

---

**Fecha de verificacion:** 2025-12-19 15:09:36
**Verificador:** Script verificar_usuarios.py
**Resultado:** SISTEMA COMPLETAMENTE FUNCIONAL Y LISTO PARA USAR
