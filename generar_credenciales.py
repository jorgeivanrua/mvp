"""
Script para generar documento de credenciales de todos los usuarios
"""
import json
from datetime import datetime

# Leer datos exportados
with open('render_data.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

users_data = data['data']['users']

# Agrupar usuarios por rol
usuarios_por_rol = {}
for user in users_data:
    rol = user['rol']
    if rol not in usuarios_por_rol:
        usuarios_por_rol[rol] = []
    usuarios_por_rol[rol].append(user)

# Generar documento
output = []
output.append("# 🔐 Credenciales de Usuarios - Sistema Electoral")
output.append("")
output.append(f"**Fecha de generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
output.append("")
output.append("**⚠️ IMPORTANTE:** Todas las contraseñas han sido reseteadas a `test123`")
output.append("")
output.append("---")
output.append("")

# URLs
output.append("## 🌐 URLs de Acceso")
output.append("")
output.append("- **Producción (Render):** https://mvp-b9uv.onrender.com/auth/login")
output.append("- **Local (Desarrollo):** http://localhost:5000/auth/login")
output.append("")
output.append("---")
output.append("")

# Resumen
output.append("## 📊 Resumen")
output.append("")
output.append(f"**Total de usuarios:** {len(users_data)}")
output.append("")
for rol, users in sorted(usuarios_por_rol.items()):
    rol_nombre = rol.replace('_', ' ').title()
    output.append(f"- **{rol_nombre}:** {len(users)} usuario(s)")
output.append("")
output.append("---")
output.append("")

# Detalles por rol
output.append("## 👥 Usuarios por Rol")
output.append("")

# Orden de roles
orden_roles = [
    'super_admin',
    'admin_departamental',
    'admin_municipal',
    'coordinador_departamental',
    'coordinador_municipal',
    'coordinador_puesto',
    'auditor_electoral',
    'testigo_electoral'
]

for rol in orden_roles:
    if rol not in usuarios_por_rol:
        continue
    
    users = usuarios_por_rol[rol]
    rol_nombre = rol.replace('_', ' ').title()
    
    output.append(f"### {rol_nombre}")
    output.append("")
    
    for user in users:
        output.append(f"**Usuario:** {user['nombre']}")
        output.append("")
        output.append("```")
        output.append(f"Nombre: {user['nombre']}")
        output.append(f"Rol: {rol}")
        
        if user['ubicacion_info']:
            info = user['ubicacion_info']
            output.append(f"Departamento: {info['departamento_codigo']} - (buscar nombre)")
            output.append(f"Municipio: {info['municipio_codigo']} - (buscar nombre)")
            if info['zona_codigo']:
                output.append(f"Zona: {info['zona_codigo']}")
            if info['puesto_codigo']:
                output.append(f"Puesto: {info['puesto_codigo']}")
        else:
            output.append("Ubicación: Sin ubicación asignada")
        
        output.append("Contraseña: test123")
        output.append("```")
        output.append("")
    
    output.append("---")
    output.append("")

# Instrucciones de uso
output.append("## 📝 Instrucciones de Uso")
output.append("")
output.append("### Para Render (Producción)")
output.append("")
output.append("1. Ir a: https://mvp-b9uv.onrender.com/auth/login")
output.append("2. Seleccionar el rol del usuario")
output.append("3. Seleccionar departamento y municipio según corresponda")
output.append("4. Ingresar contraseña: `test123`")
output.append("")
output.append("### Para Local (Desarrollo)")
output.append("")
output.append("1. Asegurarse de que el servidor esté corriendo: `python run.py`")
output.append("2. Ir a: http://localhost:5000/auth/login")
output.append("3. Seleccionar el rol del usuario")
output.append("4. Seleccionar departamento y municipio según corresponda")
output.append("5. Ingresar contraseña: `test123`")
output.append("")
output.append("---")
output.append("")

# Notas de seguridad
output.append("## ⚠️ Notas de Seguridad")
output.append("")
output.append("- **Esta contraseña es solo para desarrollo y testing**")
output.append("- En producción real, cada usuario debe tener su propia contraseña segura")
output.append("- Las contraseñas están hasheadas con bcrypt en la base de datos")
output.append("- Para cambiar contraseñas en producción, usar el panel de Super Admin")
output.append("")
output.append("---")
output.append("")

# Información adicional
output.append("## 📌 Información Adicional")
output.append("")
output.append("### Departamento Principal")
output.append("- **CAQUETA** (código: 44)")
output.append("  - 16 municipios")
output.append("  - 38 zonas")
output.append("  - 150 puestos de votación")
output.append("  - 196 mesas")
output.append("")
output.append("### Municipio Principal")
output.append("- **FLORENCIA** (código: 01)")
output.append("  - Capital del departamento de Caquetá")
output.append("  - Múltiples zonas y puestos de votación")
output.append("")
output.append("---")
output.append("")

# Contacto y soporte
output.append("## 🆘 Soporte")
output.append("")
output.append("Si tienes problemas para acceder:")
output.append("")
output.append("1. Verifica que estés usando la contraseña correcta: `test123`")
output.append("2. Verifica que hayas seleccionado el departamento y municipio correctos")
output.append("3. Si el problema persiste, ejecuta el script de reseteo:")
output.append("   ```bash")
output.append("   python sync_auto.py")
output.append("   ```")
output.append("")

# Escribir archivo
with open('CREDENCIALES_USUARIOS.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("✅ Documento de credenciales generado: CREDENCIALES_USUARIOS.md")
print(f"📊 Total de usuarios: {len(users_data)}")
print(f"🔑 Contraseña para todos: test123")
